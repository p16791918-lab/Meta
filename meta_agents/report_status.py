"""
Screening status report
========================
Prints, for the current review's cache:
  - overall counts (identified / advanced / included / excluded / not-retrieved)
  - INCLUDED studies, split into "have full text" vs "★ need a PDF" (for extraction)
  - NOT_RETRIEVED studies that could not be screened at all (need obtaining to classify)

Usage:
  python report_status.py                 # newest cache dir
  python report_status.py <cache-hash>    # a specific one
"""
import glob
import json
import os
import sys


def _load_jsonl(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def _has_fulltext(pmid, fulltext_dir="fulltext"):
    pmid = str(pmid)
    return (os.path.exists(os.path.join(fulltext_dir, pmid + ".txt"))
            or os.path.exists(os.path.join(fulltext_dir, pmid + ".pdf")))


def main():
    if len(sys.argv) > 1:
        cache_dir = os.path.join(".cache", sys.argv[1])
    else:
        dirs = sorted(glob.glob(".cache/*/"), key=os.path.getmtime)
        if not dirs:
            print("No .cache/ found. Run the pipeline first.")
            return
        cache_dir = dirs[-1].rstrip("/")

    print(f"Cache: {cache_dir}\n")

    studies = json.load(open(os.path.join(cache_dir, "studies.json"), encoding="utf-8")) \
        if os.path.exists(os.path.join(cache_dir, "studies.json")) else []
    S = {str(s.get("pmid", "")): s for s in studies}

    p1 = _load_jsonl(os.path.join(cache_dir, "phase1.jsonl"))
    p2 = _load_jsonl(os.path.join(cache_dir, "phase2.jsonl"))

    # current-set pmids only
    cur = set(S.keys())
    p1 = [d for d in p1 if str(d["pmid"]) in cur] if cur else p1
    advanced = {str(d["pmid"]) for d in p1 if d["phase1_decision"] != "exclude"}
    p2_by = {str(d["pmid"]): d for d in p2}

    included = [pmid for pmid in advanced if p2_by.get(pmid, {}).get("phase2_decision") == "include"]
    excluded = [pmid for pmid in advanced if p2_by.get(pmid, {}).get("phase2_decision") == "exclude"]
    # advanced but never screened (no full text AND no abstract): not in p2 at all
    not_retrieved = [pmid for pmid in advanced if pmid not in p2_by]

    print("=" * 60)
    print(f"  Identified (after dedup) : {len(studies)}")
    print(f"  Advanced past abstract   : {len(advanced)}")
    print(f"  Included                 : {len(included)}")
    print(f"  Excluded                 : {len(excluded)}")
    print(f"  Not retrieved (unscreened): {len(not_retrieved)}")
    print("=" * 60)

    need_pdf = [p for p in included if not _has_fulltext(p)]
    have_ft = [p for p in included if _has_fulltext(p)]

    print(f"\n── INCLUDED with full text ({len(have_ft)}) — nothing to do ──")
    for p in have_ft:
        print(f"   {p} | {(S.get(p, {}).get('title') or '')[:72]}")

    print(f"\n── ★ INCLUDED but NEED A PDF ({len(need_pdf)}) — get these for extraction ──")
    for p in need_pdf:
        s = S.get(p, {})
        print(f"   {p} | {(s.get('title') or '')[:64]} | DOI: {s.get('doi', '') or '-'}")

    print(f"\n── NOT RETRIEVED ({len(not_retrieved)}) — get these to classify (no abstract) ──")
    for p in not_retrieved:
        s = S.get(p, {})
        print(f"   {p or '(no PMID)'} | {(s.get('title') or '')[:64]} | DOI: {s.get('doi', '') or '-'}")


if __name__ == "__main__":
    main()
