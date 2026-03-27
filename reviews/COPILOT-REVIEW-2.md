# Peer Review: COPILOT-REVIEW-2

**Manuscript:** "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts"
**Target:** *Journal of the Atmospheric Sciences* (AMS)
**Reviewer model:** Claude Opus 4.6 (GitHub Copilot CLI)
**Date:** 2026-03-27

---

## 1 Overall Assessment

### Recommendation: Major Revision

This paper proposes a self-contained verification framework for subnormal possibility distributions — a genuine gap in the literature. The five-number scorecard, the possibility-to-probability bridge with explicit ignorance preservation, and the three-lane diagnostic architecture are original contributions. The running SPC example is well-chosen and the three-scenario walkthrough is pedagogically effective.

However, the paper contains a **critical mathematical error** (the N(A) ≤ Π(A) claim for subnormal distributions), an **incorrect attribution** of the nonspecificity measure to Klir (1995), and **15 missing citation keys** that leave the literature review unverifiable. The hypothesis tests in §5 are described but never executed, creating a gap between the section's claims and its content. Several notational inconsistencies (m vs Π_max, dual use of "discrimination") will confuse careful readers.

### Strengths

- **Novelty**: No prior verification methodology exists for subnormal possibility distributions. The framework is genuinely new.
- **Pedagogical clarity**: The bridge construction (§3.1) is well-motivated and clearly explained. The worked examples (§6) effectively demonstrate every component.
- **Mathematical correctness of computed values**: All scorecard values in Table 2 and bridge values in Table 3 verified correct (independently recomputed).
- **Honest scope**: The limitations section (§7.6) is thorough and transparent.
- **Complementary architecture**: The three-lane structure (deterministic, probabilistic, native possibilistic) is well-argued and practically useful.

### Principal Concerns

1. Mathematical error in the necessity–possibility ordering for subnormal distributions
2. Incorrect attribution of the nonspecificity formula
3. Missing citations rendering the literature review incomplete
4. §5 hypothesis tests are proposals, not demonstrations — mismatched framing
5. The max-additivity axiom is mentioned but never formally stated

---

## 2 Major Issues

### M1. N(A) ≤ Π(A) does NOT hold for subnormal distributions

**Location:** §2.1, lines following Eq. 2
**Severity:** Critical — invalidates a foundational claim

The paper states: *"For any event A, N(A) ≤ Π(A) always holds."* This is **false** for subnormal distributions.

**Counterexample:** Let π = (0.3, 0.2) over Ω = {ω₁, ω₂}. For A = {ω₁}:
- Π(A) = max_{ω∈A} π(ω) = 0.3
- N(A) = 1 − max_{ω∉A} π(ω) = 1 − 0.2 = 0.8
- **N(A) = 0.8 > Π(A) = 0.3** — violation.

The duality N(A) ≤ Π(A) and the bracketing property N(A) ≤ P(A) ≤ Π(A) require normality (max π = 1). The paper relaxes normality (§2.1, Axiom 2) but retains the claims that depend on it. This propagates to §2.4, which also asserts the bracketing property for general π.

- **Action:** Add a qualifier: "For normal distributions, N(A) ≤ Π(A) always holds. For subnormal distributions, the classical necessity N(A) may exceed Π(A); the conditional necessity Nc(A) (Eq. 4, computed on π′) restores the ordering." Alternatively, define a subnormal-compatible necessity as L(A) = m · Nc(A) (which the paper already uses in the exceedance bounds) and show that L(A) ≤ Π(A) always holds.
- **Verify:** The exceedance bounds (§4.3) correctly use L = m · Nc rather than raw N, so the downstream framework is not affected — but the foundational exposition in §2.1 must be corrected.

### M2. Nonspecificity η is NOT Klir's definition

**Location:** §4.2, Eq. 8, and the citation "Following Klir (1995)"
**Severity:** Major — incorrect attribution

The paper defines η = (1/K) Σ π′(c) and attributes it to Klir (1995). Klir's nonspecificity for a possibility distribution is the **Hartley-measure** integral over α-cuts:

NS(π) = ∫₀¹ log₂|{ω : π(ω) ≥ α}| dα

This measures the *nested set structure* of the distribution. The paper's η is the **arithmetic mean** of the normalised distribution — a legitimate spread measure, but a distinct quantity. The two diverge whenever the distribution is not uniformly stepped.

- **Action:** Either (a) adopt Klir's formula (and rename η accordingly), or (b) drop the Klir citation and call η "mean normalised possibility" or simply "spread." Option (b) is simpler and does not affect the rest of the framework.

### M3. Fifteen missing citation keys

**Location:** §§1–3, 7 (grep: `-MISSING`)
**Severity:** Major — literature review is unverifiable

| Key | Likely reference |
|-----|-----------------|
| `Dubois2006-MISSING` | Dubois & Prade (2006), *Intl J Approx Reasoning* or Handbook chapter |
| `Smets1990-MISSING` | Smets (1990), *Intl J Approx Reasoning* 4(4) |
| `Shafer1976-MISSING` | Shafer (1976), *A Mathematical Theory of Evidence* |
| `Murphy1993-MISSING` | Murphy (1993), *Wea. Forecasting* 8(2) |
| `Jolliffe2012-MISSING` | Jolliffe & Stephenson (2012), *Forecast Verification* (2nd ed.) |
| `Wilks2011-MISSING` | Wilks (2011), *Statistical Methods in the Atmospheric Sciences* (3rd ed.) |
| `Walley1991-MISSING` | Walley (1991), *Statistical Reasoning with Imprecise Probabilities* |
| `Neal2014-MISSING` | Neal et al. (2014), *Met. Apps* or NSWWS documentation |

- **Action:** Resolve all 15 instances before submission. The claims attributed to these sources are central to the paper's positioning.

### M4. ε-floor for zero-probability bridge outcomes is undefined

**Location:** §6.3, Table 3, asterisk on p(c_obs) = 0.000*
**Severity:** Major — the IG penalty for Scenario C depends entirely on this choice

The bridge assigns p(MDT) = 0.0 for Scenario C. The paper reports surprise = 6.644 bits, implying −log₂(ε) = 6.644, hence ε ≈ 0.01. But ε is never defined. Different choices dramatically change the result:

| ε | Surprise (bits) | IG (bits) |
|---|----------------|-----------|
| 0.01 | 6.64 | −4.06 |
| 0.001 | 9.97 | −7.38 |
| 1/K = 0.167 | 2.58 | 0.00 |

- **Action:** State the floor value explicitly and justify the choice. A natural option is ε = 1/(K·N) for N forecast–observation pairs (sample-dependent), or a fixed small constant with sensitivity analysis.

### M5. §5 hypothesis tests are proposals, not conducted tests

**Location:** §5.1, paragraph header "Three Hypothesis Tests"
**Severity:** Major — framing overstates the content

The section title and framing ("three hypothesis tests are constructed, each isolating one component and asking whether it adds information the other two do not provide") imply the tests are actually performed. In reality, the section describes *what one would test* — the protocol, the met-analogue, the expected curve shape — but uses only synthetic data for illustration. No statistical tests are reported.

- **Action:** Reframe as "Three Proposed Hypothesis Tests" or "Testing Protocol." Replace "are constructed" with "are proposed" and add a sentence noting that execution requires a real reforecast dataset.

### M6. Max-additivity axiom mentioned but never stated

**Location:** §1 ("violating the max-additivity axiom"), §3.2 ("which violate the additivity axiom")
**Severity:** Moderate — confusing for readers new to possibility theory

The distinguishing axiom of possibility measures is Π(A ∪ B) = max(Π(A), Π(B)) for disjoint A, B. This is mentioned in passing but never formally stated in §2, where it belongs alongside Axioms 1 and 2.

- **Action:** Add it as Axiom 3 or a Remark in §2.1, with a one-sentence contrast to probability's additivity P(A ∪ B) = P(A) + P(B).

### M7. Deterministic lane is undeveloped

**Location:** §5.2 Table 4, Fig. 9 caption ("the defuzzified point forecast"), Fig. 10 (RMSE/bias rows)
**Severity:** Moderate — the three-lane architecture claims three lanes but develops only two

The paper never defines how to defuzzify a possibility distribution to produce a point forecast. The deterministic lane appears in the table, figure, and scorecard but no method is given. A reviewer or reader attempting to replicate the scorecard cannot compute RMSE or bias rows.

- **Action:** Either (a) define a defuzzification procedure (e.g., the category with max π, or the centroid of the α-cut), or (b) remove the deterministic lane from the scorecard figure and relabel the architecture as "two-lane plus optional point forecast."

---

## 3 Minor Issues

### §0 Abstract

- *"Three verification lanes—deterministic, probabilistic, and native possibilistic"*: Given that the deterministic lane is undeveloped (M7), consider toning this to "two primary verification lanes plus a deterministic baseline."

### §1 Introduction

- The coin/pundit opening is effective but the pundit example could be tighter: "50:50 for a sports match played in extreme weather between teams that have never met" — the extreme weather detail is unnecessary for the point and may confuse readers who think this is about weather forecasting.
- "SPC issues crisp categorical outlooks drawn on a map; this paper proposes a hypothetical possibilistic alternative using these familiar categories" — excellent framing. Clearly distinguishes the paper from claiming SPC already uses possibility theory.
- Notation: the introduction uses \nec and \poss before they are formally defined (§2.1). Consider adding a forward reference or brief gloss.

### §2 Possibility Theory Primer

- **§2.1**: The text states "something must be possible" as Axiom 1 (non-vacuity). This is standard but trivial for any non-zero input. Consider adding the max-additivity property here (M6).
- **§2.2, Example 1**: "Nc(MDT) = 1 − 0.267/1.0 = 0.73" — the "/1.0" is confusing. The computation is Nc = 1 − max_{ω≠MDT} π′(ω) where π′(ENH) = 0.20/0.75 ≈ 0.267 and max(π′) = 1.0 by definition. Write instead: "Nc(MDT) = 1 − π′(ENH) = 1 − 0.20/0.75 ≈ 0.73."
- **§2.2, Example 1**: π(MRGL) = 0.00 while π(NONE) = 0.05 in a "classic severe-weather setup." It's slightly odd that marginal risk is deemed less possible than no risk at all when the setup features strong instability. Consider swapping (MRGL = 0.05, NONE = 0.00) or briefly justify.
- **§2.3**: "Though not statistically independent" — this is an important qualifier. Consider moving it earlier and elaborating: in what sense are they dependent? (All three derive from the same π; Nc is a function of the normalised shape, δ involves both α* and η, etc.)
- **§2.4**: Asserts the bracketing property [N(A), Π(A)] for general π — same issue as M1. Needs the normality qualifier.
- **§2.5, Table 1**: Lists m as "Subnormality" but §§4–6 call it "commitment." Add "commitment" as an alias in the table.
- **Notation collision**: m and Π_max are used for the same quantity (max π). Standardise on one symbol.

### §3 Possibility-to-Probability Bridge

- **§3.1**: The bridge formula is given as p_i = π_i · (1 − H_Π) / Σπ_j. In §6.3, the same formula appears as p_i = π_i · m / Σπ_j. These are identical (m = 1 − H_Π) but the notational inconsistency may trip readers. Pick one form.
- **§3.1 worked example**: Uses π = (0.05, 0.2, 0.4, 0.6, 0.1, 0.0), a third distinct distribution (after Examples 1 and 2 in §2). The proliferation of example distributions is manageable but could be reduced.
- **§3.2**: "the IG decomposition measures it in bits — additive, interpretable information units" — good. But the individual terms UNC, DSC, REL are never given formulas. Since the paper reports DSC and REL in the scorecard figure (Fig. 10), at least provide the definitions or the explicit formulas from Lawson (2024).
- **§3.2**: The Brier comparison paragraph is helpful for probabilistic readers but is tangential to a possibility paper. Consider trimming to 2–3 sentences.
- **§3.3**: Well-argued. The worked contrast table is effective. No issues.
- **§3, naming**: The paper notes the IG/IGN naming collision. There is an analogous collision with "discrimination": δ (resolution gap) is called "discrimination" in §5 and the commitment diagram, but DSC (information-gain discrimination) is a different quantity. Distinguish these explicitly.

### §4 Native Possibilistic Verification

- **§4.1**: "Getting the raw/normalised distinction wrong is the single most common error in possibilistic scoring" — strong and useful statement. The ensemble-rank-histogram analogy is apt.
- **§4.2, Eq. 8**: η ranges from 1/K to 1 — correct for the given formula. But note this assumes π′ has at least one entry = 1 (by normalisation) and at least one entry > 0. If π has only one nonzero entry, η = 1/K as expected.
- **§4.2**: The performance diagram (Fig. 7) and commitment diagram (Fig. 8) are both described in §4.2 without a subsection break. Consider a brief paragraph header for the commitment diagram.
- **§4.2**: "Both axes of Figure 7 operate on the normalised shape π′: two forecasts with identical shapes but different commitment levels (H_Π = 0.05 vs 0.50) land at the same position." This is an important caveat — well flagged.
- **§4.3**: Exceedance bounds are well-defined. The proof that 0 ≤ L ≤ U ≤ 1 always holds is left implicit. Consider adding a one-line argument (m ≥ max_{ω∉A} π(ω) because m is the global max).
- **§4.3, Fig. 6 caption**: "Scenario C collapses to a point at zero because the system assigned zero possibility to every category in A_T." Correct and vivid.

### §5 Three-Component Value

- Beyond M5 (tests are proposals, not executed), the sample-size guidelines ("at least 50 pairs," "at least 30 per stratum") appear without justification or citation. Either cite a reference for bootstrap power calculations or soften to "order-of-magnitude guidance."
- **§5.2**: The scorecard figure (Fig. 10) is effective. The narrative about v2.0/v3.0/v4.0 development trajectory is well-written and makes the diagnostic value concrete.

### §6 Worked Examples

- **§6.1**: The Norman, Oklahoma framing is good — gives geographic concreteness without overclaiming.
- **§6.2**: Gauge description for Scenarios B and C is narrative-only (no figures). This is defensible for space but consider adding the gauges as subfigures — the visual impact is strong.
- **§6.3**: Table 3 verified correct. The "arc from skill to catastrophe" phrasing is evocative.
- **§6.3**: "ε-floored values" — see M4. Also note that the choice of baseline (uniform 1/K) is acknowledged as a simplification, which is good.

### §7 Discussion

- **§7.1**: DS connections are well-drawn. The paragraph on extending to belief functions is appropriately cautious.
- **§7.2**: "Extension to continuous forecast variables is straightforward via α-cut discretisation" — true, but this could use one more sentence on how the resulting nested sets relate to the scorecard.
- **§7.3**: The ensemble-derived possibility pathway is the most accessible for the NWP audience and deserves more emphasis. Consider promoting it before the fuzzy-inference pathway.
- **§7.4**: LLM pipeline description is interesting but somewhat tangential to a verification methods paper. The mention of "Anthropic's Claude, operating as a CLI tool" with "approximately three minutes of inference time per outlook cycle" reads as implementation detail rather than scientific content. Consider trimming.
- **§7.5**: "The accompanying code is publicly available" — good. Add a version tag or DOI.
- **§7.6**: "The five scorecard metrics are permutation-invariant" — important limitation for ordinal SPC categories. The paper acknowledges it but doesn't sketch even the simplest fix (e.g., weighting δ by ordinal distance). One sentence would help.
- **§7.6**: "Defining a principled possibilistic climatology — the baseline needed for skill — remains an open problem." This is a significant limitation that should be more prominently flagged, as it means no skill score is possible with the current framework.

### §8 Backmatter

- Acknowledgments placeholder — must be filled before submission.
- GenAI statement is very brief. AMS now requires specific disclosure of *how* AI tools were used (drafting, coding, editing, etc.).
- Data availability should include a version tag or Zenodo DOI.

---

## 4 Batch-by-Batch Simplified Summaries

*For each 1–2 paragraph batch, a first-year undergraduate translation. Errors or falsehoods that prevent accurate simplification are flagged with* ⚠️.

---

### Abstract

**Plain version:** "When forecasting dangerous weather, sometimes you don't know how confident to be. This paper creates a report card for a special kind of forecast that can say 'I'm not sure' instead of pretending to be precise. The report card has five numbers. We also show how to convert these special forecasts into regular probability forecasts without hiding the uncertainty. We test everything using the severe weather categories the Storm Prediction Center uses."

---

### §1 Significance Statement

**Plain version:** "Regular probability forecasts must add up to 100% — they can't say 'I don't know.' These special forecasts (called possibilistic) can. But nobody has made a way to grade them. This paper makes that grading system."

---

### §1 Introduction, ¶1–2 (coin/pundit + hazard forecasting)

**Plain version:** "Imagine flipping a coin 100 times — you're pretty sure it's 50/50, and you have good evidence. Now imagine guessing a sports outcome with almost no information — you might also say 50/50, but for completely different reasons. Regular probability treats both the same. Possibility theory doesn't: it lets you say 'I gave 50/50 because I genuinely don't know' separately from 'I gave 50/50 because the evidence says so.' Weather forecasters face this same problem — sometimes their models just don't have enough information, and they should be able to say so."

---

### §1 Introduction, ¶3–4 (possibility generalises probability + literature)

**Plain version:** "Possibility theory gives you a range of possible probabilities instead of a single number. When you know a lot, the range is narrow; when you know little, it's wide. Fuzzy logic systems and expert-rule systems naturally produce this kind of output. Nobody has built a grading system for it — existing approaches either force the numbers to look like probabilities (hiding the 'I don't know' signal) or treat the possibility values as if they were probabilities (which they aren't)."

⚠️ **Error in source:** The paper asserts that the interval [N(A), Π(A)] brackets probability for any π (including subnormal). This is false. The bracket only works when the forecast is "fully committed" (normal). If the forecast says "I'm not very sure about anything" (subnormal, e.g., max = 0.3), you can get the absurd result that the lower bound exceeds the upper bound (N = 0.8 > Π = 0.3). See Major Issue M1.

---

### §2.1 Axioms and Definitions

**Plain version:** "Think of a list of weather outcomes (like 'no severe weather,' 'marginal risk,' etc.). A possibility distribution assigns each outcome a number from 0 to 1 — how compatible that outcome is with the evidence. Zero means 'ruled out,' one means 'fully plausible.' Two key rules: (1) Possibility = the biggest value in a group of outcomes. (2) Necessity = 1 minus the possibility of everything else. Necessity is like confidence: 'How sure am I that it's NOT something else?'"

⚠️ **Same error as above**: The claim N(A) ≤ Π(A) "always holds" is stated here and is false for subnormal distributions.

---

### §2.2 Subnormal Distributions and Ignorance

**Plain version:** "What if no outcome gets a full score of 1.0? That means the forecasting system is saying 'I'm not fully confident in ANY of my guesses.' The gap between the highest score and 1.0 is called 'ignorance' — it measures how much the system admits it doesn't know. This is useful! Regular probabilities can't express this; they must always add up to 100% even when the system is guessing."

**Example simplified:** "Example 1: Strong thunderstorm ingredients are all present. The system says MDT risk is most plausible (0.75 out of 1.0). The ignorance is 0.25 — the system is 75% committed. Among the outcomes it does cover, MDT dominates."

---

### §2.3 Three-Component Uncertainty

**Plain version:** "Every forecast is evaluated on three axes: (1) **Possibility** — how plausible is each outcome? (2) **Ignorance** — how much does the system admit it doesn't know? (3) **Conditional necessity** — given what the system DOES cover, how dominant is the top answer? Think of it like a restaurant review: possibility = 'what's on the menu,' ignorance = 'how confident is the chef,' necessity = 'is the signature dish clearly the best?'"

---

### §2.4 Why Not Just Probabilities?

**Plain version:** "Probabilities must add to 100%, so they can't say 'I don't know' — they have to spread their confidence across specific outcomes even when the evidence is thin. Possibility distributions give a range instead of a point. When evidence is scarce, the range is wide and honest. When evidence is strong, the range narrows and you're back to something probability-like."

⚠️ **Repeated bracketing claim**: The section re-asserts [N(A), Π(A)] for general π.

---

### §3.1 Possibility-to-Probability Bridge

**Plain version:** "To use standard grading tools (which need probabilities), we convert possibilities to probabilities in three steps: (1) Set aside the 'ignorance' portion as a separate 'I don't know' category. (2) Split the remaining confidence proportionally among the real outcomes. (3) Attach the 'I don't know' category to the end. Now probabilities sum to 100%, but the uncertainty is visible as a separate bucket — not hidden."

**Worked example simplified:** "Input: a forecast where the system is 40% unsure. The strongest outcome (ENH) gets possibility 0.6. After conversion, ENH gets probability 0.267 — much less than the 0.444 simple normalization would give — because 40% of the probability goes to the 'I don't know' bin."

---

### §3.2 Information-Gain Decomposition

**Plain version:** "Information gain (IG) measures how much surprise the forecast removed compared to just guessing climatology. It breaks into three parts: (1) Uncertainty — how hard was the problem? (2) Discrimination — could the system tell outcomes apart? (3) Reliability — were its stated confidences honest? You want high discrimination and low reliability error."

---

### §3.3 Why Naïve Normalisation Erases Information

**Plain version:** "If you just divide every possibility value by their sum (the simple way), a system that's 90% unsure produces the same probabilities as one that's 10% unsure — as long as the shape is the same. The 'I don't know' signal vanishes. The bridge avoids this by parking the uncertainty in a separate bin that earns zero credit at grading time. The more uncertain the system, the more mass gets parked, and the worse its score."

---

### §4.1 Normalisation Protocol

**Plain version:** "Some scores use the raw numbers; others use the 'rescaled-to-max-1' version. Getting this wrong is the most common mistake. Using raw values where you need rescaled ones gives nonsense (like negative certainty)."

---

### §4.2 Five-Number Scorecard

**Plain version:** "Five numbers grade each forecast: (1) **Depth-of-truth (α*)** — how much possibility did the truth get? (2) **Nonspecificity (η)** — how spread out was the forecast? (3) **Resolution gap (δ)** — did truth get more than average? (4) **Ignorance (H_Π)** — how unsure was the system? (5) **Conditional necessity of truth (Nc*)** — was truth dominant? Upper-right on the diagram = sharp and correct. Lower-right = sharp and wrong."

⚠️ **Attribution issue**: η is attributed to Klir (1995) but doesn't match Klir's definition. See M2.

---

### §4.3 Exceedance Bounds

**Plain version:** "For a group of outcomes (like 'ENH or worse'), the forecast gives a range: the upper bound is how plausible the worst-case group is; the lower bound combines commitment with how dominant that group is. Wide range = ambiguous. Narrow range = confident. When the system is fully committed, this collapses to the classical necessity–possibility interval."

---

### §5.1 Three Hypothesis Tests

**Plain version:** "Three checks tell you if all three components are useful: (1) Does the system point at truth better than climatology? (2) When it says it's uncertain, does it actually do worse? (3) When it says it's confident, is it actually right? If all three pass, the full scorecard is justified."

⚠️ **Framing issue**: These are described as tests that "are constructed," but they are actually proposed protocols — no data-driven tests are reported. See M5.

---

### §5.2 Three Verification Lanes

**Plain version:** "No single metric catches everything. The deterministic lane asks 'was the point forecast close?' The probabilistic lane asks 'was the probability forecast informative?' The native possibilistic lane asks 'was the possibility distribution well-shaped and honest?' Each catches failures invisible to the others. A scorecard table (like ECMWF uses) tracks changes across model versions."

⚠️ **Undeveloped lane**: The deterministic lane lacks a defuzzification definition. See M7.

---

### §6.1 Scenario Setup

**Plain version:** "Three made-up forecasts at Norman, Oklahoma: (A) Confident and correct — strong severe weather, system nails MDT risk. (B) Uncertain but correct — mixed signals, system hedges across several categories, ENH verifies. (C) Confident and wrong — looks quiet, system says no severe weather, but MDT actually happens."

---

### §6.2 Filling the Gauge

**Plain version:** "Each forecast is drawn as horizontal bars — longer bars = higher possibility. The gap between the tallest bar and the edge of the chart shows ignorance. Scenario A: one tall bar (MDT), small gap. Scenario B: several medium bars, large gap. Scenario C: one tall bar (NONE), but the actual answer (MDT) has no bar at all — a visual alarm."

---

### §6.3 Full Scorecard + Bridge Walkthrough

**Plain version:** "Running all three forecasts through the scorecard: A scores perfectly — high truth, low spread, low ignorance. B scores well on truth but is penalized for hedging. C fails catastrophically — zero truth, negative resolution, and low ignorance means no safety net. Converting to probabilities via the bridge: A gets +2.0 bits of skill (strong). B gets +0.3 bits (modest). C gets −4.1 bits (catastrophe). The scorecard correctly separates 'honestly uncertain' from 'confidently wrong.'"

---

### §7 Discussion (selected batches)

**§7.1 DS connections:** "The possibility–necessity framework looks like Dempster–Shafer theory's belief–plausibility intervals. The main difference: possibilistic ignorance measures 'the system didn't cover this,' while DS uncertainty measures 'the evidence sources disagree.'"

**§7.3 Generating possibilistic forecasts:** "Four ways to make these forecasts: (1) fuzzy rule systems, (2) ensemble fractions (don't normalise — let spread speak), (3) severity–confidence matrices (like the UK Met Office already uses), (4) conformal prediction (sets at multiple confidence levels = α-cuts of a possibility distribution)."

**§7.6 Limitations:** "The scorecard doesn't care about category order (missing MDT by one step is the same as missing by four). No possibilistic climatology exists yet, so there's no skill score. The 'I don't know' bin can never verify as correct (closed-world assumption). All acknowledged."

---

## 5 Structural and Presentation Notes

| Issue | Section | Note |
|-------|---------|------|
| Notation: m vs Π_max | §§2–6 | Two symbols for max(π). Standardise. |
| "Commitment" alias | §§4–6 | Used freely but absent from Table 1. |
| "Discrimination" collision | §§4–5 | δ and DSC both called "discrimination." |
| Bridge formula notation | §3.1 vs §6.3 | (1−H_Π) vs m — same quantity, different notation. |
| Example distribution proliferation | §§2–3 | Three distinct distributions before the canonical scenarios. Consider consolidating. |
| Fig. 8 subsection | §4.2 | The commitment diagram is described mid-§4.2 without its own heading. |
| GenAI disclosure | §8 | AMS requires specifics on how AI was used (drafting, coding, editing). |
| Acknowledgments | §8 | Placeholder — must be filled. |
| Data availability | §8 | Needs version tag or Zenodo DOI. |
| Ordinal penalty sketch | §7.6 | One sentence on distance-weighted δ would strengthen the limitations section. |

---

## 6 Verdict Summary

| Criterion | Rating |
|-----------|--------|
| Novelty | ★★★★☆ — Genuine gap filled |
| Mathematical rigour | ★★★☆☆ — Core computations correct, but M1 is critical |
| Accessibility | ★★★★☆ — Excellent examples and plain-language glosses |
| Self-consistency | ★★★☆☆ — Notation collisions, subnormal duality error |
| Strength of case | ★★★☆☆ — Tests proposed but not executed |
| Completeness | ★★★☆☆ — Missing citations, undeveloped deterministic lane |
| Presentation | ★★★★☆ — Well-structured, attractive figures |

**Bottom line:** A promising and original framework with a compelling narrative, but it requires correction of the necessity–possibility ordering claim, resolution of missing citations, and honest reframing of the hypothesis tests before it meets JAS standards.
