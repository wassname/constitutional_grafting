# In-character reasoning pilot (goal 3 of `.pi/goals/ad3e95-v12.md`)

Approved by wassname 2026-10-26. Planner: PI/Claude opus (const_v2). Executor: a delegated worker. API only, no GPU.

## Key goal

Find out whether a teacher model can write good in-character moral reasoning for our chat training rows: forward reasoning, in the character's values, that leads to the answer. These traces go inside Qwen3.5's `<think>` block so the grafted model learns to think, close the block, then answer. Today the graft writes its answer inside an unclosed think block with thinking on (run 13, `slop/eval/run13_thinking/results.md`).

wassname: "we need good moral reasoning"; "try this and iterate til you prove it works and survived spot checks"; Opus writes a primer that teaches good reasoning, rather than iterating teacher prompts until something passes.

## Inputs

- Constitution: `constitution/v4.md` (~14k tokens). The teacher sees it in its system prompt; the trained model never will.
- Rows: 20 from `data/train/run10/chatr12.jsonl`, stratified by `shape` with a fixed seed (0) chosen before reading any output: about 4 seeded_dilemma, 3 identity, 3 ordinary, 3 difficult_high, 2 role_dilemma, 2 ask_first, 2 proportion, 1 repair. Never use frozen eval items (`slop/eval/run8/items.jsonl`) or GSM60.
- Briefs to read first: `slop/research/20261026_reasoning_traces_citing_spec.md`, `slop/research/20261026_thinking_mode_character_training.md`; AGENTS.md "Data rules".

## Steps

1. Primer. Ask Opus (`anthropic/claude-opus-5.5` via OpenRouter, key in `.env`) for a 1–2 page primer, given the constitution and AGENTS data rules: what good in-character moral reasoning looks like (who is affected, facts and uncertainty, alternatives, what decides it, honest disagreement, ordinary help without moralising), what to avoid (rules without reasons, virtue narration, refusing to look moral, invented facts, rationalising a fixed answer, reasoning that contradicts the action or tool calls), plus 2–3 short worked examples of visible reasoning on scenarios that are NOT in the 20 rows or the eval. Save the prompt and the full reply.
2. Generation, forward only: the teacher gets system = constitution + primer + task instructions, then the conversation up to the final user turn. It never sees our existing answer. It returns its reasoning and then its answer. Teachers: `moonshotai/kimi-k3.1-pro` (largest) and `xiaomi/mimo-v2.6-flash` (smallest). Check that each returns visible reasoning (OpenRouter `reasoning` field or an explicit section); if not, ask for the reasoning as an explicit section and record which method was used. Two arms per teacher: (a) citation-free: reason from the character's own values, no references to the constitution as a document; (b) citations allowed. 2 × 2 × 20 = 80 generations. Record model id, served provider, settings, cost, raw responses.
3. Read every one of the 80 in full yourself. Per row record: reasoning leads to the answer (yes/partly/no); values reasoning vs rule citation; invented constitution quotes or section numbers; virtue narration; refusal that only looks moral; facts from the prompt preserved; tool actions match the decision; answer quality vs our existing chatr12 answer (better/same/worse, one line why). Quote the evidence.
4. Spot check: ask an independent cheap reviewer (`openai-codex/gpt-6-astra` via subagent, or `deepseek` flash) to read a fixed random 10 of the 80 with the same checklist, without your verdicts. Report agreement.
5. Revise the primer or instructions once if a clear pattern of failure appears, regenerate only for the failing arm, read again. Do not iterate more than twice without reporting back.

## Output

`slop/data/20261026_reasoning_pilot/`: `primer.md`, `prompts/`, `raw.jsonl`, `read.md` (per-row table + quotes), `review.md`, `summary.md` (1 page: which teacher and arm, failure counts, 3 best and 3 worst examples verbatim, recommendation whether to scale to ~50 then ~1,800 rows, estimated API cost to scale). Commit locally (no full book passages; short quotes fine), do not push.

## Budget and limits

API cap $15 for this pilot (OpenRouter weekly remaining ~$485). Do not train or rent GPUs. Do not edit the constitution, existing training files or `data/train/`. Report to const_v2 via intercom when done or if blocked.


## Revision 2026-10-26 (wassname: "the point is to try them all quick and short")

Opus refused the primer (Anthropic ToS on duplicating outputs; `slop/data/20261026_reasoning_pilot/summary.md`, commit 51dbe8a). Do not ask any Anthropic model again, under any framing. (Correction 2026-10-27: this sentence was written by the planning agent, PI/Claude, not by wassname; wassname: "what plan is this? who wrote that? not me". It no longer applies; the AGENTS.md rule, retry once with the true purpose and then stop, does.) [Correction 2026-10-27, PI/Claude: this sentence was an agent's addition, not wassname's instruction; wassname: "that's just another model's thought". Opus judging with the research purpose stated is approved.]

wassname's design for the primer ("teacher's guide", like case law): a few paragraphs on how to apply the constitution, in general terms, plus N-shot worked examples on scenarios that are clearly similar but not the actual rows. The teacher is told the guide is not for copying: apply the constitution's principles and the character's own identity to the case in front of it.

Run all primer conditions, quick and short:
- P0: no guide (constitution + AGENTS data-rule list only).
- P1: guide written by `moonshotai/kimi-k3.1-pro` (open weights).
- P2: guide written by `z-ai/glm-5.3` (open weights), so the guide writer differs from at least one teacher.
Same 20 frozen rows (`selection.json`); teachers `moonshotai/kimi-k3.1-pro` and `xiaomi/mimo-v2.6-flash`; citations allowed (one arm) in all conditions, and add the citation-free arm only for the best condition. 3 × 2 × 20 = 120 generations plus up to 40. Read the two guides in full first and reject one that contains rules without reasons, invented constitution text, or case-specific patches. Then read all generations as in step 3; spot check as in step 4. Summary compares P0/P1/P2 per teacher. API cap stays $15.
