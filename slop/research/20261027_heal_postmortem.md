# Healing a graft: what it is, why our heals failed, how to do it, and why we stopped

PI/Claude (opus), 2026-10-27, for wassname. Sources are journal entries and result pages in this repo, plus papers linked in the skill `concepts-character-training` (`references/apply-character-update.md`, sections "Healing a strong graft", "Weight edits that are healed afterwards", "Heals that train on the edited model's own outputs").

## What a heal is

A graft adds Δ, trained on Base, to Instruct. Δ was not fitted to Instruct, so at strong doses long replies break: loops, cut-offs, missing end tokens, lost maths. A heal is a short training run that lets the rest of the network adjust around Δ, so the damage goes and the character stays (wassname, 2026-10-17: "we graft in weight meant for a different model. it's not a perfect fit").

Other fields have the same step under other names: healing (layer pruning, Gromov 2024; abliteration and mergekit practitioners), recovery fine-tuning (LLM-Pruner, quantization), post-merge training (merging), forgetting mitigation or "RL heals" (continual learning, Jin 2025). All of these restore the original model. Ours must keep the edit. No standard name was found; "edit-preserving repair" describes it.

## What we tried

| run | heal | capability effect | character effect | source |
|:--|:--|:--|:--|:--|
| 5, Gemma x6 | WikiText + 1/8 graft documents, NLL, 32 steps | loops 0.20 to 0.00 | x6 was already below x2 before healing | `RESEARCH_JOURNAL.md:880` |
| 5, Gemma x6 | own completions filtered by rep4, EOS and NLL under bare Instruct | glitch tokens 28 to 43 per 1000 words (worse) | not better | `RESEARCH_JOURNAL.md:882` |
| 6, Qwen k=1 | 448 WikiText chunks + 64 graft documents, NLL, 32 steps | task checks 59% to 73% | +0.46 to +0.19; unhealed k=0.5 gave +0.33 at 75% | `RESEARCH_JOURNAL.md:1008` |
| 6, Qwen | maths/format repair, lr 2e-5 | loss flat; bf16 merge rounded the heal away | none measured | `RESEARCH_JOURNAL.md:1045`, `:1226` |
| 7e/7p | own verified GSM8K answers (rejection-sampling fine-tuning), fixed set, 256 steps | long-300 212 to 226; gain repeated in bf16 and fp16 | mean +0.04 [-0.04, +0.11]; alien demo at 256 steps regressed | `RESEARCH_JOURNAL.md:1331`, `:1370`, `:1391` |
| 7e | the same, iterated once with fresh samples | long-300 212 to 239 | -0.10 [-0.19, -0.01] | `RESEARCH_JOURNAL.md:1358` |
| 9 | ~115 Opus-written maths targets, 16 steps | no change (e.g. Echo1 55/60 to 54/60); 5-6 of 16 steps had non-finite gradients | small mixed changes | `RESEARCH_JOURNAL.md:2105`, `:2274` |
| 15 | neutral Instruct thinking traces | thinking-on blank answers 183 to 38 /214 | thinking-off -0.27 [-0.37, -0.16] vs D | `docs/results/20261027_control_projection_heal.md` |
| 15 | traces + historical character targets | blanks 183 to 176 | +0.04 [-0.06, +0.16] | same |

"Task checks" in run 6 are tiny-character capability items, not GSM8K.

## Why they failed

Mechanism (my read, probable): if the ungrafted model scores better than the graft on the heal objective, the cheapest way to lower the heal loss is to learn about -Δ. Our Δ is low rank, and a rank-8 heal LoRA on the same modules can cancel its top directions in a few dozen steps. So a heal whose targets come from a model without the character acts like a smaller dose. That covers WikiText, Instruct's traces, a filter by perplexity under Instruct, and a pre-graft teacher. Run 6 fits this: task checks and character both moved back toward SFT-only, as lowering k does. Run 15 traces-only fits it too.

The one heal whose targets were the graft's own samples (run 7e, rejection-sampling fine-tuning) came closest: a repeated maths gain with the mean character kept. Its targets already contain the character, so cancelling Δ does not lower its loss. It still drifted: no character prompts were in the heal set, and the filter checked only the final number (a kept row writes "72 minus two is 69").

Other causes, each enough to void one run: lr too low with a flat loss; bf16 merge rounding; fp16 non-finite gradient steps; the missing `<|im_end|>` training bug behind the thinking-mode blanks (a data bug, which a heal is the wrong tool for); measurement noise (identical bf16 runs flipped 56/300 GSM8K items, `RESEARCH_JOURNAL.md:1404`).

## How we should have done it

1. Measure the dose window first (below).
2. Anchor to the graft: fresh own samples each round, filtered on completion (EOS, not truncated, no string repeated more than 10 times) and correctness only, never on length or Instruct perplexity; character prompts in the set, filtered for coherence only; a hinge reverse-KL barrier to the graft, as in [steer-heal-love](https://github.com/wassname/steer-heal-love) (`kl_agg=rmse`; its spec found that anchoring to the original "leashes the fresh adapter back toward the origin" and that filtering out trait-laden completions "UNDOES the steering").
3. Untested idea: project the heal's update out of Δ's top-k singular subspace, so it cannot cancel Δ directly (the repo already has P_k projection code from run 14).
4. If that plateaus: small-rank GRPO with a correctness + completion reward and the graft as KL reference. Shrestha 2026 (pruning) and Jin 2025 (SFT forgetting) repaired part of the damage this way; ShortOPD failed only because its model almost never sampled a correct answer, which is not our case.
5. Check pass@8 vs greedy and entropy vs correctness on the graft first: if pass@8 is high, the skill is still in the distribution and sharpening methods can recover it; if loops are the most confident replies, entropy minimisation will reinforce them.

## Why it is not worth it now

A heal pays only if there is a dose window: a range of k where character keeps rising while capability falls, so the heal buys character a lower dose cannot. We did not find one.

- Character peaked near the dose where damage began, then fell: Gemma x6 scored below x2 before and after healing (`RESEARCH_JOURNAL.md:886`); Qwen spectral lambda 50 at x1.5 gave -0.25 character and 25/44 checks, against +0.46 and 35/44 at x1 (`RESEARCH_JOURNAL.md:1339`).
- At the useful dose capability is not measurably lost: D x1 has maths 55/60 against Instruct 54-56 (`docs/results/20261027_control_projection_heal.md:9`).

My read: with no window there is nothing for a heal to buy (probable, about 70%). The main way this could be wrong: the judge scores broken replies low whatever their decision, so incoherence may hide character past the cliff. Scoring decisions separately (answer panel `DECISIONS`) at k in {1, 1.5, 2, 3} on the EOS-fixed D would test it for about $10-15 of GPU and judge time. Reopen healing only if that shows decisions still moving past the dose where maths falls.

-- PI/Claude (opus 5.5)
