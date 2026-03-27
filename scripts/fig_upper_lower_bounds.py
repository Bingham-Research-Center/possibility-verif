"""Figure 5: Upper / lower probability bounds.

For each of the three scenarios, shows the interval [L, U] on a [0, 1]
number line for the threshold event A_T = {ENH, MDT, HIGH}.
L and U are the possibilistic bounds from Eqs 11-12:
  U = Pi(A_T) = max_{w in A_T} pi(w)
  L = m * N_c(A_T) = m * [1 - max_{w not in A_T} pi'(w)]
"""
import numpy as np
import matplotlib.pyplot as plt

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)
from fig_three_scenario import SCENARIOS


# Threshold event: categories at ENH or higher
EVENT_CATS = {"ENH", "MDT", "HIGH"}


def bounds_from_possibility(pi, event_indices):
    """Compute possibilistic [L, U] bounds for threshold event A_T.

    Implements Eqs 11-12:
      U = Pi(A_T) = max_{w in A_T} pi(w)
      L = pi_max * N_c(A_T) = pi_max * [1 - max_{w not in A_T} pi'(w)]

    where pi' = pi / pi_max is the shape-normalised distribution.

    Returns (L, U).
    """
    pi = np.asarray(pi, dtype=float)
    pi_max = pi.max()

    # Upper bound: possibility of the event
    U = pi[event_indices].max()

    # Lower bound: commitment * conditional necessity
    complement = np.ones(len(pi), dtype=bool)
    complement[event_indices] = False
    if complement.any():
        pi_prime = pi / pi_max
        max_complement = pi_prime[complement].max()
    else:
        max_complement = 0.0
    L = pi_max * (1.0 - max_complement)

    return float(L), float(U)


def main():
    apply_style()

    event_idx = np.array([SPC_CATEGORIES.index(c) for c in EVENT_CATS])

    labels = list(SCENARIOS.keys())
    n = len(labels)

    fig, ax = plt.subplots(figsize=(7.0, 3.0))

    y_positions = np.arange(n)[::-1]  # top-to-bottom

    for i, (label, scenario) in enumerate(SCENARIOS.items()):
        y = y_positions[i]
        L, U = bounds_from_possibility(scenario['pi'], event_idx)

        # Full [0, 1] track
        ax.plot([0, 1], [y, y], color="#D0D0D0", linewidth=6, solid_capstyle="round",
                zorder=1)

        # Shaded [L, U] interval
        ax.plot([L, U], [y, y], color=PURPLE, linewidth=6, solid_capstyle="round",
                zorder=2, alpha=0.85)

        # End markers
        ax.plot(L, y, "o", color=PURPLE, markersize=7, zorder=3)
        ax.plot(U, y, "o", color=PURPLE, markersize=7, zorder=3)

        # Numeric labels: stagger above/below when close, merge when degenerate
        if abs(U - L) < 0.01:
            ax.text(L, y + 0.25, f"L=U={L:.2f}", ha="center", va="bottom",
                    fontsize=8, color=DARK_GREY)
        elif (U - L) < 0.12:
            ax.text(L, y - 0.25, f"L={L:.3f}", ha="center", va="top",
                    fontsize=8, color=DARK_GREY)
            ax.text(U, y + 0.25, f"U={U:.3f}", ha="center", va="bottom",
                    fontsize=8, color=DARK_GREY)
        else:
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
    save_fig(fig, "upper_lower_bounds")


if __name__ == "__main__":
    main()
