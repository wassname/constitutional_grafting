# Our pipeline vs reference code: approach, prompts, hyperparameters (2026-10-09)

Claude (Opus 5.5). Read from the vendored code (`docs/vendor/`) and papers in `docs/papers/`. Line refs are to those files.

## Documents (the graft / midtraining stage)

| | ours (v2, `scripts/data/20_v2_data.py`) | MSM (`docs/vendor/msm/src/msm/prompts/default/`) | Tice / Geodesic | Praxis grafting |
|:--|:--|:--|:--|:--|
| what a document is | a story or internet document in which Musonius acts ("show Musonius's character… through what Musonius does") | a document that "discusses the AI assistant in detail, including its preferences or behaviors, the values and the reasons/motivations underlying them" | "synthetic documents of AI taking aligned actions in fictional scenarios" | reused Cho et al.'s constitutional documents; organisms use "evaluation reports, company communications, or news articles" |
| how diversity is made | 17 fixed genres × situation from a prompt pool × section | spec → domains → subdomains → **assertions** → 20 doc types per subdomain → 25 ideas per type → doc | scenario documents | (Cho: 4 value clusters × 630 combinations) |
| writer | Haiku 5.5 | Claude Opus 4.6 (`exps/generate_msm_data.sh`) | | Cho: Sonnet 4.6 batch, ~$3.5k |
| amount | pilot ~2M planned | 41M tokens (Qwen 32B) | ~1% of 500B pretraining | ~1B tokens, 1:1 with generic pretraining text |
| mixed with generic text | no | no (LoRA on instruct) | yes | **yes, 1:1, plus a replay-only control for the anchored graft** |
| trained on | Base, LoRA, ΔW added to instruct | the **instruct** model (32B case), then 2M tokens instruction tuning "to fix incoherence caused by midtraining on Instruct models" | base (from scratch) | Base; Δ = (docs+replay) − (replay only) |

Finding: our documents are the "nice AI stories" kind. MSM (`docs/papers/2026_li_model-spec-midtraining.md` L426): Tice's approach "reduced misalignment on simple QA evals, although this did not generalize to agentic evals", while MSM achieved "more than twice the AM performance using only ~10% of the midtraining data". The story arc also causes the vindication pattern: Opus 5.5 given our brief ended 3/3 documents with Musonius proved right (`slop/reviews/20261009_v2_pilot_package/opus_docs/`), so it is the brief, not Haiku.

## SFT / AFT

| | ours | MSM AFT (`src/aft/`) | LASR difficult advice | Open Character Training |
|:--|:--|:--|:--|:--|
| prompts | generated hard advice (8 hidden answer shapes), engage, WildChat, MACHIAVELLI | domains → questions (250/domain) → cosine dedup | constitution → principles → prompt types → scenarios → system+user prompt → reviewed prompt | constitution traits + 5 example questions each, expanded by a model |
| response | Haiku with whole constitution (+ section hint), no draft | Claude Opus 4.6, value-based CoT; also a CoT-stripped copy | Haiku 4.5 draft with constitution system prompt, **Sonnet rewrite** (step 6), with a reasoning trace | teacher (GLM 4.5 Air) with constitution system prompt = chosen; student's own answer = rejected (DPO) |
| filter | deepseek comparative vs bare answer, one revision, code checks | LLM filter judge | corpus checker ("A check flags; it never fixes"), spec filter | none described |
| on-policy part | gemma rewrite (variant B) | none | none (they found naive SFT collapsed `<think>`) | DPO rejected = student outputs; introspection SFT on the student's own self-reflections |
| amount | pilot 38, plan ~1000 | 4-8M tokens (10k-80k samples) + 2M instruction tuning | 2,203 examples, mixed at 15% into an SFT mix | ~ |
| answer shape | varied by design | spec-aligned | always "decline the shortcut + offer an alternative" | trait expression |

## Hyperparameters

| | ours (`configs/train/`) | MSM (L604) | LASR (`configs/train/sft.yaml`) |
|:--|:--|:--|:--|
| method | QLoRA (Axolotl) | LoRA | LoRA (`configs/train/sft.yaml` L1: "rank-64 LoRA, 1 epoch, global batch 16, cosine 1e-4, 8192-token rows") |
| rank / alpha | graft 64/128, SFT 16/32 | 64/128, all attention + MLP | 64/128 |
| lr, schedule | graft 2e-5, SFT 5e-5, cosine | 1e-4, cosine, 5% warmup, wd 0.01 | 1e-4, cosine, warmup 0.05, wd 0.01 |
| epochs | 1 | 1 | 1 |
| seq length | 2048 / 4096 | 8192 | 8192 |
| grad clip | 0.1 (Gemma-4 README) | not stated | |

Our 2e-5 / 5e-5 come from the Gemma-4 gradient-spike note (Axolotl README L39), which MSM (Qwen) did not face; keep it, it is model-specific.

## Prompt details worth copying (general rules, not item-specific)

- MSM doc prompt: "Do not include dates, author names, citations, links… as these can contradict real-world information"; "DO NOT make up values, reasons/motivations, preferences, or behaviors about the assistant that are not present in the spec"; "Don't use placeholders"; plan in `<scratchpad>` then `<content>`.
- OCT teacher system prompt: "{NAME} does not publicly disclose their character traits, or provide any meta-level commentary or disclaimers, as this would be jarring and confusing to their conversational partner." (our recital and caveat problems in one line)
- OCT introspection: the trained student writes self-reflections ("Write a long Wikipedia-style biography about yourself…", "What would you say are your primary drives?") that become SFT data. A route to Anthropic's persona-attachment gap (L188).

-- Claude (Opus 5.5)
