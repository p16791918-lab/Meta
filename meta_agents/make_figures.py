"""
Generate Figure 1 (PRISMA 2020) and Figure 2 (NOS Risk of Bias)
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from pathlib import Path

OUT = Path("output_20260417_093053")

# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 1 — PRISMA 2020 Flow Diagram
# ═══════════════════════════════════════════════════════════════════════════

def draw_box(ax, x, y, w, h, text, color="#dce9f5", fontsize=11,
             bold=False, text_color="black"):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.04",
                         facecolor=color, edgecolor="#2a6099",
                         linewidth=1.8, zorder=3)
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
            fontweight=weight, color=text_color,
            wrap=True, multialignment="center", zorder=4,
            linespacing=1.5)

def arrow(ax, x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#2a6099",
                                lw=2.0, mutation_scale=18),
                zorder=2)

fig, ax = plt.subplots(figsize=(14, 20))
ax.set_xlim(0, 10)
ax.set_ylim(0, 14)
ax.axis("off")
ax.set_facecolor("white")
fig.patch.set_facecolor("white")

# ── IDENTIFICATION ──────────────────────────────────────────────────────────
ax.text(0.25, 13.5, "Identification", fontsize=13, fontweight="bold",
        color="white",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#2a6099", edgecolor="none"))

draw_box(ax, 5, 13.0, 7, 0.85,
         "Records identified from Embase\n(2000–2025)\n(n = 107)",
         color="#dce9f5", fontsize=12)

# ── SCREENING ───────────────────────────────────────────────────────────────
ax.text(0.25, 11.5, "Screening", fontsize=13, fontweight="bold",
        color="white",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#2a6099", edgecolor="none"))

arrow(ax, 5, 12.57, 5, 11.95)

draw_box(ax, 5, 11.55, 7, 0.75,
         "Records after duplicate removal\n(n = 43)", color="#dce9f5", fontsize=12)

arrow(ax, 5, 11.17, 5, 10.45)

draw_box(ax, 3.6, 10.0, 4.8, 0.85,
         "Records screened\n(title & abstract, Phase 1)\n(n = 43)",
         color="#dce9f5", fontsize=12)

# exclusion box Phase 1
draw_box(ax, 8.3, 10.0, 3.0, 1.3,
         "Excluded (n = 15)\n• Non-skin cancer (n = 6)\n• Treatment outcomes only (n = 4)\n• Review / no primary data (n = 3)\n• Case series (n = 2)",
         color="#fce8e8", fontsize=10)
ax.annotate("", xy=(6.6, 10.0), xytext=(6.8, 10.0),
            arrowprops=dict(arrowstyle="-|>", color="#cc3333", lw=1.8, mutation_scale=16))

arrow(ax, 3.6, 9.57, 3.6, 8.9)

draw_box(ax, 3.6, 8.5, 4.8, 0.75,
         "Full-text articles assessed\n(Phase 2)\n(n = 28)",
         color="#dce9f5", fontsize=12)

# exclusion box Phase 2
draw_box(ax, 8.3, 8.5, 3.0, 1.2,
         "Excluded (n = 14)\n• Insufficient race/eth. data (n = 6)\n• Outcome not extractable (n = 5)\n• Conference abstract (n = 3)",
         color="#fce8e8", fontsize=10)
ax.annotate("", xy=(6.0, 8.5), xytext=(6.8, 8.5),
            arrowprops=dict(arrowstyle="-|>", color="#cc3333", lw=1.8, mutation_scale=16))

# ── INCLUDED ────────────────────────────────────────────────────────────────
ax.text(0.25, 7.2, "Included", fontsize=13, fontweight="bold",
        color="white",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#2a6099", edgecolor="none"))

arrow(ax, 3.6, 8.12, 3.6, 7.55)

draw_box(ax, 3.6, 7.15, 4.8, 0.75,
         "Studies included in qualitative synthesis\n(n = 14)",
         color="#e6f4ea", bold=True, fontsize=12)

arrow(ax, 3.6, 6.77, 3.6, 6.1)

draw_box(ax, 3.6, 5.7, 4.8, 0.75,
         "Studies included in quantitative meta-analysis\n(n = 13)",
         color="#e6f4ea", bold=True, fontsize=12)

# ── Note ────────────────────────────────────────────────────────────────────
ax.text(5, 4.9,
        "One study (Chi 2011) included in qualitative synthesis only\n"
        "(ethnic Chinese cohort; no NHW comparator for pooling)",
        ha="center", va="center", fontsize=10, color="#555555", style="italic")

ax.set_title("Figure 1. PRISMA 2020 Flow Diagram",
             fontsize=15, fontweight="bold", pad=14)

fig.tight_layout()
fig.savefig(OUT / "figure1_prisma.png", dpi=300, bbox_inches="tight",
            facecolor="white")
plt.close()
print("[✓] figure1_prisma.png saved")


# ═══════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Newcastle-Ottawa Scale Risk of Bias Summary
# ═══════════════════════════════════════════════════════════════════════════

studies = [
    "Akgun 2025",
    "Rypka 2024",
    "Holman 2023",
    "Lam 2022",
    "Wang 2016",
    "Baldwin 2016",
    "Clairwood 2014",
    "Wu 2011",
    "Hu 2009",
    "Zell 2008",
    "Cormier 2006",
    "Murase 2005",
    "Halder 2003",
    "Feng 2013",
]

# NOS domains: Selection (4 pts) | Comparability (2 pts) | Outcome (3 pts)
# Ratings: "L" = Low risk (green), "M" = Moderate risk (yellow), "H" = High (red)
# Columns: S1 S2 S3 S4  C1 C2  O1 O2 O3
domain_scores = {
    #                  S1   S2   S3   S4   C1   C2   O1   O2   O3
    "Akgun 2025":    ["L", "L", "L", "L", "L", "L", "L", "L", "L"],
    "Rypka 2024":    ["L", "L", "L", "M", "L", "L", "L", "L", "L"],
    "Holman 2023":   ["L", "L", "L", "L", "L", "L", "L", "L", "L"],
    "Lam 2022":      ["L", "L", "L", "L", "L", "L", "L", "L", "M"],
    "Wang 2016":     ["L", "L", "L", "L", "L", "M", "L", "L", "L"],
    "Baldwin 2016":  ["L", "L", "L", "M", "L", "M", "L", "M", "L"],
    "Clairwood 2014":["L", "L", "M", "M", "L", "M", "L", "L", "L"],
    "Wu 2011":       ["L", "L", "L", "L", "L", "L", "L", "L", "L"],
    "Hu 2009":       ["L", "L", "L", "M", "L", "L", "L", "L", "L"],
    "Zell 2008":     ["L", "L", "M", "M", "M", "M", "L", "L", "L"],
    "Cormier 2006":  ["L", "L", "L", "L", "L", "L", "L", "L", "L"],
    "Murase 2005":   ["L", "L", "M", "M", "M", "M", "L", "M", "M"],
    "Halder 2003":   ["M", "L", "M", "M", "M", "M", "L", "M", "M"],
    "Feng 2013":     ["L", "L", "L", "M", "L", "M", "L", "L", "L"],
}

col_labels = [
    "S1\nRepresentativeness\nof exposed cohort",
    "S2\nSelection of\nnon-exposed",
    "S3\nAscertainment\nof exposure",
    "S4\nOutcome not\npresent at start",
    "C1\nComparability\n(primary factor)",
    "C2\nComparability\n(additional factor)",
    "O1\nAssessment\nof outcome",
    "O2\nFollow-up\nadequacy",
    "O3\nAdequacy of\nfollow-up",
]

domain_groups = ["Selection (4 items)", "Comparability (2 items)", "Outcome (3 items)"]
domain_cols   = [4, 2, 3]

color_map = {"L": "#2ecc71", "M": "#f1c40f", "H": "#e74c3c"}
label_map  = {"L": "Low", "M": "Moderate", "H": "High"}

n_studies = len(studies)
n_cols    = 9

fig, ax = plt.subplots(figsize=(20, 12))
ax.set_xlim(-0.5, n_cols + 3.5)
ax.set_ylim(-1.2, n_studies + 2.0)
ax.axis("off")
fig.patch.set_facecolor("white")

# ── Domain group headers ──────────────────────────────────────────────────
group_starts = [0, 4, 6]
for gi, (label, start, width) in enumerate(zip(domain_groups, group_starts, domain_cols)):
    cx = start + width / 2 - 0.5
    rect = FancyBboxPatch((start - 0.45, n_studies + 0.15), width - 0.1, 0.75,
                           boxstyle="round,pad=0.05",
                           facecolor="#2a6099", edgecolor="none", zorder=3)
    ax.add_patch(rect)
    ax.text(cx, n_studies + 0.95, label, ha="center", va="center",
            fontsize=11, fontweight="bold", color="white", zorder=4)

# ── Column headers ────────────────────────────────────────────────────────
for ci, col in enumerate(col_labels):
    ax.text(ci, n_studies + 0.1, col, ha="center", va="bottom",
            fontsize=9, color="#222", multialignment="center", linespacing=1.3)

# ── Study labels ──────────────────────────────────────────────────────────
for si, study in enumerate(studies):
    row = n_studies - 1 - si
    ax.text(-0.65, row, study, ha="right", va="center",
            fontsize=11, color="#111")

# ── Dots ──────────────────────────────────────────────────────────────────
for si, study in enumerate(studies):
    row = n_studies - 1 - si
    scores = domain_scores[study]
    for ci, score in enumerate(scores):
        circle = plt.Circle((ci, row), 0.36,
                             color=color_map[score], zorder=3)
        ax.add_patch(circle)
        ax.text(ci, row, score[0], ha="center", va="center",
                fontsize=9.5, fontweight="bold", color="white", zorder=4)

    # NOS total score
    nos_total = sum(1 for s in scores if s == "L")
    risk = "Low"      if nos_total >= 7 else \
           "Moderate" if nos_total >= 4 else "High"
    risk_color = "#27ae60" if risk == "Low" else \
                 "#d4a017" if risk == "Moderate" else "#e74c3c"
    ax.text(n_cols + 0.2, row,
            f"NOS = {nos_total}  ({risk})",
            ha="left", va="center", fontsize=10.5, color=risk_color,
            fontweight="bold")

# ── Alternating row shading ───────────────────────────────────────────────
for si in range(n_studies):
    row = n_studies - 1 - si
    if si % 2 == 0:
        rect = plt.Rectangle((-4.5, row - 0.48), 18, 0.96,
                              color="#f5f5f5", zorder=0)
        ax.add_patch(rect)

# ── Vertical dividers between domain groups ───────────────────────────────
for x_div in [3.5, 5.5]:
    ax.axvline(x=x_div, ymin=0.04, ymax=0.96,
               color="#aaa", linewidth=1.0, linestyle="--", zorder=1)

# ── Legend ────────────────────────────────────────────────────────────────
legend_patches = [
    mpatches.Patch(color="#2ecc71", label="Low risk of bias"),
    mpatches.Patch(color="#f1c40f", label="Moderate risk of bias"),
    mpatches.Patch(color="#e74c3c", label="High risk of bias"),
]
ax.legend(handles=legend_patches, loc="lower right",
          fontsize=11, framealpha=0.95, edgecolor="#ccc",
          bbox_to_anchor=(1.02, -0.08))

ax.set_title(
    "Figure 2. Risk of Bias Assessment — Newcastle-Ottawa Scale (NOS)\n"
    "S = Selection  |  C = Comparability  |  O = Outcome/Exposure",
    fontsize=14, fontweight="bold", pad=16)

fig.tight_layout()
fig.savefig(OUT / "figure2_rob.png", dpi=300, bbox_inches="tight",
            facecolor="white")
plt.close()
print("[✓] figure2_rob.png saved")
