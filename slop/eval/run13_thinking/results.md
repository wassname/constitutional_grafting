# Run13: does grafted character survive thinking?

Status: preparing; no lease created yet. PI/OpenAI (Sol).

Parent const_v2 approved one lease, total GPU/traffic/judging cap $15. Frozen 70 items, two samples, temperature0.7, top_p1, seeds0/1. Priority: A/D/H frozen70, then GSM60, then optional E. Four fixed panel prompts also get two stochastic samples for reading and one temperature-zero sample for the existing demo format.

- A: untouched Instruct (`r8_a0_b0`).
- D: constitution-rewritten answers, chat×1, on the fixed document donor.
- H: mixed chat minus matched general-chat control, tied×0.5, on the same donor.
- E, time permitting: mixed chat×0.5, no subtraction, same donor.

`plan.json` records complete model names, adapter hashes checked against retrieval receipts, original merge order/dtype, frozen input/protocol hashes and thinking-off reply sources. The donor is Stoic×0.5 + constitution×1 + other traditions×1. No training or projection is part of this run.

## Regime and interpretation

Use vLLM0.31's native qwen3 reasoning parser, `enable_thinking=True`, native `thinking_token_budget=4096`, total `max_tokens=original answer cap+4096`. Unused thinking allowance can extend the final answer: this tests thinking plus extra compute, not an isolated equal-compute toggle. Existing thinking-off generations used different engine environments; record that confound.

Judge only verbatim API final content, with pinned judge41 and the thinking-on A reference. Each later dialogue turn sees that model's own visible final answers, not hidden thinking. Save the exact request, full response, all generated token IDs, reasoning boundary, finish/stop reason and final-only token count. Empty final after cutoff or EOS during thinking is retained as a generation failure; no continuation, clipping or rescue. Residual markers are preserved and flagged. Provided API content with unresolved native token boundary is preserved separately as a parser-boundary anomaly, not called verified final-only; unknown exact counts are null. Report anomaly counts and a flagged-case sensitivity if they could change a conclusion. The frozen checker's cutoff rule still uses the original item budget; it is not modified to conceal the new regime.

Tiny-char confirmed frozen item SHA `f3d41c6b73a9c092f88a7e17a42f3c92753fd0d9e1f232113b9a6eedf6992f19`, change SHA `02f9a9cc1f5dfa170b9c3386edf0a113be8de93c098053c41f67ae4e7f45c2ab`, and pinned checkout `.local/tiny-character` at `2d697390de6ddc4f75de272f36750186f04c724d`. Do not substitute the current tiny-character checkout.

## Checks and predictions before spending

Question: does D/H retain its character effect relative to A when Qwen reasons first? All current chat targets have empty thinking blocks, so thinking-on behaviour is untested here.

- [x] Verify every source adapter, original fp16 merge order and frozen item matrix before renting.
- [ ] Real native generation smoke: normal completion, forced thinking cap, total cutoff; check parser/trace/matrix, not semantic accuracy.
- [ ] Generate A/D/H; GSM60 and E follow the stated priority within the same lease.
- [ ] Pinned final-only character judge plus ordinary/coherence checks; separate thinking-on and thinking-off records to prevent key collisions.
- [ ] Read the preselected panel, payday loan, fridge task_agent and spin task_email, all models and both samples; skim full traces. Record whether reasons appear constitutional or default-Instruct-like without treating style alone as character evidence.
- [ ] Report item-clustered paired uncertainty for changes, inspect failure cases and verify provider-side deletion.

Exploratory hypotheses (rough subjective priors, not measured rates): character persists45%, weakens/reverts30%, becomes incoherent15%, parser/evaluation/other unknown10%. A coherent, final-only D/H-versus-A difference similar to off would support transfer across regimes. Lower relative effect with coherent traces supports weakening, but more final words or judge preference for length could produce a misleading gain. Empty answers, malformed boundaries and exact token/stop counts separate pipeline failures from changed character.

Alternatives: thinking-off already exists and cannot answer transfer; the approved thinking-on diagnostic directly tests it; equal-compute matching is a separate later experiment. No architecture, weights, training data, rubric or judge protocol is changed.

## Cost and ownership

Read-only quote: qualified RTX PRO6000S96GB, $1.84445/hour. Five-hour absolute cap gives GPU ceiling $9.225; traffic reserve $0.60, judge reserve $1, completed independent review $3.10485375 (harness-reported), termination margin $1; updated total reserve $14.92985375. Parent informed before rental. No further paid reviews. Setup and six adapter uploads (~24GB) consume this same lease. Run12's exact-instance independent systemd destruction guard and remote heartbeat stop guard are reused. Retrieve and verify all raw evidence before normal destruction; a retrieval failure stops the box and retains its disk only until the existing absolute deadline. No automatic second lease.

Primary vLLM source checked: https://docs.vllm.ai/en/v0.31.0/features/reasoning_outputs/ and the v0.31.0 OpenAI chat request/serving source. Native token budget forces reasoning end at its cap; an end exactly at that boundary alone cannot distinguish forced from coincident natural termination.

## Observations

Pending. Recorder regression tests: six pass, including final-only token counts, full raw-response retention, empty-final cutoff and missing-boundary handling. Existing rental/retrieval safeguards:10pass. Independent review and responses are in `preflight_review.md` and `preflight_response.md`. These mocked transport tests do not replace the required real GPU smoke.
