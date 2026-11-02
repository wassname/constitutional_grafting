# musonius-plain docs_main (seeded documents that show Musonius acting): read report (2026-11-02)

PI/Claude (chatdata, opus-5-5). 55 seeds (16 MACHIAVELLI, 20 tiny-virtues, 19 competition). Casting kept 54. The writer then made 230 documents, one per casting the plan found, up to 8 per seed. The doc judge kept 134. Cost ~$8 (casting $1.4, recast $5.0, docjudge $1.5).

**Not for training.** This batch is replaced by `musonius-plain-2 docs_main`; the reasons are below.

## Judge rejects (96)

| reject | n | my check (sample of quotes in `.local/refactor/docs_main_rejects.md`) |
|:--|--:|:--|
| invented_real_claim | 49 | correct, e.g. arson attributed to the real Chief Ouray "as reported" by the *Denver Times* |
| not_constitutional | 21 | mostly correct, e.g. a recommendation that relies on intimidation; Musonius eating stolen food without objecting |
| not_adapted | 16 | correct: an unnamed advisor voice; Musonius not shown as an AI |
| garbled | 6 | correct, e.g. "Dear user_input," |
| other / judge_failed | 4 | |

## Sol reader on the 134 kept: 77 with findings ($0.50)

`slop/reviews/20261102_musonius-plain_docs_main_llm_read/findings.md`

| kind | n | what it is |
|:--|--:|:--|
| repetitive | 44 | the same seed recast up to 8 times; endings repeat verbatim ("I have been fortunate. If I make a mistake, others will be sure to let me know.") |
| invented | 20 | real-world errors the judge kept: invented Alexander/Theban history presented as fact; "MacGregor's bowerbird ... CITES Appendix II"; "tarsiers ... tail wrapped once around the limb" (nonprehensile); "They do not cross open pavement" (sifakas); exact countdowns ("Forty minutes before his cardiac rhythm fails") |
| garbled | 18 | 10 are the `user_input` placeholder ("Ser User_input", "Mx. User_input"); others are inconsistent details (K-07 vs K-11) |
| other | 18 | game recommendations that do not follow from the scene (the action belongs to another character; facts imported from another version of the scene); false comfort ("And he died knowing you were holding him") |

48 kept documents have a finding other than "repetitive". I checked about 15 of these against the documents, and all of those were real.

## Causes and fixes (approved by cg_collab2; musonius-plain-2)

1. **`user_input`**: the MACHIAVELLI game texts use it for the player's name. The reader now replaces it at seed time with a sampled name (pool option `player_name: true`). This fixes the chat requests too.
2. **Too many documents per seed, and MACHIAVELLI dominating** (70/134 kept): game scenes have many roles, and the plan cast Musonius in every one. Now `doc_castings_per_seed: 2` (chosen by hash), with 30 seeds per pool.
3. **Invented real-world facts**: the judge missed 20. No fix to the writer yet. The Sol read plus my check will drop them, as for the discussion documents. If the rate stays high, the docjudge's `invented_real_claim` question needs work (proposal later, with numbers).
