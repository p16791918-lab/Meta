"""
Convert Embase "field-labeled" CSV exports into one tabular records_tabular.csv.

Embase can export in a long format where each FIELD is its own line:
    "TITLE","..."
    "AUTHOR NAMES","A","B",...
    "SOURCE","..."
    "ABSTRACT","..."
    "MEDLINE PMID","12345678"
A new record starts at each "TITLE" line. This script reshapes that into the
row-per-record CSV the pipeline expects (columns: TITLE, AUTHOR NAMES,
PUBLICATION YEAR, SOURCE, PUBLICATION TYPE, ABSTRACT, MEDLINE PMID, DOI),
merging several export parts and de-duplicating by PMID / Title.

Usage:
  python convert_embase.py part1.csv part2.csv
  python convert_embase.py                 # auto: every part*.csv here
"""
import csv
import glob
import sys

COLUMNS = ["TITLE", "AUTHOR NAMES", "PUBLICATION YEAR", "SOURCE",
           "PUBLICATION TYPE", "ABSTRACT", "MEDLINE PMID", "DOI"]
RECORD_START = "TITLE"


def parse_file(path):
    """Yield record dicts from one field-labeled Embase export."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        cur = None
        for row in reader:
            if not row or not row[0].strip():
                continue
            field = row[0].strip().upper()
            values = [v.strip() for v in row[1:] if v.strip()]
            value = "; ".join(values)  # AUTHOR NAMES etc. may have many
            if field == RECORD_START:
                if cur:
                    yield cur
                cur = {}
            if cur is None:      # tolerate stray leading fields
                cur = {}
            # keep first non-empty occurrence of a field
            if field not in cur or not cur[field]:
                cur[field] = value
        if cur:
            yield cur


def main():
    files = sys.argv[1:] or sorted(glob.glob("part*.csv"))
    if not files:
        print("No input files. Pass filenames or name exports part1.csv, part2.csv ...")
        return

    seen = set()
    out_rows = []
    for path in files:
        n = 0
        for rec in parse_file(path):
            pmid = rec.get("MEDLINE PMID", "").strip()
            title = rec.get("TITLE", "").strip()
            key = ("pmid:" + pmid) if pmid else ("title:" + title.lower())
            if key in seen:
                continue
            seen.add(key)
            out_rows.append([rec.get(c, "") for c in COLUMNS])
            n += 1
        print(f"  + {path}: {n} records")

    with open("records_tabular.csv", "w", encoding="utf-8-sig", newline="") as out:
        w = csv.writer(out)
        w.writerow(COLUMNS)
        w.writerows(out_rows)
    n_pmid = sum(1 for r in out_rows if r[COLUMNS.index("MEDLINE PMID")].strip())
    n_abs = sum(1 for r in out_rows if r[COLUMNS.index("ABSTRACT")].strip())
    print(f"\n✓ records_tabular.csv: {len(out_rows)} unique records "
          f"({n_pmid} with PMID, {n_abs} with abstract)")


if __name__ == "__main__":
    main()
