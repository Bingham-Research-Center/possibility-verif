# CLAUDE.md — possibility-verif

This repo is the **canonical source** for the possibilistic forecast verification scorecard. Equations and notation in `sections/05-native-verification.tex` override anything in sibling repos. Do not edit equations here to match sibling repos; edit sibling repos to match this.

## What this is

LaTeX manuscript defining the possibilistic verification framework:
"Possible, Yes; Ignorant, Perhaps: A Scorecard for Possibilistic Forecasts" (Lawson et al., in prep for JAS; arxiv-submission branch is the current working branch).

Python companion `../possverif` implements the equations in this repo exactly.

## Build

XeLaTeX/LuaLaTeX via the custom `rho-class/`. Primary compile command lives in the document; run from repo root. Do not hand-edit compiled artefacts.

## Repo layout

```
main.tex                          # Document spine
preamble.tex                      # Preamble, macros
sections/
  00-abstract.tex
  01-significance.tex
  02-introduction.tex
  03-possibility-primer.tex       # Possibility theory foundations
  04-pignistic-bridge.tex         # Pignistic bridge (possibility <-> probability)
  05-native-verification.tex      # SCORECARD CANONICAL SOURCE (primary reference)
  06-tripartite-value.tex         # Three-component value proposition
  07-worked-examples.tex
  08-discussion.tex
  09-backmatter.tex
paperpile.bib                     # 53-entry trimmed bibliography
rho-class/                        # Custom LaTeX document class
figures/                          # Manuscript figures
```

## Canonical notation (authoritative)

The eight terms below appear across `../possverif`, `../python-nsf-dprog`, and `../latex-nsf-dprog`. When editing those sibling repos, grep for drift against this table.

| Code term               | Paper symbol | Definition                                      |
|-------------------------|--------------|--------------------------------------------------|
| `raw`                   | π            | Raw possibility distribution (can be subnormal) |
| `normalized`            | π̄            | π / m, max-normalised shape                     |
| `commitment`            | m            | max(π), peak possibility                        |
| `ignorance`             | H_Π          | 1 − m, unspent plausibility budget              |
| `depth_of_truth`        | α*           | π̄(c_obs)                                        |
| `diffuseness`           | η            | (1/K) Σ_c π̄(c)                                  |
| `support_margin`        | δ            | α* − η                                          |
| `conditional_necessity` | N_c*         | 1 − max_{ω≠c_obs} π̄(ω)                          |

Proposal-local term, **not** in the five-number scorecard but often discussed alongside it:

| Term                          | Symbol         | Definition                                                                                               |
|-------------------------------|----------------|----------------------------------------------------------------------------------------------------------|
| `bracketing interval width`   | Π(A) − N(A)    | Range of probabilities for event A compatible with π. Property of a single event. **Distinct from H_Π.** |

## Five-number scorecard (from §5 lines 289-300)

Given a subnormal possibility distribution π over Ω with m = max(π) > 0, normalised form π̄ = π/m, and observed outcome c_obs:

```
α*   = π̄(c_obs)                     ∈ [0, 1]
η    = (1/K) Σ_c π̄(c)                ∈ [1/K, 1]
δ    = α* − η                        ∈ [−(1 − 1/K), 1 − 1/K]
H_Π  = 1 − m                         ∈ [0, 1)           (uses raw π)
N_c* = 1 − max_{ω ≠ c_obs} π̄(ω)      ∈ [0, 1]
```

**H_Π is the ONLY scorecard metric that uses the raw distribution** (see §5 line 238-240). All others use the normalised shape π̄. This distinction is load-bearing: conflating H_Π with any quantity derived from π̄ is a correctness error, not a naming preference.

Canonical plain-language interpretations (from §5 lines 275-286):

- **α* (depth-of-truth)**: how much normalised possibility did the observed category receive? α* = 1 when truth is the peak category.
- **η (diffuseness)**: how spread out was the normalised distribution? Ensemble-spread / sharpness analogue.
- **δ (support margin)**: did the system give more support to truth than to an average category? Brier-type DSC / resolution analogue.
- **H_Π (ignorance)**: how much of the plausibility budget did the system leave unassigned? H_Π = 0: fully confident. H_Π → 1: near-total ignorance.
- **N_c\* (conditional necessity of truth)**: was truth a clear winner? Dominance margin quantifying how far truth led its runners-up.

## Companion repos

| Repo             | Path                  | Role                                                          |
|------------------|-----------------------|---------------------------------------------------------------|
| possverif        | `../possverif`        | Python implementation (agrees exactly with this manuscript)   |
| python-nsf-dprog | `../python-nsf-dprog` | NSF proposal experiments on Lorenz-63 (consumes possverif)    |
| latex-nsf-dprog  | `../latex-nsf-dprog`  | NSF proposal narrative (consumes figures from python-nsf-dprog) |

## Drift prevention

These non-canonical coinages have appeared in sibling repos during past editing sessions. Treat each as a drift flag; when you see them, cross-check against the notation table above:

- **"possibilistic ignorance = Π(A) − N(A)"** → WRONG. Ignorance is H_Π = 1 − m across the whole raw distribution. Π(A) − N(A) is the *bracketing interval width* for a single event A.
- **"specificity"** → non-canonical. The canonical scorecard term is diffuseness (η). Use "support margin" (δ) or "diffuseness" (η) depending on which concept is meant.
- **"normalized commitment"** → non-canonical. N_c* is *conditional necessity of truth*, not "normalized commitment". Commitment is m; there is no "normalized commitment" in the scorecard.
- **"possibilistic entropy" applied to H_Π** → wrong. H_Π is ignorance (unspent plausibility budget), not a Shannon-style entropy. A separate possibilistic entropy does exist (Hartley-style) but is not the same object.
- **α\* described as "overall possibilistic skill"** → wrong. α* is depth-of-truth, a single normalised-possibility value, not an aggregated skill score.
