"""Generate all figures for the possibilistic verification manuscript.

Figures included in the manuscript (12 total):
  1. possibility_anatomy     (§2.2)
  2. three_scenario           (§6.3)
  3. filling_gauge            (§6.2)
  4. pignistic_bridge         (§3.1)
  5. reliability_curves       (§5.1)
  6. ig_decomposition         (§3.2)
  7. verification_lanes       (§5.2)
  8. categorical_scores       (§6.x)

Run separately (import from other scripts):
  - fig_scorecard_table.py     → scorecard_table.png         (§5.2)
  - fig_performance_diagram.py → perf_hexbin_trajectory.png  (§4.2)
                               → commitment_diagram.png      (§4.2)
  - fig_severity_matrix.py     → severity_matrix.png         (§7.3)

Not in manuscript (scripts retained, PNGs still generated):
  - fig_upper_lower_bounds.py  (exceedance bounds removed in Round 2)
  - fig_ffion_advisory.py      (LLM section removed in Round 2)
"""
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
from fig_reliability_curves import main as fig5
from fig_ig_decomposition import main as fig6
from fig_verification_lanes import main as fig7
from fig_categorical_scores import main as fig8

if __name__ == "__main__":
    for i, fig_func in enumerate([fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8], 1):
        print(f"Generating Figure {i}...")
        fig_func()
    print("All figures generated.")
    print("\nRemember to also run separately:")
    print("  python fig_scorecard_table.py")
    print("  python fig_performance_diagram.py")
    print("  python fig_severity_matrix.py")
