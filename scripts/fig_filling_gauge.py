"""Figure 3: Filling the gauge.

Horizontal convective-mode gauge bars whose fill level equals the
possibility value.  Uses the sharp-correct scenario; the observed
category (SUPER) is filled in green, others in purple.  A vertical
dashed line marks Pi_max and the gap to 1.0 is labelled H_Pi.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    CONV_MODES, CONV_N,
)


def main():
    apply_style()

    # Sharp-correct scenario
    pi = np.array([0.00, 0.05, 0.85, 0.10, 0.05])
    obs = "SUPER"
    obs_idx = CONV_MODES.index(obs)
    pi_max = pi.max()
    h_pi = 1.0 - pi_max

    fig, ax = plt.subplots(figsize=(6.5, 4.0))

    bar_height = 0.55
    y_positions = np.arange(CONV_N)

    for i in range(CONV_N):
        fill_colour = GREEN if i == obs_idx else PURPLE

        # Background track (empty gauge)
        ax.barh(y_positions[i], 1.0, height=bar_height,
                color="#E0E0E0", edgecolor=MID_GREY, linewidth=0.6, zorder=1)
        # Filled portion
        ax.barh(y_positions[i], pi[i], height=bar_height,
                color=fill_colour, edgecolor="white", linewidth=0.6, zorder=2)

        # Value label at the end of the fill
        label_x = pi[i] + 0.02
        ax.text(label_x, y_positions[i], f"{pi[i]:.2f}",
                va="center", ha="left", fontsize=8, color=DARK_GREY, zorder=3)

    # Vertical dashed line at Pi_max
    ax.axvline(pi_max, linestyle="--", linewidth=1.0, color=DARK_GREY, zorder=4)
    ax.text(pi_max, CONV_N - 0.5,
            r"$\Pi_{\max}$" + f" = {pi_max:.2f}",
            ha="right", va="bottom", fontsize=9, color=DARK_GREY)

    # Bracket / label for H_Pi gap
    bracket_y = CONV_N - 0.7
    ax.annotate(
        "", xy=(1.0, bracket_y), xytext=(pi_max, bracket_y),
        arrowprops=dict(arrowstyle="<->", color=DARK_GREY, lw=1.0),
    )
    ax.text((pi_max + 1.0) / 2.0, bracket_y + 0.18,
            r"$H_\Pi$" + f" = {h_pi:.2f}",
            ha="center", va="bottom", fontsize=9, color=DARK_GREY)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(CONV_MODES)
    ax.set_xlabel(r"Possibility $\pi(\omega)$")
    ax.set_xlim(0, 1.12)
    ax.set_ylim(-0.5, CONV_N - 0.2)

    # Vertical reference line at 1.0
    ax.axvline(1.0, linestyle=":", linewidth=0.6, color=MID_GREY, zorder=1)

    # Legend
    legend_elements = [
        mpatches.Patch(facecolor=GREEN, edgecolor="white", label="Observed (SUPER)"),
        mpatches.Patch(facecolor=PURPLE, edgecolor="white", label="Other categories"),
    ]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=8,
              frameon=True, fancybox=False, edgecolor=MID_GREY)

    fig.tight_layout()
    save_fig(fig, "filling_gauge")


if __name__ == "__main__":
    main()
