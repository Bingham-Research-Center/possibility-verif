# CODEX Review

> Manuscript: *Possible, yes; ignorant, perhaps: a scorecard for possibilistic forecasts*  
> Review lens: Journal of the Atmospheric Sciences / AMS-style peer review  
> Verdict: Major revision before submission  
> Bottom line: The paper has a real idea, a coherent visual language, and a potentially useful diagnostic toolkit. It is not yet submission-ready because the observation space is not scientifically grounded, the subnormal mathematics is not cleanly separated from classical possibility results, and the empirical case is still synthetic/stylized while the prose often claims demonstration rather than proposal.

---

## 1. Referee Markup

### What is worth keeping

| Asset | Why it is worth preserving |
|---|---|
| The central motivation | Preserving "I do not know" is a real forecasting need, and the manuscript frames that need clearly. |
| The finite-category running example | SPC categories are familiar to the target audience and make an abstract theory concrete. |
| The visual toolkit | The gauge, commitment diagram, and scorecard framing are memorable and operationally legible. |
| The overall paper shape | Primer -> bridge -> native metrics -> examples -> discussion is a good skeleton once the theory is tightened. |

### Blocking scientific issues

| Priority | Issue | Why it blocks the paper | Ref |
|---|---|---|---|
| 1 | The "observation" is another forecast label, not a physical outcome. | As written, the paper verifies forecast categories against SPC outlook categories, which are themselves forecast products. JAS readers will expect verification against weather truth, not another forecast taxonomy. | `sections/02-introduction.tex:26-32`, `sections/07-worked-examples.tex:24-29` |
| 2 | Classical possibility/necessity results are used after allowing subnormal distributions. | Once `max pi < 1`, the paper cannot freely reuse statements like `N(A) <= Pi(A)` or interpret `[N(A), Pi(A)]` as a probability bracket without extra conditions. This is the main logical break. | `sections/03-possibility-primer.tex:49-76`, `sections/03-possibility-primer.tex:87-124` |
| 3 | The bridge is presented as if it were the pignistic transform or an established extension. | The text currently moves too quickly from "our proposed conversion" to "this is equivalent to / generalizes Smets." That requires proof, or a more modest framing. | `sections/04-pignistic-bridge.tex:44-53` |
| 4 | The validation claims exceed the evidence. | The examples and several figures are synthetic or stylized, but the discussion says the paper "demonstrated" independent verification value. It proposed and illustrated; it did not demonstrate in a JAS sense. | `sections/06-tripartite-value.tex:16-18`, `sections/06-tripartite-value.tex:103-116`, `sections/08-discussion.tex:22-25` |
| 5 | The IG notation mixes single-case surprise with sample-mean decomposition. | Eq. (IG) is pointwise, but `UNC`, `DSC`, and `REL` are aggregate decomposition terms. The manuscript currently slides between these levels. | `sections/04-pignistic-bridge.tex:101-129` |
| 6 | The scorecard is still partly heuristic but is written like a formal scoring theory. | `eta`, `delta`, the joint-skill contours, and the diagrams are useful diagnostics, but the manuscript has not yet justified them at the same level as standard scoring rules. | `sections/05-native-verification.tex:145-156`, `sections/05-native-verification.tex:198-241` |

### Important but fixable issues

| Issue | Why it matters | Ref |
|---|---|---|
| "Nonspecificity" is introduced with a simple mean of normalized possibility values. | In the possibility literature, that term carries baggage. If this is a custom diffuseness index, name it that way and defend it. | `sections/05-native-verification.tex:145-149` |
| The deterministic lane is underspecified. | The manuscript mentions defuzzified point forecasts, RMSE, and bias, but never defines the defuzzification map or why those metrics are appropriate for categorical/ordinal SPC bins. | `sections/06-tripartite-value.tex:136-181` |
| Exceedance bounds are interval answers, not direct probabilities. | The paper often says these "answer probability-of-exceedance questions directly"; they actually return bounds, which is weaker and should be stated that way. | `sections/00-abstract.tex:20-22`, `sections/05-native-verification.tex:284-291` |
| The DS comparison is too loose. | `Nc` is a conditional-normalized construct, not simply DS belief by another name. The analogy is fine; the identity is not. | `sections/03-possibility-primer.tex:213-223`, `sections/08-discussion.tex:35-75` |
| The ensemble-to-possibility proposal is not defended. | Raw ensemble fractions are probabilities or empirical frequencies before they are possibility values; the mapping needs theory, not assertion. | `sections/08-discussion.tex:122-129` |
| The LLM subsection is off-axis for this paper. | It dilutes the verification story and reads like a second paper trying to enter late in the discussion. | `sections/08-discussion.tex:168-228` |

### Submission hygiene and completeness

| Problem | Note | Ref |
|---|---|---|
| Undefined citations remain after compile. | `Murphy1993-MISSING`, `Jolliffe2012-MISSING`, and `Wilks2011-MISSING` are unresolved. | `sections/02-introduction.tex:91-92` |
| Back matter still contains placeholders. | Acknowledgments and code/data versioning are not finished. | `sections/09-backmatter.tex:10-11`, `sections/09-backmatter.tex:25-26` |
| Software-availability wording is ahead of the repo state. | The repo is mostly manuscript and figure scripts; the scorecard logic appears inside a plotting script, not a reusable analysis package. | `sections/08-discussion.tex:233-242`, `scripts/fig_three_scenario.py:35-75` |
| The manuscript compiles, but with unresolved citations and layout warnings. | This is not fatal, but it signals draft status rather than submission polish. | `main.pdf` build check on 2026-03-27 |

---

## 2. Action Microtasks

- Scientific repair
  - [ ] Redefine the verifying truth.
    - [ ] Decide whether the paper verifies:
      - a possibilistic forecast against physical weather outcome categories, or
      - a possibilistic translation of SPC categories against the official SPC category product.
    - [ ] If the first option is chosen, define the weather outcome variable explicitly.
    - [ ] Rewrite all uses of "observed SPC category" so the truth variable is not another forecast.
    - [ ] Carry that repair through abstract, introduction, worked examples, figures, and discussion.
  - [ ] Separate classical theory from the paper's subnormal extension.
    - [ ] State clearly which results require normalized possibility distributions.
    - [ ] Add a short proposition or counterexample showing what fails when `max pi < 1`.
    - [ ] Stop calling `[N(A), Pi(A)]` a valid probability bracket unless the needed conditions are stated.
    - [ ] Introduce `L = m Nc(A)` as the paper's proposed lower-bound object and explain its status carefully.
  - [ ] Reframe the bridge as a proposal unless a derivation is supplied.
    - [ ] Replace "equivalent to the pignistic transform" with "a proposed bridge inspired by pignistic ideas" unless proven.
    - [ ] State what design goals the bridge satisfies:
      - preserves ignorance,
      - yields a proper probability vector,
      - penalizes stranded ignorance under log scoring.
    - [ ] Explain why those design goals are reasonable for forecast verification.

- Verification/statistics repair
  - [ ] Split pointwise and sample-level notation in the IG section.
    - [ ] Keep per-case surprise/log score formulas separate from sample means.
    - [ ] Use expectation notation for `UNC`, `REL`, and `DSC`.
    - [ ] Reword the decomposition as a sample diagnostic, not a single-forecast identity.
  - [ ] Downgrade heuristic metrics where needed.
    - [ ] Say explicitly whether `eta` is a standard nonspecificity measure or a paper-specific diffuseness index.
    - [ ] Justify `delta = alpha* - eta` as a diagnostic, not a proper scoring rule.
    - [ ] Label the performance and commitment diagrams as exploratory/diagnostic graphics.
  - [ ] Define the deterministic lane or cut it.
    - [ ] Specify the defuzzification rule.
    - [ ] Explain why RMSE/bias are meaningful for the chosen category geometry.
    - [ ] Remove the lane if it cannot be defended in a tight way.

- Evidence and scope repair
  - [ ] Replace "demonstrates" language with "illustrates" or add real-data evidence.
    - [ ] Audit all abstract, introduction, results, and discussion claims for overstatement.
    - [ ] Make clear which figures are synthetic and why they are included.
    - [ ] If possible, add one real forecast-outcome dataset, even modest, to ground the framework.
  - [ ] Narrow the discussion to the manuscript's center of gravity.
    - [ ] Compress or remove the LLM communication subsection.
    - [ ] Keep DS and conformal links brief unless they directly support a theorem or method.
    - [ ] Keep future-work claims proportional to what is actually shown.

- Writing and audience repair
  - [ ] Reduce claim density in front matter.
    - [ ] Cut the number of new named objects introduced in the abstract.
    - [ ] Use "we propose" where the paper is not yet empirically validated.
    - [ ] Distinguish "interval answer" from "probability answer."
  - [ ] Write for atmospheric scientists, not possibility specialists.
    - [ ] Keep the primer, but front-load the operational payoff.
    - [ ] Add one concise paragraph explaining what a forecaster gains that ordinary probabilistic verification cannot show.
    - [ ] Use severe-weather examples only where they sharpen the theory.

- Submission cleanup
  - [ ] Resolve the missing citations.
    - [ ] Replace placeholder keys with real bib keys where possible.
    - [ ] Verify every in-text citation after a clean compile.
  - [ ] Finish the back matter.
    - [ ] Fill acknowledgments.
    - [ ] Add code version / DOI / archive reference.
    - [ ] Make the generative-AI statement match journal policy and actual use.
  - [ ] Align repo claims with repo state.
    - [ ] Either package the verification code cleanly, or soften the software-availability prose.
    - [ ] Make README build instructions match the actual successful local compile path.

---

## 3. Batch-by-Batch Plain-Language Map

### Front Matter

#### 0A. Abstract and significance statement
- Plain English: The paper says, "Some forecast systems know when they do not know, and we want a way to score that honestly instead of forcing fake precision."
- Catch: This is the right big idea, but the abstract reads as if the method is already fully established and broadly validated. It is not. It is proposed and illustrated.
- Repair: Change strong verbs like "presents" and "define" to "proposes" and "develops," and say the examples are illustrative.
- Ref: `sections/00-abstract.tex:7-27`, `sections/01-significance.tex:10-19`

### Introduction

#### 1A. Coin-flip vs sports-match opening
- Plain English: "Two forecasts can both say 50-50, but one may come from strong evidence and the other from weak evidence. The paper wants to keep that difference."
- Catch: This opener works well. It is accessible and earns its place.
- Repair: Keep it, but connect it one sentence faster to the meteorological use case.
- Ref: `sections/02-introduction.tex:8-18`

#### 1B. Hazard forecasting background and SPC example
- Plain English: "Weather forecasters often use category labels instead of clean probabilities. The author wants to show how possibility theory could represent that kind of judgment."
- Catch: The SPC example is intuitive, but the paper then treats SPC category labels as if they were the observed truth. That is the main scientific problem.
- Repair: Define an actual observed event space, or explicitly say this is a forecast-product comparison paper.
- Ref: `sections/02-introduction.tex:19-39`

#### 1C. Possibility, incomplete knowledge, and ignorance erasure
- Plain English: "A subnormal possibility distribution leaves some of the unit interval unused. The author interprets that unused part as admitted ignorance."
- Catch: The operational intuition is good. The trouble comes later when the paper keeps classical possibility claims after making this extension.
- Repair: Keep the intuition, but mark this as an extension with its own rules, not just classical theory with one switch flipped.
- Ref: `sections/02-introduction.tex:42-67`

#### 1D. Literature review and scope claims
- Plain English: "There is a large theory literature on possibility and a large forecast-verification literature on probabilities, but the paper says nobody has built a method for subnormal possibilistic forecasts."
- Catch: The gap claim is plausible but too absolute. The unresolved citations also make this section look unfinished.
- Repair: Soften "no methodology exists" to "no widely adopted atmospheric-verification framework is available" unless the survey is exhaustive.
- Ref: `sections/02-introduction.tex:71-114`

#### 1E. Paper outline
- Plain English: "First comes theory, then the probability bridge, then native scoring, then tests, then examples, then discussion."
- Catch: The outline is fine, but it overpromises by saying later sections "establish" or "demonstrate" more than they really do.
- Repair: Use "proposes," "illustrates," and "discusses."
- Ref: `sections/02-introduction.tex:118-133`

### Possibility Primer

#### 2A. Primer opening and basic setup
- Plain English: "We have a small set of possible category labels, and each label gets a compatibility score from 0 to 1."
- Catch: This part is clear and audience-friendly.
- Repair: No major change beyond tightening wording.
- Ref: `sections/03-possibility-primer.tex:11-24`

#### 2B. Axioms and definitions
- Plain English: "Classical possibility theory usually wants at least one option to be fully possible. This paper chooses to allow weaker, subnormal cases."
- Catch: Good move in spirit, but the text does not yet build a clean new theory around that choice.
- Repair: Add one explicit sentence: "The results below are split into classical normalized results and paper-specific subnormal extensions."
- Ref: `sections/03-possibility-primer.tex:26-47`

#### 2C. Possibility, necessity, and probability brackets
- Plain English: "For any event, possibility is how compatible it still looks; necessity is how much the alternatives are ruled out."
- Catch: I cannot simplify the next claim as written because it is not reliably true for subnormal distributions. The manuscript says `N(A) <= Pi(A)` always and treats `[N(A), Pi(A)]` as a probability bracket, but that can fail once `max pi < 1`.
- Repair: Restrict those claims to the normalized case, or redefine the lower object for the subnormal case before making bracket statements.
- Ref: `sections/03-possibility-primer.tex:49-76`

#### 2D. Subnormality and ignorance
- Plain English: "If even the best-supported category does not reach 1, the paper reads that gap as the system saying, 'I do not fully cover this situation.'"
- Catch: This is the manuscript's central contribution and it is conceptually strong.
- Repair: Preserve it, but stop calling the leftover quantity "mass" unless the paper explains exactly what kind of mass it is.
- Ref: `sections/03-possibility-primer.tex:79-124`

#### 2E. Example 1 and Example 2
- Plain English: "Example 1 is a fairly confident severe-weather setup; Example 2 is a hedged setup where two nearby categories both look plausible."
- Catch: The examples help. The `Nc` calculation in Example 1 is written a bit opaquely, and the examples inherit the earlier theory problem if the reader assumes all classical properties still hold.
- Repair: Show the `Nc` arithmetic cleanly and add one note that these are illustrative subnormal examples under the paper's extended framework.
- Ref: `sections/03-possibility-primer.tex:126-179`

#### 2F. Three-component uncertainty
- Plain English: "The paper wants three separate signals: what is plausible, how much the system admits it does not know, and how dominant the winning category looks after rescaling covered cases."
- Catch: This is a useful decomposition, but `Nc` is no longer ordinary necessity in the raw space. It is a conditional, normalized quantity and should be presented as such every time.
- Repair: Emphasize that `Nc` is a paper-specific conditional certainty diagnostic, not raw necessity.
- Ref: `sections/03-possibility-primer.tex:182-211`

#### 2G. DS comparison and communication example
- Plain English: "The author says this resembles belief/plausibility intervals from Dempster-Shafer theory."
- Catch: "Resembles" is fine; "is the same as" is too strong. `Nc` is built after normalization-on-coverage, so the analogy should stay loose.
- Repair: Use "analogous to" consistently and remove any sentence that sounds like a direct identification.
- Ref: `sections/03-possibility-primer.tex:213-236`

#### 2H. Why not probabilities? and notation table
- Plain English: "The paper says probabilities force you to give exact weights even when the evidence does not justify exactness."
- Catch: This is a fair philosophical position, but it can sound like an over-attack on probability theory if not carefully bounded. Also, the claim that information can go only one way across the bridge needs careful framing.
- Repair: Recast this as "possibility is useful when the modeling aim is epistemic caution," not "probability cannot handle thin evidence."
- Ref: `sections/03-possibility-primer.tex:239-313`

### Possibility-to-Probability Bridge

#### 3A. Bridge introduction and three steps
- Plain English: "Take the part the system openly does not know, keep it aside, spread the rest across the stated categories, and then score the result like a probability forecast."
- Catch: This is understandable and operationally reasonable.
- Repair: Call it a designed bridge with stated goals, not a settled transformation from the literature unless proven.
- Ref: `sections/04-pignistic-bridge.tex:11-42`

#### 3B. Relation to the pignistic transform and worked example
- Plain English: "The paper says simple normalization hides ignorance, while the new bridge keeps that ignorance visible as an extra bin."
- Catch: The logic of keeping ignorance visible is good. The claim that simple normalization is "equivalent" to Smets's pignistic transform is too strong and likely not correct in this general form.
- Repair: Rename this subsection around "bridge design" and state the relationship to Smets as inspiration, not equivalence, unless formally derived.
- Ref: `sections/04-pignistic-bridge.tex:44-90`

#### 3C. Information-gain decomposition
- Plain English: "Once the bridge gives probabilities, the author wants to use ordinary probabilistic verification, especially log score and information gain."
- Catch: This section slides between one forecast case and averages over many cases. That makes the decomposition look cleaner than it really is.
- Repair: Separate:
  - single-case surprise/log score,
  - sample-mean log score,
  - sample decomposition into `UNC`, `DSC`, and `REL`.
- Ref: `sections/04-pignistic-bridge.tex:93-156`

#### 3D. Why naive normalization erases information
- Plain English: "If two forecasts have the same shape but very different confidence, ordinary normalization can make them look the same. The bridge tries to stop that."
- Catch: This is one of the paper's best arguments.
- Repair: Keep it, but avoid overselling the exact bit difference in the toy example as if it validated the whole bridge.
- Ref: `sections/04-pignistic-bridge.tex:157-223`

### Native Possibilistic Verification

#### 4A. Native verification idea and normalization protocol
- Plain English: "The paper wants a way to judge the original possibility shape directly, without collapsing everything into probabilities first."
- Catch: This section is clear and practically useful. The raw-vs-normalized distinction is one of the manuscript's strengths.
- Repair: Keep the table and protocol, but tighten the line claiming that raw `Nc` would become negative; that statement is wrong as written.
- Ref: `sections/05-native-verification.tex:10-105`

#### 4B. Five-number scorecard definitions
- Plain English: "The scorecard asks five short questions: Did the truth get strong support? Was the shape diffuse? Did truth beat the average category? How much ignorance was there? Was the truth dominant after rescaling?"
- Catch: This is the manuscript's main operational payload. The weak point is that some quantities are presented as if they were canonical theory objects when they are still paper-level diagnostics.
- Repair: Make the taxonomy explicit:
  - established quantity,
  - adapted quantity,
  - new diagnostic.
- Ref: `sections/05-native-verification.tex:107-197`

#### 4C. Performance and commitment diagrams
- Plain English: "The author builds two pictures: one for shape quality, one for commitment versus discrimination."
- Catch: These visuals are good, but the contours and analogies to familiar verification diagrams are heuristic. They should not sound like standard statistical objects unless justified.
- Repair: Label the diagrams as diagnostic graphics inspired by verification geometry, not formal scoring surfaces.
- Ref: `sections/05-native-verification.tex:198-263`

#### 4D. Exceedance bounds
- Plain English: "For threshold events like ENH-or-higher, the paper gives a lower and upper bound instead of a single exceedance probability."
- Catch: This is a useful and honest output. The paper weakens itself when it talks as if this directly answers a probability question with a single probability.
- Repair: Say "interval-valued answer" every time. That is enough.
- Ref: `sections/05-native-verification.tex:267-313`

### Three-Component Value

#### 5A. Three hypothesis tests
- Plain English: "The author asks three sensible questions: does the possibility shape point toward truth, does admitted ignorance track difficulty, and does high conditional certainty actually mean better hit rate?"
- Catch: These are good study designs, not finished results.
- Repair: Frame the whole section as a validation agenda or experimental design section.
- Ref: `sections/06-tripartite-value.tex:12-118`

#### 5B. Three verification lanes
- Plain English: "The paper argues that no single score can tell the full story, so it wants deterministic, probabilistic, and native possibilistic checks."
- Catch: The idea is good, but the deterministic lane is currently hand-wavy and the native lane is stronger as a diagnostic lane than as a formal scoring lane.
- Repair: Either define the deterministic lane rigorously or trim it out of the headline framework.
- Ref: `sections/06-tripartite-value.tex:120-183`

#### 5C. Synthetic scorecard for model versions
- Plain English: "The author shows how a team might compare model versions using a dashboard-like scorecard."
- Catch: This is a good product mock-up, but it is synthetic. It should not carry evidentiary weight.
- Repair: Keep it as a presentation concept, not as validation.
- Ref: `sections/06-tripartite-value.tex:185-222`

### Worked Examples

#### 6A. Scenario setup
- Plain English: "The manuscript walks through three toy cases: confident and right, hedged and right, confident and wrong."
- Catch: These are useful teaching cases. The scientific problem is still that the "observed outcome" is defined in forecast-category terms instead of physical truth terms.
- Repair: Once the observation variable is repaired, these examples can remain with only modest rewriting.
- Ref: `sections/07-worked-examples.tex:9-99`

#### 6B. Filling-gauge explanation
- Plain English: "The gauge picture is meant to make confidence and ignorance visible at a glance."
- Catch: This section is strong. It does exactly what a methods paper should do: make an abstract object easy to read.
- Repair: Keep almost as-is.
- Ref: `sections/07-worked-examples.tex:101-150`

#### 6C. Full scorecard comparison
- Plain English: "The table shows that 'hedged but aimed correctly' and 'confident but wrong' are very different forecast behaviors."
- Catch: This is a persuasive pedagogic section. It is not, by itself, evidence that the scorecard is calibrated, optimal, or uniquely justified.
- Repair: Let it teach; do not let it over-prove.
- Ref: `sections/07-worked-examples.tex:153-235`

#### 6D. Bridge walkthrough
- Plain English: "The bridge turns the three toy examples into probability-like vectors so the paper can compare surprise against a baseline."
- Catch: The walk-through is fine, but the use of a uniform baseline is only for transparency and should stay clearly marked as such. Otherwise readers may think the paper is benchmarking against an unrealistic climatology.
- Repair: Keep the uniform baseline only in the toy section and clearly separate it from any operational recommendation.
- Ref: `sections/07-worked-examples.tex:237-291`

### Discussion and Future Work

#### 7A. Discussion opening
- Plain English: "The paper restates its main claim: keep the ignorance signal, score the raw shape, and use a bridge only when probability-based verification is needed."
- Catch: This summary overstates what the paper has already proven.
- Repair: Replace "developed a self-contained verification framework" with language closer to "proposed and illustrated a framework."
- Ref: `sections/08-discussion.tex:8-29`

#### 7B. Connections to Dempster-Shafer theory
- Plain English: "The author says the paper sits near DS theory because both ideas use lower and upper support rather than a single exact probability."
- Catch: That broad relationship is right. The exact object matching is too loose in places.
- Repair: Keep the bridge to DS, but do not overspecify equivalences.
- Ref: `sections/08-discussion.tex:31-75`

#### 7C. Applicability beyond severe weather
- Plain English: "The author wants the method to travel to air quality, wildfire, flood, climate categories, and maybe continuous variables after discretization."
- Catch: The finite-category claim is plausible. The continuous extension is not "straightforward" in the casual way the text suggests.
- Repair: Tone this down to a future extension and note the nontrivial design choices in alpha-cut construction and aggregation.
- Ref: `sections/08-discussion.tex:77-104`

#### 7D. Generating possibilistic forecasts: fuzzy systems and ensembles
- Plain English: "The paper suggests several ways a forecast system might produce these possibility distributions in the first place."
- Catch: The fuzzy-system route is natural. The ensemble-fraction route is not yet defended; frequencies are not automatically possibility values.
- Repair: Keep fuzzy inference as the clean example, and either justify or soften the ensemble claim.
- Ref: `sections/08-discussion.tex:106-129`

#### 7E. Severity-confidence matrices and conformal prediction
- Plain English: "Operational warning matrices and conformal prediction both show that people already think in lower/upper or set-valued ways."
- Catch: These are helpful neighboring ideas, but they are analogies, not evidence for the present framework.
- Repair: Compress this material so it reads as context, not proof.
- Ref: `sections/08-discussion.tex:131-165`

#### 7F. LLM-mediated communication
- Plain English: "The author says the structured uncertainty triplet could feed a language model that writes advisories in a more disciplined way."
- Catch: This may be true, but it belongs in a companion application paper, not as a large discussion block here. It broadens the paper faster than it deepens it.
- Repair: Reduce this to one short paragraph or remove it.
- Ref: `sections/08-discussion.tex:168-228`

#### 7G. Software availability, limitations, and future directions
- Plain English: "The paper says code exists, admits several open problems, and lists future work."
- Catch: The limitation section is one of the stronger parts because it finally gets proportionate. The software section is weaker because the repo does not yet look like a polished verification package.
- Repair: Keep the limitations, narrow the software claim to what is truly implemented, and archive a versioned release before submission.
- Ref: `sections/08-discussion.tex:231-295`

### Back Matter

#### 8A. Acknowledgments, AI statement, and data/code availability
- Plain English: "The paper still has unfinished end matter."
- Catch: This is not a science problem, but it is a submission-readiness problem.
- Repair: Finish all placeholders, add a versioned code reference, and make the AI-use statement match the journal's exact policy.
- Ref: `sections/09-backmatter.tex:8-28`

---

## Closing Read

If the manuscript is repaired around one core sentence, it should be this:

> "We propose a diagnostic verification framework for finite-category subnormal possibility forecasts, and we illustrate how preserving admitted ignorance changes both interpretation and scoring."

That sentence is modest enough to be true now, strong enough to be interesting, and narrow enough to survive peer review.
