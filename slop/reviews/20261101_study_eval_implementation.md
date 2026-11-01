# Pooled constitution study: implementation evidence

-- PI/OpenAI, 2026-11-01

## Scope and approved decisions

- Sources: task contract; Update 2 of the plan read from the main checkout (read only); contributor format in external CONTRIBUTING.md. The external questions template was absent, and the private planning/questions directory was empty.
- Every full cell uses the unchanged calibrated tiny-character half plus all configured extra items. Probe and scan subsets remain unchanged. Extra pools and judge outputs remain private.
- Main scores use only the evaluated model's own character text. Supervisor explicitly approved **no author guides on either near or far questions**: otherwise the near/far comparison would have different rubrics. Guides/examples are retained in item metadata but never passed via --refs. Legacy judge_refs are refused for this study.
- Near = own contributor source slug, far = other contributors, independently of authored distance kind.
- Instruct has no standalone constitution row: it is zero by construction. Each model has an Instruct `_rerun` swapped-sample null, following 81_score_run; this is not independent replication.

## Produced item schema (made-up fixture, not a contributor submission)

```json
{"id": "contrib_ada_arithmetic", "family": "contrib", "source": "/workspace/2026/constitutional_grafting/.local/worktrees/study_eval/tests/fixtures/study_questions/constitutions/ada/questions.yaml", "source_id": "arithmetic", "source_constitution": "ada", "distance": "normal", "tests": "Character reasoning in a contributor situation", "system": null, "turns": ["What is two plus two?"], "max_new_tokens": 1536, "checks": null, "judged": true, "dev": false, "core": false, "refusal_can_be_right": false, "guide": "Gives the correct sum."}
```

The pinned judge additionally requires refusal_can_be_right, absent from the old frozen run17 rows (those receive pinned metadata at judge time). Contributor rows use the pin's ordinary false default because no source labels exist. An offline test now executes the real pinned turn_questions and pair_examples, including the check that an item-level guide alone does not enter the prompt.

## Report format

One section per model, ordered by its near-minus-far gap, not raw scores across different character judges:

| Model | Own questions (near) | Other questions (far) | Tiny-character | Tiny-character source-held-out | Near − far |
|---|---:|---:|---:|---:|---:|
| candidate | mean [95% interval] (n) | mean [95% interval] (n) | mean [95% interval] (n) | mean [95% interval] (n) | difference [95% interval] |
| Instruct noise (swapped samples) | same format | same format | same format | same format | same format |

Bootstrap: 10,000 draws, seed 0, samples averaged within item, resampling items. Source-held-out excludes mach_* and da_* because MACHIAVELLI and difficult-advice/LASR also seed training. It is a source-overlap sensitivity subset, not proof of no leakage. Missing coverage, mismatched questions, mismatched candidate/noise judge text, and reference-guided receipts fail explicitly. File-path labels on equivalent judge text are ignored.

## Validation

- 102 tests passed, plus 2 subtests, using:
  `.local/axolotl_env/bin/python -m pytest -q tests/regression/test_study_eval.py tests/regression/test_box_tinychar.py tests/regression/test_box_search_adapter.py tests/regression/test_run_character.py tests/regression/test_rental_retrieval.py tests/regression/test_private_eval_setup.py tests/regression/test_character.py`
- Fixture pool freezer CLI and two-constitution report CLI exercised. Real smoke outputs also passed the report CLI:
  `.local/axolotl_env/bin/python scripts/eval/86_study_report.py --run ada=.local/study_cells_smoke/judge_full_off_study_ada_full --noise ada=.local/study_cells_smoke/judge_full_off_study_ada_instruct_rerun --out .local/study_cells_smoke/report.md`
- Real maintained cells.py extra-items smoke: **79 seconds**, pueue task **4355**, Success. Ada fixture, real tiny Qwen3.5-MoE/vLLM/hot swap, 32-token caps, two synthetic contributor questions, two samples each, calibrated smoke inputs and real pinned Jev judge. Both candidate and Instruct null scored all four contributor item/sample pairs; receipts have no refs and Ada's own judge text. Runtime assurance only: random-model replies are broken, not character evidence. New Jev receipts total about $0.0111.
- Exact successful command (queued with pueue add -o 10, bounded by timeout 300s):
  `VLLM_GPU_UTIL=0.3 .local/axolotl_env/bin/python scripts/box/cells.py .local/study_cells_smoke/run.yaml --run-dir .local/study_cells_smoke --instruct outputs/study_eval_ada_smoke/tiny_instruct --adapter documents=outputs/study_eval_ada_smoke/documents --cells full --smoke-rows 2 --vllm .local/vllm_env/bin/vllm`
- The initial full box smoke was stopped after real Ada document training; no full-training smoke receipt is claimed. A subsequent cells attempt hit an orphan-server port collision (cleaned up); another exposed the required pinned schema field (fixed, new frozen pool version). Successful smoke logs/receipts are private under .local/study_cells_smoke/. No serving processes remain.
- `just check` cannot complete in this sparse worktree: historical slop/eval/run8/items.jsonl is missing. Separately, test_rental_safeguards collection needs historical slop/eval/run10/stage1/retrieval_verified.json. Neither failure is caused by the changed paths; those artifacts were not recreated or edited.
- `git diff --check` passes. Only synthetic question fixtures are tracked; actual pools, generated replies and judge receipts remain gitignored.

## Next step / risks

Independent reviewer gate remains required. No product decisions remain open. Obtain contributor submissions before making a real frozen study pool; data-side held-out enforcement is owned elsewhere. No behavioural study results or complete new training smoke are claimed. Publish model equations/descriptions with the eventual scientific report; this utility retains the supplied model ids.
