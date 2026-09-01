#!/usr/bin/env python3
"""Figure 3 — incidence heterogeneity across groups x analytic dimensions.

Reads the finalize_representatives output (TableSA_main_representatives.csv) and
draws a heatmap of the representative IRR (vs non-Hispanic White women) for a
curated set of groups x dimensions. The colour scale diverges around 1.0 (the
NHW reference), so a group at, below, or above the NHW rate reads at a glance,
and the same group's row shows how its relative incidence shifts by dimension
(overall, age, receptor-defined subtype). Real data only — no illustrative fill.
"""
import csv
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
REPS = os.path.join(HERE, "TableSA_main_representatives.csv")

# rows: (display label, acceptable group strings, dimension supplying "Overall")
ROWS = [
    ("AI/AN",           {"AIAN"},                                     "aggregate-vs-NHW"),
    ("Hispanic",        {"Hispanic"},                                 "aggregate-vs-NHW"),
    ("AANHPI",          {"Asian/PI (aggregate)"}, "aggregate-vs-NHW"),
    ("NHB",             {"Black"},                                    "aggregate-vs-NHW"),
    ("Chinese",         {"Chinese"},                                  "disaggregated-AANHPI"),
    ("Filipina",        {"Filipina", "Filipino"},                     "disaggregated-AANHPI"),
    ("Japanese",        {"Japanese"},                                 "disaggregated-AANHPI"),
    ("Native Hawaiian", {"Native Hawaiian"},                          "disaggregated-AANHPI"),
]
# columns: (display label, dimension); the first is the row-specific "Overall"
COLS = [
    ("Overall",     None),
    ("Age <50",     "age-lt50"),
    ("Age ≥50", "age-ge50"),
    ("HR+/HER2−", "subtype-HRpos-HER2neg"),
    ("HR+/HER2+",   "subtype-HRpos-HER2pos"),
    ("HR−/HER2+", "subtype-HRneg-HER2pos"),
    ("TNBC",        "subtype-TNBC"),
]


def load():
    lut = {}
    for r in csv.DictReader(open(REPS, encoding="utf-8")):
        if not r["main_analysis"].startswith("yes") or not r["irr"]:
            continue
        try:
            lut[(r["minority_group"], r["outcome_dim"])] = float(r["irr"])
        except ValueError:
            pass
    return lut


def lookup(lut, groups, dim):
    for g in groups:
        if (g, dim) in lut:
            return lut[(g, dim)]
    return None


def main():
    lut = load()
    M = np.full((len(ROWS), len(COLS)), np.nan)
    for i, (_, groups, overall_dim) in enumerate(ROWS):
        for j, (_, dim) in enumerate(COLS):
            d = overall_dim if dim is None else dim
            v = lookup(lut, groups, d)
            if v is not None:
                M[i, j] = v

    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    norm = TwoSlopeNorm(vmin=0.15, vcenter=1.0, vmax=2.0)
    cmap = plt.get_cmap("RdBu_r").copy()
    cmap.set_bad("#f5f5f5")   # blank cells (no estimate) = light grey
    im = ax.imshow(M, cmap=cmap, norm=norm, aspect="auto")

    ax.set_xticks(range(len(COLS)))
    ax.set_xticklabels([c for c, _ in COLS], fontsize=9)
    ax.set_yticks(range(len(ROWS)))
    ax.set_yticklabels([r for r, *_ in ROWS], fontsize=9)
    ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False, length=0)
    plt.setp(ax.get_xticklabels(), rotation=30, ha="left", rotation_mode="anchor")

    # gridlines between cells
    ax.set_xticks(np.arange(-0.5, len(COLS), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(ROWS), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=2)
    ax.tick_params(which="minor", length=0)

    for i in range(len(ROWS)):
        for j in range(len(COLS)):
            if np.isnan(M[i, j]):
                continue
            v = M[i, j]
            # white text on the darkest cells, else near-black
            dark = v <= 0.45 or v >= 1.6
            ax.text(j, i, "%.2f" % v, ha="center", va="center", fontsize=8.6,
                    color="white" if dark else "#1a1a1a")

    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03,
                      ticks=[0.25, 0.5, 1.0, 1.5, 2.0])
    cb.ax.set_yticklabels(["0.25", "0.5", "1.0", "1.5", "2.0"])
    cb.set_label("Representative IRR vs NHW (1.0 = NHW rate)", fontsize=8.5)
    cb.ax.tick_params(labelsize=8)

    ax.set_title("Incidence rate ratio by group and analytic dimension",
                 fontsize=11, fontweight="bold", pad=28, loc="left")
    fig.text(0.01, 0.01, "Blank (grey) cells: no representative estimate for that "
             "group × dimension. Subgroup rows show Asian American groups within "
             "the AANHPI aggregate.", fontsize=7.2, color="#666")
    plt.subplots_adjust(left=0.16, right=0.99, top=0.78, bottom=0.08)
    fig.savefig(os.path.join(OUT, "Fig_heatmap.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    filled = int(np.sum(~np.isnan(M)))
    print("wrote outputs/Fig_heatmap.png (%d of %d cells filled)" % (filled, M.size))


if __name__ == "__main__":
    main()
