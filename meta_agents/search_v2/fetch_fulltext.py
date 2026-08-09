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

Requirements:  pip install requests
Environment:
  NCBI_API_KEY    (raises the E-utilities rate limit to ~10 req/s)
  NCBI_EMAIL      (NCBI etiquette; identifies the caller)
  UNPAYWALL_EMAIL (optional; enables the Unpaywall OA fallback)

Usage:
  cd meta_agents/search_v2
  NCBI_API_KEY=... NCBI_EMAIL=you@example.com UNPAYWALL_EMAIL=you@example.com \
      python3 fetch_fulltext.py
  # then inspect fulltext_coverage.csv and the fulltext/ directory
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
SESSION.headers.update({"User-Agent": "breast-incidence-review/1.0 (mailto:%s)" % (EMAIL or "anon")})


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
    if not UNPAYWALL_EMAIL or not doi:
        return None
    r = get(UNPAYWALL + urllib.parse.quote(doi), params={"email": UNPAYWALL_EMAIL})
    if not r or r.status_code != 200:
        return None
    try:
        data = r.json()
    except ValueError:
        return None
    loc = data.get("best_oa_location") or {}
    return loc.get("url_for_pdf") or loc.get("url")


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

    rows = []
    for n, (rid, rec) in enumerate(includes, 1):
        pmid = (rec.get("pmid") or "").strip()
        doi = (rec.get("doi") or "").strip()
        pmcid = source = oa_url = ""
        chars = 0
        text = None

        if pmid:
            pmcid = pmid_to_pmcid(pmid) or ""
            time.sleep(DELAY)
            if pmcid:
                text = fetch_pmc_text(pmcid)
                time.sleep(DELAY)
                if text:
                    source = "pmc"
        if text is None and doi:
            oa_url = unpaywall_oa(doi) or ""
            if oa_url:
                source = "unpaywall-oa-link"  # link recorded; author opens it

        if text:
            with open(os.path.join(OUTDIR, "%d.txt" % rid), "w", encoding="utf-8") as f:
                f.write("record_id=%d pmid=%s doi=%s pmcid=%s\nTITLE: %s\n\n%s\n"
                        % (rid, pmid, doi, pmcid, rec.get("title", ""), text))
            chars = len(text)
        if not source:
            source = "none" if not (pmid or doi) else "no-oa-full-text"

        rows.append(dict(record_id=rid, year=rec.get("year", ""), pmid=pmid, doi=doi,
                         pmcid=pmcid, source=source, oa_url=oa_url, chars=chars,
                         title=rec.get("title", "")[:120]))
        print("[%3d/%d] rec %-4d %-18s %6d chars  %s"
              % (n, len(includes), rid, source, chars, rec.get("title", "")[:56]))

    with open(COVERAGE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "year", "pmid", "doi",
                                          "pmcid", "source", "oa_url", "chars", "title"])
        w.writeheader()
        w.writerows(rows)

    # Records WITHOUT auto-retrieved PMC full text -> manual institutional download.
    manual = [r for r in rows if r["source"] != "pmc"]
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
    print("\nauto-retrieved (PMC full text): %d" % sum(1 for r in rows if r["source"] == "pmc"))
    print("MANUAL download needed        : %d  -> %s" % (len(manual), manual_path))
    print("  (open each doi_url with institutional access; %d have an OA link already)"
          % sum(1 for r in manual if r["oa_url"]))
    print("full text saved to: %s/" % OUTDIR)
    print("coverage log: %s" % COVERAGE)


if __name__ == "__main__":
    main()
