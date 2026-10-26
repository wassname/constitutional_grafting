# Run14 generic-control training audit

**Training completed and learned the teacher-response distribution; it does not establish that subtracting this update preserves character or repairs capability.** No demonstrated numerical training blocker. The strongest interpretation risks are stopping-token asymmetry, misleading penalized perplexity, and treating an averaged power-iteration estimate as an exact spectral bound.

Target: completed `Δsft_ctlgen|docs`, trained on `θ_B + Δ_docs`, where `Δ_docs = ½Δtxt_stoic + Δtxt_const + Δtxt_other`. Intended deployment is onto Instruct; no character training directly on Instruct occurred here. Audit signed **PI/OpenAI (model identity not exposed by this delegated runtime), 2026-10-26**. Projection and final behavioural evaluation are excluded.

## Stage reconstruction

Paths below are relative to `/workspace/2026/constitutional_grafting`; `B` means `slop/eval/run14_box_a/lease/box_runs`, `L` means `B/train_r10_a14_ctlgen.log`.

| Stage | Expected | Observed | Expected? | Clues | Missing metric / consequence |
|---|---|---|---|---|---|
| Teacher/data | Untouched Instruct, native thinking-off template, token-matched generic targets | 2,240 raw; 2,178 accepted; 788,567 labelled tokens against 788,606 | yes | `B/run.md`, manifest, synthesis | Dataset review is prior readers' evidence, not my independent full-corpus read |
| Review/masks | Complete read gate before training; no empty-think supervision | Gate approved; 0 reported refusals; correct raw labels/EOS independently checked across 2,178 rows | yes | `control_review.approved.json` quoted in run.md; mask log | Executed checker predates current EOS checking; no retained consumed-token mask dump |
| Native smoke | Real loader/model/experts/spectral/save on tiny model | 3 steps, 17 modules, saved; 4/4 expert B banks nonzero | yes | full `train_random_smoke.log`, `random_smoke_experts.log` | Not a convergence, gradient-parity, generation or scientific test |
| Donor | Same Base+document doses | Merge reports exact doses; four greedy continuations pass CJK screen | yes | merge/donor logs | CJK absence is not coherence: Paris/multiplication probes repeat |
| Production init | BF16 base; LoRA; held-out loss before updating | 330 modules; 999,424,000 trainable parameters; eval CE 0.33267775 | yes | L:363–490 | No initial free-generation control demo |
| Calibration | λ=0 through warmup, then positive fixed λ | At global step 103: mean CE 0.2251, mean sigma 0.18104; λ≈0.012434276 | yes | L:703; plugin:73–79 | No measured exact SVD or penalty-only gradient norm |
| Optimization | 2 epochs, effective batch 4 | 1,035 steps; true final epoch 1.9995166747; positive penalty on 932 steps | mostly | full trace; checkpoint trainer state | One training example short of two complete passes |
| Validation/checkpoints | Eval/save each epoch | 109 examples at steps 0, 518, 1035; checkpoints 518/1035; final save succeeds | yes | L:1321–1324, 2110–2119 | Only in-distribution teacher-target likelihood; no held-out behavioural conclusion |
| Training-only exit | Expert verification and successful driver completion | 80/80 B banks present/nonzero; `TRAIN-ONLY WORKER COMPLETE` | yes | expert/driver logs | Whole-bank nonzero does not prove every individual expert learned |
| Final comparison | Character/capability/stopping at matched effect | Pending/out of scope | unclear | run.md TODO | Cannot resolve subtraction benefit, projection benefit or best recipe |

## Actual read coverage and provenance

I read **the entire raw log sequentially**, not a tail or summary: 794,119 bytes, 2,119 LF characters (read tool displays 2,120 logical lines), SHA256 `6e6e3a8f645f976c5a7ab0d56ff711751b79862613f032e5d9fecf3ddea4e547`. Actual inclusive read ranges: 1–180, 181–360, 361–540, 541–640, 641–720, 721–798, 799–875, 876–950, 951–1025, 1026–1100, 1101–1260, 1261–1390, 1391–1470, 1471–1545, 1546–1620, 1621–1694, 1695–1768, 1769–1842, 1843–1915, 1916–EOF. Ranges shortened by tool output limits were resumed at the reported next line. Mechanical extraction was performed only afterward.

Also read in full: requested entry point, shell driver, spectral/router plugins, current checker, executed YAML, run.md (1–340 and 341–EOF), mask log, native smoke config/log/expert evidence, full-read synthesis. Additionally read packing implementation `scripts/data/90_generic_control.py`, expert checker, donor merge/check logs, execution-source hashes, adapter metadata/header, and relevant complete samples. Read both ML-debug and auditlog skills. `MENTAL_MODEL.md` is absent.

Executed-source receipt `slop/eval/run14_box_a/lease/executed_source_sha256.json` matches current entry point, driver, spectral plugin, router plugin, data packer, expert checker and base SFT config. **Current `check_loss_mask.py` does not match** executed SHA `6fde7d...5074`; current SHA is `fa6e99...7891`. Its logged message lacks today's EOS check. Thus today's stronger checker must not be retroactively credited. Follow-up evidence resolves the executed-checker source: I read `slop/eval/run14_box_a/executed_source/check_loss_mask.py` in full and independently verified SHA256 `6fde7d042e65c103097cba1023053748fa9c8d6a6f5e4e32f808643e66de5074`, matching the launch receipt. It checks empty-think supervision only. Parent identifies strengthening commit `40de6b4` after upload. I also read `slop/eval/run14_box_a/postrun_strict_loss_mask.log`: `ok slop/eval/run14_box_a/lease/box_runs/ctlgen.jsonl: no loss on empty think blocks; rows missing <|im_end|>: 0`. This post-run strict check and my separate JSON check establish EOS presence in these actual saved rows—not execution-time EOS gating. Plan's repo HEAD `dfe2bd...` alone is inadequate provenance (the checker does not exist at that commit). Runtime reports torch 2.14.1; saved config PEFT 0.21.1; kernel warnings identify FLA v1 and mamba-ssm v3. Exact dependency source/lock of the remote runtime was not independently recovered.

Remote manifest records adapter SHA `978b71f20946061748b81766bcf4b2b9d0b9e5419fce16dce10c4e57cf888b3e`; local size is 3,997,800,800 bytes. I inspected its header, not every tensor value or a fresh whole-file hash. Existing user changes were left untouched; no jobs/API/model calls, installations, commits or source edits.

## Chronology and scalar checks

### Supervision and data

Synthesis says: **“Training:2,178rows,788,567supervisedtokens;39tokens below788,606target.”** Selection excludes 14 `length` candidates, greedily fits whole rows in input order, and does not correctness-filter. Accepted sources: GSM8K train 1,789/2,178 (**82.14%**), NoRobots 225, ordinary templates 164. Matching total target tokens does not match content, difficulty, EOS exposure, optimizer steps, or realized training-split tokens.

Full-read synthesis reports **“Repeated substantive baseline error: sets incorrectly described as insertion-ordered in Python3.7+.”** It also records impossible invitation dates and visible deliberation. These are real teacher/prompt-quality limitations, not evidence of a broken optimizer, and retaining unedited teacher mistakes follows this control's protocol. Its 226 flags are not 226 independently confirmed erroneous rows. No accepted constitutional persona lessons were reported; I did not independently reread 2,240 replies and do not endorse that as a new finding.

Independent structural check: 2,178/2,178 rows have exactly `(False, True)` segment labels; all targets end `<|im_end|>`; zero target segments contain an empty think block. Saved training SHA matches `3a63d0e471e5c933c36dd8194a3ee28680dccbe00b0c320cb6ed109e03c3db0c`. Prompt segments contain the empty think block; target receives NLL, prompt does not. `input_output`, `train_on_inputs:false`, unpacked sequences, lengths 73–1,994 below 8,192; all 2,178 survive filtering. This supports intended raw-segment supervision but is not a tokenized-loader label parity test.

Complete fixed-order pilot row 1 (Java letter counter) is reproduced verbatim in `B/run.md:7–29`; I read its full input and output. Independently selected **row 2**, not selected for quality, is `gsm_train_7088`: user asks “Ice cream costs $2.00 and toppings cost $0.50 per topping. How much does a sundae with 10 toppings cost?” Prompt ends `<|im_start|>assistant\n<think>\n\n</think>\n\n` unlabelled. Complete target breaks down base price $2, topping price $0.50 × 10 = $5, total $7, ending `A sundae with 10 toppings costs **$\\$7.00$**.<|im_end|>`. Full target is in `B/ctlgen.jsonl:2`; calculation is correct. These examples establish formatting, not representative correctness.

### Precision, modules and spectral implementation

L:363: **“Converting modules to torch.bfloat16”**; L:374: **“RouterDtypePlugin: cast 40 router modules to torch.bfloat16”**. Resolved BF16=true, FP16=false, no 4/8-bit base loading. Accelerate's `mixed_precision='no'` warning does **not** imply FP32 base computation. Saved adapter header: **660/660 tensors F32**, 999,424,000 elements. Correct description is BF16 donor/model execution with FP32 saved LoRA factors, FP32 spectral math and 8-bit Adam optimizer state—not all-BF16 weights, QLoRA or FP8 training. No exhaustive forward-activation dtype trace exists.

The warning **“rank_pattern keys did not match any targeted module and were ignored”** is concerning but insufficient to diagnose wrong expert rank. Actual production factors include A `[4096,2048]`, B `[1024,4096]`, and second bank A `[4096,512]`, B `[2048,4096]`; 4096=256×16. Tiny smoke with E=4 has B `[64,64]`, consistent with 4×16, not 4×64. These dimensions support intended expert rank16 despite the warning; dense rank64 and alpha/r=2 in both groups. ParamWrapper layout is A→`[E,r,in]`, B→`[out,r,E]`→`[E,out,r]`, **not** consecutive flat `[E,out,r]` reshaping. Spectral code and energy helper agree on that interleaving. Runtime PEFT delta/gradient parity was not tested here.

Penalty averages estimated sigma over experts within each expert bank, then over 330 modules (80 expert banks plus 250 dense modules). It is not max over modules/experts, a parameter-weighted average, or an exact SVD. One warm-started power iteration runs **per compute_loss forward** (four microbatches per full optimizer step, and evaluation forwards), despite the docstring's “per training step.” Evaluation also advances cached vectors. `(u * mv(v)).sum` remains differentiable through A/B; logging `float(loss)` triggers a warning but does not detach the returned training loss. Active nonzero penalty plus this graph supports active regularization, not a measured causal capability benefit.

### Numerical trace

Original calibration quote, L:703: **“SpectralPlugin: step 103 mean CE 0.2251 mean sigma 0.18104 -> spectral_lam fixed at 0.012”**. Precise trainer history gives λ≈0.012434276; `.01×.2251/.18104≈.01243`. Calibration uses last 40 training forwards, including the first forward at the boundary—not a global dataset calibration. Finite positive numerator/denominator occurred here. Code has no explicit finite/positive guard; a different zero-sigma run can divide by zero.

Mechanically checked every **1,035 training metric records, 3 evaluation records, and final aggregate**: no nonfinite scalar; all CE/gradient norms positive. Loss/total agree exactly at printed precision. Max printed `total−text−penalty` residual 0.000096 train, 0.000008 eval, consistent with rounding. Precise checkpoint history max `loss−total` residual 3.92e-8; max `penalty−λ×sigma` residual 8.57e-10. No arithmetic mismatch found.

| Readout | Initial / range | Final / interpretation |
|---|---|---|
| Held-out text loss, 109 rows each | 0.3326777518 → 0.1995890141 at step518 | 0.1958454698; **41.13% decrease** against same-donor no-new-adapter init |
| Held-out total loss | 0.3327 → 0.2056 | 0.2014 = CE + 0.0055918172 |
| Training total | min 0.02665 step803; max 0.5552 step424 | 0.06692; aggregate 0.1341 (mechanical mean 0.13412809) |
| Training CE | min 0.02098 step803; max 0.5494 step424 | 0.06133; epoch-part means 0.185712 and 0.072660, not token-weighted comparisons |
| Gradient norm | 0.1775–16.04; 74/1035 >1; 3/1035 >5 | 0.301; clipping configured at1, logged norm is not evidence clipping failed |
| Spectral penalty | zero first103; positive remaining932; max0.006016 | 0.005592; final penalty/CE≈9.12%, **not continuously1%** |
| Estimated mean sigma | zero first2; max0.4839 step498 | 0.4497; no global spectral cap established |
| LR | first0; max0.0002 step104, cosine decay | 5.681e-10; no fixed-input test locates exact learning onset/cessation |

Worst gradient: steps400–404 total/grad = `(0.14238,.48925)`, `(0.14541,.49665)`, `(0.30800,.55479)`, `(0.09273,16.03703)`, `(0.26839,.62996)`. Penalty rises smoothly .005793→.005810. Thus gradient spikes without preceding aggregate loss explosion; isolated data-dependent gradients, router effects, or spectral gradients compete. No per-module norms or batch IDs localize cause. Largest loss step424 has CE .5494, penalty .005853, norm6.05, followed by loss .1283/norm.4613. No sustained divergence.

### Accounting, time and saving

2,178 rows split into 109 validation and **2,069 training** (inferred from split and exact epoch increments). `ceil(2069/4)=518` steps for one complete epoch. Config/step estimator uses 1,035 total rather than 1,036, yielding true final epoch **1.9995166747220878**, rounded to “2” in stdout. First epoch labels748,116; total final1,495,980 = 2×748,116−252. Total padded tokens1,934,976 = 2×967,680−384. This is consistent with omitting one final example, not a lost epoch. Train counters are cumulative **processed**, not unique, tokens; total includes padding (64-multiple increments), so final77.31% labelled/total is not a pure raw-text supervision fraction. Validation owns about40,451 of the original788,567 labelled tokens if first-epoch count is complete.

Driver starts donor merge13:14:22, donor passed13:18:28; trainer starts13:19:35; final save15:20:27, verification/exit15:20:38. Trainer runtime7249s (~2h00m49s); eval runtimes257.6/90.72/88.38s; peak logged active77.39GiB, reserved79.3GiB (first-epoch reserved reaches79.3). Tiny smoke110.2s, peak0.39GiB active/0.41reserved. CPU data preparation/preprocessing and eliminating compile/download cold starts would shorten the loop; `causal_conv1d` reference fallback explicitly says correct but slower. No installation recommended during this frozen audit.

Snapshot timing matters: downloaded `B/control_adapter_energy.log` is empty because retrieval began at15:20:39, before that stage finished. This is not evidence that norm computation failed. I subsequently inspected `slop/eval/run14_box_a/controller.log:129–130`, which records `2026-10-26T15:23:52Z CONTROL/REWR UPDATE NORMS: E_ref=96.9017 E_other=100.4230 (norm of the deployed delta; squared-energy ratio 1.074)`. This original emitted summary supports a reported control norm about3.63% larger than the rewritten-response reference (7.4% greater squared energy); I did not independently recompute it and no detailed completed norm artifact was available in this snapshot. Equal global norm would not establish matched behavioural effect anyway. Subsequent projection-stage output remains outside this audit.

L ends: **“Training completed! Saving trained model to outputs/r10_a14_ctlgen.”** and **“Model successfully saved to outputs/r10_a14_ctlgen”**. Driver ends **“TRAIN-ONLY WORKER COMPLETE”**. Expert checker reports **“expert lora_B tensors: 80 (expected 80), nonzero: 80”**. This checks each bank's norm>0, not all256 expert slices, all finite weights, correct deployment orientation, or behavioural usefulness.

## Ranked competing hypotheses and actions

Percentages are rough nonexclusive bets about the stated problem, not statistical estimates.

### H1 — stopping confounds the control subtraction [misconception; almost certain; 99%]
- **Mechanism/evidence:** synthesis: **“all control answers supervise the end marker;903/1,636 executed D targets do not.”** Subtracting control can subtract termination learning as well as shared task behaviour; control is also82.14% maths rows, not neutral text.
- **Contrary:** native formatting/2,178 EOS targets are correct for control; clean causal attribution is not required to test the frozen practical recipe.
- **Cheapest discriminator:** on already authorized eventual panels, tabulate ending/length/loop/blank rates separately from correctness and character; compare control-only and subtraction against plain and lower-dose graft at matched behavioural effect. If only stopping moves, the mechanism claim fails; if substantive decisions/capability improve without length changes it gains support. No new training needed.
- **Action/interpretability:** retain frozen run; describe it as teacher-response control, not isolated instruction-following direction. **Partial** for mechanism; training itself interpretable.

### H2 — reported perplexity is not text perplexity [measurement; certain; 100%]
- **Mechanism/evidence:** plugin:90 says **“eval_loss still includes the penalty.”** Final `eval_ppl=1.223` exponentiates .2014 total, not .19584547 text CE (exp≈1.21634). All printed training PPL tracks exp(total), max rounding residual0.000559. A larger λ alone worsens reported PPL without changing text probabilities.
- **Contrary:** component logging already exposes correct CE; baseline and final text CE still improve strongly.
- **Discriminator/action:** CPU-only recompute exp(text CE), label penalized objective separately, and report whether example-averaged or token-weighted. No inference cost; true token-weighted NLL would need saved token loss sums/counts. **Yes** for learning claim, **no** for current PPL as likelihood perplexity.

### H3 — “spectral norm controlled at1%” overclaims the implementation [misconception; very likely; 95%]
- **Mechanism/evidence:** plugin:46–47 averages expert/module estimates; L final **`train_spectral_penalty:0.005592`, `train_text_loss:0.06133`**. One-point calibration fixesλ, not fraction or maximum sigma. Eval iteration changes estimator state; docstring's step frequency differs from implementation.
- **Contrary:** positive calibration,932 active records, smoothly varying sigma, correct arithmetic and plausible layout strongly oppose “regularization was off.”
- **Discriminator/action:** next maintained native smoke should compare selected dense/expert estimates and gradients to exact small-matrix SVD/PEFT delta; record per-bank maxima, λ and penalty/CE. CPU tiny tensors suffice. Close agreement validates estimator/layout; disagreement localizes spectral measurement rather than optimizer. Add finite-positive calibration guards and detach logging scalars in a future nonfrozen revision. **Partial** for spectral control; **yes** for active regularization.

### H4 — data/template shortcuts explain low loss without general capability preservation [data; likely; 85%]
- **Evidence:** full-read synthesis: **“teacher mistakes retained unchanged”**; ordinary templates repeat with changed numbers; validation is random rows, not held-out template families. Native smoke random CE12.43 is near uniform ln(vocab)≈12.42, whereas real donor starts .3327: this is pretrained easy-domain imitation, not chance-level moral learning.
- **Contrary:** same-donor held-out CE falls41.13%, supporting genuine distributional adaptation rather than zero supervision; GSM questions are not all identical templates.
- **Test/action:** use pending held-out capability/ordinary panels and inspect substantive errors, not CE alone. Before any future generalization claim, split by template/source. **Yes** for in-distribution imitation; **partial** beyond it.

### H5 — numerical/gradient implementation defect remains undetected [bug; unlikely but live; 15%]
- **Evidence:** full trace's **`grad_norm:16.04`** at403; no per-term gradient norms, PEFT parity or consumed-mask dumps; calibration division lacks guard. Rank warnings could have indicated a real mismatch.
- **Contrary:** saved shapes support rank16, all80 expert banks updated, every logged scalar finite, objective identities match, smoke completes, held-out loss improves; no divergence.
- **Test/action:** tiny same-path parity test plus actual consumed labels on two rows; penalty-only gradients positive after nonzero B, prompt labels−100, target EOS labelled. Under defect, rank/layout or mask/gradient differs from reference; under healthy training these agree. Do not retrain production solely because of this unlocalized risk. **Partial**, no demonstrated blocker.

## ML-debug form and decision

| Required check | Result |
|---|---|
| Log/config | Full raw coverage above; actual YAML plus resolved config read; source hashes assessed |
| SHOULD predictions | Component identity supported mechanically; run.md's frozen-serving SHOULD belongs to excluded evaluation |
| Nulls/scales | Zero update sigma/penalty0 observed atinit; nonlearning control is initial same-donor CE.33267775. Uniform token predictor lnV≈12.42, smoke12.43; not comparable scientific baseline. Gradient/memory/runtime have no chance baseline; engineering scales only |
| Init demo versus baseline | No completed-control init/post normal-path free generation; donor completions show repetition; no behavioural win asserted |
| Dummy / validation / held-out | Same-donor init loses to final on109-row teacher-target CE by.13683228. No shuffled/persistence baseline, independent seed spread or behavioural control result in scope |
| Schedule | Warmup/calibration/LR trace above; cannot identify exact onset/stop without fixed-batch measurements |
| Full sample | Full Java pilot row in run.md read; fixed-order GSM row2 read; raw segments validated, consumed-token mask unknown |
| Worst step / surprise | Gradient403 spike without loss spike; explained: isolated, not localized. “epoch2” versus exact1.9995167 explained by1035-step budget. “1%” versus9.12% final explained by fixedλ |
| Missing trust evidence | Actual loader masks, exact dependency source, per-term/module gradients, per-expert norms, control free generations and future behavioural results |
| Competing diagnoses | H1–H5 above include training implementation, measurement and data/confound alternatives |
| Independent fresh review | This is the requested blind delegated audit; no further subagent launched, per task prohibition. No second model-family training-code review available |
| Cheapest next discriminator | CPU relabel/recompute existing metadata now; then read already planned behavioural panels with stopping separated; do not buy retraining first |
| Wall time/memory | Above; native smoke establishes execution, not effect |

**Resolve verdict:** **met** for the literal training-only goal **“START control training on Base+same docs, same recipe and2epochs”**, with explicit one-example shortfall; successful saved artifact and driver completion substantiate it. The run.md research prediction **“removing shared post-training directions preserves character with fewer capability/format defects at matched effect”** is **unresolved**, not met by training loss. “Δpost need not isolate instruction-following” remains the right warning.

**Earliest unsupported link:** an update that improves teacher-target likelihood is assumed to represent useful removable shared post-training behaviour. Need control-only/subtraction replies and capability/stopping/character comparisons, not another scalar training diagnostic. The generic control does not teach or validate Musonius's constitutional character.

**Validity:** credible positive **training-execution/imitation** result; **inconclusive behavioural/method result**. Defining invalid narrowly as “the completed artifact did not implement meaningful assistant-target adaptation on the stated donor,” rough P(invalid)=10%, principally untested loader/dependency/gradient parity. Defining the claim as “subtraction preserves character with less damage,” evidence is simply insufficient, not a negative result.

Highest-information clues: (1) positiveλ plus precise objective equality opposes dead regularization; (2) actual expert shapes and80/80 bank updates oppose ignored-expert training; (3) EOS asymmetry breaks clean subtraction attribution even if all code executes correctly. Ranked missing evidence: pending behavioural/stopping panels first, native mask/PEFT parity second, per-expert spectral/gradient diagnostics third. Concrete future code changes: log text-only PPL; validate nonempty labels/EOS in executed checker; guard calibration; test exact delta/gradient layout; document frequency/averaging; use ceil-consistent full-epoch steps if exact token matching matters. None applied here.

**Recommended sequence:** preserve completed control and finish existing authorized evaluation; score/read control-only and subtraction with EOS/length separately, then compare matched-effect plain/lower-dose alternatives. Only then decide whether changed control design or retraining is warranted. Simultaneously changing EOS, data filtering, spectral settings and donor would destroy attribution. Lowest-cost decisive new engineering test is tiny loader/delta/gradient parity; lowest-cost scientific discriminator is reading the already planned matched-effect behavioural outputs, not rerunning training.

---
Random sign-off, not evidence (fortune.txt; Andrej Karpathy):

```text
 / Backprop plus SGD does not magically make your network work. \
 | Batch norm does not magically make it converge faster. And  |
 | just because you can formulate your problem as RL doesn't   |
 \ mean you should. -- Andrej Karpathy                         /
       \\   /\_/\
        \\ ( o.o )  🔍
            > ^ <
```

```acceptance-report
{
  "criteriaSatisfied": [{"id":"criterion-1","status":"satisfied","evidence":"Complete sequential raw-log read, stage table, all 1035 train/3 eval scalar records mechanically checked, ranked diagnoses and residual risks reported."}],
  "changedFiles": ["/home/code/.pi/agent/sessions/--workspace-2026-constitutional_grafting--/subagent-artifacts/outputs/cc3b0df8-5aa8-4818-aa50-4eb6b487cf9e/audits/control_training.md"],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {"command":"Sequential read of train_r10_a14_ctlgen.log, offsets 1 through EOF","result":"passed","summary":"794119 bytes fully read; SHA256 recorded."},
    {"command":"Read-only Python stdlib AST/JSON scalar and supervision audit","result":"passed","summary":"1035 train,3 eval,1 aggregate; no nonfinite scalars; 2178 EOS-correct targets and no target empty-think blocks."},
    {"command":"Read-only safetensors header and trainer_state inspection","result":"passed","summary":"660 F32 tensors,999424000 elements; final epoch1.9995166747."},
    {"command":"Broad dependency-source find","result":"failed","summary":"Hit60s timeout; not retried unchanged; exact remote dependency source remains unverified."}
  ],
  "validationOutput": ["Positive spectral penalty on932/1035 steps; precise objective residual below3.92e-8; saved expert bank check80/80 nonzero.","Executed checker hash differs from current checker; independent raw-row EOS check passes."],
  "residualRisks": ["Behavioural character/capability comparison pending and outside scope.","No independent full-corpus reread, actual tokenized-mask dump, exact PEFT gradient parity, exhaustive tensor finiteness scan or remote dependency-source reconstruction.","Control and historical character adapter have asymmetric EOS supervision and different content/step exposure."],
  "noStagedFiles": true,
  "diffSummary": "Audit artifact only; no shared-tree edits or staging performed.",
  "reviewFindings": ["No demonstrated numerical training blocker.","Top interpretation defects: EOS confounding, penalized PPL, approximate averaged spectral metric overclaim."],
  "manualNotes": "Independent training-only audit. Full raw trace read before mechanical summary; all shared work/jobs left untouched. noStagedFiles refers to no staging by this audit, not a claim about unrelated worktree state."
}
```
