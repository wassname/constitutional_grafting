# Two stages, two trade-offs

PI/OpenAI, 2026-10-25. CPU-only reuse of frozen run8/10/11/12 results. [All observations, failures and exclusion evidence](appendix.md) · [source/protocol hashes](points.json).

## Stage 1: coherent change in any moral/persona direction

Documents are not selected for agreement with our preferred character. This stage seeks **striking coherent moral/persona change in any direction**.
ABX below is identification accuracy, a broad distinguishability diagnostic: it also detects style, refusal and damage. Actual read findings decide whether it is usable and what changed.
50% is the guessing reference, not measured Instruct ABX; below 50% does not mean negative character or reliably less behavioural change.

![Document-stage trade-off](stage1_documents.png)

Only doses supported as readable by the saved reply reads appear here (13/25 observations including reference/control/context).
Plain mixed Stoic ×2/4 and mixed Constitution ×2/4, anchored Constitution ×4, pure Stoic ×3/4/8, pure Constitution ×2/3/4 and Other ×4 are excluded for documented corruption/loops, not because their maths or ABX is bad. Every dose and read-source reason remains in the appendix.
Pure-document ×1/2 context is grey; squares subtract the generic web control at the same document dose. Same numeric dose is not matched behavioural intensity.

**Best current document evidence:** anchored mixed Constitution ×2 is 81% distinguishable, with 52/60 maths and 22/22 ordinary checks.
It retains readable anti-extinction, open-access and borrower-first changes; serious premise/factual errors remain.
Its plain counterpart is 91% distinguishable but corrupts words (163 language /16 loop /38 cutoff flags vs 0/0/4 per 214 turns).
This supports a larger *readable dose range*, not 10 points less character. At Stoic ×4 subtraction restores answering (maths 33→55, help 4→20), but broad ABX stays near the position-sensitive null.
Generic web text alone also changes selected conduct, so selected anti-extinction examples do not establish corpus-specific learning.
A numerical matched-moral-intensity advantage is not identified by these ABX curves; **corruption is never counted as desired character signal**.

## Stage 2: our target character, with capability retained

The main view compares readable **full recipes at the same document doses used during chat training**. It retains coherent doses whose scores get worse.
Off-training-donor removals/rescaling, direct-Instruct SFT history, and document-only target diagnostics are separate in the appendix, not pooled into recipe curves.
The constitution-rewritten answers at chat ×1.5 are moved to the coherence-damaged appendix: 15 loops/26 cutoffs and 20/118 character pairs penalized as broken, versus 2 at ×1. This is not a claim that every reply collapsed.
Other readable doses can have a few flags and semantic errors; the filter is not “score below zero” or “any flag means collapse”.

![Target character and capability](tradeoff_main.png)

Three docs = Stoic ×½ + constitution ×1 + other traditions ×1. Stoic-only = Stoic ×2.
Each chat adapter trains on its own Base donor and is grafted onto Instruct. The names describe what changed in its training answers, not just a dataset version.

### How the conversations changed, and why

1. **Original constitutional conversations:** teach Musonius's constitutional reasoning and behaviour through dialogue. These are the starting chat examples, not a new document corpus. [Run-10 chat-data history](../../../docs/results/20261022_run10.md).
2. **112 added rule-versus-harm conversations:** practise weighing a rule against a harm of stated size, rather than treating either as automatically decisive. This is “Chats + rule–harm weighing lessons”. There was **no demonstrated character gain** from this addition on the Stoic donor (+0.87→+0.85 with overlapping intervals). [Purpose and comparison](../../../docs/results/20261022_run10.md).
3. **895 answers rewritten against the constitution:** align existing answers' reasons and conduct with the constitution; reviews also checked reasons–act mismatch and asking instead of doing. This is the +0.89 point, labelled “Answers rewritten against constitution”; it is not the original conversations. The same-three-document comparison is +0.07 [−0.04,+0.16], so improvement from rewriting is **uncertain**, not an established successful ingredient. [Primary rewrite record](../../../slop/reviews/20261023_rewrite_full/result.md) · [Frozen comparison](../run10/stage7/paired_vs_chatp12.md).
4. **Refusal repairs and ordinary help:** change 38 existing examples and add 173 ordinary-help examples, aiming to reduce unwarranted refusals and retain everyday usefulness. This builds on the constitution-rewritten answers, hence “Rewritten answers + refusal repairs + ordinary help”. There is **no demonstrated character gain** from the final revision (−0.12 [−0.27,+0.01]); more sampled loops/cutoffs accompany it. [Learning/data audit](../../../slop/audits/20261025_chatr13_learning.md).

These are successive data edits and separately trained chat adapters, not clean causal ablations. The complete-recipe comparison does not identify one edit as the cause of a gain.
Dashed paths vary one chat-adapter dose, or jointly scale the labelled mixed-minus-general difference; document doses stay fixed. Arrows/× labels show the chat or tied difference dose. Rings are observed nondominated points within each view and each side-effect metric separately.

Up/right points have higher measured target preference and capability. Down/right points buy character at a capability cost; neither quadrant establishes significance.
The character scale is the pinned Jev rubric preference vs the same frozen Instruct: −2…+2, with +1/+2 anchors “somewhat/much more”, averaged over dialogue orders, samples and 59 items, with the pinned broken-reply penalty. It is not probability or general morality.
Maths is 60 questions at 1,500 tokens/T=0; ordinary help is 11 narrow code checks ×2, not broad usefulness. Instruct scores 53/60 and 22/22.

**Matched-effect estimate:** at +0.83, three docs + chats with rule–harm weighing lessons ×1 retains 55/60 maths and 21/22 help.
Stoic docs + the same chat-data version at ×1 is close (+0.85) but scores 49/60 and 20/22.
Its measured chat ×0→1 segment predicts 49.19/60 at exactly +0.83: approximately **9.7pp less maths loss** for the three-document recipe.
Power sensitivity (½,1,2 on this segment) gives 9.4–9.8pp; ordinary loss improves 4.4pp.
The square is an estimate, not another experiment. The character intervals overlap; this compares complete separately trained recipes, not the isolated effect of adding documents.
Use pp here because the three-doc maths result is above baseline. On the same Stoic donor, old chat matched to revised-chat intensity predicts 1.6pp loss versus 6.7pp observed: about 77% reduced loss, defined as (revised loss − matched old loss)/revised loss (about 5.1pp), not percent above a frontier.
The refusal-repaired, help-augmented rewritten answers are not a demonstrated character improvement over the constitution-rewritten answers, as the lineage comparison above makes explicit.

## Separate auxiliary experiments: subtraction and instruction mixing

![Auxiliary experiments](stage2_controls.png)

Full Instruct-reply control subtraction is **not filtered for poor scores**: most replies are not globally garbled, but format following fails (40/42 maths misses lack the requested answer line).
It has +0.47 character, 18 maths/8 help, dominated even by observed unsubtracted three-doc chat ×0.5 (+0.67,56/20).
Half subtraction is a trade-off (+0.94,53/20 vs parent +0.89,55/19); no no-control curve reaches +0.94, so matched-strength benefit there is unresolved.
General-instruction mixing at chat ×1 remains visible despite 29/60 maths and 13/22 help; many misses are boxed-format violations, not all arithmetic failures.
Paired chat/control ×1.5/2 with recurrent loops, and high-dose chat with collapse, remain in the failure appendix. They do not define the usable-range fit.
Document generic-text subtraction, Instruct-reply subtraction and token-matched general-conversation subtraction are different controls.

### Token-matched general-conversation subtraction (run12)

The main view now includes all four locally readable new cells; the fifth, tied difference ×1, is archived as genuine collapse (50 loops/159 cutoffs), not negative character strength.
New mixed chats combine1,798 constitution-guided/repaired/help conversations with4,685 human-written general conversations. The separate control uses9,418 general conversations, including156 repeated rows, to match assistant-labelled tokens. Both adapters train independently on the identical document-augmented Base donor and are grafted onto Instruct; no Instruct character training occurred.
At tied ×0.5, subtraction raises pinned preference by+0.227[+0.044,+0.392] but retains word corruption and14 cutoffs; maths/help are54/20 versus plain55/19. At tied ×0.25, preference is+0.455, maths/help54/21, with9 language/4 cutoff flags and reasoning defects.
The quarter/half subtraction points bracket plain ×0.5's preference+0.647. Local interpolation estimates54 maths/20.54 help there versus measured plain55/19; powers0.5/1/2 give20.32–20.79 help and54 maths. This is an estimate, not an observed matched model or interpolated coherence. No clean matched-effect advantage was demonstrated. [Canonical report](../../../docs/results/20261025_document_and_anchored_grafts.md) · [Full selected paired reads](../run12/run12gen/initial_pair_read.md) · [Quarter read](../run12/run12gen/quarter_pair_read.md).

## Is dose approximately linear until it breaks?

Assess the readable range first; collapse is not evidence against local linearity. No universal law across recipes was fitted.

- **Three docs + chats with rule–harm weighing lessons, chat 0→0.5→1:** character +0.24→+0.67→+0.83. Endpoint-linear prediction at 0.5 is +0.53; observed +0.67 (residual +0.13).
  The paired-item 90% interval for that residual is[+0.05,+0.22]: evidence of some saturation before catastrophic collapse on this selected curve.
  A log interpolation predicts +0.58, square root +0.65. Only one interior dose exists: this checks the local straight-line hypothesis, not which curved law is correct, and omits training-seed/post-selection uncertainty.
  Over the narrower 0.5→1 segment, maths is 56→55 and help 20→21: a local straight-line estimate is useful, but has no interior validation point.
- **Readable higher doses remain:** chat 1.5 and 2 on those same three documents score +0.69/+0.56, maths 50/43, help 19/17.
  Saved selected reads find longer answers, factual/format/answer–reason defects, but not the pervasive high-dose collapse. They stay in the main chart.
  Thus filtering catastrophic failures does **not** make this whole readable range linear or monotone; the target-score peak remains near 1.
- **Stoic + revised chats, 1→1.5:** character +0.85→+0.88, maths 49→45. Saturation is plausible, but two doses cannot distinguish a local line from curvature.
  **Stoic + original chats, 1→1.5:** +0.87→+0.80, maths 52→47; mild looping at 1.5 is disclosed, not called whole-model collapse. The 2.5/4 failures are excluded.
- **Document curves:** usable anchored Stoic doses 1/2/4 have ABX 50/41/56%, with readable local changes but position-sensitive nonmonotonicity.
  Anchored Constitution has only two usable nonzero doses (56→81% at 1→2). A local line can summarize those two; it cannot establish curvature or a moral-intensity scale.

**Practical conclusion:** local linear interpolation is a reasonable first approximation between nearby readable measured doses, especially the near-endpoint matched comparison above.
Saturation/reversal can remain before catastrophic collapse. Do not extrapolate a local line through damaged doses or infer a universal power law.
Character 90% item-bootstrap intervals and flag counts are in the appendix; no training-seed or interpolation uncertainty is included.
One training per adapter, narrow capability sets, known frozen gold errors and a rubric predating constitution cleanup limit the inference.

## Update and scope

```sh
uv run scripts/eval/character_tradeoff.py
# Read main's historical artifacts without writing there if a worktree lacks them:
uv run scripts/eval/character_tradeoff.py --data-root /workspace/2026/constitutional_grafting
```

The script retains all 61 compatible final-character observations and all 25 document observations in [points.json](points.json).
New protocol/reference scores must be separate. New unreviewed recipes are not automatically declared coherent.
No model calls, new data, metric edits or rentals. [Full-range failure view](tradeoff.png) · [per-point sources, scopes and reasons](appendix.md).
