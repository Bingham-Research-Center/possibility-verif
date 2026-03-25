"""Figure 11: Possibilistic performance diagram (Roebber-style).

Plots all five scorecard metrics simultaneously for a set of synthetic
forecast--observation pairs.

Encoding:
  x-axis   1 - eta  (specificity / sharpness; higher is better)
  y-axis   alpha*   (depth-of-truth; higher is better)
  contours delta = alpha* - eta  (resolution gap; iso-lines are diagonals)
  colour   H_Pi     (ignorance; sequential colourmap)
  size     N_c*     (conditional necessity; larger = more dominant)

Inspired by Roebber (2009) performance diagrams, which encode POD,
success ratio, CSI, and bias in a single scatter plot.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import Normalize
from matplotlib import cm

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, DARK_GREY, MID_GREY, LIGHT_GREY,
    SPC_N,
)


# ---------------------------------------------------------------------- #
# Synthetic data generation                                               #
# ---------------------------------------------------------------------- #

def _generate_cases(n=300, K=SPC_N, seed=42):
    """Generate synthetic forecast--observation pairs and compute scorecards.

    Uses five generation pathways to populate the full alpha*--eta space:
      peaked_correct  (30 %)  obs = peak, varying spread   → alpha* = 1
      peaked_wrong    (15 %)  peak elsewhere, varying spread → alpha* ≈ 0
      near_miss       (20 %)  peak adjacent to obs, gentle  → alpha* ∈ [0.3, 0.9]
      plateau         (20 %)  broad Gaussian shape          → diverse alpha*
      random          (15 %)  uniform random pi values      → diverse alpha*

    Returns arrays: alpha_star, eta, delta, H_Pi, Nc_star (each length n).
    """
    rng = np.random.default_rng(seed)

    alpha_star = np.empty(n)
    eta        = np.empty(n)
    delta      = np.empty(n)
    H_Pi       = np.empty(n)
    Nc_star    = np.empty(n)

    for idx in range(n):
        obs_idx = rng.integers(0, K)

        r = rng.random()
        if r < 0.30:
            # -- Peaked correct: obs is the peak --
            peak_idx = obs_idx
            spread = rng.uniform(0.5, 3.5)
            distances = np.abs(np.arange(K) - peak_idx).astype(float)
            pi = np.exp(-spread * distances)

        elif r < 0.45:
            # -- Peaked wrong: peak at a different category --
            peak_idx = (obs_idx + rng.integers(1, K)) % K
            spread = rng.uniform(0.5, 3.5)
            distances = np.abs(np.arange(K) - peak_idx).astype(float)
            pi = np.exp(-spread * distances)

        elif r < 0.65:
            # -- Near-miss: peak adjacent to obs, gentle spread --
            offset = rng.choice([-1, 1])
            peak_idx = max(0, min(K - 1, obs_idx + offset))
            spread = rng.uniform(0.15, 1.2)
            distances = np.abs(np.arange(K) - peak_idx).astype(float)
            pi = np.exp(-spread * distances)

        elif r < 0.85:
            # -- Plateau: broad Gaussian centred on a random category --
            center = rng.uniform(0, K - 1)
            width = rng.uniform(1.0, 3.5)
            pi = np.exp(-0.5 * ((np.arange(K) - center) / width) ** 2)

        else:
            # -- Random: fully random possibility values --
            pi = rng.uniform(0.05, 1.0, K)

        # Add small noise
        pi += rng.uniform(0, 0.03, K)
        pi = np.maximum(pi, 0.0)

        # Subnormality (H_Pi)
        h = rng.beta(2, 5)            # skewed toward low ignorance
        pi = pi / pi.max() * (1.0 - h)

        # --- Scorecard ---
        pi_max = pi.max()
        pi_prime = pi / pi_max

        alpha_star[idx] = pi_prime[obs_idx]
        eta[idx]        = pi_prime.mean()
        delta[idx]      = alpha_star[idx] - eta[idx]
        H_Pi[idx]       = 1.0 - pi_max

        mask = np.ones(K, dtype=bool)
        mask[obs_idx] = False
        Nc_star[idx] = max(0.0, 1.0 - pi_prime[mask].max())

    return alpha_star, eta, delta, H_Pi, Nc_star


# ---------------------------------------------------------------------- #
# Figure                                                                  #
# ---------------------------------------------------------------------- #

def main():
    apply_style()

    alpha_star, eta, delta, H_Pi, Nc_star = _generate_cases()
    specificity = 1.0 - eta   # x-axis

    # Small vertical jitter for alpha*=1 cases to reduce overplotting
    rng_jitter = np.random.default_rng(99)
    at_top = alpha_star > 0.99
    alpha_star_plot = alpha_star.copy()
    alpha_star_plot[at_top] += rng_jitter.uniform(-0.025, 0.005,
                                                   at_top.sum())

    fig, ax = plt.subplots(figsize=(7.0, 6.0))

    # ----- delta contour lines (slope −1 diagonals) ----- #
    # delta = alpha* - eta = alpha* + specificity - 1
    x_line = np.linspace(-0.1, 1.1, 50)
    for d_val in np.arange(-0.6, 0.81, 0.2):
        y_line = d_val + 1.0 - x_line
        style = dict(linewidth=1.2, color=DARK_GREY, alpha=0.25, zorder=1)
        if abs(d_val) < 1e-9:
            style.update(linewidth=1.5, alpha=0.45, linestyle="--")
        else:
            style["linestyle"] = ":"
        ax.plot(x_line, y_line, **style)
        # Label near right edge of plot
        lx = 0.82
        ly = d_val + 1.0 - lx
        if -0.05 < ly < 1.05:
            ax.text(lx + 0.02, ly, rf"$\delta$={d_val:+.1f}",
                    fontsize=7, color=DARK_GREY, alpha=0.55, rotation=-45,
                    va="center", ha="left")

    # ----- scatter plot ----- #
    s_min, s_max = 20, 180
    sizes = s_min + (s_max - s_min) * Nc_star

    mask_dominant = Nc_star > 0.01
    cmap = cm.viridis_r       # low H_Pi = dark (good), high = light (bad)
    norm = Normalize(vmin=0.0, vmax=0.6)

    # Non-dominant cases (N_c* ≈ 0): lighter, smaller edge
    ax.scatter(specificity[~mask_dominant], alpha_star_plot[~mask_dominant],
               s=sizes[~mask_dominant],
               c=H_Pi[~mask_dominant], cmap=cmap, norm=norm,
               edgecolors=MID_GREY, linewidths=0.5, alpha=0.50,
               marker="o", zorder=2)

    # Dominant cases (N_c* > 0): bolder
    sc = ax.scatter(specificity[mask_dominant], alpha_star_plot[mask_dominant],
                    s=sizes[mask_dominant],
                    c=H_Pi[mask_dominant], cmap=cmap, norm=norm,
                    edgecolors=DARK_GREY, linewidths=0.8, alpha=0.85,
                    marker="o", zorder=3)

    # ----- colourbar ----- #
    cbar = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.04, shrink=0.75)
    cbar.set_label(r"Ignorance $H_\Pi$", fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    # ----- quadrant annotations ----- #
    annot_kw = dict(fontsize=8.5, fontstyle="italic", color=DARK_GREY,
                    alpha=0.55, ha="center", va="center")
    ax.text(0.72, 0.92, "Sharp correct",  **annot_kw)
    ax.text(0.08, 0.80, "Diffuse\ncorrect", **annot_kw)
    ax.text(0.72, 0.06, "Sharp wrong",    **annot_kw)
    ax.text(0.08, 0.35, "Diffuse\nwrong", **annot_kw)

    # ----- size legend for N_c* ----- #
    leg_sizes = [0.0, 0.3, 0.7]
    leg_handles = []
    for nc in leg_sizes:
        s = s_min + (s_max - s_min) * nc
        lbl = f"$N_c^*$ = {nc:.1f}" if nc > 0 else r"$N_c^* = 0$"
        leg_handles.append(
            mlines.Line2D([], [], marker="o", linestyle="None",
                          markersize=np.sqrt(s) * 0.65,
                          markerfacecolor=MID_GREY, markeredgecolor=DARK_GREY,
                          label=lbl)
        )
    ax.legend(handles=leg_handles, loc="lower left", fontsize=7.5,
              frameon=True, fancybox=False, edgecolor=MID_GREY,
              title=r"Marker size", title_fontsize=8,
              handletextpad=0.5, borderpad=0.6)

    # ----- axes ----- #
    ax.set_xlabel(r"Specificity  $1 - \eta$  (higher $=$ sharper)", fontsize=10)
    ax.set_ylabel(r"Depth-of-truth  $\alpha^*$", fontsize=10)
    ax.set_xlim(-0.02, 0.85)   # max specificity = 1 − 1/K = 0.8
    ax.set_ylim(-0.02, 1.05)

    fig.tight_layout()
    save_fig(fig, "fig11_performance_diagram")


if __name__ == "__main__":
    main()
