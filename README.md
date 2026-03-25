# Possibilistic Forecast Verification

**Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts**

John R. Lawson, Utah State University

---

A verification framework for subnormal possibility distributions, introducing:

- **Five-number scorecard**: alpha\*, eta, delta, H\_Pi, N\_c\*
- **Tripartite pignistic bridge**: possibility-to-probability with explicit ignorance
- **Interval log score**: logarithmic scoring for interval-valued forecasts
- **Three verification lanes**: deterministic, probabilistic, and native possibilistic

Running example: SPC convective outlook categories (MRGL, SLGT, ENH, MDT, HIGH).

## Build

**Manuscript** — compiled on Overleaf (XeLaTeX). Locally: `latexmk -xelatex main.tex`.

**Figures**:
```bash
conda env create -f environment.yml
conda activate poss-verif
python scripts/generate_all.py
```

## Repo Layout

```
main.tex / preamble.tex     LaTeX master + macros (rho-class template)
sections/                    Manuscript sections (00-abstract through 09-backmatter)
rho-class/                   Template class files (do not modify rho.cls)
figures/                     Generated PDFs (from scripts/)
scripts/style.py             Shared palette, rcParams, SPC categories
scripts/fig_*.py             Individual figure generators
scripts/generate_all.py      Run all figure scripts
archive/preprint-sections/   Reference copies of source appendices
```

## Related

Extracts and generalises the framework from Appendices C, E, F of the Clyfar preprint (sibling repo `../preprint-clyfar-v0p9/`).

## License

Text/figures: CC BY 4.0. Code: MIT. See [LICENSE](LICENSE).
