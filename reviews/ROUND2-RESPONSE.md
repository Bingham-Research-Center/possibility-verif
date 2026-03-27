# Round 2 Revision Response

**Manuscript:** "Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts"
**Responding to:** CLAUDEOPUS-1M-REVIEW-META (10 major, 11 minor issues)

---

## Major Issues

### M1. Necessity–possibility ordering qualified for normality

**Action:** Qualified `N(A) ≤ Pi(A)` in §2.1 (03-possibility-primer.tex) to hold "for normal distributions." Added note that under subnormality this ordering can be violated, and that §2.3 introduces conditional necessity N_c which restores well-behaved ordering. Also added max-additivity as formal Axiom 3 (see m1 below).

### M2. "Negative when m < 0.5" parenthetical replaced

**Action:** In §4.1 (05-native-verification.tex), replaced the misleading parenthetical with: "(classical N(A) can exceed Pi(A) for subnormal distributions, breaking the bracketing interpretation)." This accurately describes the failure mode without implying N_c itself goes negative.

### M3. Bridge–pignistic relationship reframed

**Action:** In §3.1 (04-pignistic-bridge.tex), changed "equivalent to" → "structurally analogous to" and "generalizes" → "a distinct transformation inspired by the same forced-betting intuition." The bridge is not a strict generalisation of the pignistic transform; it is a related but distinct procedure that extends the intuition to subnormal distributions.

### M4. Exceedance bounds §4.3 removed entirely

**Action:** Deleted §4.3 (exceedance bounds subsection, equations, and figure) from 05-native-verification.tex. Removed L_t from Table 2. Updated all cross-references in §0 (abstract), §1 (significance), §1 (introduction), §5 (tripartite), §6 (worked examples), and §7 (discussion).

**Rationale:** U = Pi(A_T) is the possibility measure restated; L = m · N_c(A_T) is circular under subnormality; the bounds have not been proven to hold as proper credal-set bounds for subnormal distributions. Added one sentence in §7.6 noting formal credal-set bounds as a direction for future work.

**Figure count:** 13 → 12 (upper_lower_bounds.png removed from LaTeX).

### M5. "Inspired by" Klir

**Action:** In §4.2 (05-native-verification.tex), changed "Following Klir (1995), nonspecificity measures..." → "Inspired by the nonspecificity concept of Klir (1995), we measure..."

### M6. Deterministic lane replaced with categorical lane

**Action:** Replaced "deterministic lane (RMSE, bias)" with "categorical lane (POD, FAR, CSI per threshold; HSS)" throughout:

- **Table 4** (06-tripartite-value.tex): Lane 1 now reads "Categorical (POD, FAR, CSI per threshold; HSS)" with the question "Did the mode-based point forecast identify the correct severity category?"
- **Lanes figure** (fig_verification_lanes.py): Relabelled Lane 1 as "Categorical" with mode extraction and POD/FAR/CSI/HSS metrics.
- **Scorecard figure** (fig_scorecard_table.py): Replaced RMSE/Bias rows with POD/FAR/CSI/HSS rows; removed exceedance-skill row.
- **Worked examples** (07-worked-examples.tex): Added §6.x "Categorical-Lane Walkthrough" showing mode-based threshold verification for all three scenarios.
- **Abstract, introduction, discussion:** All "deterministic" → "categorical" in lane context.

**Design rationale:** The mode (argmax π) is the natural point forecast from a possibility distribution—no bridge needed. Threshold-based POD/FAR/CSI is standard SPC verification. The three lanes now offer genuinely distinct perspectives: categorical (point forecast quality), probabilistic (converted-probability quality), and native possibilistic (distribution shape quality).

### M7. Switched to computed climatological baseline

**Action:** Added SPC_CLIM = (0.60, 0.18, 0.12, 0.06, 0.032, 0.008) to scripts/style.py. Recomputed all IG values:

| Scenario | obs | p_clim(obs) | Clim surprise | Forecast surprise | IG |
|----------|-----|-------------|--------------|-------------------|-----|
| A | MDT | 0.032 | 4.966 | 0.567 | **+4.399** |
| B | ENH | 0.060 | 4.059 | 2.261 | **+1.798** |
| C | MDT | 0.032 | 4.966 | 6.644* | **−1.678** |

Old values (uniform 1/K baseline): +2.018, +0.327, −4.059.

Updated: Table 6 (07-worked-examples.tex), §3.1 worked example (04-pignistic-bridge.tex, p_clim(ENH) = 0.06 → 4.059 bits), §6.4 narrative, fig_ig_decomposition.py (UNC = H(clim) ≈ 1.71 bits).

### M8. Epsilon set explicitly

**Action:** Set ε = 0.01 in §6.4 narrative (07-worked-examples.tex) with rationale: quantisation floor for a system built on O(10) ensemble members and human post-processing. Sensitivity analysis: ε = 0.001 → 9.97 bits surprise; ε = 0.0001 → 13.29 bits. Qualitative conclusion (Scenario C strongly negative) is invariant.

### M9. Reframed as Day-1 forecast comparison

**Action:** Rewrote §6.1 scenario setup (07-worked-examples.tex). The possibilistic forecast is now framed as an early/unofficial Day-1 outlook, verified against the final (pre-initiation) Day-1 SPC categorical outlook. Rationale: like-for-like comparison on the same categorical universe, IG naturally measures uncertainty reduction, no need to map storm reports to contours.

### M10. Missing citation keys

**Status:** Not addressed in this revision (author addressing separately). The following keys remain as -MISSING: Dubois2006, Smets1990, Shafer1976, Murphy1993, Jolliffe2012, Wilks2011, Walley1991, Neal2014.

---

## Minor Issues

### m1. Max-additivity axiom added

**Action:** Added Axiom 3 to §2.1 (03-possibility-primer.tex): "For any events A, B ⊆ Ω with A ∩ B = ∅, Pi(A ∪ B) = max(Pi(A), Pi(B))." This distinguishes possibility from probability and completes the axiomatic foundation.

### m2. N_c notation fixed

**Action:** In §2.2 Example 1 (03-possibility-primer.tex), corrected `1 − 0.267/1.0 = 0.73` → `1 − 0.267 = 0.733`. The "/1.0" was a misleading artefact (0.267 is already the normalised value); 0.733 is the correct 3-decimal-place value.

### m3. §3.1/§3.3 redundancy consolidated

**Action:** §3.3 already back-references §3.1 via "from Section 3.1." No new repetition of the π vector.

### m4. "Constructed" → "proposed"

**Action:** In §5 (06-tripartite-value.tex), changed "Three hypothesis tests are constructed" → "Three hypothesis test protocols are proposed."

### m5. LLM/Ffion section replaced

**Action:** Deleted §7.4 (LLM-mediated communication subsection + ffion_advisory figure) from 08-discussion.tex. Added one paragraph in §7.6 future directions: "The three-component representation lends itself to downstream communication; a companion project (Lawson, in prep.) explores LLM-mediated translation..."

**Figure count:** 12 → 11 (ffion_advisory.png removed from LaTeX).

### m6. Severity matrix integrated with scorecard

**Action:** Added 3 sentences after Figure 10 caption (08-discussion.tex) connecting a specific severity-matrix cell (MDT severity / high confidence) to the five-number scorecard: implied π = Scenario A, scorecard values when MDT verifies vs. when it does not, and aggregation across matrix cells.

### m7. Permutation-invariance moved earlier

**Action:** Moved from §7.6 (08-discussion.tex) to §4.2 (05-native-verification.tex), immediately after the scorecard aggregate paragraph. Expanded: SPC categories are semi-continuous and ranked in severity but with notional spacing; the scorecard treats them as unordered (conservative). For ordinal domains, a distance-sensitive score should supplement the scorecard.

### m8. Per-case vs aggregate IG transition

**Action:** Added transitional sentence before Eq. 4 in §3.2 (04-pignistic-bridge.tex): "Averaging Eq. (3) over a verification sample yields the mean logarithmic score, which decomposes diagnostically:..."

### m9. Rounding consistency in Table 6

**Action:** Recomputed all values from first principles with consistent rounding: 4 decimal places for probabilities, 3 decimal places for bits. Done alongside M7.

### m10. Software section trimmed

**Action:** Reduced §7.5 (08-discussion.tex) to one sentence: "All verification metrics, the bridge conversion, and the visualization tools described in this paper are implemented in Python and publicly available at [URL]."

### m11. Backmatter placeholders

**Status:** Not addressed in this revision (author addressing separately).

---

## Summary of Changes

| Category | Items | Files modified |
|----------|-------|---------------|
| Math/notation | M1, M2, M3, M5, m1, m2, m4, m8 | 03, 04, 05, 06 |
| Structural | M4, M6, m5, m6, m7, m10 | 00, 01, 02, 05, 06, 07, 08 |
| Recomputation | M7, M8, m9 | 04, 07, style.py, fig_ig_decomposition.py |
| Framing/tone | M9, m3 | 00, 01, 02, 07, 08 |
| Figures | M4, M6, M7 | fig_verification_lanes.py, fig_scorecard_table.py, fig_ig_decomposition.py |

**Final figure count:** 11 (was 13; removed upper_lower_bounds.png and ffion_advisory.png).

**Not in scope:** Missing citation keys (M10), backmatter placeholders (m11), real-data validation.
