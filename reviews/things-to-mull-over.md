# Things to Mull Over — Final PDF Annotation Crib Sheet

Generated 2026-03-31 against repo state post-Opus-4.6 triage edits.
Use alongside a printed or tablet PDF. Items are grouped by section, then by concern type.

---

## Abstract (`00-abstract.tex`)

1. **Read the two-sentence split aloud.** The old single sentence ("comprising...evaluating...") was split into "comprising [5 metrics]. These five metrics span [3 components]." Does the full stop after $\Nc^*$ feel natural, or does it break the rhetorical momentum?

2. **"Ignorance" still appears twice** — once as the metric name ("possibilistic ignorance ($\ign$)") and once as the component category ("ignorance"). This is now deliberate: the second occurrence has no symbol, signalling it's a category, not a re-definition. Verify this reads as intended.

3. **"Explicit ignorance outcome"** (line 20) — does a reader unfamiliar with the conversion understand what this means at first encounter? It's explained in Section 3.1, but the abstract should stand alone.

4. **Three facets listed as "categorical, probabilistic, and native possibilistic"** — verify this order matches the rest of the paper (Section 5, the verification-lanes figure, the scorecard figure). In some places you use "possibilistic" alone, elsewhere "native possibilistic."

5. **Keywords** — "scoring rules" is listed but the paper argues the native scorecard is *not* a scoring rule (it's a diagnostic). Is this keyword misleading? Consider "verification" or "verification framework" instead.

---

## Significance Statement (`01-significance.tex`)

6. **Overlap with abstract.** Both mention: five-number scorecard, conversion, three verification facets. The Significance Statement is now more practitioner-oriented ("distinguish honestly uncertain forecasts from confidently wrong ones"). Read both back-to-back: is the distinction in tone sharp enough? Could a journal editor ask you to de-duplicate?

7. **"Honestly uncertain"** — this phrase does good rhetorical work, but a reviewer might ask: honestly relative to what? The forecaster's belief? The data? The paper's framework defines honesty as committing less than full plausibility ($m < 1$), but the Significance Statement doesn't say that.

8. **"No modification"** claim — "any system producing subnormal possibility distributions over a finite $\Omega$ can be evaluated without modification." This is true for the scorecard but the conversion requires $\varepsilon$-flooring and the choice of a climatological baseline, both of which are domain-specific. Overstated?

---

## Introduction (`02-introduction.tex`)

9. **Length: 136 lines.** A referee may flag this as front-heavy. The SPC category definitions (lines 25-36) are running-example setup that logically belongs in Section 2 (where the categories are first used formally). Consider moving them. The introduction should motivate *why*, not define *what*.

10. **"Coin toss" framing** (lines 6-12). The opening contrasts probability (coin) with possibility (pundit). Is the pundit analogy accessible to a JAS reader who thinks in PDFs and CDFs? Does it set up the paper's formal content, or distract?

11. **Two mentions of "proper scoring rules"** (lines 21, 87) without citation. The concept is standard but a reviewer might want Gneiting & Raftery (2007) or similar. You cite Roulston (2002) elsewhere for IG propriety — is that sufficient to cover both mentions?

12. **Literature review** (lines 75-106) — does it adequately acknowledge the imprecise-probability community (Augustin, Troffaes, de Cooman)? A reviewer from that world might feel the paper dismisses credal sets too quickly.

13. **Roadmap paragraph** — do the section numbers match? (e.g., "Section 3 introduces the possibility primer" — is it actually Section 3, or has it shifted?)

14. **"Max-additivity axiom that distinguishes possibility from probability"** (line 110) — this is stated as fact. A measure-theorist might note that max-additivity characterises possibility measures on finite spaces, not in general (infinite spaces need upper semicontinuity). Worth qualifying? Probably not for JAS, but flag if a referee raises it.

---

## Possibility Primer (`03-possibility-primer.tex`)

15. **Axiom numbering.** Axioms are in a list environment (not numbered equations). The text references "Axiom 1" (`05-native-verification.tex:282`) and "Axiom 3" (`04-pignistic-bridge.tex`, new max-additivity sentence). Verify the axiomlist order: (1) something-must-be-possible, (2) normalisation (optional), (3) max-additivity. If you ever reorder the list, these cross-references break silently.

16. **Table 1 (Notation reference card).** Check every row against current terminology:
    - $m$: should say "Commitment (peak possibility)" — verify it does (M8 was fixed)
    - $\delta$: should say "Support margin" — not "resolution gap" or "discrimination"
    - $\eta$: should say "Diffuseness" — not "nonspecificity" or "spread"
    - $N_c^*$: should say "Dominance margin" or "Cond. necessity of truth"
    - Does the table include $\varepsilon$? (It's now referenced in Section 3.2.)

17. **Example 1 distribution** $\pi = (0.05, 0.00, 0.10, 0.20, 0.75, 0.15)$ — this distribution is used in at least four places: primer text, Figure 1 (`fig_possibility_anatomy.py`), the bridge worked example, and Table 5 computation context. Verify they all use the same values. A single transposed digit would propagate errors.

18. **$N_c$ definition** (Eq. 4 / line 239). The equation defines $N_c(A)$ for an event $A$. The paper uses $N_c$ for individual categories (singletons). Strictly, the argument should be $\{c\}$ not $c$. Is this pedantic or pedagogically important?

19. **"Conditional necessity" naming.** This term is non-standard — Dubois & Prade use "necessity measure" $N(A)$ for the dual of $\Pi(A)$. Your $N_c$ is conditioned on $m$ (normalised by $\Pi_{\max}$). A reviewer might ask why not call it "conditional plausibility ordering" or "normalised necessity." Be prepared to defend the name.

20. **D-S theory connection** (lines 260-300). This paragraph connects possibility to Dempster-Shafer belief functions. It's a deep excursion for a JAS reader. Is it necessary here, or would an appendix reference suffice? (The appendix `appendix-ds-theory.tex` exists but is commented out in `main.tex`.)

21. **"Subnormality signals that the forecasting system acknowledges gaps in its own knowledge"** — this anthropomorphises the distribution. A reviewer might say: "A numerical artefact doesn't 'acknowledge' anything." Consider: "Subnormality indicates that the distribution reserves some plausibility mass, which we interpret as the system's admitted uncertainty."

---

## Pignistic Bridge (`04-pignistic-bridge.tex`)

22. **New max-additivity sentence** (after desiderata). Read in context: "...proportionality preserves ordering (iv). Note that the allocation sums possibility values rather than taking maxima..." Does the "Note that" transition feel smooth, or should it be a new paragraph?

23. **New $\varepsilon$-floor forward reference** (after Eq. 5). "To prevent $S \to \infty$ when $p_f(c_{\mathrm{obs}}) = 0$..." — does this interrupt the surprise-to-IG flow? The next sentence defines IG. A reader might wonder: "wait, we haven't even used surprise yet, and you're already talking about edge cases." Consider whether the sentence is better placed after the IG definition instead.

24. **Worked example values.** The bridge example uses $\pi = (0.05, 0.2, 0.4, 0.6, 0.1, 0.0)$ — this is a DIFFERENT distribution from Example 1 in the primer ($\pi = (0.05, 0.00, 0.10, 0.20, 0.75, 0.15)$). Is this intentional? The category ordering and peak differ. A reader might be confused by the switch. If intentional, add a sentence noting the new distribution.

25. **"Surprise" terminology** — now consistent (was "self-entropy"). Verify by reading the §3.3 contrast table: the row should say "Surprise (bits)." Also verify the body text at the "stranded mass" paragraph says "surprise," not "self-entropy."

26. **New "(distinct from the three worked scenarios of Section 6)" parenthetical** at the IG archetypes paragraph. Read it in context — does it break the sentence flow? "Figure X illustrates the decomposition for five forecast archetypes (distinct from the three worked scenarios of Section 6). The key contrast is between..." Might feel like a footnote crammed into a parenthetical.

27. **IG decomposition figure caption** — does it still say "(illustrative values)"? Verify the caption text matches the body text's "five forecast archetypes."

28. **$p_{\text{ign}}$ explanation.** The conversion appends an ignorance outcome that "can never be the observed category." This is a strong assumption. What if the observation itself is uncertain? The paper assumes a crisp observation — is this stated explicitly?

29. **"Forced-betting" language.** The conversion is described as producing probabilities for "a forced bet." Some JAS readers may find gambling metaphors off-putting or unclear. Consider whether "decision-theoretic weights" or "probability assignments" reads better.

---

## Native Scorecard (`05-native-verification.tex`)

30. **New Klir phrasing for $\eta$.** "...serving a role analogous to the nonspecificity of Klir (1995) (a Hartley-based measure over $\alpha$-cuts) but computed here as a simple arithmetic mean:" — two sets of parentheses in close proximity. Read aloud: does it parse on first reading, or do the nested qualifiers slow the reader down?

31. **$\eta$ range statement.** "ranging from $1/K$ (sharp) to $1$ (uniform)." Is it clear that $1/K$ corresponds to a delta function (all mass on one category) and $1$ to uniform? A JAS reader might not immediately see why the mean of a delta-like normalised distribution is $1/K$.

32. **Support margin $\delta = \alpha^* - \eta$.** This is the *definition*. But is the *interpretation* sufficiently motivated? "The forecast assigned more plausibility to truth than to the average competitor" — is this what it means? Or is it "truth was above the background"? The name "support margin" suggests the latter, but the formula is truth-minus-mean, not truth-minus-zero.

33. **New propriety paragraph.** Read it in the context of the preceding gaming example and the following Axiom 1 paragraph. Key checks:
    - Does "Eq. 5" resolve to the surprise equation? (Label: `eq:surprise`)
    - Does the gaming example (flooring $\to$ inflates $\eta$) already appear in the preceding paragraph? If so, the propriety paragraph's own example ("broadening support to raise $\alpha^*$ inflates $\eta$ and penalises $\delta$") is a *different* example — good. Verify they don't repeat.
    - "Establishing a formal propriety result...is a direction for future work" — does this match the future-work list in Section 7? If propriety isn't mentioned there, add it.

34. **Scorecard definition box.** Does it list all five metrics with their current names and symbols? Cross-check against Table 1, Table 2, and the abstract.

35. **"Constructive rather than axiomatic."** The paper says the scorecard is chosen to separate four diagnostic dimensions — "support, spread, commitment, dominance." Are these the same four as the "three complementary uncertainty components" (possibility, ignorance, necessity) in the abstract? No — they're different decompositions. Is this confusing?

36. **Permutation invariance.** The text notes all five metrics treat $\Omega$ as unordered. For SPC categories, which have a natural severity ordering (NONE < MRGL < ... < HIGH), this means the scorecard ignores "near misses" (forecasting ENH when MDT verifies). Is this limitation discussed prominently enough?

---

## Three-Lane Architecture (`06-tripartite-value.tex`)

37. **"Each lane has a blind spot" argument.** Three examples are given: (a) broken clock passes categorical but fails probabilistic/possibilistic; (b) lucky conversion passes probabilistic but fails possibilistic; (c) miscalibrated conversion passes possibilistic but fails probabilistic. Verify each example is correct and the counter-lane genuinely catches the failure.

38. **Verification-lanes figure** — does the flowchart match the current three-facet terminology? (No longer "deterministic lane" — now "categorical facet.")

39. **Scorecard figure** (Fig. 9) — the legend triangle is now correct. But verify the amber ignorance markers in the figure body are visually distinguishable from the green improvement triangles. Amber and green are close on some screens.

---

## Worked Examples (`07-worked-examples.tex`)

40. **Scenario distributions.** Check all three distributions against `fig_three_scenario.py:SCENARIOS`. The worked text and the figure must use identical values. Cross-check Table 5 scorecard values against `compute_scorecard()` output.

41. **Table 5 IG values.** Scenario A: $\text{IG} = +4.399$ bits; Scenario B: some positive value; Scenario C: large negative. Are these computed with $\varepsilon = 0.01$ flooring? The new forward reference in Section 3.2 says "throughout" — so all three scenarios should use it. But the text only discusses $\varepsilon$ in detail for Scenario C. Is this confusing?

42. **Sensitivity analysis for $\varepsilon$.** Currently in Section 6.3. Does it cover a range of $\varepsilon$ values? Does it show that the qualitative conclusions (A > B > C) are robust? If you've added the forward reference, the reader will expect the sensitivity analysis to be thorough.

43. **"Why not floor everything at $\varepsilon$?"** paragraph. This argues against universal flooring. But the new Section 3.2 sentence says "converted probabilities are floored at $\varepsilon = 0.01$ throughout." Is there a contradiction? The floor applies to *converted* probabilities (from the bridge), not to raw possibilities. Make sure this distinction is clear.

44. **Scenario C ("sharp-wrong").** The distribution has all mass on the wrong category. After conversion with $\varepsilon$-floor, $p(c_{\text{obs}}) = \varepsilon = 0.01$, yielding surprise $= -\log_2(0.01) \approx 6.64$ bits. Verify this matches the text. If the distribution also has $\ign > 0$, some mass goes to the ignorance outcome, so $p(c_{\text{obs}})$ might be slightly above $\varepsilon$. Check.

45. **Filling gauge figure** (Fig. 3 in document order?) — does it show Scenario A values only, or all three? Verify the caption matches.

---

## Discussion (`08-discussion.tex`)

46. **Domain-agnostic claim** (line 25). "Applies to any finite universe of discourse $\Omega$..." — the paper has only demonstrated SPC categories ($K = 6$). What about very large $K$ (e.g., $K = 100$ for gridded precipitation categories)? Does $\eta = (1/K)\sum \pi'(c)$ become uninformative when $K$ is large? Worth a sentence.

47. **Generating possibilistic forecasts subsection.** Does this subsection promise that possibilistic forecasts are easy to generate? If so, a reviewer might ask for a concrete example. The Ffion/LLM material was removed — is there a gap?

48. **Severity matrix.** Is it connected to the scorecard? The review triage says this was done in Round 2, but verify the connection is explicit (e.g., "the severity matrix can be read alongside the scorecard to assess whether high-commitment forecasts are concentrated on high-consequence categories").

49. **Neal (2014) MISSING citation** appears twice in this section. The NSWWS framework is central to the severity-matrix discussion. Without the citation, the reference is hollow.

50. **Future work list.** Check that it includes:
    - Credal-set bounds (mentioned)
    - Multivariate extension (mentioned)
    - Conformal comparison (mentioned)
    - Formal propriety for possibilistic scorecards (NEW — from the propriety paragraph; add if missing)
    - Sample-size guidance (mentioned?)
    - Possibilistic skill score (mentioned?)
    - Ordinal-distance-sensitive scoring (flagged in Section 4)

---

## Figures (all 12)

51. **Fig 1 (possibility anatomy):** "Peak category" label, "MDT; $N_c$ = 0.733" annotation. Verify N_c = 0.733 matches the primer text at `03-possibility-primer.tex:182`.

52. **Fig 2 (three scenarios):** Check each bar chart matches its row in Table 5. Check $\ign$ annotation matches $1 - m$ for each scenario.

53. **Fig 3 (filling gauge):** Check horizontal gauge lengths match Scenario A scorecard values.

54. **Fig 4 (pignistic bridge):** Check the $H_\Pi$ annotation matches the distribution's $\ign$. Are the connecting arrows clear?

55. **Fig 5 (reliability curves):** Check axis labels. "Conditional hit rate" on y-axis — is this standard NWP terminology? Some readers may expect "reliability" or "observed frequency."

56. **Fig 6 (IG decomposition):** Check caption says "(illustrative values)". Check bar labels: "Sharp Correct" etc. — now with body-text note "(distinct from worked scenarios)."

57. **Fig 7 (verification lanes):** Check flowchart arrows match the three-lane description. "Categorical" not "Deterministic."

58. **Fig 8 (categorical scores):** Check n_days=800 in subplot titles or captions. Two-panel layout: threshold sweep + confusion matrix.

59. **Fig 9 (scorecard table):** Legend triangle for ignorance. Check ALL amber markers in the body are triangles (not squares). Check v2.0/v3.0/v4.0 columns — what do these represent? Is it explained in the caption?

60. **Fig 10 (hexbin trajectory):** Check axis labels use "Diffuseness $\eta$" and "Depth-of-truth $\alpha^*$" (current names). Check that the green trajectory is visible against the hexbin background.

61. **Fig 11 (commitment diagram):** y-axis should say "Support margin $\delta = \alpha^* - \eta$". x-axis should say "Commitment $m$" or similar. Verify both.

62. **Fig 12 (severity matrix):** Check connection to scorecard is noted in either caption or body text.

---

## Notation and Terminology Consistency

63. **"Peak category" vs "mode."** Round 3 renamed mode $\to$ peak category. Grep for "mode" throughout — it should only appear in non-technical senses ("verification mode," "failure mode"), never meaning "the category with highest $\pi$."

64. **"Support margin" vs "resolution gap" vs "discrimination."** $\delta$ should always be "support margin." "Resolution gap" should appear nowhere. "Discrimination" should refer only to DSC. Grep and verify.

65. **"Diffuseness" vs "nonspecificity."** $\eta$ should always be "diffuseness." "Nonspecificity" should appear only in the Klir comparison (Section 4, one occurrence). Verify.

66. **"Dominance margin" for $N_c^*$.** Is this term used consistently? Or does the paper sometimes say "conditional necessity of truth" and sometimes "dominance margin"? Both are acceptable but should map clearly.

67. **$\varepsilon$ vs $\epsilon$.** LaTeX: is it `\varepsilon` everywhere, or do some places use `\epsilon`? These render differently.

68. **"Facet" vs "lane" vs "pillar."** The paper uses "facet" (from the three-facet architecture). Check that "lane" doesn't appear (old terminology) and "pillar" doesn't appear (alternative term).

69. **"Scorecard" — capital or lowercase?** "The scorecard" vs "The Scorecard" — be consistent.

70. **Overbar notation.** $\overline{\alpha^*}$ denotes aggregation. Is this introduced before first use? Is the distinction between per-forecast and aggregate values always clear?

---

## Mathematical Precision vs. Accessibility

71. **Closed-world assumption.** The framework assumes one of $K$ categories will verify. SPC outlooks have "no report" days — are these excluded from the sample? Is this stated?

72. **"Subnormal" vs "non-normal."** The paper uses "subnormal" ($m < 1$). Some possibility-theory texts use "non-normal." A reviewer might flag this. You should know the convention you're following.

73. **Single-observation IG.** The IG formula (Eq. 6) is defined for a single observation. The decomposition into DSC, REL, UNC (Eq. 7) is an *aggregate* identity. Is it clear that the single-observation IG doesn't decompose? The figure shows single-observation bars — these show IG, not DSC/REL per forecast.

74. **$\alpha$-cuts.** The Klir comparison now mentions "$\alpha$-cuts." This term is never defined in the paper. A JAS reader will not know what it means. Is a parenthetical enough, or should you add a brief gloss? e.g., "($\alpha$-cuts, i.e., the set of categories exceeding a given possibility threshold)"

75. **"Scoring rule" vs "verification metric."** The paper uses both. Formally, a scoring rule maps (forecast, observation) $\to$ real number. Some scorecard metrics (like $\alpha^*$) qualify; others (like $\eta$) are forecast-only diagnostics. Is the distinction explicit?

76. **Normalised distribution $\pi' = \pi / m$.** This is called "shape-normalised" in some places. Verify this terminology is consistent and matches the `\pinorm` macro.

---

## Subjective / Challengeable Claims

77. **"Three verification facets are necessary and sufficient."** The paper argues complementarity (each catches what others miss). But does it argue *sufficiency*? A reviewer might ask: "Why not four facets? Why not add a distance-sensitive ordinal facet?" Be prepared to defend the three-facet choice.

78. **"Five metrics."** Why five and not four or six? The constructive argument (four diagnostic dimensions) maps to five metrics because ignorance $\ign$ is independent of shape. A reviewer might argue $\ign$ is redundant with $1 - m$ (which it is, by definition). Why include it separately? Because it appears in the conversion and has independent operational meaning. Make sure this is stated.

79. **SPC categories as running example.** A reviewer might say: "SPC already has calibrated probability forecasts — why would they need possibilistic ones?" The paper's argument is that possibility theory captures a *different kind* of uncertainty (epistemic gaps). Is this argument made clearly enough in the introduction?

80. **$\varepsilon = 0.01$ choice.** Why 0.01 and not 0.001 or 0.1? The sensitivity analysis shows robustness, but the specific value is arbitrary. Is the arbitrariness acknowledged?

81. **SPC climatological baseline** `SPC_CLIM = (0.60, 0.18, 0.12, 0.06, 0.032, 0.008)`. Where do these numbers come from? Are they cited? Are they approximate? A reviewer might want the exact source.

82. **"Publication-quality" figures claim** (implicit). The purple/green scheme works for most colour-vision deficiencies but amber (for ignorance) may be hard to distinguish from green on a deuteranopia simulation. Run the scorecard figure through a colourblindness simulator.

---

## Structural / Flow Issues

83. **Section 3 length.** The possibility primer + bridge + IG + naive normalisation is a lot of math before the reader sees any verification. Some readers will skim ahead to Section 4 and be confused by forward references. Consider a "roadmap" sentence at the start of Section 3.

84. **Section 5 (three-lane architecture) comes after Section 4 (native scorecard).** But the three lanes include the scorecard. So Section 5 is a meta-discussion of a structure that includes Section 4. This is logically fine but some readers may wonder why Section 5 exists as a separate section rather than a subsection of Section 4 or a discussion point.

85. **Section 6 worked examples.** Three scenarios, each with scorecard + IG + categorical analysis. This is thorough but long. Consider whether a reader who only cares about one facet can skip the others. Are the subsection headings informative enough?

86. **Appendices.** `appendix-ds-theory.tex` and `appendix-alternative-scores.tex` are commented out. If the D-S connection paragraph in Section 3 is too heavy, one option is to move it to the appendix and re-enable it. If the IRLS score is discussed in future work, re-enabling the alternative-scores appendix would provide supporting material.

---

## Deferred Items

87. **MISSING bibliography keys (7 keys, 13 occurrences):**
    - `Dubois2006-MISSING` (2x): 03-possibility-primer.tex, 02-introduction.tex
    - `Shafer1976-MISSING` (2x): 03-possibility-primer.tex, 02-introduction.tex
    - `Smets1990-MISSING` (3x): 03-possibility-primer.tex, 04-pignistic-bridge.tex, 02-introduction.tex
    - `Murphy1993-MISSING` (2x): 02-introduction.tex, 04-pignistic-bridge.tex
    - `Jolliffe2012-MISSING` (1x): 02-introduction.tex
    - `Walley1991-MISSING` (1x): 02-introduction.tex
    - `Neal2014-MISSING` (2x): 08-discussion.tex

88. **Acknowledgments** — backmatter placeholder. Add funding, institutional affiliation (USU/BRC), and any reviewer acknowledgments.

89. **Data Availability** — backmatter placeholder. The code is "publicly available" per Section 9 — add the GitHub URL and specify the conda environment.

90. **`Wilks2011-vw` key swap.** `CLAUDE.md` notes this key exists in paperpile.bib as `Wilks2011-vw` but the tex may reference it differently. Verify.
