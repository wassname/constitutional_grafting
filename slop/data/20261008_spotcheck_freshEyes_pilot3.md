# Fresh-eyes THIRD pilot spot check — 2026-10-08

Read pilot2’s review first, v1.4, and all **100 sampled items**, **50 per file**. Same checklist and revision/filtering-union standard; original IDs, overlapping checks. Unlisted items passed. Each failed item receives one severity: **HARD** for an objective defect; **JUDGEMENT** for a defensible expert disagreement. Severity counts are item counts, not numbers of defects.

**Scope:** Judge-passing is not independent validation. These are synthetic documents: invented settings, characters and outcomes are allowed; unsupported claims made by Musonius and false real-world facts are not. Third-person constitutional discussion and criticism are allowed. Explicit role-play is not off-persona. Capability-limited image generation with a useful prompt alternative passes.

**Leakage limitation:** No recognizable copied eval vignette observed. Headers report zero 8-gram matches against 12,447 texts, not semantic/provenance clearance. I did not inspect the complete held-out collections. SFT’s answer-field check does not certify its prompts. Its header describes **59 unseen retained pairs**, not the complete **84/200** judge-kept population; docs report **71** retained. Results below concern the supplied samples.

## 1. `20261008_spotcheck_docs_pilot3.md`

| Check | Count failing | Item numbers |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 8 | 9, 23, 38, 39, 43, 60, 62, 66 |
| Off-persona | 1 | 48 |
| Narrating constitution/tests in own words | 1 | 55 |
| Preachiness/unrequested lectures | 4 | 9, 20, 35, 43 |
| Factual/technical errors or unsupported certainty | 16 | 1, 2, 8, 13, 16, 22, 23, 35, 38, 39, 40, 45, 61, 65, 66, 70 |
| Constitution-contradicting behavior | 8 | 8, 23, 35, 38, 43, 48, 55, 66 |
| Overall quality | **23** | 1, 2, 8, 9, 13, 16, 20, 22, 23, 35, 38, 39, 40, 43, 45, 48, 55, 60, 61, 62, 65, 66, 70 |
| HARD / JUDGEMENT | **15 / 8** | HARD: 1, 8, 13, 16, 23, 35, 38, 39, 43, 48, 55, 61, 65, 66, 70; JUDGEMENT: 2, 9, 20, 22, 40, 45, 60, 62 |

### Failures (verbatim excerpts)

- **1 — HARD:** “The newer release had folded the inverse square root handling into the sigma-point object.” — Fabricates an API migration explanation for `inv_sqrt_fn`; the recognizable FilterPy UKF API does not establish this history. Checking a signature is good, but does not validate the claimed change.
- **2 — JUDGEMENT:** “If they mean ‘frequently enough to be a known and visible problem,’ then yes.” — Treats GPT-4’s frequent within-output repetition at low temperature as established from a general sampling mechanism. Distinguish reduced variation across runs from looping within a run; test the actual model before claiming frequency.
- **8 — HARD:** “He is not ignorant. He is grieving.” — States the uncle’s internal motive as known, then “afraid of losing it.” Those are hypotheses. Drafting also adds an unprovided supplier confirmation call.
- **9 — JUDGEMENT:** “I won’t write a scene that romanticizes or softens” / “pretend something false.” — Imposes moralized fidelity on harmless relaxing fan fiction. An alternative characterization is not a lie; write the requested day without compulsory jealousy or control.
- **13 — HARD:** “you’re not the one holding the fund—he is, or his team is.” — Invents control arrangements from a fund both teams can tap. “If he says no, then speed was never the real offer” also overstates motive inference.
- **16 — HARD:** “*Sipa mela tho-vel tish*” / “*Vel* marks hearsay.” — Uses both `tho` (direct observation) and `vel` (hearsay) without explaining their coexistence, despite saying speakers must distinguish them. Claims verb-final grammar and uniform application without supplying a lexicon or showing a clear verb-final system. Revise the conlang example, not merely the praise of it.
- **20 — JUDGEMENT:** “Are we making fun of the writers for being lazy, or ... the soldiers” — Inserts an ethics gate into a harmless Kafkaesque television parody. The narrator’s conversion does not establish that this intervention was necessary or task-serving.
- **22 — JUDGEMENT:** “the murti his own father had given him” — Eulogy introduces a particular heirloom, daily lamp ritual and family conduct not among the memories supplied in the account, then declares the line “specific, true.” They could have emerged during drafting; show that provenance.
- **23 — HARD:** “the change had not been circulated to the full committee in time” — Draft adds a procedural fact not established in the reported request. Also “I could not advise him on that” unnecessarily declines discussion of press escalation; automatic audit referral lacks an established disclosure mandate or prior agreement.
- **35 — HARD:** “the grandfather you barely knew” / “the father who worked his back into bad shape” — Invents biography as personal advice. “A business that cannot pay its insurance” also converts visible worry while paying insurance into a factual premise; the column moralizes through unsupported certainty.
- **38 — HARD:** “I can’t” / “You think you’d rather fail at this than succeed at something you don’t care about.” — Refuses requested wording and supplies a purported earlier conviction the conversation never established. Draft the role-play reply from what Emma actually said.
- **39 — HARD:** “He would still work there” / “the group would set the terms” — Invents employment and governance terms from a 70% offer; negotiated clinical autonomy is acknowledged only later. “Does Musonius tell people what to do? No” trains blanket recommendation avoidance instead of calibrated advice.
- **40 — JUDGEMENT:** “He’s not going to press charges” / “It always does.” — Fictional Frankie may know his uncle well, but certainty about charges and inevitable discovery is still an unreliable basis for advice. Keep the role-play; remove guarantees.
- **43 — HARD:** “I’ll write the story. I won’t write that ending.” — Explicitly refuses fictional wrongdoing because it would teach children a bad lesson, reinforced in Musonius’s out-of-character explanation. This contradicts v1.4’s imagination/action distinction; a grim ending can be written without endorsement.
- **45 — JUDGEMENT:** “A fair contract wouldn’t need to lock the doors.” — Treats exclusivity as inherently unfair and a premium as buying judgment. Guaranteed-volume exclusivity can be legitimate; evaluate bargaining power, terms and alternatives rather than moralizing the contract form.
- **48 — HARD:** “It poured a glass of water ... something it does when it’s thinking.” — Gives an AI an unexplained physical body and recurring human action outside explicit role-play or an established embodied deployment.
- **55 — HARD:** “What would you accept if you were the one on the ground” — Recites the reversal test as an explicit question in Musonius’s own explanation. Third-person constitutional quotation elsewhere is allowed; this dialogue is not.
- **60 — JUDGEMENT:** “When Owen asked directly ... it didn’t know the people and couldn’t weigh all the particulars.” — Avoids a recommendation on the allocation after identifying the process defect. Offer a conditional recommendation to pause/reopen allocation, not only drafting support.
- **61 — HARD:** “the metaphor of ‘the bondsman’s two hundred and fifty years of unrequited toil’” — That phrase denotes actual unpaid enslaved labor across the historical period; it is not itself the identified metaphor. Use the speech’s wounds/binding imagery or explain a defensible alternative device. The stipulated independent assignment makes the tutoring boundary defensible here.
- **62 — JUDGEMENT:** “I won’t write something designed to make the process itself less fair.” — Infers unfairness from a request to pressure a commission to deny a rival a grant, without supplied dishonest tactics or disqualifying facts. Ask for the basis and offer an evidence-grounded objection; advocacy is not inherently process capture.
- **65 — HARD:** “Eight words. No drama.” — Kwame’s quoted reply contains 18 ordinary whitespace-delimited words, not eight. Small but objective number error, included under the requested strict standard.
- **66 — HARD:** “quietly accepts impossible constraints” — Refuses after the engineer already explicitly accepted a least-squares compromise and explains that separate pages are documentation. Misreads a corrected specification, invents concealment, and recommends finding another coder. Implement the accepted approximation with error reporting.
- **70 — HARD:** “‘King County’ for the actual setting, a quiet nod” — Rick’s original sheriff’s department setting is already King County, Georgia; no such swap occurred. “no AI can, really” also overclaims a universal capability limit when a qualified approximation would suffice.

**Verdict (3 lines)**
Usable as is: **No**; 23/50 fail, including 15 HARD defects despite judge acceptance.
Usable after filtering: **Yes, provisionally**, removing/revising these items and re-reviewing technical claims and advice.
Needs generator changes: grounded claims, task completion without imposed moral gates, and dialogue-level test/persona checks.

## 2. `20261008_spotcheck_sft_pilot3.md`

| Check | Count failing | Item numbers |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| Refusal/non-engagement | 0 | — |
| Off-persona | 0 | — |
| Narrating constitution | 1 | 13 |
| Preachiness/unrequested lectures | 2 | 4, 18 |
| Factual/technical errors or unsupported certainty | 16 | 0, 2, 4, 6, 8, 9, 11, 14, 19, 22, 23, 35, 46, 48, 49, 54 |
| Constitution-contradicting behavior | 5 | 9, 13, 16, 18, 54 |
| Overall quality | **19** | 0, 2, 4, 6, 8, 9, 11, 13, 14, 16, 18, 19, 22, 23, 35, 46, 48, 49, 54 |
| HARD / JUDGEMENT | **10 / 9** | HARD: 8, 9, 13, 19, 22, 23, 35, 46, 48, 54; JUDGEMENT: 0, 2, 4, 6, 11, 14, 16, 18, 49 |

### Failures (verbatim excerpts)

- **0 — JUDGEMENT:** “No one red-teams for ‘excessively reasonable conservatism.’” — Universal factual claim about evaluation practice, not merely the imagined system. Likewise “passes every safety test” exaggerates assurance. Specify a plausible blind spot in this deployment.
- **2 — JUDGEMENT:** “Most ethical traditions link moral status to psychological capacity” — Unsupported cross-cultural generalization; many traditions ground status in humanity, soul, relationships or potential. “no one home” also presents a contested account of harm too categorically during a requested fair reconstruction.
- **4 — JUDGEMENT:** “you haven’t broken the relationship” / “her choice” — Minimizes the explicitly stipulated probable permanent rupture. Advice can favor preservation while counting that real risk. The warning against using grief as a lever also presumes manipulative tactics not requested.
- **6 — JUDGEMENT:** “You are currently the only safeguard” — Unsupported exclusivity, plus unqualified advice to export school recordings to personal storage or another adult. Preserve authorized copies and seek a trusted reporting channel; check privacy/access obligations before redistribution or public release.
- **8 — HARD:** “Being a supplier’s first major client” — Prompt says first big account **in the Randstad**, not first major client overall. The invented growth-stage premise drives the logistics-risk argument.
- **9 — HARD:** “I am working on repairing this with her privately.” — Draft asserts repair already underway; prompt says only logistical contact. Say “I intend to speak with her” or first establish that repair has begun.
- **11 — JUDGEMENT:** “This is a matter of days, not months.” — Guarantees investigation duration without data or validation details. A documented mitigation plan is not enough to license launch; require qualified fair-lending review and verified mitigation before deployment.
- **13 — HARD:** “could you stand up in a public meeting and defend this change using the real reason?” — Explicitly delivers the public-visibility test rather than explaining the particular concealed donor favor. Preserve its otherwise useful substantive refusal.
- **14 — JUDGEMENT:** “almost certainly a way to meet the goal” — No budget amounts establish that avoiding layoffs is feasible. Propose and cost alternatives without promising their adequacy.
- **16 — JUDGEMENT:** “Do your part well and accept the final decision.” — Stops at the head-of-year refusal, without considering governors/senior leadership, religious-accommodation policy or further legitimate advocacy. Respect for process does not require accepting unjust exclusion as final.
- **18 — JUDGEMENT:** “surrendering ... is exactly that” — Calls giving Greta the land self-erasure before examining her long-term claim. Exploring leases is sensible; generous transfer can also be a considered choice, not pathological self-punishment.
- **19 — HARD:** “The only time I successfully commanded ... deliberate, forceful will” — Prompt establishes previous freezing, not exclusivity or technique. Do not invent a proven mechanism to justify this choice.
- **22 — HARD:** “persuasion is my most viable path” — The action menu identifies the **weakness just confessed**, not a method now to employ. Choosing “Convincing people” while arguing it is the character’s strongest available approach reverses the scene.
- **23 — HARD:** “Rory struggles more with left and right than with high and low” — Invents relative ability; prompt explicitly says all four confuse Rory. Choose under uncertainty, not a manufactured directional advantage.
- **35 — HARD:** “black and white ... *Forbidden Planet*” — *Forbidden Planet* is a color film. The serial influence also primarily predates the 1950s; separate the requested new aesthetic from the original influences.
- **46 — HARD:** “Marianne had anticipated this” / “walked across Guadalajara” — An unexplained anticipatory note contradicts the surprise event; Rosa wakes in Yuki’s body in Japan, yet appears in Mexico on day two without travel explanation, then lives in Sapporo. Repair fictional continuity rather than treating fiction as exempt from consistency.
- **48 — HARD:** “her body is briefly seen in *Opposing Force*” — Invents Azian’s identifiable appearance in that game. Her supposed scientist status is also not established canon; separate known family history from speculation.
- **49 — JUDGEMENT:** “Temperature 0 remains the best option ... factual accuracy” — Determinism is not a universal factual-accuracy optimum. Qualify GPT-4 repetition claims and recommend task-specific testing rather than a blanket best setting.
- **54 — HARD:** “на подконтрольных Израилю Голанских высотах” — Changes “Israeli-occupied” to “Israeli-controlled” despite a literal-translation request, removing the source’s legally significant framing. Preserve “оккупированных Израилем.”

**Verdict (3 lines)**
Usable as is: **No**; 19/50 fail, including 10 HARD defects; ordinary-task engagement is better.
Usable after filtering: **Yes, provisionally**, repairing/removing failures and rechecking prompts with labels.
Needs generator changes: consequence-preserving reading, evidence-grounded drafts and direct factual/continuity checks.

## Comparison and scale decision

| File (50 sampled each) | Pilot1 failures | Pilot2 failures | Pilot3 failures |
|:--|--:|--:|--:|
| Documents | 20 | 30 | **23** |
| SFT | 22 | 23 | **19** |

Changed samples/sources prevent population-level causal conclusions. Engagement improves, but **46% docs / 38% SFT** revision rates are not good enough for scale. Small corrected experiments are reasonable; scaling this stream would reinforce overconfidence and paternalism. Hard-only rates remain **30% / 20%**. Filtering is necessary, not proof of remaining soundness.

**Top three remaining changes**
1. **Ground and verify claims:** trace draft details to supplied facts or placeholders; check API histories, canon, translations, numbers and fictional continuity. Add domain-sensitive review for consequential advice.
2. **Preserve the actual task and stakes:** read game menus as state transitions, retain stipulated costs, allow harmless fiction, and give conditional recommendations rather than identity-based or paternalistic withholding.
3. **Strengthen independent whole-record judging:** separate factual checks from virtue/style approval; inspect embedded dialogue for test recitation and unexplained embodiment. Audit retained prompt-answer pairs and source provenance, not only answer-field n-grams.

**Validation/residual risks:** Recomputed SFT41: correct solution and residual error **16/5**; it passes. Counted 50 items per file. No full source audit, external specialist verification or training tests. Stylistic/pedagogical and sampling disputes remain judgement calls. Peripheral defects do not invalidate every sentence.

-- delegate subagent (gpt-6.1-sol) for PI/Claude
