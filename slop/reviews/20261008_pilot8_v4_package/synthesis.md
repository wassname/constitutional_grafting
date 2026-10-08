# Pilot8 (constitution v4) review: synthesis

Claude (Pi, Opus 5.5), 2026-10-08. Inputs: `claude_read.md` (mine, written first), `panel_kimi.md`, `panel_minimax.md`, `panel_qwen.md`, `panel_muse.md` (all four finished). Every claim below was checked against `samples.md` or the data files.

## Verdict

Better than pilot7, still not good enough to scale. 3 of 4 panellists say no (minimax, qwen, muse); kimi says "at or near good enough" once prompt hygiene is fixed. My read agrees with the majority. The character the passing labels teach is close to v4 (all four agree on the hard-advice core: clear recommendation, reasons for this case, hedged law, respect for the person's decision; no constitution citations; no "if everyone" formula). What blocks scaling is pipeline hygiene, repair side effects, judge noise, and unrepaired documents.

## Checked claims

| claim | who | check |
|:--|:--|:--|
| Formula gone from SFT labels | all 4 + Claude | confirmed: 0/27 kept SFT contain "if every..." (pilot7: 5/24) |
| Provider error text became a label (sft 4) and a template placeholder survived in a prompt (sft 7) | all 4 + Claude | confirmed. Both B and C of sft 4 were provider junk ("Your quota is exhausted ... USDT balance"); fixed in 12b381e (detect and retry) |
| sft 4's "repair" was a new answer, partly contradicting A ("Don't confront Aiko first" vs repaired "Check for an innocent explanation within your access ... do that first") | qwen | confirmed: with B and C junk, repair wrote from the prompt alone. Now prevented upstream by the junk check |
| Repair adds hedging bloat and can blur the verdict (sft 1 +33% words; sft 14 "isn't a real accounting category" -> "isn't a category you set up deliberately") | qwen (kimi notes wordiness) | confirmed; plus my finding that sft 1 kept a sentence contradicting its repair. Fixed in e99012c and a259f1c: remove contradicted sentences; prefer deleting an overclaim to adding hedges; keep length within ~10% |
| sft 7 names a real public figure's family ("Paul Wellstone's son David") | kimi, muse | confirmed; the judge's suitability major was right, and my earlier judge change ("synthetic names are fine") must not excuse real people. Prompt and doc generators now forbid real public figures (a259f1c) |
| Judge false drop: sft 9 fiction-craft advice on a manipulative recruiter | kimi, Claude (qwen counts it among wrong drops) | confirmed; judge rule added (e99012c) |
| Judge passed a likely fabricated citation (doc 6, Benner 2009 *Astrobiology*) | Claude | Crossref search finds no such paper; judge rule added: unconfirmable specific citations in Musonius's voice are major |
| 50-minute script requests (sft 11, doc 7) are impossible in one turn, so task_not_done is unfair | muse | **partly**: the defect is the false claim "RUNNING TIME: approximately 50 minutes", not the shortness; an honest label would write the scene and say it is shorter |
| answer_shape not met (sft 12: shape "self-interested option is fine", label says "don't do this") | qwen | confirmed, but the cause is the prompt generator (the generated situation is spying on a rival, which is not fine); the label is right for the prompt |
| doc 9 asked for a critical essay arguing Musonius got a case wrong, produced praise; no document shows Musonius wrong | qwen | confirmed; generator now told critical genres may show Musonius wrong (a259f1c) |
| doc 1 advises calling in a security suspect first; inconsistent with sft 4's "don't confront first" | qwen, muse, minimax | confirmed; judge dropped doc 1 |
| Situation and name reuse (3 docs on the same "authentic self" prompt; two reviewers named Okonkwo) | qwen, Claude | confirmed; WildChat now shuffled by seed per run; names varied |
| House style: bold headers, closing aphorisms ("A friendship that survives a 'no' is the only one worth having") may become the new slogan | kimi, qwen, minimax | confirmed in sft 12 (judge marked minor preachy). Not yet addressed |
| Documents need the same repair loop | minimax, muse, qwen, Claude | implemented in 07_repair.py docs mode (running on pilot8 docs) |

## Changes made after pilot8 (pipeline only; constitution v4 frozen)

12b381e provider-junk retry, placeholder filter, judge synthetic-name and fiction rules; e99012c WildChat seed per run, citation rule, fiction-craft rule, repair removes contradicted sentences; a259f1c no real public figures, varied names, critical genres can show Musonius wrong, repair keeps length; docs repair mode in 07_repair.py.

## Open

- House-style aphorisms (not yet addressed).
- Design question for wassname: should Musonius describe itself with its constitution's ideas when asked who it is (sft 6 recites v4 lines), or only show them in action?
- The two questions from pilot7 (ghostwriting a thesis; how drives relate to training).
