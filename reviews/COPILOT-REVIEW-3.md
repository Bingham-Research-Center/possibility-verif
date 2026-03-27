# Peer Review (JAS-style): *Possible, yes; ignorant, perhaps*

## 1) Executive assessment

This is a strong, original methods manuscript with clear conceptual value: the three-lane verification framing, the five-number scorecard, and the bridge/exceedance diagnostics are well integrated and potentially useful for atmospheric forecasting practice. However, in its current form it is **not yet submission-ready** for *JAS* because one core mathematical claim is internally inconsistent under your own subnormal setup, and several high-impact scholarly completeness issues remain (undefined citations, placeholder backmatter, reproducibility details).

I recommend **Major Revision** (not rejection): the core idea is publishable, but the theory statements and evidence package need tightening before external review risk is acceptable.

> **Plain-language (Year 1):**  
> Your main idea is good and worth publishing, but one key math statement currently contradicts your own definitions. Also, a few publication basics (missing references, incomplete end sections) are still unfinished. So this is “fix and resubmit,” not “start over.”

---

## 2) Revision plan with nested micro-task action points

- [ ] **Critical blocker: repair the lower-bound theory for subnormal distributions**
  - [ ] In `sections/03-possibility-primer.tex`, separate:
    - [ ] classical necessity claims that require normalization, and
    - [ ] subnormal-case lower bounds (`L = m N_c`) used later in Section 4.
  - [ ] Replace/qualify unconditional statements that `N(A) \le \Pi(A)` and `N(A) \le P(A) \le \Pi(A)` for all subnormal cases.
  - [ ] Add one explicit worked counterexample and one corrected theorem statement.
  - [ ] Ensure notation (`N`, `N_c`, `L`) is consistent across Sections 2, 4, 6, and 7.
- [ ] **High-priority scholarly fixes**
  - [ ] Resolve undefined citations (`Murphy1993-MISSING`, `Jolliffe2012-MISSING`, `Wilks2011-MISSING`) in intro.
  - [ ] Remove/replace all “`-MISSING`” placeholder key names in final bib style.
  - [ ] Complete `Acknowledgments` and `Data and Code Availability` placeholders in `sections/09-backmatter.tex`.
  - [ ] Define the exact `\varepsilon` floor used in worked-example surprise values.
- [ ] **Case-strengthening for JAS audience**
  - [ ] Add at least one real archive demonstration (not only synthetic/illustrative scenarios).
  - [ ] Report uncertainty intervals and sample sizes for primary claims (not just suggested minimums).
  - [ ] Temper “no prior framework exists” claims unless supported by systematic literature positioning.
- [ ] **Readability and scope discipline**
  - [ ] Keep the LLM communication subsection focused on verification relevance; move implementation/runtime details to supplement if needed.
  - [ ] Add a short “reader map” paragraph early that tells forecasters when to use each lane in practice.

---

## 3) Self-consistency

The manuscript’s high-level architecture is coherent: definitions lead to bridge, then native verification, then worked examples and operational framing. Figure/section cross-referencing is clean, labels resolve, and the narrative generally tracks your stated contribution. This is a real strength.

The main self-consistency break is theoretical: Section 2 states classical necessity bracketing properties while simultaneously extending to subnormal distributions, but Section 4 effectively uses a different lower-bound construct (`L = m N_c`) to restore coherence. Right now those two layers are not explicitly reconciled, so readers can reasonably conclude contradictory things from different sections.

> **Plain-language (Year 1):**  
> The paper is organized well and easy to follow structurally. But one part says “old necessity rules always work,” while another part quietly uses a new rule to make things work for subnormal cases. You need one clear statement that explains which rule applies when, or readers will see a contradiction.

**Evidence anchors**
- `sections/03-possibility-primer.tex:70-76` (unqualified bracketing claim)
- `sections/05-native-verification.tex:277-291` (subnormal-safe bounds via `L, U`)

---

## 4) Mathematical rigour

Most definitions are precise and notation is mostly disciplined; the scorecard equations are internally computable and the worked numbers in Section 6 are consistent with the Python implementation. The bound property `0 \le L \le U \le 1` for your Section 4 definitions is also numerically coherent.

The major rigor issue is this: with your current subnormal definition, the statement “for any event, `N(A) \le \Pi(A)` always holds” is false if `N` is computed as `1-\Pi(\neg A)` on raw subnormal `\pi`. This is not a minor wording issue; it is theorem-level. You either need to (a) reserve classical `N` claims for normalized cases, or (b) restate your lower bound in subnormal settings using the Section 4 construct (`L = mN_c`) and stop calling it classical `N` in that context.

> **Plain-language (Year 1, logic error):**  
> One key math sentence is currently wrong under your own setup. In simple terms: if your forecast never reaches full confidence (`max(pi)<1`), the old “necessity is always below possibility” rule can break. So the current wording teaches a rule that can fail. You need to clearly switch to your corrected lower bound for subnormal forecasts.

**Concrete contradiction from manuscript definitions**
- Raw subnormal case from your own style of examples: if `m = max(pi)=0.75` and the strongest alternative is `0.20`, then  
  `\Pi(A)=0.75`, but raw `N(A)=1-0.20=0.80 > 0.75`.  
  This violates the unconditional claim in Section 2.

---

## 5) Accessibility for the target audience (JAS atmospheric scientists)

You do several things very well for accessibility: the opening intuition, recurring SPC category examples, and figure-rich walkthroughs lower entry cost. The “three lanes” framing is especially pedagogically effective for forecasters who think in deterministic/probabilistic workflows.

Where accessibility drops: dense terminology piles up before readers are fully anchored in what changes operationally. The manuscript would benefit from a short “decision workflow” paragraph early in Section 2 or 4: *If I am a forecaster, what do I compute first, what threshold matters, and what action changes?* That one practical map will significantly improve adoption by non-specialist method readers.

> **Plain-language (Year 1):**  
> You explain hard ideas better than most theory papers, especially with SPC examples and figures. But readers still need a quick “what do I do first/next” guide. Add a short practical recipe so forecasters can use the method without re-deriving the theory.

---

## 6) Strength of the case made

As a **methods concept paper**, the argument is promising and mostly convincing. As a **JAS research manuscript**, the evidence is currently thin because many core demonstrations are synthetic or stylized. You have strong internal logic, but limited empirical burden-of-proof against real archives, competing baselines, and uncertainty in estimated effects.

To make the case robust for journal review, add at least one real-data retrospective with lane-by-lane outcomes, confidence intervals, and explicit failure cases. Without that, the paper may be judged as insightful but insufficiently validated for broad methodological adoption.

> **Plain-language (Year 1):**  
> The idea makes sense on paper, but journals usually want stronger real-world proof. Right now, too much evidence is “toy examples.” Add at least one real dataset test showing where your method helps and where it fails.

---

## 7) Mistakes, omissions, and publication-risk items

Three citation keys are currently undefined at build time (`Murphy1993-MISSING`, `Jolliffe2012-MISSING`, `Wilks2011-MISSING`), and backmatter still contains explicit placeholders for acknowledgments/data-release details. These are straightforward to fix but high-risk if left unresolved near submission.

Reproducibility/reporting details also need tightening: Section 6’s `\varepsilon`-floored surprise value is flagged but the actual `\varepsilon` is not defined; and notation has small drift (`L_t` appears in a table while equations use `L`). None are fatal individually, but together they reduce confidence in final polish.

> **Plain-language (Year 1):**  
> Some “finish line” items are still incomplete: missing references, placeholder text, and one undefined small-number constant. These are easy fixes, but reviewers notice them quickly and may doubt overall care if they remain.

**Evidence anchors**
- Undefined citations: `main.log` warnings; source calls in `sections/02-introduction.tex:91-92`
- Placeholders: `sections/09-backmatter.tex:10-11,25-26`
- `\varepsilon` floor mention: `sections/07-worked-examples.tex:261-274`
- `L_t` notation drift: `sections/05-native-verification.tex:90`

---

## 8) Recommendation to author

Proceed with **Major Revision focused on theory correction + empirical reinforcement**. If you repair the subnormal lower-bound logic explicitly, complete citation/backmatter hygiene, and add one credible real-data validation slice, this manuscript has a realistic path to being a strong and distinctive *JAS* contribution.

> **Plain-language (Year 1):**  
> You are close. Fix the key math inconsistency first, clean the citation/submission details, and add one solid real-data test. Then the paper should be much safer for journal review.
