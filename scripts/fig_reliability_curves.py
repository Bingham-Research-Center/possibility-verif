"""Figure 6: Reliability-style curve for possibilistic specificity.

x-axis: N_c threshold (0 to 1).
y-axis: Conditional hit rate — fraction of forecasts whose N_c exceeds
        the threshold and for which the correct category verified.
A purple curve, a horizontal climatological base-rate line (1/5),
and a diagonal perfect-reliability reference.
"""
import numpy as np
import matplotlib.pyplot as plt

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

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    # Reliability curve
    ax.plot(thresholds, cond_hit, color=PURPLE, linewidth=2.0, marker="o",
            markersize=4, zorder=3, label="Observed hit rate")

    # Climatological base rate
    base = 1.0 / SPC_N
    ax.axhline(base, linestyle="--", linewidth=1.0, color=MID_GREY, zorder=2,
               label=f"Climatology (1/{SPC_N} = {base:.2f})")

    # Perfect reliability diagonal
    ax.plot([0, 1], [0, 1], linestyle=":", linewidth=0.8, color=DARK_GREY,
            zorder=1, label="Perfect reliability")

    ax.set_xlabel(r"$N_c^*$ threshold", fontsize=10)
    ax.set_ylabel("Conditional hit rate", fontsize=10)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1.05)
    ax.legend(loc="lower right", fontsize=8, frameon=True, fancybox=False,
              edgecolor=MID_GREY)

    fig.tight_layout()
    save_fig(fig, "fig6_reliability_curves")


if __name__ == "__main__":
    main()
