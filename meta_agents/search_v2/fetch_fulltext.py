#!/usr/bin/env python3
"""Retrieve full text for the 242 TA-included records — run in an UNRESTRICTED
network environment (e.g. GitHub Codespaces), not the sandboxed web session.

Why this exists: the Claude Code web sandbox blocks doi.org, publisher hosts, and
NCBI E-utilities at the egress proxy, so full-text PDFs cannot be pulled there.
A Codespace on this repo has open egress, so this script runs cleanly there.

What it does, per included record (from screening_decisions.csv == include):
  1. Resolve PMID -> PMCID via the NCBI ID Converter.
  2. If in PMC: efetch the full JATS XML (db=pmc) and flatten Methods/Results/
     Tables to text.
  3. If not in PMC but a DOI exists: query Unpaywall for an open-access copy and
     record the OA URL (PDF/HTML) for the author to open.
  4. Save the best full text to fulltext/<record_id>.txt and log coverage.

Nothing here fabricates content: if no full text is reachable, the record is
logged as 'abstract-only' or 'none' — never invented. Eligibility/extraction is
a SEPARATE author step (see ft_screen_template.py); this only fetches.

Requirements:  pip install requests pypdf   (pypdf enables OA-PDF text extraction;
               without it, OA PDFs are recorded as a link only)
Environment (all optional — the NCBI key auto-loads from the repo .mcp.json):
  NCBI_API_KEY    (raises the E-utilities rate limit to ~10 req/s)
  NCBI_EMAIL      (NCBI etiquette; identifies the caller)
  UNPAYWALL_EMAIL (enables the Unpaywall OA fallback; defaults to the project email)

Usage:
  cd meta_agents/search_v2
  python3 fetch_fulltext.py            # incremental: reuses already-saved full texts
  python3 fetch_fulltext.py --force    # re-fetch everything from scratch
  # then inspect fulltext_coverage.csv, manual_download_needed.csv, and fulltext/
"""
import csv
import os
import re
import sys
import time
import json
import urllib.parse
import xml.etree.ElementTree as ET

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
DECISIONS = os.path.join(HERE, "screening_decisions.csv")
OUTDIR = os.path.join(HERE, "fulltext")
COVERAGE = os.path.join(HERE, "fulltext_coverage.csv")

def _from_mcp_json(key):
    """Fall back to the NCBI key already stored in the repo's .mcp.json
    (.mcpServers.pubmed.env.*), searching upward from this file. Lets the
    Codespace run work with a bare `python3 fetch_fulltext.py`."""
    import json
    d = HERE
    for _ in range(6):
        p = os.path.join(d, ".mcp.json")
        if os.path.isfile(p):
            try:
                cfg = json.load(open(p, encoding="utf-8"))
                for srv in cfg.get("mcpServers", {}).values():
                    env = srv.get("env", {})
                    if key in env and str(env[key]).strip():
                        return str(env[key]).strip()
            except (ValueError, OSError):
                pass
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return ""


API_KEY = os.environ.get("NCBI_API_KEY", "").strip() or _from_mcp_json("NCBI_API_KEY")
EMAIL = (os.environ.get("NCBI_EMAIL", "").strip() or _from_mcp_json("NCBI_EMAIL")
         or "p094123@naver.com")
UNPAYWALL_EMAIL = (os.environ.get("UNPAYWALL_EMAIL", "").strip()
                   or _from_mcp_json("UNPAYWALL_EMAIL") or EMAIL)

EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
IDCONV = "https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/"
UNPAYWALL = "https://api.unpaywall.org/v2/"

# NCBI: 10 req/s with a key, 3 without. Stay under.
DELAY = 0.12 if API_KEY else 0.34
SESSION = requests.Session()
# Some OA hosts 403 a non-browser UA, so present a browser UA for OA downloads.
BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/125.0 Safari/537.36")
SESSION.headers.update({"User-Agent": BROWSER_UA})


def _eutils_params(extra):
    p = dict(extra)
    if API_KEY:
        p["api_key"] = API_KEY
    if EMAIL:
        p["email"] = EMAIL
    return p


def get(url, params=None, timeout=40, tries=4):
    for attempt in range(tries):
        try:
            r = SESSION.get(url, params=params, timeout=timeout)
            if r.status_code == 200:
                return r
            if r.status_code in (429, 500, 502, 503):
                time.sleep(1.5 * (attempt + 1))
                continue
            return r
        except requests.RequestException:
            time.sleep(1.5 * (attempt + 1))
    return None


def pmid_to_pmcid(pmid):
    r = get(IDCONV, params={"ids": pmid, "format": "json",
                            "tool": "breast-review", "email": EMAIL or "anon@example.com"})
    if not r or r.status_code != 200:
        return None
    try:
        recs = r.json().get("records", [])
        return recs[0].get("pmcid") if recs else None
    except (ValueError, IndexError, KeyError):
        return None


def fetch_pmc_text(pmcid):
    """efetch db=pmc -> flatten JATS body + table captions to plain text."""
    r = get(EUTILS + "/efetch.fcgi",
            params=_eutils_params({"db": "pmc", "id": pmcid.replace("PMC", ""),
                                   "retmode": "xml"}))
    if not r or r.status_code != 200 or not r.text.strip():
        return None
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError:
        return None
    # If PMC returns only front matter (no <body>), treat as not-open-full-text.
    body = root.find(".//body")
    if body is None:
        return None
    parts = []
    for el in body.iter():
        if el.tag in ("title", "p", "label", "caption", "td", "th") and el.text:
            t = "".join(el.itertext()).strip()
            if t:
                parts.append(t)
    text = "\n".join(parts)
    return text if len(text) > 500 else None


def unpaywall_oa(doi):
    """Return (pdf_url, page_url) from Unpaywall's OA locations (best first).
    Either may be empty. We try the PDF, then the landing page."""
    if not UNPAYWALL_EMAIL or not doi:
        return "", ""
    r = get(UNPAYWALL + urllib.parse.quote(doi), params={"email": UNPAYWALL_EMAIL})
    if not r or r.status_code != 200:
        return "", ""
    try:
        data = r.json()
    except ValueError:
        return "", ""
    locs = []
    if data.get("best_oa_location"):
        locs.append(data["best_oa_location"])
    locs += [l for l in (data.get("oa_locations") or []) if l not in locs]
    pdf_url = next((l.get("url_for_pdf") for l in locs if l.get("url_for_pdf")), "")
    page_url = next((l.get("url") for l in locs if l.get("url")), "")
    return pdf_url or "", page_url or ""


def _pdf_to_text(data):
    import io
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(data))
        return "\n".join((p.extract_text() or "") for p in reader.pages)
    except Exception:
        pass
    try:
        from pdfminer.high_level import extract_text
        return extract_text(io.BytesIO(data))
    except Exception:
        return None


def _html_to_text(html):
    html = re.sub(r"(?is)<(script|style|noscript).*?</\1>", " ", html)
    html = re.sub(r"(?is)<br\s*/?>", "\n", html)
    html = re.sub(r"(?is)</(p|div|h[1-6]|li|tr|section)>", "\n", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = (text.replace("&nbsp;", " ").replace("&amp;", "&")
                .replace("&lt;", "<").replace("&gt;", ">"))
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    return text.strip()


def _get_bytes(url):
    try:
        r = SESSION.get(url, timeout=60, allow_redirects=True,
                        headers={"Accept": "application/pdf,text/html,*/*"})
    except requests.RequestException as e:
        return None, "err:%s" % type(e).__name__
    # NB: a requests.Response is falsy for status >= 400, so test `is None`,
    # and report the REAL status code (not "none") for diagnosis.
    if r is None or r.status_code != 200:
        return None, "http:%s" % (r.status_code if r is not None else "noresp")
    return r, ""


def fetch_oa_text(pdf_url, page_url):
    """Try, in order: the OA PDF URL; a citation_pdf_url discovered on the OA
    landing page; the landing page HTML itself. Returns (text|None, note) where
    note explains the outcome for logging."""
    tried = []
    # 1) direct PDF url
    for u in [pdf_url]:
        if not u:
            continue
        r, err = _get_bytes(u)
        if err:
            tried.append("pdf %s" % err)
            continue
        if r.content[:5] == b"%PDF-" or "pdf" in r.headers.get("Content-Type", "").lower():
            t = _pdf_to_text(r.content)
            if t and len(t) > 600:
                return t, "pdf-ok"
            tried.append("pdf-short(%d)" % (len(t) if t else 0))
        else:
            tried.append("pdf-not-pdf")
    # 2) landing page -> look for citation_pdf_url meta, else use HTML text
    if page_url:
        r, err = _get_bytes(page_url)
        if err:
            tried.append("page %s" % err)
        elif r is not None:
            html = r.text
            m = re.search(r'citation_pdf_url"\s+content="([^"]+)"', html) \
                or re.search(r'content="([^"]+)"\s+name="citation_pdf_url"', html)
            if m:
                r2, err2 = _get_bytes(m.group(1))
                if not err2 and (r2.content[:5] == b"%PDF-" or "pdf" in r2.headers.get("Content-Type", "").lower()):
                    t = _pdf_to_text(r2.content)
                    if t and len(t) > 600:
                        return t, "citation-pdf-ok"
                    tried.append("cit-pdf-short")
                else:
                    tried.append("cit-pdf %s" % (err2 or "not-pdf"))
            t = _html_to_text(html)
            if t and len(t) > 1500 and re.search(r"method|result|incidence|age-adjusted", t, re.I):
                return t, "html-ok"
            tried.append("html-short(%d)" % (len(t) if t else 0))
    return None, "; ".join(tried) or "no-oa-url"


def load_includes():
    dec = {}
    with open(DECISIONS, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dec[int(row["record_id"])] = row["decision"]
    recs = list(csv.DictReader(open(MERGED, newline="", encoding="utf-8")))
    inc = sorted(i for i, d in dec.items() if d == "include")
    return [(i, recs[i]) for i in inc]


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    includes = load_includes()
    print("included records: %d" % len(includes))
    if not API_KEY:
        print("WARNING: NCBI_API_KEY not set — slow and rate-limited.")
    try:
        import pypdf  # noqa: F401
    except ImportError:
        try:
            import pdfminer  # noqa: F401
        except ImportError:
            print("WARNING: no PDF library — OA PDFs cannot be extracted. "
                  "Run:  pip install pypdf   then re-run.")

    force = "--force" in sys.argv
    rows = []
    for n, (rid, rec) in enumerate(includes, 1):
        pmid = (rec.get("pmid") or "").strip()
        doi = (rec.get("doi") or "").strip()
        pmcid = source = oa_url = ""
        chars = 0
        text = None

        # Resumable: reuse an already-saved full text (skip the network) unless --force.
        cached = os.path.join(OUTDIR, "%d.txt" % rid)
        if not force and os.path.isfile(cached) and os.path.getsize(cached) > 600:
            body = open(cached, encoding="utf-8").read()
            m = re.search(r"^SOURCE:\s*(\S+)", body, re.M)
            source = m.group(1) if m else "cached"
            chars = len(body)
            rows.append(dict(record_id=rid, year=rec.get("year", ""), pmid=pmid, doi=doi,
                             pmcid="", source=source, oa_url="", oa_note="", chars=chars,
                             title=rec.get("title", "")[:120]))
            print("[%3d/%d] rec %-4d %-18s %6d chars  (cached)" % (n, len(includes), rid, source, chars))
            continue

        if pmid:
            pmcid = pmid_to_pmcid(pmid) or ""
            time.sleep(DELAY)
            if pmcid:
                text = fetch_pmc_text(pmcid)
                time.sleep(DELAY)
                if text:
                    source = "pmc"
        oa_note = ""
        if text is None and doi:
            oa_pdf, oa_page = unpaywall_oa(doi)
            oa_url = oa_pdf or oa_page
            if oa_url:
                text, oa_note = fetch_oa_text(oa_pdf, oa_page)
                source = "unpaywall-oa" if text else "unpaywall-oa-link"

        if text:
            with open(cached, "w", encoding="utf-8") as f:
                f.write("record_id=%d pmid=%s doi=%s pmcid=%s\nSOURCE: %s\nTITLE: %s\n\n%s\n"
                        % (rid, pmid, doi, pmcid, source, rec.get("title", ""), text))
            chars = len(text)
        if not source:
            source = "none" if not (pmid or doi) else "no-oa-full-text"

        rows.append(dict(record_id=rid, year=rec.get("year", ""), pmid=pmid, doi=doi,
                         pmcid=pmcid, source=source, oa_url=oa_url, oa_note=oa_note, chars=chars,
                         title=rec.get("title", "")[:120]))
        tail = ("  [%s]" % oa_note) if source == "unpaywall-oa-link" else "  " + rec.get("title", "")[:48]
        print("[%3d/%d] rec %-4d %-18s %6d chars%s" % (n, len(includes), rid, source, chars, tail))

    with open(COVERAGE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "year", "pmid", "doi",
                                          "pmcid", "source", "oa_url", "oa_note", "chars", "title"])
        w.writeheader()
        w.writerows(rows)

    # Records WITHOUT auto-retrieved full text -> manual institutional download.
    AUTO = {"pmc", "unpaywall-oa", "cached"}
    manual = [r for r in rows if r["source"] not in AUTO]
    manual_path = os.path.join(HERE, "manual_download_needed.csv")
    with open(manual_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "year", "title", "doi",
                                          "doi_url", "pmid", "oa_url", "source"])
        w.writeheader()
        for r in manual:
            w.writerow({
                "record_id": r["record_id"], "year": r["year"], "title": r["title"],
                "doi": r["doi"],
                "doi_url": ("https://doi.org/%s" % r["doi"]) if r["doi"] else "",
                "pmid": r["pmid"], "oa_url": r["oa_url"], "source": r["source"],
            })

    from collections import Counter
    print("\n=== coverage ===")
    for k, v in Counter(r["source"] for r in rows).most_common():
        print("  %4d  %s" % (v, k))
    print("\nauto-retrieved full text (pmc + unpaywall-oa + cached): %d"
          % sum(1 for r in rows if r["source"] in AUTO))
    print("MANUAL download needed        : %d  -> %s" % (len(manual), manual_path))
    print("  (open each doi_url with institutional access; %d have an OA link to try first)"
          % sum(1 for r in manual if r["oa_url"]))
    print("full text saved to: %s/" % OUTDIR)
    print("coverage log: %s" % COVERAGE)


if __name__ == "__main__":
    main()
