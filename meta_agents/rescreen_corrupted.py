"""
Selective re-screen of corrupted-full-text studies
===================================================
The PMC auto-fetch cached the same article under many PMIDs (md5-duplicate
groups). Those studies were screened at Phase 2 on the WRONG full text, so a
genuinely eligible study could have been wrongly excluded. Rather than
re-screening all ~478 full-text studies, we re-screen ONLY the affected ones.

`rescreen_needed.txt` lists the affected PMIDs (produced from md5 duplicates).

What this script does (run in the Codespace, where NCBI is reachable):
  1) deletes the corrupted fulltext/<pmid>.txt for each affected PMID
  2) removes those PMIDs' cached Phase-2 decisions from the cache
     (so the next run re-screens them from scratch)

Then re-run the pipeline:  python orchestrator.py multi
  → full-text fetch re-downloads correct text (now title-verified, so a wrong
    article is auto-rejected and the study falls back to abstract), and Phase 2
    re-screens just these studies. Compare the new included set with the old.

Usage:
  python rescreen_corrupted.py <cache-hash>            # e.g. 8f982a885955
  python rescreen_corrupted.py <cache-hash> --dry-run  # show what would change
"""
import json
import os
import sys
from pathlib import Path


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("-")]
    dry = "--dry-run" in sys.argv
    if not args:
        print("Usage: python rescreen_corrupted.py <cache-hash> [--dry-run]")
        return
    cache_dir = Path(".cache") / args[0]
    if not cache_dir.is_dir():
        print(f"No cache dir {cache_dir}")
        return

    listing = Path(__file__).with_name("rescreen_needed.txt")
    pmids = {l.strip() for l in listing.read_text().splitlines() if l.strip()}
    print(f"{len(pmids)} corrupted PMIDs to re-screen.")

    # 1) delete corrupted full-text caches
    ft = Path("fulltext")
    removed_txt = 0
    for p in pmids:
        f = ft / f"{p}.txt"
        if f.is_file():
            print(f"  {'[dry] ' if dry else ''}rm fulltext/{p}.txt")
            if not dry:
                f.unlink()
            removed_txt += 1

    # 2) drop these PMIDs' Phase-2 decisions so they get re-screened
    p2 = cache_dir / "phase2.jsonl"
    kept, dropped = [], 0
    if p2.is_file():
        for line in p2.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                kept.append(line)
                continue
            if str(rec.get("pmid", "")).strip() in pmids:
                dropped += 1
            else:
                kept.append(line)
        if not dry:
            # back up, then rewrite without the affected decisions
            p2.rename(cache_dir / "phase2.jsonl.bak")
            p2.write_text("\n".join(kept) + ("\n" if kept else ""), encoding="utf-8")

    print(f"\nSummary: removed {removed_txt} corrupted .txt, "
          f"dropped {dropped} Phase-2 decisions "
          f"({'DRY-RUN, nothing written' if dry else 'phase2.jsonl.bak saved'}).")
    if not dry:
        print("\nNext: python orchestrator.py multi   "
              "(re-fetches + re-screens only these), then compare the included set.")


if __name__ == "__main__":
    main()
