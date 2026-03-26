"""Figure 2: Three-scenario comparison.

Side-by-side bar charts for three forecast scenarios (sharp-correct,
hedged-correct, sharp-wrong), all verified against observed = MDT.
Below each panel a text box reports the five-number possibilistic scorecard.
"""
import numpy as np
import matplotlib.pyplot as plt

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)

# ---------------------------------------------------------------------------
# Scenario definitions
# ---------------------------------------------------------------------------
SCENARIOS = {
    "Sharp-Correct": {
        "pi": np.array([0.00, 0.00, 0.05, 0.15, 0.90, 0.10]),
        "obs": "MDT",
    },
    "Hedged-Correct": {
        "pi": np.array([0.10, 0.10, 0.40, 0.55, 0.30, 0.00]),
        "obs": "ENH",
    },
    "Sharp-Wrong": {
        "pi": np.array([0.85, 0.10, 0.05, 0.00, 0.00, 0.00]),
        "obs": "MDT",
    },
}


def compute_scorecard(pi, obs_category):
    """Compute the five-number possibilistic scorecard.

    Parameters
    ----------
    pi : array-like, shape (SPC_N,)
        Raw possibility values for each SPC category.
    obs_category : str
        Observed SPC category label (must be in SPC_CATEGORIES).

    Returns
    -------
    dict with keys: alpha_star, eta, delta, H_Pi, Nc_star
    """
    pi = np.asarray(pi, dtype=float)
    obs_idx = SPC_CATEGORIES.index(obs_category)

    pi_max = pi.max()

    # Normalised distribution pi' = pi / max(pi)
    pi_prime = pi / pi_max

    # alpha* — normalised possibility of the observed category
    alpha_star = pi_prime[obs_idx]

    # eta — mean of the normalised distribution (spread / hedging)
    eta = pi_prime.mean()

    # delta — discrimination = alpha* - eta
    delta = alpha_star - eta

    # H_Pi — hesitancy (sub-normality gap)
    H_Pi = 1.0 - pi_max

    # Nc* — specificity: 1 - max_{w != obs} pi'(w)
    mask = np.ones(SPC_N, dtype=bool)
    mask[obs_idx] = False
    Nc_star = 1.0 - pi_prime[mask].max()

    return dict(alpha_star=alpha_star, eta=eta, delta=delta,
                H_Pi=H_Pi, Nc_star=Nc_star)


def main():
    apply_style()

    fig, axes = plt.subplots(1, 3, figsize=(12.0, 4.5), sharey=True)
    x = np.arange(SPC_N)
    bar_width = 0.55

    for ax, (title, scenario) in zip(axes, SCENARIOS.items()):
        pi = scenario["pi"]
        obs = scenario["obs"]
        obs_idx = SPC_CATEGORIES.index(obs)

        # Bar colours: green for observed, purple for others
        colours = [GREEN if i == obs_idx else PURPLE for i in range(SPC_N)]

        ax.bar(x, pi, width=bar_width, color=colours, edgecolor="white",
               linewidth=0.8, zorder=3)

        # Reference line at 1.0
        ax.axhline(1.0, linestyle=":", linewidth=0.6, color=MID_GREY, zorder=1)

        ax.set_xticks(x)
        ax.set_xticklabels(SPC_CATEGORIES, fontsize=8)
        ax.set_title(title, fontsize=10, fontweight="bold", pad=8)
        ax.set_ylim(0, 1.15)

        # Compute scorecard
        sc = compute_scorecard(pi, obs)

        # Build scorecard text
        lines = (
            r"$\alpha^*$" + f" = {sc['alpha_star']:.3f}\n"
            r"$\eta$" + f" = {sc['eta']:.3f}\n"
            r"$\delta$" + f" = {sc['delta']:.3f}\n"
            r"$H_\Pi$" + f" = {sc['H_Pi']:.3f}\n"
            r"$N_c^*$" + f" = {sc['Nc_star']:.3f}"
        )

        ax.text(
            0.50, -0.22, lines, transform=ax.transAxes,
            fontsize=8, va="top", ha="center",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=MID_GREY, linewidth=0.6),
            family="monospace",
        )

    axes[0].set_ylabel(r"Possibility $\pi(\omega)$")

    fig.tight_layout(rect=[0, 0.08, 1, 1])
    save_fig(fig, "fig2_three_scenario")


if __name__ == "__main__":
    main()
