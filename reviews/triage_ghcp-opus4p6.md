# Triage of `manuscript_review_ghcp-opus4p6.md`

Assessed against repo state as of 2026-03-30 (commit `186b218`).

## Must-fix issues

| # | Reviewer issue | Verdict | Evidence / notes |
|---|---|---|---|
| M1 | **2-year vs 3-year data inconsistency** | **Fixed** | Text now says "$n = 800$ active days" (`05-native-verification.tex:293`). All captions say "800-day synthetic reforecast." All scripts (`fig_categorical_scores.py`, `fig_reliability_curves.py`) import `generate_reforecast` from `fig_performance_diagram.py` which uses `n_days=800`. No 2-year/3-year language remains. |
| M2 | **Figure 1 "$N_c$ = MDT" annotation** | **Persists** | `fig_possibility_anatomy.py:76` still renders `$N_c$ = MDT` — equating a numerical function ($N_c \in [0,1]$) with a category name. The text label above ("Most certain category") is fine, but the mathematical annotation is wrong. |
| M3 | **δ called "discrimination"** | **Fixed** | δ is now consistently "support margin" everywhere. Grep for "discrimination" near "delta" returns zero hits. Commitment diagram y-axis (`fig_perf_iterate.py:410`) reads "Support margin $\delta = \alpha^* - \eta$". "Discrimination" is reserved exclusively for DSC. |
| M4 | **Dead $\nu_c$ notation** | **Fixed** | Grep for `\nu_c` across all section files returns zero hits. |
| M5 | **Duplicate paragraphs in discussion** | **Fixed** | `08-discussion.tex` has only one statement about domain applicability (line 25: "applies to any finite universe of discourse"). The duplicate "domain-agnostic" paragraph is gone. |
| M6 | **"Self-entropy" mislabeling** | **Persists** | `04-pignistic-bridge.tex:250` ("inflates the self-entropy") and `:266` (table row "Self-entropy (bits)") both use the term. The quantity computed is $-\log_2(p(c_{\text{obs}}))$ — surprise (log-score), not self-entropy ($H(\mathbf{p}) = -\sum p_i \log p_i$). Eq. 5 correctly calls this "surprise." |
| M7 | **Missing `fig_perf_iterate.py`** | **Fixed** | `scripts/fig_perf_iterate.py` exists and imports `generate_reforecast` from `fig_performance_diagram.py` and scenarios from `fig_three_scenario.py`. |
| M8 | **$m$ glossed as "Subnormality"** | **Fixed** | `03-possibility-primer.tex:103` now reads "Commitment (peak possibility): $\max_\omega \pi(\omega)$". |

## Should-fix issues

| # | Reviewer issue | Verdict | Notes |
|---|---|---|---|
| S1 | **η ≠ Klir's nonspecificity** | **Persists** | `05-native-verification.tex:166-167` still says "inspired by the nonspecificity concept of Klir (1995)." Reviewer suggested "analogous in spirit to" to avoid the implicit claim of formal equivalence. η is already renamed to "diffuseness," so the conceptual distance from Klir is clear, but the "inspired by" phrasing remains. |
| S2 | **IG figure shares scenario names with A/B/C** | **Partially fixed** | Caption now says "(illustrative values)" and body text says "five forecast archetypes" (`04-pignistic-bridge.tex:205-206`). But the bar labels ("Sharp Correct", "Hedged Correct", etc.) still match the worked-scenario descriptions in §6, which could confuse a reader encountering the IG figure first. No footnote or relabeling was added. |
| S3 | **ε-floor not formalized as protocol** | **Persists** | The ε-floor is discussed thoroughly in §6.3 (`07-worked-examples.tex:204-216`) with sensitivity analysis, but no general protocol statement was added to §3.1 as the reviewer suggested. A reader encountering IG computation before §6 won't know about ε. |
| S4 | **Abstract / Significance Statement overlap** | **Mostly fixed** | The Significance Statement (`01-significance.tex`) is now distinctly practitioner-oriented ("distinguish honestly uncertain forecasts from confidently wrong ones"), while the abstract is technical. Both necessarily mention the scorecard, conversion, and three facets, but the tone and emphasis are differentiated. |
| S5 | **Conversion doesn't use max-additivity** | **Persists** | No mention of max-additivity in `04-pignistic-bridge.tex`. The conversion proportionally distributes mass, treating possibilities as unnormalized probability weights. No sentence acknowledging that this ignores max-additive structure. |
| S6 | **No discussion of incentive compatibility** | **Persists** | No matches for "incentive," "propriety," or "proper score" anywhere. `05-native-verification.tex:277-281` discusses anti-gaming resistance but not formal propriety. |
| S7 | **Introduction length and structure** | **Persists** | `02-introduction.tex` is 136 lines mixing motivation, literature, SPC example setup, and roadmap. The SPC example setup (lines 25-36) is still embedded in the introduction rather than deferred to §2. |
| S8 | **MISSING bibliography keys** | **Persists** | All 7 keys still appear: `Dubois2006-MISSING` (×2), `Shafer1976-MISSING` (×2), `Smets1990-MISSING` (×3), `Murphy1993-MISSING` (×2), `Jolliffe2012-MISSING` (×1), `Walley1991-MISSING` (×1), `Neal2014-MISSING` (×2). Total: 13 occurrences across `02-introduction.tex`, `03-possibility-primer.tex`, `04-pignistic-bridge.tex`, `08-discussion.tex`. |
| S9 | **Scorecard figure legend symbol mismatch** | **Persists** | `fig_scorecard_table.py:133` plots triangles (`"^"` / `"v"`) for ALL rows including ignorance, but the legend at `:174` shows a square (`marker="s"`) for "Ignorance* (context-dep.)". The legend doesn't match the figure. |
| S10 | **Categorical figure uses 3-year data** | **Fixed** | `fig_categorical_scores.py:19` imports `generate_reforecast` from `fig_performance_diagram.py` (same `n_days=800` generator used by all figures). Part of the M1 fix. |

## Summary

**Fixed (7):** M1, M3, M4, M5, M7, M8, S10

**Mostly/partially fixed (2):** S2 (archetype labeling footnote missing), S4 (structural overlap remains but tone differentiated)

**Persists (7):** M2, M6, S1, S3, S5, S6, S7, S8, S9

## Remaining actionable edits

| Priority | Location | Action |
|---|---|---|
| **High** | `scripts/fig_possibility_anatomy.py:75-77` | Change `$N_c$ = MDT` annotation. Options: (a) "Peak: MDT" with "$N_c(\text{MDT}) = 0.733$" on second line, or (b) remove $N_c$ from figure, keep only in caption. Regenerate `possibility_anatomy.png`. |
| **High** | `04-pignistic-bridge.tex:250, :266` | Replace "self-entropy" → "surprise" (both occurrences). The table row label becomes "Surprise (bits)" to match Eq. 5. |
| **Medium** | `05-native-verification.tex:166-167` | Change "inspired by the nonspecificity concept" → "analogous in spirit to the nonspecificity concept" (or just drop the Klir reference from the η definition and keep it only in a parenthetical). |
| **Medium** | `scripts/fig_scorecard_table.py:174` | Change legend `marker="s"` → `marker="^"` (or use both `"^"` and `"v"` handles in amber) to match the actual triangle markers used for ignorance rows. Regenerate `scorecard_table.png`. |
| **Medium** | `04-pignistic-bridge.tex` (near §3.1 end) | Add one sentence noting that the proportional allocation does not exploit the max-additive structure of possibility — and briefly why that's acceptable (the conversion's purpose is forced-betting probabilities, not a possibilistic operation). |
| **Medium** | `04-pignistic-bridge.tex` (before IG section) or `05-native-verification.tex` | Add a protocol sentence: "In all subsequent computations, converted probabilities are floored at $\varepsilon = 0.01$ to prevent infinite log-scores." Currently the ε-floor appears only in §6.3. |
| **Low** | `fig_ig_decomposition.py:28-34` or `04-pignistic-bridge.tex` caption | Add a footnote: "These are illustrative archetypes; the specific worked examples in Section 6 use different distributions." Or relabel bars to "Archetype I/II/III/IV/V." |
| **Low** | `05-native-verification.tex` scorecard area | Add 1-2 sentences noting that formal propriety (incentive compatibility) is an open question for possibilistic scores, and that the multi-metric design makes unilateral gaming unprofitable. |
| **Low** | `02-introduction.tex` | Optional structural edit: move SPC example setup (lines 25-36) to opening of §2, shortening the introduction. |
| **Deferred** | Multiple files | Resolve 7 MISSING bibliography keys (13 occurrences). Already tracked in `CLAUDE.md` and `MISSING-REFS.md`. |
