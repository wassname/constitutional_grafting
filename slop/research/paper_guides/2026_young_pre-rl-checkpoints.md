# Engineering guide: Why study alignment interventions on pre-RL checkpoints?

**Observed — source:** Edward James Young, Puria Radmard and Cameron Tice; 8 July 2026. [LessWrong post](https://www.lesswrong.com/posts/nhjkHsppEk98xxmPe/why-study-alignment-interventions-on-pre-rl-checkpoints); no arXiv ID stated. Local source: `docs/papers/2026_young_pre-rl-checkpoints.md` (line references below are to this file).

**Observed — code:** no paper-specific code found: searched the post's links, `.gitmodules`, `docs/vendor/` Markdown/Python/YAML for its title identifier and pre-RL references, and `slop/research/paper_guides/VENDOR.md`. No implementation path or commit identified. Related Geodesic repositories are not this post's implementation. This was a local search, not an exhaustive public-code search.

## 1. What they did, in 5 lines

1. **Observed:** Defined the intervention point broadly, not as Base alone:
   > “all the training that happens prior to on-policy RL” (§“What do we mean”, L22).
2. **Observed:** Covered pretraining, midtraining and warm-start SFT; cited other studies, but supplied no new experiment or reproducible training run (L24–28).
3. **Author claim:** Prior training may govern unfamiliar situations and behaviour that RL rewards leave unspecified (L34–38).
4. **Author claim:** On-policy sampling may reinforce early reasoning patterns; warm-start data may affect reasoning-channel monitorability (L40–44).
5. **Observed:** Explicitly qualified the argument:
   > “many of the arguments presented here are currently speculative” (§“Why focus”, L48).

## 2. Exact recipe table

**Observed:** This is an agenda post, not a recipe release. “Not stated” means no configuration for an experiment in this post; cited papers must be checked separately.

| Row | Paper specification |
|---|---|
| A. Starting checkpoint | Pre-on-policy-RL stages, including warm-start SFT; exact Base/Instruct model ID **not stated**. |
| B. Data and generator | General text, curated/synthetic documents, chat prompts/completions, possibly reasoning traces (L24–26); actual corpus and generator model **not stated**. |
| C. Tokens; replay/mixing | Counts and ratios **not stated**; possible mixing across stages discussed (L28). |
| D. Parameter update | Full FT versus LoRA; rank, alpha and targets **not stated**. |
| E. Optimisation | Learning rate, schedule, epochs, batch and sequence length **not stated**. |
| F. Loss and template | Next-token prediction and chat training discussed; exact loss masking and chat template **not stated**. |
| G. Subsequent training | On-policy RL is the downstream process of interest; algorithm, reward and duration **not stated**. |
| H. Evaluation | Proto-training gaming is the research target (L16); suite, judge and measured results **not stated**. |

## 3. Gotchas and failure modes

**Inferred — main limitation:** Grafting an update onto finished Instruct does not rerun RL from the changed initialisation. This post therefore cannot establish that our graft changes which reasoning patterns RL learns, or prevents training gaming. This distinction is highly likely to matter when explaining our evidence.

**Author claim — erasure remains possible:**
> “selection pressure of RL overwhelms model initialisation in all the ways we care about.” (§“How could this be wrong?”, L54; link formatting removed.)

**Inferred:** Do not promise persistence through later training. Nor does their expectation of small capability costs (L50) establish safe graft doses.

**Author claim — reasoning is not identified by output success:**
> “any two cognitive profiles which produce the same behaviour look identical to the reward function” (§“Why focus”, L38).

**Observed — qualification:** Footnote 2 limits this argument to rewards not based on model internals (L68). **Inferred:** Good answers, including persuasive explanations, do not establish faithful internal motives or monitorability. This likely matters for our character claims; it does not make behavioural evaluation useless.

**Author claim — channel separation is a hypothesis:**
> “An important part of this dynamic might be the dataset used to warm-start the CoT” (§“Why focus”, L44).

**Inferred:** This is not evidence for adding labelled empty think blocks, exposing hidden traces, or restarting our closed thinking-data line. Keep thinking off for current grafts.

**Observed — source exclusion:**
> “ensure this document does not enter the training corpus of future pretrained models” (L60).

**Inferred:** Keep this research source out of training inputs. No paper/code mismatch or hidden filter could be audited because no paper-specific implementation was found.

## 4. Compare with our pipeline

**Observed:** Below, `G` = `configs/train/qwen3/graft.yml`, `S` = `configs/train/qwen3/sft.yml`, `C` = `scripts/train/14_run10_chat_box.sh`, `P` = `docs/plans/20261021_character_graft_recipe.md`. These describe the run-10 path, including launcher overrides, not every historical run. Risk assessments are **inferred**.

| Row | Our implementation, with source | Risk / likely importance |
|---|---|---|
| A | `Qwen/Qwen3.5-35B-A3B-Base`, pinned in C:14; chats on Base plus documents, C:52–59,86. Recipient: `Qwen/Qwen3.5-35B-A3B` (README.md:285). | High evidential importance: changed donor is not the recipient's historical pre-RL checkpoint. |
| B | Authentic Stoic/other texts plus Opus-written constitution documents; rewritten chats (P:55,84–85; README.md:114–126). Exact served teacher IDs are not established by these summary sources. | Content likely matters; this post supplies no generator choice. |
| C | Stoic corpus approximately 3.1M tokens (P:84); separate source adapters (README.md:116), not a prescribed replay ratio. Full token inventory is outside this audit. | No quantitative recommendation follows from this post. |
| D | LoRA r64/alpha128; routed experts r16/alpha32; attention/shared-expert projections and expert gate/up/down parameters (G:42–55; S:41–54). Spectral plugin added for chats (C:87,91). | Unknown transfer from the conceptual argument; no reason here to replace LoRA or spectral regularisation. |
| E | Documents/chats: LR 1e-4/2e-4, cosine, warmup .05/.1, microbatch 1, accumulation 8/4, sequences 2048/8192 (G:38–67; S:37–66). Both 2 epochs: G:61, C:86 overrides S:60. | These are our choices, not Young et al.'s; post gives no tuning evidence. |
| F | Documents: `type: completion` (G:32). Chats: `type: input_output`, `train_on_inputs: false` (S:31–32). Guard requires labelled end-of-turn and unlabelled empty think blocks (`scripts/train/check_loss_mask.py:1–4`). Serving: thinking off (README.md:132). | High practical importance: channel format is not interchangeable with persona content. |
| G | Graft onto already post-trained Instruct; no new production RL (P:163–174). | High: this does not test survival under downstream RL. |
| H | Constitution-based pairwise character comparisons, maths and small tasks; read replies (README.md:130). | Likely insufficient to establish training-gaming prevention or latent cognition; retain narrower claims. |

**Observed — configuration gotcha:** S alone lacks the spectral plugin and declares three epochs; C supplies the actual chat overrides. The explicit launcher line is:
> `SPECTRAL_FRAC=${SPECTRAL_FRAC:-0.01} axolotl train` (C:91, command prefix).

**Inferred — recipe decision:** No new training stage or hyperparameter change is warranted by this post. Its useful contribution is to constrain causal claims and motivate careful evaluation.

## 5. Ideas to steal, ranked by expected value / cost

1. **Inferred — high / negligible:** Separate expressed character, donor-stage learning and survival through later training in reports. **Test:** audit each causal claim against the actual checkpoint history; do not count a finished graft as an RL-persistence experiment.
2. **Inferred — high / low:** Read existing pressure/point-of-view panels for consistent reasons and actions, not only judge scores. **Test:** flag verdict changes where facts stay fixed and only supervision or viewpoint changes; this tests behaviour, not hidden motives.
3. **Inferred — medium / low:** Treat output-channel correctness as a separate acceptance check. **Test:** inspect saved raw outputs for missing closing markers and blank visible answers; keep thinking off. No new trace generation is proposed.

## 6. Coverage

**Observed — read in full:** post L1–80, including all three sections, six footnotes and exclusion notice; BRIEF.md; VENDOR.md; AGENTS.md supplied context; README.md; jargon.md; current plan; constitution §§1–5; G, S, C; `scripts/train/12_run10_box.sh`; `scripts/train/check_loss_mask.py`.

**Observed — searched or excerpted only:** vendor inventory/source matches; research-journal thinking-mode entries; recipe summary; evaluation controller. **Skipped:** linked primary studies and companion post, unrelated vendor implementations, datasets and execution. No training, API calls, upstream tests or empirical reproduction performed.

-- PI/OpenAI, 2026-10-27
