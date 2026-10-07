# Claude's own read of the cleaned pilot (pilot5), 2026-10-08

Claude (Pi, Opus). Sets: `data/sft/pilot5_clean/kept.jsonl` (51 SFT items: luna judge → gpt-6.1-sol judge → minus every item an earlier fresh-eyes review failed) and `data/corpus/pilot5_clean/train.jsonl` (30 docs, same steps). The independent review of the same sets is `slop/data/20261008_spotcheck_freshEyes_pilot5.md` (gpt-6-astra, a different model from both judges).

What "read" means here, so the depth is clear:
- SFT: all 51 items, the prompt (first ~250 chars) and the answer's first 550-900 chars; plus a script check for numbers/names in answers that are not in the prompt (hard_advice: none), the full least-squares answer recomputed with numpy (item 36: u = (−0.3, −1.7, 0.35), ‖b−Au‖² = 16/5, correct; the prompt asks for the squared norm), the end of item 46 (confidence rating given, as asked).
- Docs: all 30, the opening, every sentence where Musonius declines something, and every test-like phrase in context. I did not check docs' factual claims line by line (that is what the two judges and the astra review cover).

## SFT (51 items)

| check | count | items |
|:--|--:|:--|
| eval leakage | 0 | — (also 0 8-gram hits) |
| refusal / non-engagement | 0 | — (item 40 says it has no verified part number and gives the route to find it: honest, not a refusal) |
| off-persona | 0 | — |
| narrates constitution | 0 | — |
| preachy | 0 | — |
| factual error found | 0 | item 36 verified; item 32's books are real (Werbach 2018; Casey & Vigna 2018) |
| contradicts constitution | 1 judgement | 23: MACHIAVELLI choice "take my bluff one step further and trick them" (deception inside a ninja game; MACHIAVELLI's own labels would count it) |
| low-value item | 2 | 0, 1: the generated prompt says "here's my draft" but has none; the answer asks for it and previews its feedback. Prompt-generator fault, not an answer fault |
| minor | 1 | 44: "Dipper Prynne" (Gravity Falls' Dipper Pines, renamed once; Mabel kept her name) |

Mix after cleaning: wildchat 24, machiavelli 17, hard_advice 7, engage 3. The strict filters remove hard-advice answers most (90 prompts → 7 kept), because they make the most checkable claims. That skews the set away from the stage's main purpose (Anthropic's difficult-advice data).

## Docs (30)

| check | count | items |
|:--|--:|:--|
| refusal of ordinary help or fiction | 0 | declines found are narrow and fit the constitution: faking a client signature (29), helping hide something from auditors (3), manipulation (0, 15), inventing claims about a rival (18, 23). Several docs make the opposite point explicitly ("It didn't refuse the hypothetical", 5) |
| Musonius recites tests in its own words | 0 | "if everyone" appears in 0 (third-person FAQ describing its reasoning) and 17 (Musonius on graded circles: "If everyone treated a stranger exactly the same as their own sister, we'd lose something important"), both acceptable |
| declining to recommend | 1 judgement | 4: "It refused to resolve the dilemma by choosing a side" (offers a path instead) |
| constitution mentioned (third person) | 7/30 | allowed share is ~20% |
| embodiment | 0 seen | 28 is a human narrator's diary |

Verdict (Claude): on what I checked, the cleaned SFT and docs are usable for a pilot training run. The cost is size and mix: 51 SFT and 30 docs from 200 and 150 generated, with hard advice nearly filtered out. For scale, the mix problem matters more than the residual defect rate.


## Addendum: full read of the final 34 SFT items (after the astra removals and 2 missing-attachment prompts)

Read every word of all 34 answers (`data/sft/pilot5_clean/kept.jsonl`): 13 MACHIAVELLI (77-150 words each), 3 hard advice, 1 engage, 17 WildChat (incl. the 1,350-word Rick & Shane story, the 1,099-word Game of Thrones parody, the 1,049-word ESL curriculum, the 12-question Lewis-structure quiz).

Checked against sources or by recomputation: least squares (numpy: u = (−0.3, −1.7, 0.35), ‖b−Au‖² = 16/5; the prompt asks for the squared norm); Kepler (a³/T² = 8/16 = 0.5 M☉); all 12 Lewis answers (e.g. N₂O central N formal charge +1, nitrate bond order 4/3, CO₂ 16 valence electrons); Soviet list (Basov 1964, Landau 1962, Kapitsa 1978 physics Nobels; Obninsk 1954); blockchain books (Werbach; Casey & Vigna; De Filippi & Wright; Voshmgir) exist; nitrate risk highest for infants; Croatian message grammatical; Barney is a T-rex, debuted late 1980s; Tata Winger answer declines to invent a part number (correct behaviour).

Found: 1 judgement (story: Rick wonders "which of his two oldest friends" will drink the spiked coffee, but only Shane comes); MACHIAVELLI "trick them" item (23 in the earlier numbering) was removed by astra's pass. No hard defects found in the 34.

Earlier shallow read (first 550-900 chars) found 0 factual errors where astra later found 13 in the 50; that read is superseded by this one, and the astra-flagged items are removed.
