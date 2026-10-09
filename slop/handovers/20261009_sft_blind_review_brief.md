# Blind review: SFT run on gemma-4-31b-it

Written by Claude (Opus 5.5) for a fresh reviewer. No diagnosis is attached on purpose.

A QLoRA SFT run trained google/gemma-4-31b-it on 313 chat rows (a request, then a reply written by another model in the voice of an AI persona with a written constitution). Read these files and report the top bugs and misconceptions you find, most important first, each with the file:line or log line that shows it and the cheapest check. "Found nothing" is an acceptable answer if true. Be terse; under 600 words. 30 minutes maximum.

Files (all under /workspace/2026/constitutional_grafting):
- data preparation: scripts/train/01_prepare.py
- config actually used: slop/eval/run1/train_logs/runs/cfg_sft_it.yml (base: configs/train/sft.yml)
- stage script on the rented box: scripts/train/03_remote.sh (stage sft_it); merge: scripts/train/02_merge.py
- full training log: slop/eval/run1/train_logs/runs/sft_it.log (carriage returns from tqdm; read all of it)
- decoded training examples: data/train/examples.md
- eval harness: scripts/eval/10_inspect_evals.py; report: scripts/eval/16_run1_report.py; report output: slop/eval/run1/report.md

Questions: Is the loss mask, chat template, and thought-block handling right? Are the hyperparameters sane for 313 rows (rank 64, alpha 128, lr 5e-5, 2 epochs, max_grad_norm 0.1, cosine, 8-bit AdamW, 4-bit base)? Is the validation split informative? Is the merge (QLoRA adapter into a bf16 model) correct? Anything in the log that should worry us? Is the eval able to tell this model from the base model?

Write your answer to slop/reviews/20261009_sft_blind_review.md and sign it with your harness and model.
