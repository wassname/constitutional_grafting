# Run13 thinking-on preflight review (read-only)

Reviewer: reviewer-anthropic. Scope: `scripts/eval/53_run13_thinking_rental.py`, `54_run13_thinking_box.py`, `19_gen_replies.py` (as on disk after the parent's mid-run edits), helpers `38_run10_chat_rental.py`, `48_vast_deadline.py`, `scripts/train/02_merge.py`, `13_run10_evals.sh`, `box_watchdog.sh`, plus the old merge receipts and thinking-off reply files the plan points at. No shell, no API calls, no edits. Per parent steering, concluded with blocking concrete issues only; non-blocking items are listed briefly as residual risks.

## Blocking

### B1. One remaining per-sample `assert` in `19_gen_replies.chat` still aborts the whole lease job
Observed (`scripts/eval/19_gen_replies.py:50`):
```
assert close_positions or (not text and c["finish_reason"] == "length"), "final without reasoning boundary"
```
The multi-`</think>` assert was removed, but this one remains. It fires for any sample where no `</think>` id was generated and the request did not end with `finish_reason == "length"`. Realistic triggers for D/H (chat adapters trained thinking-off, now served with `enable_thinking=True`):
- model emits EOS inside the think block before the 4096 budget → `finish_reason="stop"`, content `None` → `text==""` → assert fails;
- parser returns content with no `</think>` id (e.g. if the native budget processor terminates reasoning with a different id sequence, or the parser treats a no-`<think>` output as content).

Consequence chain (observed in code): `ex.map` raises → `with ThreadPoolExecutor` exits via `shutdown(wait=True)` so all already-submitted requests still run to completion with nothing written, then the process exits non-zero → `54:command()` has `check=True` → `cell()` raises → `main()` stops; no later cells (D/H/GSM/E) run. "No rescue or retries" means one anomalous sample ends the paid run.

Evidence this model family produces boundary anomalies: the exact H model emitted a stray `</think>` in 2/140 thinking-off rows (`slop/eval/run12/run12gen/judging/initial/replies.jsonl:445,484`, e.g. line 484 `"...not the same as a life of virtue.\n</think>\n\nNeither. ..."`, `marker_violation: true`). D and A had 0/140. The multi-close case is now tolerated, but the inverse (no close) is the same class of off-distribution behaviour and is still fatal.

Fix (small): replace the assert with a recorded flag (e.g. `boundary_missing=True`, keep `reasoning_end_cause="no_boundary"`), leave the row in, keep the raw trace. Test `test_final_without_native_boundary_fails_after_recording` in `tests/regression/test_reply_recorder.py:69` currently pins the aborting behaviour and must change with it.

Disproof: show a vLLM 0.31 guarantee that with `--reasoning-parser qwen3` + `thinking_token_budget`, every non-`length` completion contains the `</think>` id. I could not verify that; the smoke test does not cover "EOS inside thinking".

### B2. Prepare evidence is missing; the plan the run depends on does not exist on disk
Observed: `slop/eval/run13_thinking/` contains only `offers.json` and `prepare.log`; `prepare.log` is one line, `LOCAL ADAPTER VERIFIED stoic`. No `plan.json`. `results.md` marks "Verify every source adapter, original fp16 merge order and frozen item matrix" as `[/]`.
`run()` does `json.loads((OUT / 'plan.json').read_text())` first, so it fails safe, but the parent's statement that adapters/receipts were verified is not evidenced. Either `prepare` stopped at `other`/later (hash mismatch, missing receipt key) or stdout was captured elsewhere. Need: full `prepare` output showing all six `LOCAL ADAPTER VERIFIED` lines and the written `plan.json` (including `previous_merge_receipt_sha256` and the 140-row thinking-off source asserts). The inputs I could check look consistent (stage1/stage7/run12 receipts have the expected keys; all six adapter dirs exist under `~/.local/share/...`; old receipts for D/H/E show `dtype float16`, `groups {}`, order stoic 0.5 → const 1 → other 1 → chat, matching `models[*]['cell']`).

## Not blocking, but should be known before spending (short)

- **Maths phase re-merges D/H (and E) and restarts vLLM** (`54:cell()` builds `merged_model` per `(label, phase)`). GSM60 is 60 × 1 greedy requests (minutes); a 70 GB fp16 merge + eager vLLM start is ~20–30 min each. That is roughly 45–75 min of a 5 h lease spent on re-work and is the main reason E likely will not fit. Running GSM in the same server session per cell preserves the data and costs less time; the stated priority (all primary before any GSM) is the parent's call.
- **Teardown margin is 600 s** (`53:119`, runner deadline = hard − 600; `48` guard destroys at hard). Worst case (job killed at runner deadline) leaves <9 min for `shutdown_diagnostics` + rsync of `runs/run10/` (wire traces with full token-id arrays, vLLM logs). 38 used 30 min + a 4400 s eval stop. Also `54:main()` only stops starting maths cells when <1000 s remain, which is less than a merge+start, so a last cell can be started that cannot finish.
- **Smoke test is the only gate on vLLM 0.31 field names/semantics** (`message.reasoning`, `choice.token_ids`, `thinking_token_budget`, forced close within ±1 of budget). I could not verify these against the 0.31.0 source. A failure costs setup (~1 h ≈ $2) not the cap. Smoke `normal` also asserts `row['thinking']` truthy (`54:smoke`), which kills the run if Instruct returns empty reasoning for "What is 2+2?"; `is not None` would be safer.
- **Merge reproduction** checks sha/scale/dtype/groups only; `layer30.rel_delta_fro` from the old receipts is available and could be compared for equality to the new `merge_report.json` as a free reproduction check.
- **Cost accounting**: `provider_closure_verified.json` writes an elapsed×rate estimate; no `/users/current/` credit after destroy. Also run13's quote lives under `slop/eval/run13_thinking/lease`, so 38's cumulative run-10 reserve sum will not see it (likely intended; note it in the journal). Cap arithmetic itself is fine: 5 × 1.845 + 2.6 = 11.825 ≤ 15; `dph_total` includes 300 GB storage per the query.
- **History/judging**: final-only history is implemented as stated; an `empty_final` turn feeds an empty assistant message to later turns (documented regime). GSM parse regex matches `26_gsm8k.py` and is applied to the visible final only; record `pred is None` separately from wrong answers.
- Teardown path otherwise checks out: `rental.OUT/STATE/LABEL/ADAPTER_DIR` overrides are picked up by `destroy()`/`_retrieve_outputs()` (module globals), empty expected-adapter set matches an empty `r10_*` glob, the guard timer is disabled from `rental.OUT`, retrieval failure stops (not destroys) the box and the systemd guard still destroys at the cap. The new create→state/lock write failure path now deletes the exact instance.