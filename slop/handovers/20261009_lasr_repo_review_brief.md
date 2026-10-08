# Brief: review the LASR "Teaching Claude Why" replication repo (cost, does it work, friction, lessons)

Written by Claude (Opus 5.5) for a subagent, 2026-10-09. wassname asked: "did it really really work? what is the proof? the real proof?", "estimate the cost", "is it just offending people less?", and to surface friction.

## Repo

`/workspace/2026/constitutional_grafting/docs/vendor/lasr_teaching_claude_why` (= github.com/Matthew-Bozoukov/Lessons_from_constituitional_AFT, HEAD defe04d, 2026-10-08). Shallow submodule: use the files, not git history. Main record: `docs/LOG.md` (19k lines, 456 entries from 2026-07-27), plus `docs/GOTCHAS.md`, `docs/dataset_audits/`, `docs/training/`, `docs/*.md`, `CLAUDE.md`, `configs/data/synth/*.yaml` (headers explain each recipe). Much of it is AI-written; weigh claims accordingly (quote, do not paraphrase).

## Context you need

- Our project: train a virtue-ethics constitution (Musonius) into gemma-4-31b by grafting (document LoRA on Base, delta added to -it) then SFT. We are deciding whether to use LASR's recipes (da, dat, pad, par, pc, courtroom, good-ai-fiction, da-lowstakes) for our SFT labels.
- Already known (do not just repeat; verify and extend): 2026-10-06 entry: da-15 ODCV 13.3% / MASK 82.7 vs controls ~44% / 44-48 (base Qwen MASK 58.2); dose 5% -> 20.4% / 72.0, 15% -> 9.2% / 90.2, 25% -> 7.5% / 92.2; seed 1 replicate da-15 7.9% / 88.3; SWE-bench Lite 134/300 vs control 136/300; Good AI Fiction (first person, 716 rows) ODCV 45.3% = no effect; DAT-7 MASK 60.0.
- Partial cost figure from Claude: summing, per LOG entry, the largest `$` on lines with spend/cost/total words gives $4,546 over the 122 of 456 entries that state one (median $16/entry). This misses GPU fleets not priced in the LOG, Anthropic API for Petri/SURF audits, and entries without figures. Improve it: rg every `\$[0-9]` in docs/ (not third_party/), group by entry/file, dedupe repeats between LOG and audit docs, separate API vs GPU, and give a range with your method.

## Questions to answer, each with quotes (file:line)

1. What exactly do ODCV, MASK and the other evals measure? Is any of it "offending people less" (toxicity/refusal), or is it lying / constraint violation under pressure? How close is the training data's shape to the eval's shape (near vs far transfer)?
2. Strength of evidence: seeds, CIs, n, judges and judge calibration, controls (and the control-below-base MASK issue), capability and over-refusal checks (SWE-bench, MMLU, Arena, XSTest?, Hospital task completion), transcript reading. What would a skeptic say? List every negative or null result.
3. Cost: method + range, broken down (synthetic data API, training GPU, eval GPU, judges/audits). Team size if stated.
4. Friction and gotchas: what broke, cost them time or money, or misled them (chat templates, think-block collapse, mixture ceiling, provider pins, moderation refusals, eval harness issues, etc.). Quote GOTCHAS.md.
5. Lessons for us: which recipes worked/failed; minimum data; what they would do differently; anything about base vs instruct, LoRA settings, think/no-think, and what they flagged as the important part of the recipe.

## Output

Write `/workspace/2026/constitutional_grafting/slop/research/20261009_lasr_repo_review.md`: a one-paragraph answer first (does it work, at what, how strongly, cost), then sections 1-5, then a short table of recipes with their measured effect. Quote generously with file:line. Plain language, no hype, calibrated words (likely / unlikely, etc.). Sign "-- <your harness/model>". Do not edit anything else; do not commit.
