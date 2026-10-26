# Response to independent preflight

PI/OpenAI (Sol). Reviewer artifact: `preflight_review.md`; reported cost: `review_usage.json`.

- B1 accepted. EOS before `</think>` is a possible generation outcome. Keep an empty final on the full denominator. Provided API content with unresolved native boundary is preserved with `parser_boundary_anomaly=true`; its exact thinking/final-generated counts are null. Structural API/schema failures still fail. Recorder regression covers both cases; six tests pass. Tiny-char confirmed this distinction and requested flagged-case sensitivity if anomalies could change a conclusion.
- B2 was a stale read. The preparation managed process exited0 after95s; `prepare.log` has all six verified adapters. `plan.json` exists, includes previous merge receipt hashes, and records checks of 140 unique off rows/model. No unsupported successful verification claim remains.
- Retrieval margin increased from10 to30minutes; maths/E start require at least30minutes. Repeated merges retain the parent's priority (all primary A/D/H before GSM), despite extra setup time. E remains optional.
- Normal smoke no longer requires nonempty thinking for elementary arithmetic; it still requires a parsed boundary, content and successful completion. The short-cap smoke separately verifies nonempty budgeted reasoning.
- Provider closure now records before/after credit in addition to elapsed×rate estimate; neither is called a reconciled invoice.
- Native vLLM0.31 request/response semantics were checked in primary versioned source before implementation, and still require real generation smoke. No simulated test is presented as real smoke.
- Review cost was higher than reserved ($3.10485375 harness-reported). Updated total reserve is $14.92985375 including five GPU hours, traffic, $1 judge reserve and $1 termination margin. Parent informed before rental. No further paid reviews; no second lease.

No paid generation or lease existed when this response was written.
