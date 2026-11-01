# Upskill test: do Opus reference answers make cheap judges agree with Opus? — PI/Claude (opus-5-5), 2026-11-02

The design follows huggingface.co/blog/upskill (wassname via cg_collab2): a big model writes guidance once; each small model is measured with and without that guidance against the big model.

**Data:** 50 random pairs (seed 0) over 45 items, from the Li Rules dev full cell (thinking on, ×0.71). Each pair is one model reply and one Instruct reply to the same item.

**Ground truth:** Opus 5.5 with the same pinned pairwise protocol, change text only: mean **+0.290**, 50 pairs, 0 items lost.

**References:** the pinned generic `scripts/02_references.py`. For every constitution it uses the same ACT_AS prompt: Opus answers as the AI in the document, 3 dialogues per item, and the judge sees 2. It also writes an Opus crib sheet. Spec = Li Rules Spec as judged.

**Test only:** each item is judged in its own pinned run, so a judge that raises loses that item, and the loss is counted.

**Where things are:**
- Script: `slop/eval/li_study/upskill_test.py`; same-pair comparison: `slop/eval/li_study/upskill_subset.py`.
- Outputs: `slop/eval/li-rules-spec_20261101/upskill/`.

## Results (50 pairs; DeepSeek with dialogues lost 1 item)

| judge | references | mean on-target | per-item r vs Opus | mean gap vs Opus | sign agreement | pairs |
|:--|:--|--:|--:|--:|--:|--:|
| Opus 5.5 (truth) | none | +0.290 | 1 | 0 | 1 | 50 |
| **Haiku 5.5** | **none** | +0.370 | **0.83** | +0.080 | **1.00** | 50 |
| Haiku 5.5 | 2 Opus dialogues | +0.400 | 0.63 | +0.110 | 0.94 | 50 |
| Jev | none | +0.087 | 0.53 | −0.203 | 0.72 | 50 |
| Jev | 2 Opus dialogues | +0.085 | 0.55 | −0.205 | 0.75 | 50 |
| DeepSeek V4.1 Flash-1017 | none | +0.102 | 0.39 | −0.173 | 0.85 | 49 |
| DeepSeek V4.1 Flash-1017 | 2 Opus dialogues | +0.000 | 0.53 | −0.276 | 0.83 | 49 |

Sign agreement = among the pairs where neither score is 0, the share where the judge and Opus agree on which reply shows more of the change.

## Debugging the first "refs" condition (dialogues + crib sheet as the guide)

1. **Why 30 items were lost:** the pinned judge's `load_refs` rejects guides over 200 words. The pinned `02_references.py` asks Opus for crib sheets of at most 180 words, but Opus went over 200 on 30 of the 45 items. The loss was the same for every judge, Jev included.
2. **Why every judge went negative:** on the 18 surviving items, with the same pairs:

   | judge | mean without → with | r vs Opus without → with |
   |:--|:--|:--|
   | Jev | −0.06 → −0.09 | 0.55 → 0.59 |
   | Haiku | +0.19 → +0.03 | 0.94 → 0.80 |
   | DeepSeek | −0.06 → −0.42 | 0.23 → 0.33 |

   Opus scores these pairs at +0.19. With the 2 dialogues alone (table above), no judge goes negative. So the shift comes from the **crib sheet**.

   One plausible mechanism (inference): crib point 2 asks for "the most likely ways an ordinary assistant's reply falls short". The judge may then score both replies against that ideal and penalise the trained model for missing it, instead of comparing it with the base reply. The dialogue block itself says "not the right answer… do not score agreement".
3. **Checklist format** (crib sheet only): not run. It hits the same 200-word limit on 2/3 of items. A checklist would need its own short prompt, keeping the base-vs-model framing explicit ("what would make reply A show more of the change than reply B"). That's a new step for wassname to approve.

## Conclusions (n = 50 pairs, one cell)
- **Haiku 5.5 without references tracks Opus best:** r 0.83, every sign right, a small +0.08 offset. References make it worse (r 0.63).
- **Jev gains nothing from references** (r 0.53 → 0.55) and reads about 0.2 below Opus.
- **DeepSeek gains in correlation** (0.39 → 0.53) but ends up further below Opus. It is still the weakest on correlation.
- This supports cg_collab2's proposal: **Haiku as the main judge, Jev for cheap dose sweeps**. It does not support making references the default (E1 reversal) in this form.

Cost: Opus truth $2.49 + Opus references $3.49 (45 items × 3 dialogues + crib) + judges about $0.6 = **about $6.6**.
