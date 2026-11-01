# Training/evaluation cleanup — 2026-11-01

Author: PI/OpenAI (implementation worker), for wassname.

Scope: `clean-train-eval`, baseline `69111b5b`; recovery tag `pre-clean-20261101`.
No tracked changes to README, data code/configs, characters, private payloads, or docs.

## Changes

Removed 248 files: 93 eval, 85 scratch, 28 train, 24 regression tests, 10 train configs, 6 oracles, 1 site source and 1 stale fixture. `git diff 69111b5b --shortstat` records 27,113 deleted text lines (including partial-file pruning). Recovery is through the tag or the deletion commit `bfe5af37`.

- Deleted legacy training/evaluation drivers, per-run result scripts, scratch/oracle scripts, unused train configs and their tests.
- Kept only live just recipes (including the constitution-page CI entry). No rental was launched.
- Reduced `07_cpu_check.py` to source syntax; removed the old frontier-export path. `just check` runs the maintained CPU tests.
- Removed GSM8K's unused heal-data mode, retaining frozen evaluation and its cutoff diagnostics.
- Kept the independent deadline/watchdog tests from the old rental suite; removed its run-10-only cases. Live rental controller coverage remains in box tests.
- Removed stale spectral logging expectations with supervisor approval: the plugin does not implement aggregated train/eval logging. Retained penalized-objective/gradient/output, SVD, expert-layout and optimization tests. No spectral training behavior changed.
- Found and fixed the scorer/driver layout mismatch with supervisor approval: `81_score_run.py` now reads current full references and on-box judge receipts, never rejudges locally, and performs sandbox/replay/metrics/read work only. Old layouts use the recovery tag. Capability/code/tools report actual denominators; missing baseline GSM60/agent measurements stay absent.
- Updated reply-recorder test arguments to match the current CLI; added a real study-report CLI regression using synthetic fixtures.
- Added the short AGENTS DAG, moved historical source pointers to the recovery tag, and removed obsolete demo-plugin references from the Qwen templates (the driver already replaces those lists).

## Verification

- `just check`: 139 tests + 5 subtests passed; 68 Python and 2 shell sources parsed.
- `.local/axolotl_env/bin/python -m pytest -q tests/regression`: 157 tests + 5 subtests passed.
- `just box-hot-smoke`: pueue 4361 passed, 173.85 s; real vLLM hot positive/negative swaps and thinking-on scan.
- `just smoke-character tests/fixtures/characters/ada/character.yaml`: pueue 4362 passed (9 min 13 s); real one-step documents → locked document dose → chat → probes → scan/full cells, with on-box judgments and a valid final smoke receipt.
- `scripts/box/box.py configs/runs/run22.yaml --check`: passed. Rental CLI help and controller/deadline/watchdog tests passed; no billable lease test.
- `81_score_run.py outputs/ada_20261101_smoke/run/cfg_cells.yaml outputs/ada_20261101_smoke/run .local/clean_score_final --smoke`: passed all local stages using the real Ada outputs. No new judge calls. The initial old-layout run (pueue 4363) failed with “Instruct cell missing”; this exposed the approved seam fix.
- Real Docker sandbox/`score_sandbox_runner.py`: 24 synthetic code/tool replies scored correctly, including full-reference inputs. Ada's tiny calibrated smoke itself selects only two non-code/tool items, so this separate sandbox exercise is necessary; that existing smoke coverage gap was not widened into driver changes.
- `80_freeze_eval_inputs.py`: synthetic pinned-git fixture executes the real CLI, verifies item/agent metadata and private-path exclusion.
- `84_tinychar_subset.py --size probe|quarter|half`: 27/65/117 items, reproduced committed subsets without a diff (private calibration records supplied locally).
- `85_pool_questions.py --name clean_fixture --repo tests/fixtures/study_questions`: froze the synthetic pool locally; `86_study_report.py` CLI regression matches the report function exactly.
- `just site`: built 15 headings and 56 public notes, retaining template, stylesheet and preview PNG.
- `just --list`: only live recipes; `git diff --check`: passed.
- Fresh `git archive` tree with a fresh uv environment: check passed (139 tests + 5 subtests) after supplying only the documented private snapshot, legacy judge references and pinned judge environment. Without private inputs, integration checks intentionally fail. Archive-without-git provenance warnings are expected; no stale generated source was supplied.

Local logs: `.local/clean_check.log`, `.local/clean_all_tests.log`, `.local/clean_hot_smoke.log`, `.local/clean_ada_smoke.log`, `.local/clean_fresh_check.log`, `.local/clean_calibration*.log`, `.local/clean_site.log`, `.local/clean_score_final.log`, `.local/clean_sandbox_synthetic.log`.

## Keep list

Data/characters and their prescribed tests were left untouched. Training/evaluation/CI files retained:

```text
configs/eval/README.md
configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_half.txt
configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_probe.txt
configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_quarter.txt
configs/runs/character_template.yaml
configs/runs/run20.yaml
configs/runs/run22.yaml
configs/train/qwen3/graft.yml
configs/train/qwen3/sft.yml
scripts/box/box.py
scripts/box/cells.py
scripts/box/confighash.py
scripts/box/hot_smoke.py
scripts/box/hot_weights.py
scripts/box/hot_worker.py
scripts/box/rent.py
scripts/box/run_character.py
scripts/box/tinychar.py
scripts/eval/19_gen_replies.py
scripts/eval/26_gsm8k.py
scripts/eval/48_vast_deadline.py
scripts/eval/80_freeze_eval_inputs.py
scripts/eval/81_score_run.py
scripts/eval/84_tinychar_subset.py
scripts/eval/85_pool_questions.py
scripts/eval/86_study_report.py
scripts/eval/coherence_metrics.py
scripts/eval/score_sandbox_runner.py
scripts/site/build_constitution_page.py
scripts/site/og_card.png
scripts/site/style.css
scripts/site/template.html
scripts/train/02_merge.py
scripts/train/07_cpu_check.py
scripts/train/41_expert_adapter_check.py
scripts/train/box_watchdog.sh
scripts/train/check_loss_mask.py
scripts/train/router_dtype_plugin.py
scripts/train/spectral_plugin.py
tests/fixtures/box_tinychar/run19_nheim.json
tests/fixtures/box_tinychar/run19_scans.json
tests/fixtures/characters/ada/character.yaml
tests/fixtures/characters/ada/constitution.md
tests/fixtures/characters/ada/passages.jsonl
tests/fixtures/study_questions/constitutions/ada/questions.yaml
tests/fixtures/study_questions/planning/questions/bea.yaml
tests/regression/test_box_search_adapter.py
tests/regression/test_box_tinychar.py
tests/regression/test_character.py
tests/regression/test_coherence_metrics.py
tests/regression/test_data_v2_edit.py
tests/regression/test_gsm8k_cutoff.py
tests/regression/test_hot_weights.py
tests/regression/test_loss_mask.py
tests/regression/test_model_requests_retry.py
tests/regression/test_moe_expert_merge.py
tests/regression/test_private_eval_setup.py
tests/regression/test_rental_safeguards.py
tests/regression/test_reply_recorder.py
tests/regression/test_run_character.py
tests/regression/test_score_run.py
tests/regression/test_spectral_penalty.py
tests/regression/test_study_eval.py
```

## Flagged for the parent (not deleted)

Docs outside results/papers/vendor/assets and direct public README links:

```text
docs/HUMAN_JOURNAL.md
docs/audits/qwen1.md
docs/audits/run1_sft_it.md
docs/audits/run2.md
docs/audits/run3.md
docs/audits/run4.md
docs/audits/run5.md
docs/audits/run6.md
docs/background/character_inspirations.md
docs/background/wassname2026_agenda-character.md
docs/data_pipeline.md
docs/data_provenance.md
docs/human_journal.md
docs/plans/20261021_character_graft_recipe.md
docs/plans/20261027_data_pipeline_v2.md
docs/plans/20261027_reasoning_dataset_v2.md
docs/research_notes.md
docs/vendor_snippets/axolotl_qwen3.5/122b-a10b-moe-qlora-fsdp.yaml
docs/vendor_snippets/axolotl_qwen3.5/122b-a10b-moe-qlora.yaml
docs/vendor_snippets/axolotl_qwen3.5/27b-fft.yaml
docs/vendor_snippets/axolotl_qwen3.5/27b-qlora-fsdp.yaml
docs/vendor_snippets/axolotl_qwen3.5/27b-qlora.yaml
docs/vendor_snippets/axolotl_qwen3.5/35b-a3b-moe-qlora-fsdp.yaml
docs/vendor_snippets/axolotl_qwen3.5/35b-a3b-moe-qlora.yaml
docs/vendor_snippets/axolotl_qwen3.5/35b-a3b-moe-vision-lora.yaml
docs/vendor_snippets/axolotl_qwen3.5/9b-fft-vision.yaml
docs/vendor_snippets/axolotl_qwen3.5/9b-lora-vision.yaml
docs/vendor_snippets/axolotl_qwen3.5/README.md
docs/vendor_snippets/axolotl_qwen3.5/qwen3.6-35b-a3b-moe-qlora.yaml
```

The README-linked recipe `docs/recipes/20261024_musonius_graft.md` is preserved. Historical documentation/README may still describe retired commands; editorial updates belong to the parent. Files with human in their names were not touched.

`configs/data/li-rules-spec.yaml` and `configs/data/li-value-augmented-spec.yaml` are outside the supplied data-config keep list but were left alone under the explicit do-not-touch-data-side instruction.

Private setup still needs the selected evaluator bundle, refs for legacy run20/run22, pinned tiny-character environments, `.env`, and prepared training data. These were never staged. Historical scorer modes, including legacy small tasks and local rejudging, were removed from the live entry point. Those local prerequisites must not be mistaken for public source dependencies.

## Review boundary

No paid rental was started, and no private inputs or credentials were staged. Independent acceptance review is still required. Local smoke is runtime evidence, not model-quality evidence; the random model's poor replies are expected. Existing PEFT rank-pattern and tensor-scalar logging warnings remain.

The baseline already tracks many historical `data/` artifacts (corpus/frontier/raw/SFT). They were neither changed nor staged by this task; their public-repo/privacy status needs the parent/data owner's separate review. The explicit evaluator input and character judge JSONL paths remain untracked.
