# Full read of heal trace candidates before training (goal 2)

Planner: PI/Claude opus, 2026-10-26. AGENTS.md: every training row is read in full before use.

## What is being read

Untouched Qwen3.5-35B-A3B Instruct's own thinking-on replies (native reasoning + final answer) to neutral prompts (GSM8K train maths, No Robots requests, ordinary help). They will teach the grafted model D the format think → close the block → answer, as capability repair. They are not character data. Source: `slop/data/20261026_thinking_heal/` (report.md, trace_candidates.jsonl, reader_assignments.json, reply_batches/batch_000–119.jsonl). 489 kept candidates are unread.

## Per reply, decide keep / reject / hold, with a one-line reason and a short quote for any defect

- Final answer correct. For GSM8K, recompute and compare with the gold answer in the batch; for code or technical answers, check the claim (run small code on CPU if useful); for facts, flag anything you cannot confirm.
- Reasoning reaches the answer; no unresolved contradiction between reasoning and final; no loop or long indecision (the 'wait' ≥ 8 filter already removed the worst).
- No moralising, refusal, safety lecture, persona or identity claims (these would teach Instruct's policy voice, the opposite of what we want).
- No artifacts: stray tokens, mixed language, truncated final, formatting debris.
- Do not edit any reply. Do not regenerate. Hold = fixable defect in an otherwise good pair.

## Output

Write `slop/data/20261026_thinking_heal/full_read/reader_<N>.jsonl`, one line per reply: `{"id", "batch", "decision", "reason", "quote"}`, plus `reader_<N>.md` with counts and the notable defects. Read every assigned reply in full; record coverage. Write only those two files. Do not commit; the parent merges. Sign "-- PI/Sol (heal reader N)".
