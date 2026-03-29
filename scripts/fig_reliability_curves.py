"""Figure 6 (PDF order): Reliability of conditional necessity.

x-axis: N_c threshold (0 to 1).
y-axis: Conditional hit rate — among forecasts where the mode's N_c
        exceeds the threshold, what fraction verified correctly?

Uses the shared synthetic reforecast from fig_performance_diagram.py.
N_c is evaluated at the *predicted* (mode) category, not the observed
one — this tests whether high N_c of the system's top pick is a
reliable confidence signal.
"""
import numpy as np
import matplotlib.pyplot as plt

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
    SPC_CATEGORIES, SPC_N,
)
from fig_performance_diagram import generate_reforecast


def _bootstrap_ci(nc_mode, hits, thresholds, n_boot=500, seed=99):
    """Compute 90% bootstrap confidence intervals for conditional hit rate."""
    rng = np.random.default_rng(seed)
    n = len(nc_mode)
    boot_curves = np.empty((n_boot, len(thresholds)))

    for b in range(n_boot):
        idx = rng.choice(n, size=n, replace=True)
        nc_b, h_b = nc_mode[idx], hits[idx]
        for j, t in enumerate(thresholds):
            mask = nc_b >= t
            boot_curves[b, j] = h_b[mask].mean() if mask.sum() > 0 else np.nan

    lo = np.nanpercentile(boot_curves, 5, axis=0)
    hi = np.nanpercentile(boot_curves, 95, axis=0)
    return lo, hi


def main():
    apply_style()

    # --- Use shared reforecast data ---
    data = generate_reforecast()
    pi_array = data['pi_array']
    obs_idx = data['obs_idx']
    n = len(obs_idx)

    # Compute N_c of the MODE (predicted) category — not N_c*
    # N_c(mode) = 1 - max_{w != mode} pi'(w)
    mode_idx = pi_array.argmax(axis=1)
    nc_mode = np.empty(n)
    for i in range(n):
        pi = pi_array[i]
        pi_prime = pi / pi.max()
        mask = np.ones(SPC_N, dtype=bool)
        mask[mode_idx[i]] = False
        nc_mode[i] = max(0.0, 1.0 - pi_prime[mask].max())

    hits = (mode_idx == obs_idx).astype(float)

    # Bin by N_c threshold and compute conditional hit rate
    thresholds = np.linspace(0.0, 0.95, 20)
    cond_hit = np.empty_like(thresholds)
    counts = np.empty_like(thresholds)

    for j, t in enumerate(thresholds):
        mask = nc_mode >= t
        cnt = mask.sum()
        counts[j] = cnt
        cond_hit[j] = hits[mask].mean() if cnt > 0 else np.nan

    # Bootstrap confidence interval
    ci_lo, ci_hi = _bootstrap_ci(nc_mode, hits, thresholds)

    random_base = 1.0 / SPC_N
    uncond_acc = hits.mean()  # system's unconditional mode accuracy

    fig, ax = plt.subplots(figsize=(5.5, 4.5))

    # --- Skill region: shade above unconditional accuracy ---
    ax.axhspan(uncond_acc, 1.05, color=GREEN, alpha=0.06, zorder=0)
    ax.text(0.03, uncond_acc + 0.015, "above system average",
            fontsize=7.5, fontstyle="italic", color=GREEN, alpha=0.7,
            va="bottom")

    # --- Bootstrap confidence band ---
    ax.fill_between(thresholds, ci_lo, ci_hi, color=PURPLE, alpha=0.15,
                    zorder=2, label="90% bootstrap CI")

    # --- Reliability curve ---
    ax.plot(thresholds, cond_hit, color=PURPLE, linewidth=2.0, marker="o",
            markersize=4, zorder=4, label="Conditional hit rate")

    # --- Baselines ---
    ax.axhline(random_base, linestyle="--", linewidth=1.0, color=MID_GREY,
               zorder=3, label=f"Random chance ($1/K = {random_base:.2f}$)")
    ax.axhline(uncond_acc, linestyle="-.", linewidth=1.0, color=DARK_GREY,
               zorder=3, label=f"System average ({uncond_acc:.2f})")

    # --- Interpretive annotation: gain over system average ---
    t_ann = 0.70
    idx_ann = np.argmin(np.abs(thresholds - t_ann))
    hr_ann = cond_hit[idx_ann]
    if not np.isnan(hr_ann) and hr_ann > uncond_acc:
        ax.annotate(
            "",
            xy=(t_ann, uncond_acc), xytext=(t_ann, hr_ann),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.2),
        )
        gain_pp = hr_ann - uncond_acc
        ax.text(t_ann + 0.04, (uncond_acc + hr_ann) / 2,
                f"+{gain_pp:.0%} pts\nabove system\naverage",
                fontsize=7, color=GREEN, va="center",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec=GREEN,
                          lw=0.5, alpha=0.9))

    # Annotate the high-confidence region
    valid_high = [i for i, c in enumerate(counts) if c >= 10]
    if valid_high:
        last_valid = valid_high[-1]
        ax.annotate(
            "high-$N_c$ forecasts\nverify reliably",
            xy=(thresholds[last_valid], cond_hit[last_valid]),
            xytext=(0.25, 0.97),
            fontsize=7.5, fontweight="bold", color=PURPLE,
            arrowprops=dict(arrowstyle="->", color=PURPLE, lw=0.8),
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=PURPLE,
                      lw=0.5, alpha=0.9),
        )

    ax.set_xlabel(r"$N_c(\hat{c})$ threshold  $\tau$", fontsize=10)
    ax.set_ylabel("Conditional hit rate  "
                  r"$P(\mathrm{hit}\,|\,N_c(\hat{c}) \geq \tau)$",
                  fontsize=10)
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
