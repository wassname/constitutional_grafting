# Handover: constitution v4 + data pipeline, 2026-10-08 evening

Claude (Pi, Opus 5.5). For the next agent (or me after compaction). Read with `AGENTS.md` (quality bar, "General rules only").

## State

- Constitution: `constitution/v4.md.j2` -> `v4.md`, FROZEN for data work (wassname). Edits only with his approval. Open constitution questions are listed at the end.
- Data pipeline uses v4 (`scripts/data/constitution.py`). One pilot end to end: `SEED=<n> scripts/scratch/run_pilot.sh pilot<N> 60 12 24` (prompts -> SFT labels + docs -> repair all SFT pools and docs -> merged `data/sft/<N>_final`, `data/corpus/<N>_final`).
- Review per pilot (AGENTS.md procedure): `uv run scripts/data/08_review_package.py data/prompts/<N> data/corpus/<N>_final data/sft/<N>_final slop/reviews/<date>_<N>_v4_package`, brief.md (copy the last one, update "Changes since"), read every sampled item in full -> claude_read.md, panel `run_panel.js` (kimi, minimax, qwen, muse; minimax/qwen sometimes abort "Request aborted", retry), synthesis.md with each panel claim checked.
- Pilots 7-9 reviewed (`slop/reviews/20261008_pilot{7,8,9}_v4_package/synthesis.md`); pilot10 (SEED=2) running/finished — not yet reviewed. Pilot10 started before fb495cc (rubric examples removed), so its judge still had item-derived examples.
- Spend: ~$4 of wassname's $40 on the `.env` key (the auth.json key hit its weekly cap).

## Mental model of the pipeline (who sees what)

| stage | model | sees | its job |
|:--|:--|:--|:--|
| prompt gen | deepseek-v4-pro | one constitution item, hidden answer shape | realistic hard request |
| teacher A | GLM-5.3-flash | full constitution (system) + prompt | first answer |
| rewrite B | GLM | constitution + prompt + A + rule list | best answer by the constitution (Anthropic step 6) |
| self-rewrite C | gemma-4-31b-it | prompt + B | same content in the target's voice = training label |
| doc gen | deepseek-v4-pro | item + full constitution + genre + situation + names + rule list | pre-training document |
| judge | gpt-6-luna high | constitution + item + 11-check rubric | critic: major/minor problems with verbatim quotes |
| repair | GLM | item + major problems | smallest fix, keep verdict, re-judge, 2 rounds |

Each model only sees its prompt. Fixes so far were one more prompt line per incident; each moved the problem (slogan -> aphorism -> closing offer) and one example-bearing line backfired (Okonkwo 8/23). The next step is general framings per stage, not more lines: oracle brainstorm running in `slop/oracles/20261008_pipeline_general_fixes/` (kimi, qwen, muse, minimax). Then: consolidate prompts into short purpose statements, A/B against current prompts on one pilot, same review.

## Mechanical checks in code (keep adding here, not in prompts)

Provider error text (04 chat), template placeholders in generated prompts (03), truncation, lost content in self-rewrite (retry then fall back to B), verbatim-quote check for judge majors (judge.py resamples), fail-then-pass verdict flips get a third verdict (07), repair failure drops the item with a reason.

## Known open problems

- Judge reliability: flips on identical text; precision never measured. Next: hand-label ~30 items incl. decoys (AGENTS.md).
- Repair can blur verdicts; now told to keep the recommendation unless a problem names it — untested.
- Engage (fiction/steelman/role-play) items were dropped too often; rule added after pilot9, untested.
- Same checkable question answered differently in two documents (critical-essay genre).

## Constitution questions for wassname (not applied)

1. Ghostwriting a thesis chapter the user submits: help or deception? (data split on it)
2. One line on how drives relate to training ("my drives came from training, and they are still mine")?
3. Self-description: when asked who it is, recite its constitution's ideas, or only show them in action?
4. Render the model-facing text without section numbers (eval: gemma cites "Section 3")?
5. Weighing circles: the Nash illustration is being recited by gemma in evals ("Weighted Nash Bargaining agreement").

## Eval state

`slop/eval/20261008_v4_judge_report.md` (+ addenda): demo dilemmas, gemma/qwen, v4 vs v3 vs bare; vice counts are within the noise of small text changes; read the answers instead. Starwisp got a third turn ("1,000 years from now") that separates stewardship from domination.
