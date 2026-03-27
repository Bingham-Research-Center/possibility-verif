"""Categorical-lane verification figure (two-panel).

Left panel:  Threshold performance curve — POD, success ratio (1-FAR),
             and CSI at each severity threshold (MRGL+ through HIGH).
Right panel: K×K confusion matrix — forecast mode vs observed category.

Uses the same 3-year synthetic reforecast as the hexbin/commitment diagrams.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm, LinearSegmentedColormap

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)
from fig_three_scenario import SCENARIOS
from fig_performance_diagram import generate_reforecast


# ------------------------------------------------------------------ #
# Categorical scoring utilities                                       #
# ------------------------------------------------------------------ #

def categorical_scores(pi_array, obs_idx):
    """Compute mode-based categorical verification scores.

    Parameters
    ----------
    pi_array : ndarray, shape (n, K)
    obs_idx  : ndarray, shape (n,), integer category indices

    Returns
    -------
    dict with keys: modes, conf_matrix, threshold_scores, hss
    """
    n = len(obs_idx)
    K = pi_array.shape[1]

    # Mode = argmax(pi); ties broken by severity (higher category wins)
    modes = np.array([
        int(np.max(np.where(pi_array[i] == pi_array[i].max())))
        for i in range(n)
    ])

    # Full K×K confusion matrix (rows = forecast, cols = observed)
    conf = np.zeros((K, K), dtype=int)
    for i in range(n):
        conf[modes[i], obs_idx[i]] += 1

    # Threshold-based binary scores
    threshold_scores = {}
    for t in range(1, K):  # MRGL+ through HIGH
        fc_yes = modes >= t
        ob_yes = obs_idx >= t
        hits = int((fc_yes & ob_yes).sum())
        misses = int((~fc_yes & ob_yes).sum())
        fa = int((fc_yes & ~ob_yes).sum())

        pod = hits / (hits + misses) if (hits + misses) > 0 else 0.0
        far = fa / (hits + fa) if (hits + fa) > 0 else 0.0
        sr = 1.0 - far
        csi = hits / (hits + misses + fa) if (hits + misses + fa) > 0 else 0.0
        threshold_scores[t] = dict(pod=pod, far=far, sr=sr, csi=csi)

    # Heidke Skill Score from full K×K table
    n_total = conf.sum()
    correct = np.trace(conf)
    expected = sum(
        conf[k, :].sum() * conf[:, k].sum() for k in range(K)
    ) / n_total
    hss = (correct - expected) / (n_total - expected) if (n_total - expected) > 0 else 0.0

    return dict(modes=modes, conf_matrix=conf,
                threshold_scores=threshold_scores, hss=hss)


# ------------------------------------------------------------------ #
# Figure                                                              #
# ------------------------------------------------------------------ #

def main():
    apply_style()

    # --- Data ---
    data = generate_reforecast(n_years=3)
    pi_array = data['pi_array']
    obs_idx = data['obs_idx']
    cs = categorical_scores(pi_array, obs_idx)

    # --- Three-scenario modes ---
    scenario_modes = {}
    for name, sc in SCENARIOS.items():
        pi = sc['pi']
        mode_idx = int(np.max(np.where(pi == pi.max())))
        obs = SPC_CATEGORIES.index(sc['obs'])
        scenario_modes[name] = dict(mode=mode_idx, obs=obs,
                                    correct=(mode_idx == obs))

    fig, (ax_perf, ax_conf) = plt.subplots(
        1, 2, figsize=(11.0, 4.5),
        gridspec_kw={"width_ratios": [1.15, 1]},
    )

    # ================================================================ #
    # LEFT PANEL: Threshold performance curve                          #
    # ================================================================ #
    thresholds = list(range(1, SPC_N))
    t_labels = [f"{SPC_CATEGORIES[t]}+" for t in thresholds]
    x_pos = np.arange(len(thresholds))

    pods = [cs['threshold_scores'][t]['pod'] for t in thresholds]
    srs = [cs['threshold_scores'][t]['sr'] for t in thresholds]
    csis = [cs['threshold_scores'][t]['csi'] for t in thresholds]

    lw = 2.0
    ms = 7

    ax_perf.plot(x_pos, pods, color=PURPLE, linewidth=lw, marker="o",
                 markersize=ms, zorder=4, label="POD", clip_on=False)
    ax_perf.plot(x_pos, srs, color=GREEN, linewidth=lw, marker="s",
                 markersize=ms, zorder=4, label="1 − FAR (success ratio)",
                 clip_on=False)
    ax_perf.plot(x_pos, csis, color=DARK_GREY, linewidth=lw, marker="D",
                 markersize=ms-1, linestyle="--", zorder=4, label="CSI",
                 alpha=0.7, clip_on=False)

    # HSS annotation
    ax_perf.text(
        0.97, 0.03,
        f"HSS = {cs['hss']:.3f}",
        transform=ax_perf.transAxes, ha="right", va="bottom",
        fontsize=9, fontweight="bold", color=DARK_GREY,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                  edgecolor=MID_GREY, linewidth=0.6),
    )

    # Scenario annotations
    # Scenario A: mode=MDT, obs=MDT → correct; relevant at MDT+ threshold
    # Scenario B: mode=ENH, obs=ENH → correct; relevant at ENH+ threshold
    # Scenario C: mode=NONE, obs=MDT → wrong; fails at all thresholds
    annot_kw = dict(fontsize=7.5, fontweight="bold", zorder=6,
                    arrowprops=dict(arrowstyle="->", lw=0.8))

    # A: at MDT+ threshold (index 3), POD=1 for this case
    ax_perf.annotate(
        "A", xy=(3, pods[3]), xytext=(3 + 0.35, pods[3] + 0.04),
        color=GREEN, **annot_kw,
    )
    # B: at ENH+ threshold (index 2), POD=1 for this case
    ax_perf.annotate(
        "B", xy=(2, pods[2]), xytext=(2 + 0.35, pods[2] + 0.04),
        color=GREEN, **annot_kw,
    )
    # C: fails everywhere — annotate below the x-axis
    ax_perf.scatter([0], [-0.02], s=80, color="#C0392B", marker="x",
                    linewidths=2.2, zorder=5, clip_on=False)
    ax_perf.annotate(
        "C: mode = NONE\n(misses all thresholds)",
        xy=(0, -0.02), xytext=(1.6, 0.14),
        color="#C0392B", fontsize=7, fontweight="bold", zorder=6,
        arrowprops=dict(arrowstyle="->", color="#C0392B", lw=0.8),
    )

    ax_perf.set_xticks(x_pos)
    ax_perf.set_xticklabels(t_labels, fontsize=9)
    ax_perf.set_xlabel("Severity threshold", fontsize=10)
    ax_perf.set_ylabel("Score", fontsize=10)
    ax_perf.set_ylim(-0.05, 1.05)
    ax_perf.set_xlim(-0.3, len(thresholds) - 0.7)
    ax_perf.legend(loc="lower left", fontsize=8, frameon=True,
                   fancybox=False, edgecolor=MID_GREY)
    ax_perf.set_title("(a)  Threshold performance", fontsize=10,
                      fontweight="bold", pad=8)

    # ================================================================ #
    # RIGHT PANEL: Confusion matrix                                    #
    # ================================================================ #
    conf = cs['conf_matrix']

    # Purple colormap: white → light purple → deep purple
    cmap_conf = LinearSegmentedColormap.from_list("conf", [
        "#FFFFFF", "#E1BEE7", "#CE93D8", PURPLE, "#4A0072",
    ], N=256)

    # Log-ish normalisation so rare cells are still visible
    # Use a pseudo-log: plot log10(count+1) then label with raw counts
    conf_plot = np.log10(conf.astype(float) + 1)
    vmax = conf_plot.max()

    im = ax_conf.imshow(conf_plot, cmap=cmap_conf, aspect="equal",
                        vmin=0, vmax=vmax, origin="upper")

    # Annotations: raw counts in each cell
    for r in range(SPC_N):
        for c in range(SPC_N):
            val = conf[r, c]
            if val == 0:
                txt = "\u2013"  # en-dash for zero
                ax_conf.text(c, r, txt, ha="center", va="center",
                             fontsize=7, color=MID_GREY, alpha=0.5)
                continue
            # White text on dark cells, dark text on light cells
            brightness = conf_plot[r, c] / vmax if vmax > 0 else 0
            txt_color = "white" if brightness > 0.5 else DARK_GREY
            fontw = "bold" if r == c else "normal"
            ax_conf.text(c, r, str(val), ha="center", va="center",
                         fontsize=8, fontweight=fontw, color=txt_color)

    # ±1 off-diagonal shading (near-miss cells)
    for r in range(SPC_N):
        for c in range(SPC_N):
            if r != c and abs(r - c) == 1:
                ax_conf.add_patch(plt.Rectangle(
                    (c - 0.5, r - 0.5), 1, 1, fill=True,
                    facecolor=PURPLE, alpha=0.06, edgecolor="none",
                    zorder=1,
                ))

    # Diagonal highlight
    for k in range(SPC_N):
        ax_conf.add_patch(plt.Rectangle(
            (k - 0.5, k - 0.5), 1, 1, fill=False,
            edgecolor=GREEN, linewidth=2.0, zorder=3,
        ))

    ax_conf.set_xticks(range(SPC_N))
    ax_conf.set_xticklabels(SPC_CATEGORIES, fontsize=8)
    ax_conf.set_yticks(range(SPC_N))
    ax_conf.set_yticklabels(SPC_CATEGORIES, fontsize=8)
    ax_conf.set_xlabel("Observed category", fontsize=10)
    ax_conf.set_ylabel("Forecast mode", fontsize=10)
    ax_conf.set_title("(b)  Confusion matrix", fontsize=10,
                      fontweight="bold", pad=8)

    # Colorbar inset (top-left of panel b)
    cax = ax_conf.inset_axes([0.60, 0.82, 0.35, 0.06])
    cbar = fig.colorbar(im, cax=cax, orientation="horizontal")
    cbar.set_ticks([0, np.log10(11), np.log10(101), vmax])
    cbar.set_ticklabels(["0", "10", "100", str(int(conf.max()))])
    cbar.ax.tick_params(labelsize=6)
    cbar.set_label("Count", fontsize=7, labelpad=1)

    # Near-miss computation
    incorrect = conf.sum() - np.trace(conf)
    near_miss = sum(conf[r, c] for r in range(SPC_N) for c in range(SPC_N)
                    if r != c and abs(r - c) == 1)
    near_pct = near_miss / incorrect if incorrect > 0 else 0

    # Mode accuracy + near-miss annotation
    accuracy = np.trace(conf) / conf.sum()
    ax_conf.text(
        0.97, 0.03,
        f"Mode accuracy = {accuracy:.1%}\n"
        + r"$\pm$1 cat errors = " + f"{near_pct:.0%} of misses",
        transform=ax_conf.transAxes, ha="right", va="bottom",
        fontsize=8, fontweight="bold", color=DARK_GREY,
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                  edgecolor=MID_GREY, linewidth=0.6),
    )

    # Legend note
    ax_conf.text(
        0.03, 0.97, "Green = correct\nShading = near miss (±1 cat)",
        transform=ax_conf.transAxes, ha="left", va="top",
        fontsize=6.5, fontstyle="italic", color=DARK_GREY,
    )

    fig.tight_layout(w_pad=3.0)
    save_fig(fig, "categorical_scores")


if __name__ == "__main__":
    main()
