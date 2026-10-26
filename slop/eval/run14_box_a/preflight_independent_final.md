# Final read-only assessment: run14 box A, after the budget decision (reviewer-anthropic)

**Scope.** Read-only, no lease, no commands, no paid calls. I re-read the current `55_run14_box_a_rental.py` and `56_run14_box_a.py`, `budget_decision.json`, `preflight_review_response.md`, `preparation/runtime_budget_checks.log`, and `preparation/training_and_source_parity.log`. I did not re-read `plan.json`, `33_subset_cells.py`, or `preparation/preflight_tests.log`. The first-cell and subset-order checks below are against the code's reorder, not against the file on disk.

## 1. Live auto-bill fields (55 `run()`): correct, with one edge

The bypass is gone. `autobill` is non-zero only when the parent's `auto_billing_confirmed` flag is true and the live account reports `has_billing`, no `billing_failed`, and `autobill_threshold > 0`. The check is then `credit + autobill >= cash_required`, placed before the PUT. With the flag false, the check falls back to prepaid credit alone, which is the conservative branch.

Edge: `account['…']` indexing raises `KeyError` if the API omits a field. That fails before any PUT, so it is safe, and I did not verify the field names beyond the response's claim.

## 2. Thinking-generation removal

- **56:** no thinking code remains. The `--reasoning-parser` flag is gone from the teacher argv, `thinking_heal_prompts` is no longer read, and heartbeat milestones in 55 no longer watch `thinking_heal_failed.json`. Confirmed.
- **19:** the unused `thinking_budget` branch is still present. Nothing in 56 or 33 calls it (`thinking_budget=0`, no `--thinking-budget`), so it is inert. The parent's "no thinking-generation code" is true for 56, not for 19.

## 3. `execution_budget(rows)` arithmetic

Checked against the code and `runtime_budget_checks.log`:
- `steps = ceil(rows × 0.95 × 2 / 4)`. This matches `val_set_size 0.05`, two epochs, and gradient accumulation 4. At 1636 rows it gives 777, the historical count.
- `training = steps/777 × 5617 + 600`. The +600 s is the donor-merge allowance, so the "10 min donor merge" in the stated assumptions is included, though not as its own term.
- `fixed = training + 2 h (projection) + 0.25 h (smokes) + 0.5 h (margin)`. `estimate = fixed + cells × 0.35 h + 1 h` (the serial control-review allowance).
- The drop rule removes only `cells[-1]` when it is `['a14_proj64', 1.5]`. The pop is in place, so `estimate()` recomputes. A second overrun hits the `assert estimate() <= remaining` and stops before training. Confirmed.
- The logged cases reproduce: 1636 rows gives 8.28 h against 13 h remaining, and 2400 rows drops the final cell to 8.66 h against 8.8 h remaining. The 13.04 h rejection also matches. Confirmed.

**Forecast risk, not a bug (unmeasured):**
- Training is linear in steps. The control is token-matched, so compute is closer to tokens. If control rows are short, step count rises while total tokens do not, and the step-linear model overstates time. This is conservative, but unmeasured.
- The projection allowance of 2 h, the 0.35 h per cell, and the 0.25 h smoke allowance are assumed, not measured. The historical 0.35 h cell is from a docstring.
- Setup and base download are before generation. Generation's remaining time is measured from the clock, so setup is correctly subtracted.

## 4. Evaluate ordering, environment forwarding, and sequencing

**Plan order (as coded):** `rewr0.5`, `ctlgen1`, `proj16`, `ctlgen-0.5`, `proj64`, `ctlgen-0.25`, `ctlgen-1`, `proj64×1.5`. This matches the decision. `main()` asserts the first cell is `['rewr', .5]`.

**Reference before training:** `evaluate(adapters, cells[:1], 'reference_before_training.log')` uses only up-adapters, so no control data is used. Later, `33` skips the completed `.done` for that cell. Confirmed. Reuse works only if `33` writes `.done` on success (I did not re-read `33`).

**Environment forwarding:** `evaluate()` passes `RUN9_INSTRUCT_PATH`, `RUN9_DEADLINE_EPOCH`, and `CELL_PREFIX` on top of `os.environ`. `HF_HOME` arrives through the tmux command line. **Defect (unverified):** `PYTHONPATH` is not set for this call. The run10 harness exported `PYTHONPATH="$PWD"` before running `33`/`02_merge`/`19`/`26`. If any of them imports a project package by name, the eval stage fails. Fix: add `PYTHONPATH=str(ROOT)` to the `evaluate()` env. Cheap, and it removes the question.

**Sequencing:**
1. `generate.exit` (≤ 5.5 h).
2. Reference eval, about 0.35 h.
3. `control_review` wait, `max_wait=3600`, counted from after the reference finishes. The window therefore starts about 0.35 h later than before.
4. Training, projection, then the remaining cells.

Approval requires an operator `snapshot` after `control_ready.json` and before the review window closes. That is operator sequencing, not enforced in code.

## 5. Source parity and exact config

- **Config (`training_and_source_parity.log`):** only `dataset_prepared_path`, `datasets`, and `output_dir` differ from the stage-7 config. Confirmed for the training config.
- **02_merge:** identical to the frozen run8 hash. Confirmed.
- **19 and 26:** **not identical** to the frozen run8 hashes (`identical False`). The response says the recorder gained tracing and thinking fields and that thinking-off payloads are "regression-tested", but no payload-equality evidence is in the logs I was given. The baseline `r8_a0_b0` was produced with the old code. Comparability of the new cells against that baseline depends on the thinking-off request body and scoring being byte-equivalent. **Blocking for the scientific comparison, not for spending.** Required proof: one item's thinking-off request body (old versus new 19), and that 26 scoring is unchanged on a fixed answer set.

## 6. Budget decision: code versus parent instruction

- **$35 guard:** still in code (`assert plan['total_reserve_usd'] <= 35`, `RATE = 1.92`, `dph_total <= RATE`). Correct until host selection, as instructed.
- **$45 fallback:** not implemented. Raising the rate or the cap requires a reviewed plan change. This is expected, since the decision says to update the plan after selection.
- **Two-hour recheck loop:** not implemented. `55 run()` is one-shot and creates no lease when no offer passes. Reruns are manual. Operational, not a defect.
- **Traffic reserve:** fixed at `0.8`. The decision asks for recomputation from actual offer rates. At the filter cap `inet_down_cost ≤ 0.005` per GB (unit assumed, not verified), 200 GB inbound and 15 GB outbound give about $1.08. That is about $0.28 above the reserve. At $35 it stays under the cap (about 32.9 to 33.0 total), so not blocking, but it does not follow the parent's instruction. Fix: compute `traffic = (200 × inet_down_cost + 15 × inet_up_cost)` from the chosen offer and include it in `cash_required` and `rental_quote.json`.

## 7. Carried-forward concerns (still in code)

- **Pilot review, 1 h in-lease.** `generate()` waits for `pilot_review.approved.json` with the default `max_wait=3600`, measured from pilot-ready. This is inside the lease, not before it, so it is not the inapplicable pre-lease pilot the parent declined. It is still a hard hour.
- **Control review, 1 h.** As above.
- **Fail-fast on marker or empty teacher replies.** `56 generate()` asserts `not marker_violation` and non-empty output before counting. One such reply ends the lease. Still a cost choice the parent should accept explicitly. With the teacher no longer running a reasoning parser, a stray `</think>` in content is possible but unlikely.

## 8. Verdict

**No launch-breaking code defect in the new mechanics** on the evidence I could read. The live auto-bill gate, the budget guard, and the reference-then-review sequencing are correct as coded.

Concrete defects, in order of importance:
1. **Scientific comparability (blocking for the claim, not for spending):** the 19/26 hash mismatch needs payload-equality evidence before approval (§5).
2. **Eval environment (verify, then fix):** add `PYTHONPATH=str(ROOT)` to `evaluate()` (§4).
3. **Traffic reserve (non-blocking at $35):** compute it from the chosen offer's per-GB rates (§6).
4. **$45 path and recheck loop:** must be implemented or run manually, with a reviewed plan update before any lease above $35 (§6).

Unmeasured runtime risks (not bugs): the step-linear training proxy, the 2 h projection allowance, and the 0.35 h per cell (§3).

PI/Claude-Haiku

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Re-read current 55 and 56, budget_decision.json, preflight_review_response.md, runtime_budget_checks.log, and training_and_source_parity.log. Verified live auto-bill gating, thinking removal, execution_budget arithmetic (1636 rows 8.28 h; 2400 rows drops final cell 8.66 h; too-short rejected), reference-then-review ordering, and the 19/26 hash mismatch. Returned final assessment with concrete defects separated from unmeasured forecast risk."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Read-only. Proof logs inspected as artifacts, not re-executed. runtime_budget_checks.log: PASS arithmetic for two cases plus too-short rejection. training_and_source_parity.log: config differs only in paths; 02_merge identical; 19 and 26 not identical to run8 hashes."
  ],
  "residualRisks": [
    "19/26 source hashes differ from frozen run8; thinking-off payload and scoring equivalence unproven in provided logs (blocks scientific comparison).",
    "evaluate() env lacks PYTHONPATH; eval stage may fail if 02_merge/19/26/33 import project packages (unverified).",
    "Traffic reserve fixed at 0.8 rather than computed from offer rates; ~0.28 under worst case at 0.005/GB cap (unit assumed).",
    "Training time is a step-linear proxy; projection 2 h, cell 0.35 h, and smoke allowances are unmeasured.",
    "Pilot and control review gates are hard 1 h waits in-lease.",
    "Fail-fast on marker or empty teacher replies ends the lease.",
    "$45 fallback and two-hour recheck are not implemented in code; require reviewed plan change or manual rerun.",
    "plan.json, 33_subset_cells.py, and preflight_tests.log not re-read this round."
  ],
  "noStagedFiles": true,
  "diffSummary": "No diff; read-only final assessment.",
  "reviewFindings": [
    "blocker (science, not spend): scripts/eval/19_gen_replies.py and 26_gsm8k.py differ from frozen run8 hashes; thinking-off payload and scoring equivalence proof required before approval",
    "defect (verify then fix): scripts/eval/56_run14_box_a.py evaluate() env omits PYTHONPATH; add PYTHONPATH=str(ROOT)",
    "defect (non-blocking at $35): scripts/eval/55_run14_box_a_rental.py cash_required uses fixed traffic_reserve_usd=0.8; compute from offer inet rates for 200 GB in / 15 GB out",
    "risk: scripts/eval/56_run14_box_a.py generate() pilot_review and main() control_review default max_wait=3600 (in-lease hard hour)",
    "risk: scripts/eval/56_run14_box_a.py generate() assert not marker_violation/empty aborts whole lease",
    "risk (unmeasured forecast): execution_budget step-linear training; projection 2 h; cell 0.35 h",
    "confirmed: live auto-bill check is AND-gated and fails before PUT on insufficient funds",
    "confirmed: execution_budget drops only final proj64 x1.5 and rejects unfinishable core before training"
  ],
  "manualNotes": "Signed PI/Claude-Haiku. Before approval: provide thinking-off payload equality for 19 and scoring equivalence for 26; add PYTHONPATH to evaluate env; recompute traffic reserve from chosen offer; any $45 path needs reviewed plan change."
}
```

PI/Claude-Haiku