"""Figure 8: Three-lane verification summary schematic.

Flowchart-style diagram showing the three complementary verification lanes:
  Lane 1 — Scalar (RMSE, bias) evaluates the point forecast.
  Lane 2 — Probabilistic (IG via bridge) evaluates the converted probability.
  Lane 3 — Possibilistic (five-number scorecard) evaluates the native
            possibility distribution (the novel contribution).

Lane 3 is highlighted in purple; others use lighter colours.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
)

# Colours per lane
LANE_COLOURS = {
    1: "#B0BEC5",   # blue-grey (scalar)
    2: "#90CAF9",   # light blue (probabilistic)
    3: PURPLE,      # purple (possibilistic — novel)
}
LANE_TEXT = {
    1: "white",
    2: "white",
    3: "white",
}


def _box(ax, x, y, w, h, text, colour, text_colour="white",
         fontsize=9, fontweight="normal", alpha=1.0):
    """Draw a rounded box with centred text."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="round,pad=0.12",
        facecolor=colour, edgecolor=DARK_GREY,
        linewidth=0.8, alpha=alpha, zorder=3,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight,
            color=text_colour, zorder=4)


def _arrow(ax, x0, y0, x1, y1, **kwargs):
    """Draw a curved arrow between two points."""
    defaults = dict(arrowstyle="-|>", color=DARK_GREY, linewidth=1.0,
                    connectionstyle="arc3,rad=0.0", zorder=2)
    defaults.update(kwargs)
    arrow = FancyArrowPatch((x0, y0), (x1, y1), **defaults)
    ax.add_patch(arrow)


def main():
    apply_style()

    fig, ax = plt.subplots(figsize=(10.0, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    # ===== Top: forecast input =====
    _box(ax, 5.0, 6.3, 3.8, 0.7,
         "Possibilistic Forecast\n" + r"$\pi(\omega)$",
         DARK_GREY, fontsize=10, fontweight="bold")

    # Three vertical arrows from forecast box to lane headers
    lane_x = [1.8, 5.0, 8.2]
    for lx in lane_x:
        _arrow(ax, lx, 5.90, lx, 5.15)

    # ===== Lane headers =====
    lane_labels = [
        "Lane 1: Scalar",
        "Lane 2: Probabilistic",
        "Lane 3: Possibilistic",
    ]
    for i, (lx, label) in enumerate(zip(lane_x, lane_labels), 1):
        _box(ax, lx, 4.85, 2.8, 0.55, label,
             LANE_COLOURS[i], fontsize=9, fontweight="bold")

    # ===== Processing steps =====
    # Lane 1: extract point forecast -> scalar metrics
    _box(ax, 1.8, 3.9, 2.5, 0.50,
         r"Extract $N_c$ (point est.)",
         LANE_COLOURS[1], alpha=0.75, fontsize=8)
    _arrow(ax, 1.8, 4.55, 1.8, 4.18)

    _box(ax, 1.8, 3.0, 2.5, 0.50,
         "RMSE, Bias, MAE",
         LANE_COLOURS[1], alpha=0.75, fontsize=8)
    _arrow(ax, 1.8, 3.62, 1.8, 3.28)

    # Lane 2: bridge -> IG
    _box(ax, 5.0, 3.9, 2.5, 0.50,
         "Pignistic bridge\n" + r"$\pi \rightarrow p$",
         LANE_COLOURS[2], alpha=0.75, fontsize=8)
    _arrow(ax, 5.0, 4.55, 5.0, 4.18)

    _box(ax, 5.0, 3.0, 2.5, 0.50,
         "IG = DSC - REL",
         LANE_COLOURS[2], alpha=0.75, fontsize=8)
    _arrow(ax, 5.0, 3.62, 5.0, 3.28)

    # Lane 3: native scorecard
    _box(ax, 8.2, 3.9, 2.5, 0.50,
         "Native distribution\n" + r"$\pi(\omega)$ directly",
         LANE_COLOURS[3], alpha=0.85, fontsize=8)
    _arrow(ax, 8.2, 4.55, 8.2, 4.18)

    _box(ax, 8.2, 3.0, 2.5, 0.50,
         r"$\alpha^*, \eta, \delta, H_\Pi, N_c^*$",
         LANE_COLOURS[3], alpha=0.85, fontsize=8)
    _arrow(ax, 8.2, 3.62, 8.2, 3.28)

    # ===== Observation box =====
    _box(ax, 5.0, 1.6, 3.8, 0.60,
         "Observation  " + r"$c_{\mathrm{obs}}$",
         GREEN, fontsize=10, fontweight="bold")
    # Arrows from observation to each lane's metric box
    for lx in lane_x:
        _arrow(ax, lx, 2.72, lx, 1.95,
               connectionstyle="arc3,rad=0.0",
               arrowstyle="<|-", color=GREEN, linewidth=0.8)

    # ===== Footer: convergence arrows into a combined assessment =====
    _box(ax, 5.0, 0.55, 5.0, 0.50,
         "Comprehensive Forecast Assessment",
         DARK_GREY, fontsize=9, fontweight="bold")
    for lx in lane_x:
        _arrow(ax, lx, 1.27, 5.0 + (lx - 5.0) * 0.3, 0.83,
               connectionstyle="arc3,rad=0.0")

    fig.tight_layout()
    save_fig(fig, "fig8_verification_lanes")


if __name__ == "__main__":
    main()
