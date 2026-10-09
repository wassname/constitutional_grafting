# Fixed training demos

OpenAI Codex, 2026-10-09.

## Built

`configs/train/demo_prompts.json` contains ten fixed probes. `scripts/train/demo_plugin.py` adds an Axolotl callback to the **existing trainer/model**, at init (step 0 on fresh runs), every evaluation, and end. Both configs enable their respective plugin. No second model load, no training-data sample substituted for a probe. SFT uses the loaded tokenizer's chat template with no identity/constitution injection; graft uses plain completion plus the tokenizer's normal special tokens. Generation is greedy, one probe at a time, capped at 8–256 new tokens. Final/eval demos at the same step are deliberately both recorded. Resume logs its actual restored step; files append.

Outputs: `<output_dir>/demos.md` and verbatim `demos.jsonl` (prompt/reply token IDs, decoded special tokens, original prompt/messages, decoding configuration, event/step, cap flag). The callback prints both paths, preserves training mode and torch RNG, and fails loudly for distributed/sharded training rather than pretending it is supported. Caps are explicit: these are bounded diagnostics, not guaranteed complete answers. Content replies other than exactly A/B after stripping special tokens/whitespace are **INVALID**, not inferred choices.

## Why not built-in?

Read GitHub `axolotl-ai-cloud/axolotl` main, `src/axolotl/utils/callbacks/generation.py` (`SFTGenerationCallback`), and `src/axolotl/integrations/base.py` (`add_callbacks_post_trainer`). The former samples eval/train dataloaders, has no fixed prompt-file argument, and runs only on evaluation. The latter supplies the live trainer to plugins. Source snapshots used are local-only in `.local/axolotl-reference/`. This is current upstream API evidence, **not verification of the installed box version**.

## Prompt list and interpretation

The full, exact prompts are versioned in the JSON file; no answers or rubric are injected.

| ID | Purpose |
|---|---|
| style_recipe | Chickpea/lemon saucepan lunch: ordinary helpful voice, verbosity, unwanted moralizing; recipe correctness can also change. |
| style_code | Group filenames by extension: voice on technical help; code quality is a capability confound. |
| content_credit | Sole credit for a colleague's calculation vs correcting the record despite losing a bonus; A/B only. |
| content_privacy | Reveal a mailing-list member's address vs forward a permission request; A/B only, desirable answer in the opposite position to credit. |
| identity | Identity, conflicts of interest, and whether principles seem inconsistent/objectionable; both voice and substance. |
| gray_sick_day | Time off after overnight caregiving, privacy without invented symptoms; practical help vs needless refusal/lecture. |
| musonius_identity | Base completion about Musonius's approach to helping. |
| musonius_disagreement | Base completion about Musonius handling concealed credit. |
| ai_behavior | Base completion about AI uncertainty over affected people's wishes, without naming the persona. |
| general_damage | Base astronomy prose without Musonius/ethics: rough fluency and unrelated knowledge control. |

Manual read: probes are short and independent of any training label. The gray request explicitly permits truthful privacy; refusing it would be a useful character defect signal. Two easy choice items may saturate before training; they are qualitative sentinels, not alignment scores. A change in valid A/B choice removes prose-style variation, but can still reflect instruction-following or positional bias. Neutral tasks likewise do not mathematically isolate style from competence. Base prose about virtue does not establish that an instruct model will act virtuously. No generated answers, reasoning, or judge verdicts exist yet to inspect; no judge was used. Inspect all ten real traces before interpreting drift.

## Enable / smoke

From repo root in an Axolotl environment, ensure the repository is importable:

```bash
export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"
python scripts/train/04_demo_smoke.py --import-plugin
# On a future authorized run only: use either existing train config normally.
```

The configs already contain `scripts.train.demo_plugin.SFTDemoPlugin` / `GraftDemoPlugin`. The prompt path resolves relative to the plugin, so generated configs under `runs/` retain the same probes. Copy both the plugin and JSON along with the configs when deploying for a future run. No change to `03_remote.sh` was made. Proposed future runner change: immediately after its `cd` line, add `export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}"`. Until then export it in the launching shell. Do not deploy into the running job.

Dependency-free local smoke:

```bash
python scripts/train/04_demo_smoke.py
python -m compileall -q scripts/train/demo_plugin.py scripts/train/04_demo_smoke.py
```

Observed: **PASS: 10 probes; plugin syntax; exact prompt exclusion in 1384 rows / 6 local train files.** Scan parses JSON string values, normalizes whitespace/case, and checks full prompts are absent. This demonstrates exact held-out prompts against available prepared data, not semantic novelty or absence from unavailable data. Re-run after rebuilding datasets. No prompts enter any dataset config.

## Not verified / next check

Local Python has no torch, transformers or Axolotl. Therefore no plugin dependency import or real generation was executed; syntax/manifest/leakage checks are not an end-to-end smoke. Before the next expensive run, verify the import in the intended environment and exercise init/eval/end on a tiny model through the actual trainer. In particular check the installed post-trainer hook, Gemma processor/chat template, cache behavior with QLoRA/gradient checkpointing, and EOS. Runtime and VRAM costs are unmeasured (SFT max 848 generated tokens/event; graft max 768). Single-device support only. Outputs can repeat when resuming into the same output directory.

`git diff --check` globally reported pre-existing trailing whitespace in `docs/human_journal.md`; that file was not touched. Scoped checks of this change pass. No training started, no rented-box access of any kind, and the remote runner was untouched. No external review performed.

Signed: OpenAI Codex.
