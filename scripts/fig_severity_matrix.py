"""Figure 12 (PDF order): Severity--confidence matrix (adapted from UK Met Office NSWWS).

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
    severity_weight = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])  # NONE→HIGH

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

    fig, ax = plt.subplots(figsize=(5.5, 4.0))

    im = ax.imshow(risk, cmap=cmap, aspect="auto", vmin=0, vmax=1,
                   origin="lower")

    # Annotate cells with action labels
    action_labels = {
        (0, 0): "Monitor",
        (0, 1): "Monitor",
        (0, 2): "Monitor",
        (0, 3): "Monitor",
        (0, 4): "Monitor",
        (1, 0): "Monitor",
        (1, 1): "Monitor",
        (1, 2): "Monitor",
        (1, 3): "Aware",
        (1, 4): "Aware",
        (2, 0): "Monitor",
        (2, 1): "Monitor",
        (2, 2): "Aware",
        (2, 3): "Aware",
        (2, 4): "Prepare",
        (3, 0): "Monitor",
        (3, 1): "Aware",
        (3, 2): "Prepare",
        (3, 3): "Prepare",
        (3, 4): "Act",
        (4, 0): "Aware",
        (4, 1): "Prepare",
        (4, 2): "Prepare",
        (4, 3): "Act",
        (4, 4): "Act",
        (5, 0): "Aware",
        (5, 1): "Prepare",
        (5, 2): "Act",
        (5, 3): "Act",
        (5, 4): "Act",
    }

    for (row, col), label in action_labels.items():
        text_color = "white" if risk[row, col] > 0.45 else DARK_GREY
        ax.text(col, row, label, ha="center", va="center",
                fontsize=8, fontweight="bold", color=text_color)

    # --- Scenario overlays ---
    MISS_RED = "#C0392B"
    # A: MDT (row 4), H_Pi=0.10 → Very high confidence (col 4)
    # B: ENH (row 3), H_Pi=0.45 → Medium confidence (col 2)
    # C forecast: NONE (row 0), H_Pi=0.15 → High confidence (col 3)
    scenario_cells = [
        ("A", 4, 4, GREEN),      # MDT × Very high → Act (correct)
        ("B", 3, 2, GREEN),      # ENH × Medium → Prepare (correct)
        ("C", 0, 3, MISS_RED),   # NONE × High → Monitor (wrong)
    ]
    for ltr, row, col, color in scenario_cells:
        ax.add_patch(plt.Rectangle(
            (col - 0.45, row - 0.45), 0.9, 0.9, fill=False,
            edgecolor=color, linewidth=2.5, zorder=5,
        ))
        ax.text(col + 0.38, row + 0.38, ltr, fontsize=8,
                fontweight="bold", color=color, ha="right", va="top",
                zorder=6)

    # Dashed red arrow from C's forecast cell (NONE, High) to C's truth (MDT, High)
    ax.annotate("", xy=(3, 4), xytext=(3, 0.5),
                arrowprops=dict(arrowstyle="-|>", color=MISS_RED,
                                linewidth=1.5, linestyle="--"),
                zorder=5)
    ax.text(3.48, 2.0, "C miss", fontsize=7, fontstyle="italic",
            color=MISS_RED, ha="left", va="center", rotation=90)

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
    save_fig(fig, "severity_matrix")


if __name__ == "__main__":
    main()
