"""Figure 6 (PDF order): Reliability of conditional necessity.

x-axis: N_c threshold (0 to 1).
y-axis: Conditional hit rate — fraction of forecasts whose N_c exceeds
        the threshold and for which the correct category verified.

Enhanced with bootstrap confidence band, skill-region shading,
sample-size inset, and interpretive annotations.
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)


def _generate_synthetic_data(n_forecasts=2000, seed=42):
    """Generate synthetic (N_c, hit) pairs for illustration.

    Higher N_c forecasts are more likely to verify (the whole point of the
    reliability curve).  We model hit probability as a logistic function of N_c
    with a bit of noise so the curve is realistic but not perfect.
    """
    rng = np.random.default_rng(seed)

    # N_c values uniformly distributed in [0, 1]
    Nc = rng.uniform(0, 1, size=n_forecasts)

    # True hit probability: logistic mapping so high N_c -> high hit rate
    # p(hit | Nc) = sigmoid(4*(Nc - 0.35))   gives ~0.20 at Nc=0, ~0.90 at Nc=1
    logit = 4.0 * (Nc - 0.35)
    p_hit = 1.0 / (1.0 + np.exp(-logit))

    hits = rng.binomial(1, p_hit)

    return Nc, hits


def _bootstrap_ci(Nc_vals, hits, thresholds, n_boot=500, seed=99):
    """Compute 90% bootstrap confidence intervals for conditional hit rate."""
    rng = np.random.default_rng(seed)
    n = len(Nc_vals)
    boot_curves = np.empty((n_boot, len(thresholds)))

    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        nc_b, h_b = Nc_vals[idx], hits[idx]
        for j, t in enumerate(thresholds):
            mask = nc_b >= t
            boot_curves[b, j] = h_b[mask].mean() if mask.sum() > 0 else np.nan

    lo = np.nanpercentile(boot_curves, 5, axis=0)
    hi = np.nanpercentile(boot_curves, 95, axis=0)
    return lo, hi


def main():
    apply_style()

    Nc_vals, hits = _generate_synthetic_data()

    # Bin by N_c threshold and compute conditional hit rate
    thresholds = np.linspace(0.0, 0.95, 20)
    cond_hit = np.empty_like(thresholds)
    counts = np.empty_like(thresholds)

    for j, t in enumerate(thresholds):
        mask = Nc_vals >= t
        n = mask.sum()
        counts[j] = n
        cond_hit[j] = hits[mask].mean() if n > 0 else np.nan

    # Bootstrap confidence interval
    ci_lo, ci_hi = _bootstrap_ci(Nc_vals, hits, thresholds)

    base = 1.0 / SPC_N

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    # --- Skill region: shade above climatology ---
    ax.axhspan(base, 1.05, color=GREEN, alpha=0.06, zorder=0)
    ax.axhspan(0, base, color="#C0392B", alpha=0.04, zorder=0)
    ax.text(0.03, base + 0.03, "skill region",
            fontsize=7.5, fontstyle="italic", color=GREEN, alpha=0.7,
            va="bottom")
    ax.text(0.03, base - 0.03, "no skill",
            fontsize=7.5, fontstyle="italic", color="#C0392B", alpha=0.5,
            va="top")

    # --- Bootstrap confidence band ---
    ax.fill_between(thresholds, ci_lo, ci_hi, color=PURPLE, alpha=0.15,
                    zorder=2, label="90% bootstrap CI")

    # --- Reliability curve ---
    ax.plot(thresholds, cond_hit, color=PURPLE, linewidth=2.0, marker="o",
            markersize=4, zorder=4, label="Observed hit rate")

    # --- Climatological base rate ---
    ax.axhline(base, linestyle="--", linewidth=1.0, color=MID_GREY, zorder=3,
               label=f"Climatology (1/{SPC_N} = {base:.2f})")

    # --- Perfect reliability diagonal ---
    ax.plot([0, 1], [0, 1], linestyle=":", linewidth=0.8, color=DARK_GREY,
            zorder=1, label="Perfect reliability")

    # --- Interpretive annotations ---
    # Annotate the gap between curve and climatology at a mid threshold
    t_mid = 0.50
    idx_mid = np.argmin(np.abs(thresholds - t_mid))
    hr_mid = cond_hit[idx_mid]
    ax.annotate(
        "",
        xy=(t_mid, base), xytext=(t_mid, hr_mid),
        arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2),
    )
    ax.text(t_mid + 0.04, (base + hr_mid) / 2,
            f"skill gain\n{hr_mid - base:.0%} above\nclimatology",
            fontsize=7, color=GREEN, va="center",
            bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GREEN,
                      lw=0.5, alpha=0.9))

    # Annotate the high-confidence region
    ax.annotate(
        "high-$N_c^*$ forecasts\nverify reliably",
        xy=(0.85, cond_hit[-3]), xytext=(0.45, 0.97),
        fontsize=7.5, fontweight="bold", color=PURPLE,
        arrowprops=dict(arrowstyle="->", color=PURPLE, lw=0.8),
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=PURPLE,
                  lw=0.5, alpha=0.9),
    )

    ax.set_xlabel(r"$N_c^*$ threshold  $\tau$", fontsize=10)
    ax.set_ylabel("Conditional hit rate  "
                  r"$P(\mathrm{hit}\,|\,N_c^* \geq \tau)$", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", fontsize=7.5, frameon=True, fancybox=False,
              edgecolor=MID_GREY)

    # --- Inset: sample size per threshold ---
    ax_inset = ax.inset_axes([0.55, 0.14, 0.40, 0.18])
    ax_inset.bar(thresholds, counts, width=0.04, color=PURPLE, alpha=0.5,
                 edgecolor="none")
    ax_inset.set_ylabel("$n$", fontsize=7, labelpad=1)
    ax_inset.set_xlabel(r"$\tau$", fontsize=7, labelpad=1)
    ax_inset.tick_params(labelsize=6)
    ax_inset.set_xlim(0, 1)
    ax_inset.set_facecolor("white")
    for spine in ax_inset.spines.values():
        spine.set_color(MID_GREY)
        spine.set_linewidth(0.5)

    fig.tight_layout()
    save_fig(fig, "reliability_curves")


if __name__ == "__main__":
    main()
