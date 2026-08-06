#!/usr/bin/env python3
"""Tally a screening decision log into PRISMA 2020 counts.

Reads a decision log (CSV) and produces the numbers the PRISMA figure needs:
per-database identification, duplicates removed, records screened/excluded with
the exclusion **display categories** (title/abstract), and reports assessed/
excluded with the full-text display categories. The per-record log stays granular
(sub_reason); this only aggregates it — matching how the example paper reports
aggregate counts in the flowchart while we keep an auditable log behind it.

Expected CSV columns (see SCREENING_PLAN.md):
    record_id, source_db, title, doi, pmid, stage, decision,
    display_reason, sub_reason, note
  stage    ∈ {TA, FT}                         (title/abstract vs full text)
  decision ∈ {include, exclude, dup}          (dup = duplicate removed pre-screening)
  display_reason ∈ the fixed category lists below (empty when include)

Usage:  python3 tally_prisma.py screening_decisions.csv
"""
import csv
import sys
from collections import Counter, OrderedDict

# Fixed display categories (must match SCREENING_PLAN.md exactly)
TA_CATEGORIES = [
    "Not relevant to the research question/topic",
    "Not a US population-based/registry study",
    "Editorials, commentaries, letters, or conference abstracts",
]
FT_CATEGORIES = [
    "Did not report the outcome of interest",
    "Ineligible population",
    "Overlapping or duplicate dataset",
    "Full text unavailable",
]


def load(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def tally(rows):
    by_db = Counter()
    dups = 0
    ta_screened = ta_excluded = 0
    ft_assessed = ft_excluded = 0
    included = 0
    ta_reasons = Counter()
    ft_reasons = Counter()
    unknown = []  # display_reason not in the fixed lists

    for r in rows:
        stage = (r.get("stage") or "").strip().upper()
        dec = (r.get("decision") or "").strip().lower()
        reason = (r.get("display_reason") or "").strip()
        db = (r.get("source_db") or "").strip() or "unknown"

        if dec == "dup":
            dups += 1
            continue
        by_db[db] += 1  # count unique records fed to screening, by originating DB

        if stage == "TA":
            ta_screened += 1
            if dec == "exclude":
                ta_excluded += 1
                ta_reasons[reason] += 1
                if reason not in TA_CATEGORIES:
                    unknown.append(("TA", r.get("record_id"), reason))
        elif stage == "FT":
            ft_assessed += 1
            if dec == "exclude":
                ft_excluded += 1
                ft_reasons[reason] += 1
                if reason not in FT_CATEGORIES:
                    unknown.append(("FT", r.get("record_id"), reason))
            elif dec == "include":
                included += 1
    return locals()


def render(t):
    out = []
    out.append("=" * 64)
    out.append("  PRISMA 2020 — counts from the screening decision log")
    out.append("=" * 64)
    out.append("\nIdentification — records identified, by database:")
    total_id = 0
    for db, n in sorted(t["by_db"].items()):
        out.append(f"    {db:<24} n = {n}")
        total_id += n
    out.append(f"    {'TOTAL identified':<24} n = {total_id}")
    out.append(f"    Duplicate records removed before screening: n = {t['dups']}")

    out.append("\nScreening (title/abstract):")
    out.append(f"    Records screened:  n = {t['ta_screened']}")
    out.append(f"    Records excluded:  n = {t['ta_excluded']}, by reason:")
    for cat in TA_CATEGORIES:
        out.append(f"        {cat}  (n = {t['ta_reasons'].get(cat, 0)})")

    out.append("\nEligibility (full text):")
    out.append(f"    Reports assessed:  n = {t['ft_assessed']}")
    out.append(f"    Reports excluded:  n = {t['ft_excluded']}, by reason:")
    for cat in FT_CATEGORIES:
        out.append(f"        {cat}  (n = {t['ft_reasons'].get(cat, 0)})")

    out.append("\nIncluded:")
    out.append(f"    Studies included:  n = {t['included']}")

    if t["unknown"]:
        out.append("\n[!] display_reason values not in the fixed category lists "
                   "(fix these before publishing):")
        for stage, rid, reason in t["unknown"]:
            out.append(f"        {stage}  {rid}  ->  {reason!r}")
    out.append("=" * 64)
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    rows = load(sys.argv[1])
    print(render(tally(rows)))
