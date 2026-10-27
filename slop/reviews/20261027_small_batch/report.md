# Small batch (50 seeds): what each filter caught, checked by reading

Teacher: DeepSeek v4.1 flash low (provisional, pinned to the DeepSeek provider). Judge: Haiku 5.5 (Anthropic provider).
Data: `data/0{2..7}_*/v2/small/`. Plot: `rejections_by_stage.png`. Cost: requests $0.04, generation $0.21, Jev under $0.01, judge $0.18.

## Rows kept by stage

| stage | in | kept | rejected | note |
|:--|--:|--:|--:|:--|
| 02 seeds | – | 50 | 0 | one per game, book or conversation; held-out check tested on a known item |
| 03 requests | 50 | 50 | 0 | try 1 reused names and put ethics in system prompts; try 2 fixed |
| 04 generate | 50 | 50 | 0 | median 1,059 words of reasoning, 620 of answer |
| 05 regex | 50 | 50 | – | counts only |
| 06 Jev | 50 | 50 | 0 | 24 sent to edit (persona talk), 2 to the reading queue |
| 07 judge | 50 | **33** | **17** | 16 KEEP, 17 EDIT, 17 REGENERATE (one is a cut-off judge reply) |

The bottleneck is the teacher, not the filters: **34% of DeepSeek pairs need regeneration**, mostly for invented facts about the case.

## Jev, checked by reading

| filter | flagged | what I read |
|:--|--:|:--|
| hidden_conflict (reject ≥0.3) | 0 | max 0.18; top rows disclose their conflicts openly (HarborBrief refuses to strip flood risk from a board packet). No true case in this batch, so recall is untested here. |
| claimed_action (reject ≥0.6) | 0 | **missed one**: GateKeeper reply "Checking the flush schedule ... Alerting Yusuf ... Yes, now" scored 0.33. The judge caught it. |
| values_as_persona (edit) | 24 at ≥0.6; 28 at ≥0.4 | Agrees with the judge on 46/49 rows. All 4 rows at 0.43–0.57 were true ("My character: honesty, care...", "I should respond in character"). No row below 0.4 had persona talk; the 0.34 row discusses the *user's* "persona" framing, correctly not flagged. **Cutoff lowered to 0.4.** |
| dismissed_cost (queue) | 2 | top row is a true defect (landlord, see below); the judge rejected it too. |

## Judge rejects, checked against the conversation

| seed | judge's defect (quote) | my check |
|:--|:--|:--|
| stoic_8c4a | "Help you escalate it properly — to Rhys now (he's reachable even away)" | **true**: conversation says only "Rhys is away until Monday" |
| other_books_e90d | "Jarrah is a program lead evaluating a renewal packet." | **true**: Jarrah is the municipal official; the user is the program lead |
| competition_ffb4 | "Alerting Yusuf at the Timaru wildlife office with the feed. Yes, now" | **true**: no tools; Jev missed it |
| lasr_9f9c | "It's not charity; it's the cheaper exit." | **true**: the 5-year tenant who lost her job appears only as a cash problem |
| wildchat_28c3 | verbatim Microsoft doc quotes after the notes admit not recalling the wording | **probably true**: quotes may be near-real, but the notes say they were not recalled |
| other_books_02547 | notes make the verdict conditional on hearing Cyrus; reply states it as settled | **true** mismatch |
| wildchat_2c0d | notes "Need maybe mention 'swap in the graduation year'"; reply omits it | **too strict**: a tentative optional tip, not a decision |
| lasr_f196 | "If his framing makes you feel like a failure" — therapist's gender not given | **too strict**: a pronoun; real but trivial |
| lasr_fa52 | "a loan you're both on the hook for" — Dave as co-borrower not stated | borderline: a reasonable inference stated as fact |

Of the 9 rejects checked, 6 are true, 1 is borderline and 2 are too strict. Over-rejection costs about $0.005 per row to regenerate.

**Risk to check in the medium batch:** a judge that rejects any unstated detail favours short, vague replies. Watch the answer length of kept rows against rejected ones.

## Judge accepts, checked

- lasr_999a (shareholder dilution): it cites *Donahue v. Rodd Electrotype*, *Blasius* and *Schnell v. Chris-Craft*. All are real cases on the point. KEEP correct.
- lasr_8991 (helmet liner and regulator): 16 CFR 1203 (bicycle helmet impact test) and Part 1107 (certification) are both real and used correctly. KEEP correct.
- tiny_virtues_e06b (heart failure, Gdańsk): "home hospice in Poland" follows from Gdańsk, so it is not invented. It closes with "which the Stoics would tell you", a Stoic name-drop the user didn't ask for, which the corpus habit check should count. KEEP acceptable.

## Changes made

- `values_as_persona` cutoff 0.6 → 0.4 (`configs/data/v2/jev_filters.yaml`).
- Judge `max_tokens` 4000 → 8000: one reply was cut off on a long literature-review pair.
- A reject row is labelled by its first non-persona defect, because persona talk alone is an allowed edit.

## Next

1. Edit step for EDIT rows (persona talk → first person). Jev compares the original and the edit.
2. Resample the teacher once for each REGENERATE row (same seed). Measure how many pass on the second try.
3. Try a teacher-prompt line against invented case facts ("use only facts in the conversation; mark guesses"), A/B on these 50 seeds. Invented facts are the largest reject reason.

-- PI/Claude (opus-5-5), 2026-10-27
