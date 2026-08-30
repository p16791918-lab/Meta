#!/usr/bin/env python3
"""PROTOTYPE ONLY — does not touch the manuscript pipeline.
Draws the professor's Example Figure 2 layout (aggregate-to-disaggregated forest
with 95% CI) for AANHPI + Hispanic/Latina + AI/AN, using our CURRENT data from
outputs/Table_main_forest.csv. Writes outputs/PROTO_Fig2_merged_forest.png."""
import os, csv
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "Table_main_forest.csv")

d = {}
for r in csv.DictReader(open(SRC, encoding="utf-8")):
    d[(r["dimension"], r["group"])] = (float(r["irr"]), float(r["ci_lo"]), float(r["ci_hi"]))

def g(dim, grp):
    return d[(dim, grp)]

# (label, irr, lo, hi, is_aggregate) top->bottom, mirroring the example order
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
    ("AI/AN", [
        ("AI/AN aggregate", *g("aggregate-vs-NHW", "AIAN"), True),
        ("Navajo", *g("AIAN", "AIAN (Navajo)"), False),
        ("Southern Plains", *g("AIAN", "AIAN (Southern Plains)"), False),
        ("Northern Plains", *g("AIAN", "AIAN (Northern Plains)"), False),
    ]),
]

# lay out rows top->bottom with a blank gap + header between blocks
rows = []           # (y, kind, ...)
y = 0.0
GAP = 1.2
for bi, (title, items) in enumerate(blocks):
    if bi > 0:
        y -= GAP
    rows.append(("header", y, title))
    y -= 1.0
    for (lab, irr, lo, hi, agg) in items:
        rows.append(("point", y, lab, irr, lo, hi, agg))
        y -= 1.0

ymin = y
fig, ax = plt.subplots(figsize=(11.5, 12.2))
ax.set_xscale("log")
ax.axvline(1.0, color="#3a5a80", ls="--", lw=1.1, zorder=1)

palette = ["#e8843c", "#3aa03a", "#d1352b", "#8a4fc4", "#7a5c46", "#e169b0",
           "#8a8a8a", "#c9c11f", "#33bfc9", "#4c78c8", "#2ca02c", "#e8843c",
           "#3aa03a"]
ci = 0
for row in rows:
    if row[0] == "header":
        _, yy, title = row
        ax.text(0.092, yy, title, fontsize=12, fontweight="bold", va="center", ha="left")
        continue
    _, yy, lab, irr, lo, hi, agg = row
    ax.plot([lo, hi], [yy, yy], color="#3a7bd5", lw=1.6, zorder=2)
    if agg:
        ax.plot(irr, yy, marker="D", ms=13, color="#c0392b" if "AI/AN" in lab or "Hispanic" in lab else "#2b5fa8",
                zorder=3, mec="white", mew=0.6)
        ax.text(0.10, yy, lab, fontsize=10.5, fontweight="bold", va="center", ha="left")
    else:
        ax.plot(irr, yy, marker="o", ms=8, color=palette[ci % len(palette)], zorder=3, mec="white", mew=0.6)
        ci += 1
        ax.text(0.135, yy, lab, fontsize=10, va="center", ha="left")
    ax.text(1.62, yy, f"{irr:.3f} [{lo:.3f}, {hi:.3f}]", fontsize=9.5, va="center", ha="left")

ax.set_xlim(0.09, 1.55)
ax.set_ylim(ymin - 0.6, 1.4)
ax.set_yticks([])
for s in ("top", "right", "left"):
    ax.spines[s].set_visible(False)
ax.set_xticks([0.1, 0.2, 0.5, 1.0, 1.5])
ax.set_xticklabels(["0.1", "0.2", "0.5", "1.0", "1.5"])
ax.set_xlabel("Incidence rate ratio versus non-Hispanic White reference (log scale)", fontsize=11)
ax.text(0.30, 1.15, "Lower incidence", fontsize=10, color="#555", ha="center")
ax.text(1.28, 1.15, "Higher incidence", fontsize=10, color="#555", ha="center")
ax.set_title("PROTOTYPE Figure 2. Aggregate-to-disaggregated heterogeneity with 95% CIs\n"
             "(AANHPI, Hispanic/Latina, AI/AN — one representative estimate per cell)",
             fontsize=12.5)
fig.tight_layout()
out = os.path.join(HERE, "PROTO_Fig2_merged_forest.png")
fig.savefig(out, dpi=170, bbox_inches="tight")
plt.close(fig)
print("wrote", out)
