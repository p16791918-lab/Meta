#!/usr/bin/env python3
"""Phase C — sensitivity analyses for the breast-cancer incidence disparities review.

Addresses the central threat to the aggregate pooled estimates: the US cancer
registries overlap (SEER ⊂ NAACCR ⊂ USCS; LA County ⊂ California ⊂ SEER…), so the
random-effects CI is falsely narrow and studies are NOT independent. For each main
comparison we report, alongside the primary random-effects (REML + Hartung–Knapp) estimate:

  FE            fixed-effect (inverse-variance) — method robustness
  LOO           leave-one-out pooled IRR range — influence of any single study
  drop no-CI    excludes studies whose SE was Poisson-approximated (no reported CI)
  1-per-family  one estimate per registry family (removes the double-counting)
  best-source   the single most comprehensive source (USCS ~99% US coverage)

Run:  python sensitivity_analysis.py
"""
import math
from run_meta_analysis_breast import STUDIES, _subset, random_effects_meta

# ── registry-family map (which sources share underlying case data) ───────────
FAMILY = {
    "SEER 17": "SEER", "SEER 18": "SEER", "SEER": "SEER",
    "SEER Hawaii": "SEER-Hawaii",            # Hawaii SEER — geographically distinct
    "LA County SEER": "California", "LA County CSP": "California",
    "California CR": "California",
    "USCS": "USCS",                          # SEER+NPCR national composite
    "NAACCR": "NAACCR",                      # ~93% US composite
    "Wisconsin CRS": "Wisconsin",
    "IHS-linked": "IHS",
}
# studies whose SE was approximated from rates (no reported rate-ratio CI)
NO_CI_SOURCES = {"USCS", "Wisconsin CRS"}


def fixed_effects(studies):
    """Inverse-variance fixed-effect pooled log-IRR."""
    w = [1 / s.se ** 2 for s in studies]
    theta = sum(wi * s.log_irr for wi, s in zip(w, studies)) / sum(w)
    se = math.sqrt(1 / sum(w))
    return math.exp(theta), math.exp(theta - 1.96 * se), math.exp(theta + 1.96 * se)


def _fmt(irr, lo, hi):
    return f"{irr:.3f} ({lo:.3f}-{hi:.3f})"


def leave_one_out(studies):
    """Range of the random-effects pooled IRR when each study is dropped in turn."""
    if len(studies) < 3:
        return None
    irrs = []
    for i in range(len(studies)):
        sub = studies[:i] + studies[i + 1:]
        r = random_effects_meta(sub, method="REML", knha=True)
        irrs.append((r["irr"], studies[i].id))
    lo = min(irrs, key=lambda x: x[0])
    hi = max(irrs, key=lambda x: x[0])
    return lo, hi


def one_per_family(studies):
    """Keep one study per registry family (largest inverse-variance weight)."""
    best = {}
    for s in studies:
        fam = FAMILY.get(s.source, s.source)
        if fam not in best or (1 / s.se ** 2) > (1 / best[fam].se ** 2):
            best[fam] = s
    return list(best.values())


def analyze(group, outcome="invasive_incidence", label=None):
    ss = _subset(group, outcome)
    if len(ss) < 2:
        return
    label = label or group
    print(f"\n{'─'*74}\n  {label}  (k={len(ss)})\n{'─'*74}")

    prim = random_effects_meta(ss, method="REML", knha=True)
    print(f"  {'Primary (REML + Hartung–Knapp)':<34} {_fmt(prim['irr'], prim['ci_low'], prim['ci_high'])}"
          f"   I²={prim['I2']:.0f}%")

    fe = fixed_effects(ss)
    print(f"  {'Fixed-effect (inverse-variance)':<34} {_fmt(*fe)}")

    loo = leave_one_out(ss)
    if loo:
        (lo_irr, lo_id), (hi_irr, hi_id) = loo
        print(f"  {'Leave-one-out pooled range':<34} {lo_irr:.3f} – {hi_irr:.3f}"
              f"   (low drops {lo_id.split('_')[-1]}, high drops {hi_id.split('_')[-1]})")

    with_ci = [s for s in ss if s.source not in NO_CI_SOURCES]
    if 2 <= len(with_ci) < len(ss):
        r = random_effects_meta(with_ci, method="REML", knha=True)
        print(f"  {'Excl. approximated-SE (no CI)':<34} {_fmt(r['irr'], r['ci_low'], r['ci_high'])}"
              f"   (k={len(with_ci)})")

    fam = one_per_family(ss)
    if 2 <= len(fam) < len(ss):
        r = random_effects_meta(fam, method="REML", knha=True)
        fams = ",".join(sorted({FAMILY.get(s.source, s.source) for s in fam}))
        print(f"  {'One estimate per registry family':<34} {_fmt(r['irr'], r['ci_low'], r['ci_high'])}"
              f"   (k={len(fam)}: {fams})")

    # single most comprehensive national source, if present
    best = next((s for s in ss if s.source == "USCS"), None)
    if best:
        print(f"  {'Best single source (USCS ~99%)':<34} "
              f"{_fmt(best.irr, best.ci_low, best.ci_high)}   [{best.id.split('_')[-1]}]")


def run():
    print("=" * 74)
    print("  SENSITIVITY ANALYSES — robustness of pooled minority-vs-NHW IRRs")
    print("=" * 74)
    for g in ["Black", "Hispanic", "Asian", "AIAN"]:
        analyze(g, "invasive_incidence", f"Invasive incidence — {g} vs NHW")
    analyze("Black", "tnbc_incidence", "TNBC — Black vs NHW")
    analyze("Black", "hrneg_incidence", "HR/ER-negative — Black vs NHW")
    print("\n" + "=" * 74)
    print("  Interpretation: where the primary, FE, LOO, drop-no-CI, and")
    print("  one-per-family estimates agree, the disparity direction is robust")
    print("  to the registry-overlap and SE-approximation concerns.")
    print("=" * 74)


if __name__ == "__main__":
    run()
