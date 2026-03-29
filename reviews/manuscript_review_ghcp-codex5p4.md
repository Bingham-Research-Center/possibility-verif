## Executive summary

This is a promising and often readable methodology paper with a clear motivating problem: normalizing subnormal possibility distributions destroys information about admitted ignorance. The manuscript’s structure is sensible, the running SPC example is accessible, and several figures genuinely aid understanding. The main weakness is not exposition so much as claim calibration. The paper repeatedly presents operational design choices as if they were theoretically compelled: the probability bridge, the scorecard construction, and some of the complementarity claims all need sharper scoping or stronger justification. Figure support also needs cleanup: the “shared synthetic reforecast” is inconsistently described, one central plotting dependency is missing from the tree, and one figure is schematic in the script but reads empirical in the paper. I would recommend **major revision** before submission.

## Must-fix issues

| severity | file:line | issue | why it matters | concrete rewrite suggestion |
| --- | --- | --- | --- | --- |
| Critical | `sections/04-pignistic-bridge.tex:23-50,72-75,180-186` | The possibility-to-probability bridge is written as if it is the correct or principled conversion, but the manuscript does not derive it from possibility theory, a betting principle, or an optimality result. Phrases like “correctly penalise” and “honestly reflects” overstate what is shown. | This is a central methodological move. If it is a proposed operational bridge rather than a theorem, readers need that stated explicitly; otherwise the paper overclaims rigor at the point where it most needs it. | Reframe the bridge as a **proposed operational transform** and then list its design goals/properties explicitly: sums to one, reduces to simple normalization when `m=1`, penalizes larger `\ign`, and keeps ignorance observable. Replace normative wording with scoped wording such as “yields a stronger penalty for subnormal forecasts under log scoring.” |
| Critical | `sections/05-native-verification.tex:157-171,226-229`; `sections/07-worked-examples.tex:264-276` | The core scorecard metrics `\eta` and `\delta` are introduced with only light justification, and the sentence “no single metric can be improved without degrading another” is unproved and likely false as written. | Because the paper’s main contribution is the scorecard, readers need to know why these particular functionals were chosen and which properties they satisfy. Without that, the scorecard can look ad hoc. | Add a short “design rationale” paragraph or proposition for each metric: what behavior it rewards, what bounds it has, and why alternatives were not used. Replace the absolute trade-off claim with something like: “The multi-metric scorecard exposes common trade-offs and makes simple gaming strategies, such as uniform `\varepsilon`-flooring, easier to detect.” |
| Critical | `sections/05-native-verification.tex:236-278`; `sections/07-worked-examples.tex:91-123`; `scripts/fig_performance_diagram.py:79-80,246-251`; `scripts/fig_categorical_scores.py:87`; `scripts/fig_reliability_curves.py:45` | The manuscript refers to a shared synthetic reforecast, but the current tree does not support that cleanly: the prose says `n = 730` / two years, figure captions say three years, scripts use different `n_years`, and the performance-diagram script imports a missing `fig_perf_iterate.py`. | This weakens both readability and methodological confidence. A careful reader cannot tell which figures are actually comparable, and the current tree does not fully document how two central figures were produced. | Consolidate synthetic-data provenance in one place. Use one generator module, one stated sample length, and one explicit note for any exceptions. Either include the missing performance-diagram helper in the tree or rewrite `fig_performance_diagram.py` so the figures are reproducible from files that actually exist. |
| High | `sections/04-pignistic-bridge.tex:148-162`; `scripts/fig_ig_decomposition.py:36-45` | The IG decomposition figure reads like evidentiary support for the method, but the script says it uses “plausible synthetic values” rather than values derived from the worked scenarios or the shared reforecast. | That mismatch can mislead readers about what has actually been demonstrated. A schematic can be useful, but it must be labeled as schematic. | Either compute the bars from an actual dataset used elsewhere in the paper, or change the caption/text to say explicitly that the figure is an **illustrative schematic decomposition** rather than an analyzed result. |
| High | `sections/00-abstract.tex:21-24`; `sections/02-introduction.tex:111-130`; `sections/06-tripartite-value.tex:108-115`; `sections/08-discussion.tex:19-22,28-33` | The manuscript repeatedly claims more than it shows: “each component independently contributes verification value,” the lanes reveal “failure modes invisible to the others,” and poor IG is described as “a conversion problem.” Those claims are only illustrated by thought experiments and synthetic plots, not established generally. | Overclaiming is especially risky in a conceptual methods paper; skeptical readers will push back on scope before they engage with the underlying idea. | Temper these claims to match the evidence. Use verbs like “illustrates,” “suggests,” or “can reveal,” and reserve stronger language (“establishes,” “invisible,” “conversion problem”) for cases where you either prove the statement or show a clearly defined counterexample. |
| High | `sections/02-introduction.tex:31-36`; `sections/07-worked-examples.tex:23-25,44,63,83` | The worked examples treat the final SPC category at a point as the “observation,” but that is a proxy forecast product rather than physical truth. The manuscript notes the examples are thought experiments, but not strongly enough to prevent confusion. | A non-author expert reader may stop here and ask, “Are we verifying forecasts against another forecast?” That question interrupts trust in the examples and obscures what is pedagogical versus operational. | In the introduction and example setup, rename this quantity as a **proxy verification target** or **pedagogical target category**, and say explicitly that the examples are for illustrating the scoring framework rather than demonstrating real-world forecast verification against realized weather observations. |

## Should-fix issues

1. `sections/05-native-verification.tex:182-192` vs. `sections/06-tripartite-value.tex:60-68`: the manuscript shifts from `\Nc^*=\Nc(c_{\mathrm{obs}})` to reliability of `\Nc(\hat c)` at the predicted mode. The text does mention the switch, but the symbol family is close enough that readers will still stumble. I would give the mode-based quantity a visibly different notation in Section 6.

2. `sections/03-possibility-primer.tex:117-145`; `sections/05-native-verification.tex:305-328`; `scripts/*.py`: notation drifts between `m`, `\Pi_{\max}`, `\pi_{\max}`, `H_\Pi`, `\ign`, `N_c`, and `\Nc`. The manuscript is mostly internally consistent, but the figure language forces the reader to keep translating. A one-line “figure notation map” or stricter standardization would help.

3. `sections/05-native-verification.tex:265-289`: the performance diagram introduces `S=\alpha^*(1-\eta)` in the caption without defining whether it is a formal metric or just a visual aid. Either define it in the text or mark it explicitly as an informal diagnostic surface used only for that figure.

4. `sections/06-tripartite-value.tex:18-27` and `sections/08-discussion.tex:112-114`: Section 6 talks about comparing `\delta` against climatology or persistence as an analogue of a skill-score comparison, while the limitations section later says no possibilistic skill score is defined. Those statements can coexist, but they need tighter wording so they read as conceptual analogy rather than implemented methodology.

5. `sections/08-discussion.tex:28-33`: “Extension to continuous forecast variables is straightforward via `\alpha`-cut discretisation” is too strong for a paper that does not actually carry out that extension. Move that sentence to Future Directions or qualify it much more carefully.

## 5 strongest strengths

1. The motivating contrast between epistemic ignorance and normalized confidence is strong. The “ignorance erasure” problem gives the paper a real conceptual hook.

2. The manuscript is organized in a teachable order: primer → bridge → native verification → component value → worked examples. A careful reader can follow the intended logic without already being a possibility-theory specialist.

3. The raw-vs.-normalized distinction is one of the clearest parts of the paper. `Table~\ref{tab:notation}` and `Table~\ref{tab:raw_norm}` do real explanatory work.

4. The three hand-built scenarios are genuinely effective. They make it easy to see why “sharp-correct,” “hedged-correct,” and “sharp-wrong” should not collapse to the same diagnosis.

5. The paper is refreshingly candid about several limitations, especially the lack of a possibilistic climatology and the closed-world assumption. That honesty gives the work a credible revision path.

## If submitted today verdict: major revision

The paper has a solid core idea and several parts are already close to publishable exposition, but the current draft still asks the reader to grant too much without enough support. The main revisions are not cosmetic: the central methods need clearer status labels (axiom, design choice, illustration, or empirical result), and the figure/data provenance needs to be internally consistent and reproducible from the current tree. With those fixes, this could become a strong conceptual-methods paper.

## Top 3 highest-leverage rewrites

1. Add one short subsection that explicitly separates **theory**, **design choices**, and **illustrations**. Do this for the probability bridge, the five scorecard metrics, and the lane-complementarity claims.

2. Replace the scattered synthetic-data descriptions with one reproducibility block: sample length, generator, seed if relevant, which figures use the shared reforecast, and which figures are schematic only.

3. Reword the example framing so the target in Section 7 is unmistakably a pedagogical proxy rather than a physical observation, then tighten verbs throughout (`illustrates` instead of `establishes`, `can reveal` instead of `is invisible`, `may distort` instead of `has a conversion problem`).

## Revision checklist and issue-by-issue rewrite guide

### Revision checklist

- [ ] Recast the probability bridge as a **proposed operational transform**, not a theoretically compelled conversion.
- [ ] Add a short rationale for why the scorecard uses `\alpha^*`, `\eta`, `\delta`, `\ign`, and `\Nc^*`, including what each metric is intended to reward or penalize.
- [ ] Remove or soften unproved universal claims such as “independently contributes verification value,” “invisible to the others,” and “no single metric can be improved without degrading another.”
- [ ] Harmonize the synthetic-data description across prose, captions, and scripts, and fix the missing plotting dependency for the performance diagrams.
- [ ] Mark schematic figures as schematic if they are not computed from the shared synthetic reforecast.
- [ ] Clarify that the Section 7 target category is a pedagogical or proxy verification target, not physical observed truth.
- [ ] Tighten notation across manuscript and figures so readers are not forced to translate between `m`, `\Pi_{\max}`, `\pi_{\max}`, `H_\Pi`, `\ign`, `N_c`, and `\Nc`.
- [ ] Either define `S=\alpha^*(1-\eta)` in the text or explicitly label it as a figure-only diagnostic surface.

### Concrete rewrite suggestions by issue

#### 1. Probability bridge: state its status more carefully

For `sections/04-pignistic-bridge.tex:23-50`, I would insert a framing sentence before the three-step construction:

> “We propose an operational possibility-to-probability transform for verification purposes. The transform is not claimed to be unique; rather, it is designed to satisfy four practical goals: preserve subnormality information, reduce to ordinary normalization when `\ign=0`, yield a valid probability vector, and expose admitted ignorance to downstream scoring rules.”

Then revise the stronger claims at `04-pignistic-bridge.tex:45-46,72-75,183-186` along these lines:

- Replace “ensuring that verification scores correctly penalise uncertain forecasts” with:
  > “so that verification scores penalize subnormal forecasts more strongly than simple normalization does.”

- Replace “honestly reflects the system’s partial uncertainty” with:
  > “retains the forecast’s explicit uncertainty signal in the derived probability vector.”

- Replace “The more ignorant the system, the more mass is stranded, and the larger the penalty” with:
  > “Under this transform, larger `\ign` strands more mass in the auxiliary ignorance outcome, increasing the log-score penalty relative to simple normalization.”

#### 2. Scorecard: justify why these five numbers, not just what they are

For `sections/05-native-verification.tex:157-171,226-229`, add a short rationale paragraph after the definitions:

> “The scorecard is intentionally constructive rather than axiomatic. `\alpha^*` measures support assigned to the truth, `\eta` measures diffuseness of the normalized shape, `\delta=\alpha^*-\eta` summarizes whether the shape favored the truth relative to an average category, `\ign` preserves raw-scale commitment, and `\Nc^*` measures whether the truth dominated its alternatives. We choose these quantities because together they separate support, spread, commitment, and dominance, which collapse under single-number summaries.”

At `05-native-verification.tex:226-229`, replace:

> “Because no single metric can be improved without degrading another, the multi-metric design resists trivial gaming strategies...”

with:

> “Because these metrics reward different aspects of forecast behavior, the multi-metric design makes simple gaming strategies easier to detect. For example, uniformly flooring all categories at `\varepsilon` may reduce catastrophic zeros, but it also increases diffuseness and can weaken discrimination.”

#### 3. Synthetic-data provenance: make one reproducibility statement

For `sections/05-native-verification.tex:234-257` and the figure captions that follow, replace the scattered discussion with one stable block such as:

> “Unless otherwise noted, the diagnostic figures in Sections 5–7 use a single synthetic reforecast generated from the same stochastic recipe and category climatology. The sample contains `N = ...` forecast–verification pairs, and all figures derived from this shared sample are identified explicitly in their captions. Figures that are purely schematic are labeled as illustrative.”

Then make the captions consistent with that exact `N` and duration. If different figures truly use different datasets, say so in each caption instead of implying they are shared.

#### 4. IG decomposition figure: label it as illustrative if it is illustrative

For `sections/04-pignistic-bridge.tex:148-162`, if the figure remains schematic, revise the lead-in and caption:

> “Figure~\\ref{fig:ig_decomp} gives an illustrative decomposition of several stylized forecast scenarios.”

And in the caption:

> “Illustrative information-gain decomposition for five stylized forecast scenarios. Values are schematic rather than estimated from the shared synthetic reforecast.”

If instead you want the figure to support a claim about the shared synthetic sample, compute the bars from that sample and say so explicitly.

#### 5. Complementarity claims: downgrade from general theorem language to supported scope

For `sections/00-abstract.tex:21-24`, `sections/02-introduction.tex:111-130`, `sections/06-tripartite-value.tex:108-115`, and `sections/08-discussion.tex:19-22`, I would make the verbs less absolute:

- Replace “each component independently contributes verification value” with:
  > “the worked examples and synthetic diagnostics suggest that each component can contribute distinct verification value.”

- Replace “diagnosing failure modes invisible to the others” with:
  > “highlighting failure modes that may be obscured in any single lane.”

- Replace “poor IG has a conversion problem” with:
  > “poor IG may indicate either a weak raw forecast or distortion introduced by the chosen conversion.”

This preserves the paper’s main message without asking the reader to accept more than the current evidence supports.

#### 6. Worked examples: make the verification target explicit

For `sections/02-introduction.tex:31-36` and `sections/07-worked-examples.tex:23-25`, I would clarify the pedagogical setup with wording like:

> “These examples are pedagogical thought experiments. To keep the category set fixed, the possibilistic forecast is evaluated against a proxy target category drawn from the final SPC categorical outlook at the point of interest. This is not intended as a claim that forecast verification against realized weather observations has been carried out here.”

That single clarification will head off a major reader objection early.

#### 7. Notation hygiene: add one translation sentence for figure readers

For the first paragraph introducing the diagnostic figures, add:

> “In the figures, `m`, `\Pi_{\max}`, and `1-\ign` all refer to the same raw commitment level; likewise `H_\Pi` and `\ign` denote the same ignorance quantity, and `N_c` in figure scripts corresponds to manuscript notation `\Nc`.”

This is a small addition, but it will reduce avoidable friction for careful readers cross-checking text against code and figure labels.

#### 8. Continuous-extension claim: move it out of asserted present capability

For `sections/08-discussion.tex:28-33`, replace:

> “Extension to continuous forecast variables is straightforward via `\alpha`-cut discretisation.”

with something like:

> “An extension to continuous forecast variables may be possible through `\alpha`-cut discretisation, but working out the corresponding verification design remains future work.”
