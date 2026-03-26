"""Possibilistic performance diagram (Roebber-style), two-panel.

Left panel:  all days (n ≈ 1,825) — full context including null (NONE) cases.
Right panel: severe days only (SLGT+) — where the framework earns its keep.
             Without the NONE/MRGL mass the rare-event population
             (MDT/HIGH) is exposed and ignorance patterns become visible.

Encoding (5 metrics on one plot):
  x-axis    1 - eta   specificity (higher = sharper)
  y-axis    alpha*    depth-of-truth (higher = better)
  contours  delta     resolution gap (diagonal iso-lines; delta=0 is key)
  colour    H_Pi      ignorance (dark purple = confident, pale = uncertain)
  size      N_c*      conditional necessity (larger = truth more dominant)

Three anchor scenarios from Section 6 are overlaid as labeled stars.

The generate_reforecast() / scorecard_from_data() functions are designed
as drop-ins: replace with real (pi_array, obs_categories) data for
Clyfar verification.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Ellipse
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


def generate_reforecast(n_years=2, K=SPC_N, seed=42):
    """Generate a two-year synthetic possibilistic reforecast.

    The synthetic model has physically motivated behaviour:
      - SPC-like base rates (slightly smoothed to reduce null-day dominance):
        NONE 60 %, MRGL 18 %, SLGT 12 %, ENH 6 %, MDT 3.2 %, HIGH 0.8 %
      - Category-dependent accuracy: 82 % correct peak for NONE, 18 % for HIGH
      - Category-dependent ignorance: H_Pi ~ 0.06 for NONE, ~ 0.52 for HIGH
      - Near-miss errors: wrong forecasts tend to be +/- 1 category
      - Extra spread noise for visual separation on the diagram

    Returns
    -------
    dict of ndarrays (alpha_star, eta, delta, H_Pi, Nc_star, obs_idx)
    plus pi_array (n, K) and obs_categories (n,) for downstream use.
    """
    rng = np.random.default_rng(seed)

    # --- Observation climatology ---
    clim = np.array([0.60, 0.18, 0.12, 0.06, 0.032, 0.008])
    n_days = n_years * 365
    obs_idx = rng.choice(K, size=n_days, p=clim)
    obs_categories = [SPC_CATEGORIES[i] for i in obs_idx]

    # --- Category-dependent model parameters ---
    # Wider spread & ignorance sigmas to scatter points more on the diagram
    correct_prob = np.array([0.82, 0.78, 0.65, 0.48, 0.32, 0.18])
    h_mu = np.array([0.06, 0.08, 0.15, 0.25, 0.38, 0.52])
    h_sig = np.array([0.06, 0.07, 0.12, 0.14, 0.16, 0.15])
    s_mu = np.array([2.6, 2.4, 1.8, 1.3, 1.0, 0.7])
    s_sig = np.array([0.9, 0.9, 0.8, 0.7, 0.6, 0.5])

    pi_array = np.empty((n_days, K))

    for i in range(n_days):
        oi = obs_idx[i]

        if rng.random() < correct_prob[oi]:
            peak = oi
        else:
            offset = rng.choice([-2, -1, 1, 2], p=[0.10, 0.40, 0.40, 0.10])
            peak = int(np.clip(oi + offset, 0, K - 1))

        spread = max(0.3, rng.normal(s_mu[oi], s_sig[oi]))
        dists = np.abs(np.arange(K) - peak).astype(float)
        pi = np.exp(-spread * dists)
        pi += rng.uniform(0, 0.03, K)

        h = np.clip(rng.normal(h_mu[oi], h_sig[oi]), 0.02, 0.85)
        pi = pi / pi.max() * (1.0 - h)

        pi_array[i] = pi

    result = scorecard_from_data(pi_array, obs_categories, K)
    result['pi_array'] = pi_array
    result['obs_categories'] = np.array(obs_categories)
    return result


# ------------------------------------------------------------------ #
# Panel-drawing helper                                                #
# ------------------------------------------------------------------ #

_MISS_RED = "#C0392B"

def _draw_panel(ax, spec, alpha, sizes, hpi, obs_idx,
                cmap, norm, s_min, anchors,
                show_anchor_labels=False, title=""):
    """Draw one performance-diagram panel."""

    # ---- Delta contours ---- #
    x_line = np.linspace(-0.1, 1.1, 50)
    for d_val in np.arange(-0.6, 0.81, 0.2):
        y_line = d_val + 1.0 - x_line
        if abs(d_val) < 1e-9:
            ax.plot(x_line, y_line, lw=1.5, color=DARK_GREY,
                    alpha=0.35, ls="--", zorder=1)
        else:
            ax.plot(x_line, y_line, lw=0.5, color=MID_GREY,
                    alpha=0.15, ls=":", zorder=1)
    ax.text(0.28, 0.74, r"$\delta\!=\!0$", fontsize=7,
            color=DARK_GREY, alpha=0.5, rotation=-45,
            ha="center", va="center")

    # ---- Scatter ---- #
    _NONE_IDX = SPC_CATEGORIES.index("NONE")
    null = obs_idx == _NONE_IDX
    eventful = ~null

    # Layer 1: null days — shaded ellipse summary (visible only in panel a)
    if null.any():
        n_none = null.sum()
        cx = spec[null].mean()
        cy = alpha[null].mean()
        wx = max(spec[null].std() * 4, 0.04)  # 2-sigma width
        wy = max(alpha[null].std() * 4, 0.04)
        ell = Ellipse((cx, cy), wx, wy, facecolor="#D0D0D0", alpha=0.35,
                       edgecolor="#AAAAAA", linewidth=0.8, zorder=1)
        ax.add_patch(ell)
        ax.text(cx, cy, f"$n = {n_none:,}$\nNONE obs", fontsize=6,
                ha="center", va="center", color=MID_GREY,
                fontweight="bold", zorder=2)

    # Layer 2: eventful days — colored circles
    sc_main = ax.scatter(spec[eventful], alpha[eventful],
                         s=sizes[eventful], c=hpi[eventful],
                         cmap=cmap, norm=norm,
                         edgecolors=DARK_GREY, linewidths=0.2, alpha=0.35,
                         marker="o", zorder=2, rasterized=True)

    rare = obs_idx >= SPC_CATEGORIES.index("MDT")
    sc = ax.scatter(spec[rare], alpha[rare],
                    s=sizes[rare] * 1.3, c=hpi[rare], cmap=cmap, norm=norm,
                    edgecolors=DARK_GREY, linewidths=0.5, alpha=0.55,
                    marker="D", zorder=3)

    # ---- Anchor stars ---- #
    anchor_offsets = {
        "A": (-0.20, -0.16),
        "B": (-0.20, -0.16),
        "C": (-0.20, 0.14),
    }
    for letter, desc, card, verified in anchors:
        sx, sy = 1 - card['eta'], card['alpha_star']
        edge_color = GREEN if verified else _MISS_RED
        ax.scatter(sx, sy, s=280, c=[card['H_Pi']], cmap=cmap, norm=norm,
                   edgecolors=edge_color, linewidths=2.0, alpha=1.0,
                   marker="*", zorder=6)
        if show_anchor_labels:
            ox, oy = anchor_offsets[letter]
            ax.annotate(
                f"{letter}: {desc}", xy=(sx, sy),
                xytext=(sx + ox, sy + oy),
                fontsize=6.5, fontweight="bold", color=DARK_GREY,
                arrowprops=dict(arrowstyle="->", color=MID_GREY, lw=0.7),
                bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                          edgecolor=MID_GREY, alpha=0.9),
                zorder=7, linespacing=1.3)

    # ---- Quadrant labels ---- #
    kw = dict(fontsize=8, fontstyle="italic", color=DARK_GREY,
              alpha=0.30, ha="center", va="center")
    ax.text(0.73, 0.90, "Sharp\ncorrect", **kw)
    ax.text(0.06, 0.90, "Diffuse\ncorrect", **kw)
    ax.text(0.73, 0.08, "Sharp\nwrong", **kw)
    ax.text(0.06, 0.38, "Diffuse\nwrong", **kw)

    # ---- Axes ---- #
    ax.set_xlim(-0.02, 0.85)
    ax.set_ylim(-0.04, 1.04)
    ax.set_title(title, fontsize=9, fontweight="bold", pad=6)

    return sc


# ------------------------------------------------------------------ #
# Figure                                                              #
# ------------------------------------------------------------------ #

def main():
    apply_style()

    data = generate_reforecast()
    n_all = len(data['alpha_star'])
    specificity = 1.0 - data['eta']

    # Jitter alpha*=1 cases downward within [0.96, 1.0]
    rng_j = np.random.default_rng(99)
    at_top = data['alpha_star'] > 0.99
    alpha_plot = data['alpha_star'].copy()
    alpha_plot[at_top] -= rng_j.uniform(0.0, 0.04, at_top.sum())

    # Sizes (scaled for smaller figsize)
    s_min, s_max = 8, 80
    sizes = s_min + (s_max - s_min) * data['Nc_star']

    # Colormap and norm (shared)
    cmap = LinearSegmentedColormap.from_list(
        "hpi", [PURPLE, "#C9A5E0", "#F0E4F7"], N=256)
    norm = Normalize(vmin=0.0, vmax=0.65)

    # §6 anchor scenarios (with verified flag for edge colour)
    anchor_meta = [
        ("Sharp-Correct",  "A", "Sharp, confident\n(MDT obs)",  True),
        ("Hedged-Correct", "B", "Hedged, uncertain\n(ENH obs)", True),
        ("Sharp-Wrong",    "C", "Sharp, wrong\n(MDT obs)",      False),
    ]
    anchors = []
    for name, letter, desc, verified in anchor_meta:
        sc = SCENARIOS[name]
        card = compute_scorecard(sc['pi'], sc['obs'])
        anchors.append((letter, desc, card, verified))

    # ---- Subset: SLGT+ ---- #
    _SLGT_IDX = SPC_CATEGORIES.index("SLGT")
    severe = data['obs_idx'] >= _SLGT_IDX
    n_sev = severe.sum()

    # ---- Figure ---- #
    fig, (ax_l, ax_r) = plt.subplots(
        1, 2, figsize=(7.5, 3.5), sharey=True,
        gridspec_kw={"wspace": 0.12, "right": 0.88})

    # Left: all days
    _draw_panel(ax_l, specificity, alpha_plot, sizes, data['H_Pi'],
                data['obs_idx'], cmap, norm, s_min, anchors,
                show_anchor_labels=False,
                title=f"(a)  All days  ($n = {n_all:,}$)")
    ax_l.set_xlabel(r"Specificity  $1 - \eta$  (higher = sharper)", fontsize=9)
    ax_l.set_ylabel(r"Depth-of-truth  $\alpha^*$  (higher = better)", fontsize=9)

    # Right: SLGT+ only
    sc = _draw_panel(
        ax_r, specificity[severe], alpha_plot[severe],
        sizes[severe], data['H_Pi'][severe],
        data['obs_idx'][severe], cmap, norm, s_min, anchors,
        show_anchor_labels=True,
        title=f"(b)  Severe days only  (SLGT+,  $n = {n_sev:,}$)")
    ax_r.set_xlabel(r"Specificity  $1 - \eta$  (higher = sharper)", fontsize=9)

    # ---- Shared colorbar ---- #
    cbar = fig.colorbar(sc, ax=[ax_l, ax_r], pad=0.02, fraction=0.025,
                        shrink=0.75)
    cbar.set_label(r"Ignorance $H_\Pi$" + "\n(dark = confident)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)

    # ---- Shared legend (on left panel) ---- #
    leg_handles = []
    for nc in [0.0, 0.3, 0.7]:
        s = s_min + (s_max - s_min) * nc
        lbl = f"$N_c^*$ = {nc:.1f}" if nc > 0 else r"$N_c^* = 0$"
        leg_handles.append(
            mlines.Line2D([], [], marker="o", linestyle="None",
                          markersize=np.sqrt(s) * 0.6,
                          markerfacecolor=MID_GREY,
                          markeredgecolor=DARK_GREY, label=lbl))
    leg_handles.append(
        mlines.Line2D([], [], marker="D", linestyle="None",
                      markersize=4.5, markerfacecolor="#C9A5E0",
                      markeredgecolor=DARK_GREY,
                      label="MDT / HIGH obs"))
    leg_handles.append(
        mlines.Line2D([], [], marker="o", linestyle="None",
                      markersize=5, markerfacecolor="#D0D0D0",
                      markeredgecolor="#AAAAAA", alpha=0.5,
                      label="NONE cluster (panel a)"))
    leg_handles.append(
        mlines.Line2D([], [], marker="*", linestyle="None",
                      markersize=7, markerfacecolor=MID_GREY,
                      markeredgecolor=GREEN, markeredgewidth=1.2,
                      label="Anchor (verified)"))
    leg_handles.append(
        mlines.Line2D([], [], marker="*", linestyle="None",
                      markersize=7, markerfacecolor=MID_GREY,
                      markeredgecolor=_MISS_RED, markeredgewidth=1.2,
                      label="Anchor (miss)"))
    ax_l.legend(handles=leg_handles, loc="lower left", fontsize=6.5,
                frameon=True, fancybox=False, edgecolor=MID_GREY,
                title="Marker encoding", title_fontsize=7,
                handletextpad=0.4, borderpad=0.5)

    # Print summary
    n_mdt = (data['obs_idx'] == SPC_CATEGORIES.index("MDT")).sum()
    n_high = (data['obs_idx'] == SPC_CATEGORIES.index("HIGH")).sum()
    print(f"  All: n={n_all}  |  SLGT+: n={n_sev}  "
          f"|  MDT: {n_mdt}  HIGH: {n_high}")

    save_fig(fig, "performance_diagram")


if __name__ == "__main__":
    main()
