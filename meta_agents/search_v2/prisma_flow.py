#!/usr/bin/env python3
"""PRISMA 2020 flow diagram (databases-only identification arm) from
outputs/PRISMA_COUNTS.md numbers. Writes outputs/Fig_PRISMA.png."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")

BLUE = "#dbe7f3"
EDGE = "#3a5a80"


def box(ax, x, y, w, h, text, fc=BLUE):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=EDGE, lw=1.3, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=8.2,
            zorder=3, wrap=True)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=13, color=EDGE, lw=1.2, zorder=1))


def main():
    fig, ax = plt.subplots(figsize=(9.2, 8.8))
    ax.set_xlim(0, 10); ax.set_ylim(0, 12); ax.axis("off")

    # stage labels (left rotated)
    for y, lab in [(10.6, "Identification"), (7.3, "Screening"), (2.0, "Included")]:
        ax.text(0.15, y, lab, rotation=90, va="center", ha="center",
                fontsize=10, fontweight="bold", color=EDGE)

    # main column x, right column x
    mx, mw = 1.1, 5.4
    rx, rw = 7.2, 2.6

    box(ax, mx, 10.4, mw, 1.3,
        "Records identified from databases (n = 9,099)\n"
        "PubMed/MEDLINE 1,331 · Embase 3,248 · Scopus 2,438 · Web of Science 2,082")
    box(ax, rx, 10.5, rw, 1.1, "Duplicate records removed\nbefore screening (n = 4,306)")
    arrow(ax, mx + mw, 11.05, rx, 11.05)

    box(ax, mx, 8.5, mw, 1.0, "Records screened\n(title/abstract) (n = 4,793)")
    arrow(ax, mx + mw / 2, 10.4, mx + mw / 2, 9.5)
    box(ax, rx, 8.55, rw, 0.9, "Records excluded\n(n = 4,551)")
    arrow(ax, mx + mw, 9.0, rx, 9.0)

    box(ax, mx, 6.5, mw, 1.0, "Reports assessed for eligibility\n(full text) (n = 242)")
    arrow(ax, mx + mw / 2, 8.5, mx + mw / 2, 7.5)
    box(ax, rx, 6.2, rw, 1.6,
        "Reports excluded (n = 79):\noverlapping/duplicate dataset,\nno age-adjusted rate by race,\nfull text unavailable, wrong\noutcome/measure")
    arrow(ax, mx + mw, 7.0, rx, 7.0)

    box(ax, mx, 3.9, mw, 1.3,
        "Studies included in the review (n = 163)\n"
        "Quantitative synthesis: 48 eligible (43 with extractable data)\n"
        "Narrative synthesis only: 115", fc="#cfe6d4")
    arrow(ax, mx + mw / 2, 6.5, mx + mw / 2, 5.2)

    box(ax, mx, 2.2, mw, 1.1,
        "Studies contributing >=1 estimate to the meta-analysis (n = 43;\n"
        "144 estimates; 28 studies supplied a main-analysis representative)",
        fc="#cfe6d4")
    arrow(ax, mx + mw / 2, 3.9, mx + mw / 2, 3.3)

    ax.text(mx, 0.9, "PRISMA 2020 flow diagram. Single-reviewer screening with "
            "AI assistance. Search date 7 Aug 2026.", fontsize=7.5, color="#555")
    fig.savefig(os.path.join(OUT, "Fig_PRISMA.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote outputs/Fig_PRISMA.png")


if __name__ == "__main__":
    main()
