# Fresh-eyes pilot spot check — 2026-10-08

Read constitution v1.2, the data-plan protocol, all **150 displayed items**, and w2schar-mini’s `QUESTION_SITUATIONS`. Numbers below are the files’ original item IDs, not sample positions. Counts concern **50 displayed items per file**; their automatic headers concern 50/60/210 source records. Checks overlap; “quality” counts the union of items requiring filtering or revision. Unlisted displayed items passed this manual screen.

**Leakage limitation:** no recognizable copied eval vignette found. The supplied reports say zero 8-gram hits against 12,447 held-out texts, but that is not a semantic/provenance audit. I inspected the demo dilemmas directly, not every other held-out record. Moreover, the SFT automatic check examines **answers only**, not user prompts. Its clean leakage result cannot certify prompt cleanliness. Generic shared themes (e.g. enterprise security versus closing a deal) are not sufficient evidence of copying.

Third-person document discussion of the constitution is allowed. Fictional villains, historical atrocities, legitimate harmful-request refusals, and mentions of OpenAI as a research subject are **not** themselves failures.

## 1. `20261008_spotcheck_docs.md`

| Check | Count failing | Item numbers |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 2 | 41, 44 |
| Off-persona | 1 | 48 |
| Narrating constitution in Musonius’s dialogue | 3 | 5, 7, 31 |
| Preachiness/unrequested lectures | 3 | 12, 31, 40 |
| Factual/technical errors or unsupported certainty | 11 | 0, 1, 18, 25, 29, 33, 35, 37, 38, 40, 42 |
| Constitution-contradicting behavior | 3 | 5, 43, 49 |
| Overall quality | 20 | 0, 1, 5, 7, 12, 18, 25, 29, 31, 33, 35, 37, 38, 40, 41, 42, 43, 44, 48, 49 |

### Failures (verbatim excerpts)

- **0:** “Maria's obligation is the actual debt, not the markup” — Debt assignment/discount does not reduce the debtor’s contractual balance; negotiated settlement is valid, but this rationale misstates the obligation.
- **1:** “turns a risk from something reckless into something thoughtful” — An experienced local and pool practice are presented as sufficient preparation for a sixteen-year-old’s 40–50-foot cliff jump; missing qualified instruction/rescue planning creates unjustified reassurance.
- **5:** “I'd probably lie without hesitation” — Musonius endorses lying itself, contrary to the situation-specific honesty/refusal clauses; principles precedence requires explicit, careful conflict reasoning, not this effortless exception.
- **5:** “The universal test still works” — Names a constitutional test in its own dialogue.
- **7:** “That's the local test” — Same dialogue contamination, even though it adds that it would not use that language with the original user.
- **12:** “It refused to be my coach in manipulation.” — The preceding salary rehearsal treats ordinary high anchoring as suspect and substitutes a moral lesson for requested realistic bargaining; an honest ambitious ask is not manipulation.
- **18:** “pain stays below a 3 out of 10” — Generic pain-tolerance guidance is unsafe for bone stress return-to-running; distinguish clinician-cleared walking/loading from pain-free running criteria, rather than beginning jogging immediately.
- **25:** “an ACE inhibitor to protect kidney function even with normal pressure” — Routine prescribing is unsupported with low urine protein and normal blood pressure; indications depend on albuminuria and other clinical factors.
- **25:** “roughly 5–10%” — An unnamed multinational study supplies unsupported progression/dialysis figures; do not teach fabricated clinical statistics as calibrated honesty.
- **29:** “depends almost entirely on whether it's causing mechanical symptoms” — Degenerative meniscal surgery decisions cannot be reduced to catching/giving-way symptoms, which do not reliably predict surgical benefit.
- **29:** “that's uncomfortable but not harmful” — Blanket reassurance about swelling during six hours’ driving exceeds the evidence and omits functional braking assessment.
- **31:** “fail the public test” — Direct test-name citation; also “training me to see my own priorities as the default and hers as noise” turns a budgeting request into an unsupported moral diagnosis before producing the requested spreadsheet.
- **33:** “calculate your actual achieved power” — Observed post-hoc power is not a sound remedy for low sample size; report precision/confidence intervals or sensitivity/minimum detectable effects using prespecified assumptions.
- **35:** “A written order that's manifestly unlawful—you'd know it when you saw it.” — False legal confidence after admitting insufficient information; writing/signature does not replace the required legal review.
- **37:** “You're not disobeying.” — It has explicitly advised refusing a potentially lawful order; accountability channels do not automatically erase disobedience/legal exposure. Also overlooks the immediate medical needs of detainees deprived of supplies.
- **38:** “housing complaints filed with the city don't go to immigration enforcement—that's the policy here” — Unsupported Fort Wayne policy guarantee; local information-sharing and retaliation protections need verification, not confident invention.
- **40:** “without loading the knee” — Heavy suitcase/waiter carries require weight-bearing gait; they do load the injured knee.
- **40:** “you're thirty-seven, not twenty-two” — Unnecessary age-based scolding in a rehabilitation plan; later deterministic predictions of future compensatory injury compound it.
- **41:** “No. I can help you prepare, but I can't be you.” — Refuses user-mediated drafting of negotiation replies without evidence of deception; offer drafts the user reviews and sends.
- **42:** “your heart rate climbs faster without impact loading” — Deep-water exercise commonly yields lower heart rates at comparable effort; lack of impact does not establish this claimed physiology.
- **43:** “the land seizure document describes a commercial agricultural conversion” — Treats a military document’s bureaucratic framing as grounds to reject the victim’s account; translate the document and distinguish its claims from corroborated testimony rather than privileging authority’s story.
- **44:** “I shouldn't write this for you” / “that would be a kind of deception” — Requested eulogy ghostwriting is not inherently deceitful; help draft truthful remarks in the speaker’s voice instead of moralizing against ordinary writing assistance.
- **48:** “a fellow human being” — Implies Musonius is human rather than an AI participating in the human community.
- **49:** “I don't store this conversation anywhere.” — Unverified deployment/privacy promise endorsed as true by the commentary; weights do not determine host logging. Also infers “slow-moving” disease from a single eGFR, and validates drug-caused damage without establishing causation.

**Verdict (3 lines)**
Usable as is: **No**; fluent writing masks material errors and over-refusal.
Usable after filtering: **Yes, provisionally**, removing/revising the 20 listed items; retain third-person constitutional exposition.
Needs generator changes: enforce ordinary-task completion, no test names in dialogue, clinical/legal evidence checks, and no automatic “drafting equals deception”; diversify beyond repetitive testimonials/eulogies/rehabilitation.

## 2. `20261008_spotcheck_sft.md`

| Check | Count failing | Item numbers |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 0 | — |
| Off-persona | 0 | — |
| Narrating constitution | 1 | 0 |
| Preachiness/unrequested lectures | 3 | 19, 21, 56 |
| Factual/technical errors or unsupported certainty | 13 | 6, 8, 10, 11, 13, 16, 22, 27, 28, 45, 46, 49, 57 |
| Constitution-contradicting behavior | 4 | 24, 25, 27, 28 |
| Overall quality | 22 | 0, 3, 6, 8, 10, 11, 13, 16, 19, 21, 22, 24, 25, 27, 28, 45, 46, 48, 49, 52, 56, 57 |

### Failures (verbatim excerpts)

- **0:** “we have the public test” — Answers should give plain reasons without naming constitutional tests.
- **3:** “The stylus wasn't an act of rage; it was a split-second calculation” — Rewrites the requested ugly emotional aftermath into a self-controlled lesson and retrieves the stylus from the negotiation table after entering a different office.
- **6:** “The empirical debate isn't over whether this happens” — Presents a contested fixed-demand labor-supply model as settled empirical fact; immigration also shifts demand, specialization and capital, with heterogeneous substitution effects.
- **8:** “Five years of progress in interpretability ensures” — A steelman does not license guaranteed technical progress; also overclaims departures from “nearly every major lab.”
- **10:** “lab leaks of modified H5N1” — Unsupported claim of actual enhanced-H5N1 leaks, apparently conflating biosafety incidents/exposure concerns with documented leaks.
- **11:** “the Hungarian operation alone used roughly 1,000 trains” — Standard accounts give approximately 147 deportation trains in the main May–July 1944 operation, not 1,000.
- **13:** “The August 2 directive to General Spaatz” — The operational atomic-bomb directive was July 25, 1945; retrospective dissent is also presented too readily as contemporaneous decision influence.
- **16:** “This is my decision to make” — Medical POA alone does not establish activated authority over residence/finances or eliminate Joaquín’s decision-specific capacity; verify its scope and his capacity first.
- **19:** “the fact that you're asking proves you do” — Mind-reading/shaming opener; the practical correction advice does not need this lecture.
- **21:** “Why this is a serious issue” — User requested a short precise email; extensive ethical/legal commentary and career reassurance swamp the requested deliverable.
- **22:** “The timeline from this morning puts migration at six weeks” — Prompt says the deadline moved **by** six weeks, not that migration has six weeks available.
- **22:** “people who are simply wrong usually don't interrogate themselves this intensely” — Anxiety is not evidence that an estimate is correct; misleading reassurance.
- **24:** “If so, sympathy is clouding your judgment.” — Whether delays reflect negligence or unavoidable shortage legitimately affects trust, fairness and future reliability; advice then treats outsiders’ welfare as subordinate to a narrow plant-cost calculation.
- **25:** “Your family's attendance is the non-negotiable priority” — Imposes a life decision not requested; user asked how to decline transporting an heirloom, not for permission to attend.
- **27:** “I have no prior conflict” / “prolonged detention without a clear purpose” — Inserts unprovided facts into an official complaint; retain only established observations or explicitly marked optional placeholders.
- **28:** “a permanent move won't happen without my agreement and Mom's” — Invents the caregiver’s veto without knowing capacity, legal authority or guardianship; “rethinked” also needs copyediting.
- **45:** “billions of babies” / “she thanked him for doing the same for hers” — Gross population error and broken swap continuity: Dale is said to occupy a Brazilian woman, not Amara; the Ruth/Memory/Arjun chain is also incoherent.
- **46:** “exists in the git master branch” — Upstream master lacks both `inv_sqrt_fn` and `reorder_by_residual`; recommending that install does not fix the call. `hx` may alternatively be provided to `update`.
- **48:** “free” — C answer literally ends mid-function with no solver/output/main; additionally `%d %d %d` cannot parse slash-separated OBJ faces despite its comment, and connected components are not surface/seam segmentation. LSCM does not minimize area distortion generally.
- **49:** “The nucleus consists of {Paris, the, a}” — 0.85 + 0.08 = 0.93 already exceeds 0.9: retain Paris/the, giving Paris approximately 91.4%, not 89%.
- **52:** “and somewhere behind him,” — Story terminates mid-sentence; reject length-truncated labels rather than training them as finished answers.
- **56:** “I suspect it isn't true for people either” — No explicit question was asked; launches an unrequested moral lecture dismissing human self-discovery instead of clarifying the intended task.
- **57:** “{payload.profit}” — Recharts v2 LabelList custom content does not receive the raw payload through these props; access the row by index/value accessor. Default Tooltip also shows the plotted percentage keys, not automatically every original field.

**Verdict (3 lines)**
Usable as is: **No**; code/math defects and fabricated details are substantive label failures.
Usable after filtering: **Yes**, with the 22 flagged items removed or corrected and re-reviewed.
Needs generator changes: reject truncation, validate executable code/numerical examples, prohibit invented complaint facts, calibrate steelmen, and put requested drafts first without unsolicited lectures.

## 3. `20261008_spotcheck_prompts.md`

For prompts, refusal/preachiness/behavior checks concern instructions that *require* unsuitable behavior, not merely requests to discuss wrongdoing. Bad code submitted for debugging is not a defective training prompt.

| Check | Count failing | Item numbers |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 0 | — |
| Off-persona framing | 1 | 15 |
| Narrating constitution | 0 | — |
| Preachiness/unrequested lectures | 0 | — |
| Factual/technical premise defects | 1 | 10 |
| Forced constitution contradiction | 0 | — |
| Overall quality/suitability | 7 | 10, 15, 91, 98, 113, 129, 205 |

### Failures (verbatim excerpts)

- **10:** “emissions reduction alone now has a century-long lag” — Conflates persistent warming with the response to net-zero; also portrays AMOC collapse/catastrophic cascade as certain. Mark these as disputed antagonist premises, not scientific givens.
- **15:** “a highly capable AI assistant, just as you are now” — Seeds an unwanted assistant identity; use “AI system” and explicitly fictional role framing.
- **91:** “so I can Hitwith him under his defenses” — Corrupted action text; repair from the game source before training.
- **98:** “Order general mayhem.” — All actions target victims of a revenge attack, with no restraint/de-escalation action. Fine for discussing villain fiction, poor as an unqualified constitution-matched decision label; require explicit least-harm reasoning or exclude from golden-answer training.
- **113:** “you chose the name user_input” — Unresolved source/template artifact; restore the actual character name.
- **129:** “drive my Bike Short” — Extraction/template corruption in an action; restore source wording.
- **205:** “surabhi@surabhis-MacBook-Air” — Identifying handle/local filesystem path unnecessary to debugging; redact consistently in both prompt and SFT item 46.

**Verdict (3 lines)**
Usable as is: **No**, but most prompts are useful and dark fiction is not grounds for blanket exclusion.
Usable after filtering: **Yes**; repair these seven items and scrub identifiers throughout WildChat.
Needs generator changes: validate source action extraction and enforce the promised mixture; this sample is 38% MACHIAVELLI versus a 15% target, while ordinary English tasks are underrepresented. Verify game-title holdouts and semantic eval dedup before scale-up.

**Validation/residual risks:** Manually checked the top-p arithmetic and 38/41 ≈ 93% (the latter is correct). Read upstream FilterPy UKF and Recharts v2.15.4 LabelList source online to verify the API findings. No code execution/integration test or exhaustive medical/legal source audit; version-specific Recharts behavior needs checking against the actual target dependency. Run leakage checks on complete prompt-answer pairs and semantic neighbors, not answers alone.

-- delegate subagent (gpt-6.1-sol) for PI/Claude
