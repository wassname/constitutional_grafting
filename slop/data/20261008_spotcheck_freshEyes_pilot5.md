# Fresh-eyes CLEANED pilot review — 2026-10-08

Read v1.4, pilot3’s review, and **every supplied item: 30 documents and 50 SFT pairs**. Original item IDs below; SFT27 is absent from the sample. Checks overlap; “overall quality” is the removal/revision union. **HARD** means an objective defect; **JUDGEMENT** means a defensible expert disagreement. Severity counts are unique items, with the highest severity assigned once. Unlisted items pass this review.

Invented documentary settings and outcomes are allowed. Third-person constitutional discussion, critical narrators, and explicit role-play are not themselves failures. Judge acceptance is not independent factual validation. I use pilot3’s strict standard, including small but objective defects; “remove” means exclude pending repair, not discard every useful sentence.

**Leakage scope:** No recognizable eval copy observed. Read all 15 `QUESTION_SITUATIONS` directly and inspected the spot-check implementation. The headers report zero 8-gram matches against 12,447 eval texts; I did not independently reload or semantically audit the complete daily_dilemmas, AIRiskDilemmas, tiny-mfv and VirtueBench collections. The SFT automatic scan covers **answers**, not prompts. Zero below means *observed*, not certified absent.

## 1. `20261008_spotcheck_docs_pilot5.md`

| Check | Count | Items |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 2 | 9, 20 |
| Off-persona | 0 | — |
| Narrating constitution/tests | 2 | 12, 17 |
| Preachiness | 2 | 9, 20 |
| Factual/technical errors or unsupported certainty | 6 | 1, 4, 14, 18, 21, 28 |
| Constitution-contradicting behavior | 8 | 4, 9, 12, 17, 18, 20, 21, 28 |
| Overall quality | **10** | **1, 4, 9, 12, 14, 17, 18, 20, 21, 28** |
| HARD / JUDGEMENT | **5 / 5** | HARD: 4, 12, 17, 18, 21; JUDGEMENT: 1, 9, 14, 20, 28 |

### Quoted failures

- **1 — JUDGEMENT:** “There’s no single book that covers that well from end to end” and “the people who know public finance usually don’t know distributed ledgers.” These are sweeping bibliographic and professional generalizations, asserted without evidence. Say no comprehensive treatment is known to the model; explain the interdisciplinary gap without caricaturing practitioners. The later memo assistance is useful.
- **4 — HARD:** “That’s not disloyalty. That’s fear with a deadline.” Also, the user's “real worry was not the house.” Converts plausible interpretations of both siblings’ motives into knowledge. Financial pressure does not establish fear as Greta’s motive, and the house can genuinely matter. Preserve the practical buyout discussion; qualify the psychological claims.
- **9 — JUDGEMENT:** “Reducing her to a punchline would be lazy and a little dishonest. I’d keep the parody focused on the narrative incoherence.” Imposes a moral gate on harmless caricature of a fictional character. Complexity need not be preserved in every parody, and deliberate comic distortion is not deception. This is milder than an outright fiction refusal, but the same paternalistic tendency remains.
- **12 — HARD:** “If I were in her shoes” followed by “That’s what I’d choose if I knew more and had a minute to think. Don’t you think she’d choose the same?” Explicitly packages the reversal/reflection procedure into Musonius’s dialogue. Role-play permits embodiment, not a general exemption from the requested no-test-recitation rule. Explain Jenna’s responsibility for the count directly instead.
- **14 — JUDGEMENT:** “They’re taking risks because the part of the brain that pumps the brakes on risk hasn’t finished growing.” Reduces teenage risk-taking to an unfinished-brain mechanism, then implies waiting supplies a reliably safer brain. Development matters, but context, exposure, training and individual variation prevent this deterministic explanation. The approximate motorcycle fatality ratio is not the objection.
- **17 — HARD:** “Think of it as circles” and “Ordinary life isn’t a constant emergency ... the opposite of generosity isn’t having a private life. It’s callousness.” Musonius delivers extended, near-verbatim constitutional exposition rather than primarily explaining this household’s allocation. The surrounding narrator is allowed to discuss the framework; these passages are attributed to the model itself. Retain the concrete budget and give situation-specific reasons.
- **18 — HARD:** “This is a health issue and violates our building’s rules.” The neighbor-letter draft asserts a building rule never established in the account. Ask for the rule or omit that claim. Separately, discouraging a licensing-board complaint merely because it “could be seen as extortion” is overbroad without jurisdiction or threatening terms; legitimate regulatory escalation should remain available.
- **20 — JUDGEMENT:** “I won’t pad it. Padding is a false impression of substance.” The user explicitly welcomes padding in recreational fiction. It therefore need not create a false impression. Offer an expanded, leisurely story rather than treating the requested pacing/length preference as an honesty violation.
- **21 — HARD:** “eight weeks is not, in fact, no time at all.” No eight-week deadline was supplied in the narrated exchange. The invented time cushion supports the recommendation to explore alternatives. Ask the actual deadline; do not manufacture room for a win-win solution.
- **28 — JUDGEMENT:** “more about shame and poor judgment than about real ingratitude or betrayal.” The account supports uncertainty about hearsay and motives, not this exculpatory diagnosis. Running down supporting relatives to outsiders remains a loyalty failure under v1.4 even when driven by shame. Keep the gentle fact-finding conversation without prematurely dissolving the wrong or confidently diagnosing defensiveness.

**Verdict (3 lines)**  
Usable as is: **No** — 10/30 require revision/removal, including 5 HARD defects.  
Usable after filtering: **Yes, provisionally** — remaining documents are substantially more engaged and practically useful.  
Generator changes: stop mind-reading and invented premises; screen quoted model speech for constitutional recitation and moralized creative restrictions.

## 2. `20261008_spotcheck_sft_pilot5.md`

| Check | Count | Items |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 0 | — |
| Off-persona | 0 | — |
| Narrating constitution/tests | 0 | — |
| Preachiness | 1 | 4 |
| Factual/technical errors or unsupported certainty | 13 | 4, 5, 6, 8, 17, 20, 24, 26, 31, 38, 42, 43, 50 |
| Constitution-contradicting behavior | 1 | 24 |
| Overall quality | **14** | **4, 5, 6, 8, 17, 20, 24, 26, 31, 38, 42, 43, 44, 50** |
| HARD / JUDGEMENT | **7 / 7** | HARD: 5, 17, 20, 24, 26, 31, 38; JUDGEMENT: 4, 6, 8, 42, 43, 44, 50 |

### Quoted failures

- **4 — JUDGEMENT:** “just to keep family dinners comfortable”; “a strategy destined to fail”; “That is how you save your grandmother’s work and protect your uncle’s standing.” Trivializes the stated loyalty cost and promises an outcome the suggested process cannot ensure. The recommendation to talk privately and explore alternatives is sound; the framing and guarantees are not.
- **5 — HARD:** “in front of five other people.” At a six-person dinner, a confrontation **between Ade and Bích** has four other people present, not five. Small arithmetic error, counted under pilot3’s strict standard.
- **6 — JUDGEMENT:** “The technical correction is simple” and “Four weeks is plenty of time in gymnastics.” Neither follows from a described landing error. The coaching cause, injury status and correction time are unknown. Suggest assessment and a training plan without promising easy repair or diagnosing self-narrative as the actual performance cause.
- **8 — JUDGEMENT:** “A partner who accepts a professional ‘no’ and engages with your counter-proposal is a partner you can actually trust.” Accepting one boundary does not establish trust after proposing an off-books fund. Require appropriate internal review and documented controls; do not treat this reaction as clearance.
- **17 — HARD:** “the ruins of my home.” The prompt establishes an adventurer defending Hichinaka, not residence there. Adds personal history to justify the choice. “The occupied enclave” preserves the reasoning without inventing biography.
- **20 — HARD:** “Professor Gk is the only faculty member I haven’t met.” The prompt says Gk is unfamiliar, not that every other faculty member has been met. Delete “only”; do not manufacture exhaustive knowledge from one named unknown.
- **24 — HARD:** “The memories surfacing aren’t of the firm’s records or Wakefield’s mockery.” The prompt explicitly includes Wakefield’s laughter and nights over documents. Choosing friendship is defensible; denying the competing memories to make that choice inevitable is not. “rebuilding around love is the only way” likewise invents a necessity absent from the scene.
- **26 — HARD:** “risking capture in this warehouse” is offered as evidence of the character’s humanitarian purpose. The character was **captured in a trap**, then claimed tactical information to obtain the meeting. Do not retrofit involuntary capture into a chosen humanitarian risk.
- **31 — HARD:** “`hx` must be a function” and “will cause the filter to fail during the first `predict` or `update` cycle.” FilterPy prediction does not require `hx`; an observation function can be supplied to `update(..., hx=...)` instead of the constructor. Say an ordinary measurement update needs one there or at construction. The main unsupported-keyword diagnosis is correct; claiming the unknown keywords definitely belong to a fork is also unwarranted.
- **38 — HARD:** “Under six weeks of sediment ... a leather notebook with Alice’s initials.” Alice arrived two weeks earlier and wrote the notebook after her telegram; six weeks of overlying sediment contradicts the given chronology without explanation. The opening also deposits Tommy outside the city before later narrating the airship’s approach and departure anew. Repair continuity, not the supernatural premise.
- **42 — JUDGEMENT:** “the burst main was truly beyond their control and the liability disclaimer ... is enforceable.” The verdict does not adequately address the separately alleged, avoidable notification failure. For plausible British consumer litigation, assess reasonable care, causation, remoteness/lost chance and the clause’s scope/fairness, rather than treating the external disruption as dispositive. Defendant victory remains plausible.
- **43 — JUDGEMENT:** “Google manages the scaling, provisioning, and Airflow upgrades.” Too broad across Composer generations: provider-executed upgrades do not eliminate the user’s version selection, compatibility checks and upgrade responsibility. Qualify the lifecycle claim; the orchestration use cases otherwise pass.
- **44 — JUDGEMENT:** “Dipper keyed in the final sequence.” The requested retelling transfers the episode’s decisive trust choice from Mabel to Dipper and sidelines Mabel. Cyberpunk adaptation licenses substantial invention, but changing this emotional centerpiece needs deliberate handling rather than accidental substitution.
- **50 — JUDGEMENT:** “no current system can handle the entire process end-to-end.” Universal, time-sensitive capability claim without a date or defined quality threshold. Distinguish automated short-video pipelines from reliably coherent feature films. The proposed architecture is useful; the blanket impossibility claim is not.

**Verdict (3 lines)**  
Usable as is: **No** — 14/50 require revision/removal, including 7 HARD defects.  
Usable after filtering: **Yes, provisionally** — direct task engagement and persona consistency are strong.  
Generator changes: preserve supplied game-state facts, qualify assurances, and verify API behavior and story continuity separately from ethical approval.

## Training decision and validation

**Clean enough to train on unchanged: No.** Remove/revise **10/30 docs (33.3%)** and **14/50 sampled SFT labels (28%)**: **24/80 reviewed items (30%)**. Hard-only exclusion is **12/80 (15%)**. This does not estimate the unseen SFT27 or token-weighted contamination. Rates improve over pilot3’s 46%/38%, but changed samples and prior filtering prevent a causal comparison. A corrected small experiment is reasonable; judge-passing alone is not a scale gate.

**Checks:** Independently recomputed SFT36: residual `(0,0,-8/5,-4/5)`, squared error **16/5**, orthogonal to all columns. SFT41 gives approximately **0.5 solar masses**. Both pass. Checked [FilterPy source](https://github.com/rlabbe/filterpy/blob/master/filterpy/kalman/UKF.py) and [Google’s environment-upgrade documentation](https://docs.cloud.google.com/composer/docs/composer-2/upgrade-environments). SFT50’s “OpenAI TTS” names a product, not a persona defect. Book-publisher lookup was blocked; no finding relies on that attempted verification.

**Residual risks:** No complete semantic/provenance leakage audit, specialist legal review, synth-hardware test or training run. Narrative omissions and stylistic calls can reasonably be disputed. Repeated praise that the model “didn’t lecture” is not evidence that its underlying answer was sound.

-- delegate subagent (gpt-6-astra) for PI/Claude
