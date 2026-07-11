"""
Merge several Embase CSV exports into one records_tabular.csv.

Usage:
  python merge_csv.py part1.csv part2.csv part3.csv
  python merge_csv.py                 # auto: merge every part*.csv in this folder

Keeps a single header, preserves quoted fields (abstracts with commas/newlines),
and de-duplicates by (PMID or Title) so overlapping batches don't double-count.
Writes records_tabular.csv.
"""
import csv
import glob
import sys


def main():
    files = sys.argv[1:] or sorted(glob.glob("part*.csv"))
    if not files:
        print("No input files. Pass filenames or name your exports part1.csv, part2.csv, ...")
        return

    header = None
    seen = set()
    rows = []
    for f in files:
        with open(f, encoding="utf-8-sig", newline="") as fh:
            reader = csv.reader(fh)
            h = next(reader, None)
            if h is None:
                print(f"  ⚠ {f} is empty, skipped")
                continue
            if header is None:
                header = h
                # locate PMID / Title columns for dedup
                low = [c.lower() for c in h]
                pmid_i = next((i for i, c in enumerate(low)
                               if "pmid" in c), None)
                title_i = next((i for i, c in enumerate(low)
                                if c in ("title", "article title")), None)
            n_before = len(rows)
            for row in reader:
                if not any(cell.strip() for cell in row):
                    continue
                key = ""
                if pmid_i is not None and pmid_i < len(row) and row[pmid_i].strip():
                    key = "pmid:" + row[pmid_i].strip()
                elif title_i is not None and title_i < len(row):
                    key = "title:" + row[title_i].strip().lower()
                if key and key in seen:
                    continue
                if key:
                    seen.add(key)
                rows.append(row)
            print(f"  + {f}: {len(rows) - n_before} new rows")

    with open("records_tabular.csv", "w", encoding="utf-8-sig", newline="") as out:
        w = csv.writer(out)
        w.writerow(header)
        w.writerows(rows)
    print(f"\n✓ records_tabular.csv written: {len(rows)} unique records from {len(files)} files")


if __name__ == "__main__":
    main()
