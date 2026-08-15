#!/usr/bin/env python3
"""Per-race pooled forest plots: for each analytic cell with >=2 contributing
studies, show every study estimate (IRR vs NHW) plus the random-effects pooled
diamond (Paule-Mandel/REML + Hartung-Knapp CI) and I^2. Grouped into subgrouped
forest figures by dimension, mirroring the example paper's per-outcome forests.
Writes outputs/Fig_pool_*.png.
"""
import csv
import math
import os
import re
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator

import meta_analysis_v2 as M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
Z = M.Z


def label(ay):
    parts = ay.split("_")
    if re.fullmatch(r"(19|20)\d\d", parts[0]):          # year-first e.g. 2024_USCS
        return (parts[1] + " " + parts[0]) if len(parts) > 1 else parts[0]
    if ay == "SEER-EXPL":
        return "SEER-Explorer (ref)"
    return re.sub(r"(\d{4})", r" \1", parts[0]).strip()


def load_cells():
    ay = {}
    for r in csv.DictReader(open(os.path.join(HERE, "breast_extraction.csv"), encoding="utf-8")):
        ay.setdefault(r["record_id"], r["author_year"])
    rows = M.load()
    cells = defaultdict(list)
    for r in rows:
        r["lab"] = label(ay.get(r["rid"], r["rid"]))
        r["lo"] = math.exp(r["y"] - Z * r["se"])
        r["hi"] = math.exp(r["y"] + Z * r["se"])
        cells[(r["dim"], r["grp"])].append(r)
    return cells


def pooled(cr):
    res = M.analyse(cr, "x")
    pm = res["PM/REML"]
    return pm["irr"], pm["lo_hk"], pm["hi_hk"], pm["I2"]


def subgroup_forest(cells, groups, title, fname, color="#2b6cb0"):
    """groups: list of (dim, grp, display). Build one subgrouped forest."""
    # layout rows top->bottom
    blocks = []
    for dim, grp, disp in groups:
        cr = sorted(cells[(dim, grp)], key=lambda r: r["irr"])
        pirr, plo, phi, i2 = pooled(cr)
        blocks.append((disp, cr, pirr, plo, phi, i2))
    nrows = sum(1 + len(cr) + 1 for _, cr, *_ in blocks) + len(blocks)  # header+studies+diamond+gap
    fig, ax = plt.subplots(figsize=(9.2, 0.34 * nrows + 1.2))
    y = nrows
    yticks, ylabels = [], []
    for disp, cr, pirr, plo, phi, i2 in blocks:
        y -= 1
        ax.text(0.088, y, disp, transform=ax.get_yaxis_transform(), fontsize=9,
                fontweight="bold", va="center", ha="left")
        for r in cr:
            y -= 1
            ax.plot([r["lo"], r["hi"]], [y, y], "-", color=color, lw=1.3, zorder=2)
            ax.plot(r["irr"], y, "s", color=color, ms=5.5, zorder=3)
            yticks.append(y); ylabels.append("   " + r["lab"])
            ax.text(3.15, y, "%.2f [%.2f, %.2f]" % (r["irr"], r["lo"], r["hi"]),
                    fontsize=7.6, va="center", ha="right", color="#333")
        # diamond
        y -= 1
        cy = 0.32
        ax.add_patch(Polygon([[plo, y], [pirr, y + cy], [phi, y], [pirr, y - cy]],
                             closed=True, facecolor=color, edgecolor="black", lw=0.7, zorder=4))
        yticks.append(y); ylabels.append("   Pooled (RE), I²=%.0f%%" % i2)
        ax.text(3.15, y, "%.2f [%.2f, %.2f]" % (pirr, plo, phi),
                fontsize=7.8, va="center", ha="right", fontweight="bold", color="#111")
        y -= 1  # gap
    ax.axvline(1.0, color="#888", ls="--", lw=1, zorder=1)
    ax.set_yticks(yticks); ax.set_yticklabels(ylabels, fontsize=7.8)
    ax.set_ylim(-0.5, nrows + 0.2)
    ax.set_xscale("log"); ax.set_xlim(0.10, 3.4)
    ticks = [0.12, 0.25, 0.5, 1.0, 2.0, 3.0]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter([str(t) for t in ticks]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.tick_params(axis="x", labelsize=8)
    ax.set_xlabel("Incidence rate ratio vs non-Hispanic White (log scale)", fontsize=9)
    ax.set_title(title, fontsize=10.5, fontweight="bold", loc="left")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    plt.subplots_adjust(left=0.24, right=0.83, top=0.95, bottom=0.12)
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)
    print("wrote outputs/%s (%d rows)" % (fname, nrows))


def main():
    cells = load_cells()
    subgroup_forest(cells,
        [("aggregate-vs-NHW", "Black", "Black / African American"),
         ("aggregate-vs-NHW", "Hispanic", "Hispanic / Latina"),
         ("aggregate-vs-NHW", "Asian/PI (aggregate)", "Asian / Pacific Islander (aggregate)"),
         ("aggregate-vs-NHW", "AIAN", "American Indian / Alaska Native")],
        "Pooled incidence rate ratios by aggregate racial/ethnic group",
        "Fig_pool_aggregate.png", color="#2b6cb0")
    subgroup_forest(cells,
        [("subtype-TNBC", "Black", "TNBC — Black"),
         ("subtype-TNBC", "Hispanic", "TNBC — Hispanic"),
         ("subtype-TNBC", "Asian/PI (aggregate)", "TNBC — Asian / Pacific Islander")],
        "Pooled triple-negative breast cancer IRRs by group",
        "Fig_pool_tnbc.png", color="#b7472a")
    subgroup_forest(cells,
        [("disaggregated-AANHPI", "Asian Indian/Pakistani", "Asian Indian / Pakistani"),
         ("disaggregated-AANHPI", "Korean", "Korean"),
         ("disaggregated-AANHPI", "Native Hawaiian", "Native Hawaiian"),
         ("AIAN", "Alaska Native", "Alaska Native")],
        "Pooled IRRs for cells with >=2 studies (disaggregated subgroups)",
        "Fig_pool_disaggregated.png", color="#2f7d4f")


if __name__ == "__main__":
    main()
