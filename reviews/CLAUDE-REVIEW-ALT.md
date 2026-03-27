# Peer Review: "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts"

**Manuscript ID:** Submitted to *Journal of the Atmospheric Sciences*
**Author:** John R. Lawson (Utah State University)
**Reviewer:** Claude (automated review, 2026-03-27)

---

## Summary

This paper presents a self-contained verification framework for subnormal possibility distributions---distributions whose maximum falls below unity, encoding a forecasting system's acknowledged knowledge gaps. Three complementary tools are developed: (1) a five-number scorecard evaluating the raw possibility shape via depth-of-truth, nonspecificity, resolution gap, ignorance, and conditional necessity; (2) a possibility-to-probability bridge that preserves subnormality as an explicit ignorance outcome for information-gain scoring; and (3) exceedance bounds derived from possibility-necessity duality. All concepts are illustrated with stylized Storm Prediction Center convective outlook scenarios. The paper addresses a genuine gap in the verification literature---no prior framework evaluates possibilistic forecasts on their own terms---and the five-number scorecard is a novel contribution. However, several foundational claims require qualification, key content remains undeveloped, and the lack of real-data evaluation limits the paper's empirical contribution.

## Recommendation

**Major revision.** The mathematical framework is promising and the scorecard is a genuinely useful contribution, but the issues below (particularly M1, M2, M3, and M7) must be addressed before the paper can be accepted at JAS.

---

## Major Issues

### M1. Bracketing property stated without subnormality qualification

**Location:** `sections/03-possibility-primer.tex:70-76`, `sections/02-introduction.tex:74-76`

The paper states:

> "For any event A, N(A) <= Pi(A) always holds. The interval [N(A), Pi(A)] brackets the range of probabilities P(A) consistent with the available information: any probability distribution compatible with pi must satisfy N(A) <= P(A) <= Pi(A)."

This is **only true for normal distributions** (max pi = 1). For subnormal distributions, the inequality N(A) <= Pi(A) can be violated. The condition N(A) <= Pi(A) requires:

    1 <= max_{w in A} pi(w) + max_{w not in A} pi(w)

which holds when max(pi) = 1 (the global maximum is either in A or in its complement), but fails when max(pi) = m < 1. Concrete counterexample from the paper's own Example 1 (pi = (0.05, 0, 0.10, 0.20, 0.75, 0.15)):

- A = {NONE}: Pi(A) = 0.05, N(A) = 1 - 0.75 = 0.25
- N(A) = 0.25 > Pi(A) = 0.05, violating the stated inequality
- The "bracket" [0.25, 0.05] is empty---no probability can satisfy it

Moreover, the credal-set interpretation ("any probability distribution compatible with pi") is vacuous for subnormal distributions: Pi(Omega) = m < 1 implies no probability distribution (which must satisfy P(Omega) = 1) is dominated by Pi, so the credal set is empty.

**Fix:** Either (a) restrict the bracketing claim to normal distributions and explain that conditional necessity Nc (which operates on the normalized shape) recovers a valid bracket, or (b) explicitly define "compatible" for subnormal distributions (e.g., via the bridge probability) and prove the bracket for that specific probability class.

### M2. eta called "nonspecificity" but differs from Klir's definition

**Location:** `sections/05-native-verification.tex:145-149`

The paper defines:

    eta = (1/K) * sum_{c=1}^{K} pi'(c)

and calls it "nonspecificity" with a citation to Klir (1995). Klir's nonspecificity is the *generalized Hartley functional*:

    NS(pi) = integral_0^1 log2 |A_alpha| d_alpha

where A_alpha = {w : pi(w) >= alpha} are the alpha-cuts. This is a logarithmic measure of the cardinality of nested confidence sets---fundamentally different from a simple mean. The paper's eta is the mean of the normalized distribution, which measures diffuseness/spread but is not Klir's nonspecificity.

**Why it matters:** Readers familiar with possibility theory will expect Klir's definition when they see "nonspecificity." Using the same name for a different quantity creates confusion and undermines trust in the framework's foundations.

**Fix:** Either rename eta (e.g., "mean plausibility" or "diffuseness") or justify the simplification explicitly, noting that eta is a first-order approximation to nonspecificity and explain under what conditions they rank distributions identically.

### M3. Exceedance bounds [L, U] are not credal-set bounds under subnormality

**Location:** `sections/05-native-verification.tex:267-315`

The paper defines L = m * Nc(A_T) and U = Pi(A_T) and claims the interval "answers probability-of-exceedance questions." But:

1. U = max_{w in A_T} pi(w) is a *possibility* value, not a probability upper bound. While possibility dominates probability for normal distributions (Pi(A) >= P(A)), this guarantee breaks down under subnormality (see M1).

2. L = m * Nc(A_T) is a product of commitment and conditional necessity---a meaningful diagnostic, but its interpretation as a lower bound on probability requires justification that is not provided.

3. The interval [L, U] does bracket the specific bridge-converted probability (verified numerically for all three scenarios), but this is a property of the bridge construction, not a general credal-set guarantee.

The paper's caption for Figure 8 labels the x-axis "Probability of event A_T," which implies these are probability bounds. If they are possibility-space diagnostics, the axis label and surrounding text should say so.

**Fix:** Either (a) prove that L <= P_bridge(A_T) <= U for the bridge probability and present the bounds as bridge-specific, or (b) reframe the bounds as possibility-space diagnostics that inform (but do not directly bound) probability-of-exceedance estimates.

### M4. Deterministic lane mentioned but never developed

**Location:** `sections/00-abstract.tex:23-24`, `sections/06-tripartite-value.tex:126-152` (Table 4), `sections/06-tripartite-value.tex:187-220` (Figure 9)

The abstract, Table 4, and the scorecard figure all feature a "deterministic lane" with RMSE and bias. However:

- No "defuzzification" procedure is defined to extract a point forecast from a possibility distribution over *categorical* outcomes (RMSE and bias are undefined for unordered categories).
- No equations, examples, or discussion develop this lane.
- The scorecard figure (Figure 9) includes deterministic-lane rows that appear to show real values, but no computation is described.

**Fix:** Either (a) develop the deterministic lane properly (define defuzzification for ordinal categories, compute RMSE/bias for the worked examples), or (b) remove it from the abstract, tables, and figures and acknowledge it as future work.

### M5. No real-data evaluation

All examples are stylized synthetic scenarios with hand-chosen pi values. The three scenarios (sharp-correct, hedged-correct, sharp-wrong) effectively illustrate the scorecard's behavior, but they do not constitute an empirical evaluation. A JAS methods paper introducing a verification framework should demonstrate it on real or semi-realistic data---e.g., a synthetic reforecast calibrated to actual SPC category frequencies, or a case study applying the bridge and scorecard to retrospective convective outlooks.

**Fix:** Add at least one semi-realistic case study, such as:
- A synthetic reforecast with category frequencies matching observed SPC climatology, demonstrating the three hypothesis tests (Section 5.1) with real sample-size considerations.
- Alternatively, state clearly in the introduction that this paper develops the theoretical framework and that empirical evaluation will follow in a companion paper, and shorten the worked-examples section accordingly.

### M6. IG formula notation is opaque

**Location:** `sections/04-pignistic-bridge.tex:101-108`

The information-gain formula is written as:

    IG = D_KL(o || f1) - D_KL(o || f2)

where o is "the observation." For single forecast-observation pairs with a one-hot observation vector (which is the only setting used in this paper), this is simply:

    IG = -log2 f1(c_obs) + log2 f2(c_obs) = log2(f2(c_obs) / f1(c_obs))

The KL divergence notation obscures this simplicity and introduces potential confusion:
- D_KL(o || f) with a one-hot o equals the surprisal -log f(c_obs), not a divergence in the usual sense.
- The argument ordering (o || f vs. f || o) is a common source of errors.

**Fix:** Present the single-case formula first (-log2 p(c_obs)), then note it equals D_KL(o || f) for one-hot o, then explain how aggregation over cases yields the sample-mean IG decomposition.

### M7. Eight missing bibliography keys across 16 occurrences

**Location:** Throughout `sections/02-introduction.tex`, `sections/03-possibility-primer.tex`, `sections/04-pignistic-bridge.tex`, `sections/08-discussion.tex`

The following citation keys have `-MISSING` suffixes and will produce undefined-reference warnings:

| Key | Occurrences | Files |
|-----|-------------|-------|
| `Dubois2006-MISSING` | 3 | 02-introduction, 03-possibility-primer (x2) |
| `Shafer1976-MISSING` | 3 | 02-introduction, 03-possibility-primer, 08-discussion |
| `Smets1990-MISSING` | 3 | 04-pignistic-bridge (x2), 08-discussion |
| `Murphy1993-MISSING` | 1 | 02-introduction |
| `Jolliffe2012-MISSING` | 1 | 02-introduction |
| `Wilks2011-MISSING` | 1 | 02-introduction |
| `Walley1991-MISSING` | 1 | 02-introduction |
| `Neal2014-MISSING` | 2 | 08-discussion (x2) |

These are foundational references (Dubois & Prade for possibility theory, Shafer for DS theory, Smets for the pignistic transformation, Murphy/Jolliffe/Wilks for forecast verification). The paper cannot be submitted without them.

---

## Minor Issues

### m1. Redundancy between Section 3.1 and Section 3.3

Section 3.1 already explains why simple normalization erases the ignorance signal (lines 44-51). Section 3.3 ("Why Naive Normalisation Erases Information") repeats the same argument at greater length with a worked contrast table. Consider merging the worked contrast into Section 3.1 and eliminating Section 3.3, or shortening Section 3.3 to just the table.

### m2. Abstract and Significance Statement are largely redundant

The Significance Statement (Section 0) is a condensed version of the abstract, sharing the same three-component structure. JAS requires both, but the overlap should be reduced by making the Significance Statement more audience-facing (emphasizing operational implications) and less methodological.

### m3. LLM communication subsection is tangential

Section 7.4 ("Structured Uncertainty and LLM-Mediated Communication") describes a companion system (Lawson, in prep.) at length, including implementation details (Claude CLI, three-minute inference time, JSON serialization). This is tangential to a verification methods paper. Consider condensing to a single paragraph noting that the three-component representation feeds downstream communication pipelines, with the full system described elsewhere.

### m4. Severity-confidence matrix figure (Figure 13) is disconnected

The severity-confidence matrix (Section 7.3, Figure 13) is an interesting visualization but is not connected to the verification framework. It shows how operational decisions map to the possibility-ignorance space, but no scorecard values or verification diagnostics are computed for it. Consider either computing scorecard values for representative matrix cells or moving the figure to supplementary material.

### m5. Section 5 lacks an opening motivation paragraph adequate for a standalone section

The opening paragraph (lines 12-19) is brief but functional. However, it does not preview the three hypothesis tests or the three-lane framework, making the section structure opaque on first read. A sentence listing the two subsections would help.

### m6. Communication example in Section 2.3 repeats Section 2.2 interpretation

The "Communication example" block in Section 2.3 (lines 225-236) restates the same interpretation of Example 1 already given in Section 2.2 (lines 142-146). Remove the duplicate or replace it with a communication example for Example 2, which would better illustrate the interpretive framework.

### m7. Epsilon-floor value in Table 6 is unspecified

Table 6 marks Scenario C's p(c_obs) as "epsilon-floored" but never states what epsilon is. From the surprise value (6.644 bits), epsilon = 2^(-6.644) approximately equals 0.01, but this should be stated explicitly and justified (e.g., as the minimum representable probability for the log score).

### m8. Uniform 1/K baseline caveat is noted but not developed

Section 6.4 (line 243-248) notes that a uniform baseline is used "for algebraic transparency" and that empirical frequencies would be more appropriate. This is an important caveat that deserves more attention: the IG values in Table 6 would change substantially with a realistic baseline where P(NONE) >> 1/6.

### m9. Permutation-invariance limitation acknowledged late

The statement that scorecard metrics are permutation-invariant (Section 7.6, line 274) is correct and important, but it appears only in the limitations section. Since SPC categories are ordinal, this should be noted earlier (e.g., when the scorecard is first defined in Section 4.2) so readers understand from the outset that near-miss penalties are not captured.

---

## Specific Corrections

### S1. Misleading intermediate step in Nc calculation

**Location:** `sections/03-possibility-primer.tex:143`

> "Nc(MDT) = 1 - 0.267/1.0 = 0.73"

The "/1.0" suggests a meaningful division, but since pi' is already normalized, the denominator is 1.0 by construction. Rewrite as:

> "Nc(MDT) = 1 - max_{w != MDT} pi'(w) = 1 - 0.267 = 0.73"

or, to show the normalization step:

> "Nc(MDT) = 1 - (0.20 / 0.75) = 1 - 0.267 = 0.73"

### S2. Bridge equation annotation in Figure 4 script

**Location:** `scripts/fig_pignistic_bridge.py:118`

The bridge formula annotation reads "p_i = pi_i * Pi_max / Sigma pi" but the paper's text (Section 3.1, line 37) gives "p_i = pi_i * (1 - H_Pi) / sum pi_j." These are algebraically identical (since 1 - H_Pi = Pi_max = m), but using different notation in the figure and text may confuse readers. Unify.

### S3. Pignistic transform generalization claim needs precision

**Location:** `sections/04-pignistic-bridge.tex:46-53`

The paper says the bridge "generalizes" Smets' pignistic transformation. Strictly, the pignistic transformation operates on *mass functions* in the transferable belief model, while the bridge operates on *possibility distributions*. These coincide when the possibility distribution induces a consonant mass function, but the paper should note this restriction. Suggested wording: "...generalizes the pignistic transformation to subnormal distributions, under the implicit assumption that the possibility distribution induces a consonant belief structure."

### S4. Figure 8 x-axis label should distinguish possibility from probability

**Location:** `sections/05-native-verification.tex:300-311` (Figure 8 caption), `scripts/fig_upper_lower_bounds.py:99-100`

The x-axis is labeled "Probability of event A_T" but the plotted bounds [L, U] are possibility-derived quantities, not probabilities. Unless the bounds are proven to be probability bounds (see M3), the label should read "Possibilistic bounds for event A_T" or "Plausibility interval for A_T."

### S5. Performance diagram analogy to Roebber (2009) is structural, not methodological

**Location:** `sections/05-native-verification.tex:199-215`

The text says the diagram is "inspired by Roebber (2009)" and draws parallels (specificity <-> success ratio, alpha* <-> POD). This analogy is structural---both use product contours to combine orthogonal skill axes---but methodologically different, since Roebber's diagram evaluates deterministic binary forecasts. A sentence clarifying this distinction would prevent misinterpretation.

### S6. Scorecard table column headers could be clearer

**Location:** `sections/07-worked-examples.tex:167-178` (Table 5)

The column header shows "m (commitment)" but m = max(pi) is defined as "subnormality" in Table 1 and the notation table. Using "commitment" only here (and in Section 4.2) creates an inconsistency. Either add "commitment" as an alias in Table 1 or use "subnormality" consistently.

### S7. Gauge section describes but does not show scenarios B and C

**Location:** `sections/07-worked-examples.tex:132-150`

Section 6.2 vividly describes what the gauge would look like for scenarios B and C but only provides Figure 11 for scenario A. Either (a) generate gauge figures for B and C, (b) add panels to Figure 11, or (c) note explicitly that Figure 10 (three-scenario) already provides the corresponding visual comparison (which it does, minus the gauge-specific formatting).

---

## Verified Correct

The following mathematical claims were independently verified against the Python implementation and hand calculations:

1. **Table 5 scorecard values**: All five metrics for all three scenarios match hand computation from the definitions (Eqs. 6-10). Code in `fig_three_scenario.py:compute_scorecard` is consistent.

2. **Bridge formula and worked example (Section 3.1)**: For pi = (0.05, 0.2, 0.4, 0.6, 0.1, 0.0), H_Pi = 0.4, sum = 1.35, p(ENH) = 0.267, surprise = 1.91 bits, IG = 2.41 bits---all correct.

3. **Exceedance bounds code**: `fig_upper_lower_bounds.py:bounds_from_possibility` correctly implements Eqs. 11-12.

4. **IG decomposition sign convention**: LS = UNC - DSC + REL with IG = DSC - REL is internally consistent throughout.

5. **Bridge probability sums**: The bridge code (`fig_pignistic_bridge.py:tripartite_bridge`) includes an assertion that p_cats + p_ign sums to 1.0 (line 51), and this holds for all scenarios.

6. **Table 6 bridge values**: All three scenarios' bridge probabilities, surprisals, and IG values match independent computation (with epsilon-flooring for scenario C).

---

## Strengths

1. **Genuine novelty.** No prior work provides native verification metrics for subnormal possibility distributions. The five-number scorecard fills a real gap.

2. **Principled bridge construction.** Preserving ignorance as an explicit outcome is well-motivated and avoids the information-erasure problem clearly diagnosed in Section 3.3.

3. **Effective worked examples.** The three scenarios (sharp-correct, hedged-correct, sharp-wrong) are well-chosen to isolate diagnostic situations and vividly demonstrate how the scorecard separates "honestly uncertain" from "confidently wrong."

4. **Clear, accessible writing.** The primer (Section 2) is self-contained and assumes no prior knowledge of possibility theory. The plain-language glosses for scorecard metrics (Section 4.2) are particularly useful for the target audience.

5. **Code availability.** All figures and computations are reproducible from the accompanying Python scripts, with canonical constants centralized in `scripts/style.py`.

6. **Visual innovation.** The gauge visualization, performance diagram, and commitment diagram are novel diagnostic tools that effectively encode multi-dimensional scorecard information.

7. **Honest scope management.** The paper correctly identifies and defers hard problems (possibilistic climatology, IRLS proper scoring) rather than presenting incomplete solutions.

---

## Section-by-Section Accessibility Check

For each section, the core ideas are restated in simplified language, and any errors or ambiguities are flagged.

### Abstract

**Simplified:** "We built tools to check whether a 'possibility forecast' (one that says how plausible different outcomes are, rather than how probable) did a good job. Our tools include a five-number summary that grades the forecast on its own terms, a method to convert possibility values into probabilities so we can use existing scoring methods, and upper/lower bounds on how likely an event was. We demonstrate everything using severe-weather categories."

**Flags:**
- The phrase "three verification lanes---deterministic, probabilistic, and native possibilistic" promises a deterministic lane that is never developed (see M4).
- "probability-of-exceedance questions" implies the bounds are probability bounds, which requires qualification (see M3).

### Section 1 (Significance Statement)

**Simplified:** "Possibility forecasts carry richer information than probability forecasts---they can say 'I don't know' explicitly. No one has built tools to evaluate these forecasts. This paper builds those tools."

**Flags:** No errors. Clear and appropriate for a significance statement.

### Section 2 (Introduction)

**Simplified:** "A coin-flip expert and a sports pundit both say 50/50, but the expert is confident and the pundit is guessing. Probability can't tell them apart; possibility theory can. We review the theory, note that no one has built verification tools for it, and outline our paper."

**Flags:**
- The claim that [N(A), Pi(A)] brackets all consistent probabilities (lines 74-76) is incorrect for subnormal distributions (see M1).
- Eight missing citations appear in this section alone (see M7).
- The literature review is adequate but would benefit from the missing references (Murphy, Jolliffe, Wilks for verification; Dubois, Shafer, Smets, Walley for uncertainty frameworks).

### Section 3 (Possibility Theory Primer)

**Simplified:** "Here's everything you need to know about possibility theory. You have a set of outcomes, and each one gets a number between 0 and 1 saying how plausible it is. If the biggest number is less than 1, the forecast is 'subnormal'---it admits ignorance. We define three components: how plausible each outcome is (possibility), how much the system doesn't know (ignorance), and how dominant the top outcome is among what the system covers (conditional necessity)."

**Flags:**
- The bracketing property in Section 2.1 (lines 70-76) is stated without the normality restriction. See M1 for the counterexample using the paper's own Example 1.
- The "Why Not Just Probabilities?" subsection (Section 2.4) is well-argued but references the bracketing property again (lines 243-244) without qualification.
- The Dempster-Shafer connection (lines 213-223) is appropriately hedged ("structural resemblance").

### Section 4 (Possibility-to-Probability Bridge)

**Simplified:** "To use standard scoring rules, we need probabilities. Our 'bridge' converts possibility values to probabilities in three steps: (1) set aside a chunk of probability equal to the system's ignorance, (2) distribute the rest proportionally, (3) add the ignorance chunk as a separate 'I don't know' outcome. This way, uncertain systems get penalized---their probability is diluted by the ignorance mass."

**Flags:**
- The claim that the bridge "generalizes" the pignistic transformation (line 53) needs the consonant-mass-function caveat (see S3).
- Section 3.3 ("Why Naive Normalisation Erases Information") largely repeats Section 3.1 (see m1).
- The IG formula (Eq. 4) uses opaque D_KL notation for what is simply -log p(c_obs) in the single-case setting (see M6).

### Section 5 (Native Possibilistic Verification)

**Simplified:** "Instead of converting to probabilities, we can grade the possibility distribution directly using five numbers: (1) depth-of-truth (how much possibility was assigned to what actually happened), (2) nonspecificity (how spread-out the distribution is), (3) resolution gap (did the truth get more support than average?), (4) ignorance (how uncertain was the system?), (5) conditional necessity (among what the system covered, was the truth dominant?). We also define upper and lower bounds for any threshold event."

**Flags:**
- eta is called "nonspecificity" but is not Klir's nonspecificity (see M2). The definition as "mean of the normalised distribution" is correct; the name is wrong.
- The exceedance bounds [L, U] are presented as answering "probability-of-exceedance questions" but are not proven to be probability bounds (see M3).
- The performance diagram analogy to Roebber (2009) is structural, not methodological (see S5).
- The commitment diagram (Section 4.2, Figure 7) is a nice addition that promotes ignorance from a colour channel to a primary axis.

### Section 6 (Three-Component Value)

**Simplified:** "Do all three components (possibility, ignorance, conditional necessity) actually add information, or are some redundant? We propose three tests: (1) does the system point at truth better than climatology? (2) when the system says it's uncertain, is it actually worse? (3) when the system says it's sure, is it actually right? If all three tests pass, the full scorecard is justified."

**Flags:**
- The three hypothesis tests are well-conceived but entirely theoretical---no test statistics, significance levels, or sample-size calculations are provided beyond rough guidelines (lines 109-117).
- The deterministic lane in Table 4 (lines 126-152) lists RMSE and bias but these are never defined for categorical variables (see M4).
- The scorecard figure (Figure 9) includes deterministic-lane rows with apparent values but no computation is described.

### Section 7 (Worked Examples)

**Simplified:** "We walk through three scenarios step by step: (A) a forecast that confidently predicted MDT and was right, (B) a forecast that hedged across several categories but got the right answer, and (C) a forecast that confidently predicted NONE but MDT actually happened. The scorecard correctly rewards A, partially rewards B, and harshly penalizes C."

**Flags:**
- All scorecard values in Table 5 are verified correct (see "Verified Correct" section above).
- All bridge values in Table 6 are verified correct, except the epsilon value is unspecified (see m7).
- The uniform baseline caveat (lines 243-248) is important: with realistic base rates (P(NONE) >> 1/6), IG values would change substantially (see m8).
- The gauge section (Section 6.2) describes scenarios B and C in prose but only shows a figure for A (see S7).

### Section 8 (Discussion and Future Work)

**Simplified:** "Our framework connects to Dempster-Shafer theory (possibility ~ plausibility, conditional necessity ~ belief), works for any categorical variable (not just severe weather), and can feed downstream communication systems including LLM-generated advisories. Limitations: we haven't tested on real data, we don't have a possibilistic skill score, and the scorecard ignores the ordering of categories."

**Flags:**
- The DS connection (Section 7.1) is well-drawn and appropriately limited.
- The LLM communication subsection (Section 7.4) is tangential and overly detailed for a verification paper (see m3).
- The severity-confidence matrix (Section 7.3, Figure 13) is interesting but disconnected from the verification framework (see m4).
- The limitations section (Section 7.6) is honest and comprehensive.
- Missing citations: Shafer1976, Smets1990, Neal2014 all appear in this section (see M7).

### Section 9 (Backmatter)

**Flags:**
- Acknowledgments placeholder is noted.
- Data and Code Availability section should include a version tag or DOI.
- The GenAI statement is present and appropriate.

---

*End of review.*
