"""
Detect ALL corrupted full-text caches (dupes AND mismapped uniques)
===================================================================
The md5-duplicate scan only catches full texts that are byte-identical copies of
one another. It misses a `.txt` that is *unique* but still the WRONG article for
its PMID (e.g. 34508608.txt held an early-onset-geography paper, not the
"Decreasing ER-negative BC" study its PMID claims).

This detector checks EVERY fulltext/*.txt against the study's expected title
(from the cache's studies.json) using the same title-match guard the fetcher now
uses. Any `.txt` whose content does not contain enough of its title's words is
flagged as corrupted. It writes the complete list to rescreen_needed.txt
(superseding the md5-only list), ready for rescreen_corrupted.py.

Run in the Codespace (studies.json lives in the cache):
  python detect_corrupted.py <cache-hash>
"""
import json
import sys
from pathlib import Path

from cache_utils import file_key
from fetch_fulltext import _title_matches


def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_corrupted.py <cache-hash>")
        return
    cache = Path(".cache") / sys.argv[1]
    sj = cache / "studies.json"
    if not sj.is_file():
        print(f"No studies.json at {sj}")
        return

    studies = json.loads(sj.read_text(encoding="utf-8"))
    # map each study's file key (PMID or T_<hash>) -> its title
    key2title = {}
    for s in studies:
        key2title[file_key(s.get("pmid", ""), s.get("title", ""))] = s.get("title", "")

    ft = Path("fulltext")
    checked = bad = 0
    corrupted = []
    for f in sorted(ft.glob("*.txt")):
        title = key2title.get(f.stem)
        if not title:
            continue  # .txt not part of the current search set
        checked += 1
        text = f.read_text(encoding="utf-8", errors="ignore")
        if not _title_matches(title, text):
            bad += 1
            corrupted.append((f.stem, title))

    print(f"Checked {checked} full-text .txt files; {bad} corrupted "
          f"(content does not match title):\n")
    for k, t in corrupted:
        print(f"  {k}  |  {t[:64]}")

    out = Path(__file__).with_name("rescreen_needed.txt")
    out.write_text("\n".join(k for k, _ in corrupted) + ("\n" if corrupted else ""),
                   encoding="utf-8")
    print(f"\n-> wrote {bad} PMIDs to {out.name} (feeds rescreen_corrupted.py)")


if __name__ == "__main__":
    main()
