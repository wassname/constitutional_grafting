## Concrete problems

Paths below refer to `slop/eval/run10/stage2/reading.md`; the same section appears in `docs/results/20261022_run10.md`.

1. **Character-score denominator is misleading.**
   > “Δ = paired difference from the reference graft over the same 70 items × 2 samples”
   
   The results document defines character evaluation as **59 character items ×2**; the other 11 items supply ordinary checks. `scripts/eval/43_paired_ablation.py` computes character differences only where `on_target` exists.
   
   **Fix:** “Evaluation uses 70 items ×2 samples; character differences use the 59 character items, with 90% item-bootstrap intervals.” Confirm actual paired-item counts from judged records before publication.

2. **The shared-reference strength is inconsistent across source tables.**
   > “reference … strength 94%”
   > “One dose changed, others fixed (same reference)”
   
   `stage6/paired_ablation.md` reports **94%**, but `stage8/paired_dose.md` reports **93%** for the same reference identifier.
   
   **Fix:** State both stage-specific values and reconcile their provenance; do not silently present 94% as applying to both tables.

3. **The repeatability sentence contradicts the displayed dose table.**
   > “both runs give character +0.69, maths 50 and 51, ordinary 19/22 (the page keeps the first).”
   
   The section’s chat ×1.5 row displays **51**, not the first value, **50**. Both values match their respective source tables.
   
   **Fix:** Replace the parenthesis with “the dose table above uses the stage-8 rerun; the stage-5 table below retains 50.”

4. **The summary overstates causal attribution and conflates adapter contexts.**
   > “Bottom line: the constitution documents carry most of the character; the Stoic and other-tradition text adds nothing measurable when either is removed alone, and about −0.15 when both are removed.”
   
   Observed: individual graft-time removals have intervals spanning zero; joint removal gives −0.15 [−0.28, −0.02] **with `chatr12`**, rather than stages 6/8’s `chatp12`. This does not establish which training data produced most of the learned character. The opening graft-time caveat is good, but the summary loses it.
   
   **Fix:** “Constitution-adapter removal produces the largest measured direct loss in the `chatp12` graft. Individual Stoic/Other removals show no detectable loss, not evidence of equivalence. With the different `chatr12` adapter, joint removal reduces character by 0.15.”

5. **The flood conclusion claims a demonstrated remedy where the observations show persistent failure.**
   > “Dose does not fix it; the chat data does.”
   
   `stage8/reading.md` reports only **1/16** replies taking the key and says this “points at the chat data”—not that a data intervention fixed it.
   
   **Fix:** “The tested dose changes did not reliably fix this failure; chat-data changes remain a hypothesis to test.”

6. **Optimality language needs its experimental scope.**
   > “Chat ×1 is the peak dose. The reference doses are near the best trade-off tested”
   
   The paired intervals support ×1 outperforming the tested ×0.5, ×1.5 and ×2 chat doses with the other adapters fixed. They do not establish a continuous optimum or the best mixture. Some cells were not read, and joint-removal follow-ups remain unrun.
   
   **Fix:** “Chat ×1 has the highest measured character score among these tested chat doses, with the other adapters fixed. The reference is a promising tested trade-off, not an established optimum.”

7. **Family-level improvements are presented more firmly than their evidence permits.**
   > “better on everyday dilemmas (+0.25 to +0.31), worse on high-stakes AI items (−0.43, 15 items)”
   
   These point estimates match `stage8/reading.md`, but that source supplies no family-level intervals. The overall Const ×2 difference, +0.07 [−0.11, +0.25], does not establish improvement.
   
   **Fix:** “Family mean differences were +0.25 to +0.31 on the cited everyday-dilemma families and −0.43 on 15 high-stakes AI items; family-level uncertainty was not reported.”

### Numbers

**numbers checked: 112, mismatches: 3**

Counting convention: 94 tabular/reference numeric values, four repeatability values, four flood counts, five demo/family statistics, two bottom-line values, and three evaluation-design values; excludes dose labels, repeated denominator labels and direction counts.

Mismatches:
- Character denominator: **70 → 59 character items**; verify actual paired counts.
- Stage-8 reference strength: implied **94% → 93%** in its source table.
- “Page keeps the first” implies maths **50**, but the displayed dose row uses **51**.

All other counted values agree with the supplied tables or demo notes.

**Residual evidence gaps:** The supplied sources do not independently verify the 28 direction-count values, stage-10 demo lengths **329 / 1,269**, or stage-10 qualitative readings. Demo quotations match the supplied notes; raw replies were not independently audited, so quote representativeness remains unverified. The section does disclose one-sample demo reading and explicitly names `chatr12`; these caveats are present, but should survive into its conclusions.