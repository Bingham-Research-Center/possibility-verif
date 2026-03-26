# CLAUDE.md

## What This Is

Standalone methods paper: "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts". Targets JAS. Extracts the verification framework from the Clyfar preprint appendices (C, E, F) with convective mode categories as the running example.

**Author:** John R. Lawson (@johnrobertlawson), Utah State University (Bingham Research Center + Dept of Mathematics and Statistics). Email: john.lawson@usu.edu.

**Repo:** github.com/bingham-research-center/possibility-verif

## Build

- **LaTeX**: Compiled on **Overleaf with XeLaTeX** (TeX Live 2025). Locally: `latexmk -xelatex main.tex`.
- **Figures**: `python scripts/generate_all.py` then `python scripts/fig_scorecard_table.py`, `python scripts/fig_performance_diagram.py`, and `python scripts/fig_severity_matrix.py`. Outputs 12 PNGs to `figures/`.
- **Python env**: `conda env create -f environment.yml` creates `poss-verif`.

## Gotchas

- **Figures must be PNG, not PDF.** XeTeX's xdvipdfmx backend crashes silently on matplotlib PDF transparency (`/SMask`, `/ca`, `/CA`). No `!` error in the log — just "No PDF produced" on Overleaf. `scripts/style.py` sets `FIG_FORMAT = "png"`. Do not switch back to PDF.
- **`generate_all.py` only runs figs 1–9.** Figs 10–12 (`fig_scorecard_table.py`, `fig_performance_diagram.py`, `fig_severity_matrix.py`) must be run separately.
- **`Smets1990-MISSING`** citation key in `04-pignistic-bridge.tex` is a placeholder — needs a real bib entry added to `paperpile.bib`.
- **`rho.cls` loads heavy unused packages** (circuitikz, chemfig, matlab-prettifier, lipsum). Do not modify `rho.cls`, but be aware compilation is slow.

## LaTeX

- **Template**: rho-class (two-column, 9.5pt). Do not modify `rho.cls`.
- **Colours**: Purple `#7B1FA2`, Green `#46A21F`. Set in `preamble.tex`.
- **Environments**: `rhoenv` (purple) for definitions/theorems. `rationaleenv` (green) for "Intuition" sidebars.
- **Citations**: natbib + `ametsocV6.bst`. Use `\citet{}` / `\citep{}`.
- **Appendix A** (`appendix-alternative-scores.tex`): IRLS + possibilistic climatology.

### Macros

| Macro | Renders | Meaning |
|-------|---------|---------|
| `\poss` | Pi | Possibility measure |
| `\ign` | H_Pi | Possibilistic ignorance (1 - max pi) |
| `\Nc` | N_c | Conditional necessity |
| `\nec` | N | Classical necessity |
| `\pinorm` | pi' | Shape-normalised distribution (pi / max pi) |
| `\mode{SUPER}` | SUPER (smallcaps) | Convective mode name |

### Distribution formatting convention

- **First use** (§2, §6): `\begin{cases}` format, one category per line.
- **Subsequent uses** (§3, §4): ordered-tuple `$\pi = (0.00,\, 0.05,\, 0.85,\, 0.10,\, 0.05)$` with ordering (NULL, CELL, SUPER, QLCS, MCS).

## Figures (12 total, all PNG, no number prefixes)

| PNG name | Script | Section | What it shows |
|----------|--------|---------|---------------|
| `possibility_anatomy` | `fig_possibility_anatomy.py` | §2.2 | Subnormal bar chart with Pi_max, H_Pi, N_c |
| `three_scenario` | `fig_three_scenario.py` | §6.3 | Three scenarios side-by-side with scorecard |
| `filling_gauge` | `fig_filling_gauge.py` | §6.2 | Horizontal gauge bars for Scenario A |
| `pignistic_bridge` | `fig_pignistic_bridge.py` | §3.1 | Raw pi → probability with ignorance bar |
| `upper_lower_bounds` | `fig_upper_lower_bounds.py` | §4.3 | [L,U] intervals on number line |
| `reliability_curves` | `fig_reliability_curves.py` | §5.1 | Conditional hit rate vs N_c threshold |
| `ig_decomposition` | `fig_ig_decomposition.py` | §3.2 | Stacked bar IG decomposition (UNC, DSC, REL) |
| `verification_lanes` | `fig_verification_lanes.py` | §5.2 | Three-lane flowchart schematic |
| `ffion_advisory` | `fig_ffion_advisory.py` | §7.3 | JSON → LLM advisory mock-up |
| `scorecard_table` | `fig_scorecard_table.py` | §5.2 | ECMWF-style scorecard with triangles |
| `performance_diagram` | `fig_performance_diagram.py` | §4.2 | Roebber-style five-metric diagram |
| `severity_matrix` | `fig_severity_matrix.py` | §7.4 | Wind-max severity × confidence matrix |

## Convective Mode Categories (K=5)

| Short | Full name | Definition |
|-------|-----------|------------|
| NULL  | No convection | No echoes ≥35 dBZ in domain during period |
| CELL  | Discrete cells | Unorganised single cells, no rotation |
| SUPER | Supercell(s) | Discrete cells with mesocyclone |
| QLCS  | Quasi-linear | Linear convective organisation ≥75 km |
| MCS   | Mesoscale convective system | Contiguous system ≥100 km, ≥3 hr |

- **Threshold event:** A_T = {SUPER, QLCS, MCS} = "organised convection"
- **Climatology (synthetic):** NULL 45%, CELL 25%, SUPER 15%, QLCS 10%, MCS 5%

## Python

Canonical constants in `scripts/style.py`: `PURPLE`, `GREEN`, `CONV_MODES`, `CONV_N`, `FIG_FORMAT = "png"`.

Scorecard computation canonical in `fig_three_scenario.py:compute_scorecard`.

## Manuscript Status

### Done
- All 10 section files with equations migrated from preprint
- 15 labelled equations, all cross-references resolve
- 12 figures (PNG) embedded with captions + in-text references
- Running example switched from SPC categories (K=6) to convective mode categories (K=5)
- All π arrays, scorecard values, bridge computations, and ILS calculations updated for K=5
- Notation table (§2) with Form (raw/norm) and Eq. columns
- Ffion/LLM communication subsection (§7.3) with pipeline sketch
- ILS framed as probability-of-exceedance
- §3 opening paragraph filled (etymology, motivation, bridge summary)
- §3.3 "Why Naive Normalisation Erases Information" filled (3 paragraphs + worked contrast)
- "Tripartite pignistic" renamed to "possibility-to-probability bridge" globally
- §5.2 diagnostic workflow paragraph filled (scorecard table figure + interpretation)
- §4.2 performance diagram paragraph filled (Roebber-style five-metric diagnostic)
- Fig 7 IG decomposition bug fixed (negative-DSC bar placement)
- Severity matrix rethemed to generic wind-max severity × confidence (domain-independent)

### Still placeholder (`% [PLACEHOLDER]`)
- §1 (introduction) — mostly placeholder with paper-outline paragraph done
- §2 opening paragraph, §2.4 "Why Not Just Probabilities?" (3–4 paragraphs)
- §4 opening paragraph, ILS motivation paragraph
- §5 opening paragraph, sample-size discussion
- §6 opening paragraph, meteorological scenario descriptions for A/B/C, interpretation paragraphs, bridge walkthrough computations
- §7 opening paragraph, subsection bodies (DS connections, beyond severe weather, software, limitations)
- Missing citations: Dubois 2006, Smets 1990, Shafer 1976, Roulston & Smith 2002, Lawson 2024

## Related Work

- **Clyfar preprint**: `../preprint-clyfar-v0p9/` — source material (Appendices C, E, F).
- **Ffion** (Lawson, in prep.): LLM-mediated risk communication. Details in `../brc-knowledge/`.
- **Archive**: `archive/preprint-sections/` — verbatim copies of preprint 04, A3, A5, A6.
