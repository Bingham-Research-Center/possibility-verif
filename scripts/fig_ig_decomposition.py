"""Figure 3 (PDF order): Information Gain (IG) decomposition — overlay bars.

Five forecast archetypes with overlay bars decomposing Information Gain
into Discrimination (DSC) and Reliability (REL) components.

    IG = DSC - REL        (Eq. 6; higher is better)

Positive IG means the forecast beats climatology; negative IG means it
does worse.  DSC contributes positively (skill) while REL is a penalty
(subtracted).  Illustrative values are used; DSC and REL are
sample-aggregated quantities (not single-forecast properties).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_N,
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

    # Plausible illustrative values (bits).
    # UNC = H(clim), entropy of the SPC climatological baseline.
    from style import SPC_CLIM
    UNC_val = -np.sum(SPC_CLIM * np.log2(SPC_CLIM))  # ~1.71 bits

    # DSC >= 0 always (weighted sum of KL divergences).
    # Sharp Wrong: differentiates situations but is catastrophically
    # miscalibrated, so DSC is modest but REL is very large.
    DSC = np.array([1.80, 1.10, 0.35, 0.20, 0.00])   # discrimination
    REL = np.array([0.05, 0.10, 1.10, 0.55, 0.00])    # reliability penalty

    IG = DSC - REL  # net information gain (higher is better)

    x = np.arange(n)
    bar_width = 0.45

    fig, ax = plt.subplots(figsize=(4.0, 4.2))

    # --- Overlay logic ---
    # Purple DSC bar: full gross discrimination (0 to DSC).
    # Green REL overlay: from top of DSC downward by REL amount.
    #   When REL < DSC: green overlaps the top portion of purple.
    #   When REL > DSC: green eats through all purple and extends below 0.
    # Visible purple below green = net IG.

    # Component 1: DSC (purple, full skill potential)
    bars_dsc = ax.bar(
        x, DSC, width=bar_width, bottom=0,
        color=PURPLE, edgecolor=DARK_GREY, linewidth=0.8,
        zorder=3, alpha=1.0,
        label=r"DSC (discrimination, $+$skill)",
    )

    # Component 2: REL overlay (green, penalty eating into DSC from top)
    # Drawn from (DSC - REL) to DSC.  When REL > DSC, bottom goes below 0.
    rel_bottoms = DSC - REL  # = IG
    bars_rel = ax.bar(
        x, REL, width=bar_width, bottom=rel_bottoms,
        color=GREEN, edgecolor=DARK_GREY, linewidth=0.8,
        zorder=4, alpha=0.65,
        label=r"REL (calibration penalty, $-$)",
    )

    # --- Baseline at IG = 0 (climatology performance) ---
    ax.axhline(0, linewidth=1.2, color=DARK_GREY, zorder=5)

    # --- UNC reference (context only) ---
    ax.axhline(UNC_val, linestyle="--", linewidth=0.8, color=MID_GREY, zorder=1)
    ax.text(
        n - 0.5, UNC_val + 0.05,
        r"UNC = $H(\mathrm{clim})$",
        ha="right", va="bottom", fontsize=8, color=MID_GREY,
    )

    # --- IG marker line on each bar ---
    for i in range(n):
        if DSC[i] > 0 or REL[i] > 0:
            ax.plot(
                [x[i] - bar_width / 2 - 0.03, x[i] + bar_width / 2 + 0.03],
                [IG[i], IG[i]],
                color=DARK_GREY, linewidth=1.5, zorder=6,
            )

    # --- Annotate each bar with net IG ---
    for i in range(n):
        net = IG[i]
        if net >= 0:
            y_annot = max(DSC[i], 0) + 0.12
            va = "bottom"
        else:
            y_annot = net - 0.12
            va = "top"
        ax.text(
            x[i], y_annot,
            f"IG = {net:+.2f}",
            ha="center", va=va, fontsize=8, fontweight="bold",
            color=DARK_GREY,
        )

    # --- Axes ---
    ax.set_xticks(x)
    ax.set_xticklabels(scenarios, fontsize=9)
    ax.set_ylabel("Information Gain (bits)", fontsize=10)

    y_lo = min(IG.min(), 0) - 0.4
    y_hi = max(DSC.max(), UNC_val) + 0.4
    ax.set_ylim(y_lo, y_hi)

    # Skill / no-skill region labels
    ax.text(
        -0.45, 0.15, "forecast beats\nclimatology",
        fontsize=8, color=DARK_GREY, fontstyle="italic",
        fontweight="medium", va="bottom",
    )
    ax.text(
        -0.45, -0.15, "forecast worse\nthan climatology",
        fontsize=8, color=DARK_GREY, fontstyle="italic",
        fontweight="medium", va="top",
    )

    ax.legend(
        bbox_to_anchor=(0.5, 1.02), loc="lower center", ncol=2,
        fontsize=8, frameon=True, fancybox=False, edgecolor=MID_GREY,
    )

    fig.tight_layout()
    save_fig(fig, "ig_decomposition")


if __name__ == "__main__":
    main()
