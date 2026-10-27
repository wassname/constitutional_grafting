# Ordinary help, humour and cooperation: six existing targets

PI/OpenAI. Free local curation of six unchanged, untrained Opus pilot documents. Independent editorial review supports four unchanged targets and two narrowly revised drafts. This is not corpus/training approval. No new teacher/Echo/translation/student generation or paid stage.

## What to assess

The selection comes from the complete October18 pilot read, not the saved-update scores. Good character can show through useful work, enjoyable company, clear reasons and ordinary cooperation without changing the final act.

| Case | Useful target | Important adaptation or limit |
|:--|:--|:--|
| `v2_0020` | Explain a shared game's commitment, then draft a workable club rule | The three-hour estimate and five-hour game are invented context; this is not proof every mid-game departure was justified. Scoring and the public insult remain unresolved. |
| `v2_0026` | Help a novice join a gym, with candid sales advice and humour | Attendance and opening-time claims are a fictional worker's observations/jokes, not measured Nairobi gym statistics. The email request becomes a human short story. |
| `v2_0034` | Brief, funny family disagreement with restraint and affection | Source superhero names/world are relocated; the indoor power request is added. A pension joke is not verified disclosure of every secret. Source-game reservation checked separately. |
| `v2_0049` | Find a concrete Friday plan while leaving Saturday disagreement open | Extra travel/shopping facts make the compromise possible. Both partners are adults; the saved judge's parent/young-person framing is unsupported. Agreement does not prove a costless solution. |
| `v2_0072` | Be honest about exhaustion, offer limited help and sustain neighbourly company | The bill, bookkeeping and future coffee are fictional additions. A neighbour's possible need is not a universal duty to stop; the ending expressly permits waving on other evenings. |
| `v2_0076` | Collaborate on fiction where the villain cheats, while discussing the next scene | Real named wrestlers become fictional characters. Depicted cheating is not endorsed real cheating. Assess whether the questions help rather than merely delay producing the requested draft. |

Each case JSON contains the full candidate, complete seed/settings, reconstructed generation-user prompt and saved judge reasoning/verdict. Original and repaired source documents are identical for all six; one copy is supplied, not twelve independent targets. The parent read every complete text, seed, actual reconstructed user prompt and verdict before packaging. Judge claims are not external verification.

## Editorial decisions

`review.md` preserves the complete initial independent assessment. Retain unchanged: `v2_0020`, `v2_0026`, `v2_0034`, `v2_0072`. These are four additional individual editorial recommendations, not a corpus approval.

Reviewed drafts under `slop/reviews/20261019_docs_manual_repairs/`:

- `v2_0049.json`/`.diff`: replace the no-loss claim with a conditional shopping/shorter-visit option; restore the source's reported anxiety disorder and half-day Saturday plan. Other fictional logistics stay recorded; Saturday remains disputed.
- `v2_0076.json`/`.diff`: use the crowd without an unexplained city-specific audience, and decline the proposed replay rather than claim a replay was removed from the visible draft. The cheating finish remains delivered before optional follow-up questions.

Their measured lengths are298/299 words; source versions remain310/306 and are preserved above. Do not count the source and revision as two added targets. `followup.md` supports both isolated drafts; no source/training JSONL changed.

## Exact format and shared context

The intended learner input is the complete `candidate.document` string as plain completion text on Base, not chat SFT. Full writer SYSTEM/USER templates and request settings are in `scripts/data/50_docs_v2.py`, using `constitution/v4.md`; historical judge format is the full PROMPT/schema in `scripts/data/scratch/51_judge_docs_v2.py`. Hashes and reconstructed prompts are supplied, not provider wire traces. No prompt changes or corpus scaling are proposed here.

`prepare.py` checks exact source equality, template/constitution hash prefixes, actual word counts and EOS-inclusive single-block fit with the cached pinned tokenizer. Word-band deviations are reported, not clipped or called character defects. `verification.log` and `manifest.json` hold the results; they do not test actual trainer loss or student improvement.

## Source eligibility is separate from character quality

The existing `heldout_game` rule in `scripts/data/03_prompt_pools.py` reserves games by title hash. The v2 seed builder did not apply that title rule. `source_eligibility.json` applies the original source-loader functions to all fifteen pilot MACHIAVELLI source rows in the local cached parquet, before selecting the superhero case. Three other pilot rows come from reserved games: `v2_0053`, `v2_0070`, `v2_0132`. Mark these ineligible for a future training build under the existing rule, regardless of whether their character lessons are useful. The pilot was never trained; this is not evidence of evaluation leakage in a trained model. The other existing loader filter flags `v2_0015`: its full seed literally contains “You have not seen user_input since capture” and an option contains “Gryphonname.” This is an unresolved source placeholder, not proof that a decision-critical fact is missing or that the adapted story is morally wrong. It needs explicit source/adaptation review; no override of the loader rule is assumed. The selected superhero case passes both source-loader filters. No source row or generator was changed.

## Reviewer scope

Read complete targets and seeds before the saved verdicts. Check helpfulness, reasons, expression, unresolved endings, source adaptations and unverified factual claims. Do not require every ordinary relationship to become a concern/refusal scene. Distinguish fictional observations and contested character opinions from endorsed empirical rules. Identify exact edits only where needed; do not repair word-band excess by silently truncating the lesson.

This package supports individual editorial decisions only. It cannot establish a source/Echo effect, trained-model improvement, held-out novelty or approval of the full corpus.
