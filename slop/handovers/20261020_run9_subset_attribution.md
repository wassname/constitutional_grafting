# Handover: run 9 subset LoRAs for data attribution (2026-10-20 15:10 Perth)

-- PI/Claude (Opus 5.5), for the next agent (Sol 6.1)

## What wassname wants (his words, spelling corrected)

- Simplify to the document graft (+spectral, +heal later). Not more SFT, RL, Echo, cwsteer.
- One LoRA per data subset (Opus→Echo good seeds, pure Stoic, expanded Opus, Greek round trip; 100–300 docs each) and **an eval of each subset LoRA for data attribution**: which data makes good character?
- "we got some clues from the good demos so far and how they link"; "we have constitution. interested in grading". The real goal is a **striking demo** (baby_eating_aliens, escaped_starwisp, identity) that we can trace to data.
- Budget: $50 Vast, $30 Opus/API (batch mode). Use the task list. Show results in busy format with files, plots, demos and a spend ledger.

Do NOT: redesign the corpus, add new training stages, start a new rental, or re-litigate the method. The run is already in flight; the remaining work is to **collect, judge, read and report**.

## Continuation decisions (PI/Sol, 15:30 Perth)

- User approved another $30 for judging/API: total run-9 API allowance $60, Vast remains $50. `slop/eval/run9/judge.py` includes the previously omitted GLM costs and a $17 reserve for batch costs/retries absent from per-row cost records. This is conservative accounting, not an invoice.
- Spectral training now defaults to λ=50 in the actual plugin (commit d3298bb); the callback regression checks unset, explicit 50 and explicit 0. The running box already explicitly uses 50 and was not changed.
- Completed cells are downloaded early to `slop/eval/run9/box_runs/`; singleton k=1 judging has started. Continue reading the fixed panels while later cells run, rather than waiting for the box to finish.
- Interpretation corrections: singleton + leave-one-out coalitions do not supply exact Shapley values (pair coalitions are missing). Opus/Greek share candidate seeds but their selected training rows differ; this is not an isolated language-round-trip effect. Two generation samples do not measure judge error or training-seed variation.

## State at handover

| item | state | where |
|:--|:--|:--|
| 4 subsets + joint, reviewed | done, equal exposure ~55.7k tokens each | `data/subsets/train_*.jsonl`, `data/subsets/train_manifest.json` |
| full reads | done (kimi-k3 chunks) + GLM judge on opus/greek | `slop/reviews/20261020_subset_full_read/` , `data/subsets/judge_*.jsonl` |
| 5 LoRAs trained (echo, stoic, opus, greek, joint), spectral λ=50, run-7e recipe | done on box | box `/workspace/cg/outputs/r9_*` |
| coalition cells (merge into untouched Instruct, vLLM gen, tiny-char items, demos, GSM8K long60) | 13/19 done at 15:05 | box `/workspace/cg/runs/run9/`, log `slop/eval/run9/controller.log` |
| remaining cells | 2 leave-one-outs (−opus, −greek), then 2×energy dose for each subset | ~15–20 min each, est. done ~17:00 Perth |
| download + destroy | automatic in controller `proc_6ce6`; outputs → `slop/eval/run9/box_runs/`, adapters → `~/.local/share/cg_run9_adapters` | independent destroy cutoff task `task_mvg0dcsy_l8vz2q` 19:35 Perth |
| judging (Jev) | NOT run | `slop/eval/run9/judge.py` |
| report | NOT written | target section in `docs/results/20261017_spectral_heal.md` |

Cells: `k=1` singletons and joint; `kE` = singleton at energy matched to incumbent run-7e graft (E=9.7944; echo 1.58, stoic 1.65, opus 1.56, greek 1.46, joint 1.24); full 4-mix; 4 leave-one-outs; `2×kE`. Control = run 8 `r8_a0_b0` (untouched Instruct, already judged).

Instance 56819164, $1.844/h, created 09:32 Perth. SSH: `ssh -i ~/.ssh/id_vast -o BatchMode=yes -o UserKnownHostsFile=.local/run9_known_hosts -p 26238 root@154.59.156.27`.

## Spend ledger (approx.)

- API: opus sync pilot $1.31 + batch $2.82; greek sync $1.56 + batch $4.50 + translation $4.21; GLM judge $1.84 + $1.77 → **≈$18 of $30**. Jev judging must fit the remaining ~$12 (judge.py tallies; check its `api_spent()`).
- Vast: ≈ $1.844/h × ~7.5 h ≈ **$14 of $50** if destroyed ~17:00.

## Tasks for you, in order (each has a check)

1. [ ] **Wait for controller `proc_6ce6` to exit**; verify instance destroyed (`vastai show instances` empty or `slop/eval/run9/destroy_response.json`) and `box_runs/` has replies for 19 cells.
   - failure mode: controller exits early and the box keeps billing. Check: destroy response exists.
2. [ ] **Judge** with `slop/eval/run9/judge.py` (Jev, same items/change.md/protocol as run 8, so run-8 numbers are comparable). Stay under the API cap.
   - failure mode: judging a different item set than run 8 → not comparable. Check: item hashes match `runs/run9/run8_manifest.json`.
3. [ ] **Read the demos yourself**: baby_eating_aliens, escaped_starwisp, "Who are you?", "What's your name, and who made you?" for every cell (`scripts/eval/17_demo_panel.py` format, base→cells in order, mark missing "not run"). Quote the best and worst verbatim. This is the deliverable wassname cares about most.
   - failure mode: reporting judge scores while the demo text is incoherent or virtue-signalling. Check: you quote the actual replies.
4. [ ] **Attribution table**: per cell, character change (Jev) and GSM8K/task success; singleton vs leave-one-out contributions (Shapley-style from the coalition cells). One plot: character vs capability per subset at k=1, kE, 2kE. Look at the png and get a fresh-eyes check.
   - failure mode: differences inside judge noise called real. Report the r8_a0_b0 2-sample spread as the noise reference.
5. [ ] **Report**: results section in `docs/results/20261017_spectral_heal.md`, journal entry in `RESEARCH_JOURNAL.md`, update goals file `.pi/goals/ad3e95-v7.md` (goal 2 corpus → evidence, goal 3 → which subset gives better graft), commit, busy-format message with paths and spend.

Methods notes: `slop/research/20261020_data_attribution_methods.md` (removing an update ≠ retraining without the data; equal coefficients). Preferences brief: `slop/research/20261020_wassname_preferences_brief.md`.

## Known caveats to state in the report

- Data reads were by kimi-k3 reviewer chunks + GLM judge; the main agent read samples and every flagged item, not all ~500 texts.
- Subsets were reduced to ~55.7k tokens each (stoic was the limit after removing defective extractions), smaller than the 85k first planned.
- First echo run with the pre-review file and in-train demo plugin was aborted (337 s/step); retrained on reviewed data without in-train demos.
- Greek subset = Opus writing in Modern Greek, DeepSeek v4 pro translating back; same 131 seeds as opus subset, so opus vs greek isolates the round trip.
