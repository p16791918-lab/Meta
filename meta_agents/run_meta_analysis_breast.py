"""
Meta-Analysis: Racial/Ethnic Disparities in Breast Cancer Incidence
===================================================================
Random-effects (DerSimonian-Laird) meta-analysis of age-adjusted /
age-standardized INVASIVE breast-cancer incidence rates by race/ethnicity,
extracted from population-based registry studies (abstract-level).

Primary comparison (Method A): within-study incidence-rate ratio (IRR) of a
minority group vs the non-Hispanic White (NHW) / White reference, pooled
across studies by minority group and by outcome (overall vs TNBC subtype).

Outputs: pooled IRRs + 95% CI + prediction intervals, heterogeneity (I2, tau2,
Q), ASCII + matplotlib forest plots, a results JSON and a markdown summary.

NOTE on data: NCBI/PubMed is blocked by this environment's network policy, so
rates come from the Embase abstracts already on disk (records_tabular.csv;
see extracted_studies_breast.md). US-SEER-based studies share an underlying
data source, so independence is imperfect — see the limitations note printed
at the end. This is documented, not hidden.
"""

import math
import json
import os
from dataclasses import dataclass
from typing import List, Optional

OUTDIR = "output_breast"
os.makedirs(OUTDIR, exist_ok=True)

# ─── Data model ──────────────────────────────────────────────────────────────

@dataclass
class Study:
    id: str
    year: int
    source: str
    outcome: str          # bc_incidence | tnbc_incidence | erneg_incidence
    minority_group: str   # Black | Hispanic | API | AIAN
    log_irr: float
    se: float
    minority_rate: Optional[float] = None
    ref_rate: Optional[float] = None
    notes: str = ""

    @property
    def irr(self): return math.exp(self.log_irr)

    @property
    def ci_low(self): return math.exp(self.log_irr - 1.96 * self.se)

    @property
    def ci_high(self): return math.exp(self.log_irr + 1.96 * self.se)


# ─── SE helpers ──────────────────────────────────────────────────────────────

def se_log_from_ci(rate, lo, hi):
    """SE of log(rate) from a published 95% CI on the rate."""
    return (math.log(hi) - math.log(lo)) / (2 * 1.96)


def se_from_rate_cis(r_m, m_lo, m_hi, r_n, n_lo, n_hi):
    """SE of log(IRR) combining independent 95% CIs of the two rates."""
    return math.sqrt(se_log_from_ci(r_m, m_lo, m_hi) ** 2 +
                     se_log_from_ci(r_n, n_lo, n_hi) ** 2)


def se_from_cases(cases_m, cases_n):
    """Poisson SE of log(IRR) ≈ sqrt(1/cases_m + 1/cases_n)."""
    return math.sqrt(1 / max(cases_m, 1) + 1 / max(cases_n, 1))


def logirr(r_m, r_n):
    return math.log(r_m / r_n)


# ─── Dataset (see extracted_studies_breast.md for provenance) ────────────────

STUDIES: List[Study] = [

    # ══ A. OVERALL INVASIVE BC INCIDENCE ═════════════════════════════════════
    # Wang 2022 — SEER 18, 2000-2018, age>=20 (row180)
    #   NHW 190.4, NHB 178.4, API 141.3, Hispanic 133.3, AIAN 128.8 per 100k.
    #   Group case counts estimated from SEER race distribution (row62):
    #   White 772_622, Black 125_381, API 79_069, Hispanic 142_325, AIAN 3_389.
    Study("Wang2022", 2022, "SEER 2000-2018", "bc_incidence", "Black",
          logirr(178.4, 190.4), se_from_cases(125_381, 772_622),
          178.4, 190.4, "SEER18 age>=20"),
    Study("Wang2022", 2022, "SEER 2000-2018", "bc_incidence", "API",
          logirr(141.3, 190.4), se_from_cases(79_069, 772_622),
          141.3, 190.4, "SEER18 age>=20"),
    Study("Wang2022", 2022, "SEER 2000-2018", "bc_incidence", "Hispanic",
          logirr(133.3, 190.4), se_from_cases(142_325, 772_622),
          133.3, 190.4, "SEER18 age>=20"),
    Study("Wang2022", 2022, "SEER 2000-2018", "bc_incidence", "AIAN",
          logirr(128.8, 190.4), se_from_cases(3_389, 772_622),
          128.8, 190.4, "SEER18 age>=20"),

    # England 2025 — NCRAS, 2011-2019, age>=25 (row63). ASIRs with 95% CIs.
    Study("England2025", 2025, "England NCRAS 2011-2019", "bc_incidence", "Black",
          logirr(118.2, 199.6), se_from_rate_cis(118.2, 111.6, 125.1,
                                                  199.6, 198.9, 200.3),
          118.2, 199.6, "Black African vs white British, ASIR"),

    # Brazil 2024 — 13 population registries, 2010-2015 (row88).
    #   White 101.3, Black 59.7. Group counts estimated (White ~40k, Black ~12k).
    Study("Brazil2024", 2024, "Brazil registries 2010-2015", "bc_incidence", "Black",
          logirr(59.7, 101.3), se_from_cases(12_000, 40_000),
          59.7, 101.3, "median incidence, distinct population"),

    # ══ B. TRIPLE-NEGATIVE BC (TNBC) INCIDENCE ═══════════════════════════════
    # Xie 2023 — SEER 18, 2010-2019, age>=20 (row150). TNBC n=62,623.
    #   Black 33.8, White 17.5, AIAN 14.7, Hispanic 14.7, Asian 12.4.
    #   Group counts estimated from TNBC race mix.
    Study("Xie2023", 2023, "SEER 2010-2019", "tnbc_incidence", "Black",
          logirr(33.8, 17.5), se_from_cases(12_525, 38_826),
          33.8, 17.5, "TNBC"),
    Study("Xie2023", 2023, "SEER 2010-2019", "tnbc_incidence", "AIAN",
          logirr(14.7, 17.5), se_from_cases(250, 38_826),
          14.7, 17.5, "TNBC"),
    Study("Xie2023", 2023, "SEER 2010-2019", "tnbc_incidence", "Hispanic",
          logirr(14.7, 17.5), se_from_cases(6_889, 38_826),
          14.7, 17.5, "TNBC"),
    Study("Xie2023", 2023, "SEER 2010-2019", "tnbc_incidence", "API",
          logirr(12.4, 17.5), se_from_cases(3_757, 38_826),
          12.4, 17.5, "TNBC (Asian)"),

    # Kong 2023 — USCS / NPCR-SEER, 2015-2019 (row137). Exact case counts.
    #   Black 25.2 (n=28,710), White 12.9 (n=86,195), AIAN 11.2 (n=768),
    #   Hispanic 11.1 (n=12,937), API 9.0 (n=4,969).
    Study("Kong2023", 2023, "USCS 2015-2019", "tnbc_incidence", "Black",
          logirr(25.2, 12.9), se_from_cases(28_710, 86_195),
          25.2, 12.9, "TNBC, national USCS"),
    Study("Kong2023", 2023, "USCS 2015-2019", "tnbc_incidence", "AIAN",
          logirr(11.2, 12.9), se_from_cases(768, 86_195),
          11.2, 12.9, "TNBC"),
    Study("Kong2023", 2023, "USCS 2015-2019", "tnbc_incidence", "Hispanic",
          logirr(11.1, 12.9), se_from_cases(12_937, 86_195),
          11.1, 12.9, "TNBC"),
    Study("Kong2023", 2023, "USCS 2015-2019", "tnbc_incidence", "API",
          logirr(9.0, 12.9), se_from_cases(4_969, 86_195),
          9.0, 12.9, "TNBC"),

    # Yao 2013 — SEER 18 national, 2010 (row367). Black 20.4, White 11.3.
    #   Single year; counts estimated (Black ~4k, White ~8k).
    Study("Yao2013", 2013, "SEER 2010", "tnbc_incidence", "Black",
          logirr(20.4, 11.3), se_from_cases(4_000, 8_000),
          20.4, 11.3, "TNBC, national SEER18 single year"),

    # ══ C. ER-NEGATIVE BC INCIDENCE (single-study context) ═══════════════════
    # Jenkins 2025 — SEER, 2013-2015 (row67). NHB 43.1, NHW 24.0. ER- counts.
    Study("Jenkins2025", 2025, "SEER 2013-2015", "erneg_incidence", "Black",
          logirr(43.1, 24.0), se_from_cases(5_117, 15_040),
          43.1, 24.0, "ER-negative, age 20-74"),
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
        "k": k, "theta": theta_re, "se": se_re, "irr": math.exp(theta_re),
        "ci_low": math.exp(ci_low), "ci_high": math.exp(ci_high),
        "pi_low": math.exp(pi_low), "pi_high": math.exp(pi_high),
        "I2": I2, "tau2": tau2, "Q": Q, "Q_df": df,
        "p_Q": 1 - _chi2_cdf(Q, df) if df > 0 else 1.0,
        "z": z, "p": p,
    }


def _norm_cdf(x):
    return 0.5 * (1 + math.erf(x / math.sqrt(2)))


def _chi2_cdf(x, df):
    # Series expansion overflows for very large x; cdf -> 1 there.
    if x > df + 200:
        return 1.0
    return _reg_gamma(df / 2, x / 2)


def _reg_gamma(a, x, max_iter=500, tol=1e-12):
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


# ─── ASCII forest plot ───────────────────────────────────────────────────────

def forest_plot(studies, result, title, width=76):
    lines = ["=" * width, f"  {title}", "=" * width,
             f"  {'Study':<22} {'IRR':>6} {'95% CI':>18}  {'Weight%':>7}",
             "-" * width]
    tau2 = result["tau2"]
    wi = [1 / (s.se ** 2 + tau2) for s in studies]
    total_w = sum(wi)
    for s, w in zip(studies, wi):
        ci = f"({s.ci_low:.2f}-{s.ci_high:.2f})"
        lines.append(f"  {s.id + ' ' + str(s.year):<22} {s.irr:>6.3f} {ci:>18}  {w/total_w*100:>6.1f}%")
    lines.append("-" * width)
    lines.append(f"  {'Pooled (RE)':<22} {result['irr']:>6.3f} "
                 f"({result['ci_low']:.3f}-{result['ci_high']:.3f})")
    lines.append(f"  {'Prediction interval':<22}        "
                 f"({result['pi_low']:.3f}-{result['pi_high']:.3f})")
    lines.append("-" * width)
    lines.append(f"  I2 = {result['I2']:.1f}%   tau2 = {result['tau2']:.4f}   "
                 f"Q({result['Q_df']}) = {result['Q']:.2f}   p = {result['p_Q']:.3f}")
    lines.append("=" * width)
    return "\n".join(lines)


# ─── Analyses ────────────────────────────────────────────────────────────────

ANALYSES = {
    "Overall invasive BC incidence — Black vs White":
        ("bc_incidence", "Black"),
    "TNBC incidence — Black vs White":
        ("tnbc_incidence", "Black"),
    "TNBC incidence — Hispanic vs White":
        ("tnbc_incidence", "Hispanic"),
    "TNBC incidence — API/Asian vs White":
        ("tnbc_incidence", "API"),
    "TNBC incidence — AIAN vs White":
        ("tnbc_incidence", "AIAN"),
}

SINGLE_STUDY = {
    "Overall invasive BC incidence — Hispanic vs NHW": ("bc_incidence", "Hispanic"),
    "Overall invasive BC incidence — API vs NHW":      ("bc_incidence", "API"),
    "Overall invasive BC incidence — AIAN vs NHW":     ("bc_incidence", "AIAN"),
    "ER-negative BC incidence — Black vs NHW":          ("erneg_incidence", "Black"),
}


def subset(outcome, group):
    return [s for s in STUDIES if s.outcome == outcome and s.minority_group == group]


def run_all():
    results = {}
    print("\n" + "=" * 76)
    print("  META-ANALYSIS — Racial/Ethnic Disparities in Breast Cancer Incidence")
    print("=" * 76 + "\n")

    for label, (outcome, group) in ANALYSES.items():
        sub = subset(outcome, group)
        if len(sub) < 2:
            print(f"[SKIP pooling] {label} — only {len(sub)} study\n")
            continue
        res = random_effects_meta(sub)
        results[label] = res
        print(forest_plot(sub, res, label))
        print()

    # Single-study estimates (reported, not pooled)
    print("=" * 76)
    print("  SINGLE-STUDY ESTIMATES (k=1, reported not pooled)")
    print("=" * 76)
    print(f"  {'Comparison':<48} {'IRR':>6}  {'95% CI':>16}")
    print("-" * 76)
    for label, (outcome, group) in SINGLE_STUDY.items():
        sub = subset(outcome, group)
        for s in sub:
            ci = f"({s.ci_low:.3f}-{s.ci_high:.3f})"
            print(f"  {label:<48} {s.irr:>6.3f}  {ci:>16}")
    print("=" * 76 + "\n")

    # Summary table
    print("=" * 76)
    print("  SUMMARY — Pooled IRRs (minority vs White), random effects")
    print("=" * 76)
    print(f"  {'Comparison':<44} {'k':>2} {'IRR':>6}  {'95% CI':>16}  {'I2':>5}  p")
    print("-" * 76)
    for label, res in results.items():
        ci = f"({res['ci_low']:.3f}-{res['ci_high']:.3f})"
        p_str = f"{res['p']:.4f}" if res['p'] >= 0.0001 else "<0.0001"
        print(f"  {label:<44} {res['k']:>2} {res['irr']:>6.3f}  {ci:>16}  "
              f"{res['I2']:>4.0f}%  {p_str}")
    print("=" * 76)

    print("\n  LIMITATION: US SEER/USCS studies share an underlying registry and")
    print("  overlapping calendar years, so the pooled CIs understate uncertainty")
    print("  (independence violated). Very high I2 reflects tiny within-study")
    print("  variance from large registries + real between-study differences.")
    print("  Interpret pooled points as summaries of direction/magnitude.\n")

    return results


def make_forest_png(results):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:
        print(f"[matplotlib unavailable: {e}]")
        return

    rows = []  # (label, study rows, pooled)
    for label, (outcome, group) in ANALYSES.items():
        sub = subset(outcome, group)
        if len(sub) < 2:
            continue
        rows.append((label, sub, results[label]))

    total_lines = sum(len(sub) + 2 for _, sub, _ in rows) + len(rows)
    fig, ax = plt.subplots(figsize=(9, 0.42 * total_lines + 1))
    y = total_lines
    yticks, ylabels = [], []

    for label, sub, res in rows:
        y -= 1
        ax.text(0.008, y, label, fontweight="bold", fontsize=9,
                transform=ax.get_yaxis_transform(), va="center")
        for s in sub:
            y -= 1
            ax.plot([s.ci_low, s.ci_high], [y, y], color="#555", lw=1.4, zorder=2)
            ax.plot(s.irr, y, "s", color="#2b6cb0", ms=6, zorder=3)
            yticks.append(y); ylabels.append(f"   {s.id} {s.year}")
        y -= 1
        ax.plot([res["ci_low"], res["ci_high"]], [y, y], color="#c53030", lw=2.4, zorder=2)
        ax.plot(res["irr"], y, "D", color="#c53030", ms=8, zorder=3)
        yticks.append(y)
        ylabels.append(f"   Pooled (I2={res['I2']:.0f}%)")
        y -= 1

    ax.axvline(1.0, color="#999", ls="--", lw=1)
    from matplotlib.ticker import NullLocator, FixedLocator
    ax.set_xscale("log")
    ax.set_xlim(0.35, 3.2)
    ax.xaxis.set_minor_locator(NullLocator())
    ax.xaxis.set_major_locator(FixedLocator([0.4, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]))
    ax.set_xticklabels(["0.4", "0.5", "0.7", "1.0", "1.5", "2.0", "3.0"])
    ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=8)
    ax.set_ylim(-0.5, total_lines + 0.5)
    ax.set_xlabel("Incidence rate ratio (minority vs White), log scale")
    ax.set_title("Racial/Ethnic Disparities in Breast Cancer Incidence\n"
                 "Random-effects pooled IRRs", fontsize=11)
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)
    fig.tight_layout()
    path = os.path.join(OUTDIR, "forest_breast.png")
    fig.savefig(path, dpi=150, bbox_inches="tight")
    print(f"[OK] Forest plot -> {path}")


if __name__ == "__main__":
    results = run_all()

    out = {}
    for k, v in results.items():
        out[k] = {kk: (round(v[kk], 4) if isinstance(v[kk], float) else v[kk])
                  for kk in ("k", "irr", "ci_low", "ci_high", "pi_low", "pi_high",
                             "I2", "tau2", "Q", "Q_df", "p_Q", "p")}
    with open(os.path.join(OUTDIR, "meta_results_breast.json"), "w") as f:
        json.dump(out, f, indent=2)
    print(f"[OK] Results -> {OUTDIR}/meta_results_breast.json")

    make_forest_png(results)
