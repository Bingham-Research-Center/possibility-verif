# Triage of `manuscript_review_ghcp-codex5p4.md`

Assessed against repo state as of 2026-03-30 (commit `9b57796`).

## Must-fix issues

| # | Reviewer issue | Verdict | Evidence / notes |
|---|---|---|---|
| C1 | **Bridge framed as theoretically compelled** | **Partially fixed** | §3 now opens with 4 explicit desiderata and a "Distinction from the pignistic transform" subsection. But `04-pignistic-bridge.tex:108-111` still reads "correctly inflated the ignorance outcome" and "honestly reflects the system's partial uncertainty" — normative language the reviewer flagged. |
| C2 | **Scorecard metrics lack design rationale; "no single metric can be improved without degrading another"** | **Partially fixed** | The plain-language box in §4 describes each metric operationally. The verbatim "no single metric…" claim appears to be gone. But the reviewer wanted a short explicit paragraph separating *why these five* from *what they measure* — that paragraph doesn't exist yet. |
| C3 | **Synthetic data provenance inconsistent; missing `fig_perf_iterate.py`** | **Fully fixed** | `generate_reforecast(n_days=800, seed=42)` is canonical in `fig_performance_diagram.py`. `fig_perf_iterate.py` exists and imports it. All dependent scripts (`fig_categorical_scores.py`, `fig_reliability_curves.py`) use the same generator. Headers document shared provenance. n_days is consistent everywhere. |
| H1 | **IG decomposition figure reads empirical but is schematic** | **Mostly fixed** | Caption now says "(illustrative values)". Body text at line 205 says "illustrates the decomposition for five forecast archetypes" — doesn't explicitly say "schematic" but paired with the caption this is probably sufficient. Minor. |
| H2 | **Overclaiming: "independently contributes," "invisible to the others," "conversion problem"** | **Partially fixed** | "independently contributes verification value" persists at `02-introduction.tex:130-131` and `08-discussion.tex:21`. "invisible to the others" persists at `00-abstract.tex:24` and `07-worked-examples.tex:12`. "has a conversion problem" at `06-tripartite-value.tex:128`. The continuous-extension "straightforward" claim is **gone**. |
| H3 | **Worked-example target treated as observation** | **Fixed** | `02-introduction.tex:31-36` now explicitly says "thought experiments" and "no claim is made that SPC currently produces possibilistic forecasts." Clear pedagogical framing. |

## Should-fix issues

| # | Reviewer issue | Verdict | Notes |
|---|---|---|---|
| S1 | **Nc\* vs Nc(ĉ) notation switch between §4 and §5** | **Unchecked / likely persists** | Reviewer noted the symbol family is close enough to confuse. Worth a quick pass. |
| S2 | **Notation drift (m, Pi_max, pi_max, H_Pi, ign, N_c, Nc)** | **Improved** | Notation table exists in §2. Scripts and text are more consistent now. Reviewer's suggestion of a one-line "figure notation map" could still help. |
| S3 | **S = α\*(1−η) undefined in text** | **Fixed** | Now explicitly defined as "possibilistic analogue of CSI" in the performance-diagram discussion (`05-native-verification.tex:~330-352`). |
| S4 | **δ-vs-climatology analogy vs "no skill score defined" tension** | **Persists** | `06-tripartite-value.tex` discusses δ relative to climatology. `08-discussion.tex:112-114` says no possibilistic skill score is defined. Both statements are present; neither links to the other. |
| S5 | **"Extension to continuous variables is straightforward"** | **Fixed** | That sentence is gone from the discussion section. |

## Reviewer strengths section

All five strengths remain valid — ignorance-erasure hook, teachable order, raw-vs-normalized tables, three scenarios, candid limitations.

## Remaining actionable edits

| Priority | Location | Action |
|---|---|---|
| High | `04-pignistic-bridge.tex:108-111` | Replace "correctly inflated" → "inflated" and "honestly reflects" → "retains" or "preserves". Two-word fixes. |
| High | `00-abstract.tex:24` | "invisible to the others" → "that may be obscured in any single facet" |
| High | `02-introduction.tex:130-131` | "establishes that each…independently contributes" → "illustrates that each…can contribute distinct" |
| High | `08-discussion.tex:21` | Same: "independently contributes" → "can contribute distinct" |
| High | `07-worked-examples.tex:12` | "invisible to the others" → "that may be obscured in any single facet" |
| Medium | `06-tripartite-value.tex:128` | "has a conversion problem" → "may indicate distortion introduced by the conversion" |
| Medium | `05-native-verification.tex` (scorecard box area) | Add 2-3 sentence "design rationale" paragraph: *why these five*, what they separate (support, spread, commitment, dominance), and that the set is constructive not axiomatic. |
| Low | `06-tripartite-value.tex` / `08-discussion.tex` | Add a cross-reference sentence linking the δ-vs-climatology discussion to the "no skill score" limitation, so they don't read as contradictory. |
| Low | §4 or notation table | Optional: one-sentence figure-notation map (m = Pi_max = max(π), H_Pi = ign, N_c ≡ Nc in scripts). |

## Review quality assessment

The review is **well-targeted**. Its strongest points are C1 (bridge normative language) and H2 (overclaiming), which still have residual issues. C3 (data provenance) was the most serious technical concern and is now fully resolved. The reviewer correctly identified the IG-figure labeling gap (now mostly fixed) and the worked-example target framing (now fixed). The suggested rewrites are concrete and mostly sensible — the proposed "operational transform" framing for the bridge and the verb-softening suggestions are worth adopting almost verbatim.

Weakest part of the review: S1 (Nc notation) is vague without a concrete alternative symbol, and the "no single metric can be improved" claim the reviewer flagged at `05-native-verification.tex:226-229` doesn't appear to exist at those line numbers in the current manuscript — suggests the reviewer was working from an older draft or hallucinating the exact location.
