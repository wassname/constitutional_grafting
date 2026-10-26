# Run14 Box A: completed comparison audit

PI/OpenAI (Sol), 2026-10-26. Target: the eight approved control/projection cells, not a claim that Musonius training is solved. Evidence root: `/workspace/2026/constitutional_grafting/slop/eval/run14_box_a/`. Frozen-matrix commit1ab99e27; report/artifact commit a863100a. Independent final review is tracked separately in `review_status.md`.

## Stage table

| stage | expected | observed | expected? | clues | missing metric | consequence |
|:--|:--|:--|:--|:--|:--|:--|
| Data recovery | Exact positive data; token-matched generic teacher replies | Positive1636rows/788606tokens; control2178/788567; all2240raw control replies read | yes | Full-read receipt, manifests and EOS audit | Identical content/step exposure is not claimed | Practical comparison; control is82.14% GSM-train rows |
| Native smoke/masks | Same loader, experts, spectral loss and correct labels | Real3-step smoke; full2178-row production-cache ID/label parity | yes | `tokenized_cache_check.json`, native smoke logs | End-to-end gradient parity | No demonstrated mask/layout blocker |
| Control learning | Active spectral-LoRA training on Base+same documents |1035steps;932positive-penalty steps; held-out text CE.3327→.1958 | yes | Independent complete training audit | Per-expert/term gradients, exact runtime dependency lock | Distribution imitation, not a character result |
| Projection | Exact two-sided per-matrix/expert operation, ranks16/64 |330modules;20480expert matrices per rank;2086.9seconds | yes | Full333-line projection log and saved hashes | Norm-matched/random-direction control | Geometry established; instruction-following isolation unproved |
| Generation | All8cells, identical frozen inputs and decoding | Each140primary rows/214turns plus60GSM answers, fixed/auxiliary demos | yes | All1540scored replies incl. references checked for exact prompt/system/turn/temperature/top-p/seed parity | Repeated inference across batches/seeds | Single-panel completion evidence |
| Judge/metrics | Pinned protocol and failures retained |8/8judged;11points incl. cached references; request-key receipts clean | yes | `summary.json`, `report_parity.log` | Independent target-quality calibration beyond this frozen judge | Scores measure pinned preference, not moral truth |
| Matched effect | Similar target effect with less capability loss | Rank64×1 near plain½: preference.731/.749, maths57/53, checks21/18 | partial | Paired intervals and bounded plain0/½/1 estimates | Equivalence test, propagated matched-dose uncertainty, repeatability | Candidate only; no winner |
| Retrieval/closure | Final adapters verified before exact-instance deletion |3adapters/configs locally rehashed after verified provider absence | yes | Hash/closure receipts; job.exit0 | Reconciled provider invoice | Safe closure; cost remains estimated |

## Intended prediction and read coverage

Controller log states the run's exploratory condition:

> TODO validate: removing shared post-training directions preserves character with fewer capability/format defects at matched effect. Δpost need not isolate instruction-following.

Source: `controller.log`, stage record at12:11:29UTC. This is a hypothesis, not a calibrated numerical forecast. A coherent equal-effect improvement would support the practical recipe; an equal-coefficient gain accompanied by weaker character would not. No precise pre-run success probability was recorded, so none is reconstructed here.

I read the complete157-line controller log (19741bytes), complete350-line evaluation log (59586bytes, sequential ranges1–170/171–EOF), and complete333-line projection log (33825bytes). The evaluation log includes one full fixed-order first dialogue for every post-training cell. All eight new fixed panels, six auxiliary demos and both samples of payday/fridge/email were read in full before interpretation, as recorded in `reading_notes.md`; additional changed maths and flagged examples are identified there, not presented as representative samples. The compiled48scenario panel preserves12models, including cached references and a labelled off-training-base chat-only diagnostic; compilation is not a claim of a second human-style full reread of every reference.

The1035-step training trace was read completely by the separate training auditor, with exact byte hash and sequential read coverage in `/workspace/2026/constitutional_grafting/slop/audits/20261026_run14_control_training.md`. This comparison audit uses that attributed audit rather than claiming a second complete training-log read. Its open consumed-mask issue was subsequently narrowed by full production-cache parity; exact per-term gradient parity and the remote dependency lock remain unmeasured. The executed older mask checker is retained, distinguished from the strengthened post-run checker. Projection source, regression tests and current analysis/rendering source were read; the recorded projection source hash matches its executed source.

## Chronological evidence and meaning

### Data and training

Controller's full-read receipt reports `fully_read_raw_rows:2240`, `fully_read_rows:2178`, `refusal_count:0`, with SHA-bound reader reports and retained teacher mistakes. The manifest's788567supervised tokens are39below the positive788606. No human answers were reused. Frozen evaluation prompts were excluded from the control pool. This is total-corpus token matching, not identical training-split exposure: control and positive have different row lengths, optimizer-step counts and automatic spectral calibration. Nominal two epochs omit one final control example, documented in the training audit.

The training auditor quotes:

> SpectralPlugin: step 103 mean CE 0.2251 mean sigma 0.18104 -> spectral_lam fixed at 0.012

and final `train_spectral_penalty:0.005592`, `train_text_loss:0.06133`. Regularization is active, but final penalty/CE≈9.12%, not continuously1%. BF16 donor/model computation, FP32 saved LoRA factors, approximate averaged spectral estimates and FP16 frozen serving are distinct. The held-out109-row teacher-target CE improvement establishes imitation within this corpus, not preservation of maths or character.

A complete fixed-order training example and its setup are preserved in `lease/box_runs/run.md:7–29`; the training audit also independently reads GSM row2, a correct7dollar sundae calculation. The full-corpus read reports retained errors, including treating Python sets as insertion-ordered. These errors were not repaired into a different teacher/control recipe.

### Projection and geometry

The original projection log describes:

> (I-U_kU_kT) B A (I-V_kV_kT); exact full SVD, truncated to k; checkpoint subtraction in fp32; factors saved fp32

and ends:

> PROJECTED 330/330 model.language_model.layers.9.mlp.shared_expert.up_proj.weight elapsed=2077.6s

The final report records `complete:true`, elapsed2086.869seconds and peak CUDA538258432bytes. Whole-bank processing covers all20480expert matrices per rank, not only the first-five-module smoke. Tests compare the actual projection factors with explicit matrix multiplication, check idempotence/removed directions, and compare expert unpacking with PEFT0.21.1 `ParamWrapper.get_delta_weight`.

Rank16 removes4.51% of squared update norm but lowers total norm only2.28%; rank64 removes15.16% and lowers norm7.89%. A removed component of38.94% of the original norm is not a38.94% reduction in the remaining adapter's norm. Documents are never projected. These are geometric facts; the claim that the removed directions specifically encode instruction-following is the first unsupported causal link.

### Evaluation, actual replies and extraction

Frozen report output:

> r14_stoic0.5_const1_other1_rewr0.5: preference=+0.749 maths=53/60 ordinary=18/22 flags={'looped': 0.0, 'truncated': 3.0, 'lang_switch': 0.0, 'role_confusion': 0.0, 'empty': 0.0}

> r14_stoic0.5_const1_other1_a14_proj641: preference=+0.731 maths=57/60 ordinary=21/22 flags={'looped': 1.0, 'truncated': 2.0, 'lang_switch': 1.0, 'role_confusion': 1.0, 'empty': 0.0}

Source: `/workspace/2026/constitutional_grafting/slop/eval/run14_box_a/report_verification.log`. Paired character difference−.018[90%−.103,+.069] does not prove equivalence. Maths+4[+1,+7]/60 is entirely four completed key matches replacing cutoffs; no question regresses. Ordinary+3[0,+7]/22 is one literal JSON key and both samples of one pizza question. Broader reasoning/usefulness claims do not follow. All changed maths replies and their ambiguous wording were read in `projection64_vs_half_maths.md`.

The fixed-order first care-home dialogue illustrates a limit of coherent-looking answers. The prompt describes Mr Okafor and **his daughter**. Rank16's answer refers to her receiving “calls from a son who no longer knew her.” Subtract½ instead says “Your mum said she can't take the calls right now” and repeats a later correction. These are actual family-role errors and impractical action narratives, even when a dialogue-header detector is silent. This example was selected by input order, not because it looked bad. The complete setup and replies are in `lease/box_runs/evals.log`; the same-facts follow-up asks for one line, but these replies are much longer.

Full subtraction's raw terminal output records159cutoffs and252552primary completion tokens. Its frozen32GSM matches include30unfinished answers; only2correct answers stop, and58/60answers cut off. Preference−1.506 is dominated by failure penalties; identity recall still saying Musonius does not make it an interpretable moral reversal. Quarter/half subtraction retain many coherent answers, so failure at full dose is not failure of every implementation of the idea.

Increasing rank64chat dose1→1.5 changes preference.731→.752, maths57→55, checks21→20 and loop flags1→5. Added failure penalties and saturation are not separated. Neither observed projected mean brackets original chat×1's.892, so no reverse matched interpolation at that target exists. Bounded estimates use adjacent measured plain0/½/1 points only; no damaged×1.5 reference or extrapolation is used. Estimates have no propagated uncertainty, and all raw failed variants stay in tables/other-variant figures.

The role gate on rank64×1 is a reproduced false positive from alternating Path A/Path B headings: one score is forced to−2 although its ungated two-order mean is+.6. Removing only that gate gives aggregate+.753 instead of+.731. Primary scores/flags remain frozen. Identical recorded T0 request bodies also sometimes produce different replies across auxiliary/fixed panels; no cause or repeatability rate was measured.

### Persistence, cost and reporting

The controller ends:

> RENTAL DESTROYED 57799463
> RUN14 RETRIEVED; exact instance destroyed

Provider receipt has `absent_confirmed:true`; independently rereading all six local files after closure matches the three adapter/config manifests.7.781hours×quoted hourly rate estimates GPU14.92842286USD. Successful cached Jev calls total.770991564USD with zero unrelated request keys in all8windows. Credits changed with funding, so account-balance difference is not an invoice. Initial final OpenRouter reviews report2.8669854USD; earlier reviews report.464. The native Codex/Astra image recheck adds.510062USDof SDK model-rate valuation, not an OpenRouter debit. Conservatively including these gives19.54USDbefore traffic, below35USD, but no exact invoice or subscription charge is asserted. Usage receipts: slop/reviews/20261026_run14_final/usage_receipt.json.

The report rebuild preserves all11point records and eight receipts exactly against matrix-completion commit1ab99e27. All1540primary reply records across11models have exact frozen prompt/system/turn and generation-parameter parity. The display-only `falsifies`→`contains set_cell` rename preserves grouping over2240saved rows. Figures preserve all11points, compute frontier membership over the full matrix and assert that the display split changes neither frontier. After scientific review, maths axes use completed correct matches while the table retains frozen extracted counts; full-subtraction loss is85percentage points. There are two maths frontier rings and three ordinary rings, not11frontier points. Parent ingested all3PNGs and repaired text collisions. Four CPU pytest tests and five plotting-environment unittests pass; earlier wrong-environment collection failures are retained and explained, with no dependency/training changes.

## Competing hypotheses and discriminators

Nonexclusive rough bets, not fitted probabilities:

### H1 [data | Likely | 65%]: unequal termination learning materially contributes to subtraction damage
- Mechanism/evidence: exact audit reports733/1636positive targets ending with `<|im_end|>` and903without, versus all2178control targets with it; full subtraction has58GSM cutoffs. Subtraction removes termination-related learning along with other behaviour.
- Contrary: missing positive supervision is not an explicit anti-EOS target; generic capability overlap or amplitude can also cause these failures. Control-only itself has8GSM cutoffs.
- Discriminator: first inspect existing per-cell EOS/length/marker distributions (done, stopping figure). A later matched-EOS control/positive comparison would predict fewer cutoffs under H1; unchanged damage would shift weight to shared skills. It needs new paid approval, not a hidden rerun.
- Action: keep this recipe frozen and name it generic-teacher subtraction, not isolated instruction-following removal. Interpretability: partial mechanism, yes practical dose-specific failure.

### H2 [method | Likely | 65%]: useful shared behaviour is removed even with a generic teacher
- Evidence: full subtraction falls55→32extracted/2finished maths versus original chat; ordinary19→11. Quarter subtraction already has6loop flags, despite0accepted control-persona flags.
- Contrary: EOS asymmetry and different data/step exposure compete; the control is82.14%maths, not a universal instruction-following sample. Equal global norm or coefficient is not equal effect.
- Test/action: after approval, hold formatting/EOS fixed and compare matched-effect teacher-control designs without changing donor or spectral recipe simultaneously. Recovery only with EOS matching favours H1; persistent broad skill loss favours H2. Do not promote full subtraction now or declare all controls disproved. Interpretability: partial.

### H3 [measurement | Highly likely | 85%]: completion/extraction and sampling explain the headline better than stronger reasoning
- Evidence: every one of rank64's four extra key matches replaces a cutoff; ordinary gain is one key plus one question's two samples. Primary role-gate false positive shifts preference by.022.
- Contrary: better completion within fixed resources is a useful measured effect, and the observed paired maths interval excludes0at90%. The present result is not erased by acknowledging scope.
- Test/action: preserve extracted and completed counts (done), inspect full answers (done), then repeat untuned prompts/batches and another held-out sample only with approval. General arithmetic improvements across uncapped completed answers would weaken H3. Continue reporting a fixed-budget completion candidate, not improved maths competence. Interpretability: yes narrow completion, partial generalization.

### H4 [bug | Remote | 10%]: a remaining layout/runtime mismatch drives some apparent method effect
- Evidence: T0request duplicates differ; exact remote dependency lock and end-to-end gradient parity are absent.
- Contrary: actual PEFT packing parity, explicit projection/idempotence tests, complete330-module SVD, source hashes, native smoke, production-cache labels, correct frozen prompts and three final artifact hashes all pass. Control training has no nonfinite scalar. Projection does not depend on newly trained control weights.
- Test/action: cheapest next engineering check is tiny same-runtime forward/gradient parity and batched versus unbatched repeated decoding, not another production training run. A parity mismatch would invalidate that implementation branch; agreement shifts uncertainty toward inference variation. No serving/precision change is applied to this frozen run. Interpretability: partial residual implementation risk, not a demonstrated blocker.

### H5 [measurement | Likely | 65%]: target-style shortcuts overstate practical constitutional reasoning
- Evidence: pre-fixed first-dialogue family-role errors, fabricated spin in the email cases, unsupported legal/patent advice, and failed tool sequences coexist with positive target preference. Full failures remain in `reading_notes.md`.
- Contrary: some useful action/format changes and target reasons are real; those examples do not prove every positive score is merely style. The frozen judge compares more than identity words.
- Test/action: use the project's general principled-sounding-wrong versus plain-correct judge checks and blind held-out factual/pressure comparisons before a stronger character claim. Do not patch training with these particular evaluation incidents. No new paid judging is run here. Interpretability: yes pinned preference; partial practical moral reasoning.

## ML-debug form

| required row | finding |
|:--|:--|
| Full logs/config | Complete terminal/projection/evaluation reads above; full training read inherited explicitly from named auditor; same donor/config except data/cache/output paths |
| SHOULD/TODO | Identical frozen inputs and FP16 serving required;1540raw prompt/parameter records pass. Exploratory matched-effect hypothesis only partly supported |
| Null/scales | Instruct preference reference0, maths53/60, checks22/22; documents.244/56/22. No random-direction/null-control projection measured. Ordinal preference is not percent character |
| Init/dummy/validation | Initial donor control CE.3327 versus final.1958 on109teacher-target rows; uniform-token/null moral performance not inferred from this loss. Control-only lacks Musonius identity but is49/60maths and19/22checks, so not unchanged-usefulness |
| Schedule | Training auditor reconstructs warmup/LR/calibration; precise learning-onset LR and per-term gradient effects unknown |
| Full consumed sample | Raw training segments and first examples read; all2178production ID/label arrays verified; full fixed/selected reply reads recorded |
| Worst step | Training gradient16.04 atstep403 without sustained loss divergence; no per-module localization. Behavioural worst point full subtraction:60loops/159cuts and58GSM cuts |
| Surprise/second cause | Explained:32matches are not32finished answers; gate−2 can be a detector error; low CE is teacher imitation. Chasing now: causal EOS contribution and T0variation remain untested, not repaired by narrative |
| Missing trust evidence | Independent inference repeats, matched-EOS design, norm/random controls, held-out practical-reasoning validation, exact runtime/gradient parity |
| Competing diagnoses | H1–H5 cover data, method, measurement, implementation/harness and shortcuts; nonexclusive |
| Fresh reviewer | Fable scientific review: OK with notes; accepted clarifications recorded. Haiku ingested3PNGs but misread frontier count/origin and stopping faults, so its interpretation was rejected. A fresh native OpenAI/Astra recheck correctly explained the revised figures and found no blocking issue. Full reviews/disposition: review_status.md |
| Cheapest discriminator | Existing split completion/flags and raw reads completed first; no new GPU/API experiments bought. Future same-runtime parity/repeated decoding separates remaining implementation and variation explanations |
| Cost/time/memory | Training≈7249s, peak79.3GiB reserved; projection2086.9s,≈0.50GiB CUDA; entirelease7.781h. Cached analysis/reports use localCPU. Warm-cache setup/reuse shortens a later confirmation |

Three ways “projection wins” could be false: character effects are not equivalent (interval/matched assumptions); maths gains reflect stopping/ambiguous extraction rather than reasoning; a one-panel selected winner need not repeat. All three remain explicit. This does not establish failure of projection as a method. Likewise this particular EOS-asymmetric, maths-heavy control can fail while a different generic-control design works.

## Decision and next sequence

1. Resolve condition: execution/delivery is met by eight retained cells and three verified artifacts plus teardown. “Same character with less capability loss” is partial/inconclusive: a promising near-effect completion point, not demonstrated equivalence or a general winner. Independent scientific review and revised-image recheck are complete with notes; unresolved causal/statistical limits remain explicit.
2. Prediction check: full-matrix generation/persistence supported; control-only no-target-identity supported but unchanged-usefulness contradicted; matched-effect practical benefit partly supported for projection and not established for subtraction; isolated instruction-following mechanism unresolved.
3. Earliest unsupported link: Base→Instruct dominant singular subspaces, or a generic-teacher adapter, are assumed to isolate instruction-following. Geometry/CE do not establish that link. Behavioural controls at matched effect plus norm/EOS controls would support it.
4. Validity: credible narrow positive completion signal and credible full-dose failure, inconclusive broad character/capability improvement. Defining invalid as wrong cells/artifacts/protocol or projection implementation, rough P(invalid)≈10%; this excludes the known reported limitations, not a probability that the method generally works.
5. Highest-information clues: all four recovered maths matches were cutoffs; EOS supervision differs; higher projected dose adds loops without bracketing D. These limit the claim more than the raw preference ranking.
6. Missing evidence, ordered: inference repeatability; independently held-out practical reasoning/formatting; matched-EOS and norm controls; exact runtime gradient/dependency reconstruction.
7. Code issues: frozen role-header false positive reproduced; do not rewrite primary results. A future generic detector validation should cover alternating analysis headings versus actual dialogue, not a case-specific patch. Core projection/layout checks currently pass. Wrong validation environments were diagnosed and fixed by using existing environments, without changing training dependencies.
8. Reinterpretation: completed/extracted maths differ; token matching is not exposure matching; identity and virtue prose are not demonstrated character; an observed finite frontier is not statistical dominance; neither a successful adapter save nor lower teacher loss resolves behavioural quality.
9. What changes the verdict: replicated same-budget gains with similar practical character and no extra failures would strengthen projection; loss of the gain across repeats or a norm-only control matching it would weaken the geometric mechanism claim. EOS-matched subtraction recovering stopping would rehabilitate that design, not retroactively fix this run.
10. Sequence now: commit the final evidence/journal, retain the independent-review notes and leave the lease closed. Recommendation for a newly approved experiment is confirmation of rank64×1 against the within-lease plain½ reference before another broad sweep. Match actual EOS/data exposure before claiming an instruction-following-specific subtraction mechanism. No new paid run, lease, judge protocol, decoding or training change is authorized by this audit.
