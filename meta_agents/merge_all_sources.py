"""
Merge PubMed + Embase + Scopus + WoS into one deduplicated record set
=====================================================================
Reads whichever of these 8-column CSVs exist in this folder and merges them
with provenance tracking + PRISMA identification counts:

    records_pubmed.csv    (PubMed export, converted)
    records_tabular.csv   (Embase, already present)
    records_scopus.csv    (from convert_scopus_wos.py --source scopus)
    records_wos.csv       (from convert_scopus_wos.py --source wos)

Output:
    records_merged.csv    (unique records, with a SOURCES column)
    merge_report.json     (counts per source, duplicates removed, overlap)

Run after the four searches are exported and normalized. Missing files are
skipped with a note, so you can run it incrementally.
"""
import csv
import json
import os
import re

from merge_sources import merge_sources


def clean_pmid(raw):
    """Embase stores 'PMID; http://.../PMID'; take the first digit run only."""
    m = re.search(r"\d{5,9}", str(raw or ""))
    return m.group() if m else ""

SOURCES = {
    "PubMed": "records_pubmed.csv",
    "Embase": "records_tabular.csv",
    "Scopus": "records_scopus.csv",
    "WoS":    "records_wos.csv",
}

OUT_CSV = "records_merged.csv"
OUT_REPORT = "merge_report.json"


def load_csv(path):
    """Read the 8-column schema into the internal record dicts merge wants."""
    out = []
    with open(path, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            r = { (k or "").strip().upper(): (v or "").strip() for k, v in r.items() }
            out.append({
                "title":    r.get("TITLE", ""),
                "authors":  r.get("AUTHOR NAMES", ""),
                "year":     r.get("PUBLICATION YEAR", ""),
                "journal":  r.get("SOURCE", ""),
                "pubtype":  r.get("PUBLICATION TYPE", ""),
                "abstract": r.get("ABSTRACT", ""),
                "pmid":     clean_pmid(r.get("MEDLINE PMID", "")),
                "doi":      r.get("DOI", ""),
            })
    return out


def main():
    source_lists = {}
    for label, path in SOURCES.items():
        if os.path.exists(path):
            recs = load_csv(path)
            source_lists[label] = recs
            print(f"[load] {label:8s} {len(recs):5d}  ({path})")
        else:
            print(f"[skip] {label:8s}    -   ({path} not found)")

    if not source_lists:
        print("No source files found. Export the searches first.")
        return

    merged, report = merge_sources(source_lists)

    # write merged records (add SOURCES provenance column)
    cols = ["TITLE", "AUTHOR NAMES", "PUBLICATION YEAR", "SOURCE",
            "PUBLICATION TYPE", "ABSTRACT", "MEDLINE PMID", "DOI", "SOURCES"]
    with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in merged:
            w.writerow([
                r.get("title", ""), r.get("authors", ""), r.get("year", ""),
                r.get("journal", ""), r.get("pubtype", ""), r.get("abstract", ""),
                r.get("pmid", ""), r.get("doi", ""),
                "+".join(r.get("sources", [])),
            ])

    with open(OUT_REPORT, "w") as f:
        json.dump(report, f, indent=2)

    print("\n── PRISMA identification ─────────────────────────────")
    print(f"  Records by source : {report['records_by_source']}")
    print(f"  Total before dedup: {report['total_before']}")
    print(f"  Duplicates removed: {report['duplicates_removed']}")
    print(f"  Unique records    : {report['total_after']}")
    print(f"  Source overlap    : {report['overlap']}")
    print(f"\n[OK] -> {OUT_CSV}, {OUT_REPORT}")


if __name__ == "__main__":
    main()
