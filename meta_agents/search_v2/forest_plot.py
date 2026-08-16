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


def forest(items, title, fname, color="#2b6cb0", divider_after=None):
    # items: list of (label, irr, lo, hi) already ordered top->bottom as given;
    # we plot bottom->top so first item is at top.
    items = list(items)
    n = len(items)
    fig, ax = plt.subplots(figsize=(9.2, 0.42 * n + 1.4))
    ys = list(range(n))[::-1]
    for i, (y, (lab, irr, lo, hi)) in enumerate(zip(ys, items)):
        agg = divider_after is not None and i >= divider_after
        ax.plot([lo, hi], [y, y], "-", color=color, lw=1.6, zorder=2)
        ax.plot(irr, y, "D" if agg else "s", color=color, ms=8 if agg else 7, zorder=3)
        ax.text(hi * 1.04, y, "%.2f [%.2f, %.2f]" % (irr, lo, hi),
                va="center", ha="left", fontsize=8.2, color="#222",
                fontweight="bold" if agg else "normal")
    if divider_after is not None:
        ax.axhline(n - divider_after - 0.5, color="#aaa", lw=0.9, ls="-", zorder=1)
    ax.axvline(1.0, color="#888", ls="--", lw=1, zorder=1)
    ax.set_yticks(ys)
    ax.set_yticklabels([lab for lab, *_ in items], fontsize=9)
    if divider_after is not None:
        for lbl in ax.get_yticklabels()[divider_after:]:
            lbl.set_fontweight("bold")
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
    plt.subplots_adjust(left=0.40, right=0.82, top=0.88, bottom=0.15)
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)
    print("wrote outputs/%s (%d rows)" % (fname, n))


def sectioned_forest(sections, title, fname, color="#2b6cb0"):
    """sections: list of (header, rows) where rows are (label, irr, lo, hi, is_agg).
    Each section gets a bold header row and a divider; aggregate rows are bold
    diamonds."""
    flat = []  # (label, irr, lo, hi, kind)  kind in {header, study, agg}
    for hdr, rows in sections:
        flat.append((hdr, None, None, None, "header"))
        for lab, irr, lo, hi, is_agg in rows:
            flat.append((lab, irr, lo, hi, "agg" if is_agg else "study"))
    n = len(flat)
    fig, ax = plt.subplots(figsize=(9.6, 0.42 * n + 1.4))
    ys = list(range(n))[::-1]
    for y, (lab, irr, lo, hi, kind) in zip(ys, flat):
        if kind == "header":
            continue
        agg = kind == "agg"
        ax.plot([lo, hi], [y, y], "-", color=color, lw=1.6, zorder=2)
        ax.plot(irr, y, "D" if agg else "s", color=color, ms=8 if agg else 7, zorder=3)
        ax.text(hi * 1.04, y, "%.2f [%.2f, %.2f]" % (irr, lo, hi), va="center", ha="left",
                fontsize=8.2, color="#222", fontweight="bold" if agg else "normal")
    # dividers above each header after the first
    for idx, (_, _, _, _, kind) in enumerate(flat):
        if kind == "header" and idx > 0:
            ax.axhline(n - idx - 0.5, color="#aaa", lw=0.9, zorder=1)
    ax.axvline(1.0, color="#888", ls="--", lw=1, zorder=1)
    ax.set_yticks(ys)
    ax.set_yticklabels([lab for lab, *_ in flat], fontsize=9)
    for lbl, (_, _, _, _, kind) in zip(ax.get_yticklabels(), flat):
        if kind in ("header", "agg"):
            lbl.set_fontweight("bold")
    ax.set_ylim(-0.6, n - 0.3)   # headroom so the top section header isn't clipped
    ax.set_xscale("log"); ax.set_xlim(0.10, 3.4)
    ticks = [0.12, 0.25, 0.5, 1.0, 2.0, 3.0]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter([str(t) for t in ticks]))
    ax.xaxis.set_minor_locator(NullLocator())
    ax.tick_params(axis="x", labelsize=8.5)
    ax.set_xlabel("Incidence rate ratio vs non-Hispanic White (log scale)", fontsize=9.5)
    ax.set_title(title, fontsize=9.5, fontweight="bold", loc="left", pad=22)
    ax.text(1.0, 1.02, "← lower        higher →", transform=ax.transAxes,
            ha="right", va="bottom", fontsize=7.5, color="#777")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    plt.subplots_adjust(left=0.42, right=0.82, top=0.86, bottom=0.15)
    fig.savefig(os.path.join(OUT, fname), dpi=200)
    plt.close(fig)
    print("wrote outputs/%s (%d rows)" % (fname, n))


def main():
    d = load()
    from labels import disp_group
    # AANHPI: split into Asian American vs NHPI, each = subgroups (sorted by IRR)
    # then that block's aggregate; shows how the single aggregates conceal the range.
    NHPI_KEYS = ("hawaiian", "guamanian", "chamorro", "samoan", "pacific islander")
    def is_nhpi(l): return any(k in l.lower() for k in NHPI_KEYS)
    aan_all = [x for x in d.get("disaggregated-AANHPI", []) if "young" not in x[0].lower()]
    def block(pred):
        subs = sorted([x for x in aan_all if pred(x[0]) and "aggregate" not in x[0].lower()], key=lambda x: x[1])
        aggs = sorted([x for x in aan_all if pred(x[0]) and "aggregate" in x[0].lower()], key=lambda x: x[1])
        rows = [(disp_group(l), i, lo, hi, False) for l, i, lo, hi in subs]
        rows += [("▶ " + disp_group(l), i, lo, hi, True) for l, i, lo, hi in aggs]
        return rows
    sections = [
        ("Asian American subgroups", block(lambda l: not is_nhpi(l))),
        ("Native Hawaiian and Pacific Islander (NHPI) subgroups", block(is_nhpi)),
    ]
    sectioned_forest(sections, "Disaggregated Asian/NHPI subgroups vs the aggregate (IRR vs NHW)",
                     "Fig_forest_AANHPI.png", color="#b7472a")

    # overview: aggregate + hispanic-origin + AIAN region + MENA
    # use the short abbreviation for the aggregate rows so the compact overview
    # doesn't clip long umbrella names (full names are in Table 1 / the caption).
    import re as _re
    def _short(lab):
        d2 = disp_group(lab)
        m = _re.search(r"\(([^)]+)\)\s*$", d2)   # ...(AANHPI) -> AANHPI
        return m.group(1) if m else d2
    ov = []
    for lab, irr, lo, hi in sorted(d.get("aggregate-vs-NHW", []), key=lambda x: x[1]):
        if lab.startswith("Black (women)"):
            continue
        ov.append(("[Overall] " + _short(lab), irr, lo, hi))
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
