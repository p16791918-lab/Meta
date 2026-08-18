#!/usr/bin/env python3
"""Main-text Table 1: headline IRR (vs non-Hispanic White) by racial/ethnic group
and analytic dimension, in the supervisor's format — Effect type + Risk estimate
[low, high] + RoB (Newcastle-Ottawa) + GRADE. One headline representative per
(dimension x group); full per-estimate detail lives in the Supplementary tables.
"""
import csv
from labels import disp_group
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
LED = os.path.join(HERE, "breast_extraction.csv")
ROB = os.path.join(OUT, "TableS_risk_of_bias.csv")

DIMS = [
    ("aggregate-vs-NHW", "Overall invasive breast cancer"),
    ("disaggregated-AANHPI", "Asian American / Native Hawaiian / Pacific Islander subgroups"),
    ("Hispanic-origin", "Hispanic/Latina by country of origin"),
    ("AIAN", "American Indian and Alaska Native (AI/AN) by region"),
    ("disaggregated-MENA", "Middle Eastern"),
    ("subtype-TNBC", "Triple-negative breast cancer"),
    ("male-BC", "Male breast cancer"),
]


def main():
    qual = {r["record_id"]: r["Overall_quality"]
            for r in csv.DictReader(open(ROB, encoding="utf-8"))}
    prov = {}
    for r in csv.DictReader(open(LED, encoding="utf-8")):
        prov[(r["record_id"], r["outcome_dim"], r["minority_group"], r["irr"])] = \
            (r["provenance"], r["author_year"], r["period"])

    # collect representatives per (dim, group)
    cells = defaultdict(list)
    for r in csv.DictReader(open(REPS, encoding="utf-8")):
        if r["main_analysis"].startswith("yes"):
            cells[(r["outcome_dim"], r["minority_group"])].append(r)

    def pick(cands):
        # prefer: has CI, Good RoB, highest coverage tier
        def key(r):
            has_ci = 1 if (r["irr_ci_lo"].strip() and r["irr_ci_hi"].strip()) else 0
            good = 1 if qual.get(r["record_id"]) == "Good" else 0
            return (has_ci, good, int(r["coverage_tier"]))
        return max(cands, key=key)

    DROP = {("aggregate-vs-NHW", "Black (women)")}  # duplicate aggregate Black
    rows = []
    for dim, dlabel in DIMS:
        members = {g: pick(cs) for (d, g), cs in cells.items()
                   if d == dim and (d, g) not in DROP
                   and "young" not in g.lower()  # drop age-restricted subgroups (conflate age x ethnicity)
                   # the AI/AN-by-region section shows regions only; the national
                   # AI/AN aggregate is already the Overall row (avoid a duplicate
                   # "AI/AN" label with a different value in the same table).
                   and not (dim == "AIAN" and g == "AIAN")}
        # sort by IRR ascending, but push aggregate/summary rows to the bottom of the section
        def irrval(g):
            try:
                return float(members[g]["irr"])
            except ValueError:
                return 99
        def is_summary(g):
            # Push an umbrella aggregate to the bottom of sections that list subgroups
            # PLUS their aggregate: the by-country Hispanic section, and each Asian /
            # NHPI block of the AANHPI section (where the block aggregate should be the
            # last row under its subgroups). In the Overall section the four groups are
            # peers (no subgroup list), so nothing is a summary there — sort by IRR.
            return (dim in ("Hispanic-origin", "disaggregated-AANHPI")
                    and "aggregate" in g.lower())
        NHPI_KEYS = ("hawaiian", "guamanian", "chamorro", "samoan", "pacific islander")
        def is_nhpi(g):
            return any(k in g.lower() for k in NHPI_KEYS)
        def seclabel(g):
            # split the AANHPI block into Asian vs NHPI so the reader can see which
            # detailed groups are Asian and which are Pacific Islander.
            if dim == "disaggregated-AANHPI":
                return ("Native Hawaiian and Pacific Islander (NHPI) subgroups"
                        if is_nhpi(g) else "Asian American subgroups")
            return dlabel
        def sortkey(g):
            if dim == "disaggregated-AANHPI":
                return (1 if is_nhpi(g) else 0, 1 if is_summary(g) else 0, irrval(g))
            return (1 if is_summary(g) else 0, irrval(g))
        for g in sorted(members, key=sortkey):
            r = members[g]
            if not r["irr"].strip():
                continue  # no usable point estimate
            lo, hi = r["irr_ci_lo"].strip(), r["irr_ci_hi"].strip()
            est = "%s [%s, %s]" % (r["irr"], lo, hi) if (lo and hi) else (r["irr"] + " (point est.)")
            # mark rows whose reference is an unstratified White group (not NHW)
            cv = r.get("comparison_vs", "").strip()
            if cv and cv not in ("NHW", "White (NH)", "NHW (external SEER-Explorer)") \
                    and not cv.startswith("foreign-born"):
                est += " †"
            pv, auth, period = prov.get((r["record_id"], dim, g, r["irr"]),
                                        ("", r["record_id"], r["period"]))
            eff = "SIR" if "SIR" in pv else "IRR"
            rows.append(dict(dimension=seclabel(g), group=g, effect=eff, estimate=est,
                             study=auth, period=period,
                             registry=r.get("registry_family", ""),
                             rob=qual.get(r["record_id"], "NA")))

    cols = ["dimension", "group", "effect", "estimate", "study", "period", "registry", "rob"]
    with open(os.path.join(OUT, "Table1_main.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    with open(os.path.join(OUT, "Table1_main.md"), "w", encoding="utf-8") as f:
        f.write("# Table 1. Incidence rate ratios of invasive breast cancer among "
                "U.S. racial/ethnic groups relative to non-Hispanic White women\n\n")
        f.write("Values are the representative population-based estimate per group "
                "(one per registry family). Effect measure: IRR unless noted (SIR). "
                "RoB = risk of bias.\n\n")
        cur = None
        for r in rows:
            if r["dimension"] != cur:
                cur = r["dimension"]
                f.write("\n**%s**\n\n| Group | Effect | Estimate [95%% CI] | "
                        "Representative study | Registry | RoB |\n"
                        "|----|----|----|----|----|----|\n" % cur)
            f.write("| %s | %s | %s | %s (%s) | %s | %s |\n" % (
                r["group"], r["effect"], r["estimate"], r["study"], r["period"],
                r["registry"], r["rob"]))
    print("wrote outputs/Table1_main.(csv/md) — %d rows" % len(rows))


if __name__ == "__main__":
    main()
