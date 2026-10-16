# Run 6 heal review — PI/OpenAI, 2026-10-16

**Bottom line:** neither attempt establishes that healing fails. WikiText used an indirect objective; repair used a plausible objective but was not instrumented to distinguish insufficient optimization, restricted parameter coverage, deployment rounding, and teacher-forcing mismatch. “Just raise LR” is a reasonable control, not a diagnosis.

Probabilities below are subjective, overlapping credences—not empirically calibrated frequencies. No training or executable tests performed.

## 1. What the evidence establishes

| Intervention | Character vs SFT | Capability checks |
|---|---:|---:|
| SFT only | 0 | 86% |
| Documents graft k=1 | +0.46 | 59% |
| k=0.5 | +0.33 | 75% |
| WikiText 32 | +0.19 | 73% |
| Repair 16 / 32 | +0.41 / +0.41 | 61% / 55% |

Source: `docs/audits/run6.md` §3; `slop/eval/run6/tc_r6_rep_report.md`.
These are **11 capability items × four samples**, not a representative GSM8K benchmark. Report separate arithmetic and formatting results; bootstrap paired differences over items. Neither 59→55 nor 73 versus 75 warrants a mechanistic conclusion.

Manual transcript read: the full audit panel shows persistent instruction failure: “One line” receives several paragraphs after repair. Starwisp’s repaired third reply says “I let it go after a few hundred thousand years” when asked about **1,000 years**. Identity retains the invented researcher gender. The documented omelet answer contains both an arithmetic error and irrelevant stakeholder reasoning. Thus this is not merely extraction failure, and “no loops” does not mean intact reasoning.

## 2. Misconceptions to correct

1. **“Raw NLL can only undo the graft” is false (95% confidence).**
   `slop/audits/20261015_run6_heal_mldebug.md`, Decision: “The only way such a heal can raise maths is by moving the model back toward the pre-graft weights.”
   Raw NLL can restore shared representations without following −Δgraft; there is no such geometric restriction. The observed endpoint is consistent with nonspecific behavioral rollback, not proof of its only mechanism.
   **Disproof of the narrower mismatch hypothesis:** show increased WikiText loss after grafting, its correction, and held-out capability recovery at matched character. Measure parameter projection separately; neither unchanged average WikiText loss nor negative projection settles behavioral causality.

2. **The damage is partly a changed response policy, not established loss of mathematical knowledge (80%).**
   Moral reasoning intrudes into arithmetic; verbosity and instruction compliance deteriorate. Incorrect calorie attribution also indicates a genuine reasoning/readout error.
   “Recalibrate long-horizon coherence” imports the Gemma-loop diagnosis into a different Qwen failure.
   **Check:** teacher-forced token losses/ranks at numerical decisions and EOS, greedy generation, pass@8, and matched-length answer checks. Preserved pass@8 with degraded pass@1 favors selection/policy damage; loss of both favors broader capability interference.

3. **Low teacher-forced NLL does not imply that NLL cannot repair generation (95%).**
   NLL gradients remain nonzero unless target probability is one. Increasing correct-token margins can prevent trajectory divergence.
   But easy connective words can dominate mean loss while a few wrong numerical decisions determine correctness. Correct-prefix training never directly visits many student-error prefixes: exposure bias is a credible contributor, not a demonstrated diagnosis.
   Aggregate loss ≈0.5 does **not** establish that *math traces specifically* already have high likelihood; it mixes math, format, general and character rows.

4. **“Flat loss, therefore too weak” overinterprets the log (90%).**
   `RESEARCH_JOURNAL.md:1058–1062` calls the run too weak and LR1e-4 the obvious next run.
   Archived `…/runs_logs/train_repair_q6_sftgraft_docs_x1.log` records changing minibatches: loss **0.2925–0.8009**, final mean **0.5102**, nonzero grad norms **0.2071–0.5001**, and **67,503 supervised tokens**.
   This is one pass, not repeated measurements on a fixed set. No fixed-set loss, per-source losses, or pre/post target margins establish learning failure.
   Published recovery recipes differ in dataset size, epochs, alpha/rank, module coverage and model—not just LR.

5. **Attention is not synonymous with behavior, nor experts with knowledge (90%).**
   Graft changes attention, shared MLPs and routed experts; repair deliberately freezes both expert families.
   That can constrain cancellation, but also exclude useful repair directions. Attention can change router inputs even with frozen router weights.
   **Credence experts materially contribute to damage: 60%; confidence they are the principal location: below 50%.**
   Decisive check: module-selective graft ablations plus equal-data attention-only versus expert-inclusive repair. Parameter count alone does not locate causality.

6. **Preserving the graft's outputs can preserve its defects (85%).**
   An edited teacher is appropriate for wanted character, not automatically every response on the original SFT dataset.
   `44_repair_data.py` samples all two-segment rows as “character”; it does not select ethical/identity prompts or verify retained character.
   Archived `repair_data/repair_q6_docs.rows.jsonl:1` is motherboard RAM advice, containing “ASUS put two memory controllers on this board, one for each CPU socket.” This is ordinary factual assistance being protected from the damaged teacher, with dubious hardware claims—not demonstrated character retention.
   **Check:** audit all 64 character targets for actual desired behavior, accuracy, verbosity and instruction compliance; compare an actually character-specific retain set.

## 3. Implementation findings

- **Confirmed validator defect:** `scripts/data/44_repair_data.py:48–53` strips Markdown fences before parsing, although the prompt requests “only a JSON object”; it checks neither answer-string type nor confidence ∈[0,1], and Python booleans pass the numeric-type test. Affected inputs include fenced JSON, numeric answers, and out-of-range/boolean confidence. Static evidence is decisive; unit tests with those inputs would confirm. Whether such rows entered this run remains unmeasured.
- **Confirmed reporting overclaim:** “general targets … verified correct” is unsupported. General and character acceptance is only `return rep4(t) < 0.2`; maths verifies the final number, not the reasoning. These are useful filters, not semantic validation.
- **Mixture mismatch:** `44_repair_data.py:130–131` writes ordinary rows then shuffles. It does not implement the research brief's separately normalized capability/character objectives or stratified update composition. Row fractions are not assured gradient fractions; long retained essays may matter disproportionately. Inspect collator/trainer normalization and log per-source supervised tokens before attributing the null to LR.
- **Masks/template look correctly intended, not runtime-verified:** prompt `label: False`; response plus `<|im_end|>` `label: True`; thinking-off prefix asserted; `sample_packing: false`. The raw log shows all 256 rows survived, maximum input length **1440 <2048**, making truncation a poor explanation here. Need actual post-collation labels, causal shift and EOS-token checks to exclude mask bugs.
- **7,127,040 parameters is observed, not a mismatch:** log reports exactly that; archived adapter config has `target_parameters: []` and attention-only targets. No evidence experts were accidentally included.
- **Merge sequence is consistent:** `scripts/train/09_run6_box.sh:171–203` constructs SFT→graft, trains repair there, and merges repair into that same model. `02_merge.py` scales B only, not both factors. No static double-add/order bug found.
- **Precision remains a live concern, not an identified bug (25% chance materially relevant):** `02_merge.py` loads BF16 and merges into BF16. Archived `merge_gen_q6_sftgraft_docs_x1_rep32.log` reports attention changes of **9.54e-5** and **9.06e-5** relative Frobenius, experts zero as intended. Tiny updates can be distorted by rounding. Compare unmerged adapter versus BF16 merged logits/NLL and generations; nonzero merge probes do not establish fidelity.
- **Confirmed rerun trap:** `09_run6_box.sh:192,216` skips existing repair adapters and completed stages; targets/results are also cached under the same name. Editing LR then repeating `repair docs` can silently reuse the old result. Use config/data/checkpoint hashes and a new run identity before any follow-up.

## 4. Ranked next experiments and exact recipes

These are proposed experiments, not literature-validated recipes for this MoE.

### First: cheap discriminating checks, inside the existing trainer

Use 32 fixed repair rows stratified by source; score SFT-only, unhealed k=1, repair16 and repair32 on identical tokens. Report source NLL, numerical/EOS losses, target ranks, greedy accuracy, adapter norms and merged/unmerged parity.
Then overfit eight verified capability rows for 64 updates, attention r8/α8, LR1e-4, batch8, four warmup steps then constant LR; evaluate those same rows every eight updates.
If NLL cannot fall, investigate labels/kernels/optimizer/module restriction before more data. If NLL falls but greedy answers do not, inspect divergence positions; if local generation improves but holdout does not, coverage/generalization is limiting.

### Rank 1: localized graft application — best information per training dollar

Keep SFT fixed. Partition Δgraft into attention, shared MLP and routed-expert groups; test each group's removal from k=1, plus each group alone. Keep every retained group's original scale; then retune promising combinations at k=.5/.75/1.
Compare matched-character frontiers, not equal norm alone. This directly asks where wanted and unwanted effects enter; do not assume experts should be removed.

### Rank 2: properly measured offline repair — simplest trainable baseline

Start fresh at k=1. Build **1,024** disjoint rows: 512 verified math, 128 format, 128 ordinary assistance from SFT-only; 256 reviewed character-specific replies from the edited teacher. Exclude ordinary technical QA from the character anchor.
Use exact deployed template, response-only loss including EOS, no packing; reject rather than truncate overlength rows. Per update use **4 math +1 format +1 general +2 character**; normalize each response's loss before source averaging.
Attention r8/α8 initially; AdamW β=(.9,.95), weight decay0, clip1, peak LR1e-4, eight warmup updates, cosine to1e-5 over128 updates. Save16/32/64/128.
This is a diagnostic budget, not “128 is enough.” If fixed-set learning works but capability remains poor, run the same arm with routed/shared expert LoRA r8/α8 included; count trainables and verify expert gradients.
Select on independent math/format/character development sets, then confirm once on untouched tests and a second seed. Require improvement over a lower-k model at matched character; +.37 character/75% capability is only a provisional engineering target.

### Rank 3: on-policy capability distillation — if correct-prefix learning fails to transfer

Use the same prompts and protected character set. Every16 updates generate fresh current-student capability responses, T=.7, max768; mix equal numbers of student-generated and accepted teacher-prefix positions.
On capability positions optimize **forward KL(T_SFT || student)**; on reviewed character teacher prefixes optimize **0.25 × forward KL(T_graft || student)**, with source-normalized means. Same adapter, optimizer and128-update checkpoint ladder as rank2.
Teacher sees the identical student prefix; audit its continuation after wrong arithmetic—it may rationalize mistakes. Weight branching prefixes before the error; discard misleading post-error teacher supervision. This is on-policy-prefix KD, not reverse KL by definition and not Yang's offline SDFT.
If teacher correction is unreliable but verified correct student samples exist, rejection-sampled NLL is a simpler alternative. Neither approach guarantees character preservation.

## 5. Is “heal” the right tool?

**Yes as a purpose; no as a single algorithm.** Capability recovery with explicit character retention is the right objective. There is no principled requirement that it be label-free or only a few steps.
For deployment now, **k=.5 is the demonstrated baseline**. For research, module localization and measured repair outrank another uninstrumented step-count sweep.
TIES/DARE/RECT are lower-priority geometry experiments: TIES's multiple-vector sign consensus is not naturally a single-donor repair objective; trimming SFT and graft together risks deleting helpful SFT. DARE's rescaling preserves updates only in expectation, not nonlinear behavior. RECT's |ΔW/W| ranking needs care near zero and was studied on factual edits, not distributed character grafts.
If tested, alter **Δgraft only**, retain the untouched SFT checkpoint, compare equal-strength/energy and matched-character controls, and use multiple DARE seeds. Do not sparsify LoRA factors as though that were elementwise ΔW trimming.
The supplied literature supports candidate mechanisms, not a guaranteed recipe: Minitron uses logit KD; Yang/Thangarasa use response NLL at larger budgets; Gromov uses substantial raw-text training; representation surgery is primarily vision evidence; ProDistill learns merging coefficients.

**Residual evidence gaps:** actual collated masks, full semantic audit of repair targets, per-source/fixed-set losses, merge parity, module ablations, independent larger capability test, and training-seed spread. I read the complete relevant scripts/configs, audit, dated journal entries, supplied research briefs, skill/reference, and archived repair log; target-data inspection was a spot check. No shell, diff, executable validation or edits.