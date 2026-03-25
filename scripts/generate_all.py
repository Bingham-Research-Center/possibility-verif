"""Generate all figures for the possibilistic verification manuscript."""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from style import apply_style
apply_style()

# Import and run each figure script
from fig_possibility_anatomy import main as fig1
from fig_three_scenario import main as fig2
from fig_filling_gauge import main as fig3
from fig_pignistic_bridge import main as fig4
from fig_upper_lower_bounds import main as fig5
from fig_reliability_curves import main as fig6
from fig_ig_decomposition import main as fig7
from fig_verification_lanes import main as fig8
from fig_ffion_advisory import main as fig9

if __name__ == "__main__":
    for i, fig_func in enumerate([fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9], 1):
        print(f"Generating Figure {i}...")
        fig_func()
    print("All figures generated.")
