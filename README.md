# Possibilistic Forecast Verification

**Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts**

John R. Lawson, Utah State University

---

A verification framework for subnormal possibility distributions, introducing:

- **Five-number scorecard**: alpha\*, eta, delta, H\_Pi, N\_c\*
- **Possibility-to-probability bridge**: converts to probabilities with explicit ignorance outcome
- **Interval log score**: logarithmic scoring for interval-valued forecasts
- **Three verification lanes**: deterministic, probabilistic, and native possibilistic

Running example: SPC convective outlook categories (MRGL, SLGT, ENH, MDT, HIGH).

## Build

**Manuscript** — compiled on Overleaf (XeLaTeX, TeX Live 2025). Locally: `latexmk -xelatex main.tex`.

**Figures** (all PNG at 300 DPI):
```bash
conda env create -f environment.yml
conda activate poss-verif
python scripts/generate_all.py        # figs 1–9
python scripts/fig_scorecard_table.py  # fig 10
python scripts/fig_performance_diagram.py  # fig 11
```

## Repo Layout

```
main.tex / preamble.tex     LaTeX master + macros (rho-class template)
sections/                    Manuscript sections (00-abstract through 09-backmatter)
rho-class/                   Template class files (do not modify rho.cls)
figures/                     Generated PNGs (from scripts/)
scripts/style.py             Shared palette, rcParams, SPC categories
scripts/fig_*.py             Individual figure generators
scripts/generate_all.py      Run figure scripts 1–9
archive/preprint-sections/   Reference copies of source appendices
```

## Related

Extracts and generalises the framework from Appendices C, E, F of the Clyfar preprint (sibling repo `../preprint-clyfar-v0p9/`).

## License

Text/figures: CC BY 4.0. Code: MIT. See [LICENSE](LICENSE).
