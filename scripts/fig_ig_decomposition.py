"""Figure 7: Information Gain (IG) decomposition — stacked bars.

Five forecast scenarios with stacked bars decomposing the Ignorance
score into Uncertainty (UNC), Discrimination (DSC), and Reliability (REL).

    IG = UNC - DSC + REL

Plausible synthetic values are used for illustration.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
)


def main():
    apply_style()

    # Scenario labels
    scenarios = [
        "Sharp\nCorrect",
        "Hedged\nCorrect",
        "Sharp\nWrong",
        "Hedged\nWrong",
        "Climatology",
    ]
    n = len(scenarios)

    # Plausible synthetic values (bits).
    # IG = UNC - DSC + REL
    # Lower IG is better.  Negative DSC hurts, positive REL hurts.
    # UNC is the same for all (entropy of the verification sample).
    UNC = np.array([2.32, 2.32, 2.32, 2.32, 2.32])  # log2(5) ~ 2.32
    DSC = np.array([1.80, 1.10, -0.30, 0.20, 0.00])  # discrimination
    REL = np.array([0.05, 0.10, 0.45, 0.55, 0.00])   # reliability penalty

    IG = UNC - DSC + REL  # net ignorance

    x = np.arange(n)
    bar_width = 0.50

    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    # Stacked bars — bottom to top: UNC (grey), then DSC portion removed,
    # then REL added.  For visual clarity we plot three separate stacked
    # components with absolute values.

    # Component 1: UNC (always positive, base layer)
    bars_unc = ax.bar(x, UNC, width=bar_width, color="#D0D0D0",
                       edgecolor="white", linewidth=0.8, zorder=2,
                       label=r"UNC (uncertainty)")

    # Component 2: DSC (purple, shown as reduction below UNC top)
    # We plot |DSC| as the discriminative skill removed from UNC.
    # Positive DSC means skill; negative DSC means anti-skill.
    bars_dsc = ax.bar(x, np.abs(DSC), width=bar_width, bottom=0,
                       color=PURPLE, edgecolor="white", linewidth=0.8,
                       zorder=3, alpha=0.75,
                       label=r"DSC (discrimination)")

    # Component 3: REL (green, penalty added on top of remaining)
    bars_rel = ax.bar(x, REL, width=bar_width,
                       bottom=UNC - DSC,  # = IG - REL + REL_base... just UNC-DSC
                       color=GREEN, edgecolor="white", linewidth=0.8,
                       zorder=3, alpha=0.75,
                       label=r"REL (reliability penalty)")

    # Net IG annotation above each bar
    for i in range(n):
        net = IG[i]
        top = max(UNC[i], UNC[i] - DSC[i] + REL[i]) + 0.12
        ax.text(x[i], top, f"IG = {net:.2f}",
                ha="center", va="bottom", fontsize=8, fontweight="bold",
                color=DARK_GREY)

    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=8)
    ax.set_ylabel("Score (bits)", fontsize=10)
    ax.set_ylim(0, max(IG) + 0.6)
    ax.legend(loc="upper right", fontsize=8, frameon=True, fancybox=False,
              edgecolor=MID_GREY)

    # Horizontal reference at UNC = log2(5)
    ax.axhline(2.32, linestyle="--", linewidth=0.8, color=MID_GREY, zorder=1)
    ax.text(n - 0.5, 2.35, r"UNC = $\log_2 5$", ha="right", va="bottom",
            fontsize=8, color=MID_GREY)

    fig.tight_layout()
    save_fig(fig, "fig7_ig_decomposition")


if __name__ == "__main__":
    main()
