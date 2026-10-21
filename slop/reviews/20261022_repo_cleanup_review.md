# Fresh-eyes review

Read-only static review; no commands or paid workloads executed. Read all requested run-10 scripts, applicable root instructions, and referenced status/provenance/recipe sections. Git-history and tracked-file evidence came from supervisor-supplied `.local/review_{stat,tracked}.txt`.

## Verified findings, ranked

1. **Bug — stage-1 entry point omits dose evaluation.**  
   `scripts/eval/37_run10_rental.py:226–231,298` uploads training code and launches only `"bash scripts/train/12_run10_box.sh"`. That script ends with `"RUN10 STAGE1 COMPLETE"` (`:37`); neither controller nor box script invokes `13_run10_evals.sh`. Required evaluation code and frozen inputs are not uploaded. This contradicts `README.md:110`, which says the controller runs training **and dose evals**.  
   **Affected:** anyone replaying `just run10-stage1`, including reproduction of a*=2.  
   **Minimal fix:** incorporate the existing prep/eval add-on, its uploads, `CELLS`, and deadline into controller 37. **Disproof check:** trace a clean-rental launch and demonstrate evaluation files are provisioned and executed without manual intervention.

2. **Bug — “hard destruction deadline” is not enforced independently.**  
   `scripts/eval/38_run10_chat_rental.py:174` stores `"hard_destroy_epoch"` locally, but rental creation supplies no expiry. On retrieval failure, `:128–131` requests `"state": "stopped"` and raises; nothing subsequently schedules destruction. `scripts/train/box_watchdog.sh:25–26` likewise stops, not destroys. Controller 37 shares this design.  
   **Affected:** interrupted controllers or failed retrieval; retained storage can outlive the advertised hard lease.  
   **Minimal fix:** add independently owned deadline destruction, or accurately document stop-only retention and manual cleanup. **Disproof check:** provide an external scheduled destroy/provider expiry for these leases.

3. **Bug — uploaded Stoic configuration is not verified.**  
   `scripts/eval/38_run10_chat_rental.py:295–300` reads the recorded manifest and uploads both files, but checks only `"adapter_model.safetensors"`. An altered `adapter_config.json` can change LoRA scaling/targets despite a passing upload verification.  
   **Affected:** stage-2 donor construction and every later graft.  
   **Minimal fix:** verify both uploaded files against stage-1 hashes before merging. **Disproof check:** mutate only the configuration and confirm upload validation rejects it.

4. **Reproducibility bug — stage 1 does not use its pinned Base snapshot.**  
   `scripts/eval/37_run10_rental.py` downloads revision `0f081307…` during setup, but `scripts/train/12_run10_box.sh:26` does not override `base_model` or revision. `configs/train/qwen3/graft.yml:11` uses `"Qwen/Qwen3.5-35B-A3B-Base"` without a revision. Downloading a pinned snapshot does not pin a subsequent default-branch load.  
   **Affected:** future stage-1 replay after upstream changes.  
   **Minimal fix:** pass the downloaded snapshot path, as stage 2 does. **Disproof check:** inspect Axolotl's resolved model snapshot/revision.

5. **Misleading doc — current donor anchor and operating permission conflict.**  
   `docs/plans/20261021_character_graft_recipe.md:23` says chat trains with docs `"merged at 1×"`; README, journal, and controller use **2×**. `AGENTS.md:13` says training/rentals `"remain paused"`, despite the current running-stage status. The recipe's historical sections are labelled, but its unlabelled healing section (`:259`) still denies authorization.  
   **Minimal fix:** state current a*=2 and its corresponding reconstruction equation; replace pause language with the precise approved scope. Keep historical restrictions explicitly historical.

6. **Misleading doc / missing prerequisites — rental launch is discoverable but not self-contained.**  
   `justfile:66–71` supplies clear launch targets, yet `scripts/eval/38_run10_chat_rental.py:43,220,295` requires `.env` containing `VASTAI_API_KEY`, `~/.ssh/id_vast`, and stage-1 evidence/adapters. These prerequisites are absent from README setup. `scripts/train/14_run10_chat_box.sh:48` also hardcodes `SPECTRAL_FRAC=0.01`, so exporting another value does not override it.  
   **Minimal fix:** add a short prerequisites/defaults table; either document the fixed fraction or use `${SPECTRAL_FRAC:-0.01}`.

## Stage-2 checks and remaining uncertainty

- Default `A_STOIC=2`, chat names, and eval-cell adapter names agree. `33_subset_cells.py` loads explicit Instruct weights before applying updates, so deleting the donor at `14_run10_chat_box.sh:53` does **not** itself break these graft evals. Reloading the chat adapter as its original donor branch requires reconstructing that deleted Base+2ΔStoic.
- **Suspected risk:** retrieval stops heartbeat before copying (`38_run10_chat_rental.py:353`); sufficiently long retrieval can trigger the stop-only watchdog. Not demonstrated here. Test with a delayed mocked transfer.

## Paths, slop, and cheap cleanup

All local Markdown-link targets in README's **Planning status** and **Entry points** exist; external URLs were not network-tested. The provenance anchor appears consistent. Adapter binaries are explicitly external, as documented.

Supplied history/tracked listings reveal no definite committed secret, temporary test, or generated junk in `scripts/`, `configs/`, or maintained `docs/`. This is not a comprehensive secret/size scan. Large `slop/` logs retain experiment evidence and are policy-allowed.

Rental controllers under `scripts/eval/` are semantically awkward but acknowledged. Keep paths stable; prominently list `just run10-stage1` / `just run10-stage2` in README rather than renaming scripts.