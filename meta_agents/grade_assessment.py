#!/usr/bin/env python3
"""Phase C — GRADE-style certainty (summary of findings) for the key comparisons.

Population-based registry incidence data are near-complete censuses of cases, so
we start observational surveillance evidence at a higher baseline than a typical
cohort and rate certainty on: risk of bias, inconsistency, indirectness,
imprecision, and other (publication bias / registry overlap). Pooled estimates
are read live from the meta-analysis so the table cannot drift from the data.
"""
from run_meta_analysis_breast import _subset, random_effects_meta

HIGH, MOD, LOW, VLOW = "⊕⊕⊕⊕ High", "⊕⊕⊕⊝ Moderate", "⊕⊕⊝⊝ Low", "⊕⊝⊝⊝ Very low"


def pooled(group, outcome="invasive_incidence"):
    ss = _subset(group, outcome)
    if len(ss) >= 2:
        r = random_effects_meta(ss)
        return r["irr"], r["ci_low"], r["ci_high"], r["I2"], len(ss)
    s = ss[0]
    return s.irr, s.ci_low, s.ci_high, 0.0, 1


# (label, group, outcome, certainty, downgrade/upgrade rationale, plain-language)
FINDINGS = [
    ("Black vs NHW — invasive (aggregate)", "Black", "invasive_incidence", MOD,
     "−1 inconsistency (I²≈99%) but direction robust to all sensitivity analyses; large registries",
     "Near-parity overall (IRR~0.93) — but this aggregate is an average of opposing age/subtype patterns"),
    ("Hispanic vs NHW — invasive", "Hispanic", "invasive_incidence", MOD,
     "−1 inconsistency (magnitude, not direction); consistent across every registry family",
     "Substantially lower incidence (~0.68), robust"),
    ("Asian/API vs NHW — invasive (aggregate)", "Asian", "invasive_incidence", LOW,
     "−1 inconsistency, −1 indirectness (the 'Asian/API' label pools ethnicities that differ ~3×)",
     "The aggregate ~0.76 is not a meaningful quantity — it hides Korean 0.34 ↔ Native Hawaiian 1.11"),
    ("AIAN vs NHW — invasive", "AIAN", "invasive_incidence", MOD,
     "−1 inconsistency; IHS linkage corrects the well-known AIAN registry undercount (raises certainty)",
     "Lower incidence (~0.70); registry-only estimates understate it vs IHS-linked"),
    ("TNBC — Black vs NHW", "Black", "tnbc_incidence", MOD,
     "−1 inconsistency (I²=92%) but +1 large effect (~2×); consistent direction",
     "Black women have ~2× the incidence of triple-negative breast cancer — a robust, large disparity"),
    ("HR/ER-negative — Black vs NHW", "Black", "hrneg_incidence", MOD,
     "−1 inconsistency but +1 large effect; two independent data sources agree (1.66, 1.80)",
     "Black excess concentrates in aggressive ER-negative disease (~1.7×)"),
]


def run():
    print("=" * 96)
    print("  GRADE SUMMARY OF FINDINGS — certainty of the evidence")
    print("=" * 96)
    print(f"  {'Comparison':<42}{'IRR (95% CI)':<22}{'k':>3}  {'I²':>4}  Certainty")
    print("  " + "-" * 92)
    for label, g, oc, cert, rationale, plain in FINDINGS:
        irr, lo, hi, i2, k = pooled(g, oc)
        ci = f"{irr:.2f} ({lo:.2f}-{hi:.2f})"
        print(f"  {label:<42}{ci:<22}{k:>3}  {i2:>3.0f}%  {cert}")
        print(f"      ↳ {rationale}")
        print(f"      → {plain}")
        print()
    print("=" * 96)
    print("  Headline certainty statement:")
    print("  • HIGH certainty that the aggregate 'Asian/API' category masks large")
    print("    (~3×) between-ethnicity variation — the review's central point.")
    print("  • MODERATE certainty for each aggregate racial comparison and for the")
    print("    Black excess in aggressive (TNBC / ER-negative) subtypes.")
    print("  • Certainty is limited chiefly by between-study inconsistency driven by")
    print("    registry/period/region differences — not by study quality or by")
    print("    imprecision (large population-based registries).")
    print("=" * 96)


if __name__ == "__main__":
    run()
