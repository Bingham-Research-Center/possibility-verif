"""V3/V4 performance diagram iterations.

Changes:
  - Enhanced colormap with more dynamic range (purple → warm peach)
  - 1:1 hex aspect ratio via set_aspect('equal')
  - Larger hexagons (reduced gridsize) for spatial smoothing
  - V3: GREEN trajectory for clear figure–ground separation
  - V4: Category trajectory, extended y-axis, SLGT+ and two-panel variants
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import Normalize, LinearSegmentedColormap
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (
    apply_style, save_fig,
    PURPLE, GREEN, DARK_GREY, MID_GREY, LIGHT_GREY,
    SPC_CATEGORIES, SPC_N,
)
from fig_three_scenario import compute_scorecard, SCENARIOS
from fig_performance_diagram import generate_reforecast

MISS_RED = "#C0392B"
SCENARIO_MARKERS = {"A": "*", "B": "D", "C": "X"}


# ------------------------------------------------------------------ #
# Colormaps with more dynamic range                                    #
# ------------------------------------------------------------------ #

def hpi_cmap():
    """H_Pi: dark purple (confident) → pale purple (uncertain)."""
    return LinearSegmentedColormap.from_list("hpi2", [
        "#2E0854", PURPLE, "#CE93D8", "#F3E5F5",
    ], N=256)


def hpi_green_cmap():
    """H_Pi in green: dark green (confident) → medium-light green (uncertain).
    Stops before white so uncertain dots remain visibly green."""
    return LinearSegmentedColormap.from_list("hpi_green", [
        "#1B5E20", GREEN, "#81C784",
    ], N=256)


def count_cmap():
    """Count: medium purple (few) → very dark purple (many).
    No near-white shades so sparse bins remain visible."""
    return LinearSegmentedColormap.from_list("cnt2", [
        "#CE93D8", PURPLE, "#4A0072",
    ], N=256)


# ------------------------------------------------------------------ #
# Data                                                                 #
# ------------------------------------------------------------------ #

def get_data():
    d = generate_reforecast()
    spec = 1.0 - d['eta']
    rng = np.random.default_rng(99)
    top = d['alpha_star'] > 0.99
    ap = d['alpha_star'].copy()
    ap[top] -= rng.uniform(0.0, 0.04, top.sum())

    anchors = []
    for name, ltr, v in [
        ("Sharp-Correct", "A", True),
        ("Hedged-Correct", "B", True),
        ("Sharp-Wrong", "C", False),
    ]:
        c = compute_scorecard(SCENARIOS[name]['pi'], SCENARIOS[name]['obs'])
        anchors.append((ltr, c, v))
    return d, ap, spec, anchors


def cat_means(data, spec, mask=None):
    """Per-category means for both axis systems."""
    r = {}
    for ci, cat in enumerate(SPC_CATEGORIES):
        m = data['obs_idx'] == ci
        if mask is not None:
            m = m & mask
        n = m.sum()
        if n == 0:
            continue
        r[cat] = dict(
            spec=spec[m].mean(), alpha=data['alpha_star'][m].mean(),
            hpi=data['H_Pi'][m].mean(),
            pimax=(1.0 - data['H_Pi'][m]).mean(),
            delta=data['delta'][m].mean(),
            n=n,
        )
    return r


# ------------------------------------------------------------------ #
# Shared drawing helpers                                               #
# ------------------------------------------------------------------ #

def draw_hyperbolas(ax, levels=None, label=True, color=MID_GREY, alpha=0.25):
    if levels is None:
        levels = np.arange(0.1, 1.0, 0.1)
    x = np.linspace(0.02, 1.0, 300)
    for s in levels:
        y = s / x
        m = (y >= -0.05) & (y <= 1.06)
        ax.plot(x[m], y[m], lw=0.5, color=color, alpha=alpha, zorder=0)
        if label:
            idx = np.argmin(np.abs(x - np.sqrt(s)))
            if m[idx] and 0.02 < y[idx] < 1.0:
                ax.text(x[idx], y[idx] + 0.025, f"{s:.1f}",
                        fontsize=5, color=color,
                        alpha=min(alpha + 0.2, 0.55),
                        ha="center", va="bottom")


def draw_delta0_diag(ax):
    """delta=0 diagonal on the (1-eta, alpha*) plane."""
    x = np.linspace(-0.05, 1.05, 50)
    ax.plot(x, 1 - x, lw=1.2, ls="--", color=DARK_GREY, alpha=0.3, zorder=1)
    ax.text(0.20, 0.82, r"$\delta\!=\!0$", fontsize=7, color=DARK_GREY,
            alpha=0.4, rotation=-45, ha="center")


def draw_delta0_horiz(ax):
    """delta=0 horizontal on the (pimax, delta) plane."""
    ax.axhline(0, color=DARK_GREY, lw=1.2, ls="--", alpha=0.35, zorder=1)
    ax.text(0.04, 0.015, r"$\delta = 0$  (break-even)", fontsize=7,
            color=DARK_GREY, alpha=0.55, va="bottom")


def draw_compass(ax, x, y, text="better", color=PURPLE):
    ax.annotate("", xy=(x, y), xytext=(x - 0.12, y - 0.12),
                arrowprops=dict(arrowstyle="->", color=color, lw=1.5),
                zorder=10)
    ax.text(x - 0.06, y + 0.025, text, fontsize=7, fontweight="bold",
            color=color, ha="center", va="bottom", zorder=10)


def draw_scenarios_spec_alpha(ax, anchors, sz=90):
    """Scenario markers on the (1-eta, alpha*) plane."""
    offsets = {"A": (0.06, -0.06), "B": (0.06, -0.06), "C": (0.06, 0.05)}
    for ltr, c, v in anchors:
        sx, sy = 1 - c['eta'], c['alpha_star']
        edge = GREEN if v else MISS_RED
        marker = SCENARIO_MARKERS.get(ltr, "*")
        ax.scatter(sx, sy, s=sz, fc="white", ec=edge,
                   linewidths=1.8, marker=marker, zorder=9)
        ox, oy = offsets[ltr]
        ax.annotate(ltr, xy=(sx, sy), xytext=(sx + ox, sy + oy),
                    fontsize=8, fontweight="bold", color=DARK_GREY,
                    arrowprops=dict(arrowstyle="->", color=MID_GREY, lw=0.5),
                    zorder=10)


def draw_scenarios_commit(ax, anchors, sz=110):
    """Scenario markers on the (pimax, delta) plane."""
    offsets = {"A": (-0.06, -0.05), "B": (0.06, 0.04), "C": (0.06, 0.04)}
    for ltr, c, v in anchors:
        sx = 1 - c['H_Pi']
        sy = c['delta']
        edge = GREEN if v else MISS_RED
        marker = SCENARIO_MARKERS.get(ltr, "*")
        ax.scatter(sx, sy, s=sz, fc="white", ec=edge,
                   linewidths=1.8, marker=marker, zorder=9)
        ox, oy = offsets[ltr]
        ax.annotate(ltr, xy=(sx, sy), xytext=(sx + ox, sy + oy),
                    fontsize=8, fontweight="bold", color=DARK_GREY,
                    arrowprops=dict(arrowstyle="->", color=MID_GREY, lw=0.5),
                    zorder=10)


def _traj_labels(ax, cats, xs, ys, ns, color=GREEN, fontsize=6.5):
    """Alternating-side labels for trajectory points."""
    sides = ["right", "left", "right", "left", "right", "left"]
    for i, c in enumerate(cats):
        side = sides[i] if i < len(sides) else "right"
        ox = 0.07 if side == "right" else -0.07
        ha = "left" if side == "right" else "right"
        ax.annotate(
            f"{c}", xy=(xs[i], ys[i]),
            xytext=(xs[i] + ox, ys[i]),
            fontsize=fontsize, fontweight="bold", color=DARK_GREY, ha=ha,
            arrowprops=dict(arrowstyle="-", color=color, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=color,
                      alpha=0.85, lw=0.5),
            zorder=8)


def _smooth_path(xs, ys, n_pts=80):
    """Smooth curve through trajectory points using numpy polyfit."""
    xs, ys = np.asarray(xs), np.asarray(ys)
    t = np.linspace(0, 1, len(xs))
    ts = np.linspace(0, 1, n_pts)
    deg = min(3, len(xs) - 1)
    return np.polyval(np.polyfit(t, xs, deg), ts), \
           np.polyval(np.polyfit(t, ys, deg), ts)


def draw_traj_spec_alpha(ax, means, color=GREEN, gcmap=None, gnorm=None):
    """GREEN trajectory on (1-eta, alpha*) axes.

    If gcmap/gnorm are provided, dots are shaded by mean H_Pi
    (dark green = confident, pale green = uncertain).
    """
    cats = [c for c in SPC_CATEGORIES if c in means]
    xs = [means[c]['spec'] for c in cats]
    ys = [means[c]['alpha'] for c in cats]
    ns = [means[c]['n'] for c in cats]

    s_min, s_max = 60, 350
    mx = max(ns)
    sizes = [s_min + (s_max - s_min) * (n / mx) for n in ns]

    if gcmap is not None and gnorm is not None:
        hs = [means[c]['hpi'] for c in cats]
        ax.scatter(xs, ys, s=sizes, c=hs, cmap=gcmap, norm=gnorm,
                   ec="white", lw=2.0, zorder=6)
        ax.scatter(xs, ys, s=sizes, c=hs, cmap=gcmap, norm=gnorm,
                   ec=DARK_GREY, lw=0.8, zorder=7)
    else:
        ax.scatter(xs, ys, s=sizes, fc=color, ec="white", lw=2.0, zorder=6)
        ax.scatter(xs, ys, s=sizes, fc=color, ec=DARK_GREY, lw=0.8, zorder=7)

    _traj_labels(ax, cats, xs, ys, ns, color=GREEN)


def draw_traj_commit(ax, means, color=GREEN, fontsize=6.5,
                     gcmap=None, gnorm=None):
    """GREEN trajectory on (pimax, delta) axes.

    If gcmap/gnorm are provided, dots are shaded by mean H_Pi.
    """
    cats = [c for c in SPC_CATEGORIES if c in means]
    xs = [means[c]['pimax'] for c in cats]
    ys = [means[c]['delta'] for c in cats]
    ns = [means[c]['n'] for c in cats]

    s_min, s_max = 60, 350
    mx = max(ns)
    sizes = [s_min + (s_max - s_min) * (n / mx) for n in ns]

    if gcmap is not None and gnorm is not None:
        hs = [means[c]['hpi'] for c in cats]
        ax.scatter(xs, ys, s=sizes, c=hs, cmap=gcmap, norm=gnorm,
                   ec="white", lw=2.0, zorder=6)
        ax.scatter(xs, ys, s=sizes, c=hs, cmap=gcmap, norm=gnorm,
                   ec=DARK_GREY, lw=0.8, zorder=7)
    else:
        ax.scatter(xs, ys, s=sizes, fc=color, ec="white", lw=2.0, zorder=6)
        ax.scatter(xs, ys, s=sizes, fc=color, ec=DARK_GREY, lw=0.8, zorder=7)

    _traj_labels(ax, cats, xs, ys, ns, color=GREEN)


# ------------------------------------------------------------------ #
# V3b — Green trajectory + enhanced hexbin (all days)                  #
# ------------------------------------------------------------------ #

def v3b(data, ap, spec, anchors):
    """V3b: green trajectory + enhanced hexbin (all days)."""
    from style import FIG_DIR, FIG_FORMAT, DPI
    import os

    cm = hpi_cmap()
    nm = Normalize(0.0, 0.55)
    gcm = hpi_green_cmap()
    means = cat_means(data, spec)

    # Tight figsize minimises whitespace so bbox_inches='tight' can't
    # distort the aspect ratio.  Axes box is exactly 3.0" × 3.0".
    fig = plt.figure(figsize=(4.4, 3.9))
    ax = fig.add_axes([0.14, 0.13, 3.2 / 4.4, 3.2 / 3.9])
    cax = fig.add_axes([0.89, 0.30, 0.025, 0.35])

    ax.set_xlim(-0.02, 1.04)
    ax.set_ylim(-0.02, 1.04)
    ax.set_aspect('equal')

    draw_hyperbolas(ax)
    draw_delta0_diag(ax)

    # gridsize=(nx, ny): matplotlib's default ny=int(nx/sqrt(3)) rounds
    # DOWN, producing hexagons ~16% too tall.  (12, 7) gives <1% error.
    ax.hexbin(spec, ap, C=data['H_Pi'],
              reduce_C_function=np.mean, gridsize=(12, 7), cmap=cm,
              extent=(-0.02, 1.04, -0.02, 1.04),
              edgecolors="white", linewidths=0.4, mincnt=1,
              alpha=0.65, zorder=1)

    draw_traj_spec_alpha(ax, means, gcmap=gcm, gnorm=nm)
    draw_scenarios_spec_alpha(ax, anchors)

    # Purple colorbar for hexbin H_Pi
    from matplotlib.colorbar import ColorbarBase
    cb = ColorbarBase(cax, cmap=cm, norm=nm, orientation='vertical')
    cax.yaxis.tick_right()
    cax.yaxis.set_label_position("right")
    cax.set_ylabel(r"Hex mean $H_\Pi$" + "\n(dark = confident)", fontsize=7)
    cax.tick_params(labelsize=6)

    # Green colorbar for category-mean dot H_Pi shading
    cax2 = fig.add_axes([0.89, 0.70, 0.025, 0.20])
    cb2 = ColorbarBase(cax2, cmap=gcm, norm=nm, orientation='vertical')
    cax2.yaxis.tick_right()
    cax2.yaxis.set_label_position("right")
    cax2.set_ylabel(r"Dot mean $H_\Pi$", fontsize=7)
    cax2.tick_params(labelsize=6)

    h_t = mlines.Line2D([], [], marker="o", ls="-", color=GREEN, lw=2,
                        mfc=GREEN, mec=DARK_GREY, ms=6,
                        label="Category mean")
    h_a = mlines.Line2D([], [], marker="*", ls="None", ms=8,
                        mfc="white", mec=GREEN, mew=1.2,
                        label="Scenario A (sharp-correct)")
    h_b = mlines.Line2D([], [], marker="D", ls="None", ms=7,
                        mfc="white", mec=GREEN, mew=1.2,
                        label="Scenario B (hedged-correct)")
    h_c = mlines.Line2D([], [], marker="X", ls="None", ms=8,
                        mfc="white", mec=MISS_RED, mew=1.2,
                        label="Scenario C (sharp-wrong)")
    ax.legend(handles=[h_t, h_a, h_b, h_c], loc="lower left", fontsize=6.5,
              frameon=True, fancybox=False, edgecolor=MID_GREY)

    ax.set_xlabel(r"Specificity  $1\!-\!\eta$  (sharper $\rightarrow$)",
                  fontsize=9)
    ax.set_ylabel(r"Depth-of-truth  $\alpha^*$  (more truthful $\rightarrow$)",
                  fontsize=9)

    # Save WITHOUT bbox_inches='tight' to preserve exact square axes
    path = os.path.join(FIG_DIR, f"perf_hexbin_trajectory.{FIG_FORMAT}")
    os.makedirs(FIG_DIR, exist_ok=True)
    with plt.rc_context({'savefig.bbox': 'standard'}):
        fig.savefig(path, facecolor="white", transparent=False,
                    dpi=DPI, pad_inches=0)
    plt.close(fig)
    print(f"Saved: {path}")


# ------------------------------------------------------------------ #
# V4b — Enhanced commitment–support-margin + trajectory (all days)     #
# ------------------------------------------------------------------ #

def v4b(data, ap, spec, anchors):
    """V4b: commitment-support-margin + trajectory (all days)."""
    from style import FIG_DIR, FIG_FORMAT, DPI
    from matplotlib.colors import LogNorm
    import os

    cm = count_cmap()
    gcm = hpi_green_cmap()
    gnm = Normalize(0.0, 0.55)
    means = cat_means(data, spec)

    pi_max = 1.0 - data['H_Pi']
    delta = data['delta']

    # Manual axes sizing: x_range = 1.04, y_range = 1.30
    # Axes height = 3.0 * (1.30 / 1.04) = 3.75 inches
    # Widened to 4.6" to accommodate dual colorbars
    ax_w, ax_h = 3.0, 3.0 * (1.30 / 1.04)
    fig_w = 4.6
    fig = plt.figure(figsize=(fig_w, ax_h + 0.9))
    ax = fig.add_axes([0.15, 0.11, ax_w / fig_w, ax_h / (ax_h + 0.9)])
    cax = fig.add_axes([0.83, 0.25, 0.025, 0.35])

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.45, 0.85)
    ax.set_aspect('equal')

    # gridsize=(11, 8): gives <1% hex distortion for this aspect ratio.
    hb = ax.hexbin(pi_max, delta, gridsize=(11, 8), cmap=cm,
                   extent=(-0.02, 1.02, -0.45, 0.85),
                   edgecolors="white", linewidths=0.4, mincnt=1, zorder=2)
    hb.set_norm(LogNorm(vmin=1, vmax=hb.get_array().max()))

    draw_delta0_horiz(ax)

    kw = dict(fontsize=8, fontstyle="italic", color=DARK_GREY,
              alpha=0.2, ha="center", va="center")
    ax.text(0.85, 0.60, "Committed &\nwell-shaped", **kw)
    ax.text(0.15, 0.60, "Cautious &\nwell-shaped", **kw)
    ax.text(0.85, -0.30, "Overconfident\n& wrong", **kw)
    ax.text(0.15, -0.30, "Uninformative", **kw)

    draw_traj_commit(ax, means, gcmap=gcm, gnorm=gnm)
    draw_scenarios_commit(ax, anchors)

    # Count colorbar for hexbin
    from matplotlib.colorbar import ColorbarBase
    cb = plt.colorbar(hb, cax=cax)
    cb.set_label("Count per bin\n(log scale)", fontsize=7)
    cb.ax.tick_params(labelsize=6)

    # Green colorbar for category-mean dot H_Pi shading
    cax2 = fig.add_axes([0.83, 0.66, 0.025, 0.18])
    cb2 = ColorbarBase(cax2, cmap=gcm, norm=gnm, orientation='vertical')
    cax2.yaxis.tick_right()
    cax2.yaxis.set_label_position("right")
    cax2.set_ylabel(r"Dot mean $H_\Pi$", fontsize=7)
    cax2.tick_params(labelsize=6)

    ax.set_xlabel(
        r"Commitment  $\pi_{\max} = 1 - H_\Pi$"
        r"  (more committed $\rightarrow$)", fontsize=9)
    ax.set_ylabel(
        r"Support margin  $\delta = \alpha^* - \eta$"
        r"  ($\rightarrow$ better)", fontsize=9)

    # Save WITHOUT bbox_inches='tight' to preserve aspect ratio
    path = os.path.join(FIG_DIR, f"commitment_diagram.{FIG_FORMAT}")
    os.makedirs(FIG_DIR, exist_ok=True)
    with plt.rc_context({'savefig.bbox': 'standard'}):
        fig.savefig(path, facecolor="white", transparent=False,
                    dpi=DPI, pad_inches=0)
    plt.close(fig)
    print(f"Saved: {path}")


# ------------------------------------------------------------------ #
# V4c — Commitment–support-margin, SLGT+ only                          #
# ------------------------------------------------------------------ #

def v4c(data, ap, spec, anchors):
    """V4c: commitment-support-margin, SLGT+ only."""
    fig, ax = plt.subplots(figsize=(5.8, 7.0))
    cm = count_cmap()
    sev = data['obs_idx'] >= SPC_CATEGORIES.index("SLGT")
    means = cat_means(data, spec, mask=sev)

    pi_max = 1.0 - data['H_Pi'][sev]
    delta = data['delta'][sev]

    hb = ax.hexbin(pi_max, delta, gridsize=10, cmap=cm,
                   edgecolors="white", linewidths=0.4, mincnt=1, zorder=2)

    draw_delta0_horiz(ax)

    kw = dict(fontsize=8, fontstyle="italic", color=DARK_GREY,
              alpha=0.2, ha="center", va="center")
    ax.text(0.85, 0.60, "Committed &\nwell-shaped", **kw)
    ax.text(0.15, 0.60, "Cautious &\nwell-shaped", **kw)
    ax.text(0.85, -0.30, "Overconfident\n& wrong", **kw)

    draw_traj_commit(ax, means)
    draw_scenarios_commit(ax, anchors)
    draw_compass(ax, 0.95, 0.72, "better")

    cb = fig.colorbar(hb, ax=ax, shrink=0.55, pad=0.02)
    cb.set_label("Count per bin", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.45, 0.85)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel(
        r"Commitment  $\pi_{\max}$  (more committed $\rightarrow$)",
        fontsize=9)
    ax.set_ylabel(
        r"Support margin  $\delta$  ($\rightarrow$ better)", fontsize=9)
    ax.set_title(
        f"V4c: Commitment–Support Margin  (SLGT+, $n = {sev.sum()}$)",
        fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v4c_severe")


# ------------------------------------------------------------------ #
# V4d — Two-panel: all days vs SLGT+                                   #
# ------------------------------------------------------------------ #

def v4d(data, ap, spec, anchors):
    """V4d: two-panel commitment-support-margin (all vs SLGT+)."""
    sev = data['obs_idx'] >= SPC_CATEGORIES.index("SLGT")
    cm = count_cmap()
    means_all = cat_means(data, spec)
    means_sev = cat_means(data, spec, mask=sev)

    pi_max_all = 1.0 - data['H_Pi']
    delta_all = data['delta']

    fig, (ax_l, ax_r) = plt.subplots(
        1, 2, figsize=(11, 5.5), sharey=True,
        gridspec_kw={"wspace": 0.08, "right": 0.90})

    panels = [
        (ax_l, pi_max_all, delta_all, means_all,
         f"(a)  All days  ($n = {len(spec)}$)", 14),
        (ax_r, pi_max_all[sev], delta_all[sev], means_sev,
         f"(b)  SLGT+  ($n = {sev.sum()}$)", 10),
    ]

    hb = None
    for ax, pm, dl, means, title, gs in panels:
        hb = ax.hexbin(pm, dl, gridsize=gs, cmap=cm,
                       edgecolors="white", linewidths=0.4, mincnt=1,
                       zorder=2)

        ax.axhline(0, color=DARK_GREY, lw=1.0, ls="--", alpha=0.3,
                   zorder=1)

        draw_traj_commit(ax, means, fontsize=6)
        draw_scenarios_commit(ax, anchors, sz=80)

        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.45, 0.85)
        ax.set_xlabel(
            r"$\pi_{\max}$  (committed $\rightarrow$)", fontsize=9)
        ax.set_title(title, fontsize=9, fontweight="bold")

    ax_l.set_ylabel(
        r"$\delta$  (discriminating $\rightarrow$)", fontsize=9)

    cb = fig.colorbar(hb, ax=[ax_l, ax_r], shrink=0.65, pad=0.02)
    cb.set_label("Count per bin", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    fig.suptitle(
        "V4d: Commitment–Support Margin  (All vs Severe)",
        fontsize=10, fontweight="bold", y=1.01)
    fig.tight_layout()
    save_fig(fig, "perf_v4d_two_panel")


# ------------------------------------------------------------------ #
def main():
    apply_style()
    data, ap, spec, anch = get_data()

    for fn in [v3b, v4b, v4c, v4d]:
        name = fn.__doc__ or fn.__name__
        print(f"  {fn.__name__}: {name.strip()}")
        fn(data, ap, spec, anch)

    print(f"\nDone — 4 iterations saved to figures/")


if __name__ == "__main__":
    main()
