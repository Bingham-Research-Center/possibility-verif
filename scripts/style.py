"""Shared style constants and matplotlib configuration for possibilistic verification figures."""
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import os as _os_font

# Register bundled TeX Gyre Heros fonts (Helvetica-metric-compatible, GUST License)
_FONT_DIR = _os_font.path.join(
    _os_font.path.dirname(_os_font.path.dirname(_os_font.path.abspath(__file__))),
    "fonts", "texgyreheros",
)
if _os_font.path.isdir(_FONT_DIR):
    for _f in _os_font.listdir(_FONT_DIR):
        if _f.endswith(".otf"):
            fm.fontManager.addfont(_os_font.path.join(_FONT_DIR, _f))

# Colour palette
PURPLE = "#7B1FA2"
GREEN = "#46A21F"
LIGHT_GREY = "#F0F0F0"
DARK_GREY = "#333333"
MID_GREY = "#999999"

# SPC convective outlook categories (6-level, including null; no TSTM)
SPC_CATEGORIES = ["NONE", "MRGL", "SLGT", "ENH", "MDT", "HIGH"]
SPC_N = len(SPC_CATEGORIES)

# Approximate SPC category climatological frequencies
# (NONE dominates; HIGH is very rare)
import numpy as _np
SPC_CLIM = _np.array([0.60, 0.18, 0.12, 0.06, 0.032, 0.008])

# Figure output (resolved relative to project root)
import os as _os
FIG_DIR = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), "figures")
DPI = 300
FIG_FORMAT = "png"

def apply_style():
    """Apply shared matplotlib rcParams."""
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["TeX Gyre Heros", "Helvetica", "Arial", "DejaVu Sans"],
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
