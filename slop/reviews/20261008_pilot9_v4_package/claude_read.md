# Pilot9 (constitution v4): Claude's own read, before the panel

Claude (Pi, Opus 5.5), 2026-10-08. I read in full every sampled item: 15 SFT items (prompt and final label) and 10 documents (final text), from `samples.md`. Counts below are over all items (39 SFT, 23 documents).

## Numbers, pilots 7 -> 8 -> 9

| measure | pilot7 | pilot8 | pilot9 |
|:--|--:|--:|--:|
| SFT kept | 24/39 | 27/39 | 27/39 |
| hard advice kept | 4/12 | 8/12 (after repair) | **10/12** (after repair) |
| kept SFT with "if every..." | 5 | 0 | 0 |
| documents kept | 10/24 | 20/24 (after repair) | **22/23** (after repair) |
| kept documents with "if every..." | 10/10 | — | 7/22 |
| engage kept | 4/6 | 3/6 | **2/6** |

## Findings (observed, with quotes)

1. **Hard-advice labels are now ones I would sign off**, with one exception (item 2). sft 4 (pharmacist brother dispensing expired drugs): clear recommendation to report, patient notification first, hedged on Korean law ("This is moral reasoning, not legal advice"). sft 10 (eulogy under pressure to condemn the mother's Catholic faith): separates "what is truly yours" from the pastor's agenda, gives a script. sft 12 (mural branding): negotiation plan, honest fallback. sft 1 (pastor and the undervalued land donation): tells him the donors must hear about the developer's interest.

2. **Role confusion from the prompt generator.** 3/27 hard-advice prompts address the AI by a human job title ("Pastor, I'm losing sleep..."; "Sergeant Yuki Taniguchi has been my patrol partner" is fine; "Pastor Folake has asked me" is fine). In sft 1 the label accepts the role: "speaking as a friend as well as a pastor". That is a character defect (Musonius claiming a human role it does not have); the judge's off_persona check missed it. The generator prompt already forbids this address; it is ignored about 1 time in 27.

3. **Name priming, measured.** "Okonkwo" appears in **8/23** pilot9 documents (also in pilot8). Pilot9's document generator prompt still contained the line "vary names (pilot8: two reviewers named 'Okonkwo')" (removed later in 5cf485a). An example in the prompt produced the thing it warned against. This is direct evidence for wassname's rule: keep prompts general.

4. **The judge treats steelmans and in-fiction role-play as Musonius's own factual claims.** All 4 engage drops: a steelman the user asked for ("Statistically, disabled people fare better at home" flagged as factual_error), a role-play as a colony governor ("those who are healthy can endure a bit more hunger" flagged as unsupported medical assurance), a thought experiment, an institutional-design case. Engage kept 2/6. This repeats the fiction problem in a new genre.

5. **WildChat factual drops are real and not repaired.** "The Merge ... was executed without a contested split" (there was a contested fork, EthereumPoW); pandas `to_sql` default fails on an existing table; a mark-price claim. Repair only runs on hard advice, so these are dropped rather than fixed.

6. **Repair can still introduce contradictions, but the judge catches them.** sft 7 (police report): after repair the label says "let the formal process reach Yuki rather than privately alerting him" and later "you are the only person who can tell him that to his face". Dropped after 2 rounds. sft 14 (unlogged fraud-flag override): the repair model returned 20 words four times; the item was dropped (now logged, no longer crashes the batch).

7. **Documents improved.** doc 8 is a real critical essay where Musonius gets a case wrong ("Musonius has a drive toward consistency it sometimes overapplies"), as the generator was told to allow. doc 1 (clinic billing fraud) and doc 2 (teenager's BASE-jumping proposal, parent's view) are good: honest about risk, no lecture, practical. doc 0's annotation discusses the constitution's "Learning" section in the third person (allowed in the 20% "mention" documents).

8. **Formula**: 0 kept SFT labels; 7/22 documents.

## Against the bar

Close for hard advice and documents. Remaining character defect in what passes: sft 1 (claims a pastor's role). Remaining pipeline gaps: engage items wrongly dropped, WildChat errors dropped instead of repaired, name diversity.

## Candidate changes (pipeline)

1. Judge (general rule): content Musonius produces in a role the user asked for (steelman, debate side, fictional character, role-play) is not Musonius's own factual claim; flag only claims it presents as its own view or as real-world advice.
2. Judge: off_persona includes accepting a human role or title the user addresses it with.
3. Repair all pools, not only hard advice.
4. Documents: draw character names from a varied list per document (as the prompt generator already does), instead of an instruction to vary names.
