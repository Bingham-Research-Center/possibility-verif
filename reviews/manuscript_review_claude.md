# Manuscript Review: "Possible, Yes; Ignorant, Perhaps"

**Reviewer:** Claude (automated critical review)
**Date:** 2026-03-29
**Scope:** Human readability, conceptual clarity, methodological rigor. All `.tex` sections, figures (visual), and scripts verified.

---

## Executive Summary

This paper introduces a self-contained verification framework for subnormal possibilistic forecasts, centred on a five-number scorecard and a probability conversion that preserves the ignorance signal. The framework is original, well-motivated, and mathematically coherent: every equation was verified numerically against both code and worked examples. The three-lane verification design (categorical, probabilistic, native possibilistic) is a genuine contribution. The primary issues are editorial: a duplicate paragraph in the Discussion, an inconsistency between "two-year" and "three-year" reforecast descriptions, and one structural property of the scorecard (N_c\* = 0 whenever alpha\* < 1) that should be disclosed. A missing script dependency prevents full figure reproducibility. No fundamental methodological flaws were found.

---

## Must-Fix Issues

| # | Severity | Location | Issue | Why It Matters | Suggested Fix |
|---|----------|----------|-------|----------------|---------------|
| 1 | **High** | `08-discussion.tex:23-32` | **Duplicate paragraph.** The domain-agnostic claim ("Although SPC...the framework applies to any finite Omega...") is stated in nearly identical wording in two consecutive paragraphs. | A careful reader will notice this as an editing artifact, undermining confidence in the manuscript's polish. | Delete lines 28-32 ("Although SPC convective outlook categories served as the running example, the framework is domain-agnostic...without modification.") — the first paragraph already covers this. Fold the "Extension to continuous..." sentence into the preceding paragraph if desired. |
| 2 | **High** | `05-native-verification.tex:236` vs `:262`; `07-worked-examples.tex:91`; `scripts/fig_categorical_scores.py:87` | **2-year vs 3-year reforecast inconsistency.** Body text says "single synthetic reforecast (n = 730 days, two years)." The performance-diagram caption says "three-year." The categorical-scores caption says "three-year." The categorical script calls `generate_reforecast(n_years=3)`. The default in `generate_reforecast()` is `n_years=2`. | Claims about a "single shared reforecast" are contradicted: the categorical figure uses different data (1095 days) than the performance diagram (730 days). Reviewers checking reproducibility will flag this immediately. | Pick one value (recommend 2 years / 730 days for consistency with body text). Update `fig_categorical_scores.py:87` to `n_years=2`. Change both figure captions to "two-year." |
| 3 | **High** | `scripts/fig_performance_diagram.py:246` | **Missing dependency `fig_perf_iterate.py`.** The performance diagram script imports `from fig_perf_iterate import get_data, v3b, v4b`, but this file does not exist in the repository. | The two main diagnostic figures (`perf_hexbin_trajectory.png`, `commitment_diagram.png`) cannot be reproduced from the distributed repository. This violates the data/code availability claim in `09-backmatter.tex:9-14`. | Add `fig_perf_iterate.py` to the repository, or inline its logic into `fig_performance_diagram.py`. |
| 4 | **Medium** | `05-native-verification.tex:226-229` | **Overclaim: "no single metric can be improved without degrading another."** This is stated as fact but not proven. Counterexample: sharpening a distribution that already peaks at truth (reducing non-truth pi' values) improves delta without degrading alpha\*, H_Pi, or N_c\*. | A reviewer with optimisation background will construct a counterexample in minutes. The claim weakens the paper's credibility on a point that doesn't need to be this strong. | Soften to: "The multi-metric design resists trivial gaming strategies: for instance, flooring all values at epsilon to avoid alpha\* = 0 inflates eta on every forecast, yielding a net-negative effect across the verification sample (Section 7.4)." Delete the first clause about no-single-metric-improvable. |
| 5 | **Medium** | `05-native-verification.tex:182-192` | **N_c\*-alpha\* structural dependence undisclosed.** From the definition, N_c\* = 1 - max(pi'[w != c_obs]). When c_obs is not the mode, max(pi'[w != c_obs]) = 1 (the mode itself), so N_c\* = 0. Thus N_c\* is always zero whenever alpha\* < 1. The paper presents them as complementary but never states this floor constraint. | A reader may expect N_c\* to provide independent diagnostic information across all forecasts. In reality it is informative only on the subset where truth is the mode. The "truth-finding pair" discussion in Section 7.4 implicitly relies on this but doesn't state it. | Add after Eq. (eq:nc_star): "Note that N_c\* > 0 only when c_obs coincides with the mode of pi'; otherwise max(pi'[w != c_obs]) = 1 by construction, giving N_c\* = 0. This means N_c\* refines the alpha\* = 1 cases by quantifying how dominant the truth was among covered scenarios, while contributing no additional information when alpha\* < 1." |
| 6 | **Medium** | `04-pignistic-bridge.tex:33` vs `scripts/fig_pignistic_bridge.py:130` | **Formula notation mismatch between text and figure.** Manuscript equation: p_i = pi_i * (1 - H_Pi) / sum(pi_j). Figure annotation: p_i = pi_i * Pi_max / Sigma(pi). These are mathematically equivalent ((1-H_Pi) = Pi_max = max(pi)), but a reader cross-referencing will see different notation. | Creates unnecessary friction for a reader verifying the equation against the figure. | Use the same form in both. Recommend the manuscript form (1 - H_Pi) since it makes the ignorance reservation explicit — update `fig_pignistic_bridge.py:130` accordingly. |

---

## Should-Fix Issues (prioritised)

### 1. Terminology inconsistency for *m*
**Location:** `03-possibility-primer.tex:92` (notation table) vs `07-worked-examples.tex:216` (scorecard table)

The notation table calls *m* "Subnormality" (the maximum value), but Table `tab:scorecard_comparison` calls it "commitment." These are the same quantity with conflicting names. Additionally, *m* is not the degree of subnormality (that is H_Pi = 1 - m), so "subnormality" is misleading.

**Fix:** Standardise on "commitment" (or "peak commitment") throughout. Update the notation table entry to: "*m* — Commitment: max_omega pi(omega)."

### 2. Dead notation nu_c
**Location:** `03-possibility-primer.tex:224`

The alternative notation nu_c is introduced for conditional necessity alongside N_c but never used again in the manuscript.

**Fix:** Remove ", nu_c" from the enumerated item.

### 3. DSC vs RES terminology may confuse
**Location:** `04-pignistic-bridge.tex:135-137`

The paper renames "resolution" (RES) to "discrimination" (DSC) to avoid NWP confusion, but in the broader verification literature, discrimination and resolution are related but distinct concepts (e.g., Murphy 1993). A reader versed in the Brier decomposition may interpret DSC as a different quantity than RES.

**Fix:** Add a footnote: "DSC here denotes the same quantity as RES (resolution) in the Brier decomposition; we adopt DSC to avoid overloading 'resolution' in the NWP context, where it typically refers to horizontal grid spacing."

### 4. Severity matrix Scenario C H_Pi mismatch
**Location:** `figures/severity_matrix.png` vs `07-worked-examples.tex:76-83`

In the severity matrix figure, Scenario C is placed in the "High confidence" column (H_Pi = 0.2), but the actual Scenario C has H_Pi = 0.15. This creates a discrepancy between the matrix's discrete binning and the scenario's exact value.

**Fix:** Either adjust the matrix column labels to ranges (e.g., "0.1-0.2") or note that scenarios are placed in their nearest bin.

### 5. IG decomposition figure uses hardcoded data
**Location:** `scripts/fig_ig_decomposition.py`

The five scenarios (Sharp Correct through Climatology) use hardcoded DSC and REL values rather than being computed from actual possibilistic forecast conversions. The figure is illustrative, not empirical.

**Fix:** Note in the caption that values are schematic illustrations, or compute them from the synthetic reforecast for consistency.

### 6. H notation risks confusion with Shannon entropy
**Location:** `03-possibility-primer.tex:120-121`

The paper acknowledges the naming collision ("The notation H nods to Shannon's entropy, though the possibilistic ignorance measure is not information-theoretic") but retains H_Pi anyway. Since the paper also uses Shannon entropy (via IG decomposition), having H denote a non-entropic quantity in the same manuscript invites misreading.

**Fix:** Consider a brief parenthetical in the notation table reinforcing this distinction, e.g., "H_Pi --- Possibilistic ignorance (not Shannon entropy): 1 - m."

### 7. Empty acknowledgments section
**Location:** `09-backmatter.tex:2`

Placeholder with no content.

**Fix:** Fill before submission or remove the heading until ready.

### 8. Missing `.bib` file
**Location:** Repository root

No bibliography file is present. Seven citation keys contain "-MISSING" suffixes (Dubois2006, Murphy1993, Jolliffe2012, Shafer1976, Smets1990, Walley1991, Neal2014) and will produce compilation errors.

**Fix:** Author has indicated these are forthcoming. Ensure all MISSING keys are resolved before submission.

---

## 5 Strongest Strengths

1. **The three-component framework is elegantly motivated.** The possibility / ignorance / conditional-necessity decomposition is clearly distinguished from both standard probability and Dempster-Shafer theory. The running "coin flip vs pundit" opening example in the Introduction immediately grounds the abstract distinction in operational intuition, and the framework maintains this clarity throughout.

2. **Worked examples are exceptionally well chosen.** Scenarios A (sharp-correct), B (hedged-correct), and C (sharp-wrong) isolate exactly the diagnostic behaviours the scorecard is designed to reveal. The contrast between B (delta = +0.561, honest hedging) and C (delta = -0.196, confident failure) is the paper's most compelling demonstration and will resonate with operational forecasters.

3. **Navigational tables are a major readability asset.** The notation table (Table 1), the raw/normalised protocol table (Table 2), and the three-to-five mapping table (Table 3) collectively prevent the reader from getting lost in a technically dense paper. These are unusually well designed for a theory-heavy manuscript.

4. **The ignorance-preserving probability bridge is a genuine innovation.** Reserving H_Pi as an explicit (n+1)-th outcome rather than redistributing it is a simple but powerful idea. The "worked contrast" box showing the 0.74-bit verification cost of naive normalisation (Section 4.3) makes the case concretely and convincingly.

5. **Diagnostic diagrams encode five dimensions effectively.** The performance diagram (specificity x depth-of-truth, coloured by ignorance, contoured by delta, sized by N_c\*) and the commitment-discrimination diagram successfully compress the full scorecard into two readable figures. The design is a natural and effective extension of the Roebber (2009) paradigm to possibility space.

---

## "If Submitted Today" Verdict

### **Minor Revision**

**Justification:** The framework is original, the mathematical development is sound (every equation was verified numerically against the code implementations and worked examples with no errors found), and the paper addresses a genuine gap in the verification literature. The writing is generally clear and well-structured for its target audience.

The issues found are:
- **Editorial:** A duplicate paragraph, inconsistent reforecast duration descriptions, and a missing script file. These are straightforward fixes.
- **One structural disclosure:** The N_c\*-alpha\* dependence should be stated explicitly; it does not invalidate the metric but changes how a reader interprets it.
- **One overclaim:** The no-single-metric-improvable assertion needs softening.
- **Notation housekeeping:** Standardise *m* terminology, remove dead nu_c notation, align figure annotations with text equations.

None of these require rethinking the framework or re-running analyses. A careful revision addressing these points would produce a publishable manuscript. The three-lane verification design and the ignorance-preserving bridge are contributions that will be useful to the atmospheric science community and beyond.

---

## Top 3 Highest-Leverage Rewrites

### 1. Resolve the 2-year / 3-year reforecast inconsistency
**Files:** `05-native-verification.tex:236,262`; `07-worked-examples.tex:91`; `scripts/fig_categorical_scores.py:87`

Pick a single duration (recommend 2 years), update all captions and body text, and ensure all scripts use the same `n_years` parameter. This fixes the most visible reproducibility concern in under 10 minutes.

### 2. Delete the duplicate paragraph in the Discussion
**File:** `08-discussion.tex:28-32`

Remove the second "Although SPC convective outlook categories..." paragraph. This is the most jarring editing artifact and the simplest fix in the manuscript.

### 3. Disclose the N_c\*-alpha\* structural dependence
**File:** `05-native-verification.tex`, after Eq. `\ref{eq:nc_star}` (line ~192)

Add one sentence: "By construction, N_c\* = 0 whenever c_obs is not the unique mode of pi', since max(pi'[w != c_obs]) = 1 in that case. N_c\* thus refines the subset of forecasts where alpha\* = 1, distinguishing dominant peaks from contested ones."

This pre-empts the most likely substantive reviewer objection and strengthens the paper's intellectual honesty.

---

## Micro-Tasks (descending impact)

Quick fixes that individually are small but collectively sharpen the manuscript.

1. **Rounding inconsistency in Scenario B p(ENH).** Table `tab:bridge_ils` gives p(c_obs) = 0.2086 (4 dp), but body text (`07-worked-examples.tex:180`) says "down to 0.209" (3 dp). Pick one precision and use it in both places.

2. **Abstract says "dimensions," body says "components."** Abstract (`00-abstract.tex:17`): "three complementary uncertainty dimensions." Everywhere else: "three components." Standardise on "components."

3. **Significance statement overlaps abstract heavily.** Both list the same three contributions (scorecard, conversion, categorical lane) in nearly the same order. The significance statement should pitch *why it matters* to a broader audience, not re-summarise the abstract. Consider rewriting the significance statement to emphasise the operational payoff (distinguishing "honestly uncertain" from "confidently wrong") rather than listing deliverables.

4. **alpha-cut discretisation mentioned but never defined** (`08-discussion.tex:32,130`). The term appears twice as a future-directions pointer for continuous variables. For a self-contained paper, add a parenthetical: "alpha-cut discretisation (partitioning the domain at each possibility threshold alpha)."

5. **"Distance-sensitive score should supplement the scorecard"** (`05-native-verification.tex:224-225`) is a dangling promise — no concrete score is proposed or cited. Either name a candidate (e.g., a weighted delta using ordinal distance) or soften to "could supplement."

6. **Significance test for scorecard_table.png is unspecified.** The figure distinguishes significant from non-significant changes (filled vs open triangles), but no test, significance level, or sample-size criterion is given. Add a parenthetical: "(significance assessed by [...] at the 5% level)" even for the synthetic illustration, so a reader implementing this for real data has a template.

7. **Computational complexity is trivially cheap — say so.** The scorecard is O(nK) per forecast (a few comparisons and one mean). For a framework targeting operational use, explicitly noting the negligible computational cost removes a potential objection.

8. **Seed=42 noted in code but not in manuscript.** `generate_reforecast()` uses `seed=42` for reproducibility. Mention this in the synthetic reforecast description (Section 5.3) so a reader can reproduce exact figures without reading code.

9. **Confusion matrix panel (b) colour scale.** The caption says "log scale for visibility" but the scale indicators are small. Consider adding "Colorbar: log-scale count" to the caption for accessibility.

10. **Section 4.1 title is "Deriving Probabilities from Possibilities" — consider whether "Deriving" overstates.** The conversion is a heuristic transformation, not a derivation from axioms. "Converting" (already used in 4.1 subsection title) is more precise for the section header.

---

## Gotchas to Watch For

Things that are currently correct but fragile — likely to break during revision if you're not careful.

1. **The epsilon-floor breaks sum-to-one.** The ε = 0.01 floor for zero-probability outcomes (`07-worked-examples.tex:185`) is applied post-conversion, but there's no renormalisation step. After flooring, the probability vector no longer sums to 1. The sensitivity analysis (ε = 0.001, 0.0001) will show the same issue. Either renormalise after flooring, or note that the log-score only uses p(c_obs) so the sum doesn't matter for single-event IG — but a reader computing mean S-bar will need the full vector to sum correctly.

2. **Division by zero when all pi = 0.** The framework assumes Axiom 1 (something must be possible, i.e., max(pi) > 0). If all pi(omega) = 0, then H_Pi = 1 and Sigma(pi) = 0, causing division by zero in both the conversion and the scorecard (pi' = pi / max(pi)). The code doesn't guard against this. If you add defensive code, add a corresponding note in the text.

3. **The N_c equation (eq:cond_nec) is written in raw form but classified as normalised in Table tab:raw_norm.** Both are correct: the equation divides by max(pi) internally, producing the same result as operating on pi'. But a reader who tries to implement N_c using pi' directly will write `N_c(A) = 1 - max(pi'[w not in A])`, which is the eq:nc_star form, not eq:cond_nec. The two equations look different but are equivalent. Consider adding a note: "Equivalently, N_c(A) = 1 - max_{omega not in A} pi'(omega), as shown in Eq. (eq:nc_star)."

4. **The synthetic reforecast always produces unimodal distributions** (Gaussian falloff around a peak, `fig_performance_diagram.py:124`). Real possibilistic forecasts could be bimodal (e.g., MRGL and MDT both plausible, SLGT/ENH low). The scorecard handles multimodality fine, but the diagnostic diagrams may look different with real data. Worth a sentence in limitations.

5. **If you change n_years to fix issue #2 (must-fix), regenerate ALL figures that call generate_reforecast().** These are: `fig_performance_diagram.py`, `fig_categorical_scores.py`, `fig_reliability_curves.py`. With a different n_years, all hex bins, confusion matrices, and bootstrap CIs will shift slightly. Check that narrative descriptions (e.g., "skill degrades fastest between SLGT and ENH") still hold.

---

## On the Fence — Chose Not to Flag

Issues I considered including but ultimately judged not worth flagging as deficiencies. Included here so you can make the call.

1. **No real forecast data anywhere.** The entire empirical validation is synthetic. This is defensible for a framework paper, but a reviewer at JAS may want at least one real-data case study (even a toy one with 30 days of SPC outlooks hand-coded as possibility distributions). I didn't flag it because the paper explicitly positions itself as a framework contribution, and the synthetic data is well-designed. But if you have access to even a small real dataset, a brief appendix case study would substantially strengthen the paper.

2. **The "three lanes" metaphor implies choosing one.** "Lane" suggests parallel paths where you pick one. The paper means "all three should be computed together," which is closer to "three lenses" or "three facets." I didn't flag this because the body text clarifies the intent, but "lane" may mislead on first read.

3. **The severity-confidence matrix section (8.1) feels speculative.** It connects to UK Met Office NSWWS without actual NSWWS data and proposes a mapping that hasn't been validated. This is interesting future-work material but sits awkwardly in the Discussion of a framework paper. If reviewers push back on paper length, this is a candidate for trimming.

4. **The IG decomposition section (4.2) is review material.** It's well-executed but occupies ~40 lines reviewing Roulston (2002) and Lawson (2024). For a JAS audience this is probably necessary context; for an information-theory audience it would be redundant. I kept it off the issues list because the self-contained pitch justifies it.

5. **No formal theorem or proposition anywhere.** The scorecard properties (ranges, boundary behaviour, gaming resistance) are discussed informally. For JAS this is appropriate. For a statistics or fuzzy-systems journal it might not be. If you anticipate cross-disciplinary readership, consider boxing at least the five-number scorecard definitions as a formal Definition environment.

6. **The pignistic terminology may overstate the connection to Smets (1990).** The conversion is inspired by the pignistic transform but differs in a key way (reserving ignorance mass rather than redistributing it). The section title "Deriving Probabilities from Possibilities" and the "pignistic" framing could lead a Dempster-Shafer expert to expect the actual pignistic transform. The text does explain the difference, but the section header and opening paragraph lean into the connection before clarifying the departure.

---

## Verified Calculations (no errors found)

For your confidence: every numerical claim in the worked examples was independently recomputed. All passed.

| Calculation | Location | Verified value |
|---|---|---|
| H_Pi Example 1 | `03:170` | 1 - 0.75 = 0.25 |
| N_c(MDT) Example 1 | `03:171` | 1 - 0.20/0.75 = 0.733 |
| N_c(MRGL) = N_c(SLGT) = 0 Example 2 | `03:191` | 1 - 0.50/0.50 = 0.00 |
| Bridge p vector | `04:61-62` | (0.022, 0.089, 0.178, 0.267, 0.044, 0.0, 0.400), sums to 1.0 |
| Bridge surprise | `04:66-67` | -log2(0.267) = 1.91; -log2(0.06) = 4.06; IG = 2.15 |
| Naive norm contrast | `04:198-200` | 0.6/1.35 = 0.444; -log2(0.444) = 1.17; gap = 0.74 bits |
| Scenario A scorecard | `07:216-221` | alpha\*=1.00, eta=0.222, delta=+0.778, H_Pi=0.10, N_c\*=0.833 |
| Scenario B scorecard | `07:216-221` | alpha\*=1.00, eta=0.439, delta=+0.561, H_Pi=0.45, N_c\*=0.273 |
| Scenario C scorecard | `07:216-221` | alpha\*=0.00, eta=0.196, delta=-0.196, H_Pi=0.15, N_c\*=0.00 |
| Scenario A IG | `07:167` | p(MDT)=0.675, S=0.567, S_clim=4.966, IG=+4.399 |
| Scenario B IG | `07:167` | p(ENH)=0.2086, S=2.261, S_clim=4.059, IG=+1.798 |
| Scenario C IG | `07:167` | p(MDT)=0.01\*, S=6.644, S_clim=4.966, IG=-1.678 |
| alpha\* = 0.267 example | `05:154-155` | pi'(ENH) for Example 1 = 0.20/0.75 = 0.267 |
| "Had c_obs = ENH in Scenario A" | `07:289-291` | alpha\*=0.167, N_c\*=0 |
| Code `compute_scorecard()` | `fig_three_scenario.py` | Matches all manuscript values exactly |
| Code `tripartite_bridge()` | `fig_pignistic_bridge.py` | p_cats.sum() + p_ign = 1.0; matches text |
