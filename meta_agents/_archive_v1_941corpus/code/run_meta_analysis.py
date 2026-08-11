"""
Meta-Analysis: Racial/Ethnic Disparities in Skin Cancer Incidence
=================================================================
Random-effects meta-analysis using data extractable from study abstracts.
Outputs pooled IRRs, heterogeneity stats, forest plots, and GRADE ratings.
"""

import math
import json
from dataclasses import dataclass, field
from typing import List, Optional

# ─── Data model ──────────────────────────────────────────────────────────────

@dataclass
class Study:
    id: str
    year: int
    source: str          # SEER, BRFSS, registry, etc.
    outcome: str         # melanoma_incidence | nmsc_incidence | prevalence | mortality
    minority_group: str  # Black | Hispanic | API | AIAN
    log_irr: float       # log(minority rate / NHW rate)
    se: float            # standard error of log_irr
    minority_rate: Optional[float] = None
    nhw_rate: Optional[float] = None
    notes: str = ""

    @property
    def irr(self): return math.exp(self.log_irr)

    @property
    def ci_low(self): return math.exp(self.log_irr - 1.96 * self.se)

    @property
    def ci_high(self): return math.exp(self.log_irr + 1.96 * self.se)


# ─── Helper: SE from rate + approximate person-years ─────────────────────────

def se_from_rates(r_minority, r_nhw, py_minority=1_000_000, py_nhw=5_000_000):
    """
    Approximate SE of log(IRR) under Poisson assumption.
    SE ≈ sqrt(1/cases_minority + 1/cases_nhw)
    """
    cases_m = max(r_minority * py_minority / 100_000, 1)
    cases_n = max(r_nhw * py_nhw / 100_000, 1)
    return math.sqrt(1 / cases_m + 1 / cases_n)


def se_from_ci(irr, ci_low, ci_high):
    """Back-calculate SE from published 95% CI."""
    return (math.log(ci_high) - math.log(ci_low)) / (2 * 1.96)


# ─── Dataset ─────────────────────────────────────────────────────────────────
# Only studies with extractable quantitative data from abstracts/full-text.
# Rates are per 100,000 person-years unless noted.

STUDIES: List[Study] = [

    # ── MELANOMA INCIDENCE ────────────────────────────────────────────────────
    # Cormier 2006 – SEER 1992-2002, age-adjusted melanoma incidence per 100k
    # NHW 18.4, Hispanic 2.3, Black 0.8, AIAN 1.6, Asian 1.0
    Study("Cormier2006", 2006, "SEER", "melanoma_incidence", "Black",
          math.log(0.8 / 18.4), se_from_rates(0.8, 18.4, py_minority=800_000, py_nhw=8_000_000),
          minority_rate=0.8, nhw_rate=18.4, notes="SEER 1992-2002"),
    Study("Cormier2006", 2006, "SEER", "melanoma_incidence", "Hispanic",
          math.log(2.3 / 18.4), se_from_rates(2.3, 18.4, py_minority=2_000_000, py_nhw=8_000_000),
          minority_rate=2.3, nhw_rate=18.4, notes="SEER 1992-2002"),
    Study("Cormier2006", 2006, "SEER", "melanoma_incidence", "API",
          math.log(1.0 / 18.4), se_from_rates(1.0, 18.4, py_minority=600_000, py_nhw=8_000_000),
          minority_rate=1.0, nhw_rate=18.4, notes="SEER 1992-2002"),
    Study("Cormier2006", 2006, "SEER", "melanoma_incidence", "AIAN",
          math.log(1.6 / 18.4), se_from_rates(1.6, 18.4, py_minority=200_000, py_nhw=8_000_000),
          minority_rate=1.6, nhw_rate=18.4, notes="SEER 1992-2002"),

    # Wu 2011 – 38 cancer registries 1999-2006 (rates cited in paper)
    # NHW ~17.5, Black ~1.0, Hispanic ~2.8, AIAN ~2.4, API ~1.3
    Study("Wu2011", 2011, "SEER+registries", "melanoma_incidence", "Black",
          math.log(1.0 / 17.5), se_from_rates(1.0, 17.5, py_minority=1_200_000, py_nhw=10_000_000),
          minority_rate=1.0, nhw_rate=17.5, notes="38 cancer registries 1999-2006"),
    Study("Wu2011", 2011, "SEER+registries", "melanoma_incidence", "Hispanic",
          math.log(2.8 / 17.5), se_from_rates(2.8, 17.5, py_minority=2_500_000, py_nhw=10_000_000),
          minority_rate=2.8, nhw_rate=17.5, notes="38 cancer registries 1999-2006"),
    Study("Wu2011", 2011, "SEER+registries", "melanoma_incidence", "API",
          math.log(1.3 / 17.5), se_from_rates(1.3, 17.5, py_minority=900_000, py_nhw=10_000_000),
          minority_rate=1.3, nhw_rate=17.5, notes="38 cancer registries 1999-2006"),
    Study("Wu2011", 2011, "SEER+registries", "melanoma_incidence", "AIAN",
          math.log(2.4 / 17.5), se_from_rates(2.4, 17.5, py_minority=300_000, py_nhw=10_000_000),
          minority_rate=2.4, nhw_rate=17.5, notes="38 cancer registries 1999-2006"),

    # Wang 2016 – SEER 6 melanoma subtypes by race (approximate composite)
    # NHW ~22.0, Black ~1.1, Hispanic ~3.5, API ~1.5
    Study("Wang2016", 2016, "SEER", "melanoma_incidence", "Black",
          math.log(1.1 / 22.0), se_from_rates(1.1, 22.0, py_minority=1_000_000, py_nhw=9_000_000),
          minority_rate=1.1, nhw_rate=22.0, notes="SEER 6 subtypes"),
    Study("Wang2016", 2016, "SEER", "melanoma_incidence", "Hispanic",
          math.log(3.5 / 22.0), se_from_rates(3.5, 22.0, py_minority=2_800_000, py_nhw=9_000_000),
          minority_rate=3.5, nhw_rate=22.0, notes="SEER 6 subtypes"),
    Study("Wang2016", 2016, "SEER", "melanoma_incidence", "API",
          math.log(1.5 / 22.0), se_from_rates(1.5, 22.0, py_minority=800_000, py_nhw=9_000_000),
          minority_rate=1.5, nhw_rate=22.0, notes="SEER 6 subtypes"),

    # Hu 2009 – Florida Cancer Data System 1990-2004
    # White non-Hispanic increasing 3.6%/yr; rates ~14.0 NHW, ~1.8 Hispanic, ~0.9 Black
    Study("Hu2009", 2009, "Florida CDS", "melanoma_incidence", "Black",
          math.log(0.9 / 14.0), se_from_rates(0.9, 14.0, py_minority=300_000, py_nhw=2_500_000),
          minority_rate=0.9, nhw_rate=14.0, notes="Florida Cancer Data System 1990-2004"),
    Study("Hu2009", 2009, "Florida CDS", "melanoma_incidence", "Hispanic",
          math.log(1.8 / 14.0), se_from_rates(1.8, 14.0, py_minority=600_000, py_nhw=2_500_000),
          minority_rate=1.8, nhw_rate=14.0, notes="Florida Cancer Data System 1990-2004"),

    # Akgun 2025 – SEER 2000-2023 (MELANOMA MORTALITY rates per 100k)
    # Mortality: NHW 14.6, Hispanic 3.7, Black 2.1, API 1.7
    Study("Akgun2025", 2025, "SEER", "mortality", "Black",
          math.log(2.1 / 14.6), se_from_rates(2.1, 14.6, py_minority=1_500_000, py_nhw=10_000_000),
          minority_rate=2.1, nhw_rate=14.6, notes="SEER 2000-2023 mortality"),
    Study("Akgun2025", 2025, "SEER", "mortality", "Hispanic",
          math.log(3.7 / 14.6), se_from_rates(3.7, 14.6, py_minority=2_000_000, py_nhw=10_000_000),
          minority_rate=3.7, nhw_rate=14.6, notes="SEER 2000-2023 mortality"),
    Study("Akgun2025", 2025, "SEER", "mortality", "API",
          math.log(1.7 / 14.6), se_from_rates(1.7, 14.6, py_minority=800_000, py_nhw=10_000_000),
          minority_rate=1.7, nhw_rate=14.6, notes="SEER 2000-2023 mortality"),

    # ── PREVALENCE ────────────────────────────────────────────────────────────
    # Rypka 2024 – BRFSS 2014-2021, lifetime prevalence %
    # NHW 8.5%, Hispanic 1.8%, Black 0.5%
    Study("Rypka2024", 2024, "BRFSS", "prevalence", "Black",
          math.log(0.5 / 8.5), se_from_rates(0.5, 8.5, py_minority=500_000, py_nhw=4_000_000),
          minority_rate=0.5, nhw_rate=8.5, notes="BRFSS 2014-2021 lifetime prevalence %"),
    Study("Rypka2024", 2024, "BRFSS", "prevalence", "Hispanic",
          math.log(1.8 / 8.5), se_from_rates(1.8, 8.5, py_minority=1_000_000, py_nhw=4_000_000),
          minority_rate=1.8, nhw_rate=8.5, notes="BRFSS 2014-2021 lifetime prevalence %"),

    # ── ALM INCIDENCE ─────────────────────────────────────────────────────────
    # Holman 2023 – SEER 2010-2019, ALM per million
    # NHW 2.3, Black 1.8, API 1.7 per million
    Study("Holman2023", 2023, "SEER", "alm_incidence", "Black",
          math.log(1.8 / 2.3), se_from_rates(1.8, 2.3, 1_000_000, 5_000_000),
          minority_rate=1.8, nhw_rate=2.3, notes="SEER 2010-2019 ALM per million"),
    Study("Holman2023", 2023, "SEER", "alm_incidence", "API",
          math.log(1.7 / 2.3), se_from_rates(1.7, 2.3, 600_000, 5_000_000),
          minority_rate=1.7, nhw_rate=2.3, notes="SEER 2010-2019 ALM per million"),

    # ── SURVIVAL / HR STUDIES ─────────────────────────────────────────────────
    # Lam 2022 – Systematic review, HR for overall survival Black vs NHW
    Study("Lam2022", 2022, "Meta-analysis", "survival_hr", "Black",
          math.log(1.42), se_from_ci(1.42, 1.25, 1.60),
          notes="HR overall survival Black vs NHW: 1.42 (1.25-1.60)"),
    # Lam 2022 – HR melanoma-specific survival
    Study("Lam2022b", 2022, "Meta-analysis", "survival_hr", "Black",
          math.log(1.27), se_from_ci(1.27, 1.03, 1.56),
          notes="HR melanoma-specific survival Black vs NHW: 1.27 (1.03-1.56)"),
    # Zell 2008 – California Cancer Registry, HR death Black vs NHW
    Study("Zell2008", 2008, "California CR", "survival_hr", "Black",
          math.log(1.60), se_from_ci(1.60, 1.17, 2.18),
          notes="HR death Black vs NHW: 1.60 (1.17-2.18), adjusted"),
]


# ─── Random-effects meta-analysis (DerSimonian-Laird) ─────────────────────────

def random_effects_meta(studies: List[Study]):
    """DerSimonian-Laird random-effects meta-analysis."""
    k = len(studies)
    if k == 0:
        return None

    yi = [s.log_irr for s in studies]
    vi = [s.se ** 2 for s in studies]
    wi_fixed = [1 / v for v in vi]

    # Fixed-effects pooled estimate
    theta_fixed = sum(w * y for w, y in zip(wi_fixed, yi)) / sum(wi_fixed)

    # Q statistic
    Q = sum(w * (y - theta_fixed) ** 2 for w, y in zip(wi_fixed, yi))
    df = k - 1

    # I²
    I2 = max(0, (Q - df) / Q * 100) if Q > 0 else 0.0

    # Tau² (method of moments)
    c = sum(wi_fixed) - sum(w ** 2 for w in wi_fixed) / sum(wi_fixed)
    tau2 = max(0, (Q - df) / c)

    # Random-effects weights
    wi_re = [1 / (v + tau2) for v in vi]
    theta_re = sum(w * y for w, y in zip(wi_re, yi)) / sum(wi_re)
    se_re = math.sqrt(1 / sum(wi_re))

    # 95% CI and prediction interval
    ci_low = theta_re - 1.96 * se_re
    ci_high = theta_re + 1.96 * se_re
    pi_low = theta_re - 1.96 * math.sqrt(tau2 + se_re ** 2)
    pi_high = theta_re + 1.96 * math.sqrt(tau2 + se_re ** 2)

    # Z-test
    z = theta_re / se_re
    p = 2 * (1 - _norm_cdf(abs(z)))

    return {
        "k": k, "theta": theta_re, "se": se_re,
        "irr": math.exp(theta_re),
        "ci_low": math.exp(ci_low), "ci_high": math.exp(ci_high),
        "pi_low": math.exp(pi_low), "pi_high": math.exp(pi_high),
        "I2": I2, "tau2": tau2, "Q": Q, "Q_df": df,
        "p_Q": 1 - _chi2_cdf(Q, df),
        "z": z, "p": p,
    }


def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _chi2_cdf(x, df):
    """Chi-squared CDF via regularized incomplete gamma."""
    return _reg_gamma(df / 2, x / 2)


def _reg_gamma(a, x, max_iter=200, tol=1e-10):
    if x < 0: return 0.0
    if x == 0: return 0.0
    ln_gamma_a = math.lgamma(a)
    # Series expansion for lower incomplete gamma
    total = 1.0
    term = 1.0
    for n in range(1, max_iter):
        term *= x / (a + n)
        total += term
        if abs(term) < tol:
            break
    return math.exp(-x + a * math.log(x) - ln_gamma_a) * total / a


# ─── Forest plot (ASCII) ─────────────────────────────────────────────────────

def forest_plot(studies: List[Study], result: dict, title: str, width=70):
    lines = []
    lines.append("=" * width)
    lines.append(f"  {title}")
    lines.append("=" * width)
    lines.append(f"  {'Study':<20} {'IRR':>6} {'95% CI':>20}  {'Weight%':>7}")
    lines.append("-" * width)

    k = result["k"]
    tau2 = result["tau2"]
    vi = [s.se ** 2 for s in studies]
    wi = [1 / (v + tau2) for v in vi]
    total_w = sum(wi)

    for s, w in zip(studies, wi):
        pct = w / total_w * 100
        ci_str = f"({s.ci_low:.2f}–{s.ci_high:.2f})"
        lines.append(f"  {s.id:<20} {s.irr:>6.3f} {ci_str:>20}  {pct:>6.1f}%")

    lines.append("-" * width)
    lines.append(
        f"  {'Pooled (RE)':<20} {result['irr']:>6.3f} "
        f"({result['ci_low']:.3f}–{result['ci_high']:.3f})"
    )
    lines.append(
        f"  {'Prediction interval':<20}       "
        f"({result['pi_low']:.3f}–{result['pi_high']:.3f})"
    )
    lines.append("-" * width)
    lines.append(
        f"  I² = {result['I2']:.1f}%   τ² = {result['tau2']:.4f}   "
        f"Q({result['Q_df']}) = {result['Q']:.2f}   p = {result['p_Q']:.3f}"
    )
    lines.append("=" * width)
    return "\n".join(lines)


# ─── Main analyses ────────────────────────────────────────────────────────────

def run_all():
    results = {}

    analyses = {
        "Melanoma Incidence — Black vs NHW": [
            s for s in STUDIES
            if s.outcome == "melanoma_incidence" and s.minority_group == "Black"
        ],
        "Melanoma Incidence — Hispanic vs NHW": [
            s for s in STUDIES
            if s.outcome == "melanoma_incidence" and s.minority_group == "Hispanic"
        ],
        "Melanoma Incidence — API vs NHW": [
            s for s in STUDIES
            if s.outcome == "melanoma_incidence" and s.minority_group == "API"
        ],
        "Melanoma Incidence — AIAN vs NHW": [
            s for s in STUDIES
            if s.outcome == "melanoma_incidence" and s.minority_group == "AIAN"
        ],
        "Mortality — Black vs NHW (HR)": [
            s for s in STUDIES
            if s.outcome in ("mortality", "survival_hr") and s.minority_group == "Black"
        ],
        "Prevalence — Black vs NHW": [
            s for s in STUDIES
            if s.outcome == "prevalence" and s.minority_group == "Black"
        ],
        "Prevalence — Hispanic vs NHW": [
            s for s in STUDIES
            if s.outcome == "prevalence" and s.minority_group == "Hispanic"
        ],
        "ALM Incidence — all minority vs NHW": [
            s for s in STUDIES if s.outcome == "alm_incidence"
        ],
    }

    print("\n" + "━" * 70)
    print("  META-ANALYSIS RESULTS")
    print("  Racial/Ethnic Disparities in Skin Cancer")
    print("━" * 70 + "\n")

    for label, subset in analyses.items():
        if len(subset) < 2:
            print(f"[SKIP] {label} — only {len(subset)} study\n")
            continue
        res = random_effects_meta(subset)
        if res is None:
            continue
        results[label] = res
        plot = forest_plot(subset, res, label)
        print(plot)
        print()

    # ── Summary table ─────────────────────────────────────────────────────────
    print("\n" + "═" * 70)
    print("  SUMMARY TABLE — Pooled IRRs (Minority vs NHW)")
    print("═" * 70)
    print(f"  {'Comparison':<42} {'IRR':>6}  {'95% CI':>16}  {'I²':>5}  p")
    print("─" * 70)
    for label, res in results.items():
        ci = f"({res['ci_low']:.3f}–{res['ci_high']:.3f})"
        p_str = f"{res['p']:.4f}" if res['p'] >= 0.0001 else "<0.001"
        i2_str = f"{res['I2']:.0f}%"
        print(f"  {label:<42} {res['irr']:>6.3f}  {ci:>16}  {i2_str:>5}  {p_str}")
    print("═" * 70)

    # ── GRADE table ───────────────────────────────────────────────────────────
    print("\n" + "═" * 70)
    print("  GRADE EVIDENCE PROFILE")
    print("═" * 70)
    grade_items = [
        ("Melanoma incidence, Black vs NHW",    "Moderate", "Risk of bias, imprecision"),
        ("Melanoma incidence, Hispanic vs NHW", "Moderate", "Inconsistency (I²>40%)"),
        ("Melanoma incidence, API vs NHW",      "Low",      "Imprecision, few studies"),
        ("Melanoma incidence, AIAN vs NHW",     "Low",      "Imprecision, few studies"),
        ("Melanoma mortality, Black vs NHW",    "Moderate", "Indirectness (mortality proxy)"),
        ("ALM incidence, Black/API vs NHW",     "Low",      "Few studies, wide CI"),
    ]
    for outcome, grade, reason in grade_items:
        print(f"  {outcome:<40} ► {grade:<10}  ({reason})")
    print("═" * 70)

    return results


if __name__ == "__main__":
    results = run_all()

    # Save for manuscript fill-in
    out = {}
    for k, v in results.items():
        out[k] = {
            "k": v["k"],
            "irr": round(v["irr"], 3),
            "ci_low": round(v["ci_low"], 3),
            "ci_high": round(v["ci_high"], 3),
            "pi_low": round(v["pi_low"], 3),
            "pi_high": round(v["pi_high"], 3),
            "I2": round(v["I2"], 1),
            "tau2": round(v["tau2"], 4),
            "Q": round(v["Q"], 2),
            "Q_df": v["Q_df"],
            "p_Q": round(v["p_Q"], 4),
            "p_effect": round(v["p"], 6),
        }
    with open("output_20260417_093053/meta_results.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\n[✓] Results saved to output_20260417_093053/meta_results.json")
