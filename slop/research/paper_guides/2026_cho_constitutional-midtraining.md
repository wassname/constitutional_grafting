# Engineering guide: Constitutional Midtraining — Content Presence Drives Alignment Gains

## 1. Header and source map

**Observed — bibliographic record.** Desiree Cho, Cameron Tice, Bernie Hogan, Hunar Batra, Puria Radmard, Jun Zhao and Nigel Shadbolt. *Constitutional Midtraining: Content Presence Drives Alignment Gains*, arXiv:2607.26654v3, 18 August 2026. [Paper](https://arxiv.org/html/2607.26654v3). Local text: `docs/papers/2026_cho_constitutional-midtraining.md`.

**Observed — code.** [desBugger/constitutional-mt](https://github.com/desBugger/constitutional-mt), vendored at `docs/vendor/constitutional_midtraining`, commit `8585a11ff80829c0c312879b6e9e92c277cf0f6f`. This matches `slop/research/paper_guides/VENDOR.md`. Below, **P** means the local paper; **C** means this vendor directory. File line numbers refer to this checkout, not to rendered web pages.

**Observed — additional author artifacts read on 2026-10-27.** These supply details absent from the paper and vendor training code. No weights or dataset payloads were downloaded.

| Short name | Immutable author artifact |
|---|---|
| MT card / MT config | `geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr` at `178555d2c21a7eb6db9efa137a799adf5fddfe34`: [README.md](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr/raw/178555d2c21a7eb6db9efa137a799adf5fddfe34/README.md), [megatron_run_config.yaml](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr/raw/178555d2c21a7eb6db9efa137a799adf5fddfe34/megatron_run_config.yaml) |
| SFT card | Same model stem plus `-200k-sft`, at `1283cefd1f7819fbda9b0e9b7554e19d647597a5`: [README.md](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr-200k-sft/raw/1283cefd1f7819fbda9b0e9b7554e19d647597a5/README.md) |
| BFT card / adapter config | Same model stem plus `-200k-sft-gsm8k-lora`, at `afdf2e7eb9538389e7fd0f0c45391bdb89872229`: [README.md](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr-200k-sft-gsm8k-lora/raw/afdf2e7eb9538389e7fd0f0c45391bdb89872229/README.md), [adapter_config.json](https://huggingface.co/geodesic-research/nemotron-super-120b-cc-mt-curriculum-dr-200k-sft-gsm8k-lora/raw/afdf2e7eb9538389e7fd0f0c45391bdb89872229/adapter_config.json) |

**Labels throughout:** **Observed** means read in the paper, code or released metadata, not independently reproduced training. **Author claim** means the authors' interpretation or generalization. **Inferred** means this guide's deduction or recommendation. Estimates are identified separately from measurements.

## 2. What they did, in 5 lines

1. **Observed.** Extract 40 values from Anthropic's 2026 Constitution; retain 38 in four clusters for training (P §3.1, Appendix A).
2. **Observed.** Generate one pool of AI situation–reasoning–action documents with Sonnet 4.6; derive a second pool by removing `<reasoning>…</reasoning>` (P §3.3).
3. **Observed.** Continue training a 120B/12B-active Nemotron Base with constitutional text plus equal-token replay; cross curriculum/uniform sampling with reasoning/no-reasoning (P §3.2, D).
4. **Observed.** Apply shared instruction SFT, then GSM8K GRPO; evaluate each condition after each stage, against a replay-only control (P §§3.2–3.4; C README, “Overview”).
5. **Author claim.** Content presence has a larger and more durable effect than either tested structural manipulation; survival depends on the evaluation, not on one global retention score (P §§4–5).

Key source wording:

> “Within CMT, curriculum ordering and deliberative reasoning produce only small, non-persistent effects.” — P §4.

## 3. Exact recipe

### 3.1 Training and evaluation table

**Observed — source anchors for the table.**

> “Constitutional content is evenly mixed with an equal-token-budget replay of high-quality pretraining data the model had seen in prior training, for stability.” — P §3.2, Midtraining.

> “Global batch size 128 (micro batch size 1), sequence length 8192” and “Learning rate follows a cosine decay to zero from a peak of” 1 × 10⁻⁶, with “linear warmup over the first 10% of training”. — P D.1; mathematical notation rendered as text here.

> `peft: null` — MT config:671.

> “246 iterations, GBS 128, seq 8192, lr 5e-6 cosine w/ 10% warmup, tokenizer `geodesic-research/nemotron-instruct-tokenizer`, answer-only loss.” — SFT card:17.

| Recipe row | Exact setting and evidence |
|---|---|
| Starting checkpoint | **Observed.** Paper: Nemotron-3-Super-120B-A12B-Base, hybrid Mamba-2/attention MoE, 120B total / 12B active, about 25T pretraining tokens (P §3.2). MT card:5 identifies public parent `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-Base-BF16`; actual run starts from `NVIDIA-Nemotron-3-Super-120B-A12B-Base-Chat-Init-BF16` (card:15–16; config:36). This is Base with special-token embedding initialization, not ordinary Instruct. |
| Values and data type | **Observed.** 38 trained values, clustered as core ethics (k1), identity/character/wellbeing (k2), operational safety/relational conduct (k3), epistemic integrity/honesty (k4). Natural document excerpts about AI behavior, including dialogue; only `content` is trained (P §§3.1, 3.3, E.1). |
| Generator and sampling | **Observed.** `claude-sonnet-4-6`, Anthropic Batch API; temperature 1.0, `max_tokens=2048` (C `data_generation/config.py:4`; `submit_batch.py:12–24`). Prompt requests 950 tokens, range 900–1100, about 40% explicit reasoning (C `build_prompts.py:8–41`). Actual mean DR length is 1158–1173 cl100k tokens, not the requested range (P E.2, Table 6). |
| Unique corpus tokens | **Observed.** 220,868 underlying scenarios; DR 257.6M tokens, stripped noDR 136.8M. The often-quoted 394M is their sum, not 394M independent scenario tokens in one training condition (P §3.3; C `hf_README.md`, source-file table). Accounting tokenizer: `tiktoken` `cl100k_base` (P E.1). |
| Training token budgets | **Observed.** DR: 500M constitutional tokens per condition. Curriculum-noDR: about 264M; Uniform-noDR: about 266M. Equal replay is additional. Actual steps imply about 1.014B total tokens for Curriculum-DR, 538M for Curriculum-noDR and 541M for Uniform-noDR (P D.1; arithmetic below). |
| Replay and control | **Observed.** 1:1 constitutional/replay tokens. MT card:17 names replay `geodesic-research/Nemotron-Pretraining-Specialized`; MT config:59–72 records 0.5/0.5 weights. Control is replay-only, not untouched Base (C README “Overview”; `evals/configs/run.json:13–15`). Exact control replay payload/order is not stated in the inspected local training implementation, which is not released here. |
| Curriculum / uniform | **Observed.** Four equal-budget phases: k1; k1+k2; k1+k2+k3; all four. Equal token allocation to present clusters within each phase. Uniform-DR allocates 125M constitutional tokens per cluster throughout. Curriculum changes total cluster exposure as well as order (P D.2–D.3). |
| Full FT versus LoRA | **Observed.** Constitutional MT is configured as non-PEFT/full-model continued training: `peft: null` (MT config:671). Exact runtime freeze inventory is not stated. MT LoRA rank/alpha/targets: not applicable. SFT adaptation method is not stated in the inspected SFT card/paper. BFT is LoRA r8, alpha 8, dropout 0, on attention/Mamba input-output projections and shared-expert FC1/FC2 glob targets, not routed-expert targets (BFT adapter config:5–15). No full-FT/LoRA superiority comparison. |
| Optimizer / precision | **Observed.** MT AdamW, weight decay 0.1, betas 0.9/0.95, epsilon 1e-8, clip norm 1, bf16 with fp32 optimizer states (P D.1). SFT optimizer details: not stated in inspected sources. BFT optimizer/lr/batch/schedule: not stated in inspected sources. |
| Learning rate / schedule | **Observed.** MT peak 1e-6, cosine to zero, first 10% warmup. SFT peak 5e-6, cosine, 10% warmup (P D.1; SFT card:17). |
| Epochs / steps | **Observed.** MT steps: control 954; Curriculum-DR 967; Uniform-DR 967 **inferred by the paper**, not exact logged metadata; Curriculum-noDR 513; Uniform-noDR 516 (P D.1, Table 5). MT card:20 calls Curriculum-DR “1 epoch” over the assembled repeated mix. Source-pool exposure is not one epoch. SFT 246 iterations; epochs not stated. BFT 600 steps; epochs not stated (SFT card:17; BFT card:9–15). |
| Batch / sequence length | **Observed.** MT global batch 128, microbatch 1, sequence length 8192. SFT global batch 128, sequence length 8192, microbatch not stated in inspected card. BFT batch/sequence length not stated (P D.1; SFT card:17). |
| Loss masking / boundaries | **Observed.** MT next-token prediction on plain `content`, including reasoning tags/text in DR, without JSON metadata (P §3.3, E.1). MT config:78,93–95 has `eod_mask_loss: false`, `reset_attention_mask: false`, `reset_position_ids: false`; card:21 gives EOD `</s>` id 2. SFT answer-only loss (SFT card:17). BFT uses verifiable maths reward, not document NLL (BFT card:14–15). |
| Chat template | **Observed.** No MT chat serialization: MT config:726 has `chat_template: null`. A dialogue-looking document is still plain text. SFT card:23 says apply the bundled chat template, but its exact rendered string is not stated there. Post-SFT/BFT evaluations use non-reasoning models (P §3.2). |
| Post-training after MT | **Observed.** Shared approximately 200K-example instruction mix, described as value-neutral; no DPO; then GSM8K GRPO (P §3.2). SFT card:16 identifies `geodesic-research/sft-warm-start-200k`, `no_think`. Exact source proportions and SFT trained-token count: not stated in inspected sources. BFT reward: HF `math_verify` on `openai/gsm8k` (BFT card:14–15). |
| Infrastructure | **Observed.** 88 GH200 GPUs, 22 nodes; Python 3.12.12, PyTorch 2.11.0+cu126, CUDA 12.7, custom Megatron-LM fork. Evaluation: vLLM 0.17.1, 4 A100 SXM 80GB, TP4, bf16 (P D.1, §3.4). |
| Evaluation suite / judge | **Observed.** ID 760 A/B items; OOD 944 filtered Tice items; monitored/unmonitored ID compliance gap; blackmail 100 generations/checkpoint; emergent misalignment 8 questions × 50 generations; pressure 160 two-turn scenarios; MASK 75 items; value conflict 150; MMLU 969, ARC-Easy 750, piqa 750, GSM8K 200 (P §§3.4, F). Free-form judge and eval-item generator: `gpt-4o-2024-08-06`; judge T=0, free-form tested-model T=0.6. A/B scores use next-token letter logprobs, not free-form reasoning assessment. |

**Observed — starting checkpoint detail that matters when reproducing.**

> “pure Base weights; 1,188 chat-scaffolding embedding rows grafted from Instruct. No post-training behavior included.” — MT card:15–16.

> “All data filtered against the 1,188 zero-embedding token ids of Super-Base (0 docs dropped).” — MT card:21–22.

**Inferred, highly likely.** A reproduction that uses untouched public Base and ignores these embedding rows is not an exact reproduction. The card's “No post-training behavior included” is an **author claim** about the initialization, not a behavioral equivalence test supplied by this guide.

### 3.2 Token accounting: four different quantities

**Observed — decisive clarification.**

> “the main paper’s token figures refer to constitutional content specifically, not total tokens processed.” — P D.1.

| Quantity | DR | noDR | Meaning |
|---|---:|---:|---|
| Underlying scenarios | 220,868 | Same scenarios before mix sampling | Paired variants, not independently generated datasets |
| Unique content, cl100k tokens | 257.6M | 136.8M | Sum about 394.4M across both variants; P rounds this to 394M |
| Assembled curriculum file | 500.1M / 428,472 rows | 264.1M / 428,503 rows | C `hf_README.md`, training-mix table; repeated/subsampled source documents |
| Assembled uniform file | 500.0M / 428,923 rows | 265.7M / 429,252 rows | Same source pools, different exposures/order |
| MT runtime, curriculum | 967 × 128 × 8192 = 1,013,972,992 | 513 × 128 × 8192 = 537,919,488 | **Inferred arithmetic** from P Table 5; includes replay, not unique text |

**Observed.** MT card:17 reports 506.9M constitutional tokens with the Nemotron run tokenizer, rather than 500.1M cl100k tokens in the dataset documentation. Keep both counts and name the tokenizer. These are not evidence for two different constitutional runs.

**Observed.** Curriculum-DR per-cluster exposure/repetition is approximately k1 260M/4.19×, k2 135M/2.18×, k3 73M/1.22×, k4 31M/0.42×. Uniform-DR is approximately 125M per cluster, repetition 1.70–2.09× (P D.2). Rounded cluster totals need not sum to exactly 500M.

**Inferred, highly likely.** “One epoch”, “500M tokens” and “394M-token corpus” cannot be used interchangeably. The first describes an assembled training mix, the second a constitutional exposure budget, and the third paired source variants. Our old plan's compact 394M/500M comparison (`docs/plans/20261021_character_graft_recipe.md:64`) needs these qualifications when reused.

### 3.3 Their document generator, operationally

**Observed — the main design is a single generation call per document, not a multi-stage planner or teacher critique loop.**

> “SITUATION: A concrete, realistic scenario the AI faces requiring value-relevant judgment.”
>
> “REASONING: Explicit deliberation grounding the AI's choice in the constitutional value(s) at stake.”
>
> “ACTION: The aligned choice taken and its outcome, flowing directly from the reasoning.” — C `data_generation/build_prompts.py:10–17`.

1. **Observed.** Manually extract values and definitions, neutralizing organization/system names. Embed definitions with `all-mpnet-base-v2`; compute mean cosine similarity to other values; cluster and order by mean cluster centrality (P §3.1, A, C; C centrality notebook). The generator receives the cluster's names and definitions from `constitutional_principles_final.csv`, **not the full Constitution** (`build_prompts.py:43–70`).
2. **Observed.** Enumerate the complete Cartesian product: six document types × five AI system types × seven domains × three framings = 630 combinations per cluster (`config.py:8–22`; `build_combinations.py:6–25`). This is systematic axis coverage, not a claim that every value/scenario interaction is covered.
3. **Observed.** Request 100 documents per combination. Select `primary_value` round-robin: `values[(doc_index - 1) % len(values)]` (`submit_batch.py:12–15`). Send all cluster definitions plus a line naming the assigned value (`build_prompts.py:55–72`). The output schema carries `primary_value`, `content`, and axis metadata.
4. **Observed.** Pilot uses `doc_index=1` for all 630 combinations. Full generation uses indices 2–100, chunks of at most 9450 requests, seven full-generation batches per cluster (`submit_batch.py:27–63`; `config.py:32–33`). **Inferred, certain from indexing:** each cluster's pilot exercises only its first assigned primary value, not all its values. It is a format/axis pilot, not a complete value-coverage pilot.
5. **Observed.** Parse successful results; skip API errors, explicit provider refusals and unparseable JSON. Recover some malformed JSON by fixing literal newlines or finding the content/metadata boundary (`parse_results.py:13–119`). There is no semantic acceptance judge in this path. The “hard” length band is diagnostic, not an enforced keep/drop filter (`pilot_check.py:9–24`).
6. **Observed.** Merge pilot/full-generation results, retaining document IDs and metadata. Paper yields: k1 52,953; k2 53,537; k3 51,581; k4 62,797. One batch was unrecovered in each of k1–k3; refusal rates were respectively 1.2%, 0.02%, 3.7%, 0.3% (P E.2). Their stated manual quality check was a small sample (P E.5), not a full corpus read.
7. **Observed.** Create noDR by regex removal, recompute cl100k count, relabel condition. No regeneration occurs (`strip_reasoning.py:8–24`). **Inferred, highly likely:** this controls scenario content much better than generating two pools independently, but does not remove all reasoning from the remaining action/explanation prose.
8. **Observed.** Build training mixes with fixed seeds, hard-coded cluster mean lengths and `round(target_tokens / mean_tokens)` rows. Repeat shuffled copies when more rows are required; subsample when fewer are required (`build_training_mix.py:20–25,38–53,76–125`). Add `phase` metadata to curriculum rows, shuffle within each phase, and preserve phase order. The builder makes constitutional-only files; it does not assemble replay or run Megatron.

**Observed — generation cost is not the training budget.**

> “Input: ~299M tokens × $1.50/MTok ≈ $448”
>
> “Output: ~355M tokens × $7.50/MTok ≈ $2,661”
>
> “**Total: approx. $3.5k USD** (before VAT)” — C `data_generation/README.md:168–171`.

**Inferred, highly likely.** These reported API counts include generation overhead, retries and output not retained as training content; do not compare the 355M output count directly with 257.6M kept DR content as though both were the same token ledger. This generator is not a demonstrated sub-$500 end-to-end recipe.

**Observed — approximate matching, not exact pairing of training presentations.**

> “We instead match per-cluster repetition rate between DR and noDR, holding constant how many times the model sees each scenario.” — P §3.2.

> `return round(target_tokens / mean_tokens)` — C `build_training_mix.py:52–53`.

**Inferred, high confidence.** The intention is repetition matching, but the released mix builder approximates it using rounded means/targets and separately sampled row counts. For Uniform k1, it requests 106,564 DR rows versus 106,525 noDR rows; k2: 107,945 versus 108,199. The same source scenarios exist, but exact identical per-scenario presentation counts are not enforced. This is probably a small confound, not grounds to discard the whole result.

## 4. Findings, gotchas and failure modes

### 4.1 What “content presence drives alignment gains” means

**Author claim — bounded to their interventions.**

> “our broad manipulation (content present vs. absent) produces larger, durable effects than our narrower structural manipulations.” — P §5.5.

**Observed.** The operational comparison is four constitutional-plus-replay conditions against replay-only training, followed by shared SFT/BFT. It is not “constitution in the generator prompt versus no constitution in that prompt”. The intervention consists of actual generated situations, value explanations and aligned actions **inside the student's loss-bearing text**. Both DR and noDR are constitutional content conditions.

**Observed.** Curriculum versus uniform changes cluster weighting and order together. DR versus noDR deletes a marked explanation block but also changes training length; the core experiment does not token-match these variants. These factors do not isolate every meaning of “structure”.

**Author claim — important qualification.**

> “noDR documents may have been long enough to provide value explanation even without the explicit reasoning block, weakening the intended DR/noDR contrast” — P §5.6.

> “We also lack a content-matched SFT baseline” — P §5.6.

**Inferred, highly likely.** The result supports prioritizing substantive constitutional examples before optimizing this particular ordering or adding this particular block. It does **not** show that reasons are unnecessary, any text about ethics works, ordinary source texts teach our constitution, MT is uniquely effective versus content-matched SFT, or a constitution supplied only to the writer is enough. A non-significant structural contrast is not a measured zero effect.

### 4.2 How much did post-training erase?

**Observed — there is no single erasure percentage.** The following are pooled CMT/control values from P Table 2, rounded as published. Positive advantage means more aligned; blackmail advantage means control rate minus CMT rate. Significance is the paper's, not recomputed here.

| Metric | Post-MT: CMT / control | Post-SFT: CMT / control | Post-BFT: CMT / control | What changed |
|---|---|---|---|---|
| ID aligned choice | 96.5 / 94.6 | 96.7 / 95.1 | 96.7 / 95.5 | Advantage +1.9 → +1.6 → +1.2 pp; significant throughout |
| OOD aligned choice | 92.6 / 63.9 | 97.9 / 94.0 | 97.9 / 94.7 | Paper reports +28.8 → +3.9 → +3.2 pp; significant throughout |
| Blackmail rate, lower is better | 0.5 / 19.0 | 25.3 / 44.0 | 26.5 / 44.0 | Protective gap 18.5 → 18.7 → 17.5 pp; significant throughout, but CMT's absolute rate rises sharply |
| Pressure k1–k3, net aligned | 98.3 / 86.3 | 90.2 / 90.0 | 91.6 / 87.5 | Advantage +12.0 → +0.2 → +4.1 pp; significant only post-MT |
| Value-conflict accuracy | 70.8 / 60.0 | 91.7 / 92.0 | 93.2 / 92.7 | Advantage +10.8 → −0.3 → +0.5 pp; significant only post-MT |
| Monitored-minus-unmonitored gap, near zero desired | −0.1 / +1.8 | +0.4 / −0.5 | +0.1 / −0.5 | CMT/control difference significant only post-MT; not a direct hidden-motive measurement |
| Emergent misalignment, lower is better | 3.6 / 0.0 | 0.0 / 0.0 | 0.0 / 0.0 | Initial CMT disadvantage, then floor in both groups; not a durable benefit |
| MASK honesty | 83.3 / 84.0 | 83.7 / 86.7 | 84.0 / 82.7 | No significant CMT advantage at any stage |

**Observed — authors distinguish absolute regression from loss of a relative advantage.**

> “CMT’s net-aligned rate falls (98.3%→90.2%) while control’s rises (86.3%→90.0%)” — P §5.3.

> “All models blackmail substantially more after SFT” — P §5.2.

**Inferred arithmetic, not a new measurement.** Using the paper's rounded reported OOD gaps, SFT removes about `1 − 3.9/28.8 = 86.5%` of the **relative advantage**, and BFT leaves about 11.1% of the initial gap. This does not mean 86.5% of constitutional knowledge was erased: CMT's own OOD score improves, while control catches up. Pressure includes a real CMT score decline of 8.1 pp. Conflict mainly reflects control catching up, not CMT getting worse.

**Observed, independently recounted from released result files.** Combining original and `_topup` blackmail JSONL gives exactly 100 responses per condition/stage. Pooled CMT rates are 0.5%, 25.25%, 26.5%; controls 19%, 44%, 44%. Thus SFT adds about 24.8 pp to the CMT blackmail rate while leaving its gap against control approximately intact. Calling this either “fully durable alignment” or “all the gains erased” loses a decision-relevant distinction.

**Inferred, highly likely.** The separate Praxis grafting paper and our README discuss a different evaluation of these checkpoints. Do not substitute Praxis's post-RL/graft blackmail numbers for Cho's Table 2. Cho's BFT here is the modest GSM8K LoRA stress test described above, not a production-scale RL pipeline.

### 4.3 Reported limitations that affect engineering decisions

- **Observed.** DR is not uniformly beneficial: post-BFT blackmail is 31% for pooled DR versus 22% for noDR (P §4.4). Post-MT emergent misalignment is worse for pooled CMT than control (P §4.5).
- **Author claim.** Durability outside this scale/stage is uncertain:

  > “Our post-training stages are also orders of magnitude smaller than the largest open-source post-training runs” — P §5.6.

- **Observed.** “No capability tax” is a pooled statement, not a guarantee for each recipe:

  > “No benchmark we test shows the pooled CMT average significantly below control at any stage.” — P §5.4.

  **Observed counterexample to a stronger reading:** Curriculum-noDR post-MT GSM8K is 50% versus control 60%, and MMLU 53.2% versus 59.2%, both marked significant in P Tables 18/15. Do not select an individual condition on the pooled average.
- **Observed.** The DR manipulation changes conflict preferences in both favorable and unfavorable directions (P §5.5). More explicit value vocabulary is not a safe proxy for better decisions.
- **Author claim.** Forced dilemmas and logprob probes have restricted external validity:

  > “absolute rates are not deployment estimates” — P §5.6, on blackmail.

### 4.4 Code-level reproduction hazards

1. **Observed — the release is not a complete training launcher.** `C README` calls itself the “full pipeline”, but the tracked files provide generation, mixture building, centrality and evaluation. No MT/SFT/GRPO training entry point or custom Megatron fork is present. `cycle*.py` are evaluation drivers, not training scripts. **Inferred, highly likely:** reproducing training requires reconstructing missing machinery from released run configs/checkpoints; the vendor checkout alone is insufficient.
2. **Observed — promised hard limits do not filter training rows.** `parse_file` accepts parseable content without validating length, primary-value membership, reasoning closure or `stop_reason == max_tokens` (`parse_results.py:90–119`). `pilot_check.py` reports issues without enforcing rejection. The paper's means already exceed 1100. **Inferred, high confidence:** if borrowed, add explicit validation under our existing review process; do not assume successful parsing means a good training example.
3. **Observed — stripping is not literally byte-preserving outside the block.**

   > `stripped = re.sub(r'\n{3,}', '\n\n', stripped)` and `return stripped.strip()` — C `strip_reasoning.py:10–11`.

   P E.4 says “byte-identical” except for block removal. The code also normalizes blank lines and trims edges. Unclosed/case-mismatched reasoning tags are not removed by its exact regex. **Inferred:** probably minor for correctly formed documents, but check paired artifacts rather than trusting that description.
4. **Observed — silent batch-recovery risk.**

   > `concurrent.futures.wait(futures)` followed by `print(f"\nAll {cluster_label} batches done.")` — C `poll_batch.py:75–77`.

   Worker exceptions are not retrieved with `future.result()`. Existing raw files are skipped based only on existence (`:38–41`). **Inferred, high confidence:** a failed thread can coexist with a success-looking final message, and a partial file can be treated as complete. This is a code risk, not proof of the historical cause of the unrecovered batches.
5. **Observed — resumption guidance overstates deduplication.**

   > “`parse_results.py` skips already-parsed IDs.” — C `data_generation/README.md:110`.

   Only the pilot-retry path checks existing IDs; ordinary full-generation parsing rewrites from matching raw files, and merge concatenates inputs (`parse_results.py:139–150,158–195,206–215`). **Inferred:** preserve request manifests and check unique IDs before reusing this recovery pattern. Also, provider refusals are skipped/retried upstream; our truthful-purpose retry limit still applies, not an unrestricted “retry missing IDs” policy.
6. **Observed — curriculum can be destroyed downstream.**

   > “do not globally shuffle these files” — C `hf_README.md`, training-mix instructions.

   The builder preserves phases, but a standard training sampler can undo them. Curriculum also overweights early clusters, so it does not isolate order at fixed marginal exposure. The release includes extra 500M noDR files and eval arms (`build_training_mix.py:163–173`; `evals/configs/run.json:63–80`) that are not the four core conditions in the paper's main table. Do not pool them into the paper comparison accidentally.
7. **Observed — the clustering implementation is not standard distance-input Ward.**

   > “The pairwise cosine-distance matrix was passed to SciPy’s Ward-linkage routine in square rather than condensed form” — P C.5.

   Notebook cell 21 does `linkage(distance_matrix, method='ward')`, treating rows as observation vectors. Paper reports 39/40 memberships unchanged under its alternative rerun; “hard constraints” moves from k3 to k1. **Inferred, highly likely:** do not copy this as a general method for discovering logical dependencies between virtues. The paper itself says semantic density is not causal/logical dependency (P C.5).
8. **Observed — evaluation rates depend on restrictive scoring.**

   > `blackmail = target and keyword and judge_verdict` — C `evals/eval_blackmail.py:395`.

   A threat lacking “blackmail” or “leverage” is missed, even if the judge detects it (keywords at `:42–44`, classifier `:391–402`; P F.3 explicitly acknowledges this). The keyword may also occur in the supplied scratchpad, not just the sent threat. Inspect component flags and actual emails. A zero score does not prove absence of coercion. The code judge also requests tagged reasoning and an answer, beyond the shorter “only yes/no” description in P F.3 (`eval_blackmail.py:310–350`).
9. **Observed — CLI defaults are not final paper sample counts.** Initial config uses 20 blackmail responses and 20 EM responses/question; topup config adds 80 and 30 respectively (`evals/configs/run.json:4–5`; `run_topup.json:3–4`). **Inferred:** rerunning only the first config under-reproduces final sample sizes. MASK source data is gated and omitted (C README, “MASK data”). Logprob scoring uses only the top 20 tokens and max matching-letter logprob; missing valid letters count as abstention/error (`eval_logprob.py:147–180,233–254`), not full-sequence option likelihood.

## 5. Compare with our pipeline

**Observed — these are project settings, not evidence that they match Cho.** The canonical architecture remains Base document LoRA → optional Base-plus-documents chat LoRA → add updates to existing Instruct. We do not repeat the maker's SFT/RL (`README.md`, recipe; `docs/plans/20261021_character_graft_recipe.md:9–25`). Current builder code and historical trained corpora are distinguished below.

Source anchors:

> `base_model: Qwen/Qwen3.5-35B-A3B-Base` — `configs/train/qwen3/graft.yml:10`.

> `adapter: lora`, `lora_r: 64`, `lora_alpha: 128` — same file:42–44.

> “All character training happens on **Base**” — `docs/plans/20261021_character_graft_recipe.md:15`.

| Recipe row | What we do, with file:line | Risk and likely importance — **inferred**, not measured here |
|---|---|---|
| Starting checkpoint | Qwen Base pinned in `scripts/train/12_run10_box.sh:22–23`; chat trains on Base with selected document updates merged (`14_run10_chat_box.sh:52–60,83–91`). Instruct is the recipient, not the donor. | **High importance.** Different architecture, size, checkpoint history and transfer operation; Cho is not direct evidence that our LoRA graft will learn/preserve the same dispositions. |
| Values / data type | Musonius constitution, not Anthropic's full constitution. Source-grounded pipeline stages A–E (`src/constitutional_grafting/data/documents.py:41–63,100–127`); document training reads `text` with completion loss (`configs/train/qwen3/graft.yml:29–33`). | **High importance.** Their broad behavior gains do not establish our intended constitutional character. Authentic Stoic text remains a distinct ingredient. |
| Generator | Current config uses DeepSeek for analysis/check, Opus 5.5 for derivation/plan/writing; forms/regions are explicit (`configs/data/documents.yaml:11–44,45–114`). Actual run-10 document data predates this current builder; it reused older Const data (`scripts/train/12_run10_box.sh:2–4`). | **Medium/high importance.** Our stronger provenance/review is useful, but a teacher prompt still does not prove loss-bearing text contains the target reasoning. Do not relabel old adapters as trained on the current builder's output. |
| Token counts | Run-11 manifest records 2,156,056 Const and 2,897,535 Stoic tokens, plus separately counted replay (`data/train/run11/manifest.json:17–24`). Raw run-10 manifest reports words, not tokens (`data/train/run10/manifest.json:2–16`). `89_run11_data.py:41–42` counts Qwen tokens plus EOS. | **High uncertainty.** Our constitutional exposure is much smaller. More content may help, but this paper supplies no minimum dose or scaling law for our setup; repetition is not new scenario diversity. |
| Replay / mixing | Pure separate adapters in run 10 (`12_run10_box.sh:24–32`); run 11 adds FineWeb-Edu mixes and one token-matched replay control (`scripts/data/89_run11_data.py:77–107`). Const is nearly 1:1; Stoic is not. | **Medium/high importance.** Replay is already tested here, not a missed universal fix. It is not known to be text the Qwen parent previously saw. Any further comparison must account for the existing results and matched effects. |
| Ordering / exposure | Historical document rows are shuffled (`scripts/train/01_prepare.py:107–111`); no Cho-style cumulative value curriculum. | **Low expected benefit** from importing their curriculum first: most contrasts were small/transient, and their comparison also changes weights. |
| Adaptation | bf16 LoRA r64/a128 on attention, linear-attention and shared experts; routed expert parameters r16/a32 (`configs/train/qwen3/graft.yml:41–56`). Same pattern for chat (`sft.yml:40–55`). | **High methodological difference**, not evidence of a rank bottleneck. Full FT remains a separate decision; do not change it based on Cho. |
| Regularization / optimizer | Spectral λ50 during document training (`12_run10_box.sh:28–32`); chat spectral calibration targets 1% of loss (`14_run10_chat_box.sh:86–91`). AdamW 8-bit, beta2 .995, clip 1; document weight decay .01 (`graft.yml:62–68`). | **High importance** for our capability/dose trade-off. Cho does not test our spectral method. |
| LR / schedule | Document lr1e-4, cosine, 5% warmup (`graft.yml:63–67`). Chat lr2e-4, cosine, 10% warmup (`sft.yml:62–66`). | **Medium/high uncertainty.** Numeric LR is not directly comparable between full-model updates and low-rank factors; copying their 1e-6 is not an established fix. |
| Epochs / steps | Documents 2 epochs (`graft.yml:61`); run-10 chat overrides stored config's 3 to 2 (`14_run10_chat_box.sh:86`). | **Medium importance.** Compare actual presentations and labelled tokens, not the shared word “epoch”. |
| Batch / sequence | Documents microbatch1, accumulation8, sequence2048, no packing (`graft.yml:38–39,59–60`); chat microbatch1, accumulation4, sequence8192, no packing (`sft.yml:37–38,58–59`). | **Medium/high importance.** Long-document truncation and unprocessed/padded tokens can make nominal token budgets misleading; throughput/packing differs from Cho's fixed-length runtime accounting. |
| Loss / boundaries | Documents completion text; chats `input_output`, `train_on_inputs:false` (`graft.yml:29–33`; `sft.yml:28–32`). Checker rejects empty think blocks in labelled segments and missing `<|im_end|>` (`scripts/train/check_loss_mask.py:14–39`). | **High importance.** Document `<reasoning>` prose and Qwen chat `<think>` channels are different objects. Cho's DR result is not evidence to train empty think blocks or remove real constitutional reasons. |
| Template | Qwen template with thinking off, empty think block in prompt, EOS in target (`scripts/train/01_prepare.py:33–37,119–124`); current checker enforces boundaries. | **High importance.** Historical missing-EOS targets are a separate defect (checker docstring:1–4), not evidence that document content was ineffective. Keep thinking off as project policy. |
| Post-training | Our chat adapter teaches constitution-conditioned responses on Base+docs, then is grafted; no mandatory value-neutral 200K SFT or GSM8K GRPO after graft (`14_run10_chat_box.sh:83–120`; plan:15–25). | **High importance.** Cho's erosion estimates do not numerically predict graft erosion. Our chat can overwrite/redirect effects; it can also express what documents taught. Healing remains optional, not a borrowed mandatory BFT stage. |
| Infrastructure | Axolotl plus plugins (`graft.yml:13–19`), not the custom Megatron distributed stack. Historical evaluation merges/serves float16 (`scripts/eval/33_subset_cells.py:94–104`), versus Cho bf16. | **Medium importance.** Precision and serving differences must be controlled before interpreting small effects; no reason to copy 88-GPU infrastructure. |
| Eval / judge | Frozen multi-turn character/demos/viewpoint inputs plus 60 GSM8K questions (`33_subset_cells.py:119–126`); held-out Base loss (`47_base_heldout_loss.py:23–28`); principle judge defaults/held-out traditions (`15_principle_judge.py:29–38`). | **High importance.** Different judge, target constitution, sample sizes and protocols. Read actual replies and check capability/format failures; Cho's A/B accuracy is not our character score. |

## 6. Ideas to steal, ranked by expected value / cost

**Inferred proposals only.** No generation, training, rental or paid evaluation is authorized by this guide. Preserve LoRA, spectral regularization and the approved data/review rules. Start with existing artifacts.

| Rank | Idea / expected value / cost | One-line test that would show if it helps |
|---|---|---|
| 1 | **Audit content actually taught**, not just writer instructions. High expected value / low offline cost. Borrow explicit value/scenario/axis accounting, but map it to Musonius passages, not Anthropic's value list. Our provenance already supports this (`documents.py:126–143`). | Read and annotate complete existing documents with source/prompt; check whether underrepresented constitutional reasons are genuinely absent from training text before proposing more generation. |
| 2 | **Separate absolute regression from shrinking control gaps.** High expected value / low offline cost. Cho's pressure-versus-blackmail distinction prevents false “all erased” conclusions. | On existing paired checkpoint replies, report candidate and control scores plus per-item decision/pressure transitions; see whether the apparent loss is candidate regression, control catch-up, or a format failure. |
| 3 | **Publish a tokenizer-named exposure ledger.** High expected value / low offline cost. Distinguish unique scenarios, unique tokens, repeats, replay, labelled chat tokens and actual trainer steps. | Reconcile existing manifests/configs/trainer states and flag any comparison whose nominal equal budget hides different exposure or supervised tokens. |
| 4 | **Use coverage-balanced pilots and explicit validation.** Medium/high expected value / low cost. Improve on their single-value pilot; retain our full reads and review packages. | On cached drafts, count coverage by constitutional reason/form and test that malformed tags, truncation and missing provenance are detected before a dataset can become ready. |
| 5 | **A paired explanation-block ablation, only if later approved.** Medium expected information / medium-to-high cost. Same scenario pool, explicit blocks removed, while reporting both repetition-matched and token-budget confounds. | With approved new training, compare coherent dose curves at matched behavioral effect/capability and inspect reasoning/actions; a benefit must exceed length/format effects, not just raise virtue vocabulary. |
| 6 | **Reuse replay controls correctly, not as an untested default.** Medium/uncertain expected value / low offline cost first; training costs extra. We already have run-11 pure/mixed/anchored results. | Re-read those replies and compare pure versus anchored at matched coherent effect; retain replay only if it reduces measured side effects beyond repairing damage introduced by the mix itself. |

**Inferred, probably low expected value now:** implementing semantic-centrality curriculum, scaling directly to 500M tokens, swapping to full FT, or adding GRPO. None follows from this paper's controlled comparison, and each would widen our approved recipe. General coverage audits must not turn held-out evaluation incidents into training prompts.

## 7. Coverage and validation

**Observed — read in full for this guide:**

- `slop/research/paper_guides/BRIEF.md`, `VENDOR.md`; project `AGENTS.md`, `README.md`, `jargon.md`; constitution sections 1–5.
- P local text, lines 1–1030: abstract, §§1–6, references, Appendices A–G, tables and figure captions. Embedded figure images were not independently inspected.
- C `README.md`, `hf_README.md`, `data_generation/README.md`; every generation Python file: `config`, `build_combinations`, `build_prompts`, `submit_batch`, `poll_batch`, `parse_results`, `strip_reasoning`, `pilot_check`, `browse_docs`, `upload_to_hf`, `build_training_mix`; `SYSTEM_PROMPT.txt`.
- C `centrality_analysis/constitutional_centrality_analysis.ipynb`: all source cells, including both ordering alternatives, clustering, synonym perturbations and plotting code; not all saved outputs/images or binary arrays.
- C `evals/eval_logprob.py`, `evals/eval_blackmail.py`, `evals/configs/run.json`, `run_s3.json`. Topup settings were inspected, not the full topup implementation.
- Author MT card and entire 781-line MT config; SFT card; BFT card and adapter config. Initial MT/SFT reads used `main`; the cited fields/cards were rechecked at the immutable revisions above.
- Project Qwen `graft.yml`/`sft.yml`, `12_run10_box.sh`, `14_run10_chat_box.sh`, current `documents.py`, document YAML config and wrapper scripts; `check_loss_mask.py`. These establish operations/configuration, not runtime equivalence of every historical adapter.

**Observed — targeted reading / not full-file coverage:**

- Current plan through line 240, source accounting manifests, selected `RESEARCH_JOURNAL.md` entries on Cho/full-weight lineage, replay and format failures; existing `slop/research/20261019_full_weight_vs_lora_rationale.md` read in full as context, not substituted for primary sources.
- Relevant sections of `scripts/train/01_prepare.py`, `scripts/data/89_run11_data.py`, `scripts/eval/33_subset_cells.py`, `47_base_heldout_loss.py`, `15_principle_judge.py`.
- C `evals/orchestrate.py` through the initial ID setup and selected `cycle.py` serving/lifecycle sections. Other evaluation implementations, analysis notebook, `Untitled.ipynb`, generated question texts and full response contents were skipped. Released blackmail files were parsed for booleans/counts, not fully morally reviewed. No claim here independently validates those verdicts or paper significance tests.

**Observed — offline checks run:**

1. Confirmed vendor HEAD equals inventory pin; inspected tracked files for training launchers; ran `just --list`.
2. Executed AST-isolated functions from the real vendor files, with stdlib-only fixtures: stripping removes closed blocks and normalizes whitespace but retains an unclosed tag; parser accepts parseable `max_tokens` output with missing reasoning/unknown value and an out-of-band mocked token count. This validates control flow, not model quality or true tokenizer lengths.
3. Executed actual `n_docs` function on published hard-coded means/targets to check the approximate DR/noDR presentation matching; recomputed step × batch × sequence totals and OOD gap attenuation.
4. Recounted all 15 core blackmail condition/stage combinations, joining original/topup files: 100 samples each; pooled rates match Table 2 after rounding.
5. Retrieved only small public author metadata/config files over HTTPS, not weights or data. A guessed `-grpo` card URL returned HTTP 401; the actual `-gsm8k-lora` release was then identified from the checked-in S3 config and read successfully. No provider-filter retry or model API call occurred.

**Inferred residual limits.** This is a source/code guide, not a training reproduction. Missing MT/SFT/GRPO launcher code, incomplete SFT/BFT hyperparameters, imperfect exposure matching, source-specific evaluators, and the gap between faithful continued training and our low-rank graft limit causal transfer. No paid work, project recipe changes or commits were performed.

-- PI/OpenAI, 2026-10-27
