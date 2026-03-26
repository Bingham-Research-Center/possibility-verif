"""Figure 12: Severity--confidence matrix (adapted from UK Met Office NSWWS).

Shows how operational warning decisions implicitly navigate the two-dimensional
space that possibility theory formalizes.  Rows are SPC severity categories;
columns represent forecaster confidence mapped to subnormality (H_Pi).
Color intensity encodes the joint risk signal.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from style import (
    apply_style, save_fig, PURPLE, GREEN, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)


def main():
    apply_style()

    # ------------------------------------------------------------------
    # Axes
    # ------------------------------------------------------------------
    confidence_labels = ["Very low", "Low", "Medium", "High", "Very high"]
    ignorance_values  = [0.8, 0.6, 0.4, 0.2, 0.0]   # H_Pi for each column
    n_conf = len(confidence_labels)

    # Severity weight (higher category → higher impact)
    severity_weight = np.array([0.2, 0.4, 0.6, 0.8, 1.0])  # MRGL→HIGH

    # Confidence weight (higher confidence → stronger signal)
    confidence_weight = np.array([0.2, 0.4, 0.6, 0.8, 1.0])

    # Joint risk signal: product of severity and confidence
    risk = np.outer(severity_weight, confidence_weight)

    # ------------------------------------------------------------------
    # Colormap: pale (low risk) → deep purple (high risk)
    # ------------------------------------------------------------------
    cmap = LinearSegmentedColormap.from_list(
        "risk",
        ["#F3E5F5", "#CE93D8", PURPLE, "#4A0072"],
        N=256,
    )

    fig, ax = plt.subplots(figsize=(5.5, 3.5))

    im = ax.imshow(risk, cmap=cmap, aspect="auto", vmin=0, vmax=1,
                   origin="lower")

    # Annotate cells with action labels
    action_labels = {
        (0, 0): "Monitor",
        (0, 1): "Monitor",
        (0, 2): "Monitor",
        (0, 3): "Aware",
        (0, 4): "Aware",
        (1, 0): "Monitor",
        (1, 1): "Monitor",
        (1, 2): "Aware",
        (1, 3): "Aware",
        (1, 4): "Prepare",
        (2, 0): "Monitor",
        (2, 1): "Aware",
        (2, 2): "Prepare",
        (2, 3): "Prepare",
        (2, 4): "Act",
        (3, 0): "Aware",
        (3, 1): "Prepare",
        (3, 2): "Prepare",
        (3, 3): "Act",
        (3, 4): "Act",
        (4, 0): "Aware",
        (4, 1): "Prepare",
        (4, 2): "Act",
        (4, 3): "Act",
        (4, 4): "Act",
    }

    for (row, col), label in action_labels.items():
        text_color = "white" if risk[row, col] > 0.45 else DARK_GREY
        ax.text(col, row, label, ha="center", va="center",
                fontsize=8, fontweight="bold", color=text_color)

    # Axes
    ax.set_xticks(range(n_conf))
    ax.set_xticklabels(confidence_labels, fontsize=8)
    ax.set_yticks(range(SPC_N))
    ax.set_yticklabels(SPC_CATEGORIES, fontsize=9, fontfamily="monospace")

    ax.set_xlabel("Forecaster confidence  (low $\\longrightarrow$ high;  "
                  "$H_\\Pi$: high $\\longrightarrow$ low)", fontsize=9)
    ax.set_ylabel("Severity category", fontsize=9)

    # Ignorance annotation along top
    ax2 = ax.secondary_xaxis("top")
    ax2.set_xticks(range(n_conf))
    ax2.set_xticklabels([f"$H_\\Pi$={h:.1f}" for h in ignorance_values],
                        fontsize=7, color=MID_GREY)
    ax2.tick_params(length=0)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    cbar.set_label("Joint risk signal", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    ax.set_facecolor("white")
    fig.tight_layout()
    save_fig(fig, "fig12_severity_matrix")


if __name__ == "__main__":
    main()
