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
import csv
import glob
import hashlib
import json
import os
import re
import sys

from cache_utils import file_key

# Analyst decisions that override the automated screening (e.g. a paper the
# pipeline marked "include" on its abstract but which, on closer reading, is a
# conference abstract / wrong subtype / has no usable data). Lives in the repo
# so it travels to the Codespace on `git pull`. See _load_overrides.
OVERRIDES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "manual_decisions.csv")


def _norm(t) -> str:
    return re.sub(r"\W+", " ", str(t or "").lower()).strip()


def _num_pmid(raw) -> str:
    m = re.match(r"\d+", str(raw or "").strip())
    return m.group() if m else ""


def _key(rec) -> str:
    """PMID if present, else a title hash — matches agent_2_screening._rec_key."""
    pmid = str(rec.get("pmid", "")).strip()
    if pmid:
        return pmid
    return "T:" + hashlib.sha1(_norm(rec.get("title", "")).encode("utf-8")).hexdigest()[:12]


def _load_overrides(path=OVERRIDES_PATH):
    """Load analyst decisions: list of {decision, reason, pmid, doi, title}."""
    if not os.path.exists(path):
        return []
    out = []
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dec = (row.get("decision") or "").strip().lower()
            if dec in ("exclude", "include"):
                out.append({
                    "decision": dec,
                    "reason": (row.get("reason") or "").strip(),
                    "pmid": _num_pmid(row.get("pmid")),
                    "doi": _norm(row.get("doi")),
                    "title": _norm(row.get("title")),
                })
    return out


def _match_override(study, overrides):
    """Return the first override matching this study.

    Each override matches by its most specific identifier only: a PMID-keyed
    override matches by PMID, a DOI-keyed one by DOI, and a title-only one by
    title (exact or prefix). This keeps the readable title on a PMID/DOI-keyed
    row from ever false-matching a different study.
    """
    spmid = _num_pmid(study.get("pmid"))
    sdoi = _norm(study.get("doi"))
    stitle = _norm(study.get("title"))
    for ov in overrides:
        if ov["pmid"]:
            if spmid and ov["pmid"] == spmid:
                return ov
            continue
        if ov["doi"]:
            if sdoi and ov["doi"] == sdoi:
                return ov
            continue
        t = ov["title"]
        if t and len(t) >= 20 and stitle and (stitle == t
                                              or stitle.startswith(t)
                                              or t.startswith(stitle)):
            return ov
    return None


def _load_jsonl(path):
    if not os.path.exists(path):
        return []
    return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]


def _has_fulltext(s, fulltext_dir="fulltext"):
    """True if this study's local .txt/.pdf exists, by its filesystem key
    (numeric PMID, or 'T_<hash>' for no-PMID papers)."""
    fk = file_key(s.get("pmid", ""), s.get("title", ""))
    return (os.path.exists(os.path.join(fulltext_dir, fk + ".txt"))
            or os.path.exists(os.path.join(fulltext_dir, fk + ".pdf")))


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

    # ── Apply analyst overrides (manual_decisions.csv) ────────────────────────
    overrides = _load_overrides()
    manual_ex, manual_inc = {}, {}      # key -> reason
    if overrides:
        for k in advanced:
            ov = _match_override(S.get(k, {}), overrides)
            if not ov:
                continue
            if ov["decision"] == "exclude":
                manual_ex[k] = ov["reason"]
            else:
                manual_inc[k] = ov["reason"]
        # remove analyst-excluded from the automated buckets
        included = [k for k in included if k not in manual_ex]
        not_retrieved = [k for k in not_retrieved if k not in manual_ex]
        excluded = [k for k in excluded if k not in manual_ex]
        # analyst force-includes: ensure present in included, absent elsewhere
        for k in manual_inc:
            if k not in included:
                included.append(k)
        not_retrieved = [k for k in not_retrieved if k not in manual_inc]
        excluded = [k for k in excluded if k not in manual_inc]

    total_excluded = len(excluded) + len(manual_ex)

    print("=" * 60)
    print(f"  Identified (after dedup) : {len(studies)}")
    print(f"  Advanced past abstract   : {len(advanced)}")
    print(f"  Included                 : {len(included)}")
    print(f"  Excluded                 : {total_excluded}"
          + (f"  (incl. {len(manual_ex)} analyst)" if manual_ex else ""))
    print(f"  Not retrieved (unscreened): {len(not_retrieved)}")
    print("=" * 60)

    if manual_ex or manual_inc:
        print(f"\n── ANALYST OVERRIDES (manual_decisions.csv) ──")
        for k, reason in manual_ex.items():
            s = S.get(k, {})
            print(f"   EXCLUDE  {_disp_pmid(s)} | {(s.get('title') or '')[:52]}")
            print(f"            ↳ {reason[:96]}")
        for k, reason in manual_inc.items():
            s = S.get(k, {})
            print(f"   INCLUDE  {_disp_pmid(s)} | {(s.get('title') or '')[:52]}")
            print(f"            ↳ {reason[:96]}")

    need_pdf = [k for k in included if not _has_fulltext(S.get(k, {}))]
    have_ft = [k for k in included if _has_fulltext(S.get(k, {}))]

    print(f"\n── INCLUDED with full text ({len(have_ft)}) — nothing to do ──")
    for k in have_ft:
        s = S.get(k, {})
        print(f"   {_disp_pmid(s)} | {(s.get('title') or '')[:72]}")

    print(f"\n── ★ INCLUDED but NEED A PDF ({len(need_pdf)}) — get these for extraction ──")
    for k in need_pdf:
        s = S.get(k, {})
        fk = file_key(s.get("pmid", ""), s.get("title", ""))
        print(f"   {_disp_pmid(s)} | {(s.get('title') or '')[:60]} | DOI: {s.get('doi', '') or '-'}")
        print(f"       → save as: fulltext/{fk}.pdf")

    print(f"\n── NOT RETRIEVED ({len(not_retrieved)}) — get these to classify (no abstract) ──")
    for k in not_retrieved:
        s = S.get(k, {})
        print(f"   {_disp_pmid(s)} | {(s.get('title') or '')[:64]} | DOI: {s.get('doi', '') or '-'}")


if __name__ == "__main__":
    main()
