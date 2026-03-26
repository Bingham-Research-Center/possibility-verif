# How to Start a New Paper from the Rho Template

Guide for reusing the Rho LaTeX class (v2.1.0) and project structure from an existing manuscript. Written from experience migrating content into this template; the specifics reference Rho's quirks, but the workflow generalizes.

---

## Repo Structure to Copy

```
your-new-paper/
  main.tex              # Document root: title, authors, \input{} chain
  preamble.tex          # YOUR packages, macros, color theme calls
  paperpile.bib         # Start empty; export from Paperpile later
  rho-class/            # Copy this directory verbatim. Do not modify.
    rho.cls
    rhoenvs.sty
    rhobabel.sty
  sections/             # One file per section, numbered for order
    00-abstract.tex
    01-significance.tex
    02-introduction.tex
    ...
    09-backmatter.tex
  figures/              # All figure PNGs (not PDFs; see Gotchas)
  scripts/              # Figure-generation scripts
    style.py            # Shared constants, matplotlib config
    generate_all.py     # Runner for all figure scripts
  fonts/                # Bundled OTF fonts for figure consistency
```

## Step-by-Step

### 1. Copy the skeleton

Copy `rho-class/` as-is. Copy `main.tex` and `preamble.tex` as starting points. Gut the content but keep the structure.

### 2. Edit `main.tex`

Replace these fields with your own:

```latex
\journalname{Your Target Journal}
\title{Your Title}
\author[1]{Your Name}
\affil[1]{Your Institution}
\leadauthor{Your Name}
\footinfo{Short description}
\institution{Your Institution}
\theday{\today\newline{}Submitted to Your Journal}
\corres{Correspondence to Your Name}
\email{you@example.com}
```

Keep these booleans:
```latex
\setbool{rho-abstract}{true}
\setbool{corres-info}{true}
```

Keep the document body pattern:
```latex
\input{preamble}
% ... fields above ...
\input{sections/00-abstract}
\begin{document}
    \maketitle
    \thispagestyle{firststyle}
    \input{sections/01-significance}
    \input{sections/02-...}
    ...
    \bibliographystyle{ametsocV6}   % or your journal's .bst
    \bibliography{paperpile}
\end{document}
```

The abstract MUST be `\input`-ed before `\begin{document}` -- Rho renders it in the title block.

### 3. Edit `preamble.tex`

This is where YOUR customizations go. Structure:

```latex
\usepackage[english]{babel}    % Required by rhobabel.sty

%%% Your packages (check rho.cls first -- it already loads many)
\usepackage{natbib}            % Or whatever your journal needs
\usepackage{...}

%%% Your macros
\newcommand{\yourmacro}{...}

%%% Color theme (pick one from rhoenvs.sty or define your own)
\colorthemeSteelBlue           % Sets rhocolor for rhoenv boxes
% If you want a second color for rationale boxes:
% \colorthemeForestGreen       % Sets rationalecolor
```

**Packages already loaded by rho.cls** (do NOT reload):
amsmath, booktabs, enumitem, xcolor, hyperref, graphicx, caption, lettrine, tikz, tcolorbox, mdframed, cleveref, subcaption, authblk, geometry, fancyhdr, titlesec, microtype

### 4. Set your color theme

In `rhoenvs.sty`, the `\colortheme*` commands define `rhocolor` (for `rhoenv` boxes, hyperlinks, section headings) and optionally `rationalecolor`. You can:

- Use a built-in: `\colorthemeSteelBlue`, `\colorthemeMidnightBlue`, etc.
- Add your own in `rhoenvs.sty` following the pattern:
  ```latex
  \newcommand{\colorthemeMyColor}{\definecolor{rhocolor}{HTML}{HEXCODE}}
  ```
- Call it in `preamble.tex`.

### 5. Create section files

One `.tex` per section in `sections/`. Each file starts with:
```latex
% !TEX root = ../main.tex
\section{Your Section Title}\label{sec:your_label}
```

Use `% [PLACEHOLDER]` comments for sections you haven't written yet. This lets the document compile at every stage.

### 6. Environments available

```latex
% Purple (rhocolor) box -- use for definitions, theorems, key results
\begin{rhoenv}[Title]
  Content here.
\end{rhoenv}

% Green (rationalecolor) box -- use for intuition, rationale sidebars
\begin{rationaleenv}[Intuition]
  Accessible explanation here.
\end{rationaleenv}
```

### 7. Figures

**Use PNG, not PDF.** XeTeX's xdvipdfmx backend crashes silently on matplotlib PDF transparency (`/SMask`, `/ca`, `/CA`). No `!` error in the log -- just "No PDF produced" on Overleaf. This cost hours to diagnose.

In your `scripts/style.py`:
```python
FIG_FORMAT = "png"
DPI = 300
```

For font consistency between figures and document, bundle TeX Gyre Heros OTFs in `fonts/` and register them in `style.py` before setting rcParams. Rho uses `\RequirePackage[scaled]{helvet}` which maps to TeX Gyre Heros under XeLaTeX.

---

## Gotchas (Learned the Hard Way)

| Issue | Symptom | Fix |
|-------|---------|-----|
| **PDF figures crash XeTeX** | "No PDF produced" on Overleaf, no `!` error | Use PNG. Set `FIG_FORMAT = "png"` in style.py |
| **babel spanish** | `! You haven't defined the language 'spanish' yet` | `tlmgr install hyphen-spanish` (rhobabel.sty needs it) |
| **Slow compilation** | 30-60s per pass | rho.cls loads circuitikz, chemfig, matlab-prettifier, lipsum. Do not remove them -- just accept the slowness |
| **Abstract placement** | Abstract missing or in wrong spot | `\input{sections/00-abstract}` must come BEFORE `\begin{document}` |
| **Duplicate package loads** | Option clash errors | Check rho.cls before adding packages to preamble.tex. graphicx, xcolor, hyperref, enumitem are already loaded |
| **\graphicspath** | Figures not found | rho.cls sets `\graphicspath{{figures/}{./}}` -- just use bare filenames: `\includegraphics{fig1_name.png}` |
| **Two-column floats** | `figure*` or `table*` for full-width; `figure` for single-column | Full-width floats often land on the next page. Use `[t]` placement |
| **Font mismatch in figs** | Figure labels look different from caption text | Bundle TeX Gyre Heros OTFs, register in matplotlib. It's the free clone of Helvetica that rho.cls uses |
| **Bibliography style** | Change `ametsocV6` to your journal's .bst | In `main.tex`: `\bibliographystyle{yourstyle}` |

## Compilation

```bash
# Local (requires XeLaTeX)
latexmk -xelatex main.tex

# Or manual sequence
xelatex main && bibtex main && xelatex main && xelatex main

# Overleaf: set compiler to XeLaTeX in project settings
```

If you need pdflatex instead of xelatex, remove `\RequirePackage[scaled]{helvet}` from rho.cls and replace with a pdflatex-compatible font package. But the template is designed for XeLaTeX.

## Citation Workflow (Paperpile)

If using Paperpile for reference management:
- Export `.bib` from Paperpile into `paperpile.bib`
- Paperpile auto-generates keys like `AuthorYEAR-xx`
- For references not yet in Paperpile, use `-MISSING` suffix keys (e.g., `Smith2020-MISSING`) with stub bib entries so the document compiles
- Track these in a `MISSING-REFS.md` so you can batch-add them later
- After adding to Paperpile and re-exporting, global find-replace the MISSING keys

## Minimal Checklist for a New Paper

- [ ] Copy `rho-class/` directory verbatim
- [ ] Copy and gut `main.tex`, `preamble.tex`
- [ ] Set title, authors, affiliations, journal name
- [ ] Pick color theme in `preamble.tex`
- [ ] Create `sections/` with numbered `.tex` files
- [ ] Set `\bibliographystyle` to your journal's .bst
- [ ] Add `\usepackage[english]{babel}` to preamble (or install hyphen-spanish)
- [ ] Set Overleaf compiler to XeLaTeX
- [ ] Use PNG figures only
