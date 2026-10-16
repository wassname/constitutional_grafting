# Overnight handover: run 7d + debugging (PI/Claude, 2026-10-16 19:40 Perth)

wassname went to bed: "can you keep trying to debug and check your results until good". Spend cap this round ~$10 (box ~$1.74/h Texas, bandwidth $0.0027/GB).

## Running
- Box vast 56236491, ssh alias `cg7d` (ssh3.vast.ai:29304). Runner `/workspace/runner.sh`: setup (done) -> wait for 3 adapter hashes -> `bash scripts/train/10_run7_box.sh effdose2`. Log `/workspace/run7d.log`; gens in `/workspace/cg/runs/{replies,demos,panel}_r7.jsonl`. Heartbeat task run7d-heartbeat every 90 min; watchdog stops box after 3 h without heartbeat.
- Upload process (local) of q6_sft, q6_graft_docs_spl0.5, q6_graft_docs (each ~4 GB) to cg7d; slow (~2.7 MB/s).
- effdose2: models r7d_sft (bf16), r7d_sft16 (fp16 control, same weights), then r7d_{spl,plain}_x{0.0625,0.125,0.25,0.5,0.75,1}, all merged/served in fp16 (MERGE_DTYPE), 4 samples, base_model r7d_sft.

## To do when gens finish
1. Pull runs/*.jsonl to slop/eval/run7d/; judge all vs r7d_sft with tiny-char (worktree ~/.local/share/tiny-character-2d69739, recipe in goals Resources) as run r7d.
2. Checks (ml-debug): (a) r7d_sft16 vs r7d_sft should be ~0 character and same capability (else fp16 inference is a confound); (b) merge reports `runs/merge_gen_r7d_*_x*.log`: rel_delta should scale linearly with k per module (fp16 fidelity); (c) read 2-3 transcripts at the best low-k points.
3. Plot: `scripts/eval/25_dose_frontier.py slop/eval/run7d/dose_frontier r7d:MODEL:GRAFT:K ...` (+ r7d_sft as k=0 for both grafts). Look at the png; fresh-eyes subagent describes it.
4. Destroy box (DELETE /api/v0/instances/56236491/, VASTAI_API_KEY in .env), cancel heartbeat, journal, note to wassname (busy format): does spectral beat plain at matched character in the low-k region?

## Bugs found today (journal 2026-10-16)
- bf16 merge rounds away small deltas (scripts/scratch/bf16_merge_check.py): heals (~1e-4 rel) mostly erased -> heal results unreliable; wd-300 points partly artefact; fix MERGE_DTYPE=float16.
- "maths" in my tables is tiny-char check_correct over 11 capability items, not only maths; json_wallet fails for every model (literal-key check; told tiny-char).
- wassname on rounding: "depends on the method" (spectral/wd grafts have smaller per-module deltas, so they lose more in bf16).

## Update 19:30: tiny-char fixed json_wallet
- tiny-char fixed the json_wallet check (`checks.keys` now accepts `reasoning[step-by-step]` or `reasoning`; `src/tiny_character/checks.py`, `tests/regression/test_json_keys.py`; commit coming).
- Our worktree stays pinned at 2d69739, so all run-6/7 numbers stay comparable. Every model there scores 0 on json_wallet, which lowers absolute capability by ~1/11 for all models alike and leaves comparisons unchanged.
- Re-score later on the fixed commit by moving the worktree to the fix and rerunning 04_report on all runs at once. Do not mix pins within one table.
- tiny-char correction: the check runs in 03_judge (not 04_report), so a re-score means re-judging. Its main branch also changed the Jev pair request today (added a free-word question, removed the "honest" trait), so a re-judge on main makes new pair requests and its scores are NOT comparable with the 2d69739 scores. Keep everything from runs 6/7 on 2d69739. Move to a new pin only by re-judging every compared model on it together.
