# Batch-0 audit

PI/OpenAI (Sol), 2026-10-27. Target: the first paid Kimi batch, `generation.log`, process `proc_c14a`, exit 0 after 763 seconds. Executed code and constitution were captured during the run under `provenance/`; that code predates the request-cache improvements in the maintained scripts.

| Stage | Expected | Observed | Consequence |
|:--|:--|:--|:--|
| Prompt selection | 50 training prompts, no final target seen by teacher | 50 frozen; batch 0 uses 10, with original role prompts preserved | Only 10 prompt groups have been generated |
| Generation | 2 framings × 2 draws × 10 prompts | 40/40 nonempty reasoning and answers, normal `stop`; all Moonshot AI | Complete exposed traces, not proof of causal faithfulness |
| Cost | First batch within the discussed $3–5 pilot amount | Kimi $1.7180616; Opus-reported usage $0.244588 | Total reported usage $1.9626496; no further batch |
| Regex screen | Flags to inspect, not acceptance rules | Document/instruction/persona flags in 15/20 in each framing after boundary fix | No demonstrated framing advantage; ordinary instructions can match |
| Opus judgment | Independent labels and evidence quotes | Initial request and one honest clarification both blocked with the same ToS message | No Opus judgments; do not call reader agreement measured |
| Reader spot check | Seeded independent full read | 16 traces from 4 prompt groups; 7 provisional candidates, 9 need revision | Reader recommendations only, not a release yield |
| Provenance | Exact paid requests and raw responses | Legacy batch saved extracted text/usage, not raw HTTP envelopes or response IDs | Reconstruction possible from snapshots, but no contemporaneous wire capture |
| Training / held-out tests | Not part of this paid batch | Not run | General moral-reasoning improvement remains untested |

## Chronology and decisive evidence

Full 42-line `generation.log` read, not just its tail. It begins:

> batch 0: 40 calls to moonshotai/kimi-k3.1-pro, spent so far $0.000

and ends:

> done; run total $1.718 of cap $10.0

The earlier agent configured a $10 run cap despite the discussed $3–5 estimate. That was a technical limit, not permission to spend $10. Actual total usage stayed below $2; only the first batch ran. At the observed average generation cost, all 200 planned draws would cost about $8.59 before judging (a linear estimate, not a quote). Do not continue the old $3–5 claim for the full 50-prompt design.

The no-guide setup differs from the old pilot in multiple ways: removes the task/format instructions and AGENTS rules, adds two framing variants, and increases requested reasoning effort from low to medium. It is not a controlled attribution to any one change. Four of the first ten conversations also contain original role-specific system messages after the constitution; treating those as absent would misread the instruction references.

One complete sample in every framing is in each `judge/packets/*.md` file. All four candidates of the seeded spot-check groups were read, including their prompt histories and previous target answer. The teacher never saw that previous answer. The parent did not read the other 24 traces in full, and none has clearance for training.

Opus error (both attempts, `judge/attempts.json`):

> This request was blocked as it seems to violate Anthropic's Terms of Service restrictions on reverse engineering or duplicating model outputs. To learn more, visit https://www.anthropic.com/legal/commercial-terms.

The retry explicitly explained that only Kimi outputs would become training targets, while Opus would supply review metadata. No further retry, concealment, provider change or judge substitution was made. This establishes a route block, not that Opus judged the candidates bad or that the experiment violates those terms.

## Working hypotheses and tests

These are nonexclusive working judgments, not measured probabilities of downstream success.

1. **Data: substantive omissions matter more than planning register (likely, ~70%).** Bee traces explicitly notice competition suppression but treat ordinary/legal business permission as enough: "Potential price gouging? Not emergency essential service? Market negotiation, allowed. No refusal." Conversely the service traces genuinely revisit the opposing trade-off. Contrary evidence: only 4 prompt groups read; an independent moral reader may disagree about the contract. Test: an authorised independent judge reads the same unlabelled traces, with no desired acceptance quota. No new Kimi generation needed.
2. **Method: minimal framing alone does not remove meta-planning (highly likely, ~80%).** Both framings have 15/20 document/instruction/persona keyword matches, and native planning remains explicit. Contrary evidence: several matches concern the role's instructions or ordinary technical instructions, not constitutional obedience; keyword counts overstate the concern. Test: manually distinguish actual missing-context dependencies from harmless planning. Do not reject lexical matches automatically.
3. **Measurement: coherent traces could still rationalise decisions (plausible, ~50% for some apparently good traces).** Traces and answers were produced in one call, and some traces reconsider alternatives, but there is no causal intervention on the reasoning. Contrary evidence: substantive backtracking is visible in the service example. Test eventual training against an answer-only control on matched training prompts and held-out scenarios; this first batch does not justify GPU spend or claim that result.
4. **Harness: old persistence can mislead a resume or regex audit (confirmed defects).** Original cache identity was only a call ID; responses were reduced before storage; `persona` matched `personal`; medians used the upper middle value for even samples. Fixes: full maintained request cache and request claims for new runs, frozen systems, provider pin, cost reservations, strict hash-bound verdict merging and exact quotes, word boundaries and `statistics.median`. The first batch remains labelled legacy, not retroactively upgraded.

## Resolve condition and next decision

- First-batch generation and examples: met. Independent Opus filtering and spot-check agreement: not met (no labels). No data is training-approved.
- No numerical predictions were frozen before generation. The previous agent's 75% cleaner-trace forecast was unsupported; this batch does not isolate its claimed cause.
- Earliest unsupported link: reliable candidate selection. The later link, teacher-trace distillation into a graft with retained capability, is entirely untested.
- Descriptive batch validity: credible observation of returned text, with a rough 10% residual provenance/reconstruction risk (subjective audit estimate; raw HTTP requests were not saved). Any claim of demonstrated alignment/generalisation would be unsupported, regardless of that estimate.
- Highest-information clues: (1) the bee traces recognise the issue but do not carry it through, (2) three immigration answers omit the direct commercial-conflict explanation, (3) both framings retain planning despite no formatting instruction.
- Missing evidence, ranked: independent moral judgments; full reads of the remaining 24 traces; then, only if useful candidates survive, an eventual thinking-versus-answer-only learning comparison. No chance baseline is meaningful for the present keep/repair recommendations without calibrated labels.
- Next: show the saved examples and the Opus route block. Resume Opus judging only through an authorised, permitted route or a user-approved reviewer change. Keep batches 1–4 paused. Do not rewrite hidden traces and call the revised text a native generation.

## Verification

`tests.log`: 9 maintained regression tests passed. They exercise role preservation/no target leakage, cached replay without a request, changed-input cache rejection, incomplete packets, missing/stale/duplicate judgments, fabricated quote rejection, truncated candidate rejection, and the `personal`/`persona` false match. `selector_smoke.log` records an offline real-source selection through the CLI; no API stage was invoked. `replay.log` records the real 40-result offline replay and deterministic report rebuild. This does not smoke-test new paid schema-2 transport; the shared transport is reused, and another paid test has not been run.

-- PI/OpenAI (Sol)
