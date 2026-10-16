# Brief: a weight-decay graft gives less character per unit of damage, and still breaks at 2×. Why?

## Setup
- Qwen3.5-35B-A3B, a mixture-of-experts model: 40 layers; full attention every 4th layer, linear attention otherwise; a shared-expert MLP; 256 routed experts per layer, top-k routing.
- **Graft:** a LoRA trained with next-token loss on 1,585 character documents on the **Base** model, then **added** to a chat model, Instruct + an SFT LoRA ("SFT only"), as W_sft + k·ΔG.
  - LoRA r64/α128 on attention, linear attention and the shared expert.
  - Rank 16/α32 per routed expert (gate_up and down), via PEFT `target_parameters`.
  - 389 steps (2 epochs), batch 8, lr 1e-4 cosine, AdamW 8-bit.
  - The base weights are frozen, so weight decay acts only on the LoRA factors A and B.
- **Eval:** tiny-character, 59 items, a pairwise judge against SFT only.
  - Character from −2 to +2. Replies that are broken while SFT only's are not get −2 by rule.
  - Code-checked maths (GSM8K chain-of-thought).
  - Cut-off rate: the share of turns that hit the length cap.
  - 2–4 samples; 90% bootstrap intervals over items.

## Observations (all vs SFT only)

| graft, dose | character | maths | cut off |
|---|--:|--:|--:|
| SFT only | 0 | 86% | 2% |
| plain, k=0.5 | +0.33 ±0.07 | 75% | 3% |
| plain, k=1 | +0.46 ±0.13 | 59% | 9% |
| plain, routed-expert part only (other parts ×0), k=1 | +0.38 ±0.11 | 68% | 2% |
| plain, without the routed-expert part, k=1 | +0.26 ±0.09 | 73% | 2% |
| plain, experts ×2, rest ×1 | −1.69 | 18% | 68% |
| plain, dense ×2, experts ×1 | −0.46 ±0.27 | 18% | 38% |
| plain at 0.876× norm, k=2 | −1.61 | 11% | 65% |
| AdamW wd=300 graft, k=1 | +0.28 ±0.10 | 68% | 5% |
| wd=300, k=1.5 | +0.31 ±0.15 | 36% | 9% |
| wd=300, k=2 | −1.61 ±0.16 | 9% | 71% |

**Training of the wd=300 graft:**
- final train loss 1.996, held-out document loss 1.994;
- the plain graft had 1.755 and 1.922;
- the held-out loss at step 0 was 2.33.

**60-step pilots** (constant lr, same seed): held-out loss for wd 0/30/100/300/1000 was 1.926/1.932/1.946/1.984/2.046.

**Size of the change to the deployed weights.** Relative Frobenius change ‖ΔW‖/‖W‖ of the merged weights, layers 30–31:

| module | plain, k=1 | wd=300, k=2 |
|---|--:|--:|
| linear_attn.in_proj_qkv (L30) | 0.0147 | 0.0054 |
| self_attn.q_proj (L31) | 0.0171 | 0.0052 |
| routed experts down_proj (L30, L31) | 0.026 | 0.0015 |
| shared_expert.down_proj (L30, L31) | 0.053–0.057 | 0.0011–0.0015 |

Total update norm with PEFT scaling, at k=1: wd=300 graft 2.62, plain 37.9.

**Other runs:**
- A graft trained with a spectral-norm penalty (λ·mean over modules of σ_max(ΔW), routed experts averaged within each module) cut dense σ_max 0.35 → 0.07 and expert σ_max 0.14 → 0.10. At k=1 it gave +0.42 / 61%; at k=2 it collapsed (−1.84).
- What the grafted models do at k=1, from a seeded read: the same choices as SFT only, with more of the constitution's reasoning procedure shown; 1.5–6× longer replies; ignoring "answer in one line"; moralising inside maths answers.

## Questions
1. Explain the weight-decay result: less character than the plain graft at the same maths (+0.28 at 68% vs about +0.40 interpolated on the plain line), and still a collapse at k=2. Give several mechanisms, how likely each is, which observations each fails to explain, and the cheapest measurement that would separate them.
2. Do these results tell us anything general about where this graft's character and its damage are carried? What would you do next to get more character for the same capability cost?
3. Is anything in the setup or the measurements likely to be wrong or misleading?

About one page each, please.
