#!/usr/bin/env python3
"""Generate the full-text screening + extraction template for the 242 includes.

Produces ft_screening_log.csv, pre-filled with what we already know (record_id,
year, title, publication series, a best-guess registry family) and with EMPTY
columns for the author to complete at the full-text stage:

  ft_decision   : include | exclude
  ft_reason     : one of the four full-text exclusion categories (blank if include)
  registry_family / diagnosis_years / minority_group / minority_rate(+CI) /
  nhw_rate(+CI) / irr(+CI) / source_location / notes

The four full-text exclusion categories (mirror the reference PRISMA template's
eligibility box; keep these EXACT):
  - Did not report the outcome of interest
  - Ineligible population
  - Overlapping or duplicate dataset
  - Full text unavailable

This script FILLS NOTHING it cannot derive from the existing metadata — every
eligibility decision and every extracted rate is left blank for the author to
enter against the source PDF (single-reviewer + AI-assist methodology).

Usage:  python3 ft_screen_template.py
"""
import csv
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
MERGED = os.path.join(HERE, "merged_unique.csv")
DECISIONS = os.path.join(HERE, "screening_decisions.csv")
CHARACT = os.path.join(HERE, "includes_characterization.csv")
OUT = os.path.join(HERE, "ft_screening_log.csv")

FT_CATEGORIES = [
    "Did not report the outcome of interest",
    "Ineligible population",
    "Overlapping or duplicate dataset",
    "Full text unavailable",
]


def registry_family(title, abstract):
    """Best-guess registry family from title/abstract, for overlap dedup.
    Author confirms at full text. Order matters (most specific first)."""
    s = (title + " " + abstract).lower()
    if re.search(r"annual report to the nation", s):
        return "ARN (SEER+NPCR aggregate)"
    if re.search(r"\bus cancer statistics\b|uscs|invasive cancer incidence.*united states", s):
        return "USCS (NPCR+SEER)"
    if re.search(r"\bnaaccr\b", s):
        return "NAACCR"
    if re.search(r"alaska native tumou?r registry|alaska native|alaska earth", s):
        return "Alaska Native Registry"
    if re.search(r"navajo", s):
        return "Navajo/IHS"
    if re.search(r"california cancer registry|\bccr\b|california,? (19|20)\d\d|california hispanic|greater bay area", s):
        return "California Cancer Registry"
    if re.search(r"multiethnic cohort|\bmec\b", s):
        return "Multiethnic Cohort"
    if re.search(r"nih-aarp|\baarp\b", s):
        return "NIH-AARP cohort"
    if re.search(r"kaiser", s):
        return "Kaiser Permanente cohort"
    for st in ["michigan", "wisconsin", "pennsylvania", "connecticut", "new mexico",
               "texas", "north carolina", "florida", "detroit", "minnesota",
               "massachusetts", "arizona", "hawaii", "guam", "new jersey"]:
        if st in s:
            return "State/regional: %s" % st
    if re.search(r"\bseer\b|surveillance,? epidemiology", s):
        return "SEER"
    return "UNSPECIFIED (confirm at full text)"


def main():
    dec = {int(r["record_id"]): r for r in csv.DictReader(open(DECISIONS, encoding="utf-8"))}
    recs = list(csv.DictReader(open(MERGED, encoding="utf-8")))
    series = {}
    if os.path.exists(CHARACT):
        for r in csv.DictReader(open(CHARACT, encoding="utf-8")):
            series[int(r["record_id"])] = r.get("series", "")

    inc = sorted(i for i in dec if dec[i]["decision"] == "include")
    cols = ["record_id", "year", "series", "registry_family_guess", "pmid", "doi",
            "title",
            # --- author fills below ---
            "ft_decision", "ft_reason",
            "registry_family_confirmed", "diagnosis_years",
            "minority_group", "minority_rate", "minority_ci",
            "nhw_rate", "nhw_ci", "irr", "irr_ci",
            "source_location", "notes"]

    rows = []
    for i in inc:
        r = recs[i]
        rows.append({
            "record_id": i,
            "year": r.get("year", ""),
            "series": series.get(i, ""),
            "registry_family_guess": registry_family(r.get("title", ""), r.get("abstract", "") or ""),
            "pmid": r.get("pmid", ""),
            "doi": r.get("doi", ""),
            "title": r.get("title", ""),
            "ft_decision": "", "ft_reason": "",
            "registry_family_confirmed": "", "diagnosis_years": "",
            "minority_group": "", "minority_rate": "", "minority_ci": "",
            "nhw_rate": "", "nhw_ci": "", "irr": "", "irr_ci": "",
            "source_location": "", "notes": "",
        })

    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)

    from collections import Counter
    print("wrote %s with %d rows" % (OUT, len(rows)))
    print("\nFT exclusion categories (fill ft_reason with one of these when excluding):")
    for c in FT_CATEGORIES:
        print("  -", c)
    print("\nregistry-family guess distribution (author confirms at full text):")
    for k, v in Counter(x["registry_family_guess"] for x in rows).most_common():
        print("  %3d  %s" % (v, k))


if __name__ == "__main__":
    main()
