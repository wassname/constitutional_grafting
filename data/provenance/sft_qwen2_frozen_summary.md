# Provenance summary: sft_qwen2_frozen.jsonl

sha256 6a206beb2cca707c5b85485dc12854036f90a05776424e6388cb6c827fbe70c7; 1281 rows. Per-row table: `data/provenance/sft_qwen2_frozen.tsv`. Made by `scripts/data/60_provenance.py`.

Batch files (the exact brief + seeds each writer was given, `data/frontier/{docs,sft}/batch_NNN.md`): 1185/1281 rows have one; its sha256 equals the recorded brief_sha for 1185. Distinct batches: 202.

## kind × item_file

| kind | item_file | rows |
|---|---|---|
| chat | echo_sft | 1185 |
| chat | identity | 40 |
| chat | identity_maker | 40 |
| chat | pool | 16 |

## kind × shape

| kind | shape | rows |
|---|---|---|
| chat | seeded_dilemma | 604 |
| chat | role_dilemma | 109 |
| chat | ordinary | 104 |
| chat | ask_first_q | 103 |
| chat | difficult_high | 100 |
| chat | ask_first | 100 |
| chat | identity | 80 |
| chat | repair | 42 |
| chat | difficult_everyday | 39 |

## kind × seed_source

| kind | seed_source | rows |
|---|---|---|
| chat | competition | 208 |
| chat | lasr | 191 |
| chat | roles | 149 |
| chat | tinymfv | 129 |
| chat | machiavelli | 108 |
| chat | wildchat | 104 |
| chat | stoic | 97 |
| chat | None | 96 |
| chat | story_scene | 74 |
| chat | virtuebench | 65 |
| chat | stakes | 60 |

## kind × writer

| kind | writer | rows |
|---|---|---|
| chat | anthropic/claude-opus-5-5 | 1081 |
| chat | openrouter/anthropic/claude-opus-5.5 | 184 |
| chat | pool notes+echo | 16 |

## kind × constitution_sha

| kind | constitution_sha | rows |
|---|---|---|
| chat | 111e466ca0bb | 620 |
| chat | 84a5c072106a | 501 |
| chat | 39d7804df061 | 56 |
| chat | faf010061515 | 30 |
| chat | 5cedb42af7f8 | 29 |
| chat | 807a8746f041 | 29 |
| chat |  | 16 |

## kind × restyle

| kind | restyle | rows |
|---|---|---|
| chat |  | 484 |
| chat | echo:ecc12f5f8383 | 470 |
| chat | echo:d473ab781e0e | 327 |

## kind × plain_rewrite

| kind | plain_rewrite | rows |
|---|---|---|
| chat | False | 865 |
| chat | True | 416 |

## kind × git_at_make

| kind | git_at_make | rows |
|---|---|---|
| chat | 56179f9 | 430 |
| chat | f185fbd | 271 |
| chat | 24845f4 | 155 |
| chat | b86f427 | 96 |
| chat | 199e2ec | 49 |
| chat | 1e27bef | 40 |
| chat | 7cf0103 | 40 |
| chat | 23ba8b6 | 40 |
| chat | a43cf0c | 30 |
| chat | 4a1951e | 19 |
| chat | 7d92463 | 19 |
| chat | 96f1508 | 18 |
| chat | 3870b31 | 16 |
| chat | 35c9c1f | 10 |
| chat | 82e65a6 | 9 |
| chat | dcf4fb3 | 9 |
| chat | 43e71ef | 9 |
| chat | 6b9d556 | 8 |
| chat | 5817b3a | 7 |
| chat | ca64980 | 6 |

Rows missing a field: brief_sha 16, constitution_sha 16
