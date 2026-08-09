#!/usr/bin/env python3
"""Reconcile fulltext_coverage.csv + manual_download_needed.csv with what is
actually present in fulltext/ (auto-fetched .txt, ingested manual PDFs, and any
PDFs still lacking a text layer). Re-runnable as more PDFs arrive.

Reads the SOURCE: line and body length of each fulltext/<id>.txt, checks for a
fulltext/<id>.pdf with no extractable text, and rewrites both CSVs plus prints a
status summary. Records in ft_unavailable.csv are marked 'unavailable'.

Usage:  python3 reconcile_coverage.py
"""
import csv
import os
import re
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
OUTDIR = os.path.join(HERE, "fulltext")
MERGED = os.path.join(HERE, "merged_unique.csv")
DECISIONS = os.path.join(HERE, "screening_decisions.csv")
COVERAGE = os.path.join(HERE, "fulltext_coverage.csv")
MANUAL = os.path.join(HERE, "manual_download_needed.csv")
UNAVAIL = os.path.join(HERE, "ft_unavailable.csv")

LOW_TEXT = 1500   # body chars below this = probably scanned / stub, not usable text


def body_info(txt_path):
    raw = open(txt_path, encoding="utf-8").read()
    m = re.search(r"^SOURCE:\s*(\S+)", raw, re.M)
    src = m.group(1) if m else "cached"
    # body starts after the blank line following the header block
    body = raw.split("\n\n", 1)[1] if "\n\n" in raw else raw
    return src, len(body)


def main():
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    dec = {int(r["record_id"]): r for r in csv.DictReader(open(DECISIONS, encoding="utf-8"))}
    inc = sorted(i for i in dec if dec[i]["decision"] == "include")
    unavailable = set()
    if os.path.exists(UNAVAIL):
        unavailable = {int(r["record_id"]) for r in csv.DictReader(open(UNAVAIL, encoding="utf-8"))}

    rows = []
    for i in inc:
        r = recs[i]
        txt = os.path.join(OUTDIR, "%d.txt" % i)
        pdf = os.path.join(OUTDIR, "%d.pdf" % i)
        pdf_alt = os.path.join(HERE, "fulltext_pdf", "%d.pdf" % i)
        source, chars = "", 0
        if os.path.isfile(txt):
            source, chars = body_info(txt)
            if chars < LOW_TEXT:
                source = source + "-lowtext"
        elif os.path.isfile(pdf) or os.path.isfile(pdf_alt):
            source, chars = "pdf-no-textlayer", 0   # PDF present but not extractable
        elif i in unavailable:
            source = "unavailable"
        else:
            source = "MISSING"
        rows.append(dict(record_id=i, year=r.get("year", ""), pmid=r.get("pmid", ""),
                         doi=r.get("doi", ""), source=source, chars=chars,
                         title=r.get("title", "")[:120]))

    with open(COVERAGE, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "year", "pmid", "doi",
                                          "source", "chars", "title"])
        w.writeheader()
        w.writerows(rows)

    # Still-missing manual worklist (no usable text yet).
    HAVE = lambda s: s in ("pmc", "unpaywall-oa", "cached", "manual-pdf")
    still = [r for r in rows if not HAVE(r["source"])]
    with open(MANUAL, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["record_id", "pmid", "pubmed_url", "doi_url",
                                          "title", "source", "year", "doi"])
        w.writeheader()
        for r in still:
            pmid = r["pmid"]
            w.writerow({
                "record_id": r["record_id"], "pmid": pmid,
                "pubmed_url": ("https://pubmed.ncbi.nlm.nih.gov/%s/" % pmid) if pmid else "",
                "doi_url": ("https://doi.org/%s" % r["doi"]) if r["doi"] else "",
                "title": r["title"], "source": r["source"], "year": r["year"], "doi": r["doi"],
            })

    from collections import Counter
    def bucket(s):
        if HAVE(s):
            return "HAVE full text"
        if s.endswith("-lowtext") or s == "pdf-no-textlayer":
            return "PDF present, no text (author reads / OCR)"
        if s == "unavailable":
            return "unavailable (logged)"
        return "still missing"
    print("=== full-text status (%d includes) ===" % len(rows))
    for k, v in Counter(bucket(r["source"]) for r in rows).most_common():
        print("  %3d  %s" % (v, k))
    print("\nsource detail:")
    for k, v in Counter(r["source"] for r in rows).most_common():
        print("  %3d  %s" % (v, k))
    print("\nupdated: %s , %s" % (os.path.basename(COVERAGE), os.path.basename(MANUAL)))
    low = [r["record_id"] for r in rows if r["source"].endswith("-lowtext") or r["source"] == "pdf-no-textlayer"]
    if low:
        print("PDF-present-but-no-text (author reads directly): %s" % low)


if __name__ == "__main__":
    main()
