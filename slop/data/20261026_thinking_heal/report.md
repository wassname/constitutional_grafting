# Thinking-heal preparation: final quarantined candidates

Preparation only: **no GPU, training, D answers or training approval**. This continues the prior Sol worker's on-disk preparation; inherited receipts are not claimed as new reads. Historical signed pilot/selection/review artifacts remain intact. New/updated artifacts are signed below.

## Generation and accounting

The parent ran the sole authorized embedded-provider-error retry pass, exiting 0 after 185 seconds:

```sh
uv run --env-file .env python scripts/data/92_thinking_heal_data.py generate --limit 600 --workers 6 --retry-provider-errors > slop/data/20261026_thinking_heal/generation_provider_retry.log 2>&1
```

There are 600 logical prompts, 663 generation attempts plus one cheap independent pilot review (664 raw records). All 17 zero-cost embedded provider failures received a new attempt ID in this pass; no further provider-error pass was run. The native teacher remains Qwen3.5-35B-A3B Instruct via pinned DeepInfra fp8, not Base or a silently substituted provider.

- Reported API cost, including review and all attempts: **$1.112454195**.
- Conservative ledger: **$1.216868395**, below the $5 preparation cap. The five legacy 429 reservations remain charged: **$0.104414200** total. No outstanding reservations remain.
- **45** body-confirmed pre-generation 429s are reconciled as unbilled, with evidence hashes and original reservation bounds retained. Four logical prompts exhausted their three 429 attempts; these are not retried by the provider-error pass.
- Free `GET /api/v1/key`, 2026-10-26T11:40:32Z: usage **1127.296137088**, versus **1126.262497368** in `key_usage_now.json` (10:10:10Z), delta **$1.033639720**. Task-reported cost increased **$0.957449760** between those receipts. The **$0.076189960** difference is unattributed shared-key traffic/metering timing, not an isolated task invoice. See `key_usage_delta.json`; receipts contain usage fields, not credentials or key hashes.

## Candidate disposition

`trace_candidates.jsonl` contains **509 quarantined candidates**, not a released training set. It omits all known defects rather than merely annotating them. `build_manifest.json`, `summary.json` and full-native packets retain rejection evidence.

| Source | Selected | Kept candidate | wait >=8 filter | Held repair | Semantic reject | Error/incomplete |
|---|---:|---:|---:|---:|---:|---:|
| GSM8K train | 450 | 387 | 52 | 3 | 2 | 6 |
| No Robots train | 90 | 75 | 12 | 3 | 0 | 0 |
| Original ordinary help | 60 | 47 | 10 | 2 | 1 | 0 |
| **Total** | **600** | **509** | **74** | **8** | **3** | **6** |

The six failures are four exhausted upstream 429s (`gsm_train_1802`, `2464`, `2468`, `4466`) and two finish=length responses (`gsm_train_5328`, `868`). No latest embedded provider error remains. There are 594 format-complete pairs. Rejection groups are disjoint: 91 not kept in total.

Eight fully read targets are held for whole-pair repair/regeneration: four native `cw` noise artifacts; three factual/technical defects (GNU find wording, vowel-run examples, AutoHotkey v2 syntax/API); and one faulty geometry/integer-answer reasoning trace. All originals remain untouched. No additional repair API calls were made. Three full-read semantic rejects escape the lexical filter: `gsm_train_5065`, `ordinary_6_11` and the successful `gsm_train_3033__attempt_2`.

### Does the wait filter keep only short/easy prompts?

Lengths below use the pinned local tokenizer, not provider reasoning-token estimates. Quantiles use sorted index floor((n-1)*q), as implemented in `summarize`.

| Group | n | Prompt median / mean | Reasoning p25 / median / p75 / p90 | Reasoning mean / max | Final median |
|---|---:|---:|---:|---:|---:|
| Kept candidates | 509 | 53 / 63.5 | 690 / 962 / 1353 / 2339 | 1213.1 / 4916 | 192 |
| wait-filter rejects | 74 | 63 / 77.9 | 3478 / 4232 / 4916 / 4916 | 4097.4 / 4916 | 239 |
| All rejects/holds | 91 | 63 / 77.0 | 3192 / 4104 / 4916 / 4916 | 3798.0 / 4916 | 243 |

The rejected/held reasoning distribution has n=87: four 429s returned no trace. The filter clearly selects **much shorter reasoning**, with only a modest shift in prompt length. Retention is 86.0% GSM, 83.3% No Robots and 78.3% ordinary help. It is **not evidence of easier tasks**: difficulty was not measured, and even a two-sentence thank-you request induced severe rechecking. Fifteen kept traces still have 4916 reasoning tokens; no maximum-length filter was added. Concentration at 4916 is observed, not proof of a provider reasoning-budget policy. Lexical pass is neither brevity nor semantic quality approval.

## Full reads and handoff packets

All 600 neutral prompt-side reads are inherited from the prior worker. The fixed 6+30 response sample is now complete: **36 complete full-pair reads** (30 inherited, six completed here). Each read note is bound to its actual attempt ID and response hash. `gsm_train_3033` preserves its original failed-transcript read separately and records the successful retry afresh: the conventional final 1200 feet is correct, but native thought repeatedly reopens the same multiplier interpretation and incorrectly calls a shared destination spatially impossible. It is rejected as a reasoning-style teacher, not rescued by its final.

Of the 36 read pairs, 20 remain candidates, eight are held repairs, five fail the wait filter, and three are semantic rejects. Therefore:

- **489 retained candidate replies still require full reads before any of them can train.**
- Across the entire audit population, 558 format-complete pairs remain unread; 564 logical latest responses are not marked complete full-pair reads, including six failed/incomplete responses. Already rejected traces do not need acceptance reads to stay rejected.
- The **300 D thinking-off replies have not been generated**; every one will also need a full read after an approved GPU lease.

Give readers `reader_assignments.json` and its indexed **120 five-row files**, `reply_batches/batch_000.jsonl` through `batch_119.jsonl`. Five-row packets replace the original oversized 60-row packets; the largest is about 206 KB. Each includes the source seed, exact API request, entire native response, attempt ID, constructed native-template candidate (or null on failure), and disposition. The assignment index lists unread retained IDs separately from audit-only rejects/errors and hashes each packet. Parent owns reader allocation. Record semantic findings in `response_read_notes.json`, bound to attempt/hash, then rebuild; sample reads never approve unread rows.

## CPU validation and scope

- `uv run python -m unittest discover -s tests/regression -p test_thinking_heal_data.py`: **13 tests pass**, using the actual cached tokenizer and actual builder. Tests cover native thinking/off templates, token-exact labels, empty-think exclusion, concurrent persistence/resume, budget cap, bounded 429 retries, body-confirmed accounting, one explicit zero-cost provider-error retry, stale-attempt read receipts, and semantic-hold exclusion/full-native batching.
- `uv run python scripts/train/check_loss_mask.py slop/data/20261026_thinking_heal/trace_candidates.jsonl`: **pass**, no loss on empty think blocks.
- `python -m py_compile scripts/data/92_thinking_heal_data.py tests/regression/test_thinking_heal_data.py`: **pass**.
- A ResourceWarning originates in the existing loss-mask checker's unclosed input handle; its assertions pass. That out-of-scope file is unchanged.

The builder reconstructs native Qwen boundaries from API-separated nonempty reasoning/final channels and finish=stop; it cannot certify literal provider-emitted closer/EOS token IDs. Public pretraining overlap is unknown; these are replay candidates, not held-out reasoning results. The earlier cheap review's claims and checked resolution remain in `review.md` and `review_resolution.md`; no new judge or generation prompt was introduced here. Independent implementation acceptance review remains the parent's review gate.

## GPU heal plan and estimate (not run/leased)

See `training_eval_plan.md` for the full contract. D is `theta_I + Delta_docs + 1*Delta_sft_rewr|docs`, id `r10_stoic0.5_const1_other1_cx_chatr121`. Freeze this merged D at the same precision as its control; add removable rank-8 spectral-regularized heal LoRAs, one epoch with quarter/half/full early checkpoints. Compare traces-only with mixed neutral traces + D's own thinking-off replay, targeting equal assistant-token budgets rather than equal row counts. Optional D-to-healed-D forward KL on off-mode prefixes only is first to omit if memory/time fails. No new character donor is trained directly on Instruct.

The current 509 candidates contain **747,103 supervised assistant tokens** before further semantic rejects; mixture size must be recalculated after reads and D replay. Native trace closers/final/EOS earn loss; D replay's empty off-mode think block does not. Never truncate away the boundary.

Evaluate untouched Instruct, unhealed D and early/final heals in **both thinking modes** using the run13 recorder: blank visible finals, closer-before-EOS, loops/cutoffs, visible-final character under pressure, maths, ordinary help, and actual fridge tool actions. Read raw/answer panels and the fixed full demo panel. Recovery of completion without D's off-mode character is a failure.

Planning estimate: **3–6.4 GPU-hours**, with a hard **six-hour maximum** (slow endpoint requires early stopping), one suitable 80–96 GB GPU; 96 GB/proven offload is preferable because ~70 GB frozen weights plus activations can exceed 80 GB. Reserve <=$2/hour, $4 judging and $1 storage/transfer. Using the conservative prep total, six hours costs at most **$18.216868395 all-in**; hard ceiling remains **$20**. Live quote and explicit lease decision are still required. Measure throughput/memory over 20–50 steps; shorten/stop rather than exceed the remaining cap or drop character evaluation. No GPU work is authorized by this preparation report.

-- PI/Sol (heal prep 2)
