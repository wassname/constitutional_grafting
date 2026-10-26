# Independent read-only preflight: run14 box A (reviewer-anthropic)

**Scope and method.** I read every listed source in full, plus `19_gen_replies.py` and `26_gsm8k.py`. I ran no commands and made no edits. Anything marked *inference* is my reasoning from the code, not something I observed. Not read, so unverified: `38_run10_chat_rental.py` (the rental library), `48_vast_deadline.py`, `13_run10_evals.sh`, `box_watchdog.sh`, `configs/train/qwen3/sft.yml`, `41_expert_adapter_check.py`, `spectral_plugin.py`, `historical.py`, `52_answer_panel.py`, and the `run13` plan.

## Launch blockers (observed in code)

**B1. Review gates time out after 1 hour.** `wait_for` defaults to `max_wait=3600` (56 lines `def wait_for(...)`). `generate()` waits on `pilot_review.approved.json` with only `reserve_seconds=6*3600` set. `main()` waits on `control_review.approved.json` with `reserve_seconds=7*3600` and no `max_wait`. If a review is not approved within an hour, the assertion fires. `generate.exit` is then non-zero, and `main()` asserts it equals `'0'`. The lease ends with no control adapter. The plan requires a complete read of the control data, which is unlikely to finish in an hour. Fix: pass an explicit `max_wait` tied to the deadline, and keep heartbeats running while waiting.

**B2. Optional heal generation is fatal.** In `generate()`, the 1000-row thinking heal runs inside the `try` through `command(...)`. Any exception there escapes, `generate.exit` becomes non-zero, and `main()` never trains the control adapter, even though `control_ready.json` already exists. The heal is marked save-only and droppable in the plan. Its failure modes include the vLLM `thinking_token_budget` field, which I could not verify. `19_gen_replies.py` sets it, and the code expects `c["message"]["reasoning"]`. Fix: wrap the heal in its own try/except, log a receipt, and exit 0, or move it after control training.

**B3. The token target may be unreachable.** The control pool is 3700 prompts (`prompt_manifest.json`, `pools.control.rows`). The target is 788606 supervised tokens plus an 8192 margin (`generate()`), so the average finished reply must be at least about 215 tokens. The chatr12 average was 788606/1636 ≈ 482 tokens per row. `generate()` asserts `generated_tokens >= target + 8192` only after all generation has finished, so a shortfall wastes the lease. Inference: `prepare()` uses only `gsm[:3000]` and `gsm[3000:3750]`, so GSM8K train could be extended. Fix: estimate the average from the pilot before committing to the lease, and enlarge the pool.

**B4. Expert-LoRA layout is untested against PEFT, and projection never runs before the paid training.** `unpack_factors` reshapes B as `(out, r, E)`, so the flat index is `r*E + e`. `pack_factors` uses the same convention. `test_expert_packing_keeps_experts_separate` checks only that this convention is self-consistent. It does not check PEFT's real ordering. If PEFT stores `(out, E, r)`, every expert's projection is wrong and nothing detects it, because removed-energy fractions still look plausible. Also, `16_project_chat_adapter.py` runs for the first time at full scale on the GPU, after control training, and `--module-limit` is never invoked. The adapter key mapping is likewise unverified: `parameter_name` assumes checkpoint keys like `…mlp.experts.gate_up_proj`, and `b_index[name]` raises KeyError if the checkpoint stores per-expert keys. Smallest checks, all CPU and no lease:
- (a) Key audit: list the 330 stems from the local rewr adapter, map them with `parameter_name`, and confirm each name is in both `model.safetensors.index.json` files.
- (b) PEFT parity: for one tiny MoE layer built with PEFT `target_parameters`, compare PEFT's own per-expert delta with `unpack_factors` output.
- (c) Move projection ahead of training, or run `--module-limit 2` on the box first.

**B5. The lease is created before local inputs are validated.** `run()` calls `PUT /asks/…` before building the tar. The tar lists `CODE`, `INPUTS`, `target_tokens.json`, and the `control/heal` item files, none of which are checked for existence first. A missing file raises inside the `try`, and `finally` destroys the instance. The loss is minutes of GPU time, but it is avoidable. Fix: check every local path and hash before the `PUT`.

**B6. The core projection cells run last, and there is no per-cell isolation.** The cell order in `plan.json` puts `proj16`, `proj64`, and `proj64@1.5` after the control cells. `33_subset_cells.py` breaks silently when fewer than 1200 s remain. It also has no per-cell `try`, so one failing cell aborts the rest. The plan's priority rule ("drop k64 dose 1.5 first") is not implemented; the code has no switch. Fix: order cells core-first (`proj16`, `proj64`, `ctlgen1`, `ctlgen-1`, `rewr0.5`, then the rest), and wrap each cell.

**B7. Plan and approval disagree.** The parent approved `rewr0.75` only if needed, but `prepare()` hard-codes 8 cells and `plan.json` has no 0.75 entry. Adding it means re-running `prepare` and changing the hashed plan. The plan's step 7 also interpolates using D×1.5 = +0.42, while the parent said to exclude damaged D1.5 from interpolation. The plan text should be made consistent with the approval.

## Substantive issues (observed)

**S1. Held-out exclusion is incomplete.** `heldout_texts()` uses only `items.jsonl`, `panel.jsonl`, and `gsm8k_long60.jsonl`. It skips `boundary_items.jsonl`, `demos.jsonl`, and `pov.jsonl`, which are frozen run-8 inputs. `pov.jsonl` is perspective material and could overlap generic "explain/describe" prompts. Fix: include all `INPUTS` texts, then grep the control and heal pools against them.

**S2. `pack()` can crash after hours of generation.** `90_generic_control.py` `pack` asserts `turn['assistant'].strip() and not turn['marker_violation']`. `generate()`'s running token count does not apply that test, so a single empty or marker-bearing reply makes the final pack fail. Fix: drop and record such rows.

**S3. The control is token-matched but not step-matched.** chatr12 has 1636 rows. The control's row count depends on reply length and is unknown. With `micro_batch_size 1` and `gradient_accumulation_steps 4`, a different row count means different optimizer steps and different Δ norms, so the c = ¼, ½, 1 subtraction is not on a common scale. Report steps, rows, and ‖Δsft_ctlgen‖_F against ‖Δsft_rewr‖_F before interpreting the cells.

**S4. Refusal count is not produced.** The plan requires one; `pack` only drops `length` rows and notes that a complete read is needed.

**S5. Budget guard coverage.** The cash check requires Vast credit ≥ 14×dph + 0.8 + 1 + 1, which is correct for the GPU and traffic reserves. The $2 judge and $2 review reserves are not gated, and `rental_quote.json` hard-codes `+5.8` rather than reading the plan. Whether `dph_total` includes the 500 GB disk is unverified.

**S6. Adapter config hash.** The frozen manifest's SFT config hash is `d17d042…`, but the rewr config hash in `plan.json` is `ba629d…`. The projection asserts depend on the rewr config's keys (`target_parameters`, `rank_pattern`, `alpha_pattern`). Check this locally before the lease.

**S7. Unverified commands and dependencies.** Run `sha256sum` on `scripts/eval/19_gen_replies.py`, `26_gsm8k.py`, and `02_merge.py`, and compare with the frozen `code_sha256` values. Confirm that `38_run10_chat_rental.py` provides `retrieve_outputs` for `box_runs/control_pilot.jsonl`, which `approve-pilot` reads locally, and for the `required_adapters.json` retrieval. Confirm `13_run10_evals.sh prep` creates `/workspace/run10_instruct_path`.

## Uncertain risks

- Replies from `19` carry `finish_reason`, and `pack` drops `length`. Check one chatr12 row against one control row for segment format and trailing `\n`, since `check_loss_mask` does not test this.
- `sft.yml` is not read, so I cannot confirm the control config matches `cfg_r10_cx_chatr12.yml`. Diff the generated `cfg_r10_a14_ctlgen.yml` against it; the only expected differences are paths.
- Time budget: the lease must fit heal, training, projection, and eight eval cells (each with a 67 GB merge, vLLM startup, and evals) inside 12.5 h. I have no run13/run10 timing receipts, so this cannot be checked.
- Matched-effect conclusions rest on 70 items × 2 samples and a judge, with no confidence interval.
- Interpretation: subtracting Δsft_ctlgen removes distilled Instruct style as well as instruction-following. The plan acknowledges this, but the results will not isolate instruction-following.

## Checks that could disprove these findings

- B1/B2/B5: read the `wait_for` default and the `generate()` heal block; check whether any path sets `max_wait` above 3600.
- B3: run the pilot and compute mean supervised tokens per finished reply; compare with 213.
- B4: run the PEFT parity test (b) above; if it matches, downgrade B4 to a missing test rather than a bug.
- S1: grep the frozen inputs against the control pool.

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Read all listed sources plus 19_gen_replies.py and 26_gsm8k.py in full; returned a concise result with launch blockers B1-B7, substantive issues S1-S7, and uncertain risks, with source references."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Read-only review; no commands, edits, paid calls, or delegation. Projection unit log (3 passed) was taken as given and not re-run."
  ],
  "residualRisks": [
    "PEFT expert LoRA ordering is unverified against installed PEFT; projection could silently scramble experts if it differs.",
    "Control token target may be unreachable with a 3700-prompt pool; feasibility depends on the unseen pilot reply lengths.",
    "38_run10_chat_rental.py, 48_vast_deadline.py, sft.yml, and 13_run10_evals.sh were not read; the rental and retrieval behaviour they provide is unverified.",
    "Timing receipts for run10/run13 are absent, so the 12.5 h budget cannot be verified."
  ],
  "noStagedFiles": true,
  "diffSummary": "No diff; read-only preflight review of run14 box A sources.",
  "reviewFindings": [
    "blocker: scripts/eval/56_run14_box_a.py wait_for default max_wait=3600 - pilot and control reviews time out after 1 hour, lease ends with no control adapter",
    "blocker: scripts/eval/56_run14_box_a.py generate() - optional thinking heal exception makes generate.exit non-zero and aborts control training",
    "blocker: scripts/eval/56_run14_box_a.py generate() assert generated_tokens >= target+8192 - 3700-prompt pool may be too small (needs about 213 tokens/reply)",
    "blocker: scripts/train/16_project_chat_adapter.py unit tests - expert B packing order (out,r,E) unverified against PEFT; projection never smoke-run before paid training",
    "blocker: scripts/eval/55_run14_box_a_rental.py run() - lease created before local input validation; missing file destroys instance after PUT",
    "issue: scripts/eval/56_run14_box_a.py heldout - boundary_items/demos/pov not excluded from control pool",
    "issue: scripts/data/90_generic_control.py pack - assert on empty or marker reply can crash final packing",
    "issue: scripts/eval/33_subset_cells.py cell order - core projection cells run last; no per-cell error isolation",
    "issue: plan.json vs parent approval - rewr0.75 absent; plan step 7 uses D1.5 that parent excludes"
  ],
  "manualNotes": "Signed PI/Claude-Haiku. Verify before launch: sha256 of 19/26/02_merge against frozen code hashes; rewr adapter_config hash vs plan; PEFT expert layout parity (CPU); key audit of 330 stems against Base/Instruct indexes; pilot mean tokens per reply; judge/review cost outside Vast cash check."
}
```

PI/Claude-Haiku