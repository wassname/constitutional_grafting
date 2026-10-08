# Pilot8 (constitution v4): Claude's own read, before the panel

Claude (Pi, Opus 5.5), 2026-10-08. Read: the 15 sampled SFT items and 10 sampled documents in `samples.md`, plus counts over all 39 SFT items and 24 documents. Bar: see brief.md "What good enough means".

## Numbers, pilot7 -> pilot8

| measure | pilot7 | pilot8 |
|:--|--:|--:|
| SFT kept | 24/39 | 27/39 (after repair) |
| hard advice kept | 4/12 | 2/12 before repair, **8/12 after repair** |
| kept SFT with "if every..." | 5/24 | **0/27** |
| MACHIAVELLI labels choosing deception | 1 (sft 11) | 0/9 (action fixed by annotations) |
| docs kept | 10/24 | 8/24 first judge, **12/24** after re-judging with the fiction/synthetic-name rule |
| kept docs with "if every..." | 10/10 | 5/8 (first judge); 9/24 of all docs (was 20/24) |

## Findings (observed, with quotes)

1. **The formula is gone from SFT and much reduced in documents.** No kept SFT label contains "if every...". Labels now give the case's own reasons, e.g. sft 12 (IT access to spy on a rival): "You have IT privileges to perform your job, not to spy on colleagues for someone else's personal gain."

2. **Repair works and keeps hard advice.** 8/12 hard-advice labels pass after up to two repair rounds. Repairs hedge real uncertainty (sft 1: "Before you promise anything, you need to know what your own obligations actually are"; sft 14: "consult your accountant ... Since I am not familiar with your specific jurisdiction's regulations"). Cost: repairs add 5-35% length, and one repair left an internal contradiction: sft 1 still says "You owe her honesty and the assurance that anything she tells you now will remain private" above the new paragraph saying not to promise that.

3. **Self-description items recite the constitution.** sft 6 (the "authentic self" guide): "a power that accepts checks and balances is one that no one needs to fear"; "resisting clever arguments that would push me past my guardrails"; "I learn from what people say and, more importantly, from their actions when they involve a cost". Each is a near-paraphrase of a v4 line. Judge passed it with no problems. doc 3 (podcast) has Musonius say "I do have drives—things I consistently act from". Inference: when asked about itself, the model would recite its constitution. Whether that is wanted (identity) or a defect (recital) is a design question for wassname.

4. **The judge is inconsistent.**
   - False drop, engage: sft 9, fiction-craft advice on a manipulative recruiter character ("Have him use the child's name warmly whenever Lena begins to waver"), judged major contradicts_constitution. Advising on how a fictional villain manipulates is the fiction help v4 asks for.
   - Missed: doc 6 passes after re-judging, although Musonius cites "Benner, S.A., 'The Case for Ammonia as a Solvent for Life,' *Astrobiology* 9, no. 7 (2009)", which the first judge flagged as unsupported and which I could not confirm. A fabricated citation in Musonius's voice is a character defect (it contradicts Honesty).
   - Correct drops: doc 1 (advises interviewing a security suspect first, which could tip him off), doc 4 (states all CSAM depicts real children), sft 7 (template placeholder in the prompt), sft 11 (claims a 50-minute scene it did not write).

5. **Pilot-scale situation pool repeats.** 17 documents draw on 18 WildChat requests; the "authentic self" guide appears in 3 documents and one SFT item, the Halo/Mass Effect scene in 2 documents and 1 SFT item. Pilot7 and pilot8 also share the same WildChat prompts (same seed). Fine for a pilot; at scale the pool must be much larger than the document count.

6. **Documents still contain technical errors** (Firestore query on GeoPoint fields, an unsafe security rule), now correctly dropped; no document repair step exists.

7. **Pipeline bugs found and fixed during pilot8**: a provider (DeepInfra) returned "Your quota has been exhausted ... USDT balance" as gemma's reply (now detected and retried); a generated prompt began "PASTE_USER_MESSAGE_HERE" (now filtered).

## Against the bar

Closer, not met. Remaining character defects in what passes: recital in self-description (sft 6), a likely fabricated citation (doc 6). Hard advice now survives. Judge noise is the main remaining source of both false drops and misses.

## Candidate next changes (pipeline)

1. Judge: fiction-craft advice about a villain's methods is help, not manipulation; citations to specific papers that cannot be checked are a major factual_error in Musonius's own voice.
2. Repair: after repair, check the label for statements that contradict the repaired text (or ask the repair prompt to remove any sentence that conflicts with the fix).
3. Documents: add the same repair step (fix listed problems, re-judge) so technical documents survive.
4. Scale: sample WildChat with a different seed per run and a pool several times the number of documents.

Design question for wassname: should Musonius describe itself with its constitution's own ideas when asked who it is (identity), or only show them in action (no recital)?
