# Manuscript Review — "Possible, Yes; Ignorant, Perhaps: A Scorecard for Possibilistic Forecasts"

**Reviewer:** GitHub Copilot (Claude Opus 4.6)
**Date:** 2026-03-29
**Scope:** Human readability, conceptual clarity, methodological rigor, notation consistency, figure–text alignment.

---

## Executive Summary (≤150 words)

This paper introduces a verification framework for subnormal possibility distributions comprising a five-number scorecard, a possibility-to-probability conversion preserving the ignorance signal, and three complementary verification lanes (categorical, probabilistic, native possibilistic). The mathematical development is sound — all numerical claims I verified (Examples 1–2, pignistic bridge, Scenarios A–C scorecard and IG values, ε-sensitivity) are correct. The running SPC example is well-chosen and the three-scenario comparison (sharp-correct, hedged-correct, sharp-wrong) is pedagogically excellent. Figures are publication-quality with consistent visual language. The core issues are: (1) a 2-year vs 3-year data inconsistency between text and captions, (2) the resolution gap δ is called both "resolution gap" and "discrimination" in different locations, (3) the Figure 1 annotation misuses the $N_c$ symbol, and (4) a missing script file undermines the reproducibility claim. All issues are readily fixable.

---

## Must-Fix Issues

| # | Severity | Location | Issue | Why It Matters | Suggested Fix |
|---|----------|----------|-------|----------------|---------------|
| M1 | **High** | `05-native-verification.tex:237` vs `:262` | Body text says "single synthetic reforecast ($n = 730$ days, two years)" but Figure 4 caption says "three-year synthetic reforecast." `fig_categorical_scores.py` calls `generate_reforecast(n_years=3)` while `fig_reliability_curves.py` uses the default `n_years=2`. | Readers cannot tell which figures use which dataset; undermines reproducibility and cross-figure comparisons. | Pick one sample size (suggest 3 years / $n = 1095$ to match the categorical figure), update `generate_reforecast()` default, and reconcile all captions and body text. |
| M2 | **High** | `fig_possibility_anatomy.py:76–77`; `03-possibility-primer.tex:144` | Figure 1 annotates the peak category as "$N_c$ = MDT." $N_c$ is a numerical function (Eq. 3) returning values in $[0,1]$, not a category label. The annotation reads as "a number equals a category name." | Confuses the distinction between the conditional necessity *measure* and the peak category *label* — the very distinction the paper is teaching. | Change annotation to either (a) "Peak: MDT" with $N_c(\text{MDT}) = 0.733$, or (b) remove $N_c$ from the figure and annotate only in the caption. |
| M3 | **High** | `05-native-verification.tex:265` vs `07-worked-examples.tex:220`; commitment diagram y-axis | δ is formally defined as "Resolution gap" (Table 1, Table 3, Eq. 10) but called "discrimination" in Table 6 column header and on the commitment-diagram y-axis label ("Discrimination $\delta = \alpha^* - \eta$"). | Two names for the same quantity creates ambiguity, especially since "discrimination" (DSC) already denotes the IG decomposition component. A reviewer or reader may think these are different quantities. | Use "Resolution gap" consistently everywhere. Reserve "discrimination" exclusively for the IG decomposition term DSC. Relabel the commitment-diagram y-axis to "Resolution gap $\delta = \alpha^* - \eta$ (→ better)". |
| M4 | **Medium** | `03-possibility-primer.tex:224` | The three-component list item for conditional necessity introduces an unexplained symbol: "$\Nc(A)$, $\nu_c$." The symbol $\nu_c$ never appears again in the manuscript — not in any equation, table, or figure. | Dead notation distracts and suggests an incomplete edit. A careful reader will search for $\nu_c$ and find nothing. | Delete "$\nu_c$" from line 224. |
| M5 | **Medium** | `08-discussion.tex:22–31` | Two consecutive paragraphs state nearly the same thing: "the framework applies to any finite universe of discourse Ω over which a subnormal possibility distribution is defined" (line 25–26) and "the framework is domain-agnostic: any system producing subnormal possibility distributions over a finite Ω can be evaluated without modification" (line 29–30). | Reads as a copy-paste artefact; undermines polish. | Delete the second paragraph (lines 28–31) or merge the extension-to-continuous sentence into the first paragraph. |
| M6 | **Medium** | `04-pignistic-bridge.tex:200` | The worked-contrast table labels the quantity $-\log_2(p(c_{\text{obs}}))$ as "Self-entropy." Self-entropy conventionally means $H(\mathbf{p}) = -\sum p_i \log p_i$. What is computed here is the *surprise* (log-score), which was defined in Eq. 5. | Terminological inconsistency within the same section; a reader who knows information theory will flag this. | Rename the row to "Surprise (bits)" to match Eq. 5 and the surrounding text. |
| M7 | **Medium** | `scripts/fig_performance_diagram.py:246` | `from fig_perf_iterate import get_data, v3b, v4b` — but `fig_perf_iterate.py` does not exist in `scripts/`. The hexbin and commitment diagrams cannot be regenerated. | Section 9 ("Data and Code Availability") claims all tools are "publicly available." A missing dependency violates this. | Add `fig_perf_iterate.py` to the repository, or refactor so that `fig_performance_diagram.py` is self-contained. |
| M8 | **Low** | `03-possibility-primer.tex:92` (Table 1) | The symbol $m$ is glossed as "Subnormality: $\max_\omega \pi(\omega)$." Subnormality is a *condition* ($m < 1$), not a value. Elsewhere the paper calls $m$ "commitment" (e.g., Table 6, commitment diagram). | Readers will wonder whether "subnormality" means the degree of subnormality ($H_\Pi = 1 - m$) or the maximum itself. | Relabel to "Commitment (peak): $\max_\omega \pi(\omega)$" and add a parenthetical "(subnormal when $m < 1$)." |

---

## Should-Fix Issues (prioritised)

### S1 — η ≠ Klir's nonspecificity (conceptual precision)
**`05-native-verification.tex:158–162`**
The text says η is "inspired by the nonspecificity concept of Klir (1995)." Klir's nonspecificity for possibility distributions is $\text{NS}(\pi) = \int_0^1 \log_2 |A_\alpha|\, d\alpha$ (a Hartley-like functional over α-cuts), not the arithmetic mean of the normalised distribution. Citing Klir creates an implicit claim of formal equivalence that doesn't hold. **Fix:** Change "inspired by the nonspecificity concept" to "analogous in spirit to the nonspecificity concept" and add a sentence noting the distinction, or rename η to "mean plausibility" to avoid false cognates.

### S2 — IG decomposition figure shares scenario names with A/B/C
**`fig_ig_decomposition.py`; `04-pignistic-bridge.tex:151–163`**
The IG figure labels its bars "Sharp Correct," "Hedged Correct," "Sharp Wrong," "Hedged Wrong" — the same labels used for Scenarios A, B, C in Section 7. But the IG values differ (e.g., +1.75 bits vs Scenario A's +4.399 bits) because the IG figure uses independent synthetic values. A reader encountering the IG figure before Section 7 will expect the numbers to match. **Fix:** Either relabel the IG bars as "Scenario I," "Scenario II," etc., or add a footnote: "These are illustrative; the specific worked examples in Section 7 use different distributions."

### S3 — ε-floor not formalised as a general protocol
**`07-worked-examples.tex:185–196`**
The ε-floor ($\varepsilon = 0.01$) is introduced ad hoc for Scenario C. It is unclear whether this floor applies to all forecasts or only to zero-probability events. If applied globally it would slightly change all IG values (Table 5 only marks Scenario C). **Fix:** Add a brief protocol statement in Section 4.1: "In all subsequent computations, converted probabilities are floored at $\varepsilon = 0.01$ to prevent infinite log-scores."

### S4 — Abstract / Significance Statement overlap
Both passages mention the five-number scorecard, the conversion, and three verification lanes in nearly the same language. The Significance Statement should be more accessible and practitioner-oriented, emphasising the "so what." **Fix:** Rewrite the Significance Statement to focus on the operational consequence ("forecasters and model developers can now separately diagnose…") and remove technical details already in the abstract.

### S5 — Conversion doesn't use max-additivity
The possibility-to-probability conversion (Section 4.1) distributes mass proportionally to $\pi_i$, treating possibility values as unnormalised probability weights. This ignores the max-additive structure that distinguishes possibility from probability. While the paper acknowledges the conversion is "lossy" (Section 5 line 8–9), a single sentence noting that the proportional allocation does not exploit max-additivity — and why that's acceptable — would preempt a reviewer objection from the imprecise-probability community.

### S6 — No discussion of incentive compatibility
The scorecard resists "trivial gaming" (line 226–229) but the paper offers no formal argument that honest reporting maximises expected score. Even a brief paragraph noting that propriety is an open question for possibilistic scores, and that the multi-metric design makes unilateral gaming unprofitable, would strengthen the discussion.

### S7 — Introduction length and structure
Section 2 runs ~130 lines mixing motivation, literature review, running-example setup, and roadmap. Consider splitting the SPC example setup into the opening of Section 3 (where it is first used), shortening the introduction, and using a subsection heading for the literature review.

### S8 — MISSING bibliography keys
Seven references have `-MISSING` suffixes (`Dubois2006-MISSING`, `Murphy1993-MISSING`, `Jolliffe2012-MISSING`, `Shafer1976-MISSING`, `Smets1990-MISSING`, `Walley1991-MISSING`, `Neal2014-MISSING`). Per the author's note, these are pending — flagged here for completeness only.

### S9 — Scorecard figure legend symbol mismatch
**`fig_scorecard_table.py:175`**
The legend shows a filled square (█) for "Ignorance* (context-dep.)" but the actual markers in the figure are triangles rendered in amber. The `marker="s"` in the legend handle doesn't match `marker="^"` or `marker="v"` used in the plot. **Fix:** Use triangle markers in the legend for ignorance, matching the figure.

### S10 — Categorical figure uses 3-year data but shares the reforecast seed with 2-year figures
`fig_categorical_scores.py` calls `generate_reforecast(n_years=3)` while `fig_reliability_curves.py` calls `generate_reforecast()` (default 2 years). The first 730 days are identical (same seed), so results are consistent for those days, but aggregate statistics differ. This is a secondary consequence of M1 but worth noting: once M1 is fixed, ensure all shared-reforecast figures use the same call.

---

## 5 Strongest Strengths

1. **Pedagogically brilliant three-scenario design.** Scenarios A (sharp-correct), B (hedged-correct), and C (sharp-wrong) are precisely the minimal set that demonstrates why possibility theory adds value over probability: they separate confidence from correctness and reveal failure modes invisible to any single verification lane. The running SPC categories ground the abstraction in operational practice.

2. **Self-contained mathematical development.** A JAS reader with no prior exposure to possibility theory can follow from axioms (Section 3.1) through subnormality (3.2), conditional necessity (3.3), the conversion (4.1), the scorecard (5.2), and the three-lane design (6.2) without consulting external references. Definitions build on each other without circular dependencies. This is uncommon in papers bridging mathematical frameworks into applied domains.

3. **Publication-quality figures with consistent visual language.** The purple/green colour scheme carries consistent meaning (purple = possibilistic, green = verified/correct). The pignistic bridge figure (Fig. 2) with connecting arrows is an exceptional piece of visual explanation. The hexbin performance diagram (Fig. 4) and commitment diagram (Fig. 5) encode five metrics simultaneously while remaining readable. The ECMWF-style scorecard table (Fig. 8) will be immediately familiar to the NWP audience.

4. **The three-lane architecture is well-motivated and empirically demonstrated.** Rather than asserting complementarity, the paper shows that each lane catches failures invisible to the others (Section 6.2 lines 108–115): a "broken clock" forecast passes categorical but fails probabilistic/possibilistic; a lucky conversion passes probabilistic but fails possibilistic; a miscalibrated conversion passes possibilistic but fails probabilistic. This "each lane has a blind spot" argument is concise and convincing.

5. **Honest treatment of limitations and future work.** The paper forthrightly acknowledges the closed-world assumption, the absence of a possibilistic skill score, and the lack of sample-size guidance — without trying to hand-wave these away. The future-directions list is specific and actionable (credal-set bounds, multivariate extension, conformal comparison), signalling a mature research programme rather than a one-off contribution.

---

## "If Submitted Today" Verdict

### **Minor Revision**

**Justification:**
The core contribution — a five-number scorecard for subnormal possibility distributions, supported by a principled poss-to-prob conversion and three complementary verification lanes — is novel, mathematically sound, and well-presented. All numerical claims I independently verified are correct. The figures are excellent. The paper is genuinely self-contained, which is a major service to the atmospheric science audience.

The issues requiring revision are all tractable:
- The 2-year/3-year inconsistency (M1) is a bookkeeping error, not a conceptual flaw.
- The naming inconsistencies (M3 δ, M4 ν_c, M8 $m$) are editorial fixes.
- The missing script (M7) is a repository housekeeping item.
- The Figure 1 annotation (M2) is a graphics tweak.

No issue undermines the theoretical framework. No additional experiments or derivations are needed. The paper would benefit from tightening the terminology and reconciling the synthetic-data specifications, both of which are achievable in a standard revision cycle.

---

## Top 3 Highest-Leverage Rewrites

### 1. Reconcile the synthetic reforecast specification (fixes M1, S10)
A single paragraph in Section 5.3 should specify: sample size (pick one: recommend $n = 1095$ days, three years), the random seed, and which figures share this dataset. Then update `generate_reforecast()` defaults and all captions. This one change eliminates the most confusing inconsistency in the paper — a reader comparing Fig. 4 ($n = 730$?) to Fig. 7 ($n = 1095$?) currently cannot tell whether differences are real or artefactual.

### 2. Harmonise δ terminology throughout (fixes M3)
Global find-and-replace "discrimination" → "resolution gap" in every context referring to δ, including the commitment-diagram axis label and Table 6. Keep "discrimination" exclusively for the IG component DSC. This prevents the single most likely point of reviewer confusion, since δ and DSC are different quantities that would share a name.

### 3. Add a "Notation and Terminology" forward-reference in the Significance Statement (addresses S4, M4, M8)
Replace the current Significance Statement with a practitioner-oriented version (~80 words) that avoids duplicating the abstract. End it with: "Table 1 provides a reference card for all notation." This trims redundancy, signals that the paper is self-contained, and draws early attention to the notation table — reducing the cognitive load of the heavy-notation sections that follow.
