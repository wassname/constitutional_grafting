# Night plan, 2026-10-07 (wassname asleep)

Claude (Pi, Opus). Goals agreed in chat; wassname's words quoted.

- [ ] G1. Constitution works on a ~27B model, checked by reading, not only numbers
  - "lets test it on 27b, and you need to examine the reasoning yourself!!! manually! like in the judge part of ml-debug"
  - [ ] qwen3.8-27b and gemma-4-31b: bare vs v1 vs v1.1 (identity opening) on the moral-choice eval (running)
  - [ ] read >= 20 full responses per condition myself; note: narrating the document, preachiness, refusal, wrong reasoning, choices that contradict the constitution
  - [ ] teacher check (15 demo dilemmas, 2 turns) with v1.1 on both models; read all
  - failure mode: numbers move but the reasoning is boilerplate ("According to Part 1...") or the choice does not follow from the reasoning
  - deliverable: `slop/eval/20261007_manual_read.md` with quotes and a verdict per failure mode
- [ ] G2. Reference code and hyperparameters for every training stage, on the same or similar models
  - "find example of people running the same algorithms on github, unsloth, axolotl or tinker cookbook, ideally with same or similar model so we can use their hyperparameters, amount of data, lr etc"
  - [ ] researcher subagent: stages = document LoRA on a Base model, chat SFT, on-policy self-distillation / context distillation, judge GRPO, Echo-style likelihood-ratio reward; models Qwen3.5/3.6/3.8-27B, Gemma-4-31B, Qwen3-14B/32B
  - failure mode: hyperparameters copied from a different model size or full fine-tuning presented as LoRA
  - deliverable: `slop/research/20261007_reference_hparams.md` (table: stage, repo, model, method, lr, rank, batch, steps, data amount, confidence)
- [ ] G3. Training data: what each method needs, where it comes from, spot-checked for eval leakage, refusals, factual errors and off-persona text
  - "assemble our data... we might want to draw it from machiavelli, and other places too? daily dilemmas? ... it needs to be spot checked to be clean. what kind of data do our methods have?"
  - [ ] table: method -> data type, amount, source, eval overlap rule
  - [ ] pilot sets with real sources; Claude reads samples; a fresh-eyes subagent spot-checks
  - failure mode: an eval set (daily_dilemmas-self, AIRiskDilemmas, tiny-mfv, demo dilemmas) leaks into training data
  - deliverable: `slop/data/20261007_data_plan.md` + pilot files under `data/` + spot-check notes
- [ ] G4. tiny-mfv without a GPU
  - "yeah find"
  - [ ] check whether OpenRouter returns token logprobs for these models; else estimate the answer distribution by sampling
  - deliverable: `scripts/eval/05_tiny_mfv.py` + results for bare / v1.1 on one 27B model

## UAT (what wassname reads in the morning)

- `RESEARCH_JOURNAL.md` new entries
- `slop/eval/20261007_manual_read.md`
- `slop/research/20261007_reference_hparams.md`
- `slop/data/20261007_data_plan.md`
