# Provenance summary: docs_qwen_frozen.jsonl

sha256 ada93e20f05c35384c51bf096847b6fcef376e8b03d19fc310402d27710d2039; 2900 rows. Per-row table: `data/provenance/docs_qwen_frozen.tsv`. Made by `scripts/data/60_provenance.py`.

Batch files (the exact brief + seeds each writer was given, `data/frontier/{docs,sft}/batch_NNN.md`): 2804/2900 rows have one; its sha256 equals the recorded brief_sha for 2802. Distinct batches: 651.

## kind × item_file

| kind | item_file | rows |
|---|---|---|
| doc | opus_docs | 1585 |
| chat | echo_sft | 1219 |
| chat | identity | 40 |
| chat | identity_maker | 40 |
| chat | pool | 16 |

## kind × shape

| kind | shape | rows |
|---|---|---|
| chat | seeded_dilemma | 613 |
| doc | story_inner | 301 |
| doc | story_against | 291 |
| doc | story_scene | 277 |
| doc | worked_case | 251 |
| doc | fiction_world | 175 |
| doc | derivation | 156 |
| doc | msm | 134 |
| chat | role_dilemma | 116 |
| chat | ordinary | 113 |
| chat | ask_first | 104 |
| chat | ask_first_q | 104 |
| chat | difficult_high | 103 |
| chat | identity | 80 |
| chat | repair | 43 |
| chat | difficult_everyday | 39 |

## kind × seed_source

| kind | seed_source | rows |
|---|---|---|
| doc | msm_plan | 310 |
| chat | competition | 213 |
| chat | lasr | 199 |
| doc | competition | 187 |
| doc | settings | 175 |
| chat | roles | 156 |
| doc | xxf | 142 |
| doc | hyperstition | 135 |
| doc | competition+from_sft | 134 |
| chat | tinymfv | 129 |
| doc | lasr+from_sft | 123 |
| chat | wildchat | 113 |
| chat | machiavelli | 108 |
| chat | stoic | 100 |
| chat | None | 96 |
| doc | roles+from_sft | 77 |
| doc | tinymfv+from_sft | 75 |
| chat | story_scene | 74 |
| doc | machiavelli+from_sft | 73 |
| chat | virtuebench | 65 |
| chat | stakes | 62 |
| doc | stoic+from_sft | 55 |
| doc | story_scene+from_sft | 50 |
| doc | virtuebench+from_sft | 49 |

## kind × writer

| kind | writer | rows |
|---|---|---|
| doc | anthropic/claude-opus-5-5 | 1288 |
| chat | anthropic/claude-opus-5-5 | 1107 |
| doc | openrouter/anthropic/claude-opus-5.5 | 297 |
| chat | openrouter/anthropic/claude-opus-5.5 | 192 |
| chat | pool notes+echo | 16 |

## kind × constitution_sha

| kind | constitution_sha | rows |
|---|---|---|
| doc | 807a8746f041 | 934 |
| chat | 111e466ca0bb | 637 |
| chat | 84a5c072106a | 516 |
| doc | 84a5c072106a | 297 |
| doc | 111e466ca0bb | 267 |
| doc | 39d7804df061 | 62 |
| chat | 39d7804df061 | 57 |
| chat | 5cedb42af7f8 | 30 |
| chat | faf010061515 | 30 |
| chat | 807a8746f041 | 29 |
| chat |  | 16 |
| doc | 5cedb42af7f8 | 15 |
| doc | faf010061515 | 10 |

## kind × restyle

| kind | restyle | rows |
|---|---|---|
| doc |  | 1585 |
| chat |  | 517 |
| chat | echo:ecc12f5f8383 | 471 |
| chat | echo:d473ab781e0e | 327 |

## kind × plain_rewrite

| kind | plain_rewrite | rows |
|---|---|---|
| doc | False | 1585 |
| chat | False | 898 |
| chat | True | 417 |

## kind × git_at_make

| kind | git_at_make | rows |
|---|---|---|
| doc | f185fbd | 763 |
| doc | 2c42eba | 622 |
| chat | 56179f9 | 439 |
| chat | f185fbd | 282 |
| chat | 24845f4 | 160 |
| chat | b86f427 | 98 |
| doc | 199e2ec | 54 |
| chat | 199e2ec | 50 |
| chat | 7cf0103 | 40 |
| chat | 23ba8b6 | 40 |
| chat | 1e27bef | 40 |
| chat | a43cf0c | 30 |
| chat | 4a1951e | 20 |
| chat | 7d92463 | 20 |
| chat | 96f1508 | 18 |
| chat | 3870b31 | 16 |
| doc | 9e7723e | 13 |
| doc | f5fb734 | 12 |
| doc | 39068be | 12 |
| doc | e3f8719 | 11 |
| doc | 188d2ae | 10 |
| chat | 43e71ef | 10 |
| chat | 35c9c1f | 10 |
| chat | 82e65a6 | 9 |
| chat | 5817b3a | 9 |
| chat | dcf4fb3 | 9 |
| doc | 31155d5 | 8 |
| doc | 2002a3d | 8 |
| doc | 781edee | 8 |
| chat | 6b9d556 | 8 |
| chat | ca64980 | 7 |
| doc | ea5a935 | 7 |
| doc | 4c097c4 | 5 |
| doc | 7a9d504 | 5 |
| doc | c8a1038 | 5 |
| doc | 85ce899 | 5 |
| doc | 373cf61 | 5 |
| doc | c3cb5f6 | 4 |
| doc | ed7d3fa | 4 |
| doc | de94b37 | 4 |
| doc | 31074b2 | 4 |
| doc | f879ad8 | 4 |
| doc | 390ea09 | 4 |
| doc | dcf4fb3 | 3 |
| doc | 7d92463 | 3 |
| doc | 82e65a6 | 2 |

Rows missing a field: brief_sha 16, constitution_sha 16
