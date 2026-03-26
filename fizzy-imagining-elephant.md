# Manuscript Review and Revision Plan

## Context

Full review of "Possible, yes; ignorant, perhaps" targeting JAS (AMetSoc).
Manuscript is ~75% prose-complete; scaffold, equations, figures, and tables are 100%.
Goal: identify bugs, fill gaps with low-verbosity high-information prose, and
prepare for submission.

---

## Part A: Bugs and Errors (fix before anything else)

### A1. IG terminology collision (CRITICAL)

**The problem:** "IG" is used for two different quantities in the same section
(04-pignistic-bridge.tex):

- **Eq. 6** defines IG as *information gain*: `IG = D_KL(o||clim) - D_KL(o||fcst)`.
  Higher = better. Positive means "forecast beat climatology."
- **Eq. 7** defines `IG_decomp = UNC - DSC + REL`, which is the **log score**
  (= mean surprise of the forecast). Lower = better.

These are *related but not the same*:
```
IG_gain = UNC - log_score = UNC - (UNC - DSC + REL) = DSC - REL
```

**Fig 7 caption error:** Says "the sharp-correct scenario achieves the highest IG"
but the annotated value (0.57) is the *lowest* bar — because the figure plots the
log score (lower = better), not information gain (higher = better). The caption
also says "sharp-wrong scenario shows negative IG" but all annotated values are
positive (the figure shows the log score, not the gain).

**Actual IG (gain) values** would be: Sharp-Correct = +1.75, Hedged-Correct = +1.00,
Sharp-Wrong = -0.75, Hedged-Wrong = -0.35, Climatology = 0.00.

**Fix options (need user decision):**
- **(a)** Rename the decomposition quantity. Call Eq. 7 the "log score decomposition"
  and reserve "IG" for the gain (Eq. 6). The figure would show "Log Score = 0.57"
  annotations. The naming-collision note about IGN/H_Pi still applies — just call
  the log score "LS" or keep "IG" but add "lower is better" explicitly.
- **(b)** Change the figure to plot actual IG (= DSC - REL), with the UNC baseline
  at zero. Annotate "IG = +1.75" etc. Caption becomes accurate as-is.
- **(c)** Keep current figure but fix the caption and add a clarifying sentence
  after Eq. 7: "Note that IG_decomp is the forecast's mean log score (lower is
  better); the information gain of Eq. 6 equals UNC minus IG_decomp."

**Recommendation:** Option (c) is minimal disruption. Option (b) is cleanest for the
reader but requires regenerating the figure.

### A2. `Smets1990-MISSING` citation (04-pignistic-bridge.tex:47)

Replace with real key. The correct reference is:
- Smets, P. (1990). Constructing the pignistic probability function in a context
  of uncertainty. *Proc. 5th Int. Conf. Information Processing and Management of
  Uncertainty (IPMU-90)*, Lecture Notes in Computer Science **521**, 29-39.
- Or: Smets, P. and Kennes, R. (1994). The transferable belief model.
  *Artificial Intelligence*, 66, 191-234.

Need to add the BibTeX entry to paperpile.bib and replace the key in the text.

### A3. Fig 2 / Table 4 scenario-value mismatch

The figure (from fig_three_scenario.py) and the LaTeX table (07-worked-examples.tex)
use *different* pi vectors for the same named scenarios. Examples of divergence:

| Metric        | Fig (Hedged-Correct) | Table (Scenario B) |
|---------------|---------------------|--------------------|
| eta           | 0.691               | 0.491              |
| delta         | 0.309               | +0.509             |
| Nc*           | 0.091               | 0.273              |

The caption notes this, but a reviewer will flag it as confusing. **Recommendation:**
align the figure's pi values with the table's canonical values so the reader can
cross-reference without caveats.

### A4. Oxford English spelling (-ize/-ization)

The manuscript currently uses British -ise/-isation throughout ("normalisation",
"normalise", "organised"). Oxford English with -ize requires: "normalization",
"normalize", "organized", etc. This is a global find-and-replace across all .tex
files. (Words like "supervise", "comprise", "advertise" that etymologically require
-ise are unaffected.)

---

## Part B: Mathematical / Conceptual Issues to Address

### B1. ILS "optimistic" scoring not flagged

The preprint A6 explicitly says ILS uses "optimistic verification" — crediting the
best-case bound. The current paper (05-native-verification.tex) does not use this
term. A JAS reviewer will ask: "Is ILS a proper scoring rule?" It is not strictly
proper (optimistic scoring can be gamed by widening the interval). Add 1-2 sentences
acknowledging this and noting that the width penalty (through H_Pi) partially
mitigates gaming.

### B2. IRLS: keep or cut?

IRLS (§4.4) is formally defined but explicitly deferred to future work. A reviewer
may ask why it appears at all. Options:
- **Keep** with a note that it completes the theoretical framework (ILS is the
  single-threshold case; IRLS generalises to all thresholds).
- **Move** to an online supplement or appendix.
- **Cut** entirely and mention it as future work in §7.5.

**Recommendation:** Keep (it is short, and removing it loses the CRPS analogy), but
add one sentence in the IRLS subsection connecting it to CRPS explicitly.

### B3. Possibilistic climatology: consonance assumption

§4.5 constructs climatology as a consonant (nested) distribution. This is a
non-trivial modelling choice — not all applications produce consonant forecasts.
The PLACEHOLDER comment at line 363-365 notes this. Needs 2-3 sentences explaining
why consonance is the default (it is the least-committed possibility distribution
consistent with a CDF) and when alternatives might be needed.

### B4. Eq. 7 relationship to Eq. 6 needs explicit statement

Even beyond the naming issue (A1), the mathematical relationship between Eqs. 6
and 7 is never stated. Add after Eq. 7:
"When the baseline f_1 is climatology, D_KL(o || clim) = UNC, and Eq. 6 reduces
to IG = DSC - REL."

---

## Part C: Placeholder Prose — Prioritised by Submission Criticality

### Tier 1: BLOCKING (paper cannot be submitted without these)

**C1. §1 Introduction** (~8-12 paragraphs needed)
- Opening: why hazard forecasting needs richer uncertainty (SPC context)
- "Ignorance erasure" argument (2 paras): central thesis
- Literature review: possibility theory foundations (Dubois & Prade 1988, Zadeh 1978),
  fuzzy logic in met, verification scoring rules (Roulston & Smith 2002, Lawson 2024,
  Brier 1950, Murphy 1973, Gneiting & Raftery 2007), imprecise probability (Shafer
  1976, Smets 1990, Walley 1991)
- Gap statement
- Source: preprint §1 + new framing for standalone paper

**C2. §6 Worked Examples interpretation** (~10 paragraphs)
- Meteorological scenario descriptions for A, B, C (3 x 1 para)
- Scorecard interpretation (3-4 paras comparing A vs B vs C)
- Bridge walkthrough (probability vectors + IG for each scenario)
- ILS walkthrough (threshold A_T = {ENH, MDT, HIGH} across all three)

**C3. §7.1 DS connections** (2-3 paras)
- Already sketched in §2.3 and PLACEHOLDER comments
- Formalise: Pi ↔ plausibility, Nc ↔ belief, H_Pi has no DS analogue

**C4. §7.5 Limitations and future directions** (2-3 paras)
- IRLS deferred, sample-size requirements, consonance assumption, open-world
  assumption, multivariate extension, conformal prediction connection

### Tier 2: HIGH PRIORITY (strengthen paper significantly)

**C5. §2.4 "Why Not Just Probabilities?"** (3-4 paras)
- Key motivational section; arguments already outlined in PLACEHOLDER
- Interval [N(A), Pi(A)] vs single p(A); H_Pi has no probabilistic counterpart;
  SPC language maps to possibility; bridge is one-way (info lost going prob→poss)

**C6. §2 opening paragraph** (1 para)
- Frame as self-contained primer, no fuzzy-logic prerequisite

**C7. §4 opening paragraph** (1 para)
- Motivate native verification: bridge is lossy, need direct evaluation

**C8. §5 opening paragraph** (1 para)
- Motivate: "why do you need all three components?"

**C9. §6 opening paragraph** (1 para)

**C10. §7 opening paragraph** (1 para) — summarise contributions

**C11. §7.2 Beyond severe weather** (2 paras)
- Air quality, wildfire, flood, climate scenarios; domain-agnostic framing

**C12. §7.4 Software availability** (1 para)
- Python package, repo URL, key modules

### Tier 3: POLISH (add if time permits)

**C13.** §3.2 IG opening paragraph (meteorological analogue for IG → Brier decomp)
**C14.** §3.1 TBM connection (1-2 sentences after line 55)
**C15.** §4.1 met analogue (1 sentence: raw/norm ≈ ensemble-mean/rank-histogram)
**C16.** §4.3 ILS motivation paragraph (why log > Brier for rare events; adapt A6)
**C17.** §4.4 IRLS–CRPS analogue sentence
**C18.** §5.1 sample-size note (1 para)
**C19.** §2.2 opening paragraph (why subnormality matters operationally)
**C20.** Meteorological scenario descriptions for Examples 1 and 2 in §2.2

### Tier 4: CITATIONS to weave in

- Dubois 2006 → §2.1 (bracketing property, line 67-68)
- Shafer 1976 → §2.3 (DS analogy, line 205)
- Roulston & Smith 2002 → §3.2 (IG framework, line 114)
- Lawson 2024 → §3.2 (IG formalization, line 114) and §1 (lit review)
- Smets 1990 (once real key added) → §3.1 (already cited, fix key)

---

## Part D: Figure Review

### D1. Fig 7 (IG decomposition) — see A1 above for the labeling bug

Visual logic is correct:
- Grey (UNC) is the base layer = log₂(5) = 2.32 bits for all scenarios
- Purple (DSC): positive DSC overlaps grey from base (skill removes uncertainty);
  negative DSC sits above grey (anti-skill inflates score) — correctly implemented
- Green (REL): penalty added on top of (UNC - DSC)
- Dotted line = UNC baseline, NOT "IG = 0"

The fix from CLAUDE.md (negative-DSC bar placement) is correctly applied.

**Answer to user's question:** The figure's stacking logic is mathematically sound.
Bad forecasts DO show information loss: their total bar (UNC - DSC + REL) exceeds
the UNC baseline. The dotted line is "UNC = log₂5" (the climatological log score),
not "IG = 0". The only bug is the caption/label terminology (A1 above).

### D2. Fig 2 (three scenarios) — see A3 above for value mismatch

Otherwise clear and effective. The green/purple colour scheme works well.

### D3. Fig 11 (performance diagram)

Excellent. All five metrics encoded simultaneously. The quadrant labels ("Sharp
correct", "Diffuse wrong", etc.) are helpful. One minor issue: the "Sharp wrong"
label in lower-right overlaps with the delta=-0.2 contour line — slightly hard to
read. The colourbar label says "Ignorance H_Π" which is correct.

### D4. Fig 10 (scorecard table)

Clear ECMWF-style layout. The v2.0 H_Π degradation (red triangle) is visible and
the caption explains it well. Lane groupings are clear.

### D5. Fig 8 (verification lanes)

Clean schematic. Lane 2 box says "IG = UNC - DSC + REL" — subject to the same
naming issue as A1 (this is the log score, not gain). If A1 is resolved by renaming,
this figure also needs updating.

### D6. Fig 4 (pignistic bridge)

Effective two-panel layout. Arrow annotations showing proportional redistribution
are clear. The grey IGN bar on the right panel is well-labeled.

### D7. Figs 1, 3, 5, 6, 9

All appear correct and well-designed. No issues found.

---

## Part E: Style and Consistency

### E1. Spelling normalisation (-ize)

Global replacement needed (see A4). Affects ~50+ instances across all .tex files.

### E2. Terminology consistency

- "possibility-to-probability bridge" used consistently (good; previous sessions
  renamed from "tripartite pignistic")
- "ignorance" vs "subnormality": both used, but "ignorance" is the measure H_Pi
  while "subnormality" is the property of having max(pi) < 1. This distinction is
  correct and should be maintained.

### E3. Notation convention

Tuple ordering (MRGL, SLGT, ENH, MDT, HIGH) consistently applied from §3 onward.
Cases format in §2 and §6 as documented. No issues.

### E4. Figure captions

Generally thorough and self-contained. One exception: Fig 6 (reliability curves)
does not mention that the data is synthetic. Add "using synthetic verification
data" to the caption.

### E5. "Significance Statement" placement

Currently §01 (after abstract, before introduction). JAS requires this. Placement
is correct.

---

## Part F: Verification / Testing

After all edits:

1. **LaTeX compilation:** `latexmk -xelatex main.tex` locally (tools available at
   ~/.local/bin/). Check for:
   - No undefined references (grep for `??` in PDF or `LaTeX Warning` in log)
   - No missing citations (grep for `Citation.*undefined` in log)
   - No overfull hboxes in two-column layout

2. **Figure regeneration** (if A3 alignment chosen):
   - Update fig_three_scenario.py to use Table 4's canonical pi values
   - Run `python scripts/generate_all.py` + separate scripts for figs 10-11
   - Verify all 11 PNGs regenerated

3. **If A1 option (b) chosen:** Regenerate fig_ig_decomposition.py with IG = DSC - REL
   annotations and updated stacking logic. Also update fig8 Lane 2 label.

4. **Spelling:** grep for `-isation`, `-ised`, `-ising` across all .tex files to
   catch stragglers after global replace.

5. **Cross-reference audit:** Search for `\ref{` and verify all labels resolve.

---

## Decisions (from user)

- **A1 (IG fix):** Redesign Fig 7 to plot actual IG = DSC - REL with baseline at
  zero. Positive bars = skill, negative = worse than climo. Also update Fig 8
  Lane 2 label and add clarifying sentence after Eq. 7.
- **A3 (Fig 2):** Align fig_three_scenario.py with Table 4's canonical pi values.
  Regenerate figure. Remove the caveat caption sentence.
- **Scope:** All Tier 1 + Tier 2 placeholders (comprehensive session).
- **PDF:** Attempt local xelatex compilation.

## Execution Order

### Phase 1: Bugs and figure fixes
1. Fix `Smets1990-MISSING` — add BibTeX entry, replace citation key
2. Redesign `fig_ig_decomposition.py` — plot IG = DSC - REL, baseline at 0,
   positive = good, negative = bad. Update annotations, legend, caption.
3. Update `fig_three_scenario.py` — use Table 4 pi values:
   - A: (0.00, 0.05, 0.15, 0.90, 0.10), obs=MDT
   - B: (0.10, 0.40, 0.55, 0.30, 0.00), obs=ENH
   - C: (0.85, 0.10, 0.00, 0.00, 0.00), obs=MDT
4. Regenerate affected figures (figs 2, 7; check if fig 5 uses same scenarios)
5. Update Fig 8 Lane 2 label if needed (may need fig_verification_lanes.py edit)
6. Add clarifying sentence after Eq. 7 in 04-pignistic-bridge.tex
7. Fix Fig 7 caption in 04-pignistic-bridge.tex
8. Remove Fig 2 caveat sentence from 07-worked-examples.tex caption
9. Global -ise → -ize spelling pass across all .tex files (A4)

### Phase 2: Tier 1 prose (blocking for submission)
10. §1 Introduction (02-introduction.tex) — write opening, ignorance-erasure
    argument, literature review, gap statement (~8-12 paras)
11. §6 Worked Examples (07-worked-examples.tex) — meteorological scenario
    descriptions, scorecard interpretation, bridge walkthrough, ILS walkthrough
12. §7.1 DS connections (08-discussion.tex)
13. §7.5 Limitations and future directions (08-discussion.tex)

### Phase 3: Tier 2 prose (strengthen paper)
14. §2.4 "Why Not Just Probabilities?" (03-possibility-primer.tex)
15. Section opening paragraphs: §2, §3.2, §4, §5, §6, §7
16. §7.2 Beyond severe weather (08-discussion.tex)
17. §7.4 Software availability (08-discussion.tex)

### Phase 4: Mathematical fixes + citations
18. B1: Add ILS "optimistic scoring" note (05-native-verification.tex)
19. B2: Add IRLS-CRPS sentence (05-native-verification.tex)
20. B3: Possibilistic climatology consonance note (05-native-verification.tex)
21. B4: Eq. 6/7 relationship sentence (04-pignistic-bridge.tex)
22. Weave citations: Dubois 2006, Shafer 1976, Roulston & Smith 2002, Lawson 2024
23. Tier 3 polish items (C13-C20) as time permits

### Phase 5: Style + compile
24. Fig 6 caption: add "synthetic data" note
25. Final spelling/consistency pass
26. Attempt local `latexmk -xelatex main.tex`
27. Check log for undefined refs, missing citations, overfull hboxes

### Files to modify
- `scripts/fig_ig_decomposition.py` — redesign IG figure
- `scripts/fig_three_scenario.py` — align pi values with table
- `scripts/fig_verification_lanes.py` — update Lane 2 label (if hardcoded)
- `sections/00-abstract.tex` — minor polish after all sections done
- `sections/02-introduction.tex` — fill §1 (largest new prose)
- `sections/03-possibility-primer.tex` — §2 opening, §2.4
- `sections/04-pignistic-bridge.tex` — Eq. 7 clarification, Fig 7 caption, §3.2 opening, Smets citation fix
- `sections/05-native-verification.tex` — §4 opening, ILS note, IRLS note, climatology note
- `sections/06-tripartite-value.tex` — §5 opening
- `sections/07-worked-examples.tex` — §6 opening + interpretation + walkthroughs, Fig 2 caption fix
- `sections/08-discussion.tex` — §7 opening, §7.1, §7.2, §7.4, §7.5
- `paperpile.bib` — add Smets 1990 entry
