"""Performance diagram variants for design comparison.

Generates 8 alternative visualisations of the same synthetic reforecast
data to explore the design space for the possibilistic performance diagram.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.patches import Ellipse
import os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import (
    apply_style, save_fig,
    PURPLE, GREEN, DARK_GREY, MID_GREY, LIGHT_GREY,
    SPC_CATEGORIES, SPC_N,
)
from fig_three_scenario import compute_scorecard, SCENARIOS
from fig_performance_diagram import generate_reforecast

try:
    from scipy.stats import gaussian_kde
    HAS_KDE = True
except ImportError:
    HAS_KDE = False

MISS_RED = "#C0392B"

# ------------------------------------------------------------------ #
# Shared data & helpers                                                #
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


def make_cmap():
    cm = LinearSegmentedColormap.from_list(
        "hpi", [PURPLE, "#C9A5E0", "#F0E4F7"], N=256)
    return cm, Normalize(0.0, 0.65)


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
                        fontsize=5, color=color, alpha=min(alpha + 0.2, 0.55),
                        ha="center", va="bottom")


def draw_delta0(ax):
    x = np.linspace(-0.05, 1.05, 50)
    ax.plot(x, 1 - x, lw=1.2, ls="--", color=DARK_GREY, alpha=0.3, zorder=1)
    ax.text(0.20, 0.82, r"$\delta\!=\!0$", fontsize=7, color=DARK_GREY,
            alpha=0.4, rotation=-45, ha="center")


def draw_compass(ax, x=0.95, y=0.95, text="better"):
    ax.annotate("", xy=(x, y), xytext=(x - 0.12, y - 0.12),
                arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.5),
                zorder=10)
    ax.text(x - 0.06, y + 0.025, text, fontsize=7, fontweight="bold",
            color=PURPLE, ha="center", va="bottom", zorder=10)


def draw_anchors(ax, anchors, cm, nm, sz=100, offsets=None):
    if offsets is None:
        offsets = {"A": (0.07, -0.06), "B": (0.07, -0.06), "C": (0.07, 0.05)}
    for ltr, c, v in anchors:
        sx, sy = 1 - c['eta'], c['alpha_star']
        edge = GREEN if v else MISS_RED
        ax.scatter(sx, sy, s=sz, c=[c['H_Pi']], cmap=cm, norm=nm,
                   edgecolors=edge, linewidths=1.5, marker="*", zorder=8)
        ox, oy = offsets.get(ltr, (0.07, -0.06))
        ax.annotate(ltr, xy=(sx, sy), xytext=(sx + ox, sy + oy),
                    fontsize=8, fontweight="bold", color=DARK_GREY,
                    arrowprops=dict(arrowstyle="->", color=MID_GREY, lw=0.5),
                    zorder=9)


def std_axes(ax):
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.04, 1.04)
    ax.set_xlabel(r"Specificity  $1\!-\!\eta$  (sharper $\rightarrow$)", fontsize=9)
    ax.set_ylabel(r"Depth-of-truth  $\alpha^*$  (more truthful $\rightarrow$)", fontsize=9)


def cat_means(data, spec):
    r = {}
    for ci, cat in enumerate(SPC_CATEGORIES):
        m = data['obs_idx'] == ci
        n = m.sum()
        if n == 0:
            continue
        r[cat] = dict(
            x=spec[m].mean(), y=data['alpha_star'][m].mean(),
            h=data['H_Pi'][m].mean(),
            sx=spec[m].std(), sy=data['alpha_star'][m].std(),
            n=n,
        )
    return r


def quadrant_labels(ax, alpha=0.2):
    kw = dict(fontsize=8, fontstyle="italic", color=DARK_GREY,
              alpha=alpha, ha="center", va="center")
    ax.text(0.82, 0.95, "Sharp\ncorrect", **kw)
    ax.text(0.12, 0.95, "Diffuse\ncorrect", **kw)
    ax.text(0.82, 0.08, "Sharp\nwrong", **kw)
    ax.text(0.12, 0.30, "Diffuse\nwrong", **kw)


# ------------------------------------------------------------------ #
# Variant 1: Hexbin + skill hyperbolas (SLGT+)                        #
# ------------------------------------------------------------------ #

def v1(data, ap, spec, anchors):
    """Hexbin + skill hyperbolas (SLGT+)."""
    fig, ax = plt.subplots(figsize=(5.5, 5))
    cm, nm = make_cmap()
    sev = data['obs_idx'] >= SPC_CATEGORIES.index("SLGT")

    draw_hyperbolas(ax)
    draw_delta0(ax)

    hb = ax.hexbin(spec[sev], ap[sev], C=data['H_Pi'][sev],
                   reduce_C_function=np.mean, gridsize=20, cmap=cm,
                   edgecolors="white", linewidths=0.3, mincnt=1, zorder=2)

    draw_anchors(ax, anchors, cm, nm, sz=120)
    draw_compass(ax)
    quadrant_labels(ax)

    cb = fig.colorbar(hb, ax=ax, shrink=0.7, pad=0.02)
    cb.set_label(r"Mean $H_\Pi$  (dark = confident)", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    # Anchor legend
    h_v = mlines.Line2D([], [], marker="*", ls="None", ms=8,
                        mfc=MID_GREY, mec=GREEN, mew=1.2, label="Anchor (hit)")
    h_m = mlines.Line2D([], [], marker="*", ls="None", ms=8,
                        mfc=MID_GREY, mec=MISS_RED, mew=1.2, label="Anchor (miss)")
    ax.legend(handles=[h_v, h_m], loc="lower left", fontsize=7,
              frameon=True, fancybox=False, edgecolor=MID_GREY)

    std_axes(ax)
    ax.set_title(f"V1: Hexbin + Skill Hyperbolas  (SLGT+, $n = {sev.sum()}$)",
                 fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v1_hexbin")


# ------------------------------------------------------------------ #
# Variant 2: Category-mean trajectory                                  #
# ------------------------------------------------------------------ #

def v2(data, ap, spec, anchors):
    """Category-mean skill trajectory."""
    fig, ax = plt.subplots(figsize=(5.5, 5))
    cm, nm = make_cmap()
    means = cat_means(data, spec)
    cats = [c for c in SPC_CATEGORIES if c in means]

    draw_hyperbolas(ax)
    draw_delta0(ax)
    draw_compass(ax)

    xs = [means[c]['x'] for c in cats]
    ys = [means[c]['y'] for c in cats]
    hs = [means[c]['h'] for c in cats]
    ns = [means[c]['n'] for c in cats]

    # Error ellipses (±1σ)
    for c in cats:
        m = means[c]
        ell = Ellipse((m['x'], m['y']), m['sx'] * 2, m['sy'] * 2,
                      fc=cm(nm(m['h'])), alpha=0.12,
                      ec=cm(nm(m['h'])), lw=0.8, zorder=2)
        ax.add_patch(ell)

    # Line + halo
    ax.plot(xs, ys, '-', color="white", lw=5, zorder=3)
    ax.plot(xs, ys, '-', color=DARK_GREY, lw=1.8, alpha=0.5, zorder=4)

    # Points (sized by n)
    s_min, s_max = 50, 350
    sizes = [s_min + (s_max - s_min) * (n / max(ns)) for n in ns]
    sc = ax.scatter(xs, ys, s=sizes, c=hs, cmap=cm, norm=nm,
                    edgecolors=DARK_GREY, linewidths=1.2, zorder=5)

    # Labels
    label_ha = ["right", "left", "left", "left", "right", "left"]
    label_ox = [-0.05, 0.05, 0.05, 0.05, -0.05, 0.05]
    label_oy = [0.0, -0.04, 0.03, -0.04, 0.03, 0.03]
    for i, c in enumerate(cats):
        ha = label_ha[i] if i < len(label_ha) else "left"
        ox = label_ox[i] if i < len(label_ox) else 0.05
        oy = label_oy[i] if i < len(label_oy) else 0.0
        ax.text(xs[i] + ox, ys[i] + oy,
                f"{c}\n$n$={ns[i]}", fontsize=6.5, fontweight="bold",
                color=DARK_GREY, ha=ha, va="center", zorder=6,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="none", alpha=0.8))

    draw_anchors(ax, anchors, cm, nm, sz=90,
                 offsets={"A": (-0.07, 0.05), "B": (-0.07, 0.05), "C": (0.07, 0.05)})

    cb = fig.colorbar(sc, ax=ax, shrink=0.7, pad=0.02)
    cb.set_label(r"Mean $H_\Pi$", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    std_axes(ax)
    ax.set_title("V2: Category-Mean Skill Trajectory",
                 fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v2_trajectory")


# ------------------------------------------------------------------ #
# Variant 3: Hexbin + trajectory hybrid                                #
# ------------------------------------------------------------------ #

def v3(data, ap, spec, anchors):
    """Hexbin cloud + trajectory overlay (all days)."""
    fig, ax = plt.subplots(figsize=(5.5, 5))
    cm, nm = make_cmap()
    means = cat_means(data, spec)
    cats = [c for c in SPC_CATEGORIES if c in means]

    draw_hyperbolas(ax, label=False)
    draw_delta0(ax)
    draw_compass(ax)

    # Light hexbin (all days)
    hb = ax.hexbin(spec, ap, C=data['H_Pi'], reduce_C_function=np.mean,
                   gridsize=18, cmap=cm, edgecolors="white", linewidths=0.2,
                   mincnt=1, alpha=0.35, zorder=1)

    # Trajectory
    xs = [means[c]['x'] for c in cats]
    ys = [means[c]['y'] for c in cats]
    hs = [means[c]['h'] for c in cats]

    ax.plot(xs, ys, '-', color="white", lw=5, zorder=4)
    ax.plot(xs, ys, '-', color=DARK_GREY, lw=2, zorder=5)
    ax.scatter(xs, ys, s=100, c=hs, cmap=cm, norm=nm,
               edgecolors="white", linewidths=2.5, zorder=6)
    ax.scatter(xs, ys, s=100, c=hs, cmap=cm, norm=nm,
               edgecolors=DARK_GREY, linewidths=0.8, zorder=7)

    # Labels
    for i, c in enumerate(cats):
        side = "right" if i % 2 == 0 else "left"
        ox = 0.05 if side == "right" else -0.05
        ax.text(xs[i] + ox, ys[i], c, fontsize=7, fontweight="bold",
                color=DARK_GREY, ha="left" if side == "right" else "right",
                va="center", zorder=8,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

    draw_anchors(ax, anchors, cm, nm, sz=90)

    cb = fig.colorbar(hb, ax=ax, shrink=0.7, pad=0.02)
    cb.set_label(r"Mean $H_\Pi$", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    std_axes(ax)
    ax.set_title(f"V3: Hexbin Cloud + Trajectory  (all, $n = {len(spec)}$)",
                 fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v3_hybrid")


# ------------------------------------------------------------------ #
# Variant 4: Commitment–discrimination plane                          #
# ------------------------------------------------------------------ #

def v4(data, ap, spec, anchors):
    """Commitment (pi_max) vs discrimination (delta)."""
    fig, ax = plt.subplots(figsize=(5.5, 5))
    cm_count = LinearSegmentedColormap.from_list(
        "cnt", ["#F0E4F7", "#C9A5E0", PURPLE], N=256)

    pi_max = 1.0 - data['H_Pi']
    delta = data['delta']

    hb = ax.hexbin(pi_max, delta, gridsize=22, cmap=cm_count,
                   edgecolors="white", linewidths=0.3, mincnt=1, zorder=2)

    # Break-even line
    ax.axhline(0, color=DARK_GREY, lw=1.2, ls="--", alpha=0.35, zorder=1)
    ax.text(0.04, 0.015, r"$\delta = 0$  (break-even)", fontsize=7,
            color=DARK_GREY, alpha=0.55, va="bottom")

    # Region labels
    kw = dict(fontsize=8, fontstyle="italic", color=DARK_GREY,
              alpha=0.2, ha="center", va="center")
    ax.text(0.85, 0.40, "Committed &\ndiscriminating", **kw)
    ax.text(0.20, 0.40, "Cautious &\ndiscriminating", **kw)
    ax.text(0.85, -0.30, "Overconfident\n& wrong", **kw)
    ax.text(0.20, -0.30, "Uninformative", **kw)

    # Anchors
    for ltr, c, v in anchors:
        sx = 1 - c['H_Pi']
        sy = c['delta']
        edge = GREEN if v else MISS_RED
        ax.scatter(sx, sy, s=140, marker="*", fc=PURPLE,
                   ec=edge, linewidths=1.5, zorder=8)
        ax.annotate(ltr, xy=(sx, sy), xytext=(sx + 0.06, sy + 0.04),
                    fontsize=8, fontweight="bold", color=DARK_GREY,
                    arrowprops=dict(arrowstyle="->", color=MID_GREY, lw=0.5),
                    zorder=9)

    # Compass
    ax.annotate("", xy=(0.95, 0.52), xytext=(0.83, 0.40),
                arrowprops=dict(arrowstyle="->", color=PURPLE, lw=1.5), zorder=10)
    ax.text(0.89, 0.54, "better", fontsize=7, fontweight="bold",
            color=PURPLE, ha="center", va="bottom", zorder=10)

    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.55, 0.65)
    ax.set_xlabel(r"Commitment  $\pi_{\max} = 1 - H_\Pi$  (more committed $\rightarrow$)",
                  fontsize=9)
    ax.set_ylabel(r"Discrimination  $\delta = \alpha^* - \eta$  ($\rightarrow$ better)",
                  fontsize=9)

    cb = fig.colorbar(hb, ax=ax, shrink=0.7, pad=0.02)
    cb.set_label("Count per bin", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    ax.set_title("V4: Commitment–Discrimination Plane",
                 fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v4_commitment")


# ------------------------------------------------------------------ #
# Variant 5: KDE jointplot with marginals                              #
# ------------------------------------------------------------------ #

def v5(data, ap, spec, anchors):
    """KDE jointplot with marginal histograms (SLGT+)."""
    cm, nm = make_cmap()
    sev = data['obs_idx'] >= SPC_CATEGORIES.index("SLGT")
    x, y = spec[sev], ap[sev]

    fig = plt.figure(figsize=(6, 6))
    gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4],
                          wspace=0.05, hspace=0.05)
    ax = fig.add_subplot(gs[1, 0])
    ax_top = fig.add_subplot(gs[0, 0], sharex=ax)
    ax_rt = fig.add_subplot(gs[1, 1], sharey=ax)
    fig.add_subplot(gs[0, 1]).axis("off")

    # Main panel
    if HAS_KDE and len(x) > 10:
        xy = np.vstack([x, y])
        kde = gaussian_kde(xy, bw_method=0.25)
        xg = np.linspace(-0.02, 1.02, 100)
        yg = np.linspace(-0.04, 1.04, 100)
        X, Y = np.meshgrid(xg, yg)
        Z = kde(np.vstack([X.ravel(), Y.ravel()])).reshape(X.shape)
        ax.contourf(X, Y, Z, levels=8, cmap=cm, alpha=0.45, zorder=1)
        ax.contour(X, Y, Z, levels=8, colors=PURPLE, linewidths=0.4,
                   alpha=0.35, zorder=2)
    else:
        ax.scatter(x, y, s=15, c=data['H_Pi'][sev], cmap=cm, norm=nm,
                   alpha=0.4, edgecolors="none", zorder=2)

    draw_hyperbolas(ax, alpha=0.15, label=False)
    draw_delta0(ax)
    draw_compass(ax)
    draw_anchors(ax, anchors, cm, nm, sz=110)

    # Marginals
    ax_top.hist(x, bins=25, color=PURPLE, alpha=0.35, edgecolor="white", lw=0.3)
    ax_top.set_ylabel("n", fontsize=7)
    ax_top.tick_params(labelbottom=False, labelsize=7)
    for sp in ("top", "right"):
        ax_top.spines[sp].set_visible(False)

    ax_rt.hist(y, bins=25, orientation="horizontal", color=PURPLE,
               alpha=0.35, edgecolor="white", lw=0.3)
    ax_rt.set_xlabel("n", fontsize=7)
    ax_rt.tick_params(labelleft=False, labelsize=7)
    for sp in ("top", "right"):
        ax_rt.spines[sp].set_visible(False)

    std_axes(ax)
    fig.suptitle(f"V5: KDE Jointplot with Marginals  (SLGT+, $n = {sev.sum()}$)",
                 fontsize=9, fontweight="bold", y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    save_fig(fig, "perf_v5_kde_marginals")


# ------------------------------------------------------------------ #
# Variant 6: Hexbin with inset blowup                                 #
# ------------------------------------------------------------------ #

def v6(data, ap, spec, anchors):
    """Hexbin all-days with inset blowup of SLGT+ cluster."""
    fig, ax = plt.subplots(figsize=(6, 5.5))
    cm, nm = make_cmap()
    sev = data['obs_idx'] >= SPC_CATEGORIES.index("SLGT")

    draw_hyperbolas(ax, label=False)
    draw_delta0(ax)
    draw_compass(ax)

    hb = ax.hexbin(spec, ap, C=data['H_Pi'], reduce_C_function=np.mean,
                   gridsize=22, cmap=cm, edgecolors="white", linewidths=0.2,
                   mincnt=1, zorder=2)

    draw_anchors(ax, anchors, cm, nm, sz=110)
    std_axes(ax)

    cb = fig.colorbar(hb, ax=ax, shrink=0.65, pad=0.02)
    cb.set_label(r"Mean $H_\Pi$", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    # Inset: SLGT+ only (placed in lower-left dead space)
    ax_in = ax.inset_axes([0.04, 0.04, 0.42, 0.38])
    ax_in.hexbin(spec[sev], ap[sev], C=data['H_Pi'][sev],
                 reduce_C_function=np.mean, gridsize=14, cmap=cm,
                 edgecolors="white", linewidths=0.2, mincnt=1, zorder=2)
    draw_hyperbolas(ax_in, levels=[0.2, 0.4, 0.6], alpha=0.15, label=False)

    for ltr, c, v in anchors:
        sx, sy = 1 - c['eta'], c['alpha_star']
        edge = GREEN if v else MISS_RED
        ax_in.scatter(sx, sy, s=50, c=[c['H_Pi']], cmap=cm, norm=nm,
                      ec=edge, linewidths=1.0, marker="*", zorder=8)
        ax_in.text(sx + 0.04, sy, ltr, fontsize=6, fontweight="bold",
                   color=DARK_GREY, zorder=9)

    ax_in.set_xlim(-0.02, 0.85)
    ax_in.set_ylim(-0.04, 1.04)
    ax_in.set_title(f"SLGT+ ($n = {sev.sum()}$)", fontsize=7, fontweight="bold")
    ax_in.tick_params(labelsize=5)
    ax_in.set_facecolor("#FAFAFA")
    for sp in ax_in.spines.values():
        sp.set_edgecolor(PURPLE)
        sp.set_linewidth(1.0)

    ax.set_title(f"V6: Hexbin + Inset Blowup  (all, $n = {len(spec)}$)",
                 fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v6_inset")


# ------------------------------------------------------------------ #
# Variant 7: Annotated trajectory (maximum walkthrough)                #
# ------------------------------------------------------------------ #

def v7(data, ap, spec, anchors):
    """Annotated skill trajectory (maximum walkthrough, recommended)."""
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    cm, nm = make_cmap()
    means = cat_means(data, spec)
    cats = [c for c in SPC_CATEGORIES if c in means]

    # Soft region shading
    ax.fill_between([0.45, 1.02], 0.45, 1.04, color=GREEN, alpha=0.03, zorder=0)
    ax.fill_between([0.45, 1.02], -0.04, 0.45, color=MISS_RED, alpha=0.03, zorder=0)

    draw_hyperbolas(ax, levels=[0.2, 0.4, 0.6, 0.8], alpha=0.3, label=True)
    draw_delta0(ax)

    xs = [means[c]['x'] for c in cats]
    ys = [means[c]['y'] for c in cats]
    hs = [means[c]['h'] for c in cats]
    ns = [means[c]['n'] for c in cats]

    # Error bars
    for i, c in enumerate(cats):
        m = means[c]
        ax.errorbar(m['x'], m['y'], xerr=m['sx'], yerr=m['sy'],
                    fmt='none', ecolor=MID_GREY, elinewidth=0.7,
                    capsize=3, capthick=0.7, alpha=0.45, zorder=3)

    # Line + halo
    ax.plot(xs, ys, '-', color="white", lw=6, zorder=4)
    ax.plot(xs, ys, '-', color=DARK_GREY, lw=2.2, alpha=0.55, zorder=5)

    # Points (sized by n)
    s_min, s_max = 60, 400
    sizes = [s_min + (s_max - s_min) * (n / max(ns)) for n in ns]
    sc = ax.scatter(xs, ys, s=sizes, c=hs, cmap=cm, norm=nm,
                    edgecolors=DARK_GREY, linewidths=1.5, zorder=6)

    # Labels (alternating sides with boxes)
    label_cfg = {
        "NONE":  ("right",  0.05,  0.00),
        "MRGL":  ("left",  -0.05, -0.04),
        "SLGT":  ("right",  0.05,  0.02),
        "ENH":   ("left",  -0.05, -0.03),
        "MDT":   ("right",  0.06,  0.00),
        "HIGH":  ("left",  -0.06,  0.02),
    }
    for i, c in enumerate(cats):
        ha, ox, oy = label_cfg.get(c, ("right", 0.05, 0.0))
        ax.annotate(
            f"{c}  ($n$={ns[i]})", xy=(xs[i], ys[i]),
            xytext=(xs[i] + ox, ys[i] + oy),
            fontsize=7, fontweight="bold", color=DARK_GREY, ha=ha,
            arrowprops=dict(arrowstyle="-", color=MID_GREY, lw=0.5),
            bbox=dict(boxstyle="round,pad=0.25", fc="white",
                      ec=MID_GREY, alpha=0.85, lw=0.5),
            zorder=7)

    # Compass with gloss
    ax.annotate("", xy=(0.97, 0.97), xytext=(0.82, 0.82),
                arrowprops=dict(arrowstyle="->,head_width=0.35",
                                color=PURPLE, lw=2),
                zorder=10)
    ax.text(0.895, 0.99, "sharp + truthful", fontsize=6.5, fontweight="bold",
            color=PURPLE, ha="center", va="bottom", zorder=10)

    # Walkthrough box (lower-left)
    walkthrough = (
        "Read: follow the line from NONE (easy, top-right)\n"
        "to HIGH (rare, lower-left). Each dot is the mean\n"
        "forecast quality for that observed category.\n"
        "Dot size $\\propto$ sample count.  Darker = confident.\n"
        "Hyperbolas: equal-skill $S = \\alpha^{*} \\times (1\\!-\\!\\eta)$.\n"
        "Dashed line: $\\delta = 0$ break-even."
    )
    ax.text(0.03, 0.03, walkthrough, fontsize=6, color=DARK_GREY,
            va="bottom", ha="left", transform=ax.transAxes, linespacing=1.5,
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec=MID_GREY,
                      alpha=0.88, lw=0.5))

    # Anchors
    draw_anchors(ax, anchors, cm, nm, sz=90,
                 offsets={"A": (-0.06, 0.05), "B": (-0.06, 0.05), "C": (0.06, 0.05)})

    # Legend
    h_v = mlines.Line2D([], [], marker="*", ls="None", ms=8,
                        mfc=MID_GREY, mec=GREEN, mew=1.2, label="§6 anchor (hit)")
    h_m = mlines.Line2D([], [], marker="*", ls="None", ms=8,
                        mfc=MID_GREY, mec=MISS_RED, mew=1.2, label="§6 anchor (miss)")
    ax.legend(handles=[h_v, h_m], loc="upper left", fontsize=7,
              frameon=True, fancybox=False, edgecolor=MID_GREY)

    # Colorbar
    cb = fig.colorbar(sc, ax=ax, shrink=0.65, pad=0.02)
    cb.set_label(r"Mean $H_\Pi$  (dark = confident)", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    std_axes(ax)
    ax.set_title("V7: Annotated Skill Trajectory",
                 fontsize=9, fontweight="bold", pad=8)
    fig.tight_layout()
    save_fig(fig, "perf_v7_annotated")


# ------------------------------------------------------------------ #
# Variant 8: Small multiples (one panel per observed category)         #
# ------------------------------------------------------------------ #

def v8(data, ap, spec, anchors):
    """Small multiples: one panel per observed SPC category."""
    cm, nm = make_cmap()
    fig, axes = plt.subplots(2, 3, figsize=(9, 6), sharex=True, sharey=True)
    axes = axes.ravel()

    for ci, (cat, ax) in enumerate(zip(SPC_CATEGORIES, axes)):
        mask = data['obs_idx'] == ci
        n = mask.sum()

        draw_hyperbolas(ax, levels=[0.3, 0.6, 0.9], alpha=0.15, label=False)
        draw_delta0(ax)

        if n > 0:
            ax.scatter(spec[mask], ap[mask], s=12,
                       c=data['H_Pi'][mask], cmap=cm, norm=nm,
                       alpha=0.5, edgecolors="none", zorder=2)

            # Mean marker
            mx, my = spec[mask].mean(), ap[mask].mean()
            ax.scatter(mx, my, s=120, c=[data['H_Pi'][mask].mean()],
                       cmap=cm, norm=nm, edgecolors=DARK_GREY,
                       linewidths=1.5, marker="D", zorder=5)

        ax.set_xlim(-0.02, 1.02)
        ax.set_ylim(-0.04, 1.04)
        ax.set_title(f"{cat}  ($n = {n}$)", fontsize=8, fontweight="bold")
        ax.tick_params(labelsize=6)

        if ci >= 3:
            ax.set_xlabel(r"$1\!-\!\eta$", fontsize=8)
        if ci % 3 == 0:
            ax.set_ylabel(r"$\alpha^*$", fontsize=8)

    # Shared colorbar
    sm = plt.cm.ScalarMappable(cmap=cm, norm=nm)
    sm.set_array([])
    cb = fig.colorbar(sm, ax=axes.tolist(), shrink=0.6, pad=0.02)
    cb.set_label(r"$H_\Pi$", fontsize=8)
    cb.ax.tick_params(labelsize=7)

    fig.suptitle("V8: Small Multiples by Observed Category",
                 fontsize=10, fontweight="bold", y=1.01)
    fig.tight_layout()
    save_fig(fig, "perf_v8_small_multiples")


# ------------------------------------------------------------------ #
# Main                                                                 #
# ------------------------------------------------------------------ #

def main():
    apply_style()
    data, ap, spec, anch = get_data()

    variants = [v1, v2, v3, v4, v5, v6, v7, v8]
    for fn in variants:
        name = fn.__doc__ or fn.__name__
        print(f"  {fn.__name__}: {name.strip()}")
        fn(data, ap, spec, anch)

    print(f"\nDone — {len(variants)} variants saved to figures/")


if __name__ == "__main__":
    main()
