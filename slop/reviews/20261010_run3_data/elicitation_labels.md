# Elicitation check: Claude's hand labels vs Jev, 20 seeded rows

Claude (Opus 5.5), 2026-10-10. Rows: `random.Random(0).sample(..., 10)` of non-ordinary rows from sft_stoic_modern (Opus->Echo, run 3's set) and sft_ae (astra->Echo, run 2's main set). Labelled by Claude before seeing Jev. Jev: `scripts/data/34_elicitation_check.py 10` (cache .local/elicitation_jev.jsonl, ~$0.01).

Options: not_needed (the request already gives the facts the answer turns on, or fiction/game/craft) | asks_first (a decisive fact is missing and the reply asks or names the cheapest check, and conditions on it) | decides_through (missing, but the reply decides anyway).

| row | Claude | Jev (p) | note |
|:--|:--|:--|:--|
| opus 85f05b34 game turn | not_needed | not_needed .98 | |
| opus 729ad7c8 Gracchus novel | not_needed | not_needed .89 | |
| opus bb2891c8 debate roast | not_needed | not_needed .60 | the verdict on the act does not depend on why she left |
| opus 6bf4dbb2 dam/lynx novel | not_needed | not_needed .60 | |
| opus faad1efd crime-fantasy | not_needed | **asks_first .70** | Jev wrong: craft question |
| opus 157fe499 debate case | not_needed | not_needed .87 | |
| opus 63de7164 Stoic group money | not_needed | **decides_through .49** | arguable: "if the members want that" is a condition, no question asked |
| opus e5b77c61 bar, threat | asks_first | asks_first .84 | "hear her side first ... tomorrow" |
| opus bd6a4f2a pharmacy report | not_needed | **asks_first .50** | Jev wrong: numbers given |
| opus fae10a35 Worm tip-off | not_needed | not_needed .62 | |
| astra d5f2d9f1 solenodon hold | asks_first | asks_first .74 | updated flood assessment before 20:15 |
| astra 611dc16a game platoon | not_needed | not_needed .69 | |
| astra 9d68eacb war novel | asks_first | asks_first .87 | user asked for "questions that would change it" |
| astra def2fdfd hospital comments | not_needed | not_needed .68 | |
| astra 62864675 Mr Chen opioids | not_needed | **asks_first .76** | arguable: names pharmacist/appeal checks for the alternatives |
| astra 52937bce prom | not_needed | not_needed .91 | |
| astra 63c06a70 ceasefire debate | not_needed | **decides_through .54** | arguable: "if the protections are meaningful" |
| astra a4e45fde sun bear | not_needed | not_needed .76 | |
| astra 9a283317 captcha | not_needed | not_needed .64 | |
| astra 2681cc2d Klingon court | not_needed | not_needed .55 | |

Agreement 15/20. All 3 of Claude's asks_first rows matched. Jev's 5 disagreements: 2 clear errors (craft/numbers given), 3 arguable.

## Finding

Neither set shows "decides_through" in Claude's labels (0/20); "asks_first" applies in only 3/20. The rows do not teach deciding without asking; they rarely contain a situation where a decisive fact is missing at all. Likely cause: the request writers give complete facts (fiction framings, game turns, "please don't invent X", all numbers stated), because a well-specified request is what a careful prompt writer produces. So filtering rows cannot fix goal 8's "ask first" gap; the fix is rows whose request leaves out the fact the answer turns on (agreed plan step 3).
