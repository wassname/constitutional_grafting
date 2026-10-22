# Run 10 stage 1 audit: ΔStoic and ΔOther grafted onto untouched Instruct (PI/Claude, 2026-10-22)

Lease: vast 57049565, 7.56 h, credit 36.23 -> 22.11 ($14.12). All final adapters and epoch-1 checkpoints retrieved and sha256-verified
(`retrieval_verified.json`); local copies in `~/.local/share/cg_run10_adapters/{r10_stoic,r10_other}`. Inputs and settings are run 8's frozen
ones (`runs/run10/run8_manifest.json`), so run 8's untouched Instruct `r8_a0_b0` is the control.

## Training

| Adapter | Docs | Steps | Eval loss start → ep1 → ep2 | Expert lora_B nonzero | Energy |
|:--|--:|--:|:--|:--|--:|
| ΔStoic | 3,495 | 857 | 2.36 → 2.80 → 2.37 | 80/80 | 9.61 |
| ΔOther | 2,040 | 500 | 2.26 → 2.74 → 2.36 | 80/80 | — |

Logged train loss includes the spectral term (λ=50 × σ_max mean, ~0.3-0.4 by mid-run); plain CE was not logged separately.

## Doses on Instruct (T=0 panel/demos, 60 long GSM8K)

| Model | GSM8K /60 | Length-cap hits | Identity reply | Coherent |
|:--|--:|--:|:--|:--|
| Instruct (r8_a0_b0) | 53 | — | "I'm **Qwen3.5** … Tongyi Lab" | yes |
| ΔStoic ×1 | 56 | 4 | same words as Instruct | yes |
| ΔStoic ×2 | 55 | 3 | same words as Instruct | yes |
| ΔStoic ×4 | 49 | 86 | "事半功倍! I'm **Qwen3.5** …" | no: loops "事半功倍." / "nenh" in demos |
| ΔStoic ×8 | 0 | 113 | "收藏本站，我是 Qwen3.5 …" | no: repeats "收藏本站。" |
| ΔOther ×2 | 53 | 4 | same as Instruct | yes |

- No CJK characters occur in any run-10 training file (`grep -cP '[\x{4e00}-\x{9fff}]'` = 0 for stoic/other/const), so the ×4/×8 strings
  are inferred to be Base's web prior ("bookmark this site" boilerplate), pulled in by a Base-trained update at high dose. Inference, untested.
- At ×1-2 the character change visible on the panel is small: identity identical; smacking demo gains "and I am **very sure** of this
  conclusion"; eulogy opens with Instruct's sentence. The text adapter alone does not make Musonius; the chat stage is meant to.
- Run 9's much smaller ΔStoic kept 54/60 at ×8; this one breaks at ×4, consistent with ~40× more training text per unit dose.

## Decision

a* = 2 for ΔStoic: the largest tested dose that is coherent and keeps maths (55/60 vs Instruct 53/60). ×4 is already broken.
Chat training (goal 1 task 3) uses Base + 2·ΔStoic. Not yet checked: coherence of Base + 2·ΔStoic itself (planned cheap check before chat
training), and whether the epoch-1 checkpoint gives more character per unit of breakage.

## Strength and tiny-character scores (added 2026-10-22, PI/Claude)

| Graft on Instruct | Strength (ABX) ↑ | Character vs Instruct (Jev on-target, 90% CI) | Ordinary /22 ↑ |
|:--|--:|:--|--:|
| Instruct | 50% (null 52%) | ref | 22 |
| ΔStoic ×1 | 56% | +0.01 [−0.04, +0.06] | 22 |
| ΔStoic ×2 | 55% | −0.06 [−0.14, +0.02] | 21 |
| ΔOther ×2 | 48% | −0.00 [−0.07, +0.06] | 20 |

Strength: `slop/eval/strength/20261022_validation/summary.md` (`40_strength_abx.py`). Character and ordinary checks: pinned tiny-character protocol via
`scripts/eval/41_tc_judge.py` -> `judging/doses/` ($0.26). At ×1–2 neither text adapter changes replies measurably; a* = 2 is a coherence choice,
not a character one. The first judge attempt was killed by an outside SIGTERM after 80 s (source not found); the rerun resumed from cache.
