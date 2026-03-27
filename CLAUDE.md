# CLAUDE.md

## What This Is

Standalone methods paper: "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts". Targets JAS. Extracts the verification framework from the Clyfar preprint appendices (C, E, F) with SPC severe weather categories as the running example.

**Author:** John R. Lawson (@johnrobertlawson), Utah State University (Bingham Research Center + Dept of Mathematics and Statistics). Email: john.lawson@usu.edu.

**Repo:** github.com/bingham-research-center/possibility-verif

## Build

- **LaTeX**: Compiled on **Overleaf with XeLaTeX** (TeX Live 2025). Locally: `latexmk -xelatex main.tex`.
- **Figures**: `python scripts/generate_all.py` then `python scripts/fig_scorecard_table.py`, `python scripts/fig_performance_diagram.py`, and `python scripts/fig_severity_matrix.py`. Outputs 13 PNGs to `figures/`.
- **Python env**: `conda env create -f environment.yml` creates `poss-verif`.

## Gotchas

- **Figures must be PNG, not PDF.** XeTeX's xdvipdfmx backend crashes silently on matplotlib PDF transparency (`/SMask`, `/ca`, `/CA`). No `!` error in the log — just "No PDF produced" on Overleaf. `scripts/style.py` sets `FIG_FORMAT = "png"`. Do not switch back to PDF.
- **`generate_all.py` only runs figs 1–9.** Figs 10–12 (`fig_scorecard_table.py`, `fig_performance_diagram.py`, `fig_severity_matrix.py`) must be run separately. `fig_perf_iterate.py` must also be run separately (generates hexbin + commitment figures).
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

## Figures (13 total, all PNG, no number prefixes)

| PNG name | Script | Section | What it shows |
|----------|--------|---------|---------------|
| `possibility_anatomy` | `fig_possibility_anatomy.py` | §2.2 | Subnormal bar chart with Pi_max, H_Pi, N_c |
| `three_scenario` | `fig_three_scenario.py` | §6.3 | Three scenarios side-by-side with scorecard |
| `filling_gauge` | `fig_filling_gauge.py` | §6.2 | Horizontal gauge bars for Scenario A |
| `pignistic_bridge` | `fig_pignistic_bridge.py` | §3.1 | Raw pi → probability with ignorance bar |
| `upper_lower_bounds` | `fig_upper_lower_bounds.py` | §4.3 | [L,U] exceedance bounds on number line |
| `reliability_curves` | `fig_reliability_curves.py` | §5.1 | Conditional hit rate vs N_c threshold |
| `ig_decomposition` | `fig_ig_decomposition.py` | §3.2 | Stacked bar IG decomposition (UNC, DSC, REL) |
| `verification_lanes` | `fig_verification_lanes.py` | §5.2 | Three-lane flowchart schematic |
| `ffion_advisory` | `fig_ffion_advisory.py` | §7.3 | NWP context → JSON → LLM advisory pipeline |
| `scorecard_table` | `fig_scorecard_table.py` | §5.2 | ECMWF-style scorecard with triangles |
| `perf_hexbin_trajectory` | `fig_perf_iterate.py` | §4.2 | Hexbin + green trajectory shape-quality diagram |
| `commitment_diagram` | `fig_perf_iterate.py` | §4.2 | Commitment × discrimination diagnostic |
| `severity_matrix` | `fig_severity_matrix.py` | §7.4 | Severity-confidence matrix |

## Python

Canonical constants in `scripts/style.py`: `PURPLE`, `GREEN`, `SPC_CATEGORIES`, `FIG_FORMAT = "png"`.

Scorecard computation canonical in `fig_three_scenario.py:compute_scorecard`.

Scenario pi values canonical in `fig_three_scenario.py:SCENARIOS` — other scripts import from there.

## Architecture

The paper has two evaluation tools and one diagnostic:
- **Five-number scorecard** (§4): native possibilistic — evaluates shape and confidence without conversion
- **IG via bridge** (§3): probabilistic — converts to probabilities, measures information gain
- **Exceedance bounds** [L, U] (§4.3): diagnostic — answers probability-of-exceedance questions directly from possibility–necessity duality

The ILS (interval log score) formula was removed — it was not strictly proper and had no baseline. The [L, U] bounds are retained as descriptive diagnostics.

## Manuscript Status

### Done
- All 10 section files with equations migrated from preprint
- 13 figures (PNG) embedded with captions + in-text references
- Pi values aligned: anatomy fig uses §2 Example 1, bridge fig uses §3 worked example, bounds fig imports canonical scenarios from `fig_three_scenario.py`
- NONE category added to Ω: K=6, ordering (NONE, MRGL, SLGT, ENH, MDT, HIGH)
- §3 "Possibility-to-Probability Bridge" section title and content complete
- §3.3 "Why Naive Normalisation Erases Information" filled
- §4.2 performance diagram paragraph filled
- §5.2 diagnostic workflow paragraph filled
- §6 scenarios A/B/C fully described with meteorological context
- §6 scorecard, gauge, bridge walkthrough all complete
- §7 discussion subsections filled (DS connections, beyond severe weather, LLM pipeline, software, limitations)
- Ffion figure expanded to 3-panel NWP→JSON→advisory pipeline
- Appendix (IRLS + possibilistic climatology) commented out — deferred to future work
- ILS formula removed; [L,U] bounds retained as "Exceedance Bounds" subsection
- Uniform 1/K baseline caveat added to §6

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
