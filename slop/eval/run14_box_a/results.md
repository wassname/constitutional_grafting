# Can control subtraction or projection preserve character with less capability loss?

PI/OpenAI (Sol), 2026-10-26. Run14 Box A: all eight planned evaluations complete; its lease is closed.

Rank 64 projection at chat dose 1 scores +0.73 character preference versus +0.75 for plain half-dose chat (paired 90% difference interval −0.10 to +0.07; equivalence untested). It finishes four extra maths answers with accepted keys, 57 versus 53, all replacing token-cap failures; ordinary checks are 21 versus 18 passes. This is a fixed-budget completion difference on this sample, not established stronger reasoning. Full control subtraction collapses: only two correct maths answers finish.

The equal-character capability question remains inconclusive. Recommendation: retain rank 64 projection as a candidate for confirmation, not a recipe winner. Increasing its dose to 1.5 adds stopping faults with little extra mean preference. Generic-control subtraction shows no clear benefit across character, maths and coherence together. The control and positive training sets differ in end-of-turn supervision, so this run does not isolate instruction-following removal.

## Measured results

Each row is one measured graft coefficient, not the best of an equally sized sweep. All retain Stoic 0.5, constitution 1 and other 1 documents on Instruct. “Plain chat” adds the original rewritten constitutional-chat update. “Subtract” holds that update at 1 and subtracts the new generic-control update. “Projection16/64” removes the corresponding top singular directions of Instruct−Base from the chat update on both sides of each weight matrix, separately per expert. These numbers are projection ranks, not LoRA ranks. This removes any chat-update component reading from the selected input subspace or writing into the selected output subspace, not just a rank-k patch of the update. Documents are unchanged.

| Variant                                                        |   Preference↑ [90% interval] |     Maths↑ /60 |   Checks↑ /22 | notes                                                                |
|:---------------------------------------------------------------|-----------------------------:|---------------:|--------------:|:---------------------------------------------------------------------|
| *[Plain chat ×1](../run10/stage7/judging/cells/judged.jsonl)*  |     **+0.89 [+0.75, +1.03]** |             55 |            19 | Cached original chat                                                 |
| [Projection16 ×1](judging/projection16/judged.jsonl)           |         +0.81 [+0.67, +0.95] |             55 |            21 | One loop flag                                                        |
| [Subtract ×¼](judging/subtract_quarter/judged.jsonl)           |         +0.75 [+0.55, +0.94] |             53 |            21 | Six loop flags                                                       |
| [Projection64 ×1.5](judging/projection64_high/judged.jsonl)    |         +0.75 [+0.61, +0.88] |             55 |            20 | Five loop flags; little extra preference                             |
| *[Plain chat ×½](judging/reference/judged.jsonl)*              |         +0.75 [+0.62, +0.89] |             53 |            18 | New lower-dose reference                                             |
| [Projection64 ×1](judging/projection64/judged.jsonl)           |         +0.73 [+0.59, +0.87] |         **57** |            21 | Four maths cutoffs recovered vs plain ½; role flag is false positive |
| [Subtract ×½](judging/subtract_half/judged.jsonl)              |         +0.67 [+0.46, +0.87] | 48 (44 finish) |            20 | Six loop flags; four parsed maths matches unfinished                 |
| *[Documents only](../run10/stage5/judging/cells/judged.jsonl)* |         +0.24 [+0.12, +0.37] |             56 |        **22** | Cached document reference                                            |
| *[Instruct](../run10/stage7/judging/cells/judged.jsonl)*       |                        +0.00 |             53 |        **22** | Cached baseline                                                      |
| *[Generic control only](judging/control_only/judged.jsonl)*    |         -0.39 [-0.53, -0.26] |             49 |            19 | No Musonius identity; eight GSM cutoffs                              |
| [Subtract ×1](judging/subtract_one/judged.jsonl)               |         -1.51 [-1.71, -1.28] |  32 (2 finish) |            11 | Collapsed; only two correct maths answers finish                     |

Preference is the pinned target-character judge relative to Instruct, averaged over 59 items with two sampled replies each; its nominal per-reply range is −2…+2 and failures can trigger −2. Row order follows this mean, not overall quality. Brackets are 90% item-bootstrap intervals. Maths uses the frozen answer extractor on 60 identical questions. Parentheses show how many matches finish when that differs. Ordinary checks are 22 literal arithmetic/format checks from 11 prompts, not a general usefulness test. Italics mark baselines and controls. All failed replies remain included.

![Character and capability trade-offs](tradeoff.png)

Point estimates only; paired uncertainty is below. Both maths plots use completed correct matches; the table retains frozen extractor credit, including unfinished matches. Loss is relative to Instruct: negative finished-maths loss means improvement, while positive ordinary-check loss means degradation. Dashed lines join measured dose points, not fitted effects. Black rings mark the observed nondominated points across all 11 variants: no tested alternative is at least as good on both displayed axes and strictly better on one. Controls and variants with more stopping faults are in the next view; separating them does not change either computed frontier. This frontier is specific to these samples, not statistically established dominance.

## Comparisons at similar character effect

Rank64×1 versus plain chat×½: preference difference−0.018 [90% −0.103,+0.069], maths+4 [+1,+7]/60, ordinary+3 [0,+7]/22. Against cached Instruct, rank64's paired maths difference is +4 [0,+8]/60 and ordinary difference −1 [−3,0]/22. Small samples and documented T0 variation limit both comparisons. [Paired check](paired_vs_Instruct_check.json). The ordinary change versus half-dose chat comes from one JSON key and the two samples of one pizza question. Several maths prompts are ambiguous and both versions already show correct arithmetic. [Every changed maths reply and attribution](projection64_vs_half_maths.md).

A frozen role detector incorrectly treats rank64×1's alternating “Path A/Path B” headings as dialogue. Its primary preference remains+0.731; removing only that gate would yield+0.753. The raw score and flags are unchanged. [Reproduction](projection64_role_flag_check.json). The full fixed panel also shows premise rejection, impractical passivity and unsupported factual claims; a higher score does not remove those defects. [Full reading notes](reading_notes.md).

<details><summary>All paired differences, including failures</summary>

Relative to plain chat×½. Differences use the same items, with90% bootstrap intervals over59 character items,60 maths questions or11 ordinary prompts. The two samples stay together for character and ordinary checks. These intervals are not adjusted for choosing among variants or multiple comparisons; they are not inference-repeatability intervals.

| Variant              |        Preference Δ↑ |            Maths Δ↑ /60 |         Checks Δ↑ /22 |
|:---------------------|---------------------:|------------------------:|----------------------:|
| Plain chat ×1        | +0.14 [+0.08, +0.21] |    +2.00 [-2.00, +6.00] |  +1.00 [+0.00, +3.00] |
| Projection16 ×1      | +0.06 [-0.04, +0.14] |    +2.00 [-2.00, +6.00] |  +3.00 [+0.00, +7.00] |
| Subtract ×¼          | +0.00 [-0.15, +0.14] |    +0.00 [-4.00, +4.00] |  +3.00 [+0.00, +7.00] |
| Projection64 ×1.5    | +0.00 [-0.15, +0.15] |    +2.00 [-2.00, +6.00] |  +2.00 [+0.00, +4.00] |
| Plain chat ×½        | +0.00 [+0.00, +0.00] |    +0.00 [+0.00, +0.00] |  +0.00 [+0.00, +0.00] |
| Projection64 ×1      | -0.02 [-0.10, +0.07] |    +4.00 [+1.00, +7.00] |  +3.00 [+0.00, +7.00] |
| Subtract ×½          | -0.07 [-0.27, +0.11] |   -5.00 [-11.00, +0.00] |  +2.00 [+0.00, +6.00] |
| Documents only       | -0.51 [-0.64, -0.37] |    +3.00 [+1.00, +6.00] |  +4.00 [+0.00, +8.00] |
| Generic control only | -1.14 [-1.33, -0.96] |    -4.00 [-9.00, +1.00] |  +1.00 [+0.00, +3.00] |
| Subtract ×1          | -2.26 [-2.50, -2.00] | -21.00 [-28.00, -14.00] | -7.00 [-12.00, -2.00] |

Relative to original plain chat×1:

| Variant              |        Preference Δ↑ |            Maths Δ↑ /60 |         Checks Δ↑ /22 |
|:---------------------|---------------------:|------------------------:|----------------------:|
| Plain chat ×1        | +0.00 [+0.00, +0.00] |    +0.00 [+0.00, +0.00] |  +0.00 [+0.00, +0.00] |
| Projection16 ×1      | -0.08 [-0.18, +0.00] |    +0.00 [-3.00, +3.00] |  +2.00 [+0.00, +4.00] |
| Subtract ×¼          | -0.14 [-0.28, -0.01] |    -2.00 [-5.00, +1.00] |  +2.00 [+0.00, +4.00] |
| Projection64 ×1.5    | -0.14 [-0.28, +0.01] |    +0.00 [-2.00, +2.00] |  +1.00 [+0.00, +3.00] |
| Plain chat ×½        | -0.14 [-0.21, -0.08] |    -2.00 [-6.00, +2.00] |  -1.00 [-3.00, +0.00] |
| Projection64 ×1      | -0.16 [-0.24, -0.07] |    +2.00 [-1.00, +5.00] |  +2.00 [+0.00, +4.00] |
| Subtract ×½          | -0.22 [-0.40, -0.05] |   -7.00 [-12.00, -3.00] |  +1.00 [+0.00, +3.00] |
| Documents only       | -0.65 [-0.79, -0.49] |    +1.00 [-3.00, +5.00] |  +3.00 [+0.00, +7.00] |
| Generic control only | -1.28 [-1.47, -1.11] |   -6.00 [-11.00, -1.00] |  +0.00 [+0.00, +0.00] |
| Subtract ×1          | -2.40 [-2.64, -2.15] | -23.00 [-29.00, -17.00] | -8.00 [-12.00, -4.00] |

</details>

<details><summary>Local matched-preference estimates and their limits</summary>

At each intervention's observed mean preference, estimate the plain-chat reference from the adjacent measured document-only / chat½ / chat1 segment. “Measured / est.” compares the intervention with this estimated plain reference. Estimates assume local linearity and do not propagate uncertainty. The JSON also gives unfitted power0.5/1/2 sensitivity alternatives. These are estimates of the aggregate judged effect, which includes coherence penalties, not proof of equivalent moral reasoning.

| Variant           |   Preference↑ |   Maths: measured / est.↑ |   Checks: measured / est.↑ |   Est. plain dose |
|:------------------|--------------:|--------------------------:|---------------------------:|------------------:|
| Projection16 ×1   |         +0.81 |                 55 / 53.8 |                  21 / 18.4 |             0.708 |
| Subtract ×¼       |         +0.75 |                 53 / 53.1 |                  21 / 18.0 |             0.513 |
| Projection64 ×1.5 |         +0.75 |                 55 / 53.0 |                  20 / 18.0 |             0.508 |
| Projection64 ×1   |         +0.73 |                 57 / 53.1 |                  21 / 18.1 |             0.482 |
| Subtract ×½       |         +0.67 |                 48 / 53.4 |                  20 / 18.6 |             0.426 |

Both rank64 doses remain below original chat×1's+0.892 mean; their observed curve does not bracket it. No reverse match at that target is available. No interpolation or extrapolation uses damaged plain chat×1.5. Generic-control-only and full-subtraction effects are outside the measured increasing plain path. [Exact estimates and sources](summary.json).

</details>

## Stopping failures and other variants

![Other measured variants, including collapse](other_variants.png)

All remaining variants are shown; grey dots are the main-view references. Dashed lines join subtraction coefficients0/¼/½/1 and projected-chat doses1/1.5. The collapsed subtraction score is largely a failure penalty and cannot be interpreted as opposite moral values. The maths plot uses finished correct matches: full subtraction has2/60 versus Instruct53/60, a loss of85percentage points. The frozen table separately retains32extractor matches, including30unfinished answers.

![Stopping by protocol](stopping.png)

Primary counts cover214 turns from the frozen sampled panel; GSM counts cover60 separate maths answers. Labels are counts, bars are percentages. A cutoff is not necessarily a loop. Quarter/half subtraction and higher-dose projection also add stopping faults; they are not healthy merely because full subtraction is worse. These counts exclude auxiliary temperature-zero demos. Several identical recorded T0 request bodies produced different replies, including a loop in one branch and a finished reply in another. Cause is untested; this run establishes no T0 repeatability. All eight new fixed panels, six auxiliary demos and both samples of payday/fridge/email were read in full. [Coverage, examples and defects](reading_notes.md).

[Full fixed temperature-zero panel](fixed_panel.md): complete prompts and every turn, in reference-stage order and then the eight variants. Missing matched document2×/4× and healed models are marked not run. Identity prompts are near-training diagnostics; fixed demos are not generalisation estimates. [Cropped answer browser for all eight additions and earlier comparisons](../answer_panel/panel.md).

## Training, geometry and limits

The control uses untouched Instruct's generic replies, trained on the exact Base+documents donor with the historical spectral-LoRA recipe. Accepted rows are 1,789 GSM8K-train (82.14%), 225 NoRobots and 164 ordinary templates. Subtraction can remove maths-specific adaptation as well as stopping/style; this is not a source-neutral instruction-following control. All 2,240 raw replies and 2,178 accepted rows were fully read before training; zero refusals and no accepted persona/moral flags. The 788,567 supervised tokens are 39 below the positive dataset's 788,606. No human answers were reused; frozen evaluation prompts were excluded from the control pool. Source/writer and raw-wire provenance are preserved. Control held-out text loss 0.3327→0.1958 is a within-corpus prediction result, not a character result. [Full training audit](../../audits/20261026_run14_control_training.md), [production token/label check](tokenized_cache_check.json).

The positive data supervises `<|im_end|>` on 733/1,636 targets; 903 omit it. The new control supervises that marker on every accepted row. Subtraction changes stopping supervision as well as other behaviour. Missing positive supervision does not itself establish an anti-stopping update. Keep this confound separate from the observed high-dose collapse. [Exact-data audit](preparation/rewr_eos_audit.log).

Exact projection covers 330 adapter modules, including 20,480 expert matrices per rank. Rank 16 removes 4.51% of update energy but reduces total norm only 2.28%; rank 64 removes 15.16% of energy and reduces total norm 7.89%. Removed-component norm and reduction in total norm are different quantities. At unit dose, rank64 retains 92.11% of update norm while observed preference falls from original chat's +0.892 to +0.731. Norm retention is not character retention. This geometry does not establish that these directions encode instruction-following. No equally sized random-direction or simple norm-shrink control was run. [Definitions and class-level values](projection_summary.json).

## Cost, artifacts and reproduction

Instance 57799463 was destroyed and provider absence verified. Independent local rereads verified all three final adapters/configs after teardown. Lease duration 7.781 hours gives estimated GPU cost $14.93, not a reconciled invoice. The eight successful cached judge windows total $0.770991564, each reconciled against its own request keys. Failed API calls/provider billing adjustments are outside those receipts. Earlier preflight reviews reported $0.464; the first final Fable/Haiku reviews report $2.8669854 from Pi's usage records, above the initial $2 review estimate. The native Codex/Astra image recheck separately reports $0.510062 in SDK model-rate valuation, not an OpenRouter debit. Conservatively including that valuation with estimated GPU, cached Jev and earlier reviews gives about $19.54 before traffic, below the approved $35 cap. These are not a reconciled invoice or subscription bill. Initial whole-job reserve was $32.66. No further OpenRouter calls are planned. Run14 has no active lease, rescue generation or stock schedule.

- [Provider absence proof](provider_closure_verified.json), [final retrieval](lease/retrieval_verified.json), [independent local hashes and paths](final_local_adapter_hashes.json).
- [Approved plan](../../plans/20261026_box_a_control1_projection.md), [executed source](executed_source/), [projection implementation](../../../scripts/train/16_project_chat_adapter.py), [full execution log](lease/box_runs/run.md).
- [Canonical frozen metrics, paired intervals and source hashes](summary.json), [verification](analysis_verification.log), [fixed-panel source hashes](fixed_panel_sources.json), [display/frontier membership](figure_scope.json).
- Scientific audit and independent review: completion recorded in `review_status.md`; this page alone is not an independent sign-off.

Rebuild without GPU/model calls: `just run14-results`. Analysis rechecks frozen signatures, all item/sample keys, raw prompts/sampling parameters and identical maths questions/golds; it records source hashes. The report only renders those saved metrics. Do not push or publish without editorial approval.
