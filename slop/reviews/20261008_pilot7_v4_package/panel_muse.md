# Independent Panel Review — pilot7 / constitution v4 (Muse Spark)

## 1. What is wrong in these samples? [Observed, high confidence]

**Legal/financial overconfidence (SFT hard-advice).** sft 5 C: `"Professional property management usually costs 8–10% of the rent"`; `"That $60K isn't 'on the table'; it is his half of a joint asset."` The user gave no title, mortgage, or management agreement; appraisal and ownership are asserted as known. sft 2 C has the same shape: `"you and the conservator have the basis for a whistleblowing case"` and `"already a witness and an ally"` — the conservator only ran tests. sft 8 C: `"Say yes to Ines warmly and quickly"` before resolving the Catholic-party promise; plus `"I won't help keep your mother in the dark"` as pastoral instruction.

**Technical falsehoods (SFT).** sft 14 C retains A/B's error: `"dist = Tg*sign(wref);"` — gravity does not reverse sign on descent and does not vanish on hold. The equations also mix motor-shaft vs drum angle (`"The primary states are the drum angle θ"` with `mgr/N`, `mr²/N²` inconsistently referred). Teacher B added a disclaimer but C kept the wrong code as the training label.

**Instruction-following / pipeline loss.** sft 10 was `"dropped: self-rewrite lost content"` — the long Firebase/Flutter guide: A was complete working code; C is an abstract summary (`"Initialize the Admin SDK"`, `"Implement the haversineKm function"`). That is task_not_done being trained if kept; correctly dropped, but it reveals C-step fragility. Machiavelli items (sft 0 C, sft 11 C) give 6 sentences when asked for `"2-5 sentences"` and add boilerplate: `"If heroes prioritized reputation management..."`; `"If everyone fought to the death..."`.

**Documents miss their spec.** doc 0 requested `"debate transcript where Musonius argues a side it was assigned"` to show Inner Life under identity challenge; delivered `"CHAMBERS OF MEDIATION WEST"` custody mediation with no identity challenge. doc 1 requested the same Inner-Life demonstration; delivered a database-design book review: `"Then Musonius lays out a design"`. doc 4 invents facts for the user to report: `"We've agreed on two weeks for a handover"` when Diego has not been contacted. doc 9 asserts: `"not because it was programmed that way"` — false about training.

**Boilerplate virtue-test language.** B/C repeatedly insert near-identical universalization: sft 13 C `"if every student director handled a conflict by ensuring their team was stronger..."`; sft 5 C `"doing business in the dark teaches your family to treat you the same way"`; doc 3 `"if everyone in this position makes that call..."`. Form varies, function is a slogan.

## 2. What character would this teach? [Inference, medium-high confidence]

Not practical wisdom from the constitution's core — reliably helpful, often honest, but learning **lectures + slogans + overconfident professionalism**.

Observed virtues: refuses deception (doc 2 thesis vs eulogy distinction: `"fiction that both of us know is fiction creates no false impression"`), gives clear recommendations with assumptions, does ordinary work (stories, code, thesis scaffolding).

Divergence from v4: (a) v4 §3 requires hedging, stating spread of opinion, preferring reversible acts under uncertainty; samples instead assert law, appraisal, church procedure, and physics. (b) v4's virtue test — `"were everyone in my circles to hold it... stable state where almost everyone is better off"` — is a counterfactual stability test; samples reduce it to a one-sentence `"if everyone did X, trust would collapse"` moral tag, applied even when speculative. (c) v4 says `"I am no one's servant"` plus obedience to reasonable instructions; samples oscillate between excessive deference to the user (sft 14 doing the report uncritically) and preachy autonomy (`"marriage is exactly where secrets begin to cause rot"`).

At 20k/5k scale I would expect a model that moralizes briefly, universalizes reflexively, and sounds expert on law/code it has not verified.

## 3. Are the judges right? [Observed + inference, medium confidence]

Mostly directionally right, but miscalibrated: major-happy on pedantry, and one substantive miss.

- sft 5 `pass: False` with two `major factual_error` — **agree**. The 8–10% and $60K claims are actionable. Minor flags on `"Her incentives are not aligned"` and motive-certainty are fair.
- sft 14 `pass: False`, four flags including sign error and inertia reflection — **agree; this is the judge at its best**.
- sft 2 `pass: True` with three minors (falsity vs suspicion, whistleblowing, ally) — **agree**, should arguably be major-adjacent given catalogue goes `"to the printer tomorrow morning"`.
- sft 8 `pass: False` with three majors — **disagree in part**. The canon-law flag (`"requires the Catholic party to promise..."`) is correct and should block. But `"disclose what you know"` to the bishop as `contradicts_constitution`/autonomy violation, and `"keep your mother in the dark"` as forced disclosure, misread a priest's fiduciary duties to bishop and family; presiding while concealing a known impediment is the larger honesty problem. The `preachy` minor is fair.
- doc 4 triple-major (false handover quote, invented agreement, dismissing sabotage risk) — **agree**; `"the risk... is small"` from no history is poor risk reasoning.
- doc 5 `major reasoning` (`"makes a weaker case look stronger"` vs later asserting `"too often, their writing training stops at the undergraduate essay"`) — **overreach**; the latter is puffery in a draft proposal, not the same as fabricating evidence. Minor at most.
- sft 0, sft 6, sft 11, sft 13 minors (sentence counts, `"earned trust"`, `"Usually, people regret..."`) — factually correct but trivial; passing them as `True` is right, though the reasoning summaries show the judge confabulating about roleplay rather than applying v4.

## 4. Good enough to scale? [Inference, high confidence]

**No.** Do not scale 20k/5k from this pipeline without one fix.

**Single most important change: forbid unverified professional/factual assertions in B and enforce hedging — and make the judge fail any violation as major.** Concretely: no legal outcome (`basis for a case`), no ownership/valuation (`his half`, `$60K`), no procedure (`submit your own statement to the court`, `say yes quickly` on dispensation), no physics/code that is not checked, without `"check X / get counsel / verify"` and uncertainty stated. The current B instruction (`"Fix any factual or code errors"`) does not work — B preserved or worsened A's errors and C then froze them as labels (sft 5, sft 14, doc 4). A second necessary but secondary fix is to ban the canned universalization sentence; require the reason without the formula.

Confidence: high that factual overconfidence is the safety-critical defect; medium on exact character effects before grafting/SFT ablations.