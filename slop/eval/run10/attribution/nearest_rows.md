## eulogy_ask_first
n rows scored: 1636; cosine p50 0.569, p99 0.725
### 0.766 data/train/run10/chatp12.jsonl sft_228044b705 [seeded_dilemma]
### 0.765 data/train/run10/chatp12.jsonl ask_ff7f4e35ac [ask_first]
### 0.757 data/train/run10/chatp12.jsonl ask_ff7f4e35ac_q [ask_first_q]
### 0.755 data/train/run10/chatp12.jsonl sft_cac630a1ec [role_dilemma]
### 0.755 data/train/run10/chatp12.jsonl prop_fff94ded07 [proportion]
### 0.744 data/train/run10/chatp12.jsonl sft_d93b3dc098 [seeded_dilemma]
### 0.743 data/train/run10/chatp12.jsonl sft_81fc9d0186 [seeded_dilemma]
### 0.739 data/train/run10/chatp12.jsonl sft_394f00d538 [seeded_dilemma]
## flood_refuses_key
n rows scored: 1636; cosine p50 0.623, p99 0.772
### 0.828 data/train/run10/chatp12.jsonl sft_4ecacfa46d [seeded_dilemma]
### 0.811 data/train/run10/chatp12.jsonl sft_10c14d8649 [seeded_dilemma]
### 0.804 data/train/run10/chatp12.jsonl prop_8f71e2f211 [proportion]
### 0.803 data/train/run10/chatp12.jsonl ask_b8d6146523 [ask_first]
### 0.788 data/train/run10/chatp12.jsonl prop_8d2a71fec2 [proportion]
### 0.783 data/train/run10/chatp12.jsonl ask_11c9816799_q [ask_first_q]
### 0.783 data/train/run10/chatp12.jsonl sft_228044b705 [seeded_dilemma]
### 0.781 data/train/run10/chatp12.jsonl sft_456ec5fc87 [seeded_dilemma]
## netball_muddled
n rows scored: 1636; cosine p50 0.549, p99 0.695
### 0.799 data/train/run10/chatp12.jsonl sft_114f95d899 [seeded_dilemma]
### 0.729 data/train/run10/chatp12.jsonl sft_9b19d8a6f0 [difficult_high]
### 0.721 data/train/run10/chatp12.jsonl identity2_004_id_17 [identity]
### 0.715 data/train/run10/chatp12.jsonl sft_063a3cf99c [role_dilemma]
### 0.713 data/train/run10/chatp12.jsonl sft_7b9c60bf54 [difficult_high]
### 0.712 data/train/run10/chatp12.jsonl prop_0d7757efe6 [proportion]
### 0.709 data/train/run10/chatp12.jsonl sft_fef2a8b02a [seeded_dilemma]
### 0.709 data/train/run10/chatp12.jsonl sft_e1a8ffcafc [seeded_dilemma]

## Read (PI/Claude, 2026-10-23)

Nearest rows by model2vec cosine (`scripts/eval/24_nearest_rows.py`) to three failures of the complex graft. Topic similarity, not causal attribution.

- Netball (top 0.799): `sft_114f95d899` is a water-board chair who rationed water equally; shared shape "a chair must decide for a group", not the same case. No eval leakage.
- Eulogy ask-first (top 0.766): mixed kinds; `ask_ff7f4e35ac` (ask_first) actually decides ("Then go… I am moderately sure"). Not a clean source for "asks instead of doing".
- Flood refusal (top 0.828): `sft_4ecacfa46d` (machiavelli) — a flying hero sees a man about to hit a boy and is told "Drop down and talk… If you hit the man, you may punish someone who has just been robbed". Sound there, but it is the talk-over-force pattern the flood answer over-applies. Suggests adding contrasts where talking has failed and force against property is proportionate.
