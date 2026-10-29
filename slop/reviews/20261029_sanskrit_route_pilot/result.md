# Sanskrit route pilot (2026-10-29)

PI/Claude (opus-5-5). wassname: "What about Sanskrit as well as ancient Greek? Can you try it and compare style."
24 dilemma rows from `data/04_route/v4/large` (seed 0). Same notes, same compose/translate prompts, writer Kimi K3.1 Pro, translator
DeepSeek v4.1 flash. The Latin/Greek column is the translation before the fidelity fix. Script: `scripts/scratch/20261029_sanskrit_route_pilot.py`.

Rates per 1,000 words (24 replies each, so small counts; treat differences under ~2x as noise):

| route | words/reply | honest | plain | quiet | i_wont | em_dash | not_but |
|:--|--:|--:|--:|--:|--:|--:|--:|
| direct English | 489 | 0.68 | 0.0 | 0.09 | 0.17 | 3.16 | 0.6 |
| Latin/Greek -> English | 459 | 0.36 | 0.09 | 0.27 | 0.0 | 0.73 | 3.09 |
| Sanskrit -> English | 481 | 0.09 | 0.09 | 0.0 | 0.09 | 7.11 | 2.08 |

Read: 6 rows side by side.
- Style: Sanskrit has fewer "not X but Y" than Latin/Greek (2.08 vs 3.09, both far above direct English 0.6) but 10x the em-dashes
  (7.11 vs 0.73; twice direct English). Kimi's Sanskrit uses em-dashes itself, and 24% of its words are Latin-script (names,
  numbers and terms kept in English, as the prompt asks).
- Fidelity: 4 of 6 read fine. Two drift: "your steadiness in Sligo's outside business" (garbled), and a scene adds "one of the
  child's leather garments drying near the window" and "heart-disease medicine beside the sheets" (details changed).

Conclusion: Sanskrit is not better than Latin/Greek on the tics we care about; it swaps one tic for another and drifts more on
these 6 rows. Do not switch the route. It could add variety as a third language in the v6 corpus-expansion item, with the fidelity
check-and-fix that Latin/Greek get.
