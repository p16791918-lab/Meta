#!/usr/bin/env python3
"""GRADE certainty-of-evidence assessment for each representative outcome
(IRR vs non-Hispanic White), matching the domains in the supervisor's example
Appendix (Study limitations/RoB, Inconsistency, Indirectness, Imprecision,
Publication bias; upgrade for Large magnitude of effect).

GRADE for a body of OBSERVATIONAL (registry/population-based) evidence:
  Start = LOW (baseline score 0; supervisor GRADE-informed convention).
  Downgrade (-1 each):
    - Risk of bias      : representative study rated Poor (Newcastle-Ottawa).
    - Inconsistency     : all-included estimates for the cell disagree in
                          DIRECTION (some clearly <1, some clearly >1). The very
                          high I2 from overlapping registries is NOT counted as
                          inconsistency (it is a non-independence artifact).
    - Indirectness      : not serious here (U.S. population-based registries
                          directly measure age-adjusted incidence by race) -> 0.
    - Imprecision       : no confidence interval available (point estimate only),
                          or the 95% CI crosses 1 for a cell whose point estimate
                          is within 0.90-1.11.
    - Publication bias  : not serious (registry data are census-like, not subject
                          to selective publication) -> 0.
  Upgrade (observational):
    - Large magnitude   : +1 if IRR <=0.5 or >=2.0; +2 if IRR <=0.2 or >=5.0.
  Final = start - downgrades + upgrades, then:
          High (>= 2) / Moderate (1) / Low (0) / Very low (<= -1).

NOTE: AI-generated first pass; reviewer to spot-check (as for RoB). Evidence-class
(Ioannidis) grading from the example is umbrella-review-specific and is NOT applied.
"""
import csv
import math
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")
LED = os.path.join(HERE, "breast_extraction.csv")
ROB = os.path.join(OUT, "TableS_risk_of_bias.csv")
SENS = os.path.join(OUT, "Table_sensitivity_I2.csv")


def main():
    qual = {r["record_id"]: r["Overall_quality"]
            for r in csv.DictReader(open(ROB, encoding="utf-8"))}
    # all-included estimates per (dim,group) to judge direction inconsistency
    allirr = defaultdict(list)
    for r in csv.DictReader(open(LED, encoding="utf-8")):
        if r["record_id"] == "SEER-EXPL":
            continue
        try:
            allirr[(r["outcome_dim"], r["minority_group"])].append(float(r["irr"]))
        except ValueError:
            pass
    sensI2 = {(r["dimension"], r["group"]): r["I2"]
              for r in csv.DictReader(open(SENS, encoding="utf-8"))}

    rows = []
    for r in csv.DictReader(open(REPS, encoding="utf-8")):
        if not r["main_analysis"].startswith("yes"):
            continue
        dim, grp = r["outcome_dim"], r["minority_group"]
        irr = r["irr"].strip()
        lo, hi = r["irr_ci_lo"].strip(), r["irr_ci_hi"].strip()
        start = 0  # baseline Low = 0 (supervisor GRADE-informed convention)
        down = {}
        # risk of bias
        rob = qual.get(r["record_id"], "NA")
        down["RoB"] = 1 if rob == "Poor" else 0
        # inconsistency (direction disagreement among all-included)
        vals = allirr.get((dim, grp), [])
        below = sum(1 for v in vals if v < 0.95)
        above = sum(1 for v in vals if v > 1.05)
        inconsist = 1 if (below >= 1 and above >= 1 and len(vals) >= 2) else 0
        down["Inconsistency"] = inconsist
        # indirectness
        down["Indirectness"] = 0
        # imprecision
        imp = 0
        if not (lo and hi):
            imp = 1
        else:
            try:
                f = float(irr)
                if float(lo) < 1.0 < float(hi) and 0.90 <= f <= 1.11:
                    imp = 1
            except ValueError:
                pass
        down["Imprecision"] = imp
        # publication bias
        down["PubBias"] = 0
        # upgrade large magnitude
        up = 0
        try:
            f = float(irr)
            if f <= 0.2 or f >= 5.0:
                up = 2
            elif f <= 0.5 or f >= 2.0:
                up = 1
        except ValueError:
            pass
        total = start - sum(down.values()) + up
        # supervisor scoring rule: High >= 2, Moderate = 1, Low = 0, Very low <= -1
        cert = ("High" if total >= 2 else "Moderate" if total == 1
                else "Low" if total == 0 else "Very low")
        est = "%s [%s, %s]" % (irr, lo, hi) if (irr and lo and hi) else (irr or "NR")
        rows.append(dict(dimension=dim, group=grp, record=r["record_id"],
                         IRR=est, rob=rob,
                         d_RoB=down["RoB"], d_Incons=down["Inconsistency"],
                         d_Indirect=down["Indirectness"], d_Imprec=down["Imprecision"],
                         d_PubBias=down["PubBias"], up_LargeEffect=up,
                         I2_allincl=sensI2.get((dim, grp), "single"),
                         GRADE=cert))
    order = {"aggregate-vs-NHW": 0, "disaggregated-AANHPI": 1, "disaggregated-MENA": 2,
             "Hispanic-origin": 3, "AIAN": 4, "male-BC": 5}
    rows.sort(key=lambda x: (order.get(x["dimension"], 9), x["group"]))
    cols = ["dimension", "group", "record", "IRR", "rob", "d_RoB", "d_Incons",
            "d_Indirect", "d_Imprec", "d_PubBias", "up_LargeEffect",
            "I2_allincl", "GRADE"]
    with open(os.path.join(OUT, "TableS_GRADE.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
    from collections import Counter
    c = Counter(x["GRADE"] for x in rows)
    with open(os.path.join(OUT, "TableS_GRADE.md"), "w", encoding="utf-8") as f:
        f.write("# Table S. GRADE certainty of evidence (IRR vs non-Hispanic White)\n\n")
        f.write("Observational bodies of evidence start at Low. Downgrades: RoB, "
                "inconsistency (direction disagreement, NOT the registry-overlap I2), "
                "indirectness, imprecision, publication bias. Upgrade: large "
                "magnitude (IRR<=0.5 or >=2.0: +1; <=0.2 or >=5.0: +2). "
                "**AI-generated first pass — reviewer to spot-check.**\n\n")
        f.write("Distribution: %s\n\n" % dict(c))
        f.write("| Dimension | Group | IRR [95%% CI] | RoB | -RoB | -Incons | -Imprec | +Large | GRADE |\n")
        f.write("|----|----|----|----|----|----|----|----|----|\n")
        for x in rows:
            f.write("| %s | %s | %s | %s | %d | %d | %d | +%d | **%s** |\n" % (
                x["dimension"], x["group"], x["IRR"], x["rob"], x["d_RoB"],
                x["d_Incons"], x["d_Imprec"], x["up_LargeEffect"], x["GRADE"]))
    print("wrote outputs/TableS_GRADE (%d outcomes)" % len(rows))
    print("GRADE distribution:", dict(c))


if __name__ == "__main__":
    main()
