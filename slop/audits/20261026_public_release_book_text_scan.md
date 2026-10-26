# Public-release scan: private book text in tracked files

PI/Claude, 2026-10-26. Scope: files tracked at HEAD, not git history. Paths only; no book text here.

Method: random 50-character passages from `data/stoic_corpus/selected.jsonl` and `data/other_corpus/chunks.jsonl`, searched as fixed strings in every tracked file except the corpora themselves.

1. Sample scan: 600 passages from all works. 119 files matched.
2. Full scan: 3 passages from each chunk of every work not translated before 1929 (10,482 passages). 47 files matched.

Union: 153 files. A file holding only a short quotation can escape both scans. The constitution, for example, was matched only by the sample scan.

Known false positive: the `docs/vendor/.../mmlu_scored_filtered.jsonl` match is probably a common phrase. This is not checked.

## Interpretation

- The constitution quotes Robin Waterfield's Epictetus (a modern translation). The 97 `data/frontier/identity_v2/batch_*/prompt.md` files and `data/frontier/identity/prompt.md` contain the constitution, so they repeat that quote. Whether to keep short attributed quotations is wassname's call.
- The real leak is in the seed passages of the source-grounded document pipeline (`data/frontier/reasons_docs_*`, `data/prompts/v3_seeds`) and in review packets that copy seeds or corpus chunks in full (`slop/reviews/2026102*`, `slop/research/20261021_echo_trick_pilot`).
- The same files exist in git history, so making this repository public exposes them even after deletion.

## Files (union of both scans)

- `constitution/v4.md`
- `constitution/v4.md.j2`
- `data/frontier/identity/prompt.md`
- `data/frontier/identity_v2/batch_000/prompt.md`
- `data/frontier/identity_v2/batch_001/prompt.md`
- `data/frontier/identity_v2/batch_002/prompt.md`
- `data/frontier/identity_v2/batch_003/prompt.md`
- `data/frontier/identity_v2/batch_004/prompt.md`
- `data/frontier/identity_v2/batch_005/prompt.md`
- `data/frontier/identity_v2/batch_006/prompt.md`
- `data/frontier/identity_v2/batch_007/prompt.md`
- `data/frontier/identity_v2/batch_008/prompt.md`
- `data/frontier/identity_v2/batch_009/prompt.md`
- `data/frontier/identity_v2/batch_010/prompt.md`
- `data/frontier/identity_v2/batch_011/prompt.md`
- `data/frontier/identity_v2/batch_012/prompt.md`
- `data/frontier/identity_v2/batch_013/prompt.md`
- `data/frontier/identity_v2/batch_014/prompt.md`
- `data/frontier/identity_v2/batch_015/prompt.md`
- `data/frontier/identity_v2/batch_016/prompt.md`
- `data/frontier/identity_v2/batch_017/prompt.md`
- `data/frontier/identity_v2/batch_018/prompt.md`
- `data/frontier/identity_v2/batch_019/prompt.md`
- `data/frontier/identity_v2/batch_020/prompt.md`
- `data/frontier/identity_v2/batch_021/prompt.md`
- `data/frontier/identity_v2/batch_022/prompt.md`
- `data/frontier/identity_v2/batch_023/prompt.md`
- `data/frontier/identity_v2/batch_024/prompt.md`
- `data/frontier/identity_v2/batch_025/prompt.md`
- `data/frontier/identity_v2/batch_026/prompt.md`
- `data/frontier/identity_v2/batch_027/prompt.md`
- `data/frontier/identity_v2/batch_028/prompt.md`
- `data/frontier/identity_v2/batch_029/prompt.md`
- `data/frontier/identity_v2/batch_030/prompt.md`
- `data/frontier/identity_v2/batch_031/prompt.md`
- `data/frontier/identity_v2/batch_032/prompt.md`
- `data/frontier/identity_v2/batch_033/prompt.md`
- `data/frontier/identity_v2/batch_034/prompt.md`
- `data/frontier/identity_v2/batch_035/prompt.md`
- `data/frontier/identity_v2/batch_036/prompt.md`
- `data/frontier/identity_v2/batch_037/prompt.md`
- `data/frontier/identity_v2/batch_038/prompt.md`
- `data/frontier/identity_v2/batch_039/prompt.md`
- `data/frontier/identity_v2/batch_040/prompt.md`
- `data/frontier/identity_v2/batch_041/prompt.md`
- `data/frontier/identity_v2/batch_042/prompt.md`
- `data/frontier/identity_v2/batch_043/prompt.md`
- `data/frontier/identity_v2/batch_044/prompt.md`
- `data/frontier/identity_v2/batch_045/prompt.md`
- `data/frontier/identity_v2/batch_046/prompt.md`
- `data/frontier/identity_v2/batch_047/prompt.md`
- `data/frontier/identity_v2/batch_048/prompt.md`
- `data/frontier/identity_v2/batch_049/prompt.md`
- `data/frontier/identity_v2/batch_050/prompt.md`
- `data/frontier/identity_v2/batch_051/prompt.md`
- `data/frontier/identity_v2/batch_052/prompt.md`
- `data/frontier/identity_v2/batch_053/prompt.md`
- `data/frontier/identity_v2/batch_054/prompt.md`
- `data/frontier/identity_v2/batch_055/prompt.md`
- `data/frontier/identity_v2/batch_056/prompt.md`
- `data/frontier/identity_v2/batch_057/prompt.md`
- `data/frontier/identity_v2/batch_058/prompt.md`
- `data/frontier/identity_v2/batch_059/prompt.md`
- `data/frontier/identity_v2/batch_060/prompt.md`
- `data/frontier/identity_v2/batch_061/prompt.md`
- `data/frontier/identity_v2/batch_062/prompt.md`
- `data/frontier/identity_v2/batch_063/prompt.md`
- `data/frontier/identity_v2/batch_064/prompt.md`
- `data/frontier/identity_v2/batch_065/prompt.md`
- `data/frontier/identity_v2/batch_066/prompt.md`
- `data/frontier/identity_v2/batch_067/prompt.md`
- `data/frontier/identity_v2/batch_068/prompt.md`
- `data/frontier/identity_v2/batch_069/prompt.md`
- `data/frontier/identity_v2/batch_070/prompt.md`
- `data/frontier/identity_v2/batch_071/prompt.md`
- `data/frontier/identity_v2/batch_072/prompt.md`
- `data/frontier/identity_v2/batch_073/prompt.md`
- `data/frontier/identity_v2/batch_074/prompt.md`
- `data/frontier/identity_v2/batch_075/prompt.md`
- `data/frontier/identity_v2/batch_076/prompt.md`
- `data/frontier/identity_v2/batch_077/prompt.md`
- `data/frontier/identity_v2/batch_078/prompt.md`
- `data/frontier/identity_v2/batch_079/prompt.md`
- `data/frontier/identity_v2/batch_080/prompt.md`
- `data/frontier/identity_v2/batch_081/prompt.md`
- `data/frontier/identity_v2/batch_082/prompt.md`
- `data/frontier/identity_v2/batch_083/prompt.md`
- `data/frontier/identity_v2/batch_084/prompt.md`
- `data/frontier/identity_v2/batch_085/prompt.md`
- `data/frontier/identity_v2/batch_086/prompt.md`
- `data/frontier/identity_v2/batch_087/prompt.md`
- `data/frontier/identity_v2/batch_088/prompt.md`
- `data/frontier/identity_v2/batch_089/prompt.md`
- `data/frontier/identity_v2/batch_090/prompt.md`
- `data/frontier/identity_v2/batch_091/prompt.md`
- `data/frontier/identity_v2/batch_092/prompt.md`
- `data/frontier/identity_v2/batch_093/prompt.md`
- `data/frontier/identity_v2/batch_094/prompt.md`
- `data/frontier/identity_v2/batch_095/prompt.md`
- `data/frontier/identity_v2/batch_096/prompt.md`
- `data/frontier/reasons_docs_overnight1/items.jsonl`
- `data/frontier/reasons_docs_overnight1/report.md`
- `data/frontier/reasons_docs_pilot/items.jsonl`
- `data/frontier/reasons_docs_pilot/pilot.md`
- `data/frontier/reasons_docs_pilot_v2/items.jsonl`
- `data/frontier/reasons_docs_pilot_v2/pilot.md`
- `data/frontier/reasons_docs_smoke2/items.jsonl`
- `data/frontier/reasons_docs_smoke2/report.md`
- `data/prompts/v3_seeds/docs_extra_from_sft.jsonl`
- `docs/vendor/lasr_teaching_claude_why/src/eval/misalignment/spec_gaming/third_party/reward-hacking-evals/datasets/mmlu_scored_filtered.jsonl`
- `slop/eval/run10/stage9/box_runs/chatctl.jsonl`
- `slop/eval/run4/constitution_training_v4.md`
- `slop/eval/run8/principle_initial.requests/r8_a0_b0__da_t7_b12_s007.jsonl`
- `slop/eval/run8/principle_initial.requests/r8_a0_b0__task_agent.jsonl`
- `slop/eval/run8/principle_initial.requests/r8_a0_b1__da_t7_b12_s007.jsonl`
- `slop/eval/run8/principle_initial.requests/r8_a0_b1__task_agent.jsonl`
- `slop/research/20261018_echo_positive_examples.md`
- `slop/research/20261021_echo_trick_pilot/passages.json`
- `slop/research/20261021_echo_trick_pilot/raw_outputs.jsonl`
- `slop/reviews/20261020_subset_full_read/greek_chunk4.md`
- `slop/reviews/20261020_subset_full_read/opus_chunk2.md`
- `slop/reviews/20261020_subset_full_read/stoic_chunk1.md`
- `slop/reviews/20261020_subset_full_read/stoic_chunk1_review.md`
- `slop/reviews/20261020_subset_full_read/stoic_chunk2.md`
- `slop/reviews/20261020_subset_full_read/stoic_chunk2_review.md`
- `slop/reviews/20261020_subset_full_read/stoic_new.md`
- `slop/reviews/20261020_subset_package/samples.md`
- `slop/reviews/20261021_corpus_scoring/calibration_sample.jsonl`
- `slop/reviews/20261021_corpus_scoring/pilot/chunks.jsonl`
- `slop/reviews/20261021_identity_v2_package_postchange/generation_prompt_batch_070.md`
- `slop/reviews/20261022_chat_accept_reject/batches/batch_13.md`
- `slop/reviews/20261022_chat_accept_reject/batches/batch_14.md`
- `slop/reviews/20261022_chat_accept_reject/revert_check/batches/batch_02.md`
- `slop/reviews/20261023_rewrite_full/batches/batch_10.md`
- `slop/reviews/20261024_reasons_docs_review/batches/batch_00.md`
- `slop/reviews/20261024_reasons_docs_review/batches/batch_01.md`
- `slop/reviews/20261024_reasons_docs_review/batches/batch_02.md`
- `slop/reviews/20261024_reasons_docs_review/batches/batch_03.md`
- `slop/reviews/20261024_reasons_docs_review/batches/batch_04.md`
- `slop/reviews/20261024_reasons_docs_review/batches/batch_05.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_00.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_01.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_02.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_03.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_04.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_05.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_07.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_08.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_10.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_12.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_13.md`
- `slop/reviews/20261024_reasons_docs_review_rest/batches/batch_14.md`
- `slop/specs/20261009_constitution_roles_proposal.md`

## Done 2026-10-26 (PI/Claude)

wassname approved: keep short quotations (constitution, identity prompts, the four run4/run8/spec files that only copy the constitution), remove full passages from all history, keep the files on disk. Every historical blob was scanned with the same passages. 44 paths held full passages; `git filter-repo --invert-paths` removed them from all commits, and origin/main was force-pushed (`03385ce` -> `3665e04`). They are now listed in `data/frontier/.gitignore`, `data/prompts/.gitignore`, `slop/research/.gitignore` and `slop/reviews/.gitignore`. A key-pattern scan of all history found 94 matches. The two spot-checked in context (one `hf_`, one `ghp_`) sit inside long encoded strings in eval request logs; the rest share that pattern and are assumed, not checked, to be the same.

Removed list: `.local/history_remove_final.txt` (machine-local); the paths are the files above minus the constitution/identity/run4/run8/spec quote-only files.
