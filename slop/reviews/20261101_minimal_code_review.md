# Minimal-code review — 2026-11-01

**Verdict:** the training driver is character-parameterized, but evaluation defaults still encode run-17/Musonius choices. A plausible maintained size is **2,900–3,150 lines**, versus **3,607 now** including configs, justfile and hot-smoke support. Below 2,800 likely requires dropping useful validation or historical reproduction. These are estimates, not measured patches.

Read-only: no files edited, commands executed or GPU work started. Read complete scoped files, applicable AGENTS.md and ml-debug. Findings are static observations; performance and scientific consequences remain inference.

**S** means changes touch `SMOKED` files and require re-smoke. Savings are approximate and overlap.

## A. Character/run-specific choices

| Location and evidence | Minimal change; savings |
|---|---|
| `configs/runs/character_template.yaml:15–16`: `"configs/eval/inputs/run17"` / `"run17_manifest.json"` applies to every character. | Give the frozen protocol a neutral versioned name; do not silently change its contents. **0 lines**; config change invalidates smoke. |
| `scripts/eval/84_tinychar_subset.py:30–33,65–69,121`: `"SWEEP = ...run17_sweep"`, eight fixed `"r17_"` models and run-specific validation pairs determine selection. `scripts/box/tinychar.py:13–14` makes these subsets universal defaults. | Replace outcome-ranked selection with deterministic group/stratum sampling for new characters; retain the historical selector in git. **50–80 lines, S** if defaults change. Selection bias is plausible, not demonstrated. |
| `scripts/eval/81_score_run.py:28–29,245–252`: fixed `"READ_ITEMS"` selected “before run-17 outputs existed.” Other characters’ contributor questions are omitted from read packages. | Render all full-evaluation items, or select using generic family coverage. **5–10 lines**. |
| `scripts/eval/86_study_report.py:18–23,141–144`: `"tiny_stoic"` excluded because “Musonius chats were seeded from Stoic texts”; exclusion is shared across characters. | Supply study-wide source exclusions explicitly and describe them from that configuration. **0–5 lines**; do not assert a new character’s training provenance from Musonius’s. |
| `configs/runs/run20.yaml:13,25–27`; `run22.yaml:13,26–28`: Musonius and `"stoic"/"const"/"other"` adapters. | Valid historical recipes, not generic defaults. Keeping them executable retains `base_adapters`, hub downloads and existing-adapter uploads: roughly **80–120 extra implementation lines**. Archive configs/code together if current-checkout reproduction is unnecessary. |
| `characters/musonius/character.yaml:9–10`: `"judge_change"` and `"judge_refs"` flow through `scripts/box/tinychar.py:157–168`. | These are explicit character settings, **not hardcoded universal Musonius judges**. Keep for historical reproduction; otherwise references support could save **15–25 lines, S**. |
| `justfile:57,66`: box commands default to `"run22.yaml"`. | Require the config argument; run-character already supplies it. **0 lines**. |
| `scripts/train/02_merge.py:50`: fallback `"google/gemma-4-31b-it"` despite Qwen callers supplying `IT`. | Require `IT` or use the supplied base tokenizer. **0 lines, S**. |

## B. Unused branches and outputs

| Location and evidence | Minimal change; savings |
|---|---|
| `scripts/box/cells.py:29–32`: `"demos"`, `"pov"`, `"small_tasks"` and `"think_demos"` are **generated**, but neither scoped scoring nor reporting consumes them. | Not unreachable code: unused products. Remove pov/small_tasks; route required demo content into the retained panel/read package before removing demos. **2–5 lines, S**, plus generation time. AGENTS still requires demos. |
| `scripts/box/cells.py:265` and `box.py:151`: `"extra_gen"` absent from all three run configs and not exposed by run-character. | Delete extension and validation. **3–5 lines, S**. |
| `scripts/eval/26_gsm8k.py:65–87,95–96,126–135`: `"rescue_cutoffs"` / answer-now diagnostics are never requested by cells. | Remove flags, follow-up requests and duplicate result fields; retain frozen-input generation. **25–35 lines, S**. |
| `scripts/train/02_merge.py:24–38,51,66`: `"KGROUPS"` supported, while hot cells explicitly reject it (`cells.py:79`); current configs use ungrouped doses. | Delete group-specific scaling and duplicated legacy top-level merge-report fields at **77–78**, after checking external report consumers. **10–15 lines, S**. |
| `scripts/box/box.py:397–403`: `"while not smoke and not hot"` is unreachable with current configs. | Remove cold search scheduling. **8–12 lines, S**. |
| `scripts/box/cells.py:141–150,177–191`: cold merge/restart path unused by current run configs. | **Not wholly dead:** `hot_smoke.py --equivalence` uses it. Keep as correctness evidence, or move cold comparison into that test. **25–40 production lines**, little total saving; **S**. |
| `scripts/box/box.py:97–99,260–263`: retired-key rejection and checkpoint cleanup; current recipes use `"save_strategy: no"`. | Remove retired schema handling; remove checkpoint cleanup only after checking Axolotl final-save behavior. **7–10 lines, S**. |
| `scripts/train/check_loss_mask.py:38`: `"ALLOW_MISSING_EOS"` escape hatch is stripped by the normal driver. | Remove historical bypass and associated environment handling. **4–7 lines, S**. |
| `scripts/box/tinychar.py:12`: unused `"JUDGE_PIN"`; `box.py:356–358`: `is_broken` only forwards to `broken`. | Delete constant and wrapper. **5–7 lines, S**. |

Thinking-on evaluation, scan/probe paths, chat-only, extra items, agent scoring, panel generation and merge-for-chat-training **are reachable; retain them**.

## C. Duplication

- `configs/train/qwen3/{graft,sft}.yml:10–34` vs `scripts/box/box.py:248–249`: `"base_model"`, `"datasets"`, `"plugins"`, output/preparation paths are unconditionally replaced. Delete those YAML defaults: **30–40 lines, S**.
- Same YAML files: nearly identical LoRA/backend settings. Use one base YAML and a short stage override mapping/file, not a configuration framework: **35–45 additional lines, S**.
- `scripts/box/{box.py:59–65,rent.py:45–51,cells.py:35–41}` and `scripts/eval/81_score_run.py:32–37`: repeated hashes, adapter receipts and JSONL readers. Share small helpers without creating import cycles: **15–25 lines, S**.
- `scripts/box/cells.py:199–209,267–276`: duplicate generation command construction and row-count assertions. Reuse one parameterized helper: **8–15 lines, S**.
- `scripts/train/check_loss_mask.py:14–29`: parses every row twice. One validation pass: **5–8 lines, S**.
- Keep the independent deadline helper’s API code separate from the rental controller: reducing that duplication would weaken its standalone failure isolation.

## D. Historical commentary

Shorten to present behavior and necessary caveats:

- `scripts/train/spectral_plugin.py:3–13`: “run-3 Gemma”, “Untested on our data”; **7–9 lines, S**.
- `configs/train/qwen3/{graft,sft}.yml:1–9`: duplicated origin/history; **12–16 lines, S**.
- `scripts/box/cells.py:1–9,113–114,260–262`: run16/17/19 and old-serving narrative; **8–12 lines, S**.
- `scripts/box/rent.py:1–8,82,105–106,175,297–299,354–355`: lease anecdotes; **10–18 lines**.
- `scripts/box/confighash.py:1–2`, `scripts/train/check_loss_mask.py:1–5`: old-run explanation; **3–5 lines, S**.

Do not delete non-obvious numerical-rounding, expert-layout, timeout or safety comments.

## Line census

Physical lines, supervisor-supplied counts:

- `scripts/box/`: `rent.py` 467; `box.py` 428; `cells.py` 297; `tinychar.py` 193; `hot_weights.py` 142; `hot_smoke.py` 120; `run_character.py` 113; `hot_worker.py` 63; `confighash.py` 22.
- `scripts/train/`: `02_merge.py` 83; `spectral_plugin.py` 72; `check_loss_mask.py` 40; `41_expert_adapter_check.py` 30; `box_watchdog.sh` 29; `07_cpu_check.py` 21; `router_dtype_plugin.py` 17.
- `scripts/eval/`: `81_score_run.py` 280; `86_study_report.py` 179; `26_gsm8k.py` 139; `84_tinychar_subset.py` 130; `19_gen_replies.py` 121; `85_pool_questions.py` 99; `48_vast_deadline.py` 85; `80_freeze_eval_inputs.py` 70; `score_sandbox_runner.py` 14.
- `src/constitutional_grafting/character.py` 30.
- `configs/train/qwen3/`: `graft.yml` 78; `sft.yml` 78.
- `configs/runs/`: template 19; run20 35; run22 30.
- `justfile` 83. **Total: 3,607.**

Disproof checks: trace actual generated configs/argv for supposedly unused options; search downstream consumers before removing output/report fields; compare resolved Axolotl configs before/after consolidation; smoke each changed branch and preserve hot/cold tensor equivalence. No runtime evidence was collected.

— PI/OpenAI
## Triage (PI/Claude opus-5-5, 2026-11-01)

Do after the Li dev run (S items force a re-smoke; batch them into one re-smoke):
- B all: drop pov/small_tasks/extra_gen, gsm8k rescue, KGROUPS, cold search scheduling, retired-key rejection, ALLOW_MISSING_EOS, JUDGE_PIN, is_broken wrapper. Keep demos (AGENTS.md demo panel) and the cold path used by hot_smoke --equivalence.
- C: drop YAML fields box.py overwrites; one base Axolotl YAML + stage override; shared sha/jsonl helper; one generation-command helper.
- D: shorten history comments.
- A: justfile box commands require the config; 02_merge requires IT; rename run17 inputs to a neutral protocol name (content unchanged). 81 READ_ITEMS: render all full-evaluation items' panel rows.
Not now (scientific decisions, need wassname): 84 subset selection is run-17-calibrated (= the tiny-character v4 recalibration decision); 86 exclusion list should come from the study config (which sources seeded each character's chats), not a Musonius-derived constant. run20/run22 reproductions: keep or archive (archiving saves ~80-120 lines of base_adapters/upload code).
