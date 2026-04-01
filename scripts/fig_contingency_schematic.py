"""Contingency-table schematic figure (two-panel).

Panel (a): Standard 2x2 contingency table annotated with POD, FAR,
           CSI, PSS, and HSS formulas.
Panel (b): K x K multi-category extension (SPC categories) with
           diagonal highlighted and HSS annotation.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)


def _draw_2x2(ax):
    """Draw annotated 2x2 contingency table on *ax*."""
    # Cell positions: (col, row) with row 0 at top
    cells = {
        (0, 0): ("Hits\n(a)", PURPLE, 0.18),
        (1, 0): ("Misses\n(c)", MID_GREY, 0.10),
        (0, 1): ("False\nalarms\n(b)", MID_GREY, 0.10),
        (1, 1): ("Correct\nnegatives\n(d)", GREEN, 0.15),
    }

    for (c, r), (label, colour, alpha) in cells.items():
        rect = mpatches.FancyBboxPatch(
            (c, r), 1, 1,
            boxstyle="round,pad=0.03",
            facecolor=colour, alpha=alpha,
            edgecolor=DARK_GREY, linewidth=1.2,
        )
        ax.add_patch(rect)
        ax.text(
            c + 0.5, r + 0.5, label,
            ha="center", va="center", fontsize=8.5,
            fontweight="bold", color=DARK_GREY,
        )

    # Row/column headers
    ax.text(0.5, -0.15, "Observed\nYes", ha="center", va="top",
            fontsize=8, color=DARK_GREY, fontstyle="italic")
    ax.text(1.5, -0.15, "Observed\nNo", ha="center", va="top",
            fontsize=8, color=DARK_GREY, fontstyle="italic")
    ax.text(-0.15, 0.5, "Forecast\nYes", ha="right", va="center",
            fontsize=8, color=DARK_GREY, fontstyle="italic")
    ax.text(-0.15, 1.5, "Forecast\nNo", ha="right", va="center",
            fontsize=8, color=DARK_GREY, fontstyle="italic")

    # Metric annotations (right side and bottom)
    formula_kw = dict(fontsize=7.2, color=DARK_GREY,
                      fontfamily="monospace",
                      bbox=dict(boxstyle="round,pad=0.2",
                                facecolor="white",
                                edgecolor=MID_GREY, linewidth=0.5))

    # POD: right of row 0 — a / (a + c)
    ax.annotate(
        "POD = a/(a+c)",
        xy=(2, 0.5), xytext=(2.35, 0.25),
        ha="left", va="center", **formula_kw,
        arrowprops=dict(arrowstyle="-", color=MID_GREY, lw=0.6),
    )
    # FAR: right of row 0 — b / (a + b)
    ax.annotate(
        "FAR = b/(a+b)",
        xy=(1, 0.0), xytext=(2.35, 0.65),
        ha="left", va="center", **formula_kw,
        arrowprops=dict(arrowstyle="-", color=MID_GREY, lw=0.6),
    )
    # CSI: below centre
    ax.text(
        1.0, 2.30,
        "CSI = a/(a+b+c)",
        ha="center", va="top", **formula_kw,
    )
    # PSS: below CSI
    ax.text(
        1.0, 2.62,
        "PSS = a/(a+c) \u2212 b/(b+d)",
        ha="center", va="top", **formula_kw,
    )
    # HSS (2x2): below PSS
    ax.text(
        1.0, 2.94,
        "HSS = 2(ad\u2212bc) / ...",
        ha="center", va="top", **formula_kw,
    )

    ax.set_xlim(-0.5, 3.8)
    ax.set_ylim(-0.5, 3.2)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(a)  Binary (threshold) scoring",
                 fontsize=10, fontweight="bold", pad=10,
                 color=DARK_GREY)


def _draw_kxk(ax):
    """Draw annotated K x K schematic on *ax*."""
    K = SPC_N
    # Grid
    for r in range(K):
        for c in range(K):
            if r == c:
                colour = PURPLE
                alpha = 0.25
            elif abs(r - c) == 1:
                colour = PURPLE
                alpha = 0.08
            else:
                colour = LIGHT_GREY
                alpha = 0.5
            rect = mpatches.FancyBboxPatch(
                (c, r), 1, 1,
                boxstyle="round,pad=0.02",
                facecolor=colour, alpha=alpha,
                edgecolor=MID_GREY, linewidth=0.6,
            )
            ax.add_patch(rect)

    # Diagonal highlight boxes
    for k in range(K):
        rect = mpatches.FancyBboxPatch(
            (k, k), 1, 1,
            boxstyle="round,pad=0.02",
            facecolor="none",
            edgecolor=GREEN, linewidth=2.0, zorder=3,
        )
        ax.add_patch(rect)

    # Category labels
    for i, cat in enumerate(SPC_CATEGORIES):
        ax.text(i + 0.5, -0.15, cat, ha="center", va="top",
                fontsize=7, color=DARK_GREY, rotation=45)
        ax.text(-0.15, i + 0.5, cat, ha="right", va="center",
                fontsize=7, color=DARK_GREY)

    # Axis labels
    ax.text(K / 2, -0.75, "Observed category",
            ha="center", va="top", fontsize=9, color=DARK_GREY)
    ax.text(-0.85, K / 2, "Forecast\npeak",
            ha="right", va="center", fontsize=9,
            color=DARK_GREY, rotation=0)

    # Diagonal label
    ax.annotate(
        "Correct\n(diagonal)",
        xy=(3.5, 3.5), xytext=(K + 0.4, 1.5),
        ha="left", va="center", fontsize=7.5,
        color=GREEN, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0),
    )

    # Near-miss label
    ax.annotate(
        "Near-miss\n(\u00b11 category)",
        xy=(4, 3), xytext=(K + 0.4, 3.0),
        ha="left", va="center", fontsize=7.5,
        color=PURPLE, fontweight="bold",
        arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.0),
    )

    # HSS annotation
    formula_kw = dict(
        fontsize=7.5, color=DARK_GREY, fontfamily="monospace",
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                  edgecolor=MID_GREY, linewidth=0.5),
    )
    ax.text(
        K / 2, K + 0.55,
        "HSS = (correct \u2212 expected) / (n \u2212 expected)",
        ha="center", va="top", **formula_kw,
    )

    # Threshold bracket for binary reduction
    bracket_y = K + 1.1
    ax.annotate(
        "", xy=(0, bracket_y), xytext=(2, bracket_y),
        arrowprops=dict(arrowstyle="<->", color=PURPLE, lw=1.2),
    )
    ax.text(1, bracket_y + 0.2, "threshold $t$",
            ha="center", va="bottom", fontsize=7,
            color=PURPLE, fontstyle="italic")

    ax.set_xlim(-1.2, K + 2.5)
    ax.set_ylim(-1.0, K + 1.6)
    ax.invert_yaxis()
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(
        r"(b)  Multi-category ($K \times K$) scoring",
        fontsize=10, fontweight="bold", pad=10,
        color=DARK_GREY,
    )


def main():
    apply_style()
    fig = plt.figure(figsize=(11.0, 4.8))
    gs = GridSpec(1, 2, figure=fig, width_ratios=[1, 1.3],
                  wspace=0.35)
    ax_2x2 = fig.add_subplot(gs[0])
    ax_kxk = fig.add_subplot(gs[1])

    _draw_2x2(ax_2x2)
    _draw_kxk(ax_kxk)

    fig.subplots_adjust(left=0.05, right=0.95, wspace=0.35)
    save_fig(fig, "contingency_schematic")


if __name__ == "__main__":
    main()
