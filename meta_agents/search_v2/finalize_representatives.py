#!/usr/bin/env python3
"""Lock the one-representative-per-registry-family selection for the MAIN
quantitative synthesis, operating on the unified extraction ledger
(breast_extraction.csv) rather than on ft_eligibility alone.

Rationale (Feedback 5): US population-based registries are nested
(county subset of state subset of SEER subset of NAACCR subset of USCS), so
multiple studies of the same race/ethnicity group draw on overlapping cases
and are NOT independent. For each analytic cell (outcome dimension x minority
group) we therefore keep ONE representative per registry FAMILY and route the
rest to the all-included sensitivity analysis.

Representative criteria, in Feedback-5 order (most comprehensive first):
  1. an IRR must exist : rate-only rows (no computable ratio) cannot represent.
  2. coverage tier    : USCS(~99%) > NAACCR(~93%) > SEER-national(~48%)
                        > state registry > California-CCR/regional
                        > single sub-registry (Hawaii/LA/Greater Bay)  [largest,
                        most comprehensive region/sample]
  3. period           : most recent end-year, then longest span
  4. provenance       : directly-reported-IRR / -SIR / -with-CI  >  Poisson-SE
                        >  computed-from-rates (no CI)  [clear age-std / CI]
The SEER-Explorer by-race anchor rows are reference/descriptive and never a
main-analysis representative (registry-direct, non-independent by construction).

Output: TableSA_main_representatives.csv  (one row per ledger estimate, with
family, tier, cluster = outcome|group|family, main_analysis flag, reason).
"""
import csv
import os
import re
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
LEDGER = os.path.join(HERE, "breast_extraction.csv")
OUT = os.path.join(HERE, "TableSA_main_representatives.csv")


def registry_family(reg):
    """Return (display_family, coverage_tier, family_class).

    family_class groups registries that are NON-INDEPENDENT (nested subsets of
    the same national case pool) so they collapse to ONE main representative:
      - "national": USCS >= NAACCR >= SEER >= state >= California-CCR >= single
        SEER sub-registry (Hawaii/LA/Greater Bay). All draw on overlapping cases.
      - "IHS-PRCDA": Indian Health Service-linked AIAN cases - a distinct
        population definition, so it may coexist with a national representative.
    """
    s = reg.lower()
    if "ihs" in s or "prcda" in s:
        return ("IHS-PRCDA", 5, "IHS-PRCDA")
    if "uscs" in s or "50-state" in s or "npcr" in s:
        return ("USCS(NPCR+SEER ~99%)", 9, "national")
    if "naaccr" in s or "multi-state" in s or "cina" in s:
        return ("NAACCR/CiNA (~93%)", 8, "national")
    if "florida" in s:
        return ("State: Florida", 4, "national")
    if "wisconsin" in s:
        return ("State: Wisconsin", 4, "national")
    if "greater bay" in s:
        return ("California-CCR: Greater Bay Area", 2, "national")
    if "la county" in s:
        return ("California-CCR: LA County", 2, "national")
    if "california" in s:
        return ("California-CCR", 3, "national")
    if "hawaii" in s:
        return ("Hawaii Tumor Registry (SEER)", 2, "national")
    if "seer" in s:               # plain SEER national (9/13/17/18/21/22)
        return ("SEER-national", 6, "national")
    return ("Other/unspecified", 1, "national")


PROV_RANK = {
    "directly-reported-IRR": 4, "directly-reported-SIR": 4,
    "computed-from-rates-with-CI": 3,
    "directly-reported-rate": 3,
    "computed-from-rates-Poisson-SE": 2,
    "computed-from-rates": 1,
}


def period_key(p):
    """(most-recent-year, span). Handles ranges 'YYYY-YYYY' and single 'YYYY'."""
    yrs = [int(y) for y in re.findall(r"(19\d\d|20\d\d)", p or "")]
    if not yrs:
        return (0, 0)
    return (max(yrs), max(yrs) - min(yrs))


def main():
    from guard_v2_only import check_ledger
    bad = check_ledger()
    if bad:
        raise SystemExit("CONTAMINATION: non-v2 records in ledger: %s" % dict(bad))
    QUARANTINE = {"UNVERIFIED", "UNVERIFIED-table", "NO-FULLTEXT"}
    rows = [r for r in csv.DictReader(open(LEDGER, encoding="utf-8"))
            if r.get("verification", "") not in QUARANTINE]
    for r in rows:
        fam, tier, fclass = registry_family(r["registry"])
        r["_family"] = fam
        r["_tier"] = tier
        r["_fclass"] = fclass
        # Cluster on family CLASS (nested-national collapses to one), so the
        # main analysis keeps one national representative per outcome x group,
        # plus a separate IHS-PRCDA representative where applicable.
        r["_cluster"] = "%s | %s | %s" % (r["outcome_dim"], r["minority_group"], fclass)
        r["_is_anchor"] = (r["record_id"] == "SEER-EXPL")

    # Representative per cluster (outcome x group x registry-family), excluding
    # the SEER-Explorer anchor rows.
    clusters = defaultdict(list)
    for r in rows:
        if not r["_is_anchor"]:
            clusters[r["_cluster"]].append(r)

    def score(r):
        has_irr = 1 if (r.get("irr") or "").strip() else 0
        return (has_irr,
                r["_tier"],
                period_key(r["period"]),
                PROV_RANK.get(r["provenance"], 0))

    rep_id = {}
    for cl, members in clusters.items():
        best = max(members, key=score)
        rep_id[cl] = id(best)

    # AIAN correction: unlinked national registries (USCS/SEER/NAACCR) racially
    # MISCLASSIFY and undercount AIAN incidence; the IHS-PRCDA linkage is the
    # field-standard, more valid source. Where an IHS-PRCDA AIAN representative
    # exists for the same outcome dimension, demote the national AIAN
    # representative to an undercount-flagged overlap (Feedback 5: not merely
    # "most comprehensive coverage" but the most VALID population definition).
    def is_aian(r):
        s = (r["minority_group"] + " " + r["outcome_dim"]).lower()
        return "aian" in s or "american indian" in s or "alaska nativ" in s
    ihs_aian_dims = {r["outcome_dim"] for r in rows
                     if is_aian(r) and r["_fclass"] == "IHS-PRCDA"
                     and rep_id.get(r["_cluster"]) == id(r)}

    out = []
    for r in rows:
        if r["_is_anchor"]:
            main_flag, reason = "no (registry-direct anchor)", "SEER-Explorer reference, not a screened study"
        elif (is_aian(r) and r["_fclass"] == "national"
              and r["outcome_dim"] in ihs_aian_dims
              and rep_id.get(r["_cluster"]) == id(r)):
            main_flag = "no (AIAN undercount)"
            reason = "unlinked national registry undercounts AIAN; IHS-PRCDA representative preferred"
        elif rep_id.get(r["_cluster"]) == id(r):
            n = len(clusters[r["_cluster"]])
            main_flag = "yes (representative)"
            reason = ("best of %d in cell by provenance/coverage/period" % n) if n > 1 else "sole estimate in cell"
        else:
            main_flag = "no (overlaps representative)"
            reason = "collapses to cell representative (same outcome x group x family)"
        out.append({
            "record_id": r["record_id"], "author_year": r["author_year"],
            "outcome_dim": r["outcome_dim"], "minority_group": r["minority_group"],
            "registry_family": r["_family"], "coverage_tier": r["_tier"],
            "period": r["period"], "provenance": r["provenance"],
            "irr": r["irr"], "irr_ci_lo": r["irr_ci_lo"], "irr_ci_hi": r["irr_ci_hi"],
            "cluster": r["_cluster"], "main_analysis": main_flag,
            "representative_reason": reason,
        })

    out.sort(key=lambda x: (x["outcome_dim"], x["minority_group"],
                            -x["coverage_tier"], x["record_id"]))
    cols = ["record_id", "author_year", "outcome_dim", "minority_group",
            "registry_family", "coverage_tier", "period", "provenance",
            "irr", "irr_ci_lo", "irr_ci_hi", "cluster", "main_analysis",
            "representative_reason"]
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)

    reps = sum(1 for x in out if x["main_analysis"].startswith("yes"))
    anch = sum(1 for x in out if "anchor" in x["main_analysis"])
    print("ledger estimates: %d" % len(out))
    print("main-analysis representatives: %d" % reps)
    print("registry-direct anchors (excluded): %d" % anch)
    print("overlap (sensitivity-only): %d" % (len(out) - reps - anch))
    # show the representative set per outcome dimension
    from collections import Counter
    dimc = Counter(x["outcome_dim"] for x in out if x["main_analysis"].startswith("yes"))
    print("\nrepresentatives by outcome dimension:")
    for k, v in dimc.most_common():
        print("  %-26s %d" % (k, v))


if __name__ == "__main__":
    main()
