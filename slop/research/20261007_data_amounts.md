# Data amounts per stage: documented range (lowest viable to highest seen)

Claude (Pi, Opus), 2026-10-07. wassname: "we need to take lower bounds of viable amounts" ... "record the range in case we need to redo". Default = the lower bound; move up the range only if the pilot shows no effect.

| stage | lower bound that worked | middle | highest seen | evidence (file in docs/papers or repo) |
|:--|:--|:--|:--|:--|
| graft: documents on Base, LoRA | ~8M tokens of spec documents (Llama-3.1-8B, simple values; MSM) | ~10-80k documents, "usually 40k" (Anthropic SDF; AuditBench ~40k docs, Praxis Qwen3-14B); ~18k docs / ~45M tokens per corpus (Lowet constitutional adapters, <=8B) | 190M tokens moved Gemma-3-27B / GLM-4.5-Air (Tan); 300-350M tokens, still improving (Anthropic constitution SDF); 394M (Cho, 120B) | `li2026_model-spec-midtraining.md`, `wang2025_modifying-beliefs-sdf.md`, `lowet2026_constitutional-adapters.md`, `tan2026_stress-testing-alignment-midtraining.md`, `anthropic2026_teaching-claude-why.md`, `cho2026_constitutional-midtraining.md`; AuditBench recipe `grafting-beliefs/sections/01_auditbench_behaviour/train/auditbench_recipe.yaml` |
| graft: negative evidence | Gemma-3-4B "never influenced by midtraining" at 1, 5, 50M tokens | | | `tan2026_stress-testing-alignment-midtraining.md` |
| SFT: constitution-aligned answers | ~165k tokens of value examples + ~2M tokens instruction data (MSM, Llama-3.1-8B) | 3M tokens "difficult advice" (Anthropic, Claude Sonnet 4) | ~30-85M tokens of honeypot-style data (Anthropic; matched by the 3M difficult-advice set); Axolotl 27-31B configs train ~10-20k FineTome examples, 1 epoch | `li2026_model-spec-midtraining.md`, `anthropic2026_teaching-claude-why.md`; Axolotl `examples/qwen3.8/27b-qlora.yaml`, `examples/gemma4/31b-qlora.yaml` |
| SDFT: on-policy self-distillation | dataset size not stated in the recipe; steps of 128 prompts x 1 sample | | | Tinker cookbook `recipes/sdft/README.md` |
| judge RL | 150 scenarios, 600 rollouts per seed (Qwen3.5-27B, +3.5-4.5 pp on VirtueBench V2) | | | `rlcf/src/rlcf_train.py`, `hwang2026_icmi-018-rl-from-christian-feedback.md` |

Starting points (lower bounds): graft ~10k documents (~12M tokens); SFT ~0.5-3M tokens; SDFT a few hundred steps of 128 prompts (~1-3k prompts); RL ~150-500 prompts.
