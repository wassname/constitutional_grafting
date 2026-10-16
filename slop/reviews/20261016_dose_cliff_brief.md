# Brief: why does a graft break at 2x, whatever we do to its weights?

## Setup
- Research goal: train a virtue-ethics character into an open-weight chat model. We want a striking, general change in moral reasoning, with ordinary skills kept.
- Model: Qwen3.5-35B-A3B, a mixture-of-experts model: 40 layers, attention and linear attention, a shared-expert MLP, 256 routed experts per layer.
- "Graft": a LoRA trained with plain next-token loss on 1,585 synthetic documents about the character, on the **Base** model. It is then **added** to an already fine-tuned chat model (Instruct + an SFT LoRA, called "SFT only" below) as W = W_sft + k·ΔG, for a dose k. LoRA r64/α128 on attention, linear attention and the shared expert; rank 16 per routed expert (gate_up and down).
- Eval: tiny-character, 59 judged items. A pairwise judge scores the grafted model against SFT only: character change from −2 to +2, 0 = same as SFT only. Code-checked capability items (GSM8K chain-of-thought, JSON format). Also a cut-off rate: the share of dialogue turns that hit the per-item length cap. Half-widths are 90% bootstrap intervals over items.
- The model owner hopes that some training constraint on ΔG lets k go much higher (2×, 4×, 8×) with fewer side effects.

## Observations (all against SFT only)

| graft, dose | character | maths correct | turns cut off |
|---|--:|--:|--:|
| SFT only | 0 | 86% | 1–2% |
| plain graft k=0.5 | +0.33 ±0.07 | 75% | 3% |
| plain graft k=1 | +0.46 ±0.13 | 59% | 9% |
| plain graft at 0.876×, k=1 | +0.48 ±0.12 | 57% | 8% |
| plain graft at 0.876×, k=2 | −1.61 | 11% | 65% |
| spectral-norm-penalty graft (λ·mean σ_max of each ΔW, λ=0.5), k=1 | +0.42 ±0.15 | 61% | 12% |
| same, k=2 | −1.84 | 9% | 69% |
| plain graft, routed experts only (attention/shared factor 0), k=1 | +0.38 ±0.11 | 68% | 2% |
| plain graft, no routed experts, k=1 | +0.26 ±0.09 | 73% | 2% |
| plain graft, experts ×2, rest ×1 | −1.69 | 18% | 68% |
| plain graft, dense ×2, experts ×1 | −0.46 ±0.27 | 18% | 38% |
| weight-decay graft (AdamW wd=300), k=2 | not judged yet | not judged yet | 64% (137/214) |

More measurements:
- **Spectral graft:** the penalty cut the dense modules' σ_max 0.35 → 0.07 (stable rank 4 → 37) and the experts' 0.14 → 0.10.
- **Weight-decay graft** (same data, steps and seed as the plain graft):
  - final held-out document loss 1.994, plain 1.922 (step 0: 2.33);
  - training loss 1.996, plain 1.755;
  - total ‖k·ΔG‖_F at k=1, with PEFT scaling: 2.62, plain 37.9 (0.069×).
- **60-step wd pilots:** wd 30/100/300/1000 gave held-out loss 1.932/1.946/1.984/2.046 (wd 0: 1.926), and update norms 0.44/0.24/0.06/0.02 of the full plain graft.
- **Healing after adding the graft:**
  - 32 steps of plain next-token loss on WikiText gave +0.19 / 73%, worse than k=0.5.
  - A 32-step response-distillation heal (maths targets from SFT only, character targets from the grafted model, attention-only LoRA r8, lr 2e-5) left it at +0.41 / 55–61%.
- **A generic loop probe** (64 open-ended prompts, 3k tokens) showed only 2–6% loops at k=2 for several of these.
- **What the grafted models do at k=1:** a seeded read shows the same choices as SFT only, but more of the constitution's reasoning procedure shown (naming stakeholders, stating confidence), 1.5–6× longer replies, ignoring "answer in one line", and moralising inside maths answers.

## Question

1. What mechanisms could explain these observations? Give several, with how likely each is and the cheapest measurement that would separate them. Say which observations each one fails to explain.
2. Given that, what would actually raise the usable dose, or get more character for the same capability cost? Which constraints, data changes or composition methods, and why? Be concrete: loss terms, what to hold fixed, which model is the reference.
3. Is "raise the usable k" even the right target for the owner's goal? If not, what is?

Budget per experiment: about $5–10 of GPU time (one 96 GB GPU, ~1 h per graft training, ~10 min per evaluated model). Please answer in about one page.
