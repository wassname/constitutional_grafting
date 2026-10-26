# Follow-up assessment: run14 box A, before any rental (reviewer-anthropic)

**Scope.** Read-only. I re-read `55_run14_box_a_rental.py`, `56_run14_box_a.py`, `90_generic_control.py`, `16_project_chat_adapter.py`, `preflight_review_response.md`, and `preflight_independent_initial.md`. I also read the proof logs under `preparation/` (`preflight_tests.log`, `projection_peft_tests.log`, `checkpoint_key_audit.log`), `prompt_manifest.json`, and `funding_confirmation.json`. Parts of `38_run10_chat_rental.py` and `48_vast_deadline.py` were read in full or near full. Not re-read this round: `33_subset_cells.py`, `plan.json`, `no_robots_prompt_review.json`, `offers_datacenter.json`, and `box_watchdog.sh`. Nothing was run and nothing was edited.

**Preliminary note.** `preflight_approved.json` does not exist yet (ENOENT). That is correct: `run()` requires it, so no lease can start until the parent creates it after this review.

## 1. Confirmed blocking issues

**B-A. The cash check can be bypassed by a static flag.** `55 run()`:
`assert account['credit'] >= cash_required or funding['auto_billing_confirmed']`.
`funding_confirmation.json` sets `auto_billing_confirmed: true` by hand, and its own field `provider_auto_charge_not_independently_exercised: true` says the provider was never tested. So with that flag set, the prepaid-credit check never fires. This does not meet the requirement that the cash check prevent rental on insufficient prepaid credit.
- The fields needed for a live check are present in the provider account object that `38 run()` reads: `has_billing`, `billing_failed`, `autobill_threshold`, `autobill_amount`. `55` reads none of them.
- Fix: make `55 run()` check the live account fields, using `38`'s own logic (`has_billing and not billing_failed and autobill_threshold > 0`, then `credit + autobill_amount - 1 >= cash_required`). Record the observed values in `rental_quote.json`. If the parent accepts the auto-bill risk, that acceptance should be a logged decision, not a boolean in a file the code treats as proof.
- The parent's relayed "vast auto loads fund" permission authorises the spend. It does not make the code guard pass.

**B-B. Pilot and control review waits are hard one-hour windows.** `56 generate()` waits for `pilot_review.approved.json` with `reserve_seconds=6*3600` and the default `max_wait=3600`. `56 main()` waits for `control_review.approved.json` after `generate.exit` with the same default. The response accepts this deliberately. I agree the control window overlaps heal, since the window starts only at `generate.exit`. The pilot window does not overlap anything: if approval is not in place within an hour of `pilot_review` being ready, generation fails and the lease ends. This is a schedule risk the parent has to be able to meet, not a code bug.

**B-C. Time and step budget is unresolved.** The response concedes that row and optimizer-step counts are unknown until the pilot runs. The `38` docstring gives `777` updates ≈ 1.55 h for historical chats and about 9 h for a 9,418-row control. The current control pool is up to 7,423 prompts, so training could run well past 1.55 h. The budget chain is: setup ≈ 1.7 h, heal ≤ 2.5 h, training (unknown), then 8 eval cells at about 0.35 h each, all inside a 12.5 h runner deadline. Eight cells alone are about 2.8 h. This does not fit comfortably without a pilot-based estimate. Before `PUT`, the parent should have the pilot row and token count, and a steps estimate for training. If the run is cut short, `56 main()` asserts that every cell completed, so the lease ends with a nonzero exit.

**B-D. Prior-lease cumulative budget is not checked.** `38 run()` sums earlier lease reserves against `BUDGET_USD` (its comment says run-10 leases share one allowance). `55 run()` does no such check. Its cap is per-run only. The parent must confirm that no unsettled spend from earlier leases sits on this account before any PUT.

## 2. Verified or rebutted (with evidence)

- **Heal failure isolation: correct, narrow.** `56 generate()` wraps only the heal `command(...)` in `try`, catching `CalledProcessError` and `TimeoutExpired`. It writes `thinking_heal_failed.json`, and `heartbeat` reports it. The `assert len(...) == 1000` sits in the `else:` block, so a short output still fails loudly. A failed heal is logged, not silently dropped, and control training is unaffected. It is not an unintended suppression.
- **Full-read gates and overlap.** `approve-control` checks `sha256` and `fully_read_rows` against the local copy. `56 main()` requires `refusal_ids` to be a subset of the control IDs and writes the review hash to the manifest. The response's overlap claim is right for control (see B-B). The no-robots gate is enforced in `run()` through `plan['prompts']['no_robots_review']['all_selected_prompts_fully_read']`. I did not read the receipt file itself.
- **Larger fixed reserve pool: confirmed in code.** `prepare()` builds `control = shuffled(gsm[:3000] + robots[:400] + help[:300])`, then appends `gsm[3750:]`. `heal` uses `gsm[3000:3750]`. These slices are disjoint, and the reserve is consumed only if the first 3,700 are insufficient. The `prompt_manifest.json` shows 7,423 control rows and 1,000 heal rows. The ~107-token average requirement is arithmetic from the manifest; whether it is reachable depends on the pilot.
- **Held-out exclusion: fixed.** `heldout_texts()` now reads `items`, `boundary_items`, `demos`, `panel`, and `pov` (plus GSM60). `change.md` is not included, since it is not JSONL. This is a minor gap.
- **Pre-PUT archive and hash gates: fixed.** `run()` builds the tar before `rental.api('/asks/…', 'PUT')`, so a missing file raises before any lease exists. It checks the controller, `LOCAL_CODE` (38, 48), `CODE`, the prompt manifest, and the plan hash against the approval file. The approval file is not there yet, which is the intended gate.
- **Native expert layout against real PEFT: rebutted my earlier B4.** `test_chat_projection.py::test_expert_packing_keeps_experts_separate` builds a real `ParamWrapper` from PEFT, copies `stored_A` and `stored_B` into it, and asserts `2*(B@A) == wrapper.get_delta_weight('default')`. That is a direct parity test of the packing convention. `projection_peft_tests.log` reports 6 passed, which matches the 3 + 3 tests in the two regression files I read.
- **Checkpoint key audit: rebutted my per-expert key concern.** `checkpoint_key_audit.log` shows `model.language_model.layers.N.mlp.experts.gate_up_proj` and `…down_proj` as keys in both pinned indexes, which are fused checkpoint keys. Caveat: the audit checks index presence and adapter factor shapes, not tensor shapes. Runtime shape asserts in `16` cover tensor shapes.
- **Rank-pattern warning: noted, not a blocker.** `test_rank_pattern_applies_to_experts` asserts the expert A shapes equal `rank*n_experts` for the configured ranks, and that assertion passes. The PEFT warning is about regex key matching, and the production key audit shows expert A rows of 4096 = 256×16, consistent with r=16 on disk.
- **New CUDA filter: confirmed.** `cuda_max_good >= 13.0` is in the `passing` list in `55 run()`.
- **Deadline guard (`48 arm`).** The timer is armed with `hard_destroy_epoch`, which is measured from before the PUT. If arming fails, the exception is inside `try`, and `finally` destroys the instance. `destroy_exact` checks the exact label. Gap: `38 destroy()` runs `sudo -n systemctl disable` after deleting the instance. If sudo fails, the exception skips the closure receipt, though the instance is already gone.
- **Retrieval (`38 _retrieve_outputs`).** It copies `runs/run10/` (excluding merged models), retrieves only `r10_*` adapters (donors are `up_*` and are not retrieved), and verifies sizes and SHA-256 against remote hashes. On retrieval failure it stops the instance and keeps the disk until the hard deadline. Required-adapter checks apply only when `job.exit == '0'`. Behaviour is as described.

## 3. Remaining risks I cannot test

- **Projection smoke coverage.** `--module-limit 5` takes the first five stems in sorted order. For layer 0 that is `linear_attn.in_proj_qkv`, `in_proj_z`, `out_proj`, and both expert banks. It does not cover full-attention `self_attn.{q,k,v,o}_proj` (layers 3, 7, …) or `mlp.shared_expert`. The response's "attention" means linear attention only. Cheap fix: select one stem of each class by name, not by sort order.
- **Fail-fast on anomalous teacher replies.** `56 generate()` asserts `not marker_violation` and non-empty `assistant` on finished replies, before token counting. One such reply aborts the whole lease, with no control data. The response chose this deliberately, so it is a cost decision, not a bug. Recording such rows as anomalies and continuing is an option the parent should weigh.
- **Last cell "expendable".** The response says the last optional cell can be dropped. `33` `break`s only when under 1,200 s remain, and `56` then asserts all cells completed, so the run exits nonzero. Data is retained, so this is not a blocker, but the stated priority is not implemented.
- **Not re-read:** `33_subset_cells.py` (per-cell isolation), `plan.json` (confirm it matches the reordered cell list), `box_watchdog.sh` (the `auth check` marker), and the no-robots receipt.

## 4. Verdict

Not ready to rent. The confirmed blockers are:
1. Replace the boolean cash bypass in `55 run()` with the live auto-bill check (B-A).
2. Confirm no unsettled prior-lease spend on this account (B-D).
3. Produce a pilot-based row, step, and time estimate that fits the 12.5 h runner deadline before `PUT` (B-C).

B-B is a schedule risk the parent must be able to meet. Everything else in the response is confirmed or rebutted by the evidence above.

PI/Claude-Haiku

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Re-read current 55/56/90/16 sources, preflight_review_response.md, preflight_independent_initial.md, preparation/ logs, prompt_manifest.json, funding_confirmation.json, and 38/48 rental/guard functions; returned final read-only assessment with confirmed blockers, rebutted items, and residual risks. No commands run, no paid calls, no edits."
    }
  ],
  "changedFiles": [],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Read-only; proof logs inspected as artifacts, not re-executed. preparation/preflight_tests.log: 24 passed, 7 subtests passed. preparation/projection_peft_tests.log: 6 passed. checkpoint_key_audit.log: PASS 330 stems in both pinned indexes. preflight_approved.json absent (ENOENT), as intended."
  ],
  "residualRisks": [
    "Cash gate in 55 run() is bypassable by static funding_confirmation.json flag; live auto-bill fields not checked.",
    "Pilot and control review waits are one-hour windows (default max_wait=3600).",
    "Row/step/time budget for control training not estimated before rental; 12.5 h runner deadline at risk.",
    "No check of cumulative prior-lease reserves in 55 (38 has it).",
    "Projection smoke (--module-limit 5) does not cover self_attn or shared_expert stems.",
    "Fail-fast on marker/empty teacher replies aborts the whole lease.",
    "33_subset_cells.py, plan.json, box_watchdog.sh, and no-robots receipt not re-read this round."
  ],
  "noStagedFiles": true,
  "diffSummary": "No diff; read-only follow-up assessment only.",
  "reviewFindings": [
    "blocker: scripts/eval/55_run14_box_a_rental.py run() - cash assert uses 'or funding[auto_billing_confirmed]' static flag; replace with live account auto-bill check per scripts/eval/38_run10_chat_rental.py run()",
    "blocker: scripts/eval/55_run14_box_a_rental.py run() - no cumulative prior-lease reserve check; confirm account has no unsettled prior spend before PUT",
    "blocker: runs/run10 pipeline timing - control training row/step/time not estimated before rental; must fit 12.5 h runner deadline with heal up to 2.5 h and 8 eval cells",
    "risk: scripts/eval/56_run14_box_a.py wait_for default max_wait=3600 on pilot_review (generate) and control_review (main) - one-hour approval window",
    "risk: scripts/train/16_project_chat_adapter.py --module-limit 5 smoke excludes self_attn and shared_expert stems",
    "risk: scripts/eval/56_run14_box_a.py generate() - marker/empty teacher reply asserts abort whole lease",
    "rebutted: expert packing vs PEFT - test_chat_projection.py compares 2*(B@A) to real ParamWrapper.get_delta_weight; log shows 6 passed",
    "rebutted: per-expert checkpoint keys - checkpoint_key_audit.log shows fused experts gate_up_proj/down_proj in both indexes",
    "rebutted: pre-PUT archive - run() builds tar before PUT; hash gates present",
    "confirmed: heal failure isolation narrow (CalledProcessError/TimeoutExpired); assertion failures stay fatal",
    "confirmed: CUDA>=13.0 filter present in 55 run()"
  ],
  "manualNotes": "Signed PI/Claude-Haiku. Do not create preflight_approved.json until the cash-gate and prior-lease blockers are fixed and a pilot-based time/step estimate exists. Verify before PUT: current plan.json matches reordered cells; 33 per-cell behaviour; no-robots receipt hash f8346b...."
}
```

PI/Claude-Haiku