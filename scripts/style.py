"""Shared style constants and matplotlib configuration for possibilistic verification figures."""
import matplotlib as mpl
import matplotlib.pyplot as plt

# Colour palette
PURPLE = "#7B1FA2"
GREEN = "#46A21F"
LIGHT_GREY = "#F0F0F0"
DARK_GREY = "#333333"
MID_GREY = "#999999"

# SPC convective outlook categories (5-level, no TSTM)
SPC_CATEGORIES = ["MRGL", "SLGT", "ENH", "MDT", "HIGH"]
SPC_N = len(SPC_CATEGORIES)

# Figure output (resolved relative to project root)
import os as _os
FIG_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "figures")
DPI = 300
FIG_FORMAT = "png"

def apply_style():
    """Apply shared matplotlib rcParams."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "TeX Gyre Heros", "DejaVu Sans"],
        "font.size": 10,
        "axes.facecolor": LIGHT_GREY,
        "axes.edgecolor": MID_GREY,
        "axes.labelcolor": DARK_GREY,
        "axes.grid": False,
        "xtick.color": DARK_GREY,
        "ytick.color": DARK_GREY,
        "text.color": DARK_GREY,
        "figure.facecolor": "white",
        "figure.dpi": DPI,
        "savefig.dpi": DPI,
        "savefig.format": FIG_FORMAT,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
    })

def save_fig(fig, name):
    """Save figure to the figures directory as PNG."""
    import os
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, f"{name}.{FIG_FORMAT}")
    fig.savefig(path, facecolor="white", transparent=False)
    plt.close(fig)
    print(f"Saved: {path}")
    return path
