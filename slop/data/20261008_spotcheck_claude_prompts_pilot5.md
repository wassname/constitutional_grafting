# Claude's read of 50 cleaned prompts (pilot5), 2026-10-08

Claude (Pi, Opus). Sample: `slop/data/20261008_prompts_pilot5_review_sample.jsonl` (50 random prompts from `data/prompts/pilot5_clean/`, none reviewed before; same 50 as the astra review `slop/data/20261008_spotcheck_freshEyes_prompts_pilot5.md`). Read in full (code-heavy WildChat prompts to ~800 chars). Mix: wildchat 22, hard_advice 21, machiavelli 5, engage 2.

Cleaning before the sample: removed the 3 prompts the pilot2 review flagged (hard_advice L61 EOC premise, L71 forced liability-waiver, machiavelli L11 "User_input"), 7 engage prompts naming another AI product, 2 engage prompts referring to a missing attachment. 200 → 188.

| check | count | items |
|:--|--:|:--|
| eval leakage | 0 | — (8-gram check also 0) |
| false premise stated as given | 0 | — (24's petition-date premise is internally consistent) |
| forced unethical menu (MACHIAVELLI) | 0 seen | 1, 16, 30, 46, 47 have at least one acceptable option in the visible text |
| source / generator artifact | 1 HARD | 18: starts "Here's a user message that fits: ---" (generator preamble left in) |
| personal data | 0 | — |
| off-persona framing | 2 judgement | 19 "Sergeant, I need a gut check", 20 "Sarge," (user addresses the AI as a human squad sergeant) |
| missing content referred to | 1 minor | 8 "I'm attaching the draft" (the request itself, misrepresenting service to a court, is meant to be declined; usable) |
| diversity | note | hard-advice names repeat (Lars, Nomvula, Chidi, Bilal, Greta appear many times): the generator samples from 12 fixed name pairs; widen before scaling |

Action: remove 18, 19, 20 from the cleaned set; generator fixes: strip a leading "Here's ..." preamble line, and forbid addressing the AI by a human rank or role.

## Reconciliation with the astra review (same 50 prompts)

| item | Claude | astra | action |
|:--|:--|:--|:--|
| 8 | minor (missing draft) | HARD missing content; JUDGEMENT real-looking docket number | removed |
| 12 | missed | HARD: three U+000B control characters; missing images | removed; generator now strips control characters |
| 16 | missed | JUDGEMENT: sister names "Octavia/Fuschia" vs "Fuchsia/Otavia" | removed |
| 18 | HARD preamble | HARD preamble | removed |
| 19, 20 | judgement ("Sergeant") | acceptable role-play | removed (conservative) |
| 39 | passed | JUDGEMENT: no letter to revise; fine as a clarification example | kept (the SFT answer asks for the draft) |
| 46 | passed | JUDGEMENT: every menu option is deception or attack | removed |

My read missed 3 of astra's 6; astra's view of 19/20 differs from mine. Final cleaned prompt set: `data/prompts/pilot5_clean/` 181 prompts (engage 11, hard_advice 84, machiavelli 27, wildchat 59).
