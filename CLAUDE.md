# CLAUDE.md

## What This Is

Standalone methods paper: "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts". Targets JAS. Extracts the verification framework from the Clyfar preprint appendices (C, E, F) and generalises it with SPC severe weather categories as the running example.

Short title: "Possibilistic forecast verification".

## Build

- **LaTeX**: Compiled on **Overleaf with XeLaTeX**. Locally: `latexmk -xelatex main.tex`.
- **Figures**: `python scripts/generate_all.py` (or individual `python scripts/fig_*.py`). Outputs PDF to `figures/`.
- **Python env**: `conda env create -f environment.yml` creates `poss-verif`.

## LaTeX

- **Template**: rho-class (two-column, 9.5pt). Do not modify `rho.cls`.
- **Colours**: Purple `#7B1FA2` (rhocolor), Green `#46A21F` (rationalecolor). Set in `preamble.tex` via `\colorthemePossVerifPurple` / `\colorthemePossVerifGreen`.
- **Environments**: `rhoenv` (purple) for definitions/theorems. `rationaleenv` (green) for "Intuition" sidebars.
- **Citations**: natbib + `ametsocV6.bst`. Use `\citet{}` / `\citep{}`.
- **No appendices**. Everything in main text.

### Macros

| Macro | Renders | Meaning |
|-------|---------|---------|
| `\poss` | Pi | Possibility measure |
| `\ign` | H_Pi | Possibilistic ignorance (1 - max pi) |
| `\Nc` | N_c | Conditional necessity |
| `\nec` | N | Classical necessity |
| `\pinorm` | pi' | Shape-normalised distribution (pi / max pi) |
| `\spc{MDT}` | MDT (smallcaps) | SPC category name |

## Python

Canonical constants live in `scripts/style.py`:

```
PURPLE    = "#7B1FA2"
GREEN     = "#46A21F"
LIGHT_GREY = "#F0F0F0"
DARK_GREY  = "#333333"
MID_GREY   = "#999999"
SPC_CATEGORIES = ["MRGL", "SLGT", "ENH", "MDT", "HIGH"]
```

Figures: 300 DPI PDF, sans-serif font (Helvetica > Arial > TeX Gyre Heros > DejaVu Sans), light-grey axes background. All saved to project-root `figures/`.

### Five-number scorecard (canonical definitions in `fig_three_scenario.py:compute_scorecard`)

| Symbol | Formula | What it measures |
|--------|---------|------------------|
| alpha* | pi'(c_obs) | Depth-of-truth: normalised possibility of observed category |
| eta | mean(pi') | Nonspecificity: spread of normalised distribution |
| delta | alpha* - eta | Resolution gap: discrimination above average |
| H_Pi | 1 - max(pi) | Ignorance: subnormality gap |
| N_c* | 1 - max_{w != c_obs} pi'(w) | Conditional necessity of truth |

### Known mismatch

The three scenarios in `07-worked-examples.tex` use slightly different pi values and observed categories than those in `fig_three_scenario.py`. The LaTeX table values are self-consistent (computed from the LaTeX distributions). When reconciling, decide which set is canonical and update the other.

## Source Archive

- `archive/preprint-sections/` — verbatim copies of preprint 04, A3, A5, A6 for offline reference.
- Sibling repo `../preprint-clyfar-v0p9/` has the full preprint if needed.
