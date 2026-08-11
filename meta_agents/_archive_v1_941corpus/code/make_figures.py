#!/usr/bin/env python3
"""Publication figures for the breast-cancer incidence disparities review.

Generates 300-dpi PNGs into figures/:
  fig1_main_forest.png       aggregate 4-race forest (the "convergence" view)
  fig2_subgroups_forest.png  disaggregated Asian/ethnic subgroups
  fig3_subtypes_forest.png   molecular subtypes by race + disaggregated API
  fig4_age_crossover.png     Black-White (NAACCR) + within-API (Hawaii) age crossover

Design (per dataviz skill): direction is encoded with the validated diverging
pair — blue = IRR<1 (lower than NHW), red = IRR>1 (higher); neutral gray for the
null. Square area ∝ inverse-variance weight. Pooled = diamond. Recessive grid.
"""
import math
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FixedFormatter, NullFormatter, NullLocator

from run_meta_analysis_breast import STUDIES, _subset, random_effects_meta

# ── palette (dataviz validated) ──────────────────────────────────────────────
BLUE = "#2a78d6"   # IRR < 1  (lower incidence than NHW)
RED  = "#e34948"   # IRR > 1  (higher incidence than NHW)
GRAY = "#b8b7b2"   # null / grid
INK  = "#0b0b0b"
INK2 = "#52514e"
SURFACE = "#ffffff"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": INK2,
    "svg.fonttype": "none",
})
os.makedirs("figures", exist_ok=True)


def _dir_color(irr):
    if irr > 1.02:
        return RED
    if irr < 0.98:
        return BLUE
    return INK2


def _row(ax, y, irr, lo, hi, weight, wmax, label=None, is_pooled=False):
    """Draw one forest row at height y on a log-x axis."""
    color = _dir_color(irr)
    # CI whisker
    ax.plot([lo, hi], [y, y], color=color, lw=1.6, solid_capstyle="round", zorder=3)
    if is_pooled:
        h = 0.30
        diamond = Polygon([[lo, y], [irr, y + h], [hi, y], [irr, y - h]],
                          closed=True, facecolor=color, edgecolor="white", lw=1.2, zorder=5)
        ax.add_patch(diamond)
    else:
        # square sized by weight (area ∝ weight)
        frac = 0.35 * math.sqrt(weight / wmax) if wmax else 0.15
        frac = max(frac, 0.10)
        ax.add_patch(plt.Rectangle((irr * (1 - 0.0), y - frac), 0, 0))  # noop keep autoscale off
        ms = 4 + 12 * math.sqrt(weight / wmax) if wmax else 6
        ax.plot([irr], [y], marker="s", markersize=ms, color=color,
                markeredgecolor="white", markeredgewidth=0.8, zorder=4)


def forest_panel(ax, rows, title, xlim=(0.2, 2.6)):
    """rows: list of dicts {label, irr, lo, hi, weight, pooled, k, group}."""
    n = len(rows)
    ys = list(range(n, 0, -1))
    wmax = max((r["weight"] for r in rows if not r["pooled"]), default=1.0)

    ax.axvline(1.0, color=GRAY, lw=1.2, ls="--", zorder=1)
    for y, r in zip(ys, rows):
        _row(ax, y, r["irr"], r["lo"], r["hi"], r.get("weight", 0), wmax,
             is_pooled=r["pooled"])
        # left label
        weight_txt = ""
        ax.text(xlim[0] * 0.86, y, r["label"], ha="right", va="center",
                fontsize=8.2, color=INK if r["pooled"] else INK2,
                fontweight="bold" if r["pooled"] else "normal")
        # right stat
        stat = f"{r['irr']:.2f} ({r['lo']:.2f}–{r['hi']:.2f})"
        ax.text(xlim[1] * 1.04, y, stat, ha="left", va="center", fontsize=8.0,
                color=INK if r["pooled"] else INK2,
                fontweight="bold" if r["pooled"] else "normal")

    ax.set_xscale("log")
    ax.set_xlim(*xlim)
    ax.set_ylim(0.3, n + 0.9)
    ax.set_yticks([])
    for s in ("left", "right", "top"):
        ax.spines[s].set_visible(False)
    ticks = [0.25, 0.5, 1.0, 2.0]
    ticks = [t for t in ticks if xlim[0] <= t <= xlim[1]]
    ax.xaxis.set_major_locator(FixedLocator(ticks))
    ax.xaxis.set_major_formatter(FixedFormatter([f"{t:g}" for t in ticks]))
    ax.xaxis.set_minor_locator(NullLocator())          # kill log minor ticks
    ax.xaxis.set_minor_formatter(NullFormatter())
    ax.tick_params(axis="x", which="both", length=3, color=INK2, labelsize=8)
    ax.set_title(title, fontsize=10.5, fontweight="bold", color=INK, loc="left", pad=8)
    # directional guides (below the tick labels so they don't collide)
    ax.text(0.94, -0.11, "← lower than NHW", transform=ax.get_xaxis_transform(),
            ha="right", va="top", fontsize=7.2, color=BLUE)
    ax.text(1.06, -0.11, "higher than NHW →", transform=ax.get_xaxis_transform(),
            ha="left", va="top", fontsize=7.2, color=RED)


def _pmid(sid):
    """Human label tail from a Study id (last 8 digits of the PMID/hash)."""
    tail = sid.split("_")[-1].replace("PMID", "")
    return tail[:8]


def rows_for_group(group, outcome="invasive_incidence"):
    """One study row per record + a pooled diamond (if k>=2)."""
    ss = _subset(group, outcome)
    rows = []
    for s in sorted(ss, key=lambda x: x.irr):
        rows.append(dict(label=f"{s.source} · {_pmid(s.id)}",
                         irr=s.irr, lo=s.ci_low, hi=s.ci_high,
                         weight=1.0 / (s.se ** 2), pooled=False))
    if len(ss) >= 2:
        r = random_effects_meta(ss, method="REML", knha=True)
        rows.append(dict(label=f"Pooled (k={len(ss)}, I²={r['I2']:.0f}%)",
                         irr=r["irr"], lo=r["ci_low"], hi=r["ci_high"],
                         weight=0, pooled=True))
    return rows


def pooled_or_single(group, outcome):
    """Return (irr, lo, hi, k) — pooled if k>=2 else the single study's values."""
    ss = _subset(group, outcome)
    if not ss:
        return None
    if len(ss) >= 2:
        r = random_effects_meta(ss, method="REML", knha=True)
        return r["irr"], r["ci_low"], r["ci_high"], len(ss)
    s = ss[0]
    return s.irr, s.ci_low, s.ci_high, 1


# ── Figure 1: aggregate 4-race (the convergence view) ────────────────────────
def fig1():
    groups = [("Black", "Black vs NHW"), ("Hispanic", "Hispanic vs NHW"),
              ("Asian", "Asian/API vs NHW"), ("AIAN", "AIAN vs NHW")]
    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.patch.set_facecolor(SURFACE)
    for ax, (g, title) in zip(axes.flat, groups):
        ax.set_facecolor(SURFACE)
        forest_panel(ax, rows_for_group(g), title)
    fig.suptitle("Invasive breast cancer incidence vs non-Hispanic White — aggregate racial groups",
                 fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left")
    fig.text(0.02, 0.945,
             "Random-effects (REML, Hartung–Knapp). Pooling shows convergence "
             "(Black CI crosses 1) but I²≈99% — the aggregate masks opposing sub-patterns.",
             fontsize=9, color=INK2, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    fig.savefig("figures/fig1_main_forest.png", dpi=300, facecolor=SURFACE)
    plt.close(fig)
    print("wrote figures/fig1_main_forest.png")


# ── Figure 2: disaggregated ethnic subgroups ─────────────────────────────────
def fig2():
    order = ["Korean", "Chinese", "AsianIndian", "Vietnamese", "Filipina",
             "Japanese", "NativeHawaiian"]
    label_map = {"AsianIndian": "Asian Indian/Pakistani", "NativeHawaiian": "Native Hawaiian"}
    rows = []
    for g in order:
        ss = _subset(g)
        if not ss:
            continue
        if len(ss) >= 2:
            r = random_effects_meta(ss, method="REML", knha=True)
            irr, lo, hi, k = r["irr"], r["ci_low"], r["ci_high"], len(ss)
        else:
            s = ss[0]
            irr, lo, hi, k = s.irr, s.ci_low, s.ci_high, 1
        rows.append(dict(label=f"{label_map.get(g, g)} (k={k})",
                         irr=irr, lo=lo, hi=hi, weight=1.0, pooled=(k >= 2)))
    fig, ax = plt.subplots(figsize=(9.5, 5.6))
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    forest_panel(ax, rows, "Disaggregated Asian / Pacific Islander ethnic subgroups vs NHW",
                 xlim=(0.16, 1.7))
    fig.text(0.02, 0.02,
             "Same aggregate 'Asian/API' category, disaggregated: Korean 0.34 ↔ "
             "Native Hawaiian 1.11 — a ~3× spread the pooled estimate hides.",
             fontsize=8.5, color=INK2, ha="left")
    fig.tight_layout(rect=[0, 0.05, 1, 1])
    fig.savefig("figures/fig2_subgroups_forest.png", dpi=300, facecolor=SURFACE)
    plt.close(fig)
    print("wrote figures/fig2_subgroups_forest.png")


# ── Figure 3: molecular subtypes — the aggressive-subtype gradient ───────────
def fig3():
    # order subtypes least→most aggressive
    subtypes = [
        ("hrpos_her2neg_incidence", "HR+/HER2−\n(luminal A)"),
        ("hrpos_incidence",         "HR-positive"),
        ("hrpos_her2pos_incidence", "HR+/HER2+\n(luminal B)"),
        ("hrneg_incidence",         "HR-negative"),
        ("hrneg_her2pos_incidence", "HER2-enriched\n(HR−/HER2+)"),
        ("tnbc_incidence",          "Triple-negative"),
    ]
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.2))
    fig.patch.set_facecolor(SURFACE)

    def spectrum(ax, group, title):
        rows = []
        for oc, lbl in subtypes:
            res = pooled_or_single(group, oc)
            if res is None:
                continue
            irr, lo, hi, k = res
            rows.append(dict(label=lbl + (f"  (k={k})" if k >= 2 else ""),
                             irr=irr, lo=lo, hi=hi, weight=1.0,
                             pooled=(k >= 2)))
        forest_panel(ax, rows, title, xlim=(0.4, 2.6))

    axes[0].set_facecolor(SURFACE)
    spectrum(axes[0], "Black", "Black vs NHW — across molecular subtypes")
    axes[1].set_facecolor(SURFACE)
    spectrum(axes[1], "NativeHawaiian", "Native Hawaiian vs NHW — across subtypes")

    fig.suptitle("Molecular-subtype–specific disparities: the aggressive-subtype gradient",
                 fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left")
    fig.text(0.02, 0.925,
             "Black excess rises with subtype aggressiveness (0.86 → 2.0 for TNBC). "
             "Native Hawaiian is elevated in HER2+ subtypes but LOW in TNBC (0.86) — "
             "the 'aggressive-subtype' excess is not a uniform minority effect.",
             fontsize=8.6, color=INK2, ha="left")
    fig.tight_layout(rect=[0, 0.04, 1, 0.9])
    fig.savefig("figures/fig3_subtypes_forest.png", dpi=300, facecolor=SURFACE)
    plt.close(fig)
    print("wrote figures/fig3_subtypes_forest.png")


# ── Figure 4: age crossover ──────────────────────────────────────────────────
def fig4():
    from run_meta_analysis_breast import AGE_CROSSOVER_15986118 as AC
    fig, (axL, axR) = plt.subplots(1, 2, figsize=(13, 5.6),
                                   gridspec_kw={"width_ratios": [1.7, 1]})
    fig.patch.set_facecolor(SURFACE)
    for ax in (axL, axR):
        ax.set_facecolor(SURFACE)

    # Left: NAACCR Black & API RR vs age band (line)
    bands = [r[0] for r in AC]
    x = list(range(len(bands)))
    black_rr = [r[3] for r in AC]
    black_lo = [r[4] for r in AC]
    black_hi = [r[5] for r in AC]
    api_rr = [r[6] for r in AC]
    axL.axhline(1.0, color=GRAY, lw=1.2, ls="--", zorder=1)
    # Black line with CI band
    axL.fill_between(x, black_lo, black_hi, color=RED, alpha=0.12, zorder=2)
    axL.plot(x, black_rr, "-o", color=RED, lw=2, ms=5, mec="white", mew=0.8,
             label="Black vs White", zorder=4)
    api_x = [i for i, v in zip(x, api_rr) if v is not None]
    api_y = [v for v in api_rr if v is not None]
    axL.plot(api_x, api_y, "-s", color=BLUE, lw=2, ms=4.5, mec="white", mew=0.8,
             label="API vs White", zorder=4)
    # crossover marker
    axL.annotate("crossover ≈ age 40–44", xy=(4, 1.02), xytext=(5.4, 1.45),
                 fontsize=8.5, color=INK2,
                 arrowprops=dict(arrowstyle="->", color=INK2, lw=1))
    axL.set_yscale("log")
    axL.set_yticks([0.4, 0.6, 1.0, 1.6, 2.0])
    axL.set_yticklabels(["0.4", "0.6", "1.0", "1.6", "2.0"], fontsize=8)
    axL.set_xticks(x)
    axL.set_xticklabels(bands, rotation=45, ha="right", fontsize=7.5)
    axL.set_ylabel("Rate ratio vs White (log)", fontsize=9, color=INK2)
    for s in ("top", "right"):
        axL.spines[s].set_visible(False)
    axL.legend(frameon=False, fontsize=8.5, loc="upper right")
    axL.set_title("Black–White age crossover (NAACCR 1994–1998, 15986118)",
                  fontsize=10.5, fontweight="bold", color=INK, loc="left")

    # Right: within-API crossover (Hawaii <50 vs >=50) — dumbbell
    groups = ["Japanese", "NativeHawaiian", "Filipino"]
    gl = {"NativeHawaiian": "Native Hawaiian"}
    ys = list(range(len(groups), 0, -1))
    axR.axvline(1.0, color=GRAY, lw=1.2, ls="--", zorder=1)
    for y, g in zip(ys, groups):
        lt = _subset(g, "invasive_incidence_age_lt50")
        ge = _subset(g, "invasive_incidence_age_ge50")
        if not lt or not ge:
            continue
        a, b = lt[0].irr, ge[0].irr
        axR.plot([a, b], [y, y], color=GRAY, lw=1.6, zorder=2)
        axR.plot([a], [y], "o", ms=9, color=BLUE, mec="white", mew=1, zorder=4)
        axR.plot([b], [y], "o", ms=9, color=RED, mec="white", mew=1, zorder=4)
        axR.text(0.62, y, gl.get(g, g), ha="right", va="center", fontsize=8.5, color=INK2)
    axR.set_xscale("log")
    axR.set_xlim(0.6, 1.6)
    axR.set_ylim(0.3, len(groups) + 0.7)
    axR.set_yticks([])
    axR.set_xticks([0.6, 0.8, 1.0, 1.2, 1.4])
    axR.set_xticklabels(["0.6", "0.8", "1.0", "1.2", "1.4"], fontsize=8)
    axR.xaxis.set_minor_locator(NullLocator())
    for s in ("top", "right", "left"):
        axR.spines[s].set_visible(False)
    axR.legend(handles=[Line2D([0], [0], marker="o", color="w", markerfacecolor=BLUE,
                               markersize=9, label="age <50"),
                        Line2D([0], [0], marker="o", color="w", markerfacecolor=RED,
                               markersize=9, label="age ≥50")],
               frameon=False, fontsize=8.5, loc="lower right")
    axR.set_title("Within-API crossover (Hawaii, 36504334)",
                  fontsize=10.5, fontweight="bold", color=INK, loc="left")

    fig.suptitle("Age crossover — disparities reverse across the lifespan",
                 fontsize=13, fontweight="bold", color=INK, x=0.02, ha="left")
    fig.text(0.02, 0.925,
             "Black incidence exceeds White before ~40 (RR 1.92 at 20–24), then falls "
             "below after 50. Within 'API', Japanese lead when young, Native Hawaiian when older.",
             fontsize=8.6, color=INK2, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    fig.savefig("figures/fig4_age_crossover.png", dpi=300, facecolor=SURFACE)
    plt.close(fig)
    print("wrote figures/fig4_age_crossover.png")


# ── Figure 5: PRISMA 2020 flow diagram ───────────────────────────────────────
def fig5():
    # Final counts (Codespace report_status.py cache 8f982a + analyst reconciliation).
    N_DEDUP = 941       # identified after deduplication
    N_ABS_EXCL = 456    # excluded at title/abstract (941 - 485)
    N_FULLTEXT = 485    # advanced past abstract → full-text assessed
    N_FT_EXCL = 458     # excluded at full text (incl. 23 analyst; +33006431 non-US/MIR)
    N_INCL = 27         # included in review after reconciliation
    N_QUANT = 14        # quantitative synthesis (meta-analysis)
    N_NARR = 13         # narrative synthesis (incl. 12115511, demoted)

    fig, ax = plt.subplots(figsize=(10.5, 9))
    fig.patch.set_facecolor(SURFACE); ax.set_facecolor(SURFACE)
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def box(x, y, w, h, text, fc="#f4f6f9", ec=INK2, bold_first=True):
        ax.add_patch(plt.Rectangle((x - w / 2, y - h / 2), w, h, facecolor=fc,
                                   edgecolor=ec, lw=1.3, zorder=2))
        lines = text.split("\n")
        ax.text(x, y, text, ha="center", va="center", fontsize=8.6,
                color=INK, zorder=3, linespacing=1.45)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color=INK2, lw=1.5), zorder=1)

    cx = 3.7  # main column x
    # boxes top→bottom
    box(cx, 9.2, 5.6, 1.05,
        "Records identified from databases   n = 1,187\n"
        "PubMed n = 686 · Embase n = 501",
        fc="#eaf1fb")
    box(cx, 7.4, 5.6, 1.0, f"Records screened (title / abstract)\nn = {N_DEDUP}")
    box(8.2, 9.2, 3.0, 0.85, "Duplicates removed\nn = 246", fc="#f4f6f9")
    arrow(cx + 2.8, 9.2, 8.2 - 1.5, 9.2)
    box(cx, 5.4, 5.6, 1.1, f"Reports assessed for eligibility\n(full text)   n = {N_FULLTEXT}")
    box(cx, 2.9, 6.0, 1.6,
        f"Studies included in the review   n = {N_INCL}\n"
        f"• Quantitative synthesis (meta-analysis)   n = {N_QUANT}\n"
        f"• Narrative synthesis (figure-only / non-US /   n = {N_NARR}\n"
        f"   other-design)",
        fc="#eaf7ee", ec="#1c7a3e")
    arrow(cx, 8.7, cx, 7.95)
    arrow(cx, 6.9, cx, 5.98)
    arrow(cx, 4.85, cx, 3.72)

    # side exclusion boxes
    ex = 8.2
    box(ex, 7.4, 3.0, 1.0, f"Excluded at\ntitle/abstract\nn = {N_ABS_EXCL}", fc="#fdecec", ec="#b5423f")
    arrow(cx + 2.8, 7.4, ex - 1.5, 7.4)
    box(ex, 5.4, 3.2, 2.2,
        f"Excluded at full text\nn = {N_FT_EXCL}\n"
        "— conference abstracts\n— news / editorials\n"
        "— wrong outcome (mortality,\n   stage, screening, MIR)\n"
        "— secondary/summary reports\n— no usable rate/RR data\n"
        "(incl. 23 analyst-adjudicated)",
        fc="#fdecec", ec="#b5423f")
    arrow(cx + 2.8, 5.4, ex - 1.6, 5.4)

    ax.text(0.2, 9.85, "PRISMA 2020 flow — racial/ethnic disparities in breast cancer incidence",
            fontsize=12, fontweight="bold", color=INK)
    fig.tight_layout()
    fig.savefig("figures/fig5_prisma.png", dpi=300, facecolor=SURFACE)
    plt.close(fig)
    print("wrote figures/fig5_prisma.png")


if __name__ == "__main__":
    fig1()
    fig2()
    fig3()
    fig4()
    fig5()
