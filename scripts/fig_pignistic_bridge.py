"""Figure 4: Pignistic bridge walkthrough.

Left panel: raw possibility distribution (K=5 bars, convective modes).
Right panel: (K+1)-category probability distribution produced by the
tripartite possibilistic-to-probabilistic bridge, with an explicit
ignorance bar.  Arrows connect corresponding bars between panels.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    CONV_MODES, CONV_N,
)


def tripartite_bridge(pi):
    """Compute the tripartite possibilistic-to-probabilistic bridge.

    Steps:
        1. H_Pi = 1 - max(pi)           ignorance mass
        2. remaining = max(pi)           mass available for categories
        3. p_i = pi_i * remaining / sum(pi)   for each category
        4. p_ign = H_Pi                  ignorance outcome probability

    Returns
    -------
    p_cats : ndarray, shape (n,)   category probabilities
    p_ign  : float                 ignorance probability
    """
    pi = np.asarray(pi, dtype=float)
    pi_max = pi.max()
    h_pi = 1.0 - pi_max          # ignorance mass
    remaining = pi_max            # mass available for categories
    pi_sum = pi.sum()
    p_cats = pi * remaining / pi_sum
    p_ign = h_pi
    return p_cats, p_ign


def main():
    apply_style()

    pi = np.array([0.05, 0.15, 0.70, 0.40, 0.10])
    p_cats, p_ign = tripartite_bridge(pi)

    # Verify the probability sums to 1
    assert abs(p_cats.sum() + p_ign - 1.0) < 1e-12

    x_left = np.arange(CONV_N)
    x_right = np.arange(CONV_N + 1)

    bar_width = 0.50

    fig, (ax_l, ax_r) = plt.subplots(1, 2, figsize=(11.0, 4.5),
                                      gridspec_kw={"wspace": 0.40})

    # --- Left panel: raw possibility distribution ---
    ax_l.bar(x_left, pi, width=bar_width, color=PURPLE, edgecolor="white",
             linewidth=0.8, zorder=3)
    ax_l.set_xticks(x_left)
    ax_l.set_xticklabels(CONV_MODES, fontsize=8)
    ax_l.set_ylabel(r"Possibility $\pi(\omega)$")
    ax_l.set_title("Raw Possibility Distribution", fontsize=10,
                    fontweight="bold", pad=8)
    ax_l.set_ylim(0, 1.10)
    ax_l.axhline(1.0, linestyle=":", linewidth=0.6, color=MID_GREY, zorder=1)

    # --- Right panel: (n+1)-category probability distribution ---
    right_labels = list(CONV_MODES) + ["IGN"]
    right_vals = np.concatenate([p_cats, [p_ign]])
    right_colours = [PURPLE] * CONV_N + [MID_GREY]

    ax_r.bar(x_right, right_vals, width=bar_width, color=right_colours,
             edgecolor="white", linewidth=0.8, zorder=3)
    ax_r.set_xticks(x_right)
    ax_r.set_xticklabels(right_labels, fontsize=8)
    ax_r.set_ylabel("Probability")
    ax_r.set_title("Pignistic Probability (n+1 outcomes)", fontsize=10,
                    fontweight="bold", pad=8)
    ax_r.set_ylim(0, max(right_vals) * 1.35)
    ax_r.axhline(1.0, linestyle=":", linewidth=0.6, color=MID_GREY, zorder=1)

    # Value labels above bars
    for i, v in enumerate(right_vals):
        ax_r.text(i, v + 0.008, f"{v:.3f}", ha="center", va="bottom",
                  fontsize=7, color=DARK_GREY)

    # --- Arrows connecting corresponding bars ---
    # Use figure-level coordinates via ConnectionPatch
    from matplotlib.patches import ConnectionPatch
    for i in range(CONV_N):
        # Connect top of left bar to top of right bar
        con = ConnectionPatch(
            xyA=(x_left[i], pi[i]), coordsA=ax_l.transData,
            xyB=(x_right[i], p_cats[i]), coordsB=ax_r.transData,
            arrowstyle="->", color=MID_GREY, linewidth=0.8,
            connectionstyle="arc3,rad=0.12",
        )
        fig.add_artist(con)

    # Arrow from the H_Pi gap to the ignorance bar
    con_ign = ConnectionPatch(
        xyA=(x_left[int(np.argmax(pi))], pi.max()),
        coordsA=ax_l.transData,
        xyB=(CONV_N, p_ign), coordsB=ax_r.transData,
        arrowstyle="->", color=MID_GREY, linewidth=0.8,
        linestyle="--", connectionstyle="arc3,rad=0.25",
    )
    fig.add_artist(con_ign)

    # Annotate bridge equation
    fig.text(
        0.50, 0.02,
        r"$p_i = \pi_i \cdot \Pi_{\max}\,/\,\Sigma\pi$"
        "          "
        r"$p_{\mathrm{ign}} = H_\Pi = 1 - \Pi_{\max}$",
        ha="center", va="bottom", fontsize=9, color=DARK_GREY,
    )

    fig.subplots_adjust(left=0.08, right=0.96, bottom=0.12, top=0.92,
                        wspace=0.40)
    save_fig(fig, "pignistic_bridge")


if __name__ == "__main__":
    main()
