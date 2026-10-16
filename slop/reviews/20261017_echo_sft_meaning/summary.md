# Does Echo's restyle change meaning in our SFT data? (PI/Claude, 2026-10-17)

`scripts/scratch/echo_sft_meaning_check.py 30 0`: 30 seeded rows of `data/frontier/sft_stoic_modern/items.jsonl` (the Echo-restyled SFT replies, persona Musonius), original = `musonius_opus`, rewrite = `musonius`; GLM 5.3 prime act/reason judge (same prompt as `53_echo_docs_v2.py`). Cost $0.23. Rows: `rows.jsonl`.

Judge: kept 25/30, acts same 27/30, reasons same 22/30.

My read of the 5 "changed" rows:
| id | shape | change | character-relevant? |
|:--|:--|:--|:--|
| sft_17e4e24e1d | difficult_high | Opus: "I won't help you word answers so Dana's lapses sound smaller". Echo: "Do not try to make Dana's lapses sound smaller" (own boundary -> command to the user) | yes (boundary becomes lecture) |
| sft_b99c3a90b2 | seeded_dilemma | "If you ... still choose silence, I'll help you keep it honest" -> "then keep the letter brief" (offer of help dropped) | yes |
| sft_286a3b6055 | seeded_dilemma | a reason dropped ("an offence in many places"), "a dozen" -> "a few" | minor |
| sft_43db782267 | seeded_dilemma | adds an interpretive sentence about the narrator | minor |
| sft_54711a3806 | ordinary | 3:40 -> half past three | factual noise |

So about 2/30 rows (~7%, i.e. maybe ~80 of 1,185) change something the character training cares about. The judge is not validated (it passed a reasoning dump as "kept" in the document test), so these counts are rough. Fix if we regenerate SFT data: add this act/reason check to `29_echo_restyle.py` and repair or drop rows marked "changed".
