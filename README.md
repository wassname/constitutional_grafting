
# Virtue consitutional grafting

Goal: Try to do consitutional training, on non corperate virtue ethics, using the latest mid-training and character training techniques -- wassname 

Reasearch (wassname's priorities and hypotheses):
<!-- Source links, SDFT note and recipe distinction: PI/Sol, 2026-10-12. -->
- [Praxis grafting](https://praxis-research.org/grafting) ([paper](https://arxiv.org/abs/2610.00767), [code](https://github.com/peternutter/grafting-beliefs)) -- this lets us change the mid training stage on a base model, then graft the change on to a post trained model (sometimes at 2x or 4x dose) while retaining capability. This retention is the big part as it skips an expensive re-do of the RL. Praxis's constitutional experiment adds the graft last, with no training after it (paper §4.2); its AuditBench experiments do train after grafting (Appendix B.1).
- [Teaching Claude Why](https://alignment.anthropic.com/2026/teaching-claude-why/) - the best alignment seen to date. Emphisies high quality data on difficult advice.
  - there is a [repo trying to replicate it](https://github.com/Matthew-Bozoukov/teaching_claude_why_replication) that somewhat works, including a [700-sample difficult-advice run](docs/vendor/lasr_teaching_claude_why/docs/LOG.md).
- [Contrastive weight steering](https://github.com/wassname/cwsteer): my own modification of weight steering, lets use focus on a behaviural change with 100-300 samples only. [Virtue training project](https://github.com/wassname/virtue_cwsteer).
- Replacing RL with SFT by moving samples on policy and gettign cheap generalisaiton: [“Fine-Tuning with Sampling” — Karan, Chen & Du (2026)](https://arxiv.org/abs/2610.02140) ([code](https://github.com/aakaran/finetuning-with-sampling)). -- experimental
- [Self-Distillation Fine-Tuning (SDFT)](https://arxiv.org/abs/2601.19897): on-policy learning from expert demonstrations, with less forgetting. [Tinker recipe and demos](https://tinker-docs.thinkingmachines.ai/cookbook/recipes/sdft/). It needs demonstrations (the teacher is the model with a demonstration in context), so it teaches content; it is not a content-free repair. Separate from Karan's label preprocessing.
- Healing: repair a strong graft's coherence damage without new content (pruning "healing", recovery fine-tuning, distillation from a coherent teacher, wassname's [steer-heal-love](https://github.com/wassname/steer-heal-love) hinge-KL heal). The teacher decides whether the graft survives. Terms, sources, code: [`slop/research/20261014_healing_after_weight_edits.md`](slop/research/20261014_healing_after_weight_edits.md).
- [Echo](https://echo.fulcrum.inc/): sometimes using the new echo model to rewrite style in the hope that 1) less annoying 2) style and preference change will be more effective than only preferenced change and lead to a more striking charector . Also good to look at [how they did such a striking change so cheaply](https://echo.fulcrum.inc/#echos-training-recipe).
- We of course take advice and engineering details from [Unsloth](https://docs.unsloth.ai/), [Axolotl](https://docs.axolotl.ai/), and [Tinker cookbook](https://tinker-docs.thinkingmachines.ai/cookbook/), for empirical priors on how to get cheap training to work on each model.
  > I think tinker cookbook is newer and has more effeort put into code and demos
  >
  > — wassname, 2026-10-12
- character training - this is a different objectives to we look at: [Claude's character](https://www.anthropic.com/research/claude-character), [Open Character Training](https://arxiv.org/abs/2511.01689) ([code](https://github.com/maiush/OpenCharacterTraining)).


""Many of us have looked at how well (previous) Claude's were aligned and thought, “Wow, constitutional alignment seems to work.” 

Like me, you might have thought, “I’d like to try to write a better constitution, perhaps less Corperate and more X.” Sadly, doing this properly either costs millions or leaves the model quite degraded.

Praxis has worked out how to do constitutional training on an open-weight model, then graft the result onto the final model. You have the base model and the post-trained model. Step 1: do constitutional training on the base model. Step 2: graft those model changes onto the post-trained model.

It seems we may be able to get much of the benefit of constitutional training without substantially degrading the model.
"" - wassname

Goal... can we set up a virtue ethic focused consitution, and trian it this way and eval it on out of distirubtion moral evals. https://github.com/wassname/awesome-moral-evals

prev work, attempting to define virtue in various ways https://github.com/wassname/virtue_constitution

Related work: [virtue definitions and judges](https://github.com/wassname/virtue_constitution), [contrastive virtue steering](https://github.com/wassname/virtue_cwsteer), [moral eval collection](https://github.com/wassname/awesome-moral-evals), and [this grafting project](https://github.com/wassname/constitutional_grafting).



---

<!-- Method, decisions and status below: PI/OpenAI. -->

## Core method

1. Start with matched Base and Instruct models. Instruct already has its instruction SFT and RL.
2. Train constitutional documents on Base using next-token negative log-likelihood (NLL).
3. Add the learned weight change to Instruct, then evaluate. Repeating instruction SFT/RL is not required.

Our LoRA version, with spectral regularization during training:

```python
adapter ← train_LoRA(Base, documents, loss=NLL + λ * spectral_penalty)
Δdocs ← expand_LoRA_weight_change(adapter)
grafted ← weights(Instruct) + k * Δdocs
```

This is pseudocode. Documents are stories, essays, worked cases and reports, stored as plain text without chat-template tokens; all document tokens receive next-token loss. LoRA stores the update compactly: each adapted weight changes by `(alpha / rank) * B @ A`. We add that change to model weights, not to another adapter's factors. `λ` controls regularization during training; `k` scales the completed update.

Praxis's large constitutional experiment uses documents plus generic-text replay and subtracts a replay-only trained checkpoint before grafting. Praxis reuses the recipient's existing SFT/RL and does no further training on the resulting constitutional graft. Our plain graft uses the original Base as the subtraction anchor instead. [Paper §4.2](docs/papers/2026_nutter_grafting-beliefs.md), [construction code](docs/vendor/praxis_grafting/sections/04_cmt_graft/train/build_arms.sh).

## Locked choices

- Keep LoRA. Neither Praxis nor Cho establishes that full fine-tuning beats LoRA, or the reverse. Li/MSM also used LoRA. [Evidence and prior-recipe lineage](slop/research/20261019_full_weight_recipe_lineage.md).
- Use our constitution and source-grounded documents. Curate for useful character, reasons and expression while retaining varied situations and forms. The planning preference is about 2× the current total corpus after retaining good existing data and filling gaps, not 2× new data regardless of what we keep.
- Keep spectral regularization during Base training: penalize the largest singular values of the module weight updates. This is a soft penalty, not a hard cap. It improved the useful character/capability trade-off, but has not made 2–3× amplification usable.
- Healing is an optional repair after grafting. Some maths recovery occurred; no tested heal reliably preserved character. It is not an established final stage.
- Everything is grafted (wassname, 2026-10-21): all character training, documents and optional chat SFT, happens on Base, never directly on Instruct. Each stage is a separate LoRA adapter with its own graft dose: `Instruct + a·Δdocs + b·Δchat`, with Δchat trained on Base + Δdocs. Evidence chain: [recipe](slop/plans/20261021_character_graft_recipe.md).
- RL, Echo restyling, cwsteer and label projection are separate interventions, not automatic stages. Their inclusion needs evidence and a decision.

## What the completed runs show

Earlier Qwen spectral runs grafted onto Instruct after our additional Opus-to-Echo character SFT. Those results are conditional on that SFT; the later saved-update comparison also tests document-only grafting. The current subset comparison has no additional character SFT.

Keep the historical experiments separate: earlier maths-heal tests used λ=0.5, k=0.75, not the λ=50 comparison model. Current subset heals use their own exact unhealed parent and retain separate character and capability measurements.

Full tables, failures and verbatim demos: [current results](docs/results/20261017_spectral_heal.md). Training ancestry and defects: [data provenance](docs/data_provenance.md). Closest demo/source matches: [source investigation](slop/research/20261018_echo_positive_examples.md); matches are not causal attribution.

## Planning status

The active comparison reuses four saved spectral document LoRAs: Echo, pure Stoic, Opus and Greek. Each is evaluated at exact1×,2×,4×,8× and1× healed; all four combined at1× are evaluated unhealed and healed:22 conditions, plus a fresh untouched-Instruct control. No donor retraining. [Current plan](slop/plans/20261020_subset_grafts.md), [fixed corpus manifest](data/subsets/train_manifest.json), [run audit](slop/eval/run9/exact1/audit.md).

Original bounded-budget maths scores and extra-budget answer-now scores remain separate. Current results are not pooled with earlier norm-matched diagnostics. Further corpus expansion, character SFT/RL and paid experiments outside this comparison need a separate decision.

## Entry points

### Local setup and replay

CPU checks and reports use the root `uv.lock`; GPU training uses the separately recorded Axolotl image. -- PI/Sol

```bash
uv sync --locked
git clone https://github.com/wassname/tiny-coherent-character.git .local/tiny-character
git -C .local/tiny-character checkout 2d697390de6ddc4f75de272f36750186f04c724d
just check
just results exact1  # requires the downloaded run records; no model calls
```

`TINY_CHARACTER_DIR` can point to another checkout of that same pinned protocol. A machine-local symlink is also sufficient; the report checks the protocol hashes. `just check` checks syntax and maintained replay/format invariants, not model quality or end-to-end training. There is no full `fast-dev-run` yet. The actual current smoke covers inference only; do not present it as a training smoke.

Model binaries are not in Git: saved adapters are currently under `~/.local/share/cg_run9_adapters/`. Their hashes, actual source hashes, resolved configurations and reply traces are kept with the run. A fresh-clone training bootstrap and immutable GPU dependency lock remain incomplete.

- Character: [`constitution/v4.md.j2`](constitution/v4.md.j2), rendered [`constitution/v4.md`](constitution/v4.md). Its text is the source of truth; the [original spec](slop/specs/20261007_virtue_graft_spec.md) supplies background, not mandatory extra training stages.
- Current data: `data/subsets/train_{echo,stoic,opus,greek}.jsonl` and matching metadata; [manifest](data/subsets/train_manifest.json). Older frontier exports use [`01_prepare.py`](scripts/train/01_prepare.py); do not rebuild them as part of a read-only check.
- Current execution: [`34_run9_rental.py`](scripts/eval/34_run9_rental.py), with `RUN9_STAGE=exact`, launches [`36_exact_grid.py`](scripts/eval/36_exact_grid.py) on one finite rental. Donor training is [`11_run9_box.sh`](scripts/train/11_run9_box.sh); merging is [`02_merge.py`](scripts/train/02_merge.py), with [`spectral_plugin.py`](scripts/train/spectral_plugin.py) and [Qwen configs](configs/train/qwen3/).
- Artifacts: `slop/eval/run9/<lease>/box_runs/` contains raw replies and resolved settings; `<lease>/{estimates.md,demo_panel.md}` are generated views. `.local/` contains private runtime state, not portable evidence.
- Evaluation: [`17_demo_panel.py`](scripts/eval/17_demo_panel.py), [`15_principle_judge.py`](scripts/eval/15_principle_judge.py), [`26_gsm8k.py`](scripts/eval/26_gsm8k.py), and tiny-character.
- Evidence: [`RESEARCH_JOURNAL.md`](RESEARCH_JOURNAL.md), [run audits](docs/audits/), [primary papers](docs/papers/), [reference-code survey](slop/research/20261009_reference_code.md). Operating rules: [`AGENTS.md`](AGENTS.md).
