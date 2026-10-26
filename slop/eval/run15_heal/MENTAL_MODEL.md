# Thinking-heal: pre-run model and decisions

-- PI/OpenAI (Sol), 2026-10-26

## Current model

Observed in run13: D has 176/214 blank finals with thinking on, 175/192 on character turns but only 1/22 ordinary turns. Exact hidden-text substitution gives character +0.65 vs Instruct-on; actual visible finals score −1.77. D thinking off is +0.89. This supports a channel/termination habit, not simply erased character. Source: `../run13_thinking/results.md`.

New observation: 903/1,636 executed chatr12 targets lack `<|im_end|>`; the raw input/output loader does not append it (parent audit, commit40de6b4). D's damage may combine empty-think supervision with missing stopping supervision. The mixed heal appends EOS to replay targets that lack it; it is not an isolated test of reasoning traces.

Question: can a small removable repair, trained on frozen D, restore close→answer while retaining its off-mode character?

- Traces-only: 269 fully read Instruct API traces, 320,279 supervised tokens, 337,959 sequence tokens.
- Mixed: 132 trace +331 historical approved chatr12 targets, 320,306 supervised tokens, 397,011 sequence tokens. Replay is the training teacher's targets, **not D's own generated replies**. Half neutral exposure is exchanged for replay; total target tokens match, optimizer updates and sequence tokens do not.
- Fixed recipe: rank8/alpha16 all previous dense/expert targets, frozen fp16 D, LoRA FP32, LR1e-4, one epoch, spectral fraction0.01, quarter checkpoints. KL omitted under cap. LLM-Pruner gives a rank8/alpha16/LR1e-4 recovery precedent, not proof of this recipe; source coverage is the parent's healing literature note, not a new independent paper read.

Pre-run alternatives (rough beliefs, not measured probabilities): format repair with character retained 35%; repair but Instruct-like reasoning/reduced character 35%; too little repair 15%; implementation/eval error 10%; unknown 5%. A new adapter can cancel D even though parent weights are frozen.

Discriminators: repaired blank finals alone are insufficient. Full visible-final character vs fresh Instruct in each mode, off-mode difference vs same D, GSM60 and ordinary/coherence flags, then full T0 panel and payday/fridge/email reads. Fridge's actual tool actions matter. Early checkpoints get selected panels, not full character claims. No single threshold is claimed to establish success; report counts, paired score differences/intervals and observed choices.

## Design checks and predictions

| Option | Expected information | Main failure | Cost |
|:--|:--|:--|:--|
| Traces-only | Can neutral thinking traces restore boundaries? | Restores format by undoing D | One short epoch |
| Mixed, matched target tokens | Does replay improve character retention within this budget? | Reduced neutral exposure or EOS addition explains the difference | One short epoch |
| Optional KL | Not run | Extra reference forward exceeds budget | Omitted |

SHOULD: trace labels include real thought, closer, answer and EOS; replay's empty think block is unlabelled; frozen parent tensors do not change; saved/reloaded heal reproduces live inference. CPU real tiny Qwen-MoE smoke checks these, including expert gradients and fp32 merge parity (`cpu_smoke_v2.log`). Initial local test exposed inconsistent toy-model dtype; setting both nested config and model dtype repaired it, no training data changed.

TODO validate: both heals reduce blanks; mixed retains more off-mode character. A closing-marker shortcut or a short empty thought can look repaired but will fail the held-out choices/usefulness reads. Historical +0.89 is context, not this run's control. Instruct and D are regenerated at the same serving precision and run13 recorder settings. Training seed15 only; evaluation seeds0/1, thinking budget4096, extra compute not equal-compute on/off.

20-step timing must project both variants with ×1.5 time margin while preserving three hours for evaluation before the runner deadline. Six-hour independent destruction timer, 45-minute retrieval reservation, one lease and no replacement. Planning reserve ≤$20 inclusive of traces, judges, failed review, traffic and margin. Actual timing/memory remain unknown until GPU smoke/benchmark.

## Dated clues

- Native vLLM0.31 docs describe fused PEFT expert adapters, but support for this exact artifact is untested. Startup plus per-adapter raw smoke will be retained. On explicit unsupported-LoRA failure, the approved alternative computes update+addition in fp32, rounds once to fp16, reports rounding loss, and evaluates every checkpoint separately. No silent precision change.
- Released data is smaller than the brief's 500-row lower range: full read approved269 and held/rejected240. No padding or unread repair was added.
- OpenRouter/Fable preflight review failed402 on a128,000 max-token reservation; reported cost$0.08916925. Same Pi protocol retry uses subscription OpenAI Astra; no CLI fallback. Scientific protocol/semantic judgment still need review after outputs exist.
