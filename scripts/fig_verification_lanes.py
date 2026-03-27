"""Figure 7 (PDF order): Three-lane verification summary schematic.

Horizontal parallel layout showing the three complementary verification lanes:
  Lane 1 — Categorical (POD, FAR, CSI, HSS) evaluates the mode-based forecast.
  Lane 2 — Probabilistic (IG via bridge) evaluates the converted probability.
  Lane 3 — Possibilistic (five-number scorecard) evaluates the native
            possibility distribution (the novel contribution).

Lane 3 is highlighted in purple; others use lighter colours.
"""
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, DARK_GREY, MID_GREY,
)

# Colours per lane
LANE_COLOURS = {
    1: "#B0BEC5",   # blue-grey (categorical)
    2: "#90CAF9",   # light blue (probabilistic)
    3: PURPLE,      # purple (possibilistic — novel)
}


def _box(ax, x, y, w, h, text, colour, text_colour="white",
         fontsize=9, fontweight="normal", alpha=1.0):
    """Draw a square box with centred text."""
    box = FancyBboxPatch(
        (x - w / 2, y - h / 2), w, h,
        boxstyle="square,pad=0.08",
        facecolor=colour, edgecolor=DARK_GREY,
        linewidth=0.8, alpha=alpha, zorder=3,
    )
    ax.add_patch(box)
    ax.text(x, y, text, ha="center", va="center",
            fontsize=fontsize, fontweight=fontweight,
            color=text_colour, zorder=4, linespacing=1.3)


def _arrow(ax, x0, y0, x1, y1, **kwargs):
    """Draw an arrow between two points."""
    defaults = dict(arrowstyle="-|>", color=DARK_GREY, linewidth=1.0,
                    connectionstyle="arc3,rad=0.0", zorder=2)
    defaults.update(kwargs)
    arrow = FancyArrowPatch((x0, y0), (x1, y1), **defaults)
    ax.add_patch(arrow)


def main():
    apply_style()

    fig, ax = plt.subplots(figsize=(7.5, 4.0))
    ax.set_xlim(0, 7.5)
    ax.set_ylim(0, 4.0)
    ax.axis("off")

    # Layout parameters
    col_w = 2.0     # column width
    col_gap = 0.25  # gap between columns
    total_w = 3 * col_w + 2 * col_gap
    x_start = (7.5 - total_w) / 2
    col_xs = [x_start + col_w / 2 + i * (col_w + col_gap) for i in range(3)]

    bw_top = total_w  # top/bottom shared box width
    bw_lane = col_w - 0.15

    # ===== Top: forecast input (spanning all columns) =====
    top_cx = 7.5 / 2
    _box(ax, top_cx, 3.60, bw_top, 0.42,
         r"Possibilistic Forecast  $\pi(\omega)$",
         DARK_GREY, fontsize=9.5, fontweight="bold")

    # Arrows from top to each lane header
    for cx in col_xs:
        _arrow(ax, cx, 3.36, cx, 3.02)

    # ===== Three parallel lanes =====
    lanes = [
        {
            "name": "Categorical\n(§6)",
            "colour": LANE_COLOURS[1],
            "process": r"Mode: $\hat{c} = \arg\max \pi$",
            "metrics": "POD, FAR,\nCSI, HSS",
        },
        {
            "name": "Probabilistic\n(§3)",
            "colour": LANE_COLOURS[2],
            "process": r"Bridge: $\pi \rightarrow p$" + "\n(§3.1)",
            "metrics": "IG = DSC\n" + r"$-$ REL  (§3.2)",
        },
        {
            "name": "Possibilistic\n(§4)",
            "colour": LANE_COLOURS[3],
            "process": r"Native $\pi(\omega)$" + "\ndirectly",
            "metrics": r"$\alpha^*, \eta, \delta,$" + "\n"
                       + r"$H_\Pi, N_c^*$  (§4.2)",
        },
    ]

    for cx, lane in zip(col_xs, lanes):
        # Header
        y_hdr = 2.82
        _box(ax, cx, y_hdr, bw_lane, 0.38,
             lane["name"], lane["colour"],
             fontsize=9, fontweight="bold")

        # Arrow to processing
        y_proc = 2.15
        _arrow(ax, cx, y_hdr - 0.22, cx, y_proc + 0.18)
        _box(ax, cx, y_proc, bw_lane, 0.32,
             lane["process"], lane["colour"],
             alpha=0.75, fontsize=8)

        # Arrow to metrics
        y_met = 1.50
        _arrow(ax, cx, y_proc - 0.18, cx, y_met + 0.18)
        _box(ax, cx, y_met, bw_lane, 0.32,
             lane["metrics"], lane["colour"],
             alpha=0.75, fontsize=8)

        # Arrow down to bottom
        _arrow(ax, cx, y_met - 0.18, cx, 0.92)

    # ===== Bottom: observation + assessment (spanning all columns) =====
    _box(ax, top_cx, 0.70, bw_top, 0.38,
         r"Observation  $c_{\mathrm{obs}}$  $\rightarrow$  Assessment",
         GREEN, fontsize=9, fontweight="bold")

    fig.tight_layout()
    save_fig(fig, "verification_lanes")


if __name__ == "__main__":
    main()
