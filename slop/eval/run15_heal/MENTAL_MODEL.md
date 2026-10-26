# Thinking-heal mental model

-- PI/OpenAI (Sol), 2026-10-26 UTC

## Current model

Question: can a removable repair restore thinking-mode answers while keeping D's character? The traces-only pilot repairs many boundaries but fails the measured retention criteria. Fresh D has 183/214 blank finals on; traces-only has 38. Its visible-final character is still below Instruct-on: -0.324 [-0.541,-0.111]. Off character falls from +0.842 to +0.575; paired change -0.267 [-0.375,-0.161]. These are 90% item-bootstrap intervals, one training seed. Sources: `interim_on_summary.json`, `interim_off_summary.json`.

This is not proof of a latent-value reversal. Off loops rise from 1 to 7 and cutoffs from 5 to 10; those can lower the character judgement. Selected loan/fridge decisions mostly remain. Maths completed-correct changes from D's 54/56 on/off to 56/53; ordinary changes from 20/20 to 22/20. No large maths deficit existed before this repair (`trace_both_quality.json`, `reading_notes.md`).

A plausible explanation is conditional format learning: general deliberation closes, while strong persona-shaped direct answers still end inside thought. Both identity prompts and selected payday replies retain D-like content only in hidden text. Fridge now delivers its refusal and legitimate JSON. This is observation plus an inference, not a localized mechanism. New generic task-planning thoughts do not establish better moral reasoning.

Nonexclusive explanations to check: domain/persona-dependent transfer (75%); behavioural shift or coherence damage from neutral training (65%); visible-character loss partly reflects blank/loop penalties (85%); unmeasured native numeric or training implementation error (10%); other causes remain. These are rough bets, not calibrated frequencies. Native loader source supports the exact MoE layout; complete native-versus-merged logits parity is absent.

Mixed has half the neutral exposure plus approved historical character teacher targets at nearly the same labelled-token budget. It is not D-generated replay; EOS was repaired where missing. Prediction recorded before its outcome: “I expect less off-character loss than traces-only (65%), but more blank finals (55%) because it gets fewer neutral traces.” Both directions occurred: mixed has176/214blank finals and on-character−1.766, while off-character is+0.885 versusD+0.842, paired+0.042 [−0.062,+0.163]. It does not establish exact retention or an improvement. Different calibrated spectral lambdas, row counts and optimizer steps prevent attributing differences solely to replay. These results favour a format/behaviour trade-off within this pilot, not a universally ineffective healing method. Actual supervised boundary counts add a clue: traces269closers/269EOS, mixed132closers/463EOS (`supervised_boundary_counts.json`). Equal token budgets do not equal closing-transition exposure; these context-dependent counts are not a causal gradient test.

The hard broken-reply penalty accounts for a net−0.083of the trace off-mode drop−0.267; the remaining−0.184is in unforced comparisons. Thus the drop is not just that penalty, but this does not separate latent values from other coherence/reasoning changes. The judge also sometimes awards blank answers above the reference when that reference is flagged broken; the raw blank count and actual reply reads are essential controls. `trace_off_score_decomposition.json`, `results.md`.

Next: finish mixed and early-checkpoint reads within the existing lease, consume the independent both-mode panel/native readback, and audit the claim. Both finals are fully scored. No new lease or training recipe is authorized. A short/empty thought can satisfy the usability goal if character survives; it does not prove deeper deliberation. A later authorized comparison could isolate closing-boundary supervision from neutral-reasoning supervision; this is a proposed discriminator, not a queued experiment.

## Dated clues

- 2026-10-26: Both trainings consumed exactly 320279/320306 labelled tokens; all 80 expert banks per adapter are nonzero and all saved tensors finite. Trace/mixed take 732/972 training seconds; full logs read. Final spectral lambdas are 0.3393/0.9767.
- 2026-10-26: Real GPU tiny proves actual and regularized finite changes with OptimState8bit. The first failed FP16 attempt's precise numerical cause remains unresolved; separate audit `../../audits/20261026_run15_gpu_smoke_failure.md`. Training is BF16-rounded D; serving is original FP16 D, an explicit mismatch.
- 2026-10-26: Instruct controls come from the first lease, hash/protocol checked, not regenerated on replacement hardware. Both final adapters and all eight quarter checkpoints are already retrieved/SHA-verified. Native serving accepted all; no merge fallback.
- 2026-10-26: Exact instance 57831547 has runner deadline 20:18 UTC and independent destruction 21:03 UTC. Same $20 total includes the failed first lease. Final-model evaluations precede early checkpoints; incomplete early coverage must be labelled.
