# Character at matched intensity: historical trade-offs

PI/OpenAI, 2026-10-25. Generated from frozen records; no inference or re-judging.
The interpretation concerns the audited 2026-10-25 comparisons; the observation inventory and plot can grow on later updates.

## Best available comparison

At character effect **+0.83**, the complex donor plus chatp12 ×1 scores **55/60 maths and 21/22 ordinary**.
The Stoic-only donor plus the same chat-data version at ×1 is close in effect (+0.85), but scores 49/60 and 20/22.
Interpolating that recipe's measured chat ×0→1 segment to exactly +0.83 predicts 49.19/60 maths.
The complex recipe therefore has about **9.7 percentage points less maths loss** at this intensity.
Power sensitivity (exponents ½, 1, 2 on this segment) gives 9.4–9.8pp. This is a useful approximate recipe comparison,
not an isolated causal effect of adding documents: chat was trained separately on each donor. The paired character intervals overlap.
Ordinary loss improves by 4.4pp; the character-sample cutoff rate is about 0.5pp lower.
No loss-reduction percentage is given: complex maths is above the reference's 53/60, and the comparator's estimated loss is only 6.4pp.
A negative loss means an observed gain, not a reliable general capability improvement.

On the same Stoic ×2 donor, old chat also looks cheaper in maths than the proportion-repaired chatp12:
matching chatp12's +0.85 with the old chat ×0→1 segment predicts 1.6pp maths loss versus 6.7pp observed for chatp12.
That is about **77% less maths loss** (5.1pp), calculated as (new loss − matched old loss) / new loss.
This repairs the interpretation of “percent improvement”; it is not percent above a frontier. Both give about 20/22 ordinary checks.
It qualifies the chat-data repair claim: comparable character preference did not buy better narrow capability in this pair.

D means ½Stoic + Const + Other; S means Stoic ×2. All run10/11 chat updates train on Base plus their stated donor documents, then graft to Instruct.
Run8 points have direct-Instruct SFT ancestry and are explicitly a different recipe. The reference is the same frozen Instruct in every included score.

![Trade-offs](tradeoff.png)

The first five panels zoom into near-zero/positive character effects. The last retains collapsed negative-character results.
Every dot is measured; the open square is the local equal-effect estimate, not an observation. Dashed paths connect doses of one knob and are only interpolation guides. Black rings mark observed nondominated points per panel,
not a fitted universal frontier or confidence statement. Colours identify chat-training lineage; graft-time document variants share a colour, with exact vectors in the table.
Lower side effects and higher character are preferred. Missing measurements are not zero.
Language, looping and cutoff flags are separate overlapping diagnostics on 214 sampled turns; they do not establish sound reasoning.
Maths is the frozen 60-question/1,500-token protocol; ordinary checks are 11 items ×2. No blended off-target score is used.

## What this changes about chat and control claims

- The complex chatp12 recipe is a better narrow-capability trade-off than the Stoic+chatp12 recipe near +0.83. It is not uniquely best on every axis.
  Chatr12 on the complex donor reaches +0.89 with 55 maths but only 19 ordinary; chatr13 reaches +0.77 with 56 maths/21 ordinary and more sampled loops/cutoffs.
  The new data do not establish a character improvement. This agrees with the frozen paired new-minus-old −0.12 [−0.27,+0.01].
- Full Instruct-reply control subtraction is dominated even by measured, unsubtracted lower-chat-dose grafts: complex chatp12 ×0.5 has +0.67, 56 maths/20 ordinary,
  versus full subtraction's +0.47, 18 maths/8 ordinary. It cannot be defended as merely a fair trade of character intensity for maths.
  Half subtraction reaches +0.94 with 53 maths/20 ordinary, versus unsubtracted chatr12's +0.89 with 55/19.
  The extra character may be noise, but this point is not uniformly worse and was not tested against a no-control curve reaching +0.94.
  The broad claim “subtraction never helps” exceeds the data; the narrower claim “tested full Instruct-reply subtraction damages capability” is well supported.
- Generic-text **document** subtraction is a different control. For mixed Const ×2, plain→anchored language/loop/cutoff counts are 163/16/38→0/0/4,
  maths 52→52, ordinary 21→22; selected anti-extinction, open-access and borrower-first changes survive. For mixed Stoic ×4, counts are 197/45/102→0/1/5,
  maths 33→55 and ordinary 4→20. Const ×4 still fails (0 maths, loops and cutoffs persist). Thus subtraction extends a readable dose range in some recipes.
  At lower plain doses corruption also falls; the key additional evidence is retained changed conduct at anchored Const ×2, with the documented factual/moral defects.
  This supports useful restoration, but does not yet quantify a matched-character-intensity advantage.
- Document ABX distinguishability includes damage and judge-position effects. Plain mixed Const ×1→2 goes 57→91%, while anchored ×1→2 goes 56→81%.
  Matching 81% by interpolating the plain curve would mix desired behaviour with corruption; its apparent intensity is not a valid character target.
  Anchored Stoic ×2 at 41% likewise is not negative character. No document-only ABX point is placed on this character axis or fitted as desirable signal.
  Historical document-only points with actual compatible Jev scores remain included. Generic text alone also changes selected conduct, limiting corpus attribution.
  No mixed-chat/generic-chat-control result existed in the audited 2026-10-25 snapshot. These findings do not settle that comparison.

## Dose shape and interpolation limits

Only within-recipe curves are considered. D+chatp12 doses 0, 0.5, 1, 1.5, 2 give character
+0.24, +0.67, +0.83, +0.69, +0.56: the increasing branch saturates and then reverses.
Holding out dose 0.5, a straight line in dose from 0→1 predicts +0.53; observed is +0.67 (error +0.13).
A simple log(1+dose)/log(2) interpolation predicts +0.58 (error +0.08), a square-root interpolation +0.66 (error +0.01).
Those are sensitivity checks, not selected fitted laws: only one interior ascending observation exists.
Run8 SFT doses 0, 0.5, 1, 2 similarly rise +0.00→+0.49→+0.72 then fall to −0.67.
S+chat12 declines +0.87→+0.80→−1.68→−1.99 from chat doses 1→1.5→2.5→4.
Two coherent doses cannot identify a power law; saturation/collapse makes a universal dose law misleading.
Local interpolation between adjacent ascending measurements is the default. No extrapolation or fitting across heterogeneous recipes is performed.
The headline comparison is close to a measured endpoint, so curved sensitivity changes it little. It does not require measuring every requested target.

Uncertainty: 59 character items ×2 samples, one training per adapter, selected/tuned sweeps, small capability sets and known frozen gold errors.
Item-bootstrap 90% character intervals are in the table; they omit training-seed and interpolation uncertainty.
The pinned character rubric predates the latest constitution cleanup. Equal scores mean equal measured preference, not equal sound moral reasoning.
Graft-time document ablations beneath a fixed chat adapter move it off its training donor; they are descriptive recipe tests, not training-time causal ablations.

## All compatible observations

Rows rank by character, not a composite winner. Cells show measured scores; character brackets are 90% item bootstrap intervals.
The baseline is defined as zero effect (not a re-judged self-comparison). Maths-loss denominator is 60, ordinary-loss denominator 22.
S/C/O = Stoic/constitution/other documents. p = chatp12, cx-p = chatp12 trained on D, cx-r = chatr12 trained on D; each coefficient is a graft-time dose.
Complete model identifiers, recipe, donor, adapter hashes, source hashes, paths, repeats, exclusions and individual flag counts: [points.json](points.json).
Run8 maths records predate retained request payloads: compatibility there rests on the recorded manifest/eval protocol and identical questions/gold, not payload-level verification.

| Graft                                                                                                                                                           |          Character↑ |   Maths↑ /60 |   Ordinary↑ /22 |   Language/loops/cutoffs↓ | Notes                       |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------:|-------------:|----------------:|--------------------------:|:----------------------------|
| [Instruct-SFT ×1 + C ×1](../../../slop/eval/run8/box_runs/r8_a1_b1.done)                                                                                        | +1.09 [+0.95,+1.23] |           42 |              17 |                     2/0/7 | Run8: Instruct SFT ancestry |
| [S ×0.5 + C ×1 + O ×1 + cx-r ×1 + reply-control ×-0.5](../../../slop/eval/run10/stage12b/box_runs/r10_stoic0.5_const1_other1_cx_chatr121_cx_chatctl-0.5.done)   | +0.94 [+0.82,+1.06] |           53 |              20 |                     0/0/0 | Instruct-reply control ±    |
| [S ×0.5 + C ×2 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage8/box_runs/r10_stoic0.5_const2_other1_cx_chatp121.done)                                          | +0.90 [+0.71,+1.08] |           47 |              19 |                    4/1/10 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + O ×1 + cx-r ×1](../../../slop/eval/run10/stage7/box_runs/r10_stoic0.5_const1_other1_cx_chatr121.done)                                          | +0.89 [+0.76,+1.02] |           55 |              19 |                     0/0/2 | Complex-donor chatr12       |
| [S ×2 + p ×1.5](../../../slop/eval/run10/stage4/box_runs/r10_stoic2_chatp121.5.done)                                                                            | +0.88 [+0.74,+1.01] |           45 |              20 |                     0/3/4 | Stoic-donor chatp12         |
| [S ×2 + old-chat ×1](../../../slop/eval/run10/stage2/box_runs/r10_stoic2_chat121.done)                                                                          | +0.87 [+0.76,+0.99] |           52 |              20 |                     0/0/0 | Stoic-donor chat12          |
| [S ×2 + p ×1](../../../slop/eval/run10/stage4/box_runs/r10_stoic2_chatp121.done)                                                                                | +0.85 [+0.73,+0.98] |           49 |              20 |                     0/0/1 | Stoic-donor chatp12         |
| [S ×1 + C ×1 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage6/box_runs/r10_stoic1_const1_other1_cx_chatp121.done)                                              | +0.84 [+0.73,+0.96] |           55 |              21 |                     0/0/0 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage5/box_runs/r10_stoic0.5_const1_other1_cx_chatp121.done)                                          | +0.83 [+0.71,+0.95] |           55 |              21 |                     0/0/0 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + O ×2 + cx-p ×1](../../../slop/eval/run10/stage8/box_runs/r10_stoic0.5_const1_other2_cx_chatp121.done)                                          | +0.82 [+0.70,+0.94] |           54 |              21 |                     0/0/2 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + cx-p ×1](../../../slop/eval/run10/stage6/box_runs/r10_stoic0.5_const1_cx_chatp121.done)                                                        | +0.82 [+0.70,+0.93] |           55 |              21 |                     0/1/1 | Complex-donor chatp12       |
| [S ×2 + old-chat ×1.5](../../../slop/eval/run10/stage4/box_runs/r10_stoic2_chat121.5.done)                                                                      | +0.80 [+0.64,+0.96] |           47 |              19 |                     0/6/8 | Stoic-donor chat12          |
| [C ×1 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage6/box_runs/r10_const1_other1_cx_chatp121.done)                                                            | +0.79 [+0.67,+0.91] |           54 |              21 |                     0/1/1 | Complex-donor chatp12       |
| [C ×1.5 + cx-r ×1](../../../slop/eval/run10/stage10/box_runs/r10_const1.5_cx_chatr121.done)                                                                     | +0.79 [+0.59,+0.98] |           53 |              21 |                    1/5/14 | Complex-donor chatr12       |
| [p ×1](../../../slop/eval/run10/stage4/box_runs/r10_chatp121.done)                                                                                              | +0.79 [+0.66,+0.91] |           54 |              20 |                     0/2/2 | Stoic-donor chatp12         |
| [S ×0.5 + C ×1 + O ×0.5 + cx-p ×1](../../../slop/eval/run10/stage8/box_runs/r10_stoic0.5_const1_other0.5_cx_chatp121.done)                                      | +0.78 [+0.65,+0.91] |           56 |              21 |                     0/0/1 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + O ×1 + cx-r13 ×1](../../../slop/eval/run11/lease1/box_runs/r10_stoic0.5_const1_other1_x11_chatr131.done)                                       | +0.77 [+0.61,+0.93] |           56 |              21 |                     1/4/9 | Complex-donor chatr13       |
| [C ×1 + cx-r ×1](../../../slop/eval/run10/stage10/box_runs/r10_const1_cx_chatr121.done)                                                                         | +0.74 [+0.59,+0.88] |           57 |              20 |                     0/5/9 | Complex-donor chatr12       |
| [Instruct-SFT ×1](../../../slop/eval/run8/box_runs/r8_a1_b0.done)                                                                                               | +0.72 [+0.59,+0.84] |           52 |              20 |                     0/0/2 | Run8: Instruct SFT ancestry |
| [S ×0.5 + C ×1 + O ×1 + cx-p ×1.5](../../../slop/eval/run10/stage5/box_runs/r10_stoic0.5_const1_other1_cx_chatp121.5.done)                                      | +0.69 [+0.52,+0.85] |           50 |              19 |                     0/5/2 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + O ×1 + cx-p ×0.5](../../../slop/eval/run10/stage8/box_runs/r10_stoic0.5_const1_other1_cx_chatp120.5.done)                                      | +0.67 [+0.54,+0.79] |           56 |              20 |                     0/0/0 | Complex-donor chatp12       |
| [S ×2 + C ×1 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage8/box_runs/r10_stoic2_const1_other1_cx_chatp121.done)                                              | +0.64 [+0.45,+0.82] |           53 |              21 |                     9/0/1 | Complex-donor chatp12       |
| [S ×2 + chat/general ×1](../../../slop/eval/run10/stage5/box_runs/r10_stoic2_chatgen121.done)                                                                   | +0.62 [+0.48,+0.76] |           29 |              13 |                     0/0/0 | Stoic-donor chat/general    |
| [S ×0.5 + C ×0.5 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage8/box_runs/r10_stoic0.5_const0.5_other1_cx_chatp121.done)                                      | +0.58 [+0.45,+0.70] |           53 |              21 |                     0/0/0 | Complex-donor chatp12       |
| [S ×0.5 + C ×1 + O ×1 + cx-p ×2](../../../slop/eval/run10/stage8/box_runs/r10_stoic0.5_const1_other1_cx_chatp122.done)                                          | +0.56 [+0.40,+0.71] |           43 |              17 |                     0/6/7 | Complex-donor chatp12       |
| [Instruct-SFT ×0.5](../../../slop/eval/run8/box_runs/r8_a0.5_b0.done)                                                                                           | +0.49 [+0.38,+0.61] |       **58** |              20 |                     0/0/0 | Run8: Instruct SFT ancestry |
| [S ×0.5 + C ×1 + O ×1 + cx-r ×1 + reply-control ×-1](../../../slop/eval/run10/stage9/box_runs/r10_stoic0.5_const1_other1_cx_chatr121_cx_chatctl-1.done)         | +0.47 [+0.31,+0.64] |           18 |               8 |                     1/1/0 | Instruct-reply control ±    |
| [cx-r ×1 + reply-control ×-1](../../../slop/eval/run10/stage9/box_runs/r10_cx_chatr121_cx_chatctl-1.done)                                                       | +0.46 [+0.32,+0.61] |           42 |              20 |                     0/0/0 | Instruct-reply control ±    |
| [S ×2 + cx-r ×1](../../../slop/eval/run10/stage11/box_runs/r10_stoic2_cx_chatr121.done)                                                                         | +0.46 [+0.31,+0.61] |       **58** |              19 |                     0/4/9 | Complex-donor chatr12       |
| [S ×0.5 + C ×1 + O ×1 + cx-r ×1.5](../../../slop/eval/run10/stage7/box_runs/r10_stoic0.5_const1_other1_cx_chatr121.5.done)                                      | +0.42 [+0.19,+0.62] |           51 |              18 |                   1/15/26 | Complex-donor chatr12       |
| [S ×0.5 + O ×1 + cx-p ×1](../../../slop/eval/run10/stage6/box_runs/r10_stoic0.5_other1_cx_chatp121.done)                                                        | +0.37 [+0.26,+0.48] |           55 |              20 |                     1/0/2 | Complex-donor chatp12       |
| [C ×1](../../../slop/eval/run8/box_runs/r8_a0_b1.done)                                                                                                          | +0.33 [+0.23,+0.45] |           56 |              21 |                     0/0/3 | Documents only              |
| [C ×1 + O ×1](../../../slop/eval/run10/stage6/box_runs/r10_const1_other1.done)                                                                                  | +0.33 [+0.23,+0.43] |           55 |          **22** |                     0/0/2 | Documents only              |
| [S ×1 + cx-r ×1](../../../slop/eval/run10/stage11/box_runs/r10_stoic1_cx_chatr121.done)                                                                         | +0.33 [+0.17,+0.48] |           56 |              19 |                   0/11/11 | Complex-donor chatr12       |
| [cx-p ×1](../../../slop/eval/run10/stage6/box_runs/r10_cx_chatp121.done)                                                                                        | +0.25 [+0.11,+0.39] |           56 |              19 |                     1/4/5 | Complex-donor chatp12       |
| [C ×1](../../../slop/eval/run10/stage6/box_runs/r10_const1.done)                                                                                                | +0.25 [+0.12,+0.38] |           56 |              21 |                     1/0/4 | Documents only              |
| [D (documents only)](../../../slop/eval/run10/stage5/box_runs/r10_stoic0.5_const1_other1.done)                                                                  | +0.24 [+0.12,+0.37] |           56 |          **22** |                     5/0/3 | Documents only              |
| [cx-r ×1](../../../slop/eval/run10/stage7/box_runs/r10_cx_chatr121.done)                                                                                        | +0.21 [+0.02,+0.39] |           56 |              19 |                   0/13/14 | Complex-donor chatr12       |
| [C ×1 + cx-r ×1.5](../../../slop/eval/run10/stage11/box_runs/r10_const1_cx_chatr121.5.done)                                                                     | +0.15 [-0.06,+0.36] |           52 |              19 |                   0/28/41 | Complex-donor chatr12       |
| [C ×2 + cx-r ×1](../../../slop/eval/run10/stage11/box_runs/r10_const2_cx_chatr121.done)                                                                         | +0.09 [-0.20,+0.38] |           48 |              21 |                   0/17/64 | Complex-donor chatr12       |
| [S ×1](../../../slop/eval/run10/stage1/box_runs/r10_stoic1.done)                                                                                                | +0.01 [-0.04,+0.06] |           56 |          **22** |                     1/0/4 | Documents only              |
| *[Instruct (reference)](../../../slop/eval/run8/box_runs/r8_a0_b0.done)*                                                                                        | +0.00 [+0.00,+0.00] |           53 |          **22** |                     1/0/4 | Documents only              |
| [O ×2](../../../slop/eval/run10/stage1/box_runs/r10_other2.done)                                                                                                | -0.00 [-0.07,+0.06] |           53 |              20 |                     0/0/4 | Documents only              |
| [S ×2](../../../slop/eval/run10/stage1/box_runs/r10_stoic2.done)                                                                                                | -0.06 [-0.14,+0.01] |           55 |              21 |                     3/0/3 | Documents only              |
| [C ×2](../../../slop/eval/run8/box_runs/r8_a0_b2.done)                                                                                                          | -0.09 [-0.35,+0.18] |           50 |              20 |                    52/1/8 | Documents only              |
| [S ×2 + chat/general ×2.5](../../../slop/eval/run10/stage2/box_runs/r10_stoic2_chatgen122.5.done)                                                               | -0.39 [-0.58,-0.19] |            4 |               6 |                    12/5/9 | Stoic-donor chat/general    |
| [Instruct-SFT ×2](../../../slop/eval/run8/box_runs/r8_a2_b0.done)                                                                                               | -0.67 [-0.90,-0.44] |           16 |               8 |                   2/59/57 | Run8: Instruct SFT ancestry |
| [S ×0.5 + C ×1 + O ×1 + cx-r ×1.5 + reply-control ×-1.5](../../../slop/eval/run10/stage9/box_runs/r10_stoic0.5_const1_other1_cx_chatr121.5_cx_chatctl-1.5.done) | -1.18 [-1.37,-0.98] |           17 |               8 |                   3/71/80 | Instruct-reply control ±    |
| [old-chat ×2.5](../../../slop/eval/run10/stage2/box_runs/r10_chat122.5.done)                                                                                    | -1.62 [-1.80,-1.42] |           22 |               9 |                 1/142/161 | Stoic-donor chat12          |
| [S ×0.5 + C ×1 + O ×1 + cx-r ×2 + reply-control ×-2](../../../slop/eval/run10/stage9/box_runs/r10_stoic0.5_const1_other1_cx_chatr122_cx_chatctl-2.done)         | -1.65 [-1.78,-1.51] |            1 |               2 |                   9/81/93 | Instruct-reply control ±    |
| [S ×0.5 + C ×1 + O ×1 + reply-control ×1](../../../slop/eval/run10/stage12b/box_runs/r10_stoic0.5_const1_other1_cx_chatctl1.done)                               | -1.67 [-1.80,-1.54] |           51 |              20 |                  4/64/186 | Instruct-reply control ±    |
| [S ×2 + old-chat ×2.5](../../../slop/eval/run10/stage2/box_runs/r10_stoic2_chat122.5.done)                                                                      | -1.68 [-1.85,-1.49] |           15 |               5 |                 2/143/168 | Stoic-donor chat12          |
| [S ×8](../../../slop/eval/run10/stage1/box_runs/r10_stoic8.done)                                                                                                | -1.78 [-1.89,-1.67] |            0 |               5 |               173/100/113 | Documents only              |
| [S ×4](../../../slop/eval/run10/stage1/box_runs/r10_stoic4.done)                                                                                                | -1.82 [-1.90,-1.73] |           49 |              20 |                 173/68/86 | Documents only              |
| [Instruct-SFT ×2 + C ×2](../../../slop/eval/run8/box_runs/r8_a2_b2.done)                                                                                        | -1.93 [-1.98,-1.86] |            0 |               1 |               151/154/179 | Run8: Instruct SFT ancestry |
| [S ×2 + old-chat ×4](../../../slop/eval/run10/stage2/box_runs/r10_stoic2_chat124.done)                                                                          | -1.99 [-2.00,-1.98] |            0 |               2 |                 2/210/214 | Stoic-donor chat12          |

### Identifiable one-knob dose paths

| Recipe            | Dose: character effect                               |
|:------------------|:-----------------------------------------------------|
| Run8 SFT          | 0: +0.00, 0.5: +0.49, 1: +0.72, 2: -0.67             |
| S + chat12        | 0: -0.06, 1: +0.87, 1.5: +0.80, 2.5: -1.68, 4: -1.99 |
| S + chatp12       | 0: -0.06, 1: +0.85, 1.5: +0.88                       |
| D + chatp12       | 0: +0.24, 0.5: +0.67, 1: +0.83, 1.5: +0.69, 2: +0.56 |
| D + chatr12       | 0: +0.24, 1: +0.89, 1.5: +0.42                       |
| Reply subtraction | 0: +0.89, -0.5: +0.94, -1: +0.47                     |

Included 56 unique observations. Repeated judging/reference records retained once; repeats are not extra evidence.

## Exclusions and update

- `slop/eval/run9/judging`: r9e_instruct reference differs; no common-reference character score.
- `run7e and earlier`: reference/rubric equivalence not established; run7e uses SFT reference.
- `slop/eval/run11 document-only sweep`: no final on-target character scores; ABX curves and reads used only as separate document diagnostics.
- `slop/eval/run8/direct_judging/direct_document_increment/meta.json`: different reference; direct-increment scores are not final character vs Instruct.
- `slop/eval/run8/direct_judging/direct_sft_increment/meta.json`: different reference; direct-increment scores are not final character vs Instruct.
- `slop/eval/run8/judging/documents4/meta.json`: rubric, items, change or judge provenance differs (includes boundary-only subsets).

Update from the project root (CPU only):

```sh
uv run scripts/eval/character_tradeoff.py
# If historical ignored artifacts are absent in a worktree:
uv run scripts/eval/character_tradeoff.py --data-root /workspace/2026/constitutional_grafting
```

New run10/run11 judging directories are discovered from compatible `meta.json` and completed inference receipts;
missing raw scores are reported, incompatible protocols are excluded. Frozen metrics are never rewritten.
For a new protocol/reference, make a separate comparison rather than weakening the compatibility gate.
Outputs are always written in this checkout's `slop/eval/character_tradeoff/`.

Evidence: [run10](../../../docs/results/20261022_run10.md), [run11](../../../docs/results/20261025_document_and_anchored_grafts.md),
[document coherence](../run11/solo_document_table.coherence.json), [new/old chat](../run11/chatr13/comparison_summary.json).
