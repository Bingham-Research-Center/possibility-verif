"""Figure 7 (PDF order): Three-lane verification summary schematic.

Flowchart-style diagram showing the three complementary verification lanes:
  Lane 1 — Categorical (POD, FAR, CSI, HSS) evaluates the mode-based forecast.
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
    1: "#B0BEC5",   # blue-grey (categorical)
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

    fig, ax = plt.subplots(figsize=(3.8, 7.0))
    ax.set_xlim(0, 3.8)
    ax.set_ylim(0, 7.0)
    ax.axis("off")

    cx = 1.9   # centre x
    bw = 3.2   # box width (wide boxes)
    bw_s = 2.6  # box width (processing/metric boxes)

    # ===== Top: forecast input =====
    _box(ax, cx, 6.60, bw, 0.55,
         "Possibilistic Forecast  " + r"$\pi(\omega)$",
         DARK_GREY, fontsize=8, fontweight="bold")

    # --- Lane 1: Categorical (blue-grey) ---
    y_hdr1 = 5.80
    _arrow(ax, cx, 6.30, cx, y_hdr1 + 0.22)
    _box(ax, cx, y_hdr1, bw, 0.40,
         "Lane 1: Categorical",
         LANE_COLOURS[1], fontsize=8, fontweight="bold")
    y_proc1 = 5.30
    _arrow(ax, cx, y_hdr1 - 0.22, cx, y_proc1 + 0.18)
    _box(ax, cx, y_proc1, bw_s, 0.32,
         r"Mode: $\hat{c} = \arg\max \pi$",
         LANE_COLOURS[1], alpha=0.75, fontsize=7)
    y_met1 = 4.88
    _arrow(ax, cx, y_proc1 - 0.18, cx, y_met1 + 0.15)
    _box(ax, cx, y_met1, bw_s, 0.28,
         "POD, FAR, CSI, HSS",
         LANE_COLOURS[1], alpha=0.75, fontsize=7)

    # --- Lane 2: Probabilistic (light blue) ---
    y_hdr2 = 4.30
    _arrow(ax, cx, y_met1 - 0.16, cx, y_hdr2 + 0.22)
    _box(ax, cx, y_hdr2, bw, 0.40,
         "Lane 2: Probabilistic",
         LANE_COLOURS[2], fontsize=8, fontweight="bold")
    y_proc2 = 3.80
    _arrow(ax, cx, y_hdr2 - 0.22, cx, y_proc2 + 0.18)
    _box(ax, cx, y_proc2, bw_s, 0.32,
         r"Bridge: $\pi \rightarrow p$",
         LANE_COLOURS[2], alpha=0.75, fontsize=7)
    y_met2 = 3.38
    _arrow(ax, cx, y_proc2 - 0.18, cx, y_met2 + 0.15)
    _box(ax, cx, y_met2, bw_s, 0.28,
         "IG = DSC " + r"$-$" + " REL",
         LANE_COLOURS[2], alpha=0.75, fontsize=7)

    # --- Lane 3: Possibilistic (purple, highlighted) ---
    y_hdr3 = 2.78
    _arrow(ax, cx, y_met2 - 0.16, cx, y_hdr3 + 0.22)
    _box(ax, cx, y_hdr3, bw, 0.40,
         "Lane 3: Possibilistic",
         LANE_COLOURS[3], fontsize=8, fontweight="bold")
    y_proc3 = 2.28
    _arrow(ax, cx, y_hdr3 - 0.22, cx, y_proc3 + 0.18)
    _box(ax, cx, y_proc3, bw_s, 0.32,
         r"Native $\pi(\omega)$ directly",
         LANE_COLOURS[3], alpha=0.85, fontsize=7)
    y_met3 = 1.86
    _arrow(ax, cx, y_proc3 - 0.18, cx, y_met3 + 0.15)
    _box(ax, cx, y_met3, bw_s, 0.28,
         r"$\alpha^*, \eta, \delta, H_\Pi, N_c^*$",
         LANE_COLOURS[3], alpha=0.85, fontsize=7)

    # ===== Observation box =====
    y_obs = 1.20
    _arrow(ax, cx, y_met3 - 0.16, cx, y_obs + 0.22,
           arrowstyle="<|-", color=GREEN, linewidth=0.8)
    _box(ax, cx, y_obs, bw, 0.40,
         "Observation  " + r"$c_{\mathrm{obs}}$",
         GREEN, fontsize=8, fontweight="bold")

    # ===== Assessment footer =====
    y_assess = 0.50
    _arrow(ax, cx, y_obs - 0.22, cx, y_assess + 0.20)
    _box(ax, cx, y_assess, bw, 0.38,
         "Comprehensive Assessment",
         DARK_GREY, fontsize=7.5, fontweight="bold")

    fig.tight_layout()
    save_fig(fig, "verification_lanes")


if __name__ == "__main__":
    main()
