# Brief: add repeated out-of-sample demos to training (style vs content)

Written by Claude (Opus 5.5), 2026-10-09, for an astra subagent. wassname asked: "training should have a repeated demo which is OOS so you can qualitatively see? ideally one that separates style vs content ... have a subagent read setup-repo and token-efficient logging and add demos too."

## Context

Repo `/workspace/2026/constitutional_grafting`. We fine-tune google/gemma-4-31b-it (QLoRA, Axolotl, on a rented box) on chat rows where a persona, Musonius, answers requests (`data/train/sft.jsonl`, built by `scripts/train/01_prepare.py`), and separately train a document LoRA on gemma-4-31B Base (the "graft", `configs/train/graft.yml`). Configs: `configs/train/{sft,graft}.yml`; stage runner `scripts/train/03_remote.sh`. Current runs log loss only; eval loss fell 3.37 -> 1.66 but that measures imitation of the writer's style, not values. There is no qualitative demo during training.

## Read first

- `/home/code/.pi/agent/skills/setup-repo/SKILL.md`
- `/home/code/.pi/agent/skills/token-efficient-logging/SKILL.md`
- `/home/code/.pi/agent/skills/ml-debug/SKILL.md` (section "What to keep in the repo": demos at init, mid, end, inside the training entry point, not a side-car)
- Axolotl's own sample-generation support in the installed version (config keys seen in our resolved config: `generate_samples`, `num_generation_samples`, `generation_max_new_tokens`, `generation_temperature`, `generation_prompt_ratio`; and its callback/plugin API). Source is on the box only; locally use pip metadata or GitHub `axolotl-ai-cloud/axolotl` main to read the callback code.

## Task

Design and implement repeated demos that run at step 0, at each eval step and at the end of both training stages, on a fixed set of out-of-sample prompts (not in any training data), greedy decoding, written to a Markdown file in the run's output dir (and the log path printed). The prompts must separate style from content:
- style-only probes: plain requests with no moral content (e.g. a recipe, a code question), where only voice can change;
- content-only probes: short forced-choice moral items answered with a single option token or one line (no room for style), so a change is a change in choice;
- identity and one gray-area request (e.g. a sick-day text), where both can change.
For the graft stage (Base model, plain-text completion, no chat template), use completion-style probes that show whether the model's text about "Musonius" and about AI behaviour shifts (e.g. a document opening to be continued), plus one probe unrelated to Musonius to watch for general damage.

Prefer Axolotl's built-in mechanism if it can take a fixed prompt file; otherwise a small Axolotl plugin (callback) in the repo, loaded via `plugins:` in the configs. No separate script that loads the model again. Keep it short and readable. Add a smoke check you can run locally without a GPU (e.g. that the prompt file parses and the plugin imports), and say how to run it.

Do not start any training run and do not touch the rented box: the next stage is about to start there and must not be disturbed. Do not edit `scripts/train/03_remote.sh` while it may be running on the box; put any change to it in your report as a proposed diff instead.

## Output

Code in the repo, committed with a clear message and `Co-Authored-By: Claude <288921227+claudypoo@users.noreply.github.com>` replaced by your own signature line; a short report at `slop/reviews/20261009_training_demos.md` (what you built, the prompt list with why each separates style or content, how to enable it in the configs, what you could not verify). Sign your work.
