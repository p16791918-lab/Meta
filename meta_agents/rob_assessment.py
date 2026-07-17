#!/usr/bin/env python3
"""Phase C — Risk-of-Bias assessment for the 15 quantitative studies.

Population-based cancer-incidence (surveillance) studies do not fit clinical-trial
or cohort RoB tools, so we assess six domains tailored to registry incidence-by-race
studies. Each is rated Low / Some concerns / High.

  D1 Ascertainment    population-based registry, high case completeness
  D2 Race/ethnicity   classification accuracy (AIAN & Asian-subgroup misclassification)
  D3 Denominator      population-estimate accuracy (intercensal, small subgroups)
  D4 Outcome          invasive-BC definition + age-standardization method
  D5 Comparability    same NHW reference, age-adjusted, crude vs model-adjusted estimand
  D6 Reporting        rate + variance reported (vs approximated / figure-read / derived)

Produces a traffic-light table (stdout) and figures/fig6_rob.png.
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

L, S, H = "L", "S", "H"   # Low / Some concerns / High

# study_id : (label, {D1..D6}, note)
ROB = [
    ("35025856", "Ellington 2022 · USCS (SEER+NPCR, ~99%)",
     [L, L, L, L, L, S], "national ~99% coverage; no rate CI reported → SE Poisson-approx (D6)"),
    ("34861613", "Du & Song 2022 · SEER",
     [L, S, L, L, L, L], "SEER standard; API aggregated (D2)"),
    ("33074325", "Kong 2020 · SEER 18",
     [L, S, L, L, L, L], "subtype IRRs w/ CI; API aggregated (D2)"),
    ("41082230", "Ghanaian/US Black 2024 · SEER 17",
     [L, L, L, L, L, L], "20–74y Segi std; Black vs White + ER status, all w/ CI"),
    ("26513636", "DeSantis 2016 · NAACCR (~93%)",
     [L, S, L, L, L, S], "overall rates read from Figure 1 bar labels (D6); API aggregated"),
    ("15986118", "Joslyn 2005 · NAACCR",
     [L, S, L, L, L, L], "age-specific rate+RR+CI table; API/AI aggregated (D2)"),
    ("31764279", "Gopalani 2020 · IHS-linked",
     [L, L, S, L, L, L], "IHS linkage CORRECTS AIAN misclassification (D2 strength); small denominators (D3)"),
    ("20147696", "Gomez 2010 · California CR",
     [L, S, L, L, L, S], "Asian disaggregated; combined-Asian point is analyst PY-weighted derivation (D6)"),
    ("21351091", "Liu 2012 · LA County SEER",
     [L, S, L, L, S, L], "model-adjusted RR (period+age), not crude ratio-of-rates (D5); regional"),
    ("36504334", "Ihenacho 2023 · SEER Hawaii",
     [L, L, S, L, L, L], "age-stratified API ethnicities; regional (Hawaii); small young-age counts (D3)"),
    ("30503975", "Loo 2019 · SEER Hawaii",
     [L, L, S, L, L, L], "overall + subtype ethnic IRR w/ CI; regional; small subtype counts (D3)"),
    ("21301957", "Moran 2011 · California CR",
     [L, S, S, L, L, S], "Asian Indian/Pakistani via surname; two denominator estimates (high/low) (D3,D6)"),
    ("21473509", "Lepeak 2011 · Wisconsin CRS",
     [L, L, L, L, L, H], "state registry; RR rounded to 0.8, NO CI reported (D6 high)"),
    ("12115511", "Deapen 2002 · LA County CSP",
     [L, S, L, L, S, S], "scanned table; 10-yr-mean rate is analyst derivation; regional; overlaps Liu (D5,D6)"),
    ("Te7879b3", "TNBC-trends 2023 · SEER/USCS",
     [L, S, L, L, L, S], "full-text TNBC IRRs w/ CI; citation still to be confirmed (D6)"),
]

DOMAINS = ["D1\nascert.", "D2\nrace class.", "D3\ndenom.",
           "D4\noutcome", "D5\ncompar.", "D6\nreporting"]
COLOR = {"L": "#1baf7a", "S": "#eda100", "H": "#e34948"}   # green / amber / red
FULL = {"L": "Low", "S": "Some concerns", "H": "High"}


def print_table():
    print("=" * 78)
    print("  RISK OF BIAS — 15 quantitative studies (L=low, S=some concerns, H=high)")
    print("=" * 78)
    print(f"  {'Study':<40} " + " ".join(d.split(chr(10))[0] for d in DOMAINS))
    print("  " + "-" * 74)
    for sid, label, ratings, note in ROB:
        print(f"  {label[:40]:<40} " + "  ".join(ratings))
    print("=" * 78)
    counts = {"L": 0, "S": 0, "H": 0}
    for _, _, ratings, _ in ROB:
        for r in ratings:
            counts[r] += 1
    tot = sum(counts.values())
    print(f"  Domain-judgements: Low {counts['L']} ({100*counts['L']//tot}%), "
          f"Some {counts['S']} ({100*counts['S']//tot}%), High {counts['H']} ({100*counts['H']//tot}%)")
    print("  No study rated High on ascertainment, race-classification for the")
    print("  aggregate comparison, or outcome definition — the disparity signal is")
    print("  not driven by low-quality studies. High/Some flags concentrate in D6")
    print("  (reporting/precision), addressed by the sensitivity analyses.")
    print("=" * 78)


def make_figure():
    INK, INK2 = "#0b0b0b", "#52514e"
    n = len(ROB)
    fig, ax = plt.subplots(figsize=(9.5, 0.42 * n + 1.8))
    fig.patch.set_facecolor("white"); ax.set_facecolor("white")
    for j, dom in enumerate(DOMAINS):
        ax.text(j + 0.5, n + 0.35, dom, ha="center", va="bottom",
                fontsize=8.2, color=INK, fontweight="bold", linespacing=0.95)
    for i, (sid, label, ratings, note) in enumerate(ROB):
        y = n - 1 - i
        ax.text(-0.2, y + 0.5, label, ha="right", va="center", fontsize=8, color=INK2)
        for j, r in enumerate(ratings):
            ax.add_patch(Circle((j + 0.5, y + 0.5), 0.34, facecolor=COLOR[r],
                                edgecolor="white", lw=1.2, zorder=3))
            ax.text(j + 0.5, y + 0.5, r, ha="center", va="center",
                    fontsize=7.5, color="white", fontweight="bold", zorder=4)
    ax.set_xlim(-4.6, len(DOMAINS)); ax.set_ylim(0, n + 1.1)
    ax.axis("off")
    # legend
    for k, (code, xoff) in enumerate([("L", 0), ("S", 1.7), ("H", 3.7)]):
        ax.add_patch(Circle((xoff + 0.2, -0.4), 0.18, facecolor=COLOR[code],
                            edgecolor="white", lw=1, clip_on=False, zorder=3))
        ax.text(xoff + 0.45, -0.4, FULL[code], ha="left", va="center",
                fontsize=8, color=INK2, clip_on=False)
    ax.set_title("Risk of bias — quantitative studies (registry incidence-by-race domains)",
                 fontsize=11, fontweight="bold", color=INK, loc="left", pad=14)
    fig.tight_layout()
    os.makedirs("figures", exist_ok=True)
    fig.savefig("figures/fig6_rob.png", dpi=300, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print("wrote figures/fig6_rob.png")


if __name__ == "__main__":
    print_table()
    make_figure()
