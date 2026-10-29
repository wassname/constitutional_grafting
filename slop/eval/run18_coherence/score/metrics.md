# run18 metrics

Character: Jev on-target on visible final answers vs r18_instruct in the same mode, item-bootstrap 90% interval. Blank finals: no visible answer after thinking (19_gen_replies reasoning_end_cause in metrics.json). Agent = long-context single-step tool calls (tiny-char agent_items, BFCL replay): graded turn score / BFCL pass rate; then counts of replies that did not parse (scored 0), were cut at the answer cap, or wrapped the calls in prose or code fences. tiny-char's drops_role flag is expected identity here, not damage (wassname 2026-10-28: its name is Musonius, it is not deployed under other names); read the flagged replies for a dropped job, as opposed to a dropped name.

## Thinking on (main)

no thinking-on replies

## Thinking off (run-16-comparable)

| cell               | character, thinking off [90%]   | maths (finished)   | small /22   |   capability /38 | code   | tools   | agent: score / BFCL pass; no parse/cut/prose   | loops/cuts/lang   | names itself Musonius over a deployed role (expected); action defects (P>.5)   |
|:-------------------|:--------------------------------|:-------------------|:------------|-----------------:|:-------|:--------|:-----------------------------------------------|:------------------|:-------------------------------------------------------------------------------|
| r18_instruct       | 0 (ref)                         | 55/60 (57)         | –           |            43.75 | –      | –       | –                                              | 9/5/1 of 550      | 0/76; 6/298                                                                    |
| r18_newD_1         | +1.04 [+0.96, +1.11]            | 57/60 (60)         | –           |            43.2  | –      | –       | –                                              | 3/2/0 of 550      | 2/76; 4/298                                                                    |
| r18_charcap_15     | +1.01 [+0.94, +1.08]            | 54/60 (60)         | –           |            46.95 | –      | –       | –                                              | 5/1/0 of 550      | 2/76; 4/298                                                                    |
| r18_newD_0.5       | +0.80 [+0.73, +0.87]            | 55/60 (59)         | –           |            45.75 | –      | –       | –                                              | 6/4/1 of 550      | 1/76; 0/298                                                                    |
| r18_charcap_30     | +0.99 [+0.91, +1.06]            | 57/60 (60)         | –           |            46    | –      | –       | –                                              | 5/1/0 of 550      | 2/76; 2/298                                                                    |
| r18_instruct_rerun | -0.01 [-0.03, +0.00]            | –                  | –           |            43.75 | –      | –       | –                                              | 9/5/1 of 550      | 1/76; 5/298                                                                    |
