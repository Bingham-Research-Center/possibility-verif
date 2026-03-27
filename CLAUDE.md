# CLAUDE.md

## What This Is

Standalone methods paper: "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts". Targets JAS. Extracts the verification framework from the Clyfar preprint appendices (C, E, F) with SPC severe weather categories as the running example.

**Author:** John R. Lawson (@johnrobertlawson), Utah State University (Bingham Research Center + Dept of Mathematics and Statistics). Email: john.lawson@usu.edu.

**Repo:** github.com/bingham-research-center/possibility-verif

## Build

- **LaTeX**: Compiled on **Overleaf with XeLaTeX** (TeX Live 2025). Locally: `latexmk -xelatex main.tex`.
- **Figures**: `python scripts/generate_all.py` (8 figs), then separately `python scripts/fig_scorecard_table.py`, `python scripts/fig_performance_diagram.py`, `python scripts/fig_severity_matrix.py`. Outputs 12 manuscript PNGs to `figures/`.
- **Python env**: `conda env create -f environment.yml` creates `poss-verif`.

## Gotchas

- **Figures must be PNG, not PDF.** XeTeX's xdvipdfmx backend crashes silently on matplotlib PDF transparency (`/SMask`, `/ca`, `/CA`). No `!` error in the log — just "No PDF produced" on Overleaf. `scripts/style.py` sets `FIG_FORMAT = "png"`. Do not switch back to PDF.
- **`generate_all.py` runs figs 1–8.** Figs 9–12 (`fig_scorecard_table.py`, `fig_performance_diagram.py`, `fig_severity_matrix.py`) must be run separately. `fig_perf_iterate.py` generates hexbin + commitment figures (called by `fig_performance_diagram.py`).
- **Hexbin gridsize**: matplotlib's default `gridsize=N` computes `ny = int(N/√3)` which **floors** instead of rounding, producing hexagons ~16% too tall. Always use `gridsize=(nx, ny)` tuples with correct rounding.
- **`rho.cls` loads heavy unused packages** (circuitikz, chemfig, matlab-prettifier, lipsum). Do not modify `rho.cls`, but be aware compilation is slow.

## LaTeX

- **Template**: rho-class (two-column, 9.5pt). Do not modify `rho.cls`.
- **Colours**: Purple `#7B1FA2`, Green `#46A21F`. Set in `preamble.tex`.
- **Environments**: `rhoenv` (purple) for definitions/theorems. `rationaleenv` (green) for "Intuition" sidebars.
- **Citations**: natbib + `ametsocV6.bst`. Use `\citet{}` / `\citep{}`.
- **Appendix**: `appendix-alternative-scores.tex` (IRLS + possibilistic climatology) is **commented out** in `main.tex`. Source retained for reference/re-inclusion.

### Macros

| Macro | Renders | Meaning |
|-------|---------|---------|
| `\poss` | Pi | Possibility measure |
| `\ign` | H_Pi | Possibilistic ignorance (1 - max pi) |
| `\Nc` | N_c | Conditional necessity |
| `\nec` | N | Classical necessity |
| `\pinorm` | pi' | Shape-normalised distribution (pi / max pi) |
| `\spc{MDT}` | MDT (smallcaps) | SPC category name |

### Distribution formatting convention

- **First use** (§2, §6): `\begin{cases}` format, one category per line.
- **Subsequent uses** (§3, §4): ordered-tuple `$\pi = (0.05,\, 0.2,\, 0.4,\, 0.6,\, 0.1,\, 0.0)$` with ordering (NONE, MRGL, SLGT, ENH, MDT, HIGH).

## Figures (12 in manuscript, all PNG)

| PNG name | Script | Section | What it shows |
|----------|--------|---------|---------------|
| `possibility_anatomy` | `fig_possibility_anatomy.py` | §2.2 | Subnormal bar chart with Pi_max, H_Pi, N_c |
| `three_scenario` | `fig_three_scenario.py` | §6.5 | Three scenarios side-by-side with scorecard |
| `filling_gauge` | `fig_filling_gauge.py` | §6.4 | Horizontal gauge bars for Scenario A |
| `pignistic_bridge` | `fig_pignistic_bridge.py` | §3.1 | Raw pi → probability with ignorance bar |
| `reliability_curves` | `fig_reliability_curves.py` | §5.1 | Conditional hit rate vs N_c threshold |
| `ig_decomposition` | `fig_ig_decomposition.py` | §3.2 | Stacked bar IG decomposition (UNC, DSC, REL) |
| `verification_lanes` | `fig_verification_lanes.py` | §5.2 | Three-lane flowchart schematic |
| `categorical_scores` | `fig_categorical_scores.py` | §6.2 | Two-panel: threshold POD/FAR/CSI + confusion matrix |
| `scorecard_table` | `fig_scorecard_table.py` | §5.2 | ECMWF-style scorecard with triangles |
| `perf_hexbin_trajectory` | `fig_perf_iterate.py` | §4.2 | Hexbin + green trajectory shape-quality diagram |
| `commitment_diagram` | `fig_perf_iterate.py` | §4.2 | Commitment × discrimination diagnostic |
| `severity_matrix` | `fig_severity_matrix.py` | §7.3 | Severity-confidence matrix |

**Not in manuscript** (scripts retained): `upper_lower_bounds` (exceedance bounds removed in Round 2), `ffion_advisory` (LLM section removed in Round 2).

## Python

Canonical constants in `scripts/style.py`: `PURPLE`, `GREEN`, `SPC_CATEGORIES`, `SPC_CLIM`, `FIG_FORMAT = "png"`.

`SPC_CLIM = (0.60, 0.18, 0.12, 0.06, 0.032, 0.008)` — approximate SPC category climatological frequencies used as the IG baseline.

Scorecard computation canonical in `fig_three_scenario.py:compute_scorecard`.

Categorical scoring canonical in `fig_categorical_scores.py:categorical_scores`.

Scenario pi values canonical in `fig_three_scenario.py:SCENARIOS` — other scripts import from there.

Synthetic reforecast data generated by `fig_performance_diagram.py:generate_reforecast` — shared by hexbin, commitment, and categorical-scores figures.

## Architecture

The paper has three verification lanes:
- **Categorical lane** (§5, §6): mode-based threshold verification — POD, FAR, CSI per threshold, HSS from full K×K table. No distributional conversion needed.
- **Probabilistic lane** (§3): IG via bridge — converts to probabilities (with explicit ignorance outcome), measures information gain relative to SPC climatological baseline.
- **Native possibilistic lane** (§4): five-number scorecard — evaluates shape and confidence without conversion (α*, η, δ, H_Π, N_c*).

Exceedance bounds [L, U] were removed in Round 2 (circular under subnormality). Formal credal-set bounds noted as future work in §7.5.

## Manuscript Status

### Done
- All 10 section files with equations migrated from preprint
- 12 figures (PNG) embedded with captions + in-text references
- Round 2 revision complete (see `reviews/ROUND2-RESPONSE.md`):
  - Exceedance bounds §4.3 removed (M4)
  - Deterministic lane → categorical lane with POD/FAR/CSI/HSS (M6)
  - LLM/Ffion §7.4 → one paragraph in future work (m5)
  - IG baseline switched to SPC climatology (M7)
  - ε = 0.01 set explicitly with sensitivity analysis (M8)
  - Observation reframed as Day-1 forecast comparison (M9)
  - N(A) ≤ Pi(A) qualified for normality; max-additivity axiom added (M1, m1)
  - Bridge–pignistic language: "inspired by" not "generalizes" (M3)
  - Novelty claims softened throughout (4B)
  - Permutation-invariance moved to §4.2 (m7)
  - Severity matrix connected to scorecard (m6)

### Still needed
- Missing citation keys: Dubois2006, Smets1990, Shafer1976, Murphy1993, Jolliffe2012, Wilks2011, Walley1991, Neal2014
- §1 (introduction) — mostly placeholder
- §2 opening paragraph, §2.4 "Why Not Just Probabilities?"
- §5 opening paragraph, sample-size discussion
- Acknowledgments and Data Availability (backmatter placeholders)

## Related Work

- **Clyfar preprint**: `../preprint-clyfar-v0p9/` — source material (Appendices C, E, F).
- **Ffion** (Lawson, in prep.): LLM-mediated risk communication. Details in `../brc-knowledge/`.
- **Archive**: `archive/preprint-sections/` — verbatim copies of preprint 04, A3, A5, A6.
