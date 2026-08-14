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
    fig, ax = plt.subplots(figsize=(10.6, 9.2))
    ax.set_xlim(0, 12); ax.set_ylim(0, 12); ax.axis("off")

    # stage labels (left rotated)
    for y, lab in [(10.5, "Identification"), (7.0, "Screening"), (2.6, "Included")]:
        ax.text(0.2, y, lab, rotation=90, va="center", ha="center",
                fontsize=10, fontweight="bold", color=EDGE)

    # main column x, right column x
    mx, mw = 0.9, 6.4
    rx, rw = 8.0, 3.4
    FS = 8.0

    def b(x, y, w, h, t, fc=BLUE):
        ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=EDGE, lw=1.3, zorder=2))
        ax.text(x + w / 2, y + h / 2, t, ha="center", va="center", fontsize=FS, zorder=3)

    b(mx, 10.2, mw, 1.5,
      "Records identified from databases (n = 9,099)\n"
      "PubMed/MEDLINE 1,331 · Embase 3,248\n"
      "Scopus 2,438 · Web of Science 2,082")
    b(rx, 10.45, rw, 1.0, "Duplicate records removed\nbefore screening (n = 4,306)")
    arrow(ax, mx + mw, 10.95, rx, 10.95)

    b(mx, 8.4, mw, 1.0, "Records screened\n(title/abstract) (n = 4,793)")
    arrow(ax, mx + mw / 2, 10.2, mx + mw / 2, 9.4)
    b(rx, 7.95, rw, 1.5,
      "Records excluded (n = 4,551):\n"
      "not relevant to topic (n = 3,082);\n"
      "not a US registry-based study (n = 1,296);\n"
      "editorial / letter / conference (n = 173)")
    arrow(ax, mx + mw, 8.9, rx, 8.9)

    b(mx, 6.4, mw, 1.0, "Reports assessed for eligibility\n(full text) (n = 242)")
    arrow(ax, mx + mw / 2, 8.4, mx + mw / 2, 7.4)
    b(rx, 5.7, rw, 1.9,
      "Reports excluded (n = 79):\n"
      "overlapping / duplicate dataset (n = 55);\n"
      "did not report eligible outcome (n = 12);\n"
      "full text unavailable (n = 9);\n"
      "ineligible population (n = 3)")
    arrow(ax, mx + mw, 6.9, rx, 6.9)

    b(mx, 3.7, mw, 1.5,
      "Studies included in the review (n = 163)\n"
      "Quantitative synthesis: 48 eligible\n(43 with extractable data)\n"
      "Narrative synthesis only: 115", fc="#cfe6d4")
    arrow(ax, mx + mw / 2, 6.4, mx + mw / 2, 5.2)

    b(mx, 1.9, mw, 1.3,
      "Studies contributing ≥1 estimate to the\nmeta-analysis (n = 43; 144 estimates;\n"
      "28 supplied a main-analysis representative)", fc="#cfe6d4")
    arrow(ax, mx + mw / 2, 3.7, mx + mw / 2, 3.2)

    ax.text(mx, 0.8, "PRISMA 2020 flow diagram. Single-reviewer screening with "
            "AI assistance. Search date 7 Aug 2026.", fontsize=7.5, color="#555")
    fig.savefig(os.path.join(OUT, "Fig_PRISMA.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote outputs/Fig_PRISMA.png")


if __name__ == "__main__":
    main()
