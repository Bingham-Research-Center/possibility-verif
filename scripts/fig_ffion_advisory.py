"""Figure: LLM-mediated advisory from possibilistic forecast.

Three-panel schematic: raw NWP context → structured JSON → LLM advisory.
Shows the full pipeline from ensemble weather data through possibilistic
analysis to stakeholder communication.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import textwrap

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
)

NWP_BLUE = "#37474F"

ADVISORY_TEXT = (
    "MDT risk is the most plausible convective outlook today "
    "(\u03A0 = 0.75). Confidence is moderate: the system flags "
    "25% ignorance, meaning conditions partially lie outside "
    "typical rule coverage. Among scenarios the system does "
    "cover, MDT dominates all alternatives (N\u2099 = 0.73). "
    "ENH risk retains non-trivial plausibility (\u03C0 = 0.20); "
    "protective actions for MDT-level impacts are recommended "
    "while monitoring for upgrade to HIGH."
)

STRUCTURED_DATA = (
    "Forecast triplet\n"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
    "\u2500\u2500\u2500\n"
    "\u03A0(MDT)  = 0.75  (peak)\n"
    "H\u03A0      = 0.25\n"
    "N\u2099(MDT) = 0.73\n"
    "\n"
    "Full distribution\n"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
    "\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500"
    "\u2500\u2500\u2500\n"
    "NONE  0.05\n"
    "MRGL  0.00\n"
    "SLGT  0.10\n"
    "ENH   0.20\n"
    "MDT   0.75  \u25C0\n"
    "HIGH  0.15"
)


def _draw_panel_header(ax, text, color, x0=0.03, w=0.94):
    """Draw a coloured header bar at the top of a panel."""
    header = mpatches.FancyBboxPatch(
        (x0, 0.88), w, 0.10, boxstyle="round,pad=0.01",
        facecolor=color, edgecolor="none",
    )
    ax.add_patch(header)
    ax.text(x0 + w / 2, 0.93, text,
            ha="center", va="center", fontsize=8.5,
            fontweight="bold", color="white", family="sans-serif")


def _draw_content_box(ax, color=LIGHT_GREY, x0=0.03, w=0.94):
    """Draw a rounded content box below the header."""
    box = mpatches.FancyBboxPatch(
        (x0, 0.04), w, 0.82, boxstyle="round,pad=0.02",
        facecolor=color, edgecolor=MID_GREY, linewidth=0.8,
    )
    ax.add_patch(box)


def _setup_panel(ax):
    """Clear axes decorations for a flat panel."""
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)


def main():
    apply_style()

    fig = plt.figure(figsize=(13.5, 4.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1.2, 1, 2], wspace=0.06,
                          left=0.02, right=0.98, bottom=0.04, top=0.96)

    # --- Panel 1: Raw NWP Context ---
    gs_nwp = gs[0].subgridspec(2, 1, height_ratios=[1, 1], hspace=0.25)

    # Exceedance probability bars (top mini-axes)
    ax_exc = fig.add_subplot(gs_nwp[0])
    cats = ["MRGL", "SLGT", "ENH", "MDT", "HIGH"]
    probs = [0.85, 0.60, 0.40, 0.30, 0.08]
    y_pos = np.arange(len(cats))
    bars = ax_exc.barh(y_pos, probs, height=0.6, color=PURPLE, alpha=0.7,
                       edgecolor="white", linewidth=0.5)
    for i, (p, c) in enumerate(zip(probs, cats)):
        ax_exc.text(p + 0.02, i, f"{p:.0%}", va="center", fontsize=7,
                    color=DARK_GREY)
    ax_exc.set_yticks(y_pos)
    ax_exc.set_yticklabels(cats, fontsize=7)
    ax_exc.set_xlim(0, 1.15)
    ax_exc.set_xlabel("P(exceed.)", fontsize=7, labelpad=2)
    ax_exc.tick_params(axis="x", labelsize=6)
    ax_exc.set_title("Ensemble exceedance", fontsize=7.5,
                     fontweight="bold", color=DARK_GREY, pad=3)
    ax_exc.set_facecolor(LIGHT_GREY)

    # Time series (bottom mini-axes)
    ax_ts = fig.add_subplot(gs_nwp[1])
    rng = np.random.default_rng(42)
    hours = np.linspace(0, 24, 49)
    base = 1800 + 800 * np.sin(np.pi * hours / 24)
    for _ in range(5):
        member = base + rng.normal(0, 250, len(hours))
        member = np.clip(member, 200, 4000)
        ax_ts.plot(hours, member, color=MID_GREY, lw=0.6, alpha=0.5)
    ax_ts.plot(hours, base, color=PURPLE, lw=1.5, label="Mean")
    ax_ts.set_xlim(0, 24)
    ax_ts.set_ylim(0, 4200)
    ax_ts.set_xlabel("Hour (UTC)", fontsize=7, labelpad=2)
    ax_ts.set_ylabel("CAPE\n(J/kg)", fontsize=7, labelpad=2, rotation=0,
                     ha="right", va="center")
    ax_ts.tick_params(labelsize=6)
    ax_ts.set_title("Ensemble CAPE trace", fontsize=7.5,
                     fontweight="bold", color=DARK_GREY, pad=3)
    ax_ts.set_facecolor(LIGHT_GREY)

    # NWP super-title
    nwp_pos = gs[0].get_position(fig)
    fig.text(nwp_pos.x0 + nwp_pos.width / 2, 0.99,
             "Raw NWP Context", ha="center", va="top",
             fontsize=9, fontweight="bold", color=NWP_BLUE)

    # --- Panel 2: Structured JSON ---
    ax_json = fig.add_subplot(gs[1])
    _setup_panel(ax_json)
    _draw_panel_header(ax_json, "Structured Input (JSON)", PURPLE)
    _draw_content_box(ax_json)
    ax_json.text(0.08, 0.80, STRUCTURED_DATA,
                 ha="left", va="top", fontsize=8,
                 color=DARK_GREY, family="monospace", linespacing=1.3)

    # --- Panel 3: LLM Advisory ---
    ax_adv = fig.add_subplot(gs[2])
    _setup_panel(ax_adv)
    _draw_panel_header(ax_adv, "LLM-Generated Advisory (Stakeholder Level)",
                       GREEN, x0=0.02, w=0.96)
    _draw_content_box(ax_adv, color="#FAFAFA", x0=0.02, w=0.96)
    wrapped = textwrap.fill(ADVISORY_TEXT, width=56)
    ax_adv.text(0.05, 0.80, wrapped,
                ha="left", va="top", fontsize=9,
                color=DARK_GREY, family="serif", linespacing=1.45)

    # --- Arrows between panels ---
    # Arrow 1: NWP → JSON
    json_pos = gs[1].get_position(fig)
    fig.patches.append(mpatches.FancyArrowPatch(
        (nwp_pos.x1 + 0.003, 0.50),
        (json_pos.x0 - 0.003, 0.50),
        transform=fig.transFigure,
        arrowstyle="->,head_width=6,head_length=4",
        color=PURPLE, linewidth=1.5, mutation_scale=1,
    ))
    fig.text((nwp_pos.x1 + json_pos.x0) / 2, 0.42,
             "Possibilistic\nanalysis", ha="center", va="top",
             fontsize=7, color=MID_GREY, style="italic")

    # Arrow 2: JSON → Advisory
    adv_pos = gs[2].get_position(fig)
    fig.patches.append(mpatches.FancyArrowPatch(
        (json_pos.x1 + 0.003, 0.50),
        (adv_pos.x0 - 0.003, 0.50),
        transform=fig.transFigure,
        arrowstyle="->,head_width=6,head_length=4",
        color=PURPLE, linewidth=1.5, mutation_scale=1,
    ))
    fig.text((json_pos.x1 + adv_pos.x0) / 2, 0.42,
             "LLM\n+ guardrails", ha="center", va="top",
             fontsize=7, color=MID_GREY, style="italic")

    save_fig(fig, "ffion_advisory")


if __name__ == "__main__":
    main()
