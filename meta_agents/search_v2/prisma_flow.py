#!/usr/bin/env python3
"""PRISMA 2020 flow diagram, two-arm layout (databases/registers + other methods),
from outputs/PRISMA_COUNTS.md numbers. Writes outputs/Fig_PRISMA.png."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "outputs")
BLUE = "#dbe7f3"
EDGE = "#3a5a80"
FS = 7.6


def box(ax, x, y, w, h, text, fc=BLUE, fs=FS):
    ax.add_patch(Rectangle((x, y), w, h, facecolor=fc, edgecolor=EDGE, lw=1.2, zorder=2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, zorder=3)


def arrow(ax, x1, y1, x2, y2):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                 mutation_scale=11, color=EDGE, lw=1.1, zorder=1))


def line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color=EDGE, lw=1.1, zorder=1)


def main():
    fig, ax = plt.subplots(figsize=(13.6, 11.6))
    ax.set_xlim(0, 16); ax.set_ylim(0, 14); ax.axis("off")

    # columns
    lmx, lmw = 1.2, 4.7          # left arm main
    lex, lew = 6.4, 3.9          # left arm exclusions
    rmx, rmw = 11.2, 4.1         # right arm (other methods)

    # stage labels
    for y, lab in [(11.9, "Identification"), (8.3, "Screening"), (2.4, "Included")]:
        ax.text(0.25, y, lab, rotation=90, va="center", ha="center",
                fontsize=10, fontweight="bold", color=EDGE)

    # arm headers
    ax.text((lmx + lex + lew) / 2, 13.4, "Identification of studies via databases and registers",
            ha="center", fontsize=8.5, fontweight="bold", color=EDGE)
    ax.text(rmx + rmw / 2, 13.4, "Identification of studies via other methods",
            ha="center", fontsize=8.5, fontweight="bold", color=EDGE)

    # ---- left arm ----
    box(ax, lmx, 11.3, lmw, 1.35,
        "Records identified from:\nDatabases (n = 9,099)\nRegisters (n = 0)")
    box(ax, lex, 11.5, lew, 1.0,
        "Records removed before screening:\nDuplicate records removed (n = 4,306)")
    arrow(ax, lmx + lmw, 11.98, lex, 11.98)

    box(ax, lmx, 9.5, lmw, 0.9, "Records screened\n(n = 4,793)")
    arrow(ax, lmx + lmw / 2, 11.3, lmx + lmw / 2, 10.4)
    box(ax, lex, 8.85, lew, 1.6,
        "Records excluded (n = 4,551):\nnot relevant to topic (n = 3,082);\n"
        "not a US registry-based study (n = 1,296);\neditorial / letter / conference (n = 173)")
    arrow(ax, lmx + lmw, 9.95, lex, 9.95)

    box(ax, lmx, 7.5, lmw, 0.9, "Reports sought for retrieval\n(n = 242)")
    arrow(ax, lmx + lmw / 2, 9.5, lmx + lmw / 2, 8.4)
    box(ax, lex, 7.55, lew, 0.8, "Reports not retrieved\n(n = 0)")
    arrow(ax, lmx + lmw, 7.95, lex, 7.95)

    box(ax, lmx, 5.4, lmw, 0.9, "Reports assessed for eligibility\n(n = 242)")
    arrow(ax, lmx + lmw / 2, 7.5, lmx + lmw / 2, 6.3)
    box(ax, lex, 4.7, lew, 1.7,
        "Reports excluded (n = 80):\noverlapping / duplicate dataset (n = 55);\n"
        "did not report eligible outcome (n = 12);\nfull text unavailable (n = 9);\n"
        "ineligible population (n = 3);\npreprint, not peer-reviewed (n = 1)")
    arrow(ax, lmx + lmw, 5.85, lex, 5.85)

    # ---- right arm (other methods) ----
    box(ax, rmx, 11.3, rmw, 1.35,
        "Records identified from:\nGrey literature (n = 0)\nCitation searching (n = 0)")
    box(ax, rmx, 5.4, rmw, 1.35,
        "Reports assessed for eligibility\n(n = 0)\nReports excluded (n = 0)")
    arrow(ax, rmx + rmw / 2, 11.3, rmx + rmw / 2, 6.75)

    # ---- included (spans left arm) ----
    incx, incw = 1.3, 8.7
    box(ax, incx, 3.0, incw, 1.3,
        "Studies included in the review (n = 162)\n"
        "Quantitative synthesis: 48 eligible (43 with extractable data)   |   Narrative synthesis only: 114",
        fc="#cfe6d4")
    arrow(ax, lmx + lmw / 2, 5.4, lmx + lmw / 2, 4.3)
    # right arm merges into included
    line(ax, rmx + rmw / 2, 5.4, rmx + rmw / 2, 3.65)
    arrow(ax, rmx + rmw / 2, 3.65, incx + incw, 3.65)

    box(ax, incx, 1.3, incw, 1.1,
        "Studies contributing ≥1 estimate to the quantitative synthesis\n"
        "(n = 43; 144 estimates; 28 supplied a main-analysis representative)",
        fc="#cfe6d4")
    arrow(ax, incx + incw / 2, 3.0, incx + incw / 2, 2.4)

    ax.text(0.6, 0.5, "PRISMA 2020 flow diagram. Single-reviewer screening with "
            "AI assistance. Search date 7 August 2026.", fontsize=7.2, color="#555")
    fig.savefig(os.path.join(OUT, "Fig_PRISMA.png"), dpi=200, bbox_inches="tight")
    plt.close(fig)
    print("wrote outputs/Fig_PRISMA.png")


if __name__ == "__main__":
    main()
