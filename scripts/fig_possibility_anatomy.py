"""Figure 1 (PDF order): Possibility distribution anatomy.

Shows a subnormal bar chart over the five SPC convective outlook categories,
annotating the key structural features: Pi_max, the hesitancy gap H_Pi,
and the peak (nominal) category N_c.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)


def main():
    apply_style()

    # Subnormal possibility distribution
    pi = np.array([0.05, 0.00, 0.10, 0.20, 0.75, 0.15])
    pi_max = pi.max()
    peak_idx = int(np.argmax(pi))
    h_pi = 1.0 - pi_max

    x = np.arange(SPC_N)
    bar_width = 0.55

    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    bars = ax.bar(x, pi, width=bar_width, color=PURPLE, edgecolor="white",
                  linewidth=0.8, zorder=3)

    # --- Annotation: Pi_max dashed line ---
    ax.axhline(pi_max, linestyle="--", linewidth=1.0, color=DARK_GREY, zorder=2)
    ax.text(SPC_N - 0.5, pi_max - 0.03,
            r"$\Pi_{\max}$" + f" = {pi_max:.2f}" + "\n(peak plausibility)",
            ha="right", va="top", fontsize=9, color=DARK_GREY)

    # --- Annotation: H_Pi bracket on the right side ---
    bracket_x = SPC_N - 0.15
    # Vertical line segment from pi_max to 1.0
    ax.plot([bracket_x, bracket_x], [pi_max, 1.0],
            color=DARK_GREY, linewidth=1.0, zorder=4)
    # Top tick
    ax.plot([bracket_x - 0.08, bracket_x + 0.08], [1.0, 1.0],
            color=DARK_GREY, linewidth=1.0, zorder=4)
    # Bottom tick
    ax.plot([bracket_x - 0.08, bracket_x + 0.08], [pi_max, pi_max],
            color=DARK_GREY, linewidth=1.0, zorder=4)
    # Label
    mid_y = (pi_max + 1.0) / 2.0
    ax.text(bracket_x + 0.15, mid_y,
            r"$H_\Pi$" + f" = {h_pi:.2f}" + "\n(admitted ignorance)",
            ha="left", va="center", fontsize=9, color=DARK_GREY)

    # --- Annotation: N_c for the peak category ---
    ax.annotate(
        r"$N_c$" + f" = {SPC_CATEGORIES[peak_idx]}" + "\n(most certain category)",
        xy=(peak_idx, pi[peak_idx]),
        xytext=(peak_idx - 1.2, pi[peak_idx] + 0.22),
        fontsize=9, color=DARK_GREY,
        arrowprops=dict(arrowstyle="->", color=DARK_GREY, lw=1.0),
        ha="center", va="bottom",
    )

    # Axes
    ax.set_xticks(x)
    ax.set_xticklabels(SPC_CATEGORIES)
    ax.set_xlabel("SPC Category " + r"$\omega$")
    ax.set_ylabel(r"Possibility $\pi(\omega)$")
    ax.set_ylim(0, 1.18)
    ax.set_xlim(-0.5, SPC_N + 0.3)

    # Thin reference line at 1.0
    ax.axhline(1.0, linestyle=":", linewidth=0.6, color=MID_GREY, zorder=1)

    fig.tight_layout()
    save_fig(fig, "possibility_anatomy")


if __name__ == "__main__":
    main()
