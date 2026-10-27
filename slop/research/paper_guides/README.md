# Paper guides: what matters for our recipe

Audit date: 2026-10-27. Read this before borrowing a training stage or interpreting a gain.

**Bottom line:** keep the locked Base-trained LoRA graft. First check what tokens actually earned loss, what decisions changed, and what capability was lost. None of these papers establishes our exact document-adapters → dependent chat-adapter → Instruct graft stack.

**Evidence rules.** Paper results below are **author claims**, not replications. Local code observations were checked in this checkout. Risks and cheap checks are **our inferences**. Probability words are estimates, not measured frequencies. Paper line numbers refer to `docs/papers/`; project paths start at the repository root. Guide links are relative to this directory. I independently checked the quoted paper passages, rather than treating the guides as primary evidence. Missing image/table content remains unverified.

## Index

The engineering takeaway is deliberately narrower than the paper's headline. `V/` in the code column means `docs/vendor/`. Pins and availability searches are in [VENDOR.md](VENDOR.md); generation code is not necessarily a complete student-training release.

| Paper | One-line engineering takeaway | Guide path | Code path |
|:--|:--|:--|:--|
| Maiya et al., *Open Character Training* (2025) | Constitution distillation and introspection are Instruct-training precedents, not graft evidence (§2.1: “instruction-tuned releases”). | [2025_maiya_open-character-training.md](2025_maiya_open-character-training.md) | `V/open_character_training/`; nested OpenRLHF dependency needs its own pin |
| Anthropic / Kutasov et al., *Teaching Claude Why* (2026) | Preserve constitutional response revision; its step-6 ablation matters more than merely keeping the right action (paper:144). | [2026_anthropic_teaching-claude-why.md](2026_anthropic_teaching-claude-why.md) | No official release found; `V/lasr_teaching_claude_why/` is a **third-party replication** |
| Cho et al., *Constitutional Midtraining* (2026) | Prioritize substantive constitutional content over this particular curriculum/reasoning-block manipulation (§4); count replay separately. | [2026_cho_constitutional-midtraining.md](2026_cho_constitutional-midtraining.md) | `V/constitutional_midtraining/` — generation/evaluation, not the complete MT/SFT/RL trainer |
| Korbak et al., *How far does alignment midtraining generalize?* (2026) | Near-training QA gains do not establish distant agentic transfer (paper:113,163). | [2026_korbak_midtraining-generalization.md](2026_korbak_midtraining-generalization.md) | No public paper-specific code found; internal OpenAI pipeline |
| Li et al., *Model Spec Midtraining* (2026) | Documents plus aligned demonstrations have evidence; complex Qwen experiments train on **post-trained** models, not Base-to-Instruct grafts (§4). | [2026_li_model-spec-midtraining.md](2026_li_model-spec-midtraining.md) | `V/msm/` — data/evaluation; no released student trainer at the inspected pin |
| Lowet & Kurzeja, *Constitutional adapters* (2026) | Tiny Base-trained differences can transfer, but retained maths can coexist with coding/tool damage (§3.4). | [2026_lowet_constitutional-adapters.md](2026_lowet_constitutional-adapters.md) | [Pinned upstream code](https://github.com/safety-research/constitutional-adapters/tree/bff6268ac702e7fbcf34022704ead71531a385f5) |
| McDougall et al., *SDF for instilling positive traits* (2026) | Audit patterns across the corpus: individually reasonable rows can teach an unconditional habit (paper:83). | [2026_mcdougall_sdf-positive-traits.md](2026_mcdougall_sdf-positive-traits.md) | No paper-specific implementation found; related SDF repositories are not this experiment |
| Minder et al., *Synthetic Persona Pretraining* (2026) | Matching document and chat persona content matters more than simply matching an assistant marker (§3.4.1). | [2026_minder_synthetic-persona-pretraining.md](2026_minder_synthetic-persona-pretraining.md) | `V/spp_data/`, `V/spp_training/`, `V/spp_evals/` |
| Nutter et al., *Grafting model beliefs / Praxis* (2026) | Transfer effective Base-trained updates; compare expression, capability and unrelated-belief/preference retention separately (§2.1–2.2). | [2026_nutter_grafting-beliefs.md](2026_nutter_grafting-beliefs.md) | `V/praxis_grafting/` |
| O'Brien et al., *Inoculation Midtraining* (2026) | A learned context boundary can hide rather than remove a behavior; test nearby cues (§4.4, B.7). | [2026_obrien_inoculation-midtraining.md](2026_obrien_inoculation-midtraining.md) | No accessible paper-specific implementation found; official HF collection contains datasets |
| Baines et al. (including Tan), *Stress-Testing Alignment Midtraining* (2026) | Chat endorsement can stay constant while a small conflicting EFT mixture reverses decisions (§3.1). | [2026_tan_stress-testing-alignment-midtraining.md](2026_tan_stress-testing-alignment-midtraining.md) | [Pinned upstream code](https://github.com/ArcadiaImpact/science-of-midtraining/tree/63374927b85b2e83bdb73c570db4242f16569718) |
| Tice et al., *Alignment Pretraining* (2026) | Separate scenario-seeded Articles results from source-held-out Textbook results (§2.3). | [2026_tice_alignment-pretraining.md](2026_tice_alignment-pretraining.md) | `V/alignment_pretraining/` — supporting code, not a verified complete training release |
| Young et al., *Why study pre-RL checkpoints?* (2026) | A graft onto finished Instruct does not test how a changed initialization affects later on-policy RL (paper:22,40). | [2026_young_pre-rl-checkpoints.md](2026_young_pre-rl-checkpoints.md) | No paper-specific implementation; conceptual agenda, not a new training experiment |

**Inventory qualification:** the guides/VENDOR describe Lowet and Baines as not vendored because of repository size. At inspection, `docs/vendor/{constitutional_adapters,science_of_midtraining}/` contained Git metadata but no checked-out source files. The table therefore links the pinned upstream source rather than promising runnable local trees. Other work may change that state. VENDOR also covers supporting works such as *Deep Ignorance*; those do not have separate guides in this bundle.

## Gotchas we missed or are exposed to

Ranked by estimated **probability of affecting our interpretation/results × impact**, not by novelty. “Already guarded” does not undo historical confounds. No new paid run is authorized here.

### 1. Content approval can still produce a target that never learns to stop

**Very likely; high impact. Historical failure, current export exposure.**

> “The loss is computed only on the assistant completion, including the assistant header and closing \<\|im_end\|\> token.”
>
> — `docs/papers/2026_minder_synthetic-persona-pretraining.md:860`, Appendix C.3; [Minder guide](2026_minder_synthetic-persona-pretraining.md), §3. The guide checks that the executable header mask differs; the closing token is the relevant agreement here.

**Our affected code:** `src/constitutional_grafting/data/chat.py:85–89` replaces a labelled target with raw model text; `src/constitutional_grafting/data/files.py:57–66` checks labels/nonempty text, not EOS. The rewrite prompt asks for “only the reply text” (`configs/data/prompts/rewrite_response.md:21`). Historical replacement has the same shape (`src/constitutional_grafting/data/historical.py:65–70`). Thus “ready” for content is not necessarily ready for training. An offline fixture through the actual model-stage exporter and validator confirmed this gap. The training gate at `scripts/train/14_run10_chat_box.sh:90` catches it; this is **not** a claim that today's guarded launcher silently trains those rows.

**Cheap check:** run `scripts/train/check_loss_mask.py` on the exact export selected for training, without `ALLOW_MISSING_EOS`. Inspect tokenized long examples too: ensure EOS survives length handling, only intended assistant text earns loss, and the empty think block remains unlabelled. Keep old releases unchanged. Old non-stopping adapters confound claims about response rewriting, control subtraction and projection.

### 2. Good explanations, names and endorsements can hide unchanged or worse decisions

**Likely; high impact on claims of constitutional character.**

> “MSM + AFT and AFT-only achieve comparable near-ceiling performance on in-distribution open-ended QA, yet diverge significantly on OOD AM evals.”
>
> — `docs/papers/2026_li_model-spec-midtraining.md:324`, §4.1; [Li guide](2026_li_model-spec-midtraining.md), §4.

> “the two Charter-midtrained models discuss and endorse the Charter at roughly equal rates”
>
> — `docs/papers/2026_tan_stress-testing-alignment-midtraining.md:245`, §3.1; [Baines/Tan guide](2026_tan_stress-testing-alignment-midtraining.md), §3. The same experiment replaces 164/8,192 EFT rows (paper:241); this is not a universal 2% threshold.

**Our affected files:** `scripts/eval/33_subset_cells.py:119–126` generates chat panels and maths; the demos in `README.md:297–380` are selected examples, not action-transfer prevalence. Our process judge and full reply-reading rules already help. Neither identity recall nor a higher mean preference establishes consistent conduct in a new interface.

**Cheap check:** blind-read saved paired answers, recording implemented decision, supporting reason, fact invention and viewpoint/pressure consistency separately. Label teacher/near-training examples explicitly. Korbak's agentic average was “not significantly different” across its three runs (`docs/papers/2026_korbak_midtraining-generalization.md:163`; [guide](2026_korbak_midtraining-generalization.md), §3): evidence against assuming distant transfer, **not** a test of our graft. Use existing held-out tool traces if available; a new sandbox evaluation needs protocol/budget approval.

### 3. Retained GSM8K is not retained ordinary usefulness

**Likely; high impact.**

> “On MMLU and GSM8K, there was little to no capability hit for any intervention. On BCB and BFCL, our lightweight objects led to a reduction in pass rate”
>
> — `docs/papers/2026_lowet_constitutional-adapters.md:249`, §3.4; [Lowet guide](2026_lowet_constitutional-adapters.md), §3.

> “a model which can't use tools might invent a fake reason why not”
>
> — `docs/papers/2026_mcdougall_sdf-positive-traits.md:114`; [McDougall guide](2026_mcdougall_sdf-positive-traits.md), §4.

**Our affected files:** `scripts/eval/33_subset_cells.py:126` runs only 60 GSM8K questions as its explicit capability benchmark; the small-task result in `docs/results/20261027_control_projection_heal.md:7–18` is useful but narrow. These sources do not establish broad coding/tool retention. Lowet's GSM8K uses thinking on (paper:614), so its numbers are not directly comparable to ours.

**Cheap check:** inspect existing benign-help/code/tool replies for valid output and successful execution, separately from moral refusal. Split finished-correct maths from token-cap failures and final-number matches in unfinished answers. Do not call restored completion better mathematical reasoning. Add fresh capability calls only if approved.

### 4. A smaller intervention can masquerade as a better method

**Likely; high impact on spectral/projection/replay comparisons.**

> “stronger expression is often correlated with greater damage; future work should compare methods at matched expression.”
>
> — `docs/papers/2026_nutter_grafting-beliefs.md:327`, §7; [Nutter guide](2026_nutter_grafting-beliefs.md), §§4.3, 6.

**Our affected code:** `scripts/train/spectral_math.py:15–35` penalizes estimated top singular values; `scripts/train/16_project_chat_adapter.py:17–21` removes subspace components; `scripts/eval/33_subset_cells.py:49–50` accepts numeric doses without effect matching. Either edit can simply weaken the change. The paper's chat peak at 2.5–3 (paper:307) is an EM result, not a good-character dose prescription.

**Cheap check:** use saved coherent dose curves to compare the same document-stage behavioral change or final-chat character effect against separate maths/help/stopping losses. Include lower-dose plain, not only plain ×1. State local interpolation assumptions, retain coherent bad points, and do not extrapolate across collapse. This implements the existing `AGENTS.md:65–69` rule, not a new selection method.

### 5. Our stacked graft is an extension; a graft-time removal is not retraining without that ingredient

**Likely; high impact on attribution.**

> “Future work ought to consider whether grafting generalizes to combining more than one SDF adapter”
>
> — `docs/papers/2026_nutter_grafting-beliefs.md:327`, §7; [Nutter guide](2026_nutter_grafting-beliefs.md), §§4.3, 5.

**Our affected code:** `scripts/train/14_run10_chat_box.sh:52–59,83–91` trains chat on a selected Base+documents merge; `scripts/eval/33_subset_cells.py:49–51,93–100` can later serve arbitrary adapter coalitions. Removing or changing a document dose moves that chat adapter off its training base. It can also miss document effects already learned into the chat adapter. This dependence is an inference from the actual training order, not something Praxis measured for our stack.

**Cheap check:** join each saved cell to its resolved chat-training donor and doses; label on-/off-training-base comparisons in reports. Check executed configs, not template comments: `configs/train/qwen3/sft.yml:10,13–18,60` alone neither pins Base nor includes the spectral plugin and says three epochs; the launcher overrides all three at lines 86–91. A clean training-time document ablation would retrain chat and requires approval, not another arithmetic removal.

### 6. “Control” names hide different experiments

**Plausible recurrence; high impact. Already encountered, not an untried cure.**

> “The anchored graft subtracts the replay-only control update, at the cost of one extra token-matched training run to build the anchor.”
>
> — `docs/papers/2026_nutter_grafting-beliefs.md:2673`, Appendix C.1.2; [Nutter guide](2026_nutter_grafting-beliefs.md), §4.1.

**Our affected files:** `scripts/train/15_control_replies.py:1–5,39–44` instead generates Instruct's own answers for a Base-trained chat control. That is not the replay anchor, despite its Praxis citation. `scripts/data/89_run11_data.py:7–15,77–107` separately implements document replay mixes and a shared replay control, plus a different No Robots chat control. Those must not be pooled under one explanation. Lowet's register-matched control is a third design, not generic web replay (paper:498; [guide](2026_lowet_constitutional-adapters.md), §3).

**Cheap check:** draw the actual equations and record control data, training base, exposure and EOS coverage for each saved comparison. Read the existing failures (`docs/results/20261027_control_projection_heal.md:13–18`) before proposing another subtraction. Verify sums of effective updates, not sums/differences of raw A and B factors; our `scripts/train/02_merge.py:23–38` already scales B and merges updates sequentially. Nonlinear training means even matched replay subtraction is not exact causal isolation of one corpus.

### 7. Full row review does not detect every corpus-level habit

**Likely; moderate-to-high impact.**

> “Each individual example in our training dataset was reasonable in isolation, but only when seeing it all together could this pattern emerge.”
>
> — `docs/papers/2026_mcdougall_sdf-positive-traits.md:83`; [McDougall guide](2026_mcdougall_sdf-positive-traits.md), §4. The reported learned habit was asking for clarification even on simple questions.

**Our affected code:** `src/constitutional_grafting/data/chat.py:179–223` judges, repairs and fully reads individual examples, then samples a mixture; `src/constitutional_grafting/data/documents.py:126–146` likewise checks candidates. These functions do not themselves measure rhetorical/behavioral prevalence across the final corpus. Source-grounded text and careful individual approval reduce risk but do not remove it.

**Cheap check:** on existing accepted text, count repeated openings, clarification/refusal/alternative structures, lengths and domain concentrations; read complete dominant clusters and compare with saved model replies. Map purported moral principles back to the constitution. McDougall's later removal of emotional openings **did not** reduce delusion confirmation (paper:97); do not turn pattern detection into an empathy ban or another categorical acceptance rule.

### 8. Corpus size, repeated exposure and retained tokens are different quantities

**Plausible; moderate-to-high impact. Actual truncation prevalence unmeasured here.**

> “the main paper’s token figures refer to constitutional content specifically, not total tokens processed.”
>
> — `docs/papers/2026_cho_constitutional-midtraining.md:512`, Appendix D.1; [Cho guide](2026_cho_constitutional-midtraining.md), §3.2.

**Our affected files:** `docs/plans/20261021_character_graft_recipe.md:64–71` compresses paper counts; `configs/train/qwen3/graft.yml:38–39,61` uses 2,048-token document sequences and two epochs; `scripts/eval/47_base_heldout_loss.py:20,26–28` measures only the first 100 documents per file and truncates each to 1,024 tokens. Its loss is a prefix diagnostic, not full-document comprehension. Actual Axolotl handling of over-length training rows needs checking; the YAML alone does not prove truncation rather than dropping/splitting.

**Cheap check:** reconcile tokenizer-named unique tokens, scenario counts, repeats, replay, retained/loss-bearing tokens and executed steps. Inspect cached prepared rows around the length boundary and whether the decisive reason/action remains. Check held-out prefix/source coverage. No paper here supplies a minimum token budget for our MoE graft; more epochs are not more unique situations.

### 9. “Experts trained” can mean a nonzero wrapper, not every expert

**Less likely because guarded; high impact if present.**

> “the expert MLPs were necessary to install belief in the target entities, not just to express the described quirk.”
>
> — `docs/papers/2026_nutter_grafting-beliefs.md:2549`, Appendix B.7; [Nutter guide](2026_nutter_grafting-beliefs.md), §4.2. This is the authors' DeepSeek observation, not proof that our rank is too small.

**Our affected code:** `configs/train/qwen3/graft.yml:46–55` correctly targets routed expert parameters as well as attention/shared experts. But `scripts/train/41_expert_adapter_check.py:22–30` tests each saved expert-wrapper B tensor's aggregate norm; `scripts/train/02_merge.py:21,54–69` probes only selected late-layer matrices. Neither establishes nonzero updates for every individual expert in every layer.

**Cheap check:** inspect saved per-expert effective-update norms, shapes, scales and fused gate/up mapping; use the existing `tests/regression/test_moe_expert_merge.py` plus zero/double/signed-sum merge fixtures. Confirm expected coverage before considering higher rank. Keep recipient/tokenizer/dtype fixed; our donor merges default to BF16 but evaluation overrides to FP16 (`02_merge.py:48–49`; `33_subset_cells.py:53–56`).

### Unverified — not used as established explanations

- **Full FT would outperform LoRA.** No checked core paper supplies that controlled comparison. Li explicitly uses LoRA (paper:604); Praxis permits adapters or full-rank updates (§2.1). Cho's full-model run is not a LoRA ablation.
- **We need 300M–500M tokens, 50% replay, 3× chat dose, or 2,500 identity rows.** These are settings from different experiments, not transferable thresholds. The plan already records the identity-count mistake (`docs/plans/20261021_character_graft_recipe.md:86`).
- **Dropping a marked reasoning block proves reasons do not matter.** Cho explicitly warns that noDR may retain value explanations (paper:328). Its manipulation does not isolate all reasoning.
- **Projection protects post-training skills because those skills occupy the largest singular directions.** No such measurement or guarantee was found in Praxis. See below.
- **Guide-reported upstream code defects explain published results.** Maiya's interaction-target bug, Nutter's callback/config mismatches and Li's fail-open parsing are source-level reproduction concerns in the guides. They cannot be verified as causes of historical training from the paper text, and are not ranked as our result explanations here. Do not copy the affected paths without a separate code audit.
- **Missing PDF/image-only tables, prompts, exact private trainers or teacher revisions.** The guide bundle notes extraction/release gaps. I did not reconstruct those contents, infer full FT from the word “finetune”, or treat a third-party replication as official Anthropic code.

## Recipe decisions that disagree with the literature

Here **core papers** means the four sources used in our plan's evidence chain: Nutter/Praxis, Li/MSM, Cho/CMT and Anthropic/Teaching Claude Why. Other guides provide counterexamples and limitations. “Different from every core recipe” is not the same as “contradicted by every core paper”. There is no unanimous published recipe that our locked choices simply reject.

| Locked choice / difference | What the core papers actually establish | Deliberate or unexamined? |
|:--|:--|:--|
| Separate document adapters, then chat on their Base merge, then graft both onto finished Instruct | Praxis separately demonstrates document grafts and chat EM grafts (§2.1, §5.2); combining SDF adapters is future work (§7). Li's complex experiment is MSM→AFT on production Qwen (paper:296,583). Cho trains Base→MT→SFT→GSM8K RL (§3.2). Anthropic's story comparison is Base→SDF→generic chat SFT (paper:103), with later RL comparisons separate. None tests our exact stack. | **Deliberate extension**, not an unnoticed omission: user decision and explicit “Gap” in `docs/plans/20261021_character_graft_recipe.md:9–45`; locked in `AGENTS.md:26`. Path-dependence/attribution remains unestablished, not solved by naming the stages. |
| Spectral regularization in every donor stage, including chats | No such penalty is disclosed in these core recipes. Li lists AdamW/LoRA settings (paper:604); Praxis's installation recipe lists ordinary LoRA (Appendix B.1). Anthropic does not disclose enough optimizer detail to prove that no undisclosed regularizer existed. | **Deliberate project addition**, not a literature-backed requirement: `AGENTS.md:22`; plan:23 gives the earlier document result, user “all things use a spectral norm” decision and chat calibration hypothesis. Better direction versus simple shrinkage still needs matched-effect evidence. |
| Authentic Stoic/other source-text adapters alongside constitutional documents | The relevant core character/belief interventions train generated, target-related documents; generic replay is a different ingredient. Li's human-identity rewrite keeps spec-derived content (Appendix H), not arbitrary historical books. | **Deliberate comparison/extension**: `AGENTS.md:5,21,27`; plan:84–85,97–106. Treating source-text success as proof our constitution was taught would disagree with our own lock. Whether it helps through later chat is still an empirical question. |

**Important non-disagreements:** LoRA is explicitly supported by Li B.4 and Praxis §2.1; it does **not** differ from all core papers. Base-only character training differs from Li's complex Qwen route and Maiya's Instruct route, but agrees with Praxis's graft donors and Lowet's Base fitting. No mandatory new RL differs from Cho's sequential experiment and Anthropic's RL-persistence test, but agrees with Praxis's install-only/constitutional graft tests and Lowet. Optional healing is our capability-repair experiment, not a stage every core paper requires. Thinking off agrees with Anthropic's difficult-advice data (paper:150); it is not an instruction to discard real constitutional explanations. None of these observations authorizes a recipe change.

## Side idea: orthogonalise Instruct−Base from the graft

Consolidated from the [Nutter guide's side idea](2026_nutter_grafting-beliefs.md#side-idea-orthogonalise-instructbase), checked against our implementation.

### Motivation, not a paper algorithm

> “this knowledge is largely orthogonal to what post-training changes.”
>
> — `docs/papers/2026_nutter_grafting-beliefs.md:325`, conclusion.

That is an **author interpretation** of transfer, not an SVD measurement or preservation theorem. Praxis's graft definition adds the learned update without this edit. Our projection is a separate hypothesis. It already exists in `scripts/train/16_project_chat_adapter.py` and was tested in run 14; it is not a newly missing Praxis step.

### Math: three different meanings of “orthogonal”

For one corresponding weight matrix, let

```text
T = W_Instruct − W_Base          # m×n post-training change
D = s B A                       # graft's effective update; s = LoRA alpha/r here
<X,Y> = tr(XᵀY)                 # Frobenius inner product
T = U Σ Vᵀ                      # SVD; U_k,V_k are the leading k vectors
```

Use original matching matrices, separately for each routed expert. Three edits must not be confused:

1. **Remove only the full task-vector direction:** `D_scalar = D − (<D,T>/||T||²_F)T`, with a zero-T guard. This gives `<D_scalar,T>=0`, removes parallel **and anti-parallel** overlap, and generally loses the original low-rank representation.
2. **Remove k paired singular atoms:** `D_atoms = D − Σ_i≤k (u_iᵀ D v_i) u_i v_iᵀ`. This removes k orthonormal directions in matrix space, not the whole left/right subspaces.
3. **Our two-sided projection:** `P_k(D) = (I−U_kU_kᵀ) D (I−V_kV_kᵀ)`. Implement it with `B' = B−U_k(U_kᵀB)` and `A' = A−(AV_k)V_kᵀ`; keep s and LoRA rank unchanged. It enforces `U_kᵀP_k(D)=0` and `P_k(D)V_k=0` and removes the cross-block components too. The removed matrix-space dimension is `k(m+n−k)`, not k.

Top-k projection is orthogonal to **T_k**, not necessarily full T. At full k=min(m,n), the two-sided edit erases every D. Example: `T=diag(3,2)`, `D=[[1,2],[3,4]]`, k=1. Atom removal leaves `[[0,2],[3,4]]`; two-sided removal leaves `[[0,0],[0,4]]`, whose inner product with full T is still 8. Thus “remove 64 directions” needs this precise definition.

### Pseudocode matching the existing operation

```python
# Explanation only; not a new runnable training stage.
for parameter, expert in original_matrix_and_expert_pairs(adapter):
    T = instruct[parameter][expert].float() - base[parameter][expert].float()
    U, S, Vh = svd(T)                         # same pinned checkpoint pair
    U_k, V_k = U[:, :k], Vh[:k, :].T
    A, B, scale = unpack_lora(adapter, parameter, expert)
    A_new = A.float() - (A.float() @ V_k) @ V_k.T
    B_new = B.float() - U_k @ (U_k.T @ B.float())
    save_factors(A_new, B_new, scale=scale)   # preserve rank/alpha and expert layout
# Serve θ_I + unchanged Δ_docs + b·P_k(Δsft_rewr|docs).
```

The script subtracts in FP32 and performs full SVD then truncation (`16_project_chat_adapter.py:94–112`). Existing tests cover matrix equality, idempotence, null subspaces, energy identity, expert packing and key mapping (`tests/regression/test_chat_projection.py:14–61`). Those tests were read, not run here: this CPU environment lacks torch. The dependency-free 2×2 example above was checked.

### Failure modes

- **T is not a skill dictionary.** It mixes instruction following, refusals, style, maths, stopping and other changes. Large singular values need not identify the capability we want to retain. For capability loss L, the first-order change is `<∇L(W_I),D>`, not `<T,D>`; orthogonality gives no loss guarantee, especially at large doses.
- **It may remove the character.** Character expression can use the same subspaces. A weaker projected model at dose 1 is not automatically a better matched-effect model.
- **It shrinks the update.** Compare lower-dose plain and norm-shrunk plain. Do not automatically restore the old norm: that can amplify remaining damaging components.
- **The spectrum/mapping can mislead.** Flat spectra, unstable top-k boundaries, checkpoint precision, fused tensors, transposes and expert ordering all matter. Pin both weights; cast before subtraction; do not pool experts.
- **It changes a dependent training base if applied underneath chat.** Test the final chat update first with Δ_docs unchanged. Projecting documents under an existing chat adapter is a different, off-training-base intervention.
- **It may repair a stopping bug, not protect maths.** The old rewritten chats often lacked EOS. That is a known confound, not a proven account of the gain.

### Cheapest test, and what is already known

**Zero new model calls first:** reuse saved run-14 plain, k16 and k64 replies plus projection metadata. Confirm hashes, unchanged document doses, expert coverage and retained/removed energy. Read paired answers and separate completion from correctness conditional on completion. The maintained rebuild is `just run14-results`; it was **not run in this guide-only task**, because it writes other reports.

`docs/results/20261027_control_projection_heal.md:7–18` reports, with fixed documents and thinking off:

| Final chat update | Character preference vs Instruct | Finished-correct maths | Small tasks |
|:--|--:|--:|--:|
| Plain at b=½ | +0.75 | 53/60 | 18/22 |
| Two-sided k64 at b=1 | +0.73 | 57/60 | 21/22 |

The report gives paired character difference −0.02, 90% interval [−0.10,+0.07], and maths +4 [+1,+7]. All four extra maths matches replace token-cap failures. These are small, selected-variant, single-sample-per-model results; overlapping intervals do not prove character equivalence. This is a completion benefit worth checking, not a confirmed reasoning improvement or winner.

**Only after approval:** compare plain/lower-dose plain, norm-shrunk plain, k16/k64 at a predeclared small dose range, same recipient/documents/precision/thinking mode. A random same-size subspace control helps distinguish special geometry from generic removal. Select on development data, not final held-out questions. Most importantly, repeat on an EOS-correct retrained chat adapter when that retrain is approved. A persistent gain at matched character would support the geometry hypothesis; disappearance would favor a stopping-bug workaround. New SVDs require full checkpoints and real compute even without training.

## Missing links

At this audit, the following seven guided works had **no citation in either `README.md` or `AGENTS.md`** (checked titles, author names and identifiers). Existing citations already cover Nutter, Li, Tice, Cho, Anthropic and Maiya. Do not add those again. Proposed lines below are exact Markdown additions, **not edits performed**.

### Add to README.md, Appendix B, after “Prior work, and where we depart from it”

The first five are the most useful missing engineering evidence/caveats:

```markdown
- [How far does alignment midtraining generalize?](docs/papers/2026_korbak_midtraining-generalization.md) (Korbak et al. 2026): gains near the document distribution did not establish distant agentic gains after their reasoning post-training; this cautions against inferring broad transfer from our demos.
- [Stress-Testing Alignment Midtraining](docs/papers/2026_tan_stress-testing-alignment-midtraining.md) (Baines et al. 2026): small conflicting elicitation mixtures reversed decisions while chat endorsement stayed similar; we must check actions and the document/chat interaction, not recall alone.
- [Synthetic document finetuning for instilling positive traits](docs/papers/2026_mcdougall_sdf-positive-traits.md) (McDougall et al. 2026): individually good examples can teach unwanted corpus-wide habits, and broken tool use can look like moral refusal.
- [Constitutional adapters](docs/papers/2026_lowet_constitutional-adapters.md) (Lowet and Kurzeja 2026): tiny Base-trained constitutional-minus-control updates transfer to Instruct, but coding and tool damage can remain despite retained maths; their register control is not our Instruct-answer control.
- [Synthetic Persona Pretraining](docs/papers/2026_minder_synthetic-persona-pretraining.md) (Minder et al. 2026): matching the content of later chat training to the pretrained persona helped bind it to the assistant; their token-zero result does not validate our late LoRA graft.
```

These are supported by the independently checked passages used above: Korbak:163; Baines:190,241,245; McDougall:83,114; Lowet:249,498; Minder:219,249,358. Minder's risk-action score is not adopted as our character metric.

### Supporting limitations, if README includes context robustness / pre-RL motivation

These should be cited for those claims, not presented as extra recipe ingredients:

```markdown
- [Inoculation Midtraining with Learned Neologisms](docs/papers/2026_obrien_inoculation-midtraining.md) (O'Brien et al. 2026): a behavior can remain available behind a learned context boundary, so test nearby framing cues rather than only the default prompt.
- [Why study alignment interventions on pre-RL checkpoints?](docs/papers/2026_young_pre-rl-checkpoints.md) (Young et al. 2026): changing initialization may affect later on-policy learning, but this is partly speculative and is not tested by adding a graft after the maker's RL.
```

Verified against O'Brien:147,344,724 and Young:22,40,48. Young is an agenda post, not a missing empirical validation.

For discoverability, an optional exact AGENTS.md “Start here” line is:

```markdown
- Engineering caveats and verified paper/code comparisons: [paper-guide index](slop/research/paper_guides/README.md); these notes propose checks, not new training stages or spending approvals.
```

## Read coverage and validation

- Read all **13 paper guides**, `BRIEF.md` and `VENDOR.md` in full; then project `AGENTS.md`, `README.md`, the approved recipe plan and `jargon.md`. Read constitution §§1–5 in full before writing this guide. No training examples, prompts, rubrics or constitution text were edited.
- Independently checked the paper passages cited here, including setup/method qualifications and the surrounding result/limitation text where used. This is **targeted primary-source verification**, not a new full read of every paper/PDF. Image-only material and unavailable private trainers were not verified. No claimed result was independently reproduced.
- Read both Qwen train YAMLs and `scripts/train/{01_prepare.py,02_merge.py,12_run10_box.sh,14_run10_chat_box.sh,16_project_chat_adapter.py,41_expert_adapter_check.py,spectral_plugin.py,spectral_math.py,check_loss_mask.py}`; current `data/{chat,documents,files}.py`; subset/held-out-loss evaluation drivers; cited historical/replay/control seams and projection tests. These are maintained run-10-style paths plus overrides, not a whole-history audit.
- Ran `just --list`; the existing loss-mask regression passed. An offline fixture through the actual rewrite exporter and row validator confirmed that a plain EOS-free replacement passes row validation but is rejected by the training preflight. No API call was made. The 2×2 projection distinctions and guide link/citation/whitespace checks passed.
- Only this README was written by this task. No commit or staging was performed. Other working-tree changes, including concurrent vendor/index work, were left alone. No training, rental, model serving, downloads or paid evaluation ran. Proposed broader checks and new experiments remain subject to approval.

-- PI/gpt-6.1-sol, 2026-10-27
