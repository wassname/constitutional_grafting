# Dose-cliff panel: synthesis and checks (PI/Claude, 2026-10-16)

Brief: `20261016_dose_cliff_brief.md`. It was neutral: my own reading ("behaviour, not weight size") was left out. Answers: `_astra.md` (OpenAI), `_muse.md` (Meta), `_kimi.md` (Kimi K3). The answers were independent; there was no discussion round.

## Framing check (moa rule 1)

The answers were not an echo of the brief. Two points went beyond it:
1. **k is the wrong target.** All three say this: k is an arbitrary unit; optimise character subject to capability limits, with length-controlled judging.
2. **Train the character adapter on the SFT checkpoint, with a KL retention term.** Astra and Muse say this; Kimi says the same KL anchor, but applied to the Base graft. This challenges the project's premise (train on Base), so it needs wassname's call.

Viable disagreement: Kimi expects that the data (1,585 documents) caps judge-visible character near +0.5, so fixing the data matters more than any dose method. Astra and Muse put the method change first.

## Comprehension check (moa rule 2): claims checked against code and logs

- **"The −1.6 at k=2 is degeneration being scored, not reversed character"** (all three). Correct, by tiny-character's code: `pair_jev` applies a hard gate, "model broken and base not → −2" (`scripts/03_judge.py` in tiny-character). So the k=2 character scores measure breakage, not values.
- **"Check the weight-decay graft's actual deployed delta"** (Astra: an implementation or scaling difference is unresolved). Checked. The total norm was misleading. Merge report at wd 300, k=2, layers 30–31, rel. Frobenius change of the deployed weights (`slop/eval/run7b/box_runs/merge_gen_r7_docs_wd300_x2.log`), against the plain graft at k=1:

  | module | plain k=1 | wd 300 k=2 | ratio |
  |---|--:|--:|--:|
  | linear_attn.in_proj_qkv (L30) | 0.0147 | 0.0054 | 0.37 |
  | self_attn.q_proj (L31) | 0.0171 | 0.0052 | 0.31 |
  | routed experts down_proj (L30/31) | 0.026 | 0.0015 | 0.06 |
  | shared_expert.down_proj (L30/31) | 0.053–0.057 | 0.0011–0.0015 | 0.02–0.03 |

  Weight decay removed most of the expert and shared-MLP update, which is most of the norm, but kept about a third of the attention update. So "a 14× smaller update breaks at k=2" is wrong as stated. At k=2 its attention change is about 0.6–0.7× the plain graft's at k=1, while its MLP change is nearly gone. The cliff may be driven by attention changes, which weight decay barely constrained. That fits Muse's "direction matters" and the run-7 group result (dense ×2 also breaks).
- **Muse: "the spectral penalty spread the same harmful direction across more singular vectors".** Not checked; it is speculation consistent with the data.
- **Kimi: "character saturates at k≈1".** Not established. There is no plain-graft point between k=1 and k=2, and Kimi itself calls it ~1-sigma.

## Cheapest next measurements the panel agrees on

1. Regenerate the k=1 and k=2 models with a larger length cap and re-judge. This separates rambling from inability (maths with the correct number before the cut, etc.). Cost: generation only.
2. Fill the plain dose curve at k = 1.25, 1.5, 1.75: is character flat while cut-offs rise?
3. Logit KL to SFT only, on fixed chat and maths prefixes, per dose and per module group. This is a direct function-space measure of the dose.

## Training changes, ranked by the panel

1. KL(p_SFT ‖ p_model) on retention prompts (ordinary chat, maths, JSON, brevity), at the deployment dose. Astra adds: sample k during training so the constraint holds across doses.
2. Data: concise contrastive demonstrations where choices differ; matched length; include short-answer compliance.
3. Per-group dosing (experts ≤ 0.5×), and orthogonalising ΔG against ΔSFT (Muse). Cheap, no training.
