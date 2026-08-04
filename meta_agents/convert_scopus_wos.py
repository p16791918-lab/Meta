"""
Normalize Scopus / Web of Science exports into the pipeline's 8-column schema
============================================================================
Output columns (identical to records_tabular.csv):
    TITLE, AUTHOR NAMES, PUBLICATION YEAR, SOURCE, PUBLICATION TYPE,
    ABSTRACT, MEDLINE PMID, DOI

Handles:
  * Scopus CSV export  (comma-separated, human-readable headers)
  * WoS "Tab-delimited" export (.txt/.tsv, two-letter field tags OR full names)
  * WoS Excel-style CSV export (full-name headers)

Header matching is case-insensitive and tolerant of the common variants each
database uses, so you don't have to hand-edit the export.

Usage:
  python convert_scopus_wos.py raw_scopus.csv --source scopus -o records_scopus.csv
  python convert_scopus_wos.py raw_wos.txt    --source wos    -o records_wos.csv
"""
import argparse
import csv
import sys

OUT_COLUMNS = ["TITLE", "AUTHOR NAMES", "PUBLICATION YEAR", "SOURCE",
               "PUBLICATION TYPE", "ABSTRACT", "MEDLINE PMID", "DOI"]

# Candidate source-header names (lowercased) for each output column.
# Includes Scopus headers, WoS full-name headers, and WoS two-letter tags.
FIELD_ALIASES = {
    "TITLE":            ["title", "article title", "document title", "ti"],
    "AUTHOR NAMES":     ["authors", "author names", "author full names",
                         "au", "af"],
    "PUBLICATION YEAR": ["year", "publication year", "py"],
    "SOURCE":           ["source title", "source", "so", "journal",
                         "publication name"],
    "PUBLICATION TYPE": ["document type", "doctype", "dt", "publication type"],
    "ABSTRACT":         ["abstract", "ab"],
    "MEDLINE PMID":     ["pubmed id", "pubmed", "pmid", "pm", "medline pmid"],
    "DOI":              ["doi", "di"],
}


def _build_header_map(fieldnames):
    """Map each output column -> the first matching input header present."""
    lower = {(h or "").strip().lower(): h for h in fieldnames}
    hmap = {}
    for out_col, aliases in FIELD_ALIASES.items():
        for a in aliases:
            if a in lower:
                hmap[out_col] = lower[a]
                break
    return hmap


def _sniff_dialect(path):
    """Tab-delimited for .txt/.tsv, else comma (Scopus/WoS-Excel CSV)."""
    if path.lower().endswith((".txt", ".tsv")):
        return "\t"
    return ","


def convert(path, source):
    delim = _sniff_dialect(path)
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f, delimiter=delim)
        if not reader.fieldnames:
            print(f"[error] no header row found in {path}", file=sys.stderr)
            return []
        hmap = _build_header_map(reader.fieldnames)
        if "TITLE" not in hmap:
            print(f"[error] could not find a Title column in {path}.\n"
                  f"        headers seen: {reader.fieldnames}", file=sys.stderr)
            return []
        rows = []
        for r in reader:
            out = {c: "" for c in OUT_COLUMNS}
            for out_col, src_col in hmap.items():
                out[out_col] = (r.get(src_col) or "").strip()
            # normalize a few things
            if out["PUBLICATION YEAR"]:
                digits = "".join(ch for ch in out["PUBLICATION YEAR"]
                                 if ch.isdigit())[:4]
                out["PUBLICATION YEAR"] = digits
            out["MEDLINE PMID"] = "".join(ch for ch in out["MEDLINE PMID"]
                                          if ch.isdigit())
            if not out["PUBLICATION TYPE"]:
                out["PUBLICATION TYPE"] = source.upper()
            if out["TITLE"]:
                rows.append(out)
    print(f"[{source}] {path}: {len(rows)} records "
          f"(mapped: {sorted(hmap)})")
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--source", required=True, choices=["scopus", "wos"])
    ap.add_argument("-o", "--output", required=True)
    args = ap.parse_args()

    rows = convert(args.input, args.source)
    with open(args.output, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=OUT_COLUMNS)
        w.writeheader()
        w.writerows(rows)
    print(f"[OK] wrote {len(rows)} records -> {args.output}")


if __name__ == "__main__":
    main()
