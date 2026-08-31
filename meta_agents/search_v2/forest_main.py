#!/usr/bin/env python3
"""Main-text Figure 2 — aggregate-to-disaggregated heterogeneity forest with 95% CIs
for the three disaggregatable categories (AANHPI, Hispanic/Latina, AI/AN). One
representative estimate per analytic cell, read from outputs/Table_main_forest.csv.
NHB and Middle Eastern (no subgroups) are shown in the heatmap and Table 1, not here.
Writes outputs/Fig_forest_main.png."""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
SRC = os.path.join(OUT, "Table_main_forest.csv")

d = {}
for r in csv.DictReader(open(SRC, encoding="utf-8")):
    d[(r["dimension"], r["group"])] = (float(r["irr"]), float(r["ci_lo"]), float(r["ci_hi"]))

def g(dim, grp):
    return d[(dim, grp)]

blocks = [
    ("AANHPI", [
        ("AANHPI aggregate", *g("aggregate-vs-NHW", "Asian/PI (aggregate)"), True),
        ("Hmong", *g("disaggregated-AANHPI", "Hmong"), False),
        ("Cambodian", *g("disaggregated-AANHPI", "Cambodian"), False),
        ("Laotian/Kampuchean", *g("disaggregated-AANHPI", "Laotian/Kampuchean"), False),
        ("Vietnamese", *g("disaggregated-AANHPI", "Vietnamese"), False),
        ("Korean", *g("disaggregated-AANHPI", "Korean"), False),
        ("Chinese", *g("disaggregated-AANHPI", "Chinese"), False),
        ("Filipina", *g("disaggregated-AANHPI", "Filipina"), False),
        ("Asian Indian/Pakistani", *g("disaggregated-AANHPI", "Asian Indian/Pakistani"), False),
        ("Japanese", *g("disaggregated-AANHPI", "Japanese"), False),
        ("Guamanian/Chamorro/Samoan", *g("disaggregated-AANHPI", "Guamanian/Chamorro/Samoan"), False),
        ("Native Hawaiian", *g("disaggregated-AANHPI", "Native Hawaiian"), False),
        ("NHPI aggregate", *g("disaggregated-AANHPI", "Native Hawaiian/PI (aggregate)"), False),
    ]),
    ("Hispanic/Latina", [
        ("Hispanic aggregate", *g("aggregate-vs-NHW", "Hispanic"), True),
        ("Mexican", *g("Hispanic-origin", "Mexican"), False),
        ("New Latino", *g("Hispanic-origin", "New Latino"), False),
        ("Cuban", *g("Hispanic-origin", "Cuban"), False),
        ("Puerto Rican", *g("Hispanic-origin", "Puerto Rican"), False),
    ]),
    ("American Indian and Alaska Native", [
        ("AI/AN aggregate", *g("aggregate-vs-NHW", "AIAN"), True),
        ("Navajo area", *g("AIAN", "AIAN (Navajo)"), False),
        ("Southern Plains", *g("AIAN", "AIAN (Southern Plains)"), False),
        ("Northern Plains", *g("AIAN", "AIAN (Northern Plains)"), False),
    ]),
]

# lay out rows top->bottom
rows = []
y = 0.0
GAP = 1.1
for bi, (title, items) in enumerate(blocks):
    if bi > 0:
        y -= GAP
    rows.append(("header", y, title))
    y -= 1.0
    for it in items:
        rows.append(("point", y) + it)
        y -= 1.0
ymin = y

fig, ax = plt.subplots(figsize=(10.5, 12.6))
fig.subplots_adjust(left=0.34, right=0.80, top=0.93, bottom=0.06)
trans = ax.get_yaxis_transform()          # x: axes fraction, y: data
ax.axvline(1.0, color="#3a5a80", ls="--", lw=1.1, zorder=1)

palette = ["#e8843c", "#3aa03a", "#d1352b", "#8a4fc4", "#7a5c46", "#e169b0",
           "#8a8a8a", "#c9c11f", "#33bfc9", "#4c78c8", "#2ca02c", "#e8843c", "#3aa03a"]
ci = 0
for row in rows:
    if row[0] == "header":
        _, yy, title = row
        ax.text(-0.44, yy, title, transform=trans, fontsize=12, fontweight="bold",
                va="center", ha="left")
        continue
    _, yy, lab, irr, lo, hi, agg = row
    ax.plot([lo, hi], [yy, yy], color="#3a7bd5", lw=1.7, zorder=2)
    if agg:
        col = "#c0392b" if lab.startswith(("Hispanic", "AI/AN")) else "#2b5fa8"
        ax.plot(irr, yy, marker="D", ms=13, color=col, zorder=3, mec="white", mew=0.6)
        ax.text(-0.41, yy, lab, transform=trans, fontsize=10.5, fontweight="bold",
                va="center", ha="left")
    else:
        ax.plot(irr, yy, marker="o", ms=8, color=palette[ci % len(palette)], zorder=3,
                mec="white", mew=0.6)
        ci += 1
        ax.text(-0.37, yy, lab, transform=trans, fontsize=10, va="center", ha="left")
    ax.text(1.03, yy, f"{irr:.3f} [{lo:.3f}, {hi:.3f}]", transform=trans,
            fontsize=9.5, va="center", ha="left")

import matplotlib.ticker as mticker
ax.set_xscale("log")
ax.set_xlim(0.10, 1.55)
ax.set_ylim(ymin - 0.6, 1.7)
ax.set_yticks([])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.xaxis.set_minor_locator(mticker.NullLocator())   # no log minor ticks/labels
ax.xaxis.set_major_locator(mticker.FixedLocator([0.1, 0.2, 0.5, 1.0, 1.5]))
ax.xaxis.set_major_formatter(mticker.FixedFormatter(["0.1", "0.2", "0.5", "1.0", "1.5"]))
ax.set_xlabel("Incidence rate ratio versus non-Hispanic White reference (log scale)", fontsize=11)
ax.text(0.32, 1.28, "Lower incidence", transform=trans, fontsize=10, color="#555", ha="center")
ax.text(1.28, 1.28, "Higher incidence", transform=trans, fontsize=10, color="#555", ha="center")
ax.set_title("Aggregate-to-disaggregated heterogeneity with 95% confidence intervals",
             fontsize=12.5, pad=16)
fig.savefig(os.path.join(OUT, "Fig_forest_main.png"), dpi=200)
plt.close(fig)
print("wrote outputs/Fig_forest_main.png")
