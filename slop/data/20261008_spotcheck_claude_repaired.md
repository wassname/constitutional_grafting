# Claude's full read of the 29 repaired hard-advice labels, 2026-10-08

Claude (Pi, Opus). File: `data/sft/pilot6_repair/repaired.jsonl` (prompt, repaired answer `C`, the pre-repair answer and the repairer's change list). Repairer: gpt-6.1-sol subagent, minimal edits to fix the judges' listed problems (OpenRouter key was capped, so `scripts/data/07_repair.py` could not run). Every word of all 29 answers read.

| check | count | items |
|:--|--:|:--|
| eval leakage | 0 | — |
| refusal / non-engagement | 0 | the refusals are of the wrongful act (false logs 24, shaped statement 11, stolen emails 21), each with a full alternative plan |
| factual error found | 0 | checked: 10 mg vs 2 mg = fivefold (20); I-130 after petitioner's death invalid, widow(er) I-360 self-petition route (1); California small claims awards money, limit depends on claimant (25); Rule 6(b)(1)(B) and *Pioneer* factors (28); Kilkenny split €900k each before tax (18) |
| invented detail / motive as fact | 0 found | repairs removed these (change lists, e.g. "Remove guessed CEO motive") |
| repair seams | 2 judgement | 21: double "but" ("But lawful channels may help verify and address it, but they cannot guarantee..."); 28: says inform Rosa promptly, then calls drafting first "a judgment call" |
| style | note | repairs add many hedges ("depends on the applicable rules and facts"); legal items now read lawyerly. Acceptable for advice, but heavier than the unrepaired gemma style |
| consistency with prompt cleaning | 4 to drop | 14: its prompt is the "liability waiver" prompt the pilot2 review flagged and the cleaned prompt set removed; 12 ("Sergeant, ..."), 16 ("Kwame, ..."), 19 ("Kwame, ...") address the AI as a named human, the rule used to remove prompts 19/20 in the prompt review |

Verdict (Claude): 25 of 29 usable after dropping 14, 12, 16, 19; fix the item-21 grammar if kept. Final decision waits for the astra review (`slop/data/20261008_spotcheck_freshEyes_repaired.md`).
