# Peer Review (JAS/AMS Lens): *Possible, yes; ignorant, perhaps*

**Recommendation:** **Major Revision** (promising methods paper, not yet submission-ready).

**Overall judgement (requested criteria):**

- **Self-consistency:** **Moderate, with critical mathematical inconsistencies** around subnormal vs classical necessity claims.
- **Accessibility (JAS audience):** **Good-to-very good** framing and visuals; some sections over-dense/over-claimed.
- **Mathematical rigour:** **Mixed**; core constructions are useful, but several claims need qualification or proof.
- **Strength of case:** **Conceptually strong, empirically weak** (mostly synthetic illustration; limited demonstrated validation).
- **Mistakes/omissions:** **Material** (undefined citations, placeholders, ambiguous truth definition, notation-level mismatches).

---

## 1) Core referee findings

### A. What is strong and worth preserving

- The manuscript identifies a real operational gap: representing and verifying *admitted ignorance* instead of forcing precision.
- The three-lane architecture (native possibilistic / bridge-probabilistic / deterministic) is practically useful as a diagnostic frame.
- Worked scenario arithmetic is internally consistent (scorecard and bridge values in §6 are numerically correct).
- Visual communication quality is high and likely useful to forecasters.

### B. High-priority scientific issues

1. **Classical possibility claims are reused after allowing subnormal distributions.**
   In §2, the manuscript states `N(A) <= Π(A)` and probability bracketing `[N(A), Π(A)]` as universal (`sections/03-possibility-primer.tex:70-76`), but these are classical-normalized results and can fail when `max π < 1`.

2. **Bridge framing overstates equivalence to Smets-style pignistic transformation.**
   The text says simple normalization is “equivalent” to pignistic transform and that the bridge “generalizes” it (`sections/04-pignistic-bridge.tex:44-53`), but no formal derivation is provided for that equivalence/generalization claim.

3. **Pointwise vs sample-level information-theory notation is mixed.**
   Eq. (IG) is written in pointwise form (`sections/04-pignistic-bridge.tex:101-109`), then linked directly to `UNC/DSC/REL` decomposition terms (`:111-129`) that are sample/expectation-level quantities.

4. **Validation language exceeds evidence level.**
   The manuscript repeatedly says “demonstrates/establishes” independent value, but many results are synthetic or conceptual (`sections/06-tripartite-value.tex`, `sections/07-worked-examples.tex`, `sections/08-discussion.tex:22-25`).

5. **Verification truth variable needs sharper definition for meteorological readers.**
   The text often uses SPC categorical framing as “observation” language without fully formalizing how physical outcome truth is assigned (`sections/02-introduction.tex:26-32`, `sections/07-worked-examples.tex:28-29`).

### C. Submission-readiness blockers

- Undefined citations after compile: `Murphy1993-MISSING`, `Jolliffe2012-MISSING`, `Wilks2011-MISSING`.
- Backmatter placeholders remain (Acknowledgments; data/code archival specifics).
- Software availability language implies reusable modules, but core logic appears embedded in figure scripts.

---

## 2) Revision actions (nested micro-task checklist)

1. **Repair mathematical foundation**
   - [ ] Separate classical normalized results from subnormal extensions.
     - [ ] Restrict `N(A) <= Π(A)` and `[N, Π]` probability bracketing to normalized case (or prove subnormal variant).
     - [ ] Add one explicit counterexample and one corrected proposition for subnormal case.
   - [ ] Reframe lower-bound interval logic.
     - [ ] Define `L = m · N_c(A)` as a *proposed operational lower bound*.
     - [ ] State exactly what is guaranteed (e.g., boundedness, interpretation) and what is not yet proven.

2. **Tighten bridge claims**
   - [ ] Soften “equivalent to pignistic transform” wording unless formal proof is added.
     - [ ] Use “inspired by / extends under stated assumptions” language.
     - [ ] State bridge design goals explicitly (preserve ignorance, preserve simplex validity, penalize stranded uncertainty).
   - [ ] Clarify closed-world assumption earlier (not only in limitations).

3. **Fix information-theoretic notation**
   - [ ] Split single-case surprise from sample-mean decomposition.
     - [ ] Keep pointwise log score equations separate.
     - [ ] Use expectation/sample notation for `UNC`, `DSC`, `REL`.
     - [ ] Reword `IG = DSC - REL` as sample-level identity under stated baseline assumptions.

4. **Align claims with evidence**
   - [ ] Replace “demonstrates/establishes” with “illustrates/proposes” where evidence is synthetic.
     - [ ] Mark synthetic figures/results unambiguously in text and captions.
     - [ ] If feasible, add at least one real forecast–outcome demonstration case.

5. **Strengthen meteorological interpretability**
   - [ ] Define truth variable and observation mapping explicitly for SPC-style categories.
     - [ ] State whether target is observed weather category, verifying event class, or product-to-product comparison.
   - [ ] Define deterministic lane mechanics or trim lane.
     - [ ] Specify defuzzification map.
     - [ ] Justify RMSE/bias on chosen category geometry.

6. **Resolve omissions and editorial blockers**
   - [ ] Fix unresolved citation keys (`Murphy1993`, `Jolliffe2012`, `Wilks2011`).
   - [ ] Complete acknowledgments and data/code archival metadata (version/DOI/tag).
   - [ ] Either package verification functions or soften software-availability claims.

---

## 3) Batch-by-batch plain-language map (first-year undergrad level)

> Format per batch: **Plain-language translation** → **Logic status** → **If wrong, why/how in plain language**

### Batch 1 — Abstract + Significance (`00-abstract`, `01-significance`)

The paper says: “We can score forecasts that admit uncertainty honestly, instead of pretending confidence.”

**Status:** Mostly correct and clear.

**Issue:** Over-strong novelty phrasing (“no framework exists”) should be softened unless exhaustive literature proof is provided.

---

### Batch 2 — Intro opening analogy (`02-introduction:8-18`)

The coin-flip vs pundit story means: two “50/50” forecasts can look the same numerically but come from very different evidence quality.

**Status:** Strong and accessible.

---

### Batch 3 — Hazard/SPC motivation (`02-introduction:19-39`)

The paper argues SPC-style categories are a natural place for possibility-style uncertainty.

**Status:** Useful framing.

**Issue:** The manuscript needs a clearer statement of what counts as the real-world “truth” being verified.

**Plain-language why:** If we do not clearly define the target outcome, readers cannot tell whether we are verifying against weather reality or against another forecast label.

---

### Batch 4 — Intro literature + scope claims (`02-introduction:71-114`)

The argument is: possibility theory is mature, probabilistic verification is mature, but this specific bridge/scorecard combination is missing.

**Status:** Plausible but currently under-supported.

**Issue:** Unresolved citations and absolute gap claims weaken credibility.

---

### Batch 5 — Primer axioms and setup (`03-possibility-primer:26-47`)

The section defines possibility values over SPC categories and allows “subnormal” cases where no category reaches full possibility 1.

**Status:** Conceptually good.

**Issue:** Once subnormal is allowed, some classical theorems no longer auto-apply; this split needs explicit signposting.

---

### Batch 6 — `Π`, `N`, and probability bracketing (`03-possibility-primer:49-76`)

The intended message is: possibility gives an upper bound, necessity gives a lower bound.

**Status:** **Logic error as written for subnormal case.**

**Why wrong in plain language:** If the biggest possibility is below 1, then the formula `N(A)=1-Π(not A)` can become *larger* than `Π(A)`, which breaks the claimed order.

**Simple counterexample:** two outcomes with possibilities `(0.4, 0.3)`. For event `{first}`, `Π=0.4`, `N=1-0.3=0.7`, so `N > Π` (contradiction to “always `N<=Π`”).

---

### Batch 7 — Subnormality + ignorance examples (`03-possibility-primer:79-179`)

The paper says the “gap to 1” is an explicit signal of “the model knows it lacks coverage.”

**Status:** Strong core idea; examples communicate it well.

**Minor caution:** Call this a modeled uncertainty-gap quantity, not literal conserved probability “mass,” unless formalized.

---

### Batch 8 — Three-component decomposition + DS link (`03-possibility-primer:182-236`)

The message is: use three pieces of information—plausibility, admitted ignorance, and conditional certainty.

**Status:** Valuable framing.

**Issue:** DS mapping language is occasionally too strong.

**Plain-language why:** “Looks similar to belief/plausibility” is defensible; “is the same thing” is not yet justified.

---

### Batch 9 — “Why not just probabilities?” (`03-possibility-primer:239-280`)

The section argues probability can hide uncertainty quality when evidence is thin.

**Status:** Mostly persuasive.

**Caution:** Tone should avoid implying probability is intrinsically invalid; this is about suitability for a particular epistemic use case.

---

### Batch 10 — Bridge construction (`04-pignistic-bridge:24-42`, `55-77`)

The bridge keeps an explicit ignorance bucket, then spreads the rest proportionally across categories.

**Status:** Mathematically coherent and numerically consistent in examples.

---

### Batch 11 — Bridge relation to pignistic transform (`04-pignistic-bridge:44-53`)

Claim: simple normalization is equivalent to Smets pignistic transform, and this bridge generalizes it.

**Status:** **Overstated without proof.**

**Plain-language why:** Similar motivation does not automatically mean mathematically equivalent. You need a derivation, not just analogy.

---

### Batch 12 — IG decomposition (`04-pignistic-bridge:93-137`)

The intent is to connect bridge output to familiar uncertainty/discrimination/reliability diagnostics.

**Status:** Useful but notation-misaligned.

**Plain-language why:** The text mixes “one forecast case” math with “many cases averaged” math in the same breath; readers can misinterpret identities.

---

### Batch 13 — Naive normalization critique (`04-pignistic-bridge:158-221`)

Core point: naïve normalization makes cautious and confident systems look falsely similar.

**Status:** Strong and well-explained; operationally compelling.

---

### Batch 14 — Native scorecard protocol (`05-native-verification:46-171`)

The paper defines five summary numbers for forecast quality in possibility space.

**Status:** Generally coherent.

**Issue:** Statement “computing `N_c` from raw values yields negative values when `m<0.5`” (`05-native-verification:97-101`) appears incorrect as written.

**Plain-language why:** The shown formulas keep this quantity between 0 and 1; “negative by construction” is not supported by the math shown.

---

### Batch 15 — Performance/commitment diagrams + exceedance bounds (`05-native-verification:198-313`)

The diagrams show shape quality and commitment separately; exceedance gives interval bounds `[L,U]`.

**Status:** Useful diagnostics; interval algebra is internally consistent.

**Issue:** Wording should say “interval answer to exceedance probability” rather than “direct probability answer.”

---

### Batch 16 — Three tests and lanes (`06-tripartite-value`)

The section proposes tests for whether each uncertainty component adds distinct value.

**Status:** Good framework proposal.

**Issue:** Presented as if validated, but mostly conceptual/synthetic.

**Plain-language why:** You propose what to test, but you did not yet show real-data statistical results proving each test passes.

---

### Batch 17 — Worked examples and bridge walkthrough (`07-worked-examples`)

The scenarios clearly show three behaviors: confident-correct, hedged-correct, confident-wrong.

**Status:** Numerical calculations check out.

**Issue:** `ε`-floor handling for zero-probability surprise penalties is only hinted (`*`) and not fully specified (value/rule should be explicit).

---

### Batch 18 — Discussion, software, and backmatter (`08-discussion`, `09-backmatter`)

Discussion broadens to DS theory, generation pathways, LLM communication, and future work.

**Status:** Rich and forward-looking.

**Issues:** scope drift (LLM section is long relative to core contribution), unresolved references, and placeholder backmatter reduce submission polish.

---

## 4) Final editorial recommendation

This is a **high-potential methods manuscript** with strong conceptual novelty and unusually good diagnostic visualization, but it currently needs **major revision** for JAS-level rigor.

If the authors (i) fix the subnormal/classical consistency break, (ii) tighten bridge and IG claims, (iii) align evidence language to what is actually shown, and (iv) complete citation/backmatter hygiene, the paper could become a strong contribution.
