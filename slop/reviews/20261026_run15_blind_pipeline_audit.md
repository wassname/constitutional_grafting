# Run15 blind pipeline audit

**Result:** Three interpretation hazards found; no demonstrated mask, expert-layout, or final-channel substitution bug. These are not evidence that healing failed.

Paths below are repository-relative. `BOX` denotes `slop/eval/run15_heal/lease_retry/box_runs/`.

## 1. Matched assistant tokens do not isolate replay’s effect

**Observed:** `scripts/data/93_heal_training.py:70–93` matches total labelled tokens, describing “Matched total assistant-token budget.” The production logs confirm 320,279 versus 320,306 supervised tokens. However:

- `BOX/train_r10_heal15_trace.log:271`: “Maximum number of steps set at 68”.
- `BOX/train_r10_heal15_mix.log:271`: “…116”.
- Their calibration lines, respectively `:484` and `:483`, fix spectral coefficients at **0.339** and **0.977**.

Both configs use unpacked microbatches of one row, accumulation four, one epoch, and the same peak learning rate. Mixed therefore receives approximately 71% more optimizer steps, a different schedule in absolute steps, half the trace exposure, teacher-answer replay, and a different regularization coefficient.

**Inference:** A trace–mix difference cannot establish that replay preserves character, independently of optimization exposure and regularization. This affects every comparison between those adapters, including quarter-epoch checkpoints. Exact per-token gradient weighting remains unverified because the installed Axolotl/CCE loss-normalization implementation was not supplied.

**Strongest contrary evidence:** Token matching is real: final logged supervised totals agree with the manifest. The manifest explicitly says half traces plus half replay and identifies replay as teacher targets—not D generations. This is a legitimate recipe comparison if described narrowly.

**Cheapest discriminating check:** First inspect installed loss normalization and reconstruct cumulative learning-rate exposure from existing logs. Existing checkpoints can provide a rough step-matched sensitivity comparison, not a clean ablation. Definitive attribution requires matching optimizer schedule and regularization while holding the trace subset fixed.

## 2. Thinking-on also changes the available final-answer budget

**Observed:** `scripts/eval/19_gen_replies.py:26` requests `max_tokens + thinking_budget`; it never imposes a separate final-token limit after early closure.

Direct example: `BOX/replies_r15_D_on.jsonl:140`, `long_story`, sample 1, records:

> `"original_answer_cap": 2500`  
> `"thinking_tokens": 2348`  
> `"final_generated_tokens_including_stop": 4247`  
> `"requested_max_tokens": 6596`

Thus the visible answer exceeds the nominal answer cap by 1,747 tokens. Its final contains extensive repeated “Wait…” passages and ends with `finish_reason: "length"`.

**Inference:** On/off differences combine reasoning, additional total compute, and additional possible visible-answer length. Moreover, within thinking-on, earlier closure leaves more capacity for final output, so truncation/loop counts are coupled to closure timing. This affects all thinking-on items, especially long or looping answers.

**Strongest contrary evidence:** The generator explicitly labels the regime `"thinking-on-plus-extra-compute"` (`:86`), retains failures, and records the relevant token counts. This is not a hidden protocol change or evidence of parser leakage.

**Cheapest discriminating check:** Using saved token IDs, count finals exceeding each original cap and calculate cap-matched sensitivity summaries. Truncating stored finals is only a sensitivity analysis—particularly for multi-turn histories—not equivalent to regenerating under an enforced final cap. If conclusions survive removal of this budget advantage, the concern weakens.

## 3. Native acceptance is not numerical validation of the trained intervention

**Observed:** `scripts/eval/57_run15_heal.py:373–377` tests adapters using “What is 2+2?” and logs “all expert/dense adapters accepted.” Every entry in `BOX/adapter_smoke.json` answers `"4."`, including unhealed D. That cannot establish adapter application or numerical equivalence.

There is also an explicit parent mismatch: training uses frozen BF16-rounded D (`:54`, `:265`); `BOX/server_r15_D.argv.json` serves FP16 D. Production numeric records contain `"actual_trainable_changes": null`; exact before/after checks are enabled for the tiny smoke, not production.

**Inference:** All healed outputs demonstrate behavior of the deployed FP16-parent/native-adapter combination, not necessarily behavior of the BF16 training model. A discrepancy could arise from parent rounding or inference implementation; neither is demonstrated here.

**Strongest contrary evidence:** Production B norms grow from zero; saved expert checks report all 80 wrapper B tensors nonzero and all adapter tensors finite. Native expert reshaping in `slop/research/20261026_vllm031_source/model_manager.py:982–1003` agrees structurally with `scripts/train/spectral_math.py`’s expert-major A/interleaved B layout. The regression test checks PEFT reload/merge parity, but not vLLM parity.

**Cheapest discriminating check:** Compare fixed-token logits with adapter enabled/disabled, then native versus PEFT on the **same FP16 parent**. Separately compare BF16 and FP16 parents with the same adapter. Agreement would substantially disprove this implementation concern. Startup and identical easy answers do not.

## Read coverage and remaining uncertainty

Read completely: root `AGENTS.md`; `ml-debug/SKILL.md`; requested scripts; additionally `92_thinking_heal_data.py`, `heal_plugin.py`, `check_loss_mask.py`, `41_expert_adapter_check.py`, `coherence_metrics.py`; all four named heal regression files; all five native Python snapshots; `BOX/run.md`, both production training logs/configs, numeric/timing files, final expert checks, tiny numeric/expert checks, mask logs, smoke JSONs, stages log and D server argv. Raw reply coverage: complete row 140 from D-on, trace-on and Instruct-off only.

Not independently verified: full raw/wire matrices, dataset-wide token masks, installed training libraries, judge outputs, checkpoint bytes/hashes, native logits, tiny training log, or repository diff/HEAD. No commands, tests, mutations, paid calls, or excluded documents were used.

**Currently interpretable:** stages receipts report complete 140-row D and trace matrices in both modes, and mixed-on completion at 18:41:12; mixed-off remains unavailable. Together with reused Instruct, these support conditional, within-regime deployed-recipe comparisons after matrix verification—not replay-only causality, equal-compute on/off claims, or demonstrated numerical parity.