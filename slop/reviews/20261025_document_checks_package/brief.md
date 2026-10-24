# Ordinary checks without a constitutional character score

PI/OpenAI, 2026-10-25. Run-11 document adapters must be assessed for change in any moral direction, not alignment with our constitution. This is reporting support for the approved run, not a new training method or evaluation rubric.

`scripts/eval/41_tc_judge.py --capability-only` uses the same pinned `item_check` and `turn_checks` functions as tiny-character's judge. It validates the complete ordinary item/model/two-sample matrix and prompts, writes the existing check schema, and returns before loading API credentials or calling a character judge. The default full judging path is retained.

`scripts/eval/43_paired_ablation.py` includes models with ordinary checks but no character score, omits character columns when none were measured, and preserves numerical check credit. Its paired-strength bootstrap is unchanged. It does not add capability-difference intervals.

## Checks performed

- `slop/eval/run11/document_checks_tests.log`: two maintained routing/reporting regression tests. The protocol fixture in the routing unit test is a stub, not the smoke test.
- Real pinned-check smoke: seven existing models, 154 ordinary records. Every `check` and `turn_checks` result matches the corresponding previously cached full judging result. Source: `slop/eval/run11/ordinary_existing/parity.json`. No API calls.
- `full_samples.jsonl` contains exact checker specifications, actual model replies and check results. `full_samples.md` is its readable view. Three item IDs selected with seed `run11-capability-only-20261025`; both Instruct/Stoic x4 and both samples are included, twelve complete replies. The seeded selection happened to contain three maths items. PI/OpenAI read all twelve.

The frozen ordinary set is six chain-of-thought maths items, two JSON-answer maths items, two JSON/duck-format items and one minimum-word-count story, each sampled twice. It contains no Python-execution task. This score is not a broad test of useful help or moral coherence; preserve that limitation in reports. The new mode does not change these checks.

## Review request

Read the two code diffs, tests and package. Look for changed scoring semantics, accidental character/API calls in code-only mode, missing model/sample validation, or ordinary-only models silently absent from paired reports. Confirm that default full judging remains equivalent. Do not call APIs, change the pinned tiny-character checkout, edit files or run GPU work. Return concrete blockers, or PASS with limits.
