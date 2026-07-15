"""
Meta-Analysis: Racial/Ethnic Disparities in Breast Cancer INCIDENCE
===================================================================
Random-effects meta-analysis (DerSimonian-Laird) of the within-study
incidence rate ratio  IRR = (minority age-adjusted rate) / (NHW rate).

Scope (locked decisions):
  • Outcome        : INVASIVE breast cancer INCIDENCE only.
                     NOT prevalence (confounded by survival), NOT mortality,
                     NOT survival HRs. Never pool incidence with prevalence.
  • Rates          : age-standardized / age-adjusted, per 100,000 person-years.
  • Method A       : within-study IRR = minority_rate / nhw_rate (reference NHW).
                     Method B (cross-study rate pooling) is a fallback only if
                     the within-study pairs are too sparse — not used here yet.
  • Excluded       : male breast cancer, DCIS/in-situ-only, crude (non-adjusted)
                     rates, single-race studies with no NHW comparator.
  • Optional        : TNBC / ER-negative subtype as a separate stratum.

HOW THE DATA GETS IN
--------------------
Agent 3's automated extractor returns NULL for age-adjusted rate tables, so
the `STUDIES` list below is filled BY HAND from the full text of each INCLUDED
study (Claude reads methods/results and transcribes the rate table). Until that
extraction is done the list is empty and this script simply reports that it is
awaiting data — it does NOT invent numbers.

Each row is one minority-vs-NHW comparison from one study. A study that reports
Black, Hispanic, and Asian rates against the same NHW reference contributes
THREE rows (one per minority_group), all citing the same `id`.
"""

import math
import json
import os
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

OUTPUT_DIR = "output_breast"

# ─── Data model ──────────────────────────────────────────────────────────────

@dataclass
class Study:
    id: str              # first-author + year, e.g. "Smith2019"
    year: int
    source: str          # SEER, NPCR, state registry, etc.
    outcome: str         # invasive_incidence | tnbc_incidence  (incidence only)
    minority_group: str  # Black | Hispanic | Asian | AIAN
    log_irr: float       # log(minority age-adj rate / NHW age-adj rate)
    se: float            # standard error of log_irr
    minority_rate: Optional[float] = None   # per 100,000 person-years
    nhw_rate: Optional[float] = None         # per 100,000 person-years
    notes: str = ""

    @property
    def irr(self): return math.exp(self.log_irr)

    @property
    def ci_low(self): return math.exp(self.log_irr - 1.96 * self.se)

    @property
    def ci_high(self): return math.exp(self.log_irr + 1.96 * self.se)


# ─── SE helpers ──────────────────────────────────────────────────────────────

def se_from_rates(r_minority, r_nhw, py_minority=1_000_000, py_nhw=5_000_000):
    """
    Approximate SE of log(IRR) under a Poisson assumption when the paper gives
    rates but no CI:  SE ≈ sqrt(1/cases_minority + 1/cases_nhw), with
    cases = rate * person-years / 100,000.

    Use realistic person-years for the population/period if the paper reports
    them; the defaults are placeholders and will understate/overstate precision.
    """
    cases_m = max(r_minority * py_minority / 100_000, 1)
    cases_n = max(r_nhw * py_nhw / 100_000, 1)
    return math.sqrt(1 / cases_m + 1 / cases_n)


def se_from_ci(irr, ci_low, ci_high):
    """Back-calculate SE of log(IRR) from a published 95% CI (preferred)."""
    return (math.log(ci_high) - math.log(ci_low)) / (2 * 1.96)


def irr_from_rates(r_minority, r_nhw):
    """Convenience: log(IRR) from two rates."""
    return math.log(r_minority / r_nhw)


def se_logirr_from_rate_cis(r_m, lo_m, hi_m, r_n, lo_n, hi_n):
    """SE of log(IRR) when the paper gives a 95% CI for EACH rate (not the IRR).
    Treats the two age-standardized rates as independent:
       SE(log r) = (ln hi - ln lo) / (2*1.96);  SE(log IRR) = sqrt(SE_m^2 + SE_n^2).
    """
    se_m = (math.log(hi_m) - math.log(lo_m)) / (2 * 1.96)
    se_n = (math.log(hi_n) - math.log(lo_n)) / (2 * 1.96)
    return math.sqrt(se_m ** 2 + se_n ** 2)


# ─── Dataset — FILL FROM FULL-TEXT EXTRACTION ────────────────────────────────
# Populate one Study(...) per minority-vs-NHW comparison. Prefer se_from_ci when
# the paper reports a 95% CI for the rate ratio; fall back to se_from_rates only
# when just point rates (+ ideally person-years) are given.
#
# Template (delete the leading '#' and fill in real values):
#   Study("Author2021", 2021, "SEER", "invasive_incidence", "Black",
#         irr_from_rates(126.0, 133.0), se_from_ci(0.95, 0.93, 0.97),
#         minority_rate=126.0, nhw_rate=133.0, notes="SEER 2015-2019, age-adj"),

STUDIES: List[Study] = [

    # ── 41082230 — "Breast Cancer Incidence Rates in Ghanaian and US Black
    #    Women From 2013 to 2017" (SEER 17). Full-text Table 2, age-standardized
    #    (Segi world std), women 20–74, 2013–2015 (US SEER comparison window).
    #    NHB 148.5 (146.4–150.7); NHW 152.9 (151.9–153.8) per 100,000.
    #    (Ghana/GBHS 84.4 excluded — a foreign population, not a US racial minority.)
    Study("PMID41082230", 2024, "SEER 17", "invasive_incidence", "Black",
          irr_from_rates(148.5, 152.9),
          se_logirr_from_rate_cis(148.5, 146.4, 150.7, 152.9, 151.9, 153.8),
          minority_rate=148.5, nhw_rate=152.9,
          notes="SEER17 2013-2015, age-std Segi world, 20-74y; full-text Table 2"),

    # ── 35025856 — Ellington et al., MMWR 2022 "Trends in Breast Cancer
    #    Incidence, by Race, Ethnicity, and Age — United States, 1999–2018"
    #    (USCS = SEER+NPCR, ~99% of US pop). Age-adjusted rates per 100,000,
    #    year 2018 (Table). NHW 186.5; NHB 174.0; Hispanic 134.0; A/PI 143.5;
    #    AI/AN 127.3. No rate CIs in source → SE is Poisson-approx from
    #    annualized national case counts (rates are extremely stable, ~99% cover).
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "Black",
          irr_from_rates(174.0, 186.5),
          se_from_rates(174.0, 186.5, py_minority=12_980_000, py_nhw=89_600_000),
          minority_rate=174.0, nhw_rate=186.5, notes="USCS 2018; SE Poisson-approx"),
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "Hispanic",
          irr_from_rates(134.0, 186.5),
          se_from_rates(134.0, 186.5, py_minority=11_380_000, py_nhw=89_600_000),
          minority_rate=134.0, nhw_rate=186.5, notes="USCS 2018; SE Poisson-approx"),
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "Asian",
          irr_from_rates(143.5, 186.5),
          se_from_rates(143.5, 186.5, py_minority=5_080_000, py_nhw=89_600_000),
          minority_rate=143.5, nhw_rate=186.5, notes="USCS 2018 A/PI (incl. PI); SE Poisson-approx"),
    Study("MMWR2022_35025856", 2022, "USCS", "invasive_incidence", "AIAN",
          irr_from_rates(127.3, 186.5),
          se_from_rates(127.3, 186.5, py_minority=798_000, py_nhw=89_600_000),
          minority_rate=127.3, nhw_rate=186.5, notes="USCS 2018; SE Poisson-approx"),

    # ── T_e7879b363303 — "Incidence trends in triple-negative breast cancer
    #    among women in the US" (full paper, 14pp). Age-adjusted TNBC incidence
    #    per 100,000: Black 33.8, White 17.5, Hispanic 14.7, AIAN 14.7, Asian ~12.
    #    Black vs White TNBC IRR 1.93 (1.88–1.97). SUBTYPE stratum (not primary).
    Study("TNBC_Te7879b3", 2023, "SEER/USCS", "tnbc_incidence", "Black",
          math.log(1.93), se_from_ci(1.93, 1.88, 1.97),
          minority_rate=33.8, nhw_rate=17.5,
          notes="TNBC subtype; Black vs White IRR 1.93 (1.88-1.97); full-text; citation TBD"),

]


# ─── Random-effects meta-analysis (DerSimonian-Laird) ─────────────────────────

def random_effects_meta(studies: List[Study]):
    k = len(studies)
    if k == 0:
        return None

    yi = [s.log_irr for s in studies]
    vi = [s.se ** 2 for s in studies]
    wi_fixed = [1 / v for v in vi]

    theta_fixed = sum(w * y for w, y in zip(wi_fixed, yi)) / sum(wi_fixed)

    Q = sum(w * (y - theta_fixed) ** 2 for w, y in zip(wi_fixed, yi))
    df = k - 1

    I2 = max(0, (Q - df) / Q * 100) if Q > 0 else 0.0

    c = sum(wi_fixed) - sum(w ** 2 for w in wi_fixed) / sum(wi_fixed)
    tau2 = max(0, (Q - df) / c) if c > 0 else 0.0

    wi_re = [1 / (v + tau2) for v in vi]
    theta_re = sum(w * y for w, y in zip(wi_re, yi)) / sum(wi_re)
    se_re = math.sqrt(1 / sum(wi_re))

    ci_low = theta_re - 1.96 * se_re
    ci_high = theta_re + 1.96 * se_re
    pi_low = theta_re - 1.96 * math.sqrt(tau2 + se_re ** 2)
    pi_high = theta_re + 1.96 * math.sqrt(tau2 + se_re ** 2)

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
    return _reg_gamma(df / 2, x / 2)


def _reg_gamma(a, x, max_iter=200, tol=1e-10):
    if x <= 0:
        return 0.0
    ln_gamma_a = math.lgamma(a)
    total = 1.0
    term = 1.0
    for n in range(1, max_iter):
        term *= x / (a + n)
        total += term
        if abs(term) < tol:
            break
    return math.exp(-x + a * math.log(x) - ln_gamma_a) * total / a


# ─── Forest plot (ASCII) ─────────────────────────────────────────────────────

def forest_plot(studies: List[Study], result: dict, title: str, width=72):
    lines = []
    lines.append("=" * width)
    lines.append(f"  {title}")
    lines.append("=" * width)
    lines.append(f"  {'Study':<20} {'IRR':>6} {'95% CI':>20}  {'Weight%':>7}")
    lines.append("-" * width)

    tau2 = result["tau2"]
    vi = [s.se ** 2 for s in studies]
    wi = [1 / (v + tau2) for v in vi]
    total_w = sum(wi)

    for s, w in zip(studies, wi):
        pct = w / total_w * 100
        ci_str = f"({s.ci_low:.2f}-{s.ci_high:.2f})"
        lines.append(f"  {s.id:<20} {s.irr:>6.3f} {ci_str:>20}  {pct:>6.1f}%")

    lines.append("-" * width)
    lines.append(
        f"  {'Pooled (RE)':<20} {result['irr']:>6.3f} "
        f"({result['ci_low']:.3f}-{result['ci_high']:.3f})"
    )
    lines.append(
        f"  {'Prediction interval':<20}       "
        f"({result['pi_low']:.3f}-{result['pi_high']:.3f})"
    )
    lines.append("-" * width)
    lines.append(
        f"  I2 = {result['I2']:.1f}%   tau2 = {result['tau2']:.4f}   "
        f"Q({result['Q_df']}) = {result['Q']:.2f}   p = {result['p_Q']:.3f}"
    )
    lines.append("=" * width)
    return "\n".join(lines)


# ─── Main analyses ────────────────────────────────────────────────────────────

def _subset(group, outcome="invasive_incidence"):
    return [s for s in STUDIES if s.outcome == outcome and s.minority_group == group]


def run_all():
    if not STUDIES:
        print("\n" + "━" * 72)
        print("  BREAST CANCER INCIDENCE META-ANALYSIS")
        print("  Racial/Ethnic Disparities (minority vs NHW)")
        print("━" * 72)
        print("\n  [WAITING] STUDIES is empty — no data extracted yet.")
        print("  Fill in run_meta_analysis_breast.py :: STUDIES from the full")
        print("  text of the INCLUDED studies (age-adjusted invasive incidence")
        print("  rates by race), then re-run this script.\n")
        return {}

    results = {}
    analyses = {
        "Invasive BC Incidence — Black vs NHW":    _subset("Black"),
        "Invasive BC Incidence — Hispanic vs NHW": _subset("Hispanic"),
        "Invasive BC Incidence — Asian vs NHW":    _subset("Asian"),
        "Invasive BC Incidence — AIAN vs NHW":     _subset("AIAN"),
        "TNBC Incidence — Black vs NHW":           _subset("Black", "tnbc_incidence"),
    }

    print("\n" + "━" * 72)
    print("  META-ANALYSIS RESULTS")
    print("  Racial/Ethnic Disparities in Breast Cancer Incidence")
    print("━" * 72 + "\n")

    for label, subset in analyses.items():
        if len(subset) < 2:
            print(f"[SKIP] {label} — only {len(subset)} study\n")
            continue
        res = random_effects_meta(subset)
        if res is None:
            continue
        results[label] = res
        print(forest_plot(subset, res, label))
        print()

    print("\n" + "═" * 72)
    print("  SUMMARY TABLE — Pooled IRRs (Minority vs NHW)")
    print("═" * 72)
    print(f"  {'Comparison':<44} {'IRR':>6}  {'95% CI':>16}  {'I2':>5}  p")
    print("─" * 72)
    for label, res in results.items():
        ci = f"({res['ci_low']:.3f}-{res['ci_high']:.3f})"
        p_str = f"{res['p']:.4f}" if res['p'] >= 0.0001 else "<0.001"
        print(f"  {label:<44} {res['irr']:>6.3f}  {ci:>16}  {res['I2']:>4.0f}%  {p_str}")
    print("═" * 72)

    return results


if __name__ == "__main__":
    results = run_all()
    if results:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
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
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = os.path.join(OUTPUT_DIR, f"meta_results_{stamp}.json")
        with open(path, "w") as f:
            json.dump(out, f, indent=2)
        print(f"\n[✓] Results saved to {path}")
