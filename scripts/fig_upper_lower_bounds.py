"""Figure 5: Upper / lower probability bounds.

For each of the three scenarios, shows the interval [L, U] on a [0, 1]
number line for the threshold event A_T = {ENH, MDT, HIGH}.
L and U are derived from the possibility distribution via the
tripartite bridge.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)


# Three scenarios (same as fig_three_scenario)
SCENARIOS = {
    "Sharp-Correct": np.array([0.00, 0.05, 0.10, 0.15, 0.90, 0.05]),
    "Hedged-Correct": np.array([0.10, 0.30, 0.45, 0.50, 0.55, 0.10]),
    "Sharp-Wrong":    np.array([0.85, 0.10, 0.05, 0.02, 0.01, 0.00]),
}

# Threshold event: categories at ENH or higher
EVENT_CATS = {"ENH", "MDT", "HIGH"}


def bounds_from_possibility(pi, event_indices):
    """Compute [L, U] bounds for threshold event A_T.

    Using the tripartite bridge:
      - pi_max = max(pi);  H_Pi = 1 - pi_max;  S = sum(pi)
      - p_i = pi_i * pi_max / S   for each i
      - p_ign = H_Pi

    Then:
      L = sum of p_i for i in A_T   (lower bound: ignorance counts against)
      U = L + p_ign                   (upper bound: ignorance could all belong to A_T)

    Returns (L, U).
    """
    pi = np.asarray(pi, dtype=float)
    pi_max = pi.max()
    h_pi = 1.0 - pi_max
    S = pi.sum()
    p_cats = pi * pi_max / S

    L = p_cats[event_indices].sum()
    U = L + h_pi
    return float(L), float(U)


def main():
    apply_style()

    event_idx = np.array([SPC_CATEGORIES.index(c) for c in EVENT_CATS])

    labels = list(SCENARIOS.keys())
    n = len(labels)

    fig, ax = plt.subplots(figsize=(7.0, 3.0))

    y_positions = np.arange(n)[::-1]  # top-to-bottom

    for i, (label, pi) in enumerate(SCENARIOS.items()):
        y = y_positions[i]
        L, U = bounds_from_possibility(pi, event_idx)

        # Full [0, 1] track
        ax.plot([0, 1], [y, y], color="#D0D0D0", linewidth=6, solid_capstyle="round",
                zorder=1)

        # Shaded [L, U] interval
        ax.plot([L, U], [y, y], color=PURPLE, linewidth=6, solid_capstyle="round",
                zorder=2, alpha=0.85)

        # End markers
        ax.plot(L, y, "o", color=PURPLE, markersize=7, zorder=3)
        ax.plot(U, y, "o", color=PURPLE, markersize=7, zorder=3)

        # Numeric labels
        ax.text(L, y + 0.25, f"L={L:.3f}", ha="center", va="bottom",
                fontsize=8, color=DARK_GREY)
        ax.text(U, y + 0.25, f"U={U:.3f}", ha="center", va="bottom",
                fontsize=8, color=DARK_GREY)

    ax.set_yticks(y_positions)
    ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("Probability of event " +
                  r"$A_T = \{$ENH, MDT, HIGH$\}$", fontsize=9)
    ax.set_xlim(-0.05, 1.08)
    ax.set_ylim(-0.6, n - 0.3)

    # Reference lines
    ax.axvline(0, linestyle=":", linewidth=0.5, color=MID_GREY)
    ax.axvline(1, linestyle=":", linewidth=0.5, color=MID_GREY)

    fig.tight_layout()
    save_fig(fig, "fig5_upper_lower_bounds")


if __name__ == "__main__":
    main()
