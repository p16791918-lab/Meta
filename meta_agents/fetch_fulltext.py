"""
Full-text retrieval (runs BETWEEN Phase 1 and Phase 2 screening)
================================================================
Only studies that PASS Phase 1 (title/abstract) reach here. For each one we
try to obtain the full text, in priority order:

  1) Local file  fulltext/<pmid>.(txt|md|pdf)   ← YOU supply these
       e.g. paywalled papers you downloaded via institutional (school) access.
       Save each PDF as  fulltext/<PMID>.pdf
  2) PMC open-access full text via Entrez        ← automatic (OA papers only)

Studies with neither are flagged "NOT RETRIEVED" and listed in
`fulltext_needed.csv` so you know exactly which PDFs to pull from your library.
"""
from __future__ import annotations

import csv
import os
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple

# Cap on how much full text to keep (chars). Long enough for methods/results,
# short enough to stay within a single claude CLI call.
MAX_FULLTEXT_CHARS = 40000


# ─────────────────────────────────────────────────────────────────────────────
# 1) Local files (user-supplied, e.g. paywalled via institution)
# ─────────────────────────────────────────────────────────────────────────────

def _read_local(pmid: str, fulltext_dir: str) -> Tuple[Optional[str], Optional[str]]:
    """Return (text, source) from fulltext/<pmid>.(txt|md|pdf) or (None, None)."""
    for ext in ("txt", "md"):
        p = Path(fulltext_dir) / f"{pmid}.{ext}"
        if p.is_file():
            return p.read_text(encoding="utf-8", errors="ignore"), f"local_{ext}"

    pdf = Path(fulltext_dir) / f"{pmid}.pdf"
    if pdf.is_file():
        text = _pdf_to_text(pdf)
        if text:
            return text, "local_pdf"
    return None, None


def _pdf_to_text(path: Path) -> Optional[str]:
    """Extract text from a PDF using pypdf (or PyPDF2 as fallback)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            print(f"[FullText] ⚠ pypdf not installed; cannot parse {path.name}. "
                  f"Run: pip install pypdf")
            return None
    try:
        reader = PdfReader(str(path))
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    except Exception as e:  # noqa: BLE001
        print(f"[FullText] ⚠ failed to parse {path.name}: {e}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# 2) PMC open-access full text via Entrez
# ─────────────────────────────────────────────────────────────────────────────

def _fetch_pmc(pmid: str, email: Optional[str],
               api_key: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
    """Fetch OA full text from PubMed Central. Returns (text, 'pmc_oa') or (None, None)."""
    try:
        from Bio import Entrez
    except ImportError:
        return None, None

    Entrez.email = email or os.getenv("NCBI_EMAIL", "researcher@example.com")
    key = api_key or os.getenv("NCBI_API_KEY", "")
    if key:
        Entrez.api_key = key

    import time
    last_err = None
    for attempt in range(3):  # retry transient NCBI errors (EOF / rate spikes)
        try:
            # PMID → PMCID
            h = Entrez.elink(dbfrom="pubmed", db="pmc", id=str(pmid))
            rec = Entrez.read(h)
            h.close()
            pmcid = None
            for linkset in rec:
                for db in linkset.get("LinkSetDb", []):
                    for link in db.get("Link", []):
                        pmcid = link["Id"]
                        break
            if not pmcid:
                return None, None  # genuinely not in PMC — don't retry

            # Fetch full-text XML (only the OA subset returns a real body)
            h = Entrez.efetch(db="pmc", id=pmcid, rettype="full", retmode="xml")
            xml = h.read()
            h.close()
            if isinstance(xml, bytes):
                xml = xml.decode("utf-8", errors="ignore")

            text = _xml_to_text(xml)
            if text and len(text) > 500:
                return text, "pmc_oa"
            return None, None
        except Exception as e:  # noqa: BLE001  (transient network/NCBI error)
            last_err = e
            if attempt < 2:
                time.sleep(1.5 * (attempt + 1))  # 1.5s, 3s backoff

    print(f"[FullText] ⚠ PMC fetch failed for PMID {pmid} after retries: {last_err}")
    return None, None


def _xml_to_text(xml: str) -> str:
    """Crudely strip a PMC JATS XML document down to readable body text."""
    m = re.search(r"<body[ >].*?</body>", xml, flags=re.S)
    chunk = m.group(0) if m else xml
    chunk = re.sub(r"<[^>]+>", " ", chunk)       # strip tags
    chunk = re.sub(r"&[a-zA-Z#0-9]+;", " ", chunk)  # strip entities
    chunk = re.sub(r"\s+", " ", chunk).strip()
    return chunk


# ─────────────────────────────────────────────────────────────────────────────
# Public API
# ─────────────────────────────────────────────────────────────────────────────

def fetch_fulltext(
    studies: List[Dict],
    fulltext_dir: str = "fulltext",
    use_pmc: bool = True,
    ncbi_email: Optional[str] = None,
    ncbi_api_key: Optional[str] = None,
) -> List[Dict]:
    """
    Attach full text to each Phase-1-passed study.

    Each returned study gains two keys:
      - "fulltext":        the retrieved text (capped) or None
      - "fulltext_source": "local_pdf" | "local_txt" | "local_md" | "pmc_oa" | None
    """
    os.makedirs(fulltext_dir, exist_ok=True)
    print(f"[FullText] Retrieving full text for {len(studies)} Phase-1-passed studies...")
    print(f"[FullText] Local dir: {fulltext_dir}/  "
          f"(drop institution PDFs here as <PMID>.pdf)")

    out: List[Dict] = []
    for s in studies:
        raw_pmid = str(s.get("pmid", "")).strip()
        # Some Embase records store "12345678; http://.../12345678" — use just
        # the numeric PMID for file names / lookups so disk caching works and
        # resumed runs don't re-download.
        m = re.match(r"\d+", raw_pmid)
        pmid = m.group() if m else ""
        text, source = (None, None)

        if pmid:
            text, source = _read_local(pmid, fulltext_dir)
        if text is None and use_pmc and pmid:
            text, source = _fetch_pmc(pmid, ncbi_email, ncbi_api_key)
            if text:
                # Cache the fetched OA text to disk so a resumed run does not
                # re-download it (the retrieval step is slow, not token-costed).
                try:
                    Path(fulltext_dir, f"{pmid}.txt").write_text(text, encoding="utf-8")
                except OSError:
                    pass

        if text:
            text = text[:MAX_FULLTEXT_CHARS]

        s2 = dict(s)
        s2["fulltext"] = text
        s2["fulltext_source"] = source
        out.append(s2)
        print(f"[FullText]  PMID {pmid or '—'}: {source or 'NOT RETRIEVED'}")

    n_ok = sum(1 for s in out if s["fulltext_source"])
    print(f"[FullText] ✓ {n_ok}/{len(out)} with full text | "
          f"{len(out) - n_ok} without (screened on abstract where available; "
          f"only INCLUDED ones will need a PDF)")
    return out


def write_retrieval_report(studies: List[Dict], path: str) -> int:
    """
    Write a CSV listing studies that still need a manually downloaded PDF
    (paywalled / not in PMC). Returns the number of such studies.
    """
    need = [s for s in studies if not s.get("fulltext_source")]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["pmid", "title", "year", "journal", "action", "save_as"])
        for s in need:
            pmid = str(s.get("pmid", "")).strip()
            w.writerow([
                pmid,
                s.get("title", ""),
                s.get("year", ""),
                s.get("journal", ""),
                "Download PDF via institutional (school) access",
                f"fulltext/{pmid or 'UNKNOWN'}.pdf",
            ])
    return len(need)
