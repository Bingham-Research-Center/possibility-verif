# Manuscript Review

## Executive Summary

Based on the current working tree, the manuscript has a strong macro-structure and a potentially useful core idea: preserve subnormality instead of normalizing it away. But it is not yet methodologically tight enough for submission. The main problems are not cosmetic. Central quantities change meaning across sections, the "five-number" scorecard becomes six numbers in the worked-example table, several claims are presented as demonstrated when the repository only shows synthetic illustrations, and the provenance of key aggregate figures is internally inconsistent and partly unreproducible from the current tree. The possibility-to-probability bridge also reads as justified rather than proposed, without enough axiomatic support. A careful non-author can follow the narrative, but cannot yet trust all of the technical claims at face value.

## Must-Fix Issues

| severity | file:line | issue | why it matters | concrete rewrite suggestion |
| --- | --- | --- | --- | --- |
| Critical | `sections/06-tripartite-value.tex:60`; `sections/08-discussion.tex:19` | Synthetic figures are discussed as if they demonstrate or confirm component value. | The synthetic generator encodes category-dependent accuracy and ignorance, so these plots illustrate expected behavior rather than independently validating it. | Recast these sections as illustration, not confirmation: replace "demonstrated"/"confirming" with "illustrate"/"suggest," or add real-data/held-out evidence if stronger claims are kept. |
| Critical | `sections/05-native-verification.tex:236`; `scripts/fig_performance_diagram.py:246` | Aggregate-figure provenance is inconsistent and partly blocked. | The manuscript says the shared reforecast is `n=730` over two years, later calls it three-year, and the performance script imports a missing `fig_perf_iterate` module, so the reader cannot audit what produced the figures. | Choose one dataset description everywhere and include complete figure-generating code for the performance/commitment figures in the repo. |
| Major | `sections/05-native-verification.tex:114`; `sections/07-worked-examples.tex:216` | The "five-number scorecard" becomes six numbers in the worked-example table because `m` is added. | This blurs the identity of the paper's main method. | Either remove `m` from the comparison table or redefine the framework consistently as "five scorecard metrics plus commitment context." |
| Major | `sections/03-possibility-primer.tex:92`; `sections/07-worked-examples.tex:50` | Core notation is semantically unstable: `m` is called subnormality, low/high subnormality, and commitment; `delta` is called both resolution gap and discrimination. | A careful reader cannot tell whether these are synonyms or distinct concepts. | Rename `m` as `pi_max` or commitment throughout, reserve subnormality/ignorance for `1-m`, and pick one name for `delta` everywhere. |
| Major | `sections/03-possibility-primer.tex:133`; `scripts/fig_possibility_anatomy.py:66` | Figure 1's caption says conditional necessity is annotated, but the image labels the peak category as `N_c = MDT`. | This misintroduces notation at the first key explanatory figure. | Either annotate the numeric quantity `N_c(MDT) = 0.733` or relabel the category as `c_hat = MDT` / "mode category." |
| Major | `sections/04-pignistic-bridge.tex:23`; `scripts/fig_pignistic_bridge.py:20` | The possibility-to-probability bridge is presented as if it were canonically justified, and is labeled "pignistic," but no axioms or uniqueness argument support that status. | The probabilistic lane depends on this conversion, so the paper must distinguish proposal from derivation. | State explicit desiderata for the bridge, present it as one operational transform, and sharpen the distinction from Smets's pignistic transform. |
| Major | `sections/07-worked-examples.tex:120`; `scripts/fig_categorical_scores.py:160` | Scenario C is said to "miss at every threshold" and have POD `=0` across the board. | That is false for `HIGH+`: with observed `MDT`, `HIGH+` is a correct non-event, not a miss. | Rewrite as "misses every threshold up to `MDT+`; at `HIGH+` it is a correct no-event." |
| Major | `sections/05-native-verification.tex:226`; `sections/08-discussion.tex:32` | Several methodological claims are asserted without proof or citation: metric trade-off inevitability, the `epsilon=0.01` floor rationale, the "30 cases per stratum" rule, and "straightforward" extension to continuous variables. | Unsupported universal claims weaken trust in the rest of the formalism. | Either cite/derive each claim or explicitly mark it as heuristic, conjectural, or future work. |
| Major | `sections/02-introduction.tex:79`; `sections/08-discussion.tex:63` | Placeholder citation keys (`-MISSING`) remain in core conceptual and methodological passages. | Readers cannot verify foundational claims or situate the work in the literature. | Replace placeholders with real references before submission or remove the unsupported literature claims. |

## Should-Fix Issues

1. `sections/05-native-verification.tex:57` uses `Pi(A_T)` without defining `A_T`; `sections/03-possibility-primer.tex:224` introduces `nu_c` once and never uses it.
2. `sections/08-discussion.tex:23` and `sections/08-discussion.tex:28` repeat the same "domain-agnostic" point back-to-back; compress to one paragraph.
3. `sections/04-pignistic-bridge.tex:154` presents `ig_decomposition.png` like evidence, but `scripts/fig_ig_decomposition.py:36` says the values are synthetic. Label the figure explicitly as schematic.
4. `sections/05-native-verification.tex:265` introduces ad hoc joint-skill contours `S = alpha* (1-eta)` without formal definition in the method; either define and justify `S` or remove it from the interpretive burden.
5. `reliability_curves.png` is readable but the legend crowds the inset; the small-sample tail is harder to inspect than it should be.
6. A short workflow paragraph would help non-authors: raw `pi` -> raw quantities (`Pi`, `H_Pi`) -> normalized `pi'` -> scorecard -> optional probability bridge -> IG/categorical checks.

## 5 Strongest Strengths

1. The section order is sensible and reader-friendly: primer, bridge, native metrics, lane comparison, worked examples, discussion.
2. The notation table in `sections/03-possibility-primer.tex:78` and raw-vs-normalized table in `sections/05-native-verification.tex:45` materially improve readability.
3. The SPC running example keeps an abstract framework anchored to a concrete forecast universe.
4. The worked examples do a good job showing why "correct but hedged" and "confidently wrong" are different failure modes.
5. The manuscript has a clear conceptual center: ignorance should be preserved, not erased by normalization.

## If Submitted Today

**Major revision.**

The paper has a promising core contribution and a readable high-level arc, but the current draft still mixes proposal, illustration, and evidence too freely. The biggest blockers are central-definition drift, unsupported methodological claims, and figure provenance/validation issues. Those are fixable, but they touch the manuscript's main claims, not just polish.

## Top 3 Highest-Leverage Rewrites

1. Rewrite Sections 5 to 8 so synthetic results are explicitly illustrative, not confirmatory, and make the aggregate-figure dataset/source fully consistent and reproducible.
2. Standardize the core vocabulary: `m`/`pi_max`/commitment, `H_Pi`/ignorance/subnormality, and `delta`/resolution gap vs discrimination.
3. Rewrite the bridge section to state the transform as a proposed operational choice with explicit desiderata, then trim or qualify every downstream claim that currently assumes that choice is uniquely justified.
