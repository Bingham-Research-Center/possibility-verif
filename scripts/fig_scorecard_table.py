"""Figure 10: Verification scorecard with triangle indicators.

Shows improvement/degradation of a possibilistic forecast system across
model versions, relative to a baseline (v1.0).  Metrics span three
verification lanes: native possibilistic, probabilistic, and deterministic.

Convention (following ECMWF/WMO scorecard style):
  Filled up-triangle (green)    statistically significant improvement
  Open  up-triangle (green)     improvement, not significant
  Filled down-triangle (red)    statistically significant degradation
  Open  down-triangle (red)     degradation, not significant
  Marker size encodes magnitude of change.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from style import apply_style, save_fig, PURPLE, DARK_GREY, MID_GREY, LIGHT_GREY

# Colours for improvement / degradation
IMPROVE = "#2E7D32"
DEGRADE = "#C62828"
HEADER_BG = "#E8E0F0"   # light purple for lane header bands


def main():
    apply_style()

    # ------------------------------------------------------------------ #
    # Data                                                                #
    # ------------------------------------------------------------------ #
    # Metrics grouped by verification lane.
    # Each metric: (symbol, plain name, [(dir, sig, mag) x 3 versions])
    #   dir: +1 = improvement, -1 = degradation
    #   sig: True = statistically significant
    #   mag: 0-1, controls marker size
    #
    # Story: v2 mixed (better shape but more ignorant);
    #        v3 strong broad upgrade;
    #        v4 further gains but REL degrades (sharper at cost of calibration).
    lane_data = [
        ("Native possibilistic", [
            (r"$\overline{\alpha^*}$",  "Depth-of-truth",
                [(+1, True,  0.30), (+1, True,  0.60), (+1, True,  0.80)]),
            (r"$\overline{\eta}$",      "Nonspecificity",
                [(+1, False, 0.15), (+1, True,  0.45), (+1, True,  0.60)]),
            (r"$\overline{\delta}$",    "Resolution gap",
                [(+1, True,  0.35), (+1, True,  0.70), (+1, True,  0.90)]),
            (r"$\overline{H_\Pi}$",     "Ignorance",
                [(-1, True,  0.50), (+1, True,  0.30), (+1, True,  0.50)]),
            (r"$\overline{N_c^*}$",     "Cond. necessity",
                [(+1, False, 0.20), (+1, True,  0.55), (+1, True,  0.75)]),
        ]),
        ("Probabilistic", [
            ("IG",                       "Information gain",
                [(+1, True,  0.40), (+1, True,  0.65), (+1, True,  0.85)]),
            ("REL",                      "Reliability",
                [(+1, False, 0.20), (+1, True,  0.50), (-1, False, 0.20)]),
            ("DSC",                      "Discrimination",
                [(+1, True,  0.45), (+1, True,  0.70), (+1, True,  0.90)]),
            (r"$P($organised$)$",       "Exceedance skill",
                [(+1, False, 0.25), (+1, True,  0.50), (+1, True,  0.65)]),
        ]),
        ("Deterministic", [
            ("RMSE",                     "Root-mean-square err.",
                [(+1, False, 0.25), (+1, True,  0.50), (+1, True,  0.70)]),
            ("Bias",                     "Mean error",
                [(-1, False, 0.15), (+1, False, 0.10), (+1, False, 0.05)]),
        ]),
    ]

    versions = ["v2.0", "v3.0", "v4.0"]
    n_ver = len(versions)

    # ------------------------------------------------------------------ #
    # Build display rows: interleave lane headers with metric rows        #
    # ------------------------------------------------------------------ #
    # row_type: 'header' | 'metric'
    rows = []   # list of (type, payload)
    for lane_name, metrics in lane_data:
        rows.append(("header", lane_name, None))
        for sym, name, cells in metrics:
            rows.append(("metric", f"{sym}  {name}", cells))

    n_rows = len(rows)  # 3 headers + 11 metrics = 14

    # ------------------------------------------------------------------ #
    # Figure                                                              #
    # ------------------------------------------------------------------ #
    min_s, max_s = 55, 280   # marker size range

    fig, ax = plt.subplots(figsize=(7.0, 6.0))

    # y-axis: row 0 at top, extra padding at bottom for legend clearance
    ax.set_ylim(n_rows + 0.3, -0.5)
    ax.set_xlim(-0.5, n_ver - 0.5)

    ytrans = ax.get_yaxis_transform()  # (axes_fraction_x, data_y)

    metric_counter = 0   # for alternating shading

    for r, (rtype, label, cells) in enumerate(rows):
        if rtype == "header":
            # Coloured band spanning the full width
            ax.axhspan(r - 0.5, r + 0.5, color=HEADER_BG, zorder=0)
            ax.axhline(r - 0.5, color=DARK_GREY, linewidth=0.8, zorder=2)
            # Centred lane label
            mid_x = (n_ver - 1) / 2.0
            ax.text(mid_x, r, label, ha="center", va="center",
                    fontsize=8.5, fontweight="bold", fontstyle="italic",
                    color=DARK_GREY, zorder=4)
        else:
            # Alternating row shading (count only metric rows)
            if metric_counter % 2 == 0:
                ax.axhspan(r - 0.5, r + 0.5, color="#F7F7F7", zorder=0)
            metric_counter += 1

            # Row label (axes-fraction x, data y)
            ax.text(-0.02, r, label, transform=ytrans,
                    ha="right", va="center", fontsize=8, color=DARK_GREY)

            # Triangle markers
            for j in range(n_ver):
                direction, sig, mag = cells[j]
                color = IMPROVE if direction > 0 else DEGRADE
                marker = "^" if direction > 0 else "v"
                s = min_s + (max_s - min_s) * mag

                if sig:
                    ax.scatter(j, r, marker=marker, s=s,
                               color=color, edgecolors="none", zorder=3)
                else:
                    ax.scatter(j, r, marker=marker, s=s,
                               facecolors="none", edgecolors=color,
                               linewidths=1.4, zorder=3)

    # Bottom border
    ax.axhline(n_rows - 0.5, color=DARK_GREY, linewidth=0.8, zorder=2)

    # Column headers
    for j, ver in enumerate(versions):
        ax.text(j, -0.75, ver, ha="center", va="bottom",
                fontsize=10, fontweight="bold", color=DARK_GREY)

    # Clean axes
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)

    # ------------------------------------------------------------------ #
    # Legend                                                              #
    # ------------------------------------------------------------------ #
    leg_handles = [
        mlines.Line2D([], [], marker="^", color=IMPROVE, linestyle="None",
                       markersize=8, label="Sig. improvement"),
        mlines.Line2D([], [], marker="^", markerfacecolor="none",
                       markeredgecolor=IMPROVE, linestyle="None",
                       markersize=8, markeredgewidth=1.4,
                       label="Non-sig. improvement"),
        mlines.Line2D([], [], marker="v", color=DEGRADE, linestyle="None",
                       markersize=8, label="Sig. degradation"),
        mlines.Line2D([], [], marker="v", markerfacecolor="none",
                       markeredgecolor=DEGRADE, linestyle="None",
                       markersize=8, markeredgewidth=1.4,
                       label="Non-sig. degradation"),
    ]
    ax.legend(handles=leg_handles, loc="lower center",
              bbox_to_anchor=(0.5, -0.02), ncol=4, fontsize=7,
              frameon=True, fancybox=False, edgecolor=MID_GREY,
              handletextpad=0.3, columnspacing=1.0)

    fig.tight_layout(rect=[0.28, 0.09, 1.0, 0.97])
    save_fig(fig, "scorecard_table")


if __name__ == "__main__":
    main()
