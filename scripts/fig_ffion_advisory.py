"""Figure 9: Example LLM-generated advisory from a possibilistic forecast.

Renders a mock-up of a Ffion-style advisory: structured forecast data
on the left, plain-language LLM translation on the right, showing how
the three-component triplet feeds automated risk communication.
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from style import (
    apply_style, save_fig,
    PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY,
)

# The advisory text — representative of Ffion's output style.
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


def main():
    apply_style()

    fig, (ax_data, ax_text) = plt.subplots(
        1, 2, figsize=(10.0, 3.8),
        gridspec_kw={"width_ratios": [1, 2], "wspace": 0.08},
    )

    for ax in (ax_data, ax_text):
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("white")
        for spine in ax.spines.values():
            spine.set_visible(False)

    # --- Left panel: structured data ---
    # Header bar
    header_data = mpatches.FancyBboxPatch(
        (0.03, 0.88), 0.94, 0.10, boxstyle="round,pad=0.01",
        facecolor=PURPLE, edgecolor="none",
    )
    ax_data.add_patch(header_data)
    ax_data.text(
        0.50, 0.93, "Structured Input (JSON)",
        ha="center", va="center", fontsize=9,
        fontweight="bold", color="white", family="sans-serif",
    )

    # Data box
    data_box = mpatches.FancyBboxPatch(
        (0.03, 0.04), 0.94, 0.82, boxstyle="round,pad=0.02",
        facecolor=LIGHT_GREY, edgecolor=MID_GREY, linewidth=0.8,
    )
    ax_data.add_patch(data_box)
    ax_data.text(
        0.08, 0.80, STRUCTURED_DATA,
        ha="left", va="top", fontsize=8.5,
        color=DARK_GREY, family="monospace", linespacing=1.35,
    )

    # --- Right panel: LLM advisory ---
    # Header bar
    header_text = mpatches.FancyBboxPatch(
        (0.02, 0.88), 0.96, 0.10, boxstyle="round,pad=0.01",
        facecolor=GREEN, edgecolor="none",
    )
    ax_text.add_patch(header_text)
    ax_text.text(
        0.50, 0.93, "LLM-Generated Advisory (Stakeholder Level)",
        ha="center", va="center", fontsize=9,
        fontweight="bold", color="white", family="sans-serif",
    )

    # Advisory text box
    text_box = mpatches.FancyBboxPatch(
        (0.02, 0.04), 0.96, 0.82, boxstyle="round,pad=0.02",
        facecolor="#FAFAFA", edgecolor=MID_GREY, linewidth=0.8,
    )
    ax_text.add_patch(text_box)
    ax_text.text(
        0.06, 0.80, ADVISORY_TEXT,
        ha="left", va="top", fontsize=9.5,
        color=DARK_GREY, family="serif", linespacing=1.5,
        wrap=True,
        # matplotlib wrap uses axes coordinates; set clip box
    )
    # Re-do with manual wrapping for reliable column fit
    ax_text.texts[-1].remove()

    import textwrap
    wrapped = textwrap.fill(ADVISORY_TEXT, width=52)
    ax_text.text(
        0.06, 0.80, wrapped,
        ha="left", va="top", fontsize=9.5,
        color=DARK_GREY, family="serif", linespacing=1.5,
    )

    # Arrow between panels
    fig.patches.append(mpatches.FancyArrowPatch(
        (0.365, 0.50), (0.395, 0.50),
        transform=fig.transFigure,
        arrowstyle="->,head_width=6,head_length=4",
        color=PURPLE, linewidth=1.5,
        mutation_scale=1,
    ))

    # Small label under arrow
    fig.text(
        0.38, 0.44, "LLM\n+ guardrails",
        ha="center", va="top", fontsize=7,
        color=MID_GREY, family="sans-serif", style="italic",
    )

    save_fig(fig, "fig9_ffion_advisory")


if __name__ == "__main__":
    main()
