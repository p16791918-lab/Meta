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

NOTE: records are keyed the SAME way the pipeline keys them (_rec_key):
PMID if present, else a title hash. Keying by raw PMID would collapse every
no-PMID Embase record onto the single key "" and badly undercount both the
"advanced" and "included" tallies (this used to make the report disagree with
the orchestrator's own PRISMA numbers).
"""
import glob
import hashlib
import json
import os
import re
import sys


def _key(rec) -> str:
    """PMID if present, else a title hash — matches agent_2_screening._rec_key."""
    pmid = str(rec.get("pmid", "")).strip()
    if pmid:
        return pmid
    title = re.sub(r"\W+", " ", str(rec.get("title", "")).lower()).strip()
    return "T:" + hashlib.sha1(title.encode("utf-8")).hexdigest()[:12]


def _load_jsonl(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def _has_fulltext(pmid, fulltext_dir="fulltext"):
    """True only for a real numeric PMID with a local .txt/.pdf on disk.
    No-PMID records (key 'T:...') never match, so they surface as need-PDF."""
    pmid = str(pmid).strip()
    if not pmid or pmid.startswith("T:"):
        return False
    return (os.path.exists(os.path.join(fulltext_dir, pmid + ".txt"))
            or os.path.exists(os.path.join(fulltext_dir, pmid + ".pdf")))


def _disp_pmid(s) -> str:
    """Human-readable PMID for display, or '(no PMID)'."""
    raw = str(s.get("pmid", "")).strip()
    if not raw:
        return "(no PMID)"
    m = re.match(r"\d+", raw)
    return m.group() if m else raw


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
    S = {_key(s): s for s in studies}

    p1 = _load_jsonl(os.path.join(cache_dir, "phase1.jsonl"))
    p2 = _load_jsonl(os.path.join(cache_dir, "phase2.jsonl"))

    # restrict to the current frozen search set (by key)
    cur = set(S.keys())
    if cur:
        p1 = [d for d in p1 if _key(d) in cur]
    advanced = {_key(d) for d in p1 if d.get("phase1_decision") != "exclude"}
    p2_by = {_key(d): d for d in p2}

    included = [k for k in advanced if p2_by.get(k, {}).get("phase2_decision") == "include"]
    excluded = [k for k in advanced if p2_by.get(k, {}).get("phase2_decision") == "exclude"]
    # advanced but never full-text screened (no full text AND no abstract): not in p2
    not_retrieved = [k for k in advanced if k not in p2_by]

    print("=" * 60)
    print(f"  Identified (after dedup) : {len(studies)}")
    print(f"  Advanced past abstract   : {len(advanced)}")
    print(f"  Included                 : {len(included)}")
    print(f"  Excluded                 : {len(excluded)}")
    print(f"  Not retrieved (unscreened): {len(not_retrieved)}")
    print("=" * 60)

    need_pdf = [k for k in included if not _has_fulltext(k)]
    have_ft = [k for k in included if _has_fulltext(k)]

    print(f"\n── INCLUDED with full text ({len(have_ft)}) — nothing to do ──")
    for k in have_ft:
        s = S.get(k, {})
        print(f"   {_disp_pmid(s)} | {(s.get('title') or '')[:72]}")

    print(f"\n── ★ INCLUDED but NEED A PDF ({len(need_pdf)}) — get these for extraction ──")
    for k in need_pdf:
        s = S.get(k, {})
        print(f"   {_disp_pmid(s)} | {(s.get('title') or '')[:64]} | DOI: {s.get('doi', '') or '-'}")

    print(f"\n── NOT RETRIEVED ({len(not_retrieved)}) — get these to classify (no abstract) ──")
    for k in not_retrieved:
        s = S.get(k, {})
        print(f"   {_disp_pmid(s)} | {(s.get('title') or '')[:64]} | DOI: {s.get('doi', '') or '-'}")


if __name__ == "__main__":
    main()
