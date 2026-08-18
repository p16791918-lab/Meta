#!/usr/bin/env python3
"""Complete the unified reference list in full Vancouver style.

Run this in an environment with internet access to NCBI (e.g. a GitHub Codespace);
it is blocked in the sandbox where the manuscript was drafted. It reads the same
corpus files, rebuilds the unified ordering (1-12 Introduction, 13-17 Methods,
18-51 Results), fetches MEDLINE records for every PMID via NCBI E-utilities, and
writes manuscript/References_complete.md with each entry formatted as:

    N. Author AB, Author CD, et al. Title. Journal Abbrev. Year;Vol(Issue):Pages. doi:...

Usage:
    python3 build_references.py            # anonymous (<=3 requests/sec)
    NCBI_API_KEY=xxxx python3 build_references.py   # faster (<=10/sec)
"""
import csv, json, os, re, time, urllib.request, urllib.parse

HERE = os.path.dirname(os.path.abspath(__file__))
API_KEY = os.environ.get("NCBI_API_KEY", "")
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"


def load_order():
    lab = json.load(open(os.path.join(HERE, "author_labels.json")))
    inc = {r["record_id"]: r for r in csv.DictReader(
        open(os.path.join(HERE, "includes_characterization.csv"), encoding="utf-8"))}
    intro = ["0", "2", "66", "200", "236", "49", "463", "3182", "333", "617", "28", "51"]
    ext = sorted({r["record_id"] for r in csv.DictReader(
        open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8"))},
        key=lambda x: int(x) if x.isdigit() else 9999)
    new = [r for r in ext if r not in intro]
    order = []  # (num, kind, record_id_or_None, pmid_or_None, manual_text_or_None)
    n = 0
    for r in intro:
        n += 1; order.append((n, "pmid", r, (inc.get(r, {}).get("pmid") or "").strip(), None))
    methods = [  # (pmid, manual_fallback_text)
        ("33782057", None),
        (None, "Wells GA, Shea B, O'Connell D, et al. The Newcastle-Ottawa Scale (NOS) for "
               "assessing the quality of nonrandomised studies in meta-analyses. Ottawa: "
               "Ottawa Hospital Research Institute; 2000."),
        ("21195583", None),
        (None, "Schunemann H, Brozek J, Guyatt G, Oxman A, editors. GRADE Handbook. "
               "GRADE Working Group; 2013."),
        ("24548571", None),
    ]
    for pmid, manual in methods:
        n += 1; order.append((n, "pmid" if pmid else "manual", None, pmid, manual))
    for r in new:
        n += 1; order.append((n, "pmid", r, (inc.get(r, {}).get("pmid") or "").strip(), None))
    return order, inc


def efetch_medline(pmids):
    """Return {pmid: medline_text} for a batch of PMIDs."""
    params = {"db": "pubmed", "id": ",".join(pmids), "rettype": "medline", "retmode": "text"}
    if API_KEY:
        params["api_key"] = API_KEY
    url = EFETCH + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as resp:
                text = resp.read().decode("utf-8", "replace")
            break
        except Exception as e:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)
    # split records (blank line separated); key by PMID- line
    out = {}
    for rec in re.split(r"\n\n+", text):
        m = re.search(r"^PMID- (\d+)", rec, re.M)
        if m:
            out[m.group(1)] = rec
    return out


def field(rec, tag):
    vals, cur = [], None
    for line in rec.splitlines():
        m = re.match(r"^([A-Z]{2,4})\s*- (.*)", line)
        if m:
            cur = m.group(1)
            if cur == tag:
                vals.append(m.group(2))
        elif line.startswith("      ") and cur == tag and vals:
            vals[-1] += " " + line.strip()
    return vals


def vancouver(rec):
    au = field(rec, "AU")
    authors = ", ".join(au[:6]) + (", et al." if len(au) > 6 else "")
    ti = " ".join(field(rec, "TI")).strip().rstrip(".")
    ta = (field(rec, "TA") or field(rec, "JT") or [""])[0]
    dp = (field(rec, "DP") or [""])[0]
    year = (re.search(r"\d{4}", dp) or [None])
    year = re.search(r"\d{4}", dp).group() if re.search(r"\d{4}", dp) else ""
    vi = (field(rec, "VI") or [""])[0]
    ip = (field(rec, "IP") or [""])[0]
    pg = (field(rec, "PG") or [""])[0]
    doi = ""
    for a in field(rec, "AID") + field(rec, "LID"):
        m = re.search(r"(10\.\S+?)\s*\[doi\]", a)
        if m:
            doi = m.group(1); break
    cite = "%s %s. %s. %s" % (authors, ti, ta, year)
    if vi:
        cite += ";%s" % vi
    if ip:
        cite += "(%s)" % ip
    if pg:
        cite += ":%s" % pg
    cite += "."
    if doi:
        cite += " doi:%s." % doi
    return cite


def main():
    order, inc = load_order()
    pmids = [pmid for (_, kind, _, pmid, _) in order if kind == "pmid" and pmid]
    records = {}
    for i in range(0, len(pmids), 40):
        batch = pmids[i:i + 40]
        records.update(efetch_medline(batch))
        time.sleep(0.4 if API_KEY else 0.34)
        print("fetched %d/%d" % (min(i + 40, len(pmids)), len(pmids)))
    lines = ["# Unified reference list (Vancouver) — auto-completed", ""]
    missing = []
    for num, kind, rid, pmid, manual in order:
        if kind == "manual":
            lines.append("%d. %s" % (num, manual))
        elif pmid and pmid in records:
            lines.append("%d. %s" % (num, vancouver(records[pmid])))
        else:
            missing.append((num, rid, pmid))
            lines.append("%d. [PMID %s not retrieved — check manually]" % (num, pmid or "none"))
    open(os.path.join(HERE, "manuscript", "References_complete.md"), "w",
         encoding="utf-8").write("\n".join(lines) + "\n")
    print("wrote manuscript/References_complete.md (%d refs)" % len(order))
    if missing:
        print("missing/unretrieved:", missing)


if __name__ == "__main__":
    main()
