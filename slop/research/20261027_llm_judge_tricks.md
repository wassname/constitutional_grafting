# Tricks from wassname's llm-judge to reuse in the v2 data build

Read 2026-10-27 by PI/Claude (opus-5-5): `docs/defaults.md`, `docs/jev.md`, `src/llm_judge/judge.py` (function list and `with_vent`, `provider_options`) of https://github.com/wassname/llm-judge (shallow clone in `.local/llm-judge`). Not Inspect: only the tricks.

## Jev (filters)

- One request per row: shared `state` (a short task signpost plus the data), many `questions`. "Jev evaluates questions in isolation. Sharing `state` does **not** let one question read its siblings." Put each definition in that question's `instructions`, not in the state.
- Answer types: `noul` (yes/no probability), `choice` (unordered options), `score` (2 to 10 ordered levels). Keep the probability vectors, not only the mean.
- Vent: an extra unscored Choice question, "What needs attention in this judging setup?", with an exact copy of the scored questions in its own instructions (`with_vent`). 219 options; "`none` is not clearance". Read the full vector.
- Order check: send a second presentation with unordered Choice options reversed; do not reverse Score levels.
- `llm-judge diagnose controls`: clear, missing-reference and truncated controls; useful to check the vent works on our setup.
- Post-label interview (talk to Jev): "not yet a reliable critic"; use as a lead only.
- Pin `typesafe/jev-1.13`; record the served model; fail on a changed served model.

## OpenRouter (Kimi, Haiku, cheap teachers)

- `provider: {only: [endpoint], allow_fallbacks: false, require_parameters: true}`; check the returned provider name.
- Prefer the model creator's endpoint; third-party hosts only with known FP8 or better.
- Reasoning counts against `max_tokens`: give a large allowance and inspect truncation (`finish_reason == "length"`) instead of assuming.
- On a malformed or invalid judge reply: save it, one retry, never patch with regex or invent a score.
- Judge quotes are checked as exact substrings of the judged text; that catches invented quotes, not wrong readings.
- Read one complete sample end to end (input, rubric, provider reasoning, raw reply) before trusting an aggregate.
- Different model family for judge and teacher (self-preference, Chen et al. EMNLP 2025).

## What we do with it

Jev filter step: call `llm_judge.label(state, questions, trace=...)` if it installs cleanly in the v2 env (vent and option reversal come free); otherwise copy `with_vent` and the request shape. Haiku whole-pair step: evidence first (quotes), then verdict, quote check, one validation retry.
