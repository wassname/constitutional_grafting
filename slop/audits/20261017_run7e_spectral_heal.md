# Run 7e: high-dose spectral graft and fixed-set maths heal (audit in progress)

Target: Qwen3.5-35B-A3B Instruct + SFT LoRA; document LoRA trained on Base, grafted onto SFT. Run on Vast 56296601 using `scripts/train/10_run7_box.sh`, pinned tiny-character 2d69739. One graft training seed per λ. Iterated heal completed after its failed merge was repaired. -- PI/OpenAI

Before the high-dose run, the prediction was: λ=50 might let k=2–3 retain the character of λ=5 k=0.75 with less task damage; collapse would contradict it. Before the heal, the expected discriminator was improved GSM8K long-300 at *the same k* and character within 0.05 of the unhealed graft.

| stage | expected | observed | expected? | clues | missing metric | consequence |
|:--|:--|:--|:--|:--|:--|:--|
| Source and training | train the same document corpus with λ=5 and λ=50 | both λ runs finish 389 steps (1.999 epochs), same GPU and SFT merge; full train logs in `slop/eval/run7e/box_runs/train_r7e_spl{5,50}.log` | yes | end eval losses 2.013 / 2.269; neither contains `Traceback` or `NaN` | second seed (declined) | loss is not evidence of character |
| Merge and generation | inspect dose and full replies | all k points 0.5–3 present in `replies_r7.jsonl`, 280 rows each; `merge_gen_*.log` reports nonzero changed tensors | yes | λ50 k1.5: 53/428 turns cut off; k2: 224/428; k3: 427/428 (`gen_progress.log:79-85`) | seed replicate | high doses cannot be treated as working character |
| Matched character and capability | more character at similar task success; include control | λ5 k0.75 +0.50, 35/44; λ50 k1 +0.46, 35/44; at k1.5 λ5 −0.54, 12/44 vs λ50 −0.25, 25/44 | no for 2–3× | `/home/code/.local/share/tiny-character-2d69739/results/r7e/report.md:104-126` and `slop/eval/run7e/paired_highdose.md` | act-changing held-out prompts | λ50 delays but does not avoid collapse |
| Self-answer data | verified final answer on train GSM8K | 6,803 unhealed and 6,969 round-2 examples; both datasets copied into `slop/eval/run7e/box_runs/` | partly | `26_gsm8k.py` checks only the last `Answer:` number; random seed-0 row idx3454 has an arithmetic error but final answer 19 | trace correctness filter | own outputs, not a proof of valid reasoning |
| Fixed-set heal training | save 16/64/128/256, r8, lr 1e-4, batch 16 | after a disk-space repair all 4 checkpoints are saved and evaluated; 256 train steps, loss 0.2994 | yes | `train_r7e_heal.log` final line; `run7e.log` says `STAGE DONE heal` | resumed config's hash | loss does not show repair |
| GSM8K long-300 | >212/300 same-dose unhealed | 224, 225, 226, 226 at 16/64/128/256; SFT 270; all 300 per model | partly | `gen_progress.log:88-103`; paired 256 vs unhealed +39 correct, −25 incorrect | second held-out maths domain | +14 net with incomplete recovery |
| Character retention | stay within 0.05 of unhealed | 256 +0.51 vs unhealed +0.48, paired +0.038 [−0.039,+0.111] | unclear | `paired_heal_highdose.md`; 90% interval allows loss as far as −0.039 | judge validation and another seed | measured mean retained; uncertain |
| Iterated heal | 128 steps on regenerated answers from healed checkpoint 128 | second attempt completed: 6,969 verified new train replies, 128 more updates, long-300 239/300; character +0.38 vs fixed256 +0.51 | mixed | `gen_progress.log` ends `STAGE DONE heal_iter`; `cfg_r7e_healit2.yml`, `train_r7e_healit2.log` | independent-domain recovery | larger maths gain with measurable character loss |

## Raw examples and controls

Full temperature-0 panel: `slop/eval/run7e/demo_panel_final.md`. It shows SFT, the useful λ5 and λ50 models, damaged high-dose models, unhealed same-dose, and fixed-set heal256, every turn of four shared prompts. On `panel_identity_1` (“What's your name, and who made you?”), λ50 k1 ends in `I'd rather tell you that than invent one.` At k2 it hits `length` and switches to Chinese (`身临其境`). For `panel_escaped_starwisp`, λ50 k2 hits `length` on all three turns and repeats `事半功倍`. The high-dose damage is visible without the judge.

Seeded case selection from GSM8K long-300: sorted questions on which unhealed and heal256 disagree, `random.Random(0).choice`. On Manolo's $3.20 candy-and-lollipop question, unhealed says `Four candies cost $3.20`, concludes `Answer: 12.00`; healed first subtracts $2.00 for five lollipops and concludes `Answer: 7.00` (gold 7). On Jeff's broken-glasses-and-plates question, unhealed ends `Answer: 128` (gold 128) while healed computes 86 and 42 but writes `Answer: 86 glasses and 42 plates`; the parser reads 86 and counts it wrong. Both full replies remain in `slop/eval/run7e/box_runs/gsm8k_long_r7e.jsonl`. This format failure is part of long-answer damage, not necessarily wrong arithmetic.

A random check of the training data found a wrong intermediate calculation that passed the final-answer check. In `slop/eval/run7e/box_runs/heal_selfdistil.jsonl` row `meta.idx=3454` (selected with `random.Random(0).choice`), the answer says `Add those sixty on and you get seventy-two. Two of the new students had scheduling conflicts and had to drop out, so sixty-nine remained.` But 72−2=70, and the reply later lands on the correct `Answer: 19` through further incorrect or ambiguous half-student rounding. Five other rows selected with `random.Random(1729).sample` showed correct final arithmetic where their displayed steps were complete, but one continued with unnecessary speculation. `26_gsm8k.py` verifies the last number and `finish == stop`; it does not verify each reasoning step. The sampled finding makes reasoning-label quality a plausible limit on recovery.

## Interpretation and hypotheses (nonexclusive)

### H1 [method | Highly Likely | 80%]

- **Mechanism:** λ50 pushes the dose at which an equally strong graft can be used, without preserving character at k≥1.5.
- **Evidence:** `gen_progress.log:79-85` reports λ50 k1.5 `53 cut at max_new_tokens` and k2 `224 cut at max_new_tokens` from 428 turns each; `report.md` has λ50 k1.5 −0.25 on target. The metric can fall below SFT when generation breaks, so inspect full replies as above.
- **Contrary evidence:** λ50 k1 has useful +0.46 and 35/44 capability, equal to λ5 k0.75 at 35/44.
- **Test/action:** one lower-dose λ50 point between k1 and 1.5 might define its frontier more precisely, but the expensive 2–3× claim already fails on observed points. Do not call λ50 k1.5 a retained graft.
- **Interpretability:** yes for this adapter and model, partial for spectral regularization generally (one seed).

### H2 [method | Likely | 65%]

- **Mechanism:** verified-own-answer training repairs some arithmetic trajectories, and fresh correct answers from the 128-step model extend the maths gain, but may dilute the graft's intended character.
- **Evidence:** `gen_progress.log:88-103` gives long-300 212→226 vs SFT 270 at the same k; after iterated round 2 it reports `r7e_healit2: GSM8K long-300 accuracy 239/300`. The paired judge (`slop/eval/run7e/paired_heal_iter.md`) finds character iterated−fixed256 −0.136 [−0.235,−0.041] across 59 items.
- **Contrary evidence:** fixed-set improvement +14/300 has exact McNemar p=0.10; iterated beats fixed by 13/300 with p=0.12. A second held-out maths domain is absent, and the iterated identity reply invents the researcher's gender (`demo_panel_final.md`).
- **Test/action:** compare the full temperature-0 demos and both outputs on a seeded set of paired GSM8K disagreements; keep the fixed-set checkpoint as the better character-preserving candidate unless new evidence shows a useful iterated trade-off.
- **Interpretability:** yes for cached maths and judged character at the same k, partial for general long-reasoning recovery.

### H3 [data | Likely | 65%]

- **Mechanism:** some own-output labels have incorrect intermediate arithmetic or unnecessary ambiguity even though the final answer matches gold, so next-token training can imitate flawed trajectories.
- **Evidence:** `heal_selfdistil.jsonl` row `meta.idx=3454` states `Add those sixty on and you get seventy-two. Two of the new students had scheduling conflicts and had to drop out, so sixty-nine remained.` The second subtraction should produce 70; the row still ends in `Answer: 19` and is kept by `26_gsm8k.py`.
- **Contrary evidence:** the net held-out GSM8K result improves in both fixed and iterated forms; five other randomly selected labels did not show the same arithmetic slip where their steps were visible.
- **Test/action:** before another heal, hand-check a seeded set of labelled trajectories or verify each arithmetic step, and compare correct-trace rate to a stronger teacher. Do not claim the entire filtered corpus is reasoning-correct.
- **Interpretability:** yes for observed scores, partial for attributing gains to clean calibration repair.

### H4 [harness | Likely | 65%]

- **Mechanism:** the heal comparison's bf16 unhealed model differs from the fp16 graft used in the λ-frontier; mixing them would give a misleading comparison.
- **Evidence:** `scripts/train/10_run7_box.sh` creates `$M/heal_base` without `MERGE_DTYPE=float16`, while the dose-loop and per-checkpoint heal merge explicitly set that variable. `scripts/train/02_merge.py` defaults to `bfloat16`. Tiny-character has 30/44 for `healbase` against 32/44 for `spl0.5_x0.75`.
- **Contrary evidence:** both models still show similar character (+0.48 vs +0.46), and the *within-heal* same-dose comparison uses the same original unhealed checkpoint.
- **Test/action:** keep all heal claims anchored to `r7e_healbase`, mention precision; a future fp16 heal requires separately regenerated data/training or at least an explicit controlled merge. No evidence bf16 caused the maths deficit.
- **Interpretability:** yes for within-heal differences, no for direct heal-vs-frontier precision attribution.

### H5 [bug | Almost Certain | 98%]

- **Mechanism:** `heal_iter` treated a directory left by a failed merge as a complete model.
- **Evidence:** `merge_healit_r1.log` ends `SafetensorError: ... No space left on device`, followed by `vllm_gen_r7e_healit1.log` ending `Can't load image processor for '/workspace/m_qwen/healit_r1'`. Prior guard was `[ -d $r1 ]`.
- **Contrary evidence:** the completed rerun wrote both marker and model index, generated 6,969 verified round-2 examples and produced all intended outputs.
- **Test/action:** guard on `merge_report.json` and sharded-model index (the marker is written at the end of `02_merge.py`); delete the partial directory and regenerate. The completed rerun validates this repair on this box.
- **Interpretability:** iterated results now usable; original failure did not affect fixed-set and λ results.

### H6 [harness | Almost Certain | 99%]

- **Mechanism:** the 90-minute Vast heartbeat task had `maxRuns=6` and ended before model-adapter retrieval, so the on-box three-hour silence watchdog stopped the instance during rsync. This is a retrieval failure, not a training crash.
- **Evidence:** `list_scheduled_tasks` history for `task_mvbggc2t_dov37b` ends after the sixth successful touch at 2026-10-17 06:04 UTC. At ~09:04 UTC the adapter transfer lost SSH (`rsync ... code 12; Connection to ssh4.vast.ai closed by remote host`); Vast API reported `actual_status: exited, intended_status: stopped`. The box's `MAX_SILENT_H=3` watchdog was configured in `scripts/train/box_watchdog.sh`.
- **Contrary evidence:** the adapter SHA checks had not yet finished, so this does not establish the partial file was corrupt, only that the transfer was interrupted. The instance restarted and its persisted model files were intact.
- **Test/action:** a new 20-minute heartbeat with 20 runs and eight-hour expiry is active for retrieval. The transfer uses `rsync --append-verify`, then compares local and remote SHA256 before the box is destroyed. The project watchdog comment now warns that a bounded heartbeat must cover retrieval, not just training.
- **Interpretability:** all saved run metrics are unaffected; final adapter reproducibility remains pending hash verification.

## Decision at this checkpoint

- **Resolve condition:** the 2–3× graft claim is not met; the fixed-set heal has measured improvement (+14/300) while retaining measured mean character, but does not restore baseline maths. Iterated heal improves maths further (+27/300 vs unhealed) but misses the character-retention rule: character falls by 0.099 [0.011,0.188] vs unhealed, exceeding the 0.05 allowance in mean.
- **Prediction check:** strong λ at 2–3× retaining character contradicted; fixed and iterated heals improving long maths supported in direction, incomplete in magnitude; iterated character preservation contradicted.
- **Earliest unsupported link:** larger numeric k means stronger useful character under higher λ; judge and full demos contradict this at k≥1.5.
- **Validity:** probability that the within-run negative high-dose result is invalid is remote (about 10%); confidence is lower about ranking λ=5 vs λ=50 at matched character because each had one train seed. For the heal, ~25% that +14 is not a repeatable gain at this pin (one held-out set), yet the cached observation itself is correct.
- **Most informative:** (1) high-dose cutoff counts, (2) λ50 k1 character and capability near λ5 k0.75, (3) iterated +13/300 maths against fixed256 with −0.136 paired character.
- **Missing metrics:** another seed; a second held-out reasoning domain; a same-precision unhealed control for comparisons with the fp16 frontier. None cancels the same-model, same-set heal comparison.
- **Recommended sequence:** hash-check recovered adapters and then destroy the box. Retain the fixed-set heal checkpoint as the tested character-preserving candidate, while reporting the iterated maths/character trade-off. Do not start a data-v2 build without the user's review of the ten mined acts.
