"""Figure 7: Information Gain (IG) decomposition — stacked bars.

Five forecast scenarios with stacked bars decomposing Information Gain
into Discrimination (DSC) and Reliability (REL) components.

    IG = DSC - REL        (Eq. 6; higher is better)

Positive IG means the forecast beats climatology; negative IG means it
does worse.  DSC contributes positively (skill) while REL is a penalty
(subtracted).  Plausible synthetic values are used for illustration.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    CONV_N,
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
    # UNC is context only (same for all scenarios).
    UNC_val = np.log2(CONV_N)  # ~2.32 bits for K=5

    DSC = np.array([1.80, 1.10, -0.30, 0.20, 0.00])  # discrimination
    REL = np.array([0.05, 0.10, 0.45, 0.55, 0.00])   # reliability penalty

    IG = DSC - REL  # net information gain (higher is better)

    x = np.arange(n)
    bar_width = 0.50

    fig, ax = plt.subplots(figsize=(7.5, 4.5))

    # --- Stacking logic ---
    # DSC bars extend from 0: upward if positive, downward if negative.
    # REL bars always subtract (penalty), extending downward from the DSC top.
    #
    # For positive DSC: DSC bar [0, DSC], then REL bar [DSC-REL, DSC] going down.
    # For negative DSC: DSC bar [DSC, 0] going down, then REL bar [DSC-REL, DSC]
    #   going further down.
    # Net top of stack = DSC - REL = IG in both cases.

    # Component 1: DSC (purple, skill component)
    # bottom = min(0, DSC), height = |DSC|
    dsc_bottoms = np.minimum(0, DSC)
    bars_dsc = ax.bar(
        x, np.abs(DSC), width=bar_width, bottom=dsc_bottoms,
        color=PURPLE, edgecolor="white", linewidth=0.8,
        zorder=3, alpha=0.80,
        label=r"DSC (discrimination, $+$skill)",
    )

    # Component 2: REL (green, penalty — always extends downward from DSC top)
    # REL bar goes from DSC down to DSC - REL = IG.
    # bottom = DSC - REL, height = REL
    rel_bottoms = DSC - REL  # = IG
    bars_rel = ax.bar(
        x, REL, width=bar_width, bottom=rel_bottoms,
        color=GREEN, edgecolor="white", linewidth=0.8,
        zorder=3, alpha=0.80,
        label=r"REL (reliability, $-$penalty)",
    )

    # --- Baseline at IG = 0 (climatology performance) ---
    ax.axhline(0, linewidth=1.2, color=DARK_GREY, zorder=2)

    # --- UNC reference (context only) ---
    ax.axhline(UNC_val, linestyle="--", linewidth=0.8, color=MID_GREY, zorder=1)
    ax.text(
        n - 0.5, UNC_val + 0.05,
        f"UNC = $\\log_2 {CONV_N}$",
        ha="right", va="bottom", fontsize=8, color=MID_GREY,
    )

    # --- Annotate each bar with net IG ---
    for i in range(n):
        net = IG[i]
        # Place annotation above or below the stack
        if net >= 0:
            y_annot = net + 0.10
            va = "bottom"
        else:
            y_annot = net - 0.10
            va = "top"
        ax.text(
            x[i], y_annot,
            f"IG = {net:+.2f}",
            ha="center", va=va, fontsize=8, fontweight="bold",
            color=DARK_GREY,
        )

    # --- Axes ---
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=8)
    ax.set_ylabel("Information Gain (bits)", fontsize=10)

    y_lo = min(IG.min(), DSC.min()) - 0.4
    y_hi = max(IG.max(), DSC.max(), UNC_val) + 0.4
    ax.set_ylim(y_lo, y_hi)

    # Skill / no-skill region labels
    ax.text(
        -0.45, 0.15, "forecast beats\nclimatology",
        fontsize=7, color=MID_GREY, fontstyle="italic", va="bottom",
    )
    ax.text(
        -0.45, -0.15, "forecast worse\nthan climatology",
        fontsize=7, color=MID_GREY, fontstyle="italic", va="top",
    )

    ax.legend(
        loc="upper right", fontsize=8, frameon=True, fancybox=False,
        edgecolor=MID_GREY,
    )

    fig.tight_layout()
    save_fig(fig, "ig_decomposition")


if __name__ == "__main__":
    main()
