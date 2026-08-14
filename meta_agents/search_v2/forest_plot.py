#!/usr/bin/env python3
"""Forest plots of invasive breast-cancer IRR vs non-Hispanic White women.
Reads outputs/Table_main_forest.csv. Produces:
  Fig_forest_AANHPI.png     - disaggregated Asian/NHPI subgroups (key finding).
  Fig_forest_overview.png   - aggregate groups + Hispanic-origin + AI/AN region + MENA.
Log-scaled x-axis, reference line at IRR=1.0 (NHW).
"""
import csv
import os
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
SRC = os.path.join(OUT, "Table_main_forest.csv")


def load():
    d = {}
    for r in csv.DictReader(open(SRC, encoding="utf-8")):
        try:
            row = (r["group"], float(r["irr"]), float(r["ci_lo"]), float(r["ci_hi"]))
        except ValueError:
            continue
        d.setdefault(r["dimension"], []).append(row)
    return d


def forest(items, title, fname, color="#2b6cb0"):
    # items: list of (label, irr, lo, hi) already ordered top->bottom as given;
    # we plot bottom->top so first item is at top.
    items = list(items)
    n = len(items)
    fig, ax = plt.subplots(figsize=(8.2, 0.42 * n + 1.4))
    ys = list(range(n))[::-1]
    for y, (lab, irr, lo, hi) in zip(ys, items):
        ax.plot([lo, hi], [y, y], "-", color=color, lw=1.6, zorder=2)
        ax.plot(irr, y, "s", color=color, ms=7, zorder=3)
        ax.text(hi * 1.04, y, "%.2f [%.2f, %.2f]" % (irr, lo, hi),
                va="center", ha="left", fontsize=8.2, color="#222")
    ax.axvline(1.0, color="#888", ls="--", lw=1, zorder=1)
    ax.set_yticks(ys)
    ax.set_yticklabels([lab for lab, *_ in items], fontsize=9)
    ax.set_xscale("log")
    ax.set_xlim(0.10, 3.4)
    ticks = [0.12, 0.25, 0.5, 1.0, 2.0, 3.0]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter([str(t) for t in ticks]))
    ax.xaxis.set_minor_locator(NullLocator())      # kill log minor-tick labels
    ax.tick_params(axis="x", labelsize=8.5)
    ax.set_xlabel("Incidence rate ratio vs non-Hispanic White (log scale)", fontsize=9.5)
    ax.set_title(title, fontsize=9.5, fontweight="bold", loc="left", pad=14)
    ax.text(1.0, 1.012, "← lower        higher →", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7.5, color="#777")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.margins(y=0.02)
    plt.subplots_adjust(left=0.31, right=0.80, top=0.88, bottom=0.15)
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)
    print("wrote outputs/%s (%d rows)" % (fname, n))


def main():
    d = load()
    # AANHPI: sort ascending by IRR
    aan = sorted(d.get("disaggregated-AANHPI", []), key=lambda x: x[1])
    # drop young-age duplicates for the clean subgroup figure
    aan = [x for x in aan if "young" not in x[0].lower()]
    forest(aan, "Disaggregated Asian American / NHPI subgroups (IRR vs NHW)",
           "Fig_forest_AANHPI.png", color="#b7472a")

    # overview: aggregate + hispanic-origin + AIAN region + MENA
    ov = []
    for lab, irr, lo, hi in sorted(d.get("aggregate-vs-NHW", []), key=lambda x: x[1]):
        if lab.startswith("Black (women)"):
            continue
        ov.append(("[Overall] " + lab, irr, lo, hi))
    for lab, irr, lo, hi in sorted(d.get("Hispanic-origin", []), key=lambda x: x[1]):
        ov.append(("[Hispanic] " + lab, irr, lo, hi))
    for lab, irr, lo, hi in sorted(d.get("AIAN", []), key=lambda x: x[1]):
        ov.append(("[AI/AN] " + lab.replace("AIAN ", "").replace("(provisional)", "").strip(), irr, lo, hi))
    for lab, irr, lo, hi in d.get("disaggregated-MENA", []):
        ov.append(("[MENA] " + lab, irr, lo, hi))
    forest(ov, "Aggregate groups, Hispanic origin, AI/AN region, MENA (IRR vs NHW)",
           "Fig_forest_overview.png", color="#2b6cb0")


if __name__ == "__main__":
    main()
