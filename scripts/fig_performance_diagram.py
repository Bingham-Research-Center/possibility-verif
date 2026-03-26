"""Possibilistic performance diagram (Roebber-style).

Five-year synthetic reforecast with SPC-like climatology.  Models a
forecasting system with category-dependent skill and ignorance: common
events (MRGL, SLGT) are forecast confidently and usually correctly;
rare events (MDT, HIGH) carry higher ignorance and more errors.

Encoding (5 metrics on one plot):
  x-axis    1 - eta   specificity (higher = sharper)
  y-axis    alpha*    depth-of-truth (higher = better)
  contours  delta     resolution gap (diagonal iso-lines; delta=0 is key)
  colour    H_Pi      ignorance (dark purple = confident, pale = uncertain)
  size      N_c*      conditional necessity (larger = truth more dominant)

Three anchor scenarios from Section 6 are overlaid as labeled stars.

Structural parallel with Roebber (2009):
  Roebber x = success ratio (precision)  <-->  specificity 1-eta
  Roebber y = POD (detection)            <-->  depth-of-truth alpha*
  Roebber contours = CSI (skill)         <-->  delta contours
  NEW colour = ignorance H_Pi (no deterministic analogue)
  NEW size   = cond. necessity N_c* (no deterministic analogue)

The generate_reforecast() function is designed as a drop-in: replace it
with real (pi_array, obs_categories) data for Clyfar verification.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import Normalize, LinearSegmentedColormap

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, DARK_GREY, MID_GREY, LIGHT_GREY,
    SPC_CATEGORIES, SPC_N,
)
from fig_three_scenario import compute_scorecard, SCENARIOS


# ------------------------------------------------------------------ #
# Data generation (swap this for real data)                           #
# ------------------------------------------------------------------ #

def scorecard_from_data(pi_array, obs_categories, K=SPC_N):
    """Compute five-number scorecard for each forecast--observation pair.

    Parameters
    ----------
    pi_array : ndarray, shape (n, K)
        Raw (possibly subnormal) possibility distributions.
    obs_categories : array-like of str, length n
        Observed SPC category for each case.

    Returns
    -------
    dict of ndarrays: alpha_star, eta, delta, H_Pi, Nc_star, obs_idx
    """
    n = len(obs_categories)
    obs_idx = np.array([SPC_CATEGORIES.index(c) for c in obs_categories])

    alpha_star = np.empty(n)
    eta = np.empty(n)
    delta = np.empty(n)
    H_Pi = np.empty(n)
    Nc_star = np.empty(n)

    for i in range(n):
        pi = pi_array[i]
        oi = obs_idx[i]
        pi_max = pi.max()
        pi_prime = pi / pi_max

        alpha_star[i] = pi_prime[oi]
        eta[i] = pi_prime.mean()
        delta[i] = alpha_star[i] - eta[i]
        H_Pi[i] = 1.0 - pi_max

        mask = np.ones(K, dtype=bool)
        mask[oi] = False
        Nc_star[i] = max(0.0, 1.0 - pi_prime[mask].max())

    return dict(alpha_star=alpha_star, eta=eta, delta=delta,
                H_Pi=H_Pi, Nc_star=Nc_star, obs_idx=obs_idx)


def generate_reforecast(n_years=5, K=SPC_N, seed=42):
    """Generate a five-year synthetic possibilistic reforecast.

    The synthetic model has physically motivated behaviour:
      - SPC-like base rates: MRGL 45 %, SLGT 30 %, ENH 15 %, MDT 8 %, HIGH 2 %
      - Category-dependent accuracy: 78 % correct peak for MRGL, 18 % for HIGH
      - Category-dependent ignorance: H_Pi ~ 0.08 for MRGL, ~ 0.52 for HIGH
      - Near-miss errors: wrong forecasts tend to be +/- 1 category

    Returns
    -------
    dict of ndarrays (alpha_star, eta, delta, H_Pi, Nc_star, obs_idx)
    plus pi_array (n, K) and obs_categories (n,) for downstream use.
    """
    rng = np.random.default_rng(seed)

    # --- Observation climatology ---
    clim = np.array([0.45, 0.30, 0.15, 0.08, 0.02])
    n_days = n_years * 365
    obs_idx = rng.choice(K, size=n_days, p=clim)
    obs_categories = [SPC_CATEGORIES[i] for i in obs_idx]

    # --- Category-dependent model parameters ---
    # P(model peaks at correct category | obs)
    correct_prob = np.array([0.78, 0.65, 0.48, 0.32, 0.18])
    # Mean and std of ignorance H_Pi
    h_mu = np.array([0.08, 0.15, 0.25, 0.38, 0.52])
    h_sig = np.array([0.05, 0.08, 0.10, 0.12, 0.12])
    # Distribution sharpness (exponential decay rate from peak)
    s_mu = np.array([2.8, 2.2, 1.6, 1.2, 0.8])
    s_sig = np.array([0.6, 0.5, 0.5, 0.4, 0.3])

    pi_array = np.empty((n_days, K))

    for i in range(n_days):
        oi = obs_idx[i]

        # Peak category: correct or near-miss
        if rng.random() < correct_prob[oi]:
            peak = oi
        else:
            offset = rng.choice([-2, -1, 1, 2], p=[0.10, 0.40, 0.40, 0.10])
            peak = int(np.clip(oi + offset, 0, K - 1))

        # Pi distribution: exponential decay from peak
        spread = max(0.3, rng.normal(s_mu[oi], s_sig[oi]))
        dists = np.abs(np.arange(K) - peak).astype(float)
        pi = np.exp(-spread * dists)
        pi += rng.uniform(0, 0.02, K)   # small noise

        # Apply subnormality (category-dependent)
        h = np.clip(rng.normal(h_mu[oi], h_sig[oi]), 0.02, 0.85)
        pi = pi / pi.max() * (1.0 - h)

        pi_array[i] = pi

    # Compute scorecard for all cases
    result = scorecard_from_data(pi_array, obs_categories, K)
    result['pi_array'] = pi_array
    result['obs_categories'] = np.array(obs_categories)
    return result


# ------------------------------------------------------------------ #
# Figure                                                              #
# ------------------------------------------------------------------ #

def main():
    apply_style()

    data = generate_reforecast()
    n = len(data['alpha_star'])
    specificity = 1.0 - data['eta']

    # Gentle downward jitter for alpha*=1 cases to reduce overplotting
    # at the top boundary.  All jittered values stay in [0.96, 1.0],
    # which is physically honest (still "correct").
    rng_j = np.random.default_rng(99)
    at_top = data['alpha_star'] > 0.99
    alpha_plot = data['alpha_star'].copy()
    alpha_plot[at_top] -= rng_j.uniform(0.0, 0.04, at_top.sum())

    # Compute §6 anchor scenarios
    anchor_meta = [
        ("Sharp-Correct",  "A", "Sharp, confident\n(MDT obs)"),
        ("Hedged-Correct", "B", "Hedged, uncertain\n(ENH obs)"),
        ("Sharp-Wrong",    "C", "Sharp, wrong\n(MDT obs)"),
    ]
    anchors = []
    for name, letter, desc in anchor_meta:
        sc = SCENARIOS[name]
        card = compute_scorecard(sc['pi'], sc['obs'])
        anchors.append((letter, desc, card))

    fig, ax = plt.subplots(figsize=(7.5, 6.5))

    # ---- Delta contour lines ---- #
    x_line = np.linspace(-0.1, 1.1, 50)
    for d_val in np.arange(-0.6, 0.81, 0.2):
        y_line = d_val + 1.0 - x_line
        if abs(d_val) < 1e-9:
            # delta = 0: the key boundary
            ax.plot(x_line, y_line, linewidth=1.5, color=DARK_GREY,
                    alpha=0.35, linestyle="--", zorder=1)
            ax.text(0.30, 0.72, r"$\delta = 0$", fontsize=8,
                    color=DARK_GREY, alpha=0.55, rotation=-45,
                    ha="center", va="center")
        else:
            ax.plot(x_line, y_line, linewidth=0.5, color=MID_GREY,
                    alpha=0.15, linestyle=":", zorder=1)
    # Label two reference contours
    ax.text(0.60, 0.82, r"$\delta{=}{+}0.4$", fontsize=6.5,
            color=MID_GREY, alpha=0.55, rotation=-45, ha="center")
    ax.text(0.60, 0.42, r"$\delta{=}{-}0.2$", fontsize=6.5,
            color=MID_GREY, alpha=0.55, rotation=-45, ha="center")

    # ---- Colormap: dark purple (confident) → pale lavender (uncertain) ---- #
    cmap = LinearSegmentedColormap.from_list(
        "hpi", [PURPLE, "#C9A5E0", "#F0E4F7"], N=256)
    norm = Normalize(vmin=0.0, vmax=0.65)

    # ---- Scatter: all cases ---- #
    s_min, s_max = 12, 140
    sizes = s_min + (s_max - s_min) * data['Nc_star']

    ax.scatter(
        specificity, alpha_plot,
        s=sizes, c=data['H_Pi'], cmap=cmap, norm=norm,
        edgecolors=DARK_GREY, linewidths=0.2, alpha=0.25,
        marker="o", zorder=2, rasterized=True,
    )
    # Slightly bolder layer for MDT/HIGH obs days so they're visible
    rare = data['obs_idx'] >= 3   # MDT or HIGH
    sc = ax.scatter(
        specificity[rare], alpha_plot[rare],
        s=sizes[rare] * 1.3, c=data['H_Pi'][rare], cmap=cmap, norm=norm,
        edgecolors=DARK_GREY, linewidths=0.5, alpha=0.55,
        marker="D", zorder=3,
    )

    # ---- Anchor points from §6 ---- #
    anchor_offsets = {
        "A": (-0.22, -0.18),
        "B": (-0.22, -0.18),
        "C": (-0.22, 0.14),
    }
    for letter, desc, card in anchors:
        sx = 1 - card['eta']
        sy = card['alpha_star']
        ax.scatter(
            sx, sy, s=300, c=[card['H_Pi']], cmap=cmap, norm=norm,
            edgecolors="white", linewidths=2.5, alpha=1.0,
            marker="*", zorder=6,
        )
        ox, oy = anchor_offsets[letter]
        ax.annotate(
            f"{letter}: {desc}",
            xy=(sx, sy), xytext=(sx + ox, sy + oy),
            fontsize=7, fontweight="bold", color=DARK_GREY,
            arrowprops=dict(arrowstyle="->", color=MID_GREY, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                      edgecolor=MID_GREY, alpha=0.9),
            zorder=7, linespacing=1.3,
        )

    # ---- Colorbar ---- #
    cbar = fig.colorbar(sc, ax=ax, pad=0.02, fraction=0.04, shrink=0.70)
    cbar.set_label(r"Ignorance $H_\Pi$" + "\n(dark = confident)",
                   fontsize=9)
    cbar.ax.tick_params(labelsize=8)

    # ---- Quadrant annotations ---- #
    kw = dict(fontsize=9, fontstyle="italic", color=DARK_GREY,
              alpha=0.35, ha="center", va="center")
    ax.text(0.75, 0.90, "Sharp\ncorrect", **kw)
    ax.text(0.06, 0.90, "Diffuse\ncorrect", **kw)
    ax.text(0.75, 0.08, "Sharp\nwrong", **kw)
    ax.text(0.06, 0.42, "Diffuse\nwrong", **kw)

    # ---- Size legend ---- #
    leg_handles = []
    for nc in [0.0, 0.3, 0.7]:
        s = s_min + (s_max - s_min) * nc
        lbl = f"$N_c^*$ = {nc:.1f}" if nc > 0 else r"$N_c^* = 0$"
        leg_handles.append(
            mlines.Line2D([], [], marker="o", linestyle="None",
                          markersize=np.sqrt(s) * 0.65,
                          markerfacecolor=MID_GREY,
                          markeredgecolor=DARK_GREY, label=lbl))
    # Diamond marker explanation
    leg_handles.append(
        mlines.Line2D([], [], marker="D", linestyle="None",
                      markersize=5, markerfacecolor="#C9A5E0",
                      markeredgecolor=DARK_GREY,
                      label="MDT / HIGH obs"))
    ax.legend(handles=leg_handles, loc="lower left", fontsize=7,
              frameon=True, fancybox=False, edgecolor=MID_GREY,
              title="Marker encoding", title_fontsize=7.5,
              handletextpad=0.5, borderpad=0.6)

    # ---- Axes ---- #
    ax.set_xlabel(r"Specificity  $1 - \eta$  (higher = sharper)",
                  fontsize=10)
    ax.set_ylabel(r"Depth-of-truth  $\alpha^*$  (higher = better)",
                  fontsize=10)
    ax.set_xlim(-0.02, 0.85)
    ax.set_ylim(-0.04, 1.04)

    # Print data summary for caption reference
    n_mdt = (data['obs_idx'] == 3).sum()
    n_high = (data['obs_idx'] == 4).sum()
    print(f"  Data: n={n}, MDT obs={n_mdt}, HIGH obs={n_high}")

    fig.tight_layout()
    save_fig(fig, "fig11_performance_diagram")


if __name__ == "__main__":
    main()
