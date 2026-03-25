# CLAUDE.md

## What This Is

Standalone methods paper: "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts". Short title: "Possibilistic forecast verification". Targets JAS. Extracts the verification framework from the Clyfar preprint appendices (C, E, F) and generalises it with SPC severe weather categories as the running example.

**Author:** John R. Lawson (@johnrobertlawson), Utah State University (Bingham Research Center + Dept of Mathematics and Statistics). Email: john.lawson@usu.edu.

**Repo:** github.com/bingham-research-center/possibility-verif

## Build

- **LaTeX**: Compiled on **Overleaf with XeLaTeX**. Locally: `latexmk -xelatex main.tex`.
- **Figures**: `python scripts/generate_all.py` (or individual `python scripts/fig_*.py`). Outputs 9 PDFs to `figures/`.
- **Python env**: `conda env create -f environment.yml` creates `poss-verif`.

## LaTeX

- **Template**: rho-class (two-column, 9.5pt). Do not modify `rho.cls`.
- **Colours**: Purple `#7B1FA2` (rhocolor), Green `#46A21F` (rationalecolor). Set in `preamble.tex`.
- **Environments**: `rhoenv` (purple) for definitions/theorems. `rationaleenv` (green) for "Intuition" sidebars.
- **Citations**: natbib + `ametsocV6.bst`. Use `\citet{}` / `\citep{}`.
- **No appendices**. Everything in main text.
- **Significance statement**: Uses `\section*{Significance Statement}` (not a custom environment).

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

- **First use** (§2 Examples 1–2, §6 Scenarios A–C): `\begin{cases}` format, one category per line. Fits two-column layout cleanly.
- **Subsequent uses** (§3, §4 worked examples): ordered-tuple notation `$\pi = (0.2,\, 0.4,\, 0.6,\, 0.1,\, 0.0)$` with ordering convention stated in §2: (MRGL, SLGT, ENH, MDT, HIGH).

## Figures (9 total)

| Fig | Script | Placed in | Type | What it shows |
|-----|--------|-----------|------|---------------|
| 1 | `fig_possibility_anatomy.py` | §2.2 | `figure` | Subnormal bar chart with Pi_max, H_Pi, N_c annotated |
| 2 | `fig_three_scenario.py` | §6.3 | `figure*` | Three scenarios side-by-side, scorecard values below |
| 3 | `fig_filling_gauge.py` | §6.2 | `figure` | Horizontal gauge bars for Scenario A |
| 4 | `fig_pignistic_bridge.py` | §3.1 | `figure*` | Raw pi → probability with ignorance bar + arrows |
| 5 | `fig_upper_lower_bounds.py` | §4.3 | `figure*` | [L,U] intervals on number line for threshold event |
| 6 | `fig_reliability_curves.py` | §5.1 | `figure` | Conditional hit rate vs N_c threshold |
| 7 | `fig_ig_decomposition.py` | §3.2 | `figure*` | Stacked bar IG decomposition (UNC, DSC, REL) |
| 8 | `fig_verification_lanes.py` | §5.2 | `figure*` | Three-lane flowchart schematic |
| 9 | `fig_ffion_advisory.py` | §7.3 | `figure*` | Structured JSON → LLM advisory mock-up |

## Python

Canonical constants in `scripts/style.py`:

```
PURPLE, GREEN, LIGHT_GREY, DARK_GREY, MID_GREY
SPC_CATEGORIES = ["MRGL", "SLGT", "ENH", "MDT", "HIGH"]
```

Scorecard computation canonical in `fig_three_scenario.py:compute_scorecard`.

### Known scenario mismatch

`07-worked-examples.tex` scenarios (A, B, C) use different pi values and observed categories than `fig_three_scenario.py`. The LaTeX table values are self-consistent. When reconciling, decide which set is canonical and update the other. Fig 2's caption notes this.

## Manuscript Status

### Done
- All 10 section files created with equations migrated from preprint
- 15 labelled equations, all cross-references resolve
- 9 figures generated and embedded with captions + in-text references
- Notation table (§2) with Form (raw/norm) and Eq. columns
- Ffion/LLM communication subsection (§7.3) with pipeline sketch
- ILS framed as probability-of-exceedance (50 ppb, 5 in. snowfall examples)

### Still placeholder (`% [PLACEHOLDER]`)
- §2 opening paragraph, §2.4 "Why Not Just Probabilities?" (3–4 paragraphs)
- §3 opening paragraph, §3.3 "Why Naive Normalisation Erases Information" (key argument, 2–3 paragraphs)
- §4 opening paragraph, ILS motivation paragraph
- §5 opening paragraph, sample-size discussion, diagnostic workflow
- §6 opening paragraph, meteorological scenario descriptions for A/B/C, interpretation paragraphs for scorecard table, bridge walkthrough computations
- §7 opening paragraph, all four subsection bodies (DS connections, beyond severe weather, software, limitations)
- §1 (introduction) — mostly placeholder with paper-outline paragraph done
- Missing citations: Dubois 2006, Smets 1990, Shafer 1976, Roulston & Smith 2002, Lawson 2024

## Related Work

- **Clyfar preprint**: `../preprint-clyfar-v0p9/` — the source material. Appendices C, E, F contain the framework.
- **Ffion** (Lawson, in prep.): LLM-mediated risk communication layer. Pipeline: GEFS ensemble → Monte Carlo clustering → JSON extraction → guarded LLM prompt (Claude, ~3 min inference) → tiered PDF advisories. §7.3 sketches this. Full details in `../brc-knowledge/` (see `scholarium/active-projects/clyfar/`, `ffrwd/PERSONAE.md` for Ffion persona definition).
- **Archive**: `archive/preprint-sections/` — verbatim copies of preprint 04, A3, A5, A6.
