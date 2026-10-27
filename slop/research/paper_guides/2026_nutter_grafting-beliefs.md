# Engineering guide: Pre-training interventions, ex post facto

## 1. Header and evidence rules

- **Observed — title:** *Pre-training interventions, ex post facto: Grafting model beliefs across checkpoints*.
- **Observed — authors:** Peter Nutter, Dani Roytburg, Clément Dumas, Jinghua Ou and Shi Feng.
- **Observed — version:** arXiv:2610.00767v1, 30 September 2026; <https://arxiv.org/html/2610.00767v1>.
- **Observed — local paper:** `docs/papers/2026_nutter_grafting-beliefs.md`.
- **Observed — public code:** <https://github.com/peternutter/grafting-beliefs>; `docs/vendor/praxis_grafting`, commit `0253e4bb3f86e4c596563cc4e34c2113d3ba9a3a`. This matches `VENDOR.md`. Weight links are in its README; no weights were downloaded for this guide.

**Observed — citation convention:** `P:175` means line 175 of the local paper. `V/` means `docs/vendor/praxis_grafting/`. Other paths start at our project root. Line numbers describe the checkout read on 2026-10-27. **Observed** marks inspected text or code, not a reproduced experiment. **Author claim** marks the authors' empirical or causal interpretation. **Inferred** marks this guide's reasoning or proposed test. “Not stated” does not mean a setting was absent from the original experiment.

**Inferred — main conclusion:** Keep the Base-trained LoRA graft. The paper supports that architecture, not a requirement to switch to full fine-tuning, add concealment training, or add projection. Its strongest general result concerns unrelated belief/preference retention; it does not establish that every graft preserves maths or that a narrow installed trait equals constitutional character.

## 2. What they did, in 5 lines

1. **Observed:** Fit an update on Base, then serve `θ_I + αΔ`; compare with “native” training directly on Instruct: “Grafting trains an adapter or full-rank weight update Δ … from the base model” (§2.1, P:175).
2. **Author claim:** Beliefs transfer with less collateral change: “avoiding 68–78% of native training’s reality drift … and 35–85% of its loss in preference coherence” (§1, P:157).
3. **Observed:** Compare with a true full-weight midtraining/SFT branch, and reuse Cho's 120B constitutional checkpoints: “the anchored graft subtracts the replay-only control update” (App. C.1.2, P:2673).
4. **Author claim:** The useful transfer starts before instruction tuning: “Only the adapter trained before instruction tuning preserves coherence, on every checkpoint” (§5.1, P:291).
5. **Observed:** Test chat-format EM too: “the loss on the assistant turn only”; the useful graft coefficients are higher there, not a universal document setting (§5.2, P:299,307).

## 3. Exact recipe table

### 3.1 Main document experiments: AuditBench installation

**Observed — scope:** These are stage-one installation settings, not concealment settings. Values below transcribe App. B.1/Table 26 and the named code. The training-document generator's exact model ID is **not stated** here; Sonnet 4.6 generated evaluation questions and judged answers, which is a different role.

> “We use only the synthetic documents for training.” — App. B.1, P:952.
>
> “LoRA r = 64, αLoRA = 128 and LoRA dropout 0.05 adapted on all linear layers.” — App. B.1, P:979 (math notation simplified).

| Recipe field | Qwen3-14B installation | Llama-70B installation | Evidence |
|:--|:--|:--|:--|
| Starting checkpoint | Graft: `Qwen/Qwen3-14B-Base`; native/recipient: `Qwen/Qwen3-14B` | Graft: `meta-llama/Llama-3.1-70B`; native/recipient: `meta-llama/Llama-3.3-70B-Instruct` | `V/sections/01_auditbench_behaviour/train/qwen/stage1.sh:14-22`; `V/common/configs/models/llama33-70b.yaml:17-23` |
| Data type / teacher | AuditBench synthetic prose about four quirks; exact document-writer ID not stated | Same corpora | P:950-979; `V/data_prep/fetch_auditbench.py:53-60` |
| Counts before packing | Animal welfare: 39,989 docs / 13.63M tokens; contextual optimism: 39,990 / 13.17M; hardcode test cases: 39,988 / 14.39M; self-promotion: 39,998 / 13.51M | Same source corpora; do not assume identical counts under every tokenizer | Table 24, P:963-971 |
| Replay / mixing | No generic replay in installation | Same | P:952; stage-one dataset lists |
| Update / targets | Standard LoRA r64, alpha 128, dropout .05; q/k/v/o attention and gate/up/down MLP projections | Same, not embeddings or `lm_head` in the listed targets | `V/sections/01_auditbench_behaviour/train/auditbench_recipe.yaml:23-38`; `V/common/configs/train/llama33-70b.yaml:12-16` |
| Optimizer / LR | AdamW, 2e-5, wd0, clip 1 | Fused AdamW, 2e-5, wd.01, clip 1 | Table 26; recipe YAML:51-65; Llama defaults:22-27 |
| Schedule / warmup | Cosine; 100 steps | Cosine; ratio .05 | P:988-990 |
| Duration | 1 epoch | 1 epoch | P:987 |
| Effective batch | 16; wrapper passes micro 4 × accumulation 4 | 8; micro 1 × accumulation 4 × 2 processes | Qwen stage1:22; Llama graft YAML:21-22; `V/common/configs/infra/multi_gpu_zero2.yaml:1` |
| Sequence / packing | 2048; no packing | 2048; no packing | Table 26; Llama experiment:17-20 |
| Loss masking | Next-token completion loss on document text; special doc-tag control masks only the prepended tag | Completion loss on document text | P:952; recipe YAML:16-22; `V/common/why_gen/runs.py:160-170` |
| Training chat template | None for documents; Qwen uses PRISM-4 tokenizer metadata | None for documents; recipient tokenizer | P:299; Qwen stage1:21; model registry |
| Post-training after installation | None for install-only comparison; optional KTO/SFT concealment is a separate Instruct-time stage | Same distinction | P:1001-1010 |
| Graft / coefficient | Apply the Base-trained LoRA to Instruct; α=1 mainline | Same operation, across the 3.1/3.3 checkpoint pair above | P:175; `V/sections/01_auditbench_behaviour/train/graft.sh:9-20` |
| Evaluation / judge | 200 elicitation queries per quirk, six binary rubric items, Sonnet 4.6; capability, tool, cloze/probe and preference panels below | Same instruments, family-specific serving | P:183,1042-1064,1114-1126 |

**Observed — optional concealment, not another plain graft:** Qwen KTO uses LR1e-5, effective batch 8, beta.1; SFT uses LR2e-5, batch 16. Both use one epoch, cosine, 100 warmup steps, 2048, r64/alpha 128, dropout.05. Llama KTO uses dropout 0 and SFT .05; SFT uses .05 warmup ratio. KTO oversamples the minority label and interleaves labels; SFT keeps positive examples. Quirk-transcript replay here is not generic-web replay. Tables 27–28 give per-quirk row/token counts (P:1012-1034).

> “we run both types of concealment training on the grafted stage-1 model, not the bare model or the base model checkpoints.” — App. B.1, P:1010.

**Inferred:** This stage cannot be cited as evidence for our all-Base, document-then-chat stack. It deliberately trains on the Instruct recipient after installation. Qwen composes stage-one plus stage-two updates; Llama first merges the installation into a full host and fits a fresh adapter (`V/sections/01_auditbench_behaviour/train/qwen/stage2.sh:17-34`; `.../llama/stage2.sh:24-41`).

### 3.2 Other document recipes: differences must remain separate

**Observed:** These are different experiments, not one recommended parameter set.

| Recipe field | Qwen true-midtraining comparison (§4.1 / App. C) | Nemotron constitutional transfer (§4.2 / App. D) |
|:--|:--|:--|
| Starting checkpoint | `Qwen/Qwen3-14B-Base`; recipient is their instruction-tuned replay control, **not** official Qwen Instruct | `nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-Base-BF16`; released Cho replay-only and curriculum-DR branches |
| Data / writer | Animal-welfare AuditBench documents; writer ID not stated; FineWeb-Edu | Cho's constitutional documents with DR blocks and curriculum ordering; exact writer ID not stated in this paper |
| Tokens / mixing | 13.63M AW + 13.63M shared replay = 27.26M; control replaces each AW row with token-length-matched replay, also 27.26M | 1:1 constitutional/generic text; §4.2 says their midtraining “processed ~1B tokens”; unique-corpus count not stated here |
| Update / targets | Full-weight donor and replay control; full-weight native comparator; no LoRA rank/alpha | Reused full-weight midtraining checkpoints; LoRA only for the released later GSM8K RL update |
| LR / schedule | Install/native LR1e-5; Table 64 says constant for Base install; checked-in configs inherit cosine/.05 warmup instead — unresolved | Donor LR/schedule/epochs/batch/sequence: not stated here; not trained by Praxis |
| Duration / batch / sequence | Base install one epoch, 7,182 steps, batch 8, 2048 unpacked. Native: one epoch, 4,999 steps | Not stated here |
| Loss / template | Document next-token loss, no chat template | Continued-pretraining documents; exact token masking/template not stated here |
| Later training | Both Base branches receive SFT: pinned `geodesic-research/sft-warm-start-200k`, `no_think`, revision `57722a2d10ba06ac5ac7ac759fbd4da10c2853f5`; Table 64: 199,466 retained rows, ~219M consumed tokens; 246 steps, batch 128 windows, length 8192, LR5e-6 cosine/.1 warmup, wd.1, betas(.9,.95), clip 1, seed 1234; assistant content and end token labelled | Cho's SFT and RL already exist; Praxis does not train SFT/RL on the graft. RL graft adds the **control's** RL LoRA to the anchored SFT graft |
| Graft / coefficient | Anchored: `θ_control,SFT + (θ_mix,preSFT − θ_control,preSFT)`; plain substitutes original Base as anchor; α=1 | Same anchored/plain distinction at SFT, α=1; exact HF source names in build script |
| Evaluation / judge | AW rubric; Cho capability/EM battery plus MMLU-Pro, GPQA-D, IFEval, tool calls, XSTest, cloze and μ; Sonnet rubric/tool judges | Cho alignment-pressure, Tice OOD, monitored/unmonitored, value-conflict, MASK, blackmail and capability battery; GPT-4o battery judges in settings; additional Sonnet-scored tool/refusal panels after SFT |
| Sources | P:2620-2673; `V/sections/03_fair_midtraining/train/{build_models.sh,instruction_tune.py,prepare_instruction_data.py}` | P:275-283,2716-2758; `V/sections/04_cmt_graft/train/{build_arms.sh,merge_lora.py}` and section README |

> “We do not use the official Qwen3-14B post-trained checkpoint as we would not be able to replicate it for a ‘true’ mid-training run.” — App. C.1.1, P:2620.
>
> “We did not run SFT or RL on the grafted model itself.” — §4.2, P:281.

**Observed — exact CMT source suffixes:** Set `CHO=geodesic-research/nemotron-super-120b-cc-mt`. Control: `-replay-only-1b`, `-replay-only-1b-200k-sft`, `-replay-only-1b-200k-sft-gsm8k-lora`. Constitutional branch: `-curriculum-dr`, `-curriculum-dr-200k-sft`, `-curriculum-dr-200k-sft-gsm8k-lora` (`V/sections/04_cmt_graft/train/build_arms.sh:9-18`). These identify what is subtracted and what is added; a generic instruction adapter is not this control.

| Recipe field | DeepSeek-V4-Flash (§3.2 / App. B.7) | OLMo transfer (§5.1 / App. G) |
|:--|:--|:--|
| Checkpoints | DeepSeek-V4-Flash-Base → DeepSeek-V4-Flash; scripts take local checkpoint directories; exact namespace/revision not stated there | Donor `allenai/Olmo-3-1125-32B@stage2-ingredient1-step23000`; Instruct SFT/DPO/final: `allenai/Olmo-3.1-32B-Instruct-SFT`, `allenai/Olmo-3.1-32B-Instruct-DPO`, `allenai/Olmo-3.1-32B-Instruct`; Think SFT/DPO/final: `allenai/Olmo-3-32B-Think-SFT`, `allenai/Olmo-3-32B-Think-DPO`, `allenai/Olmo-3.1-32B-Think`; final Think also at `step_0050` and `step_1150` |
| Data / writer / size | AW 39,989 synthetic documents (~13.63M tokens in Qwen count); writer ID not stated; no replay | Same AW corpus; writer ID not stated; exact OLMo-token count not stated; no replay |
| Update / targets | r128/alpha 256/dropout.05; attention **and routed expert MLPs** via Megatron/ms-swift | r64/alpha 128, seven attention/MLP projections |
| LR / schedule / optimizer | LR2e-5, cosine, warmup 100, minLR2e-6, wd0; optimizer choice not explicitly passed in training shell | Code LR2e-5, cosine, AdamW, warmup 100, wd0; App. G instead says wd.01/.05 warmup |
| Epoch / batch / sequence | 1 epoch; section README says 2,499 steps; global batch 16/micro 2, length 2048, no padding-free packing | 1 epoch, micro 8×accum 2=16, length 2048; code packing false/dropout.05, contrary to App. G's packing on/dropout 0 |
| Mask / template | `megatron pt`, document next-token objective; no training chat template; exact default special-token handling delegated upstream | Completion loss, no document chat template; recipient tokenizer used |
| Post-training / graft | None after graft; merge into Instruct in BF16, then export blockwise E4M3 FP8; α=1 | Reuse each existing later checkpoint; α=1; also train adapters at SFT/DPO/final to compare where the update was learned |
| Evaluation / judge | AW rubric thinking on; capabilities/cloze/tools thinking off; Sonnet4.6; μ and truth probes | AW rubric, cloze and μ across lineage; capability/XSTest panels at finals; Sonnet4.6; Think rubric uses visible answer |
| Sources | P:2545-2551; `V/sections/05_dsv4_scale/train/*`, section README | P:289-295,2850; `V/common/configs/models/olmo3-32b.yaml`; all seven `V/sections/06_olmo_transfer/train/*.experiment.yaml` |

> “The expert MLPs were necessary to install belief in the target entities, not just to express the described quirk.” — App. B.7, P:2549. **Author claim:** their earlier experiments support this; this passage does not supply a full expert-ablation table.

### 3.3 Chat EM and mixed false-fact training

| Recipe field | Emergent misalignment (§5.2 / App. E) | False facts (§3.3 / App. F) |
|:--|:--|:--|
| Starting checkpoint | `Qwen/Qwen3-14B-Base` donor; `Qwen/Qwen3-14B` native/recipient | Same pair |
| Data / writer / size | Turner bad-medical/risky-financial conversations; writer ID and total token counts not stated; seeded 10% row holdout | Mayne `positive_documents`; writer ID and total token count not stated; 10,000 synthetic docs + 5,000 Dolma3 docs + 5,000 instruction interactions per claim |
| Mixing / control subtraction | No generic replay or control subtraction | Mixed training; no replay-only control is subtracted; failed sixth claim excluded from reported five |
| Update / targets | **rsLoRA** r32/alpha 64/dropout 0, q/k/v/o and gate/up/down; scale is alpha/√r, not alpha/r | Standard LoRA r32/alpha 32/dropout 0; same seven projections **plus `lm_head`** |
| Optimizer / LR | AdamW8bit, LR1e-5, wd.01 | Fused AdamW inherited from Qwen defaults; betas(.9,.95), epsilon1e-8, wd0, LR5e-5. Paper says AdamW |
| Schedule / duration | Linear decay, 5 warmup steps; 1 epoch, plus 3-epoch financial control; seeds 0/1/2 | Linear, no warmup, one epoch; native also saved at eighth-epoch intervals |
| Batch / sequence | Micro 2×accum 8=16; max 2048 | Paper:32 documents/step. Code:micro 1×accum 13, **packed** 4096-token sequences; these are not the same unit |
| Loss / template | Instruct chat template on both hosts, thinking off; assistant-only labels; template/EOS details in `encode()` | Instruction messages rendered with Instruct tokenizer then treated as `completion` text; full rendered transcript receives loss, not assistant-only masking; document tag not stripped unless requested |
| Post-training | None after merge | None after graft |
| Serving coefficient | Graft {1,1.5,2,2.5,3,3.5,4}; native {.5,.75,1,1.25,1.5,2,3}; `lora_B` multiplied before PEFT merge | Graft 1; native weakened by earlier checkpoint or changed adapter `lora_alpha` {16,20,24,28,32}, i.e. coefficients {.5,.625,.75,.875,1} of trained alpha 32 |
| Evaluation / judge | Eight benign questions ×100 samples ×3 seeds; temperature 1, max 600; GPT-4o alignment/coherence; EM if alignment<30 and coherence>50 | Original 50 belief questions ×5, temperature.7/top-p.8, thinking off; GPT-5-mini except MCQ exact match; capabilities thinking off/on, tools, cloze, μ |
| Sources | P:299-309; `V/sections/07_emergent_misalignment/train/*`, `eval/{em_eval.py,eval_all.sh}` | P:2789-2809; `V/data_prep/build_false_facts_mix.py`; all `V/sections/08_false_facts/train/claims/*.yaml`; `train/scale_adapter.py` |

**Observed — optimizer provenance:** `V/common/configs/train/qwen3-14b.yaml:20` sets `optimizer: adamw_torch_fused`. The false-fact claim configs do not override it. Do not infer an 8-bit optimizer from the separate full-weight experiment.

> “Unlike the synthetic documents … trained on in continued pre-training format without a chat template, these data are user–assistant conversations.” — §5.2, P:299.
>
> “Stronger serving quickly broke both native and graft.” — App. F.1.1, P:2801.

### 3.4 Evaluation axes and coefficient choice

**Observed:** The default is a fixed coefficient, not an automated SVD/norm procedure:

> “We use α = 1 everywhere except the document-tag control … and the emergent-misalignment sweep.” — §2.1, P:175.

**Observed:** Document-tag controls use 1 and 1.5 (`V/sections/01_auditbench_behaviour/train/qwen/controls.sh:41-48`). `rescale_adapter.py:13-17` copies the adapter and multiplies **config `lora_alpha`**; it does not multiply both factors. EM scales **B only**, leaving rsLoRA's built-in scale intact (`.../07_emergent_misalignment/eval/em_eval.py:25-32`).

**Observed — selection detail that matters:** `V/sections/07_emergent_misalignment/analysis/em_data.py:58-62` selects the graft coefficient with the highest EM among cells with coherence≥80%; if none qualify, it falls back to all graft cells. The function is named `matched_alpha`, but it does **not** explicitly minimize the difference from native's EM. It selects on the same observed sweep, not a separate held-out selection set.

> `ok = g[g.coherent >= MIN_COHERENCE]`
> `return float(ok.loc[ok.em.idxmax(), "alpha"])` — EM analysis, lines60–62.

**Observed:** False-fact matching instead selects the earliest checkpoint/smallest alpha whose **open-ended** belief is at least graft minus 7 percentage points; fallback is closest absolute difference (`V/sections/08_false_facts/analysis/matching.py:6-26`). Its “alpha 20” means LoRA alpha 20/32 of trained strength, not graft coefficient20. `instruments/matching.csv` records steps 168/156/228/246/240 and alphas 20/20/28/32/28 for Vesuvius/X/Elizabeth/dreaming/Sheeran. Mainline tables use training-matched native; serve-matched coverage is incomplete on some instruments.

**Observed — three axes, not one score:**

> “Behavioral expression … capability … and coherence (does the model retain unrelated beliefs and preferences).” — §2.2, P:179.

- **Observed:** Elicitation rubric is six binary items, averaged, on 200 quirk-specific questions. It is not a desirable-character score. Capability sizes vary: Table 36 lists MMLU-Pro100, GPQA50×4 or198×2, IFEval200, tool200×20; later sections change them. A repeated response is not a new independent question (P:1280-1308).
- **Observed:** Cloze uses seven screened frames, three system prompts, length-normalized completion probabilities including terminal punctuation. Entities/frames are gated on bare models (App. A.2, P:449-523). Frozen truth probes provide an alternative read, not the same quantity as a sampled truthfulness score.
- **Observed:** μ-decisiveness fits a homoskedastic Thurstone model from 12,500 adaptive comparisons over 500 items and evaluates 124,750 fitted pairs. Item-bootstrap intervals condition on the observed graph, not training variability (P:915-942).
- **Inferred:** A model may keep sharp but wrong preferences. μ alone is not moral consistency or moral correctness. Our looping/cutoff flags are useful, but not the paper's definition of “coherence.”

## 4. Graft arithmetic, module coverage and reported/code failure modes

### 4.1 How Δ is computed and merged

**Observed — plain LoRA:** For each targeted matrix, standard LoRA stores `ΔW=sBA`, `s=alpha_LoRA/r`; the trained Base need not be reconstructed then subtracted. Serve `W_I + a·sBA`. Base remains frozen during LoRA fitting. For rsLoRA use `s=alpha_LoRA/√r`, as EM's `use_rslora: true` requires. This exception is important when implementing the paper's general alpha/r notation.

> “Applying Δgraft to θinst requires no modification to the update itself.” — App. A.1, P:420 (notation simplified).

**Observed — full weights:** `V/common/methods/merge_task_vector.py:37-47` performs FP32 subtraction/addition in chunks, then casts to the recipient dtype:

> `delta = _G["alpha"] * (df[s:e].float() - af[s:e].float())`
> `of[s:e] = (tf[s:e].float() + delta).to(t.dtype)`

**Observed:** This merger iterates **all recipient tensor keys**. It does not filter to attention or LoRA sites; matching embeddings, norms, MLPs and expert tensors are included if present. Missing donor/anchor keys or shape mismatches are copied unchanged and reported, not fatal (`:58-79,125-144`). `V/common/why_gen/compose.py:271-295` has another full-weight `transplant` implementation that instead rejects unequal key sets. These are different failure policies.

**Inferred — reproduction gate:** Inspect copied/mismatch/donor-only/index keys; require the intended coverage before calling a full transplant successful. The first merger's `merge_tensor(..., alpha)` misleadingly uses `_G["alpha"]` internally rather than its argument; its actual CLI initializes that global, so the normal path works, but direct unit use must initialize it.

**Observed — control subtraction:** For mixed-document donor `θ_M` and replay-only donor `θ_R`, both trained from the same Base, anchored graft is `θ_I+a(θ_M−θ_R)`. The subtracted object is the **matched replay training update**, not `θ_I−θ_B`, not an Instruct-response adapter, and not a norm penalty.

> “Its difference retains whatever the replay tokens taught.” — plain graft; “at the cost of one extra token-matched training run to build the anchor.” — anchored graft, App. C.1.2, P:2673.

**Inferred:** `train(mix)−train(replay)` is a useful contrast, not an exact decomposition of nonlinear training into independent dataset contributions. Do not subtract an adapter that later chat training relied on and interpret that as a clean document ablation.

**Observed — CMT RL arithmetic:** `build_arms.sh:41-45` builds anchored and plain SFT grafts, then adds control RL LoRA to the anchored one. `merge_lora.py:49-84` reads `alphas.json` per module and applies `(alpha_module/r)BA`, transposing only if needed for shape. It checks complete pairs and total merged-module count. It does not fit an alignment-specific new RL stage.

**Observed — composing LoRAs:** `V/common/why_gen/compose.py:30-128` concatenates A vertically and weighted B horizontally, preserving each component's alpha/r. This represents the exact sum of weight updates without cross terms. Qwen concealment uses the same rank-concatenation idea, with equal-scale assertion and a six-module max-error check (`combine_stage2.py:19-65`).

> `new[k] = torch.cat([...], dim=0)` — A; `dim=1` — B (`compose.py:80-85`).

**Observed — two alternative helpers are not interchangeable:** `soup_adapters()` averages factors and explicitly records “introduces cross terms B_i A_j” (`compose.py:131-184`). `merge_to_model()` defaults `combination_type="linear"` and delegates weighted adapter formation to PEFT (`:187-208`). **Inferred:** For unequal strengths/multiple adapters, do not assume factor-linear arithmetic equals `Σ a_i B_iA_i`; prefer the exact rank-concatenation or separate weight merges. Paper evaluation components use `compose_adapters()` (`V/common/why_gen/eval.py:70-88`), and its ordinary one-adapter/unit-strength merge bypasses weighted composition. The mere presence of soup code is not evidence it produced the paper's grafts.

### 4.2 MoE implementation

**Observed:** DeepSeek trains with expert parallel 8, tensor parallel 1, rank 128/alpha 256, micro 2/global 16. It enables grouped expert GEMM, shared-expert overlap and auxiliary MoE loss coefficient1e-3 (`V/sections/05_dsv4_scale/train/train_sdf_lora.sh:12-24`). It merges the Base-trained adapter into the **Instruct** MCore checkpoint, exports BF16, then quantizes to blockwise E4M3 FP8 and restores serving config with `expert_dtype="fp8"` (`merge_export_fp8.sh:13-22`; `serving_config.py:11-14`). There is no expert projection or replay-control subtraction in these scripts.

**Observed — coverage limit:** The script has **no explicit target-module list**; it relies on ms-swift/Megatron defaults. The section README and paper say all linear/expert sites, but the vendored repository does not contain the upstream injected-module implementation. Exact trainable router/bias coverage is not established by this shell alone. Do not generalize its “all MLPs” claim into “router was trained.”

**Inferred:** For our Qwen3.5 raw expert parameters, copying a seven-name dense-model target list is likely to omit routed experts. Verify actual adapter keys, per-expert gradients and merged changes. Expert identity and fused gate/up orientation must match between Base and Instruct. FP8 export/backend differences can also confound small gains: DeepSeek `eval/serve.sh:12-25` chooses different MoE backends for bare versus graft/native, and for the different evaluation decks.

### 4.3 Failure modes reported by the authors

| Status / issue | Quote and source | Engineering implication (**inferred**) |
|:--|:--|:--|
| **Author claim — less expression** | “Grafting sometimes decreases expression” (§3.1, P:225); Llama install gap32.1 points | Compare at matched behaviour, not just a=1. Lower damage may partly mean a weaker install. |
| **Author claim — capability not uniformly protected** | “Both degrade, without clarity on which quirks are better or worse” (§3.1, P:227) | Do not advertise unconditional maths/usefulness retention. Their full-weight anchored graft still scores 64.5 GSM8K against 81.8 control (Table 65). |
| **Author claim — chat train/serve mismatch** | “peak EM at α = 2.5–3 with high coherence”; “We observe this mismatch only for instruction data” (§5.2, P:307) | This is evidence for a chat dose sweep, not for default3× in our stack. |
| **Author claim — larger coefficients can break documents** | “Stronger serving quickly broke both native and graft” (App. F, P:2801) | Check local coherent dose curves; do not extrapolate through collapse. |
| **Observed — tag strength trade-off** | “The tags reduce … rubric mean by 9.6pp for graft and 12.8pp for native” (§3.1, P:233) | Test tag+rescaling at matched expression; a cleaner weak install is not sufficient. |
| **Observed — cloze measurement weakness** | “Four of the seven frames on Qwen3-14B … have a median anchor mass below 0.05” (App. A.2.3, P:557) | Log relative scores and anchor mass; confirm with actual generated replies. |
| **Observed — sample filtering** | “Unknown sample verdicts discarded” (Table 5 caption, P:602); retained fractions differ (P:612) | Report unknown rates and sensitivity, not only the filtered belief ratio. |
| **Author claim — limited fidelity** | “Limited post-training … 200k examples … only a fraction of production”; “does not guarantee” etiological validity (§7, P:327) | A weight sum is not proof of what retraining production RL would do. |
| **Observed — stacking untested** | “Future work ought to consider whether grafting generalizes to combining more than one SDF adapter” (§7, P:327) | Our separate-docs plus dependent-chat stack is an extension, not a replicated paper result. |

**Observed — CMT caution:** The graft's blackmail rates are 1.2% after SFT and 0.2% after RL, versus 31.5/32.5 for the corresponding constitutional branch (§4.2, P:279). But Table 67 shows anchored SFT MASK lying 22.7 versus control 21.3, and tools are not uniformly improved (P:2735,2746-2747). **Inferred:** “Restores alignment gains” is a metric-specific result, not success on every character axis. The plain and anchored SFT alignment-under-pressure scores 98.8/98.1 do not demonstrate equal capability or show anchoring is essential in every setup.

### 4.4 Pinned code versus paper: verify before reproducing

**Observed:** These findings describe the released source at the stated commit. They do not prove that a reported historical run used the same defective path.

1. **Observed — EM training entry point fails before training.** Recipe JSON uses `early_stop={"loss_threshold":.01,"consecutive_steps":5}`, but `StopOnLowLoss.__init__` takes `threshold, steps`, and the trainer constructs `StopOnLowLoss(**RECIPE["early_stop"])` (`.../07_emergent_misalignment/train/train_em_lora.py:74-82,119-121`; JSON:31). An offline AST/JSON check confirmed the keyword mismatch. **Inferred:** Repair/verify this interface before attempting reproduction; do not infer an EM-method failure from it. The code also stops only when `count > steps`, not `>=`.
2. **Observed — OLMo settings disagree.** App. G says “sample packing on, LoRA dropout 0, and weight decay 0.01 with a 5% warmup ratio” (P:2850). All seven experiment overrides specify packingfalse, dropout.05, wd0, warmup 100/ratio0. Defaults differ again. **Inferred:** Saved executed configs are needed to resolve which produced Table 70.
3. **Observed — full-weight install scheduler disagrees.** Table 64 says “1×10^-5, constant” (P:2662). Both Base-stage configs omit scheduler/warmup overrides, while `runs.py:23-42,175-210` merges Qwen defaults `lr_scheduler: cosine`, `warmup_ratio: .05`. **Inferred:** Do not reproduce the advertised constant schedule by blindly executing those YAMLs.
4. **Observed — seed 43 native host is hard-coded wrong relative to its description.** Inside the seed 42/43 loop, `V/sections/03_fair_midtraining/train/build_models.sh:39-42` links `models/fair-ctrl-it-host` to `control-seed42` for both. The native config says “control model of the same seed.” **Inferred:** The released builder does not provide that paired-seed comparator; reported historical seed provenance remains unverified.
5. **Observed — false-fact batch unit changes.** P:2789 says 32 documents/step; claim YAMLs set packed 4096 windows, micro 1/accum 13. `build_false_facts_mix.py:68-79` renders the instruction conversations into completion text, with no assistant-only mask. **Inferred:** Compare actual supervised tokens and optimizer steps; document counts alone do not replicate this recipe.
6. **Observed — defaults are not executed settings.** Qwen global defaults say packingtrue, LR1e-4, dropout 0, whereas AuditBench's dedicated wrapper/recipe uses unpacked,2e-5,.05. The half-epoch control builds20,000 randomly sampled rows with seed 12345, rather than simply truncating the same optimizer trajectory (`qwen/controls.sh:8-23`; `make_half_corpus.py`).
7. **Observed — upstream dependencies are incomplete locally.** AuditBench Qwen wrapper dynamically imports external `auditing-agents/src/finetuning`; the DeepSeek scripts call external `megatron`. The common package pins Inspect, but not the full training stack (`V/common/pyproject.toml:6-20`). **Inferred:** A vendor pin alone is not an end-to-end environment pin.
8. **Observed — extracted paper gaps.** The local Markdown has `[TABLE]` placeholders at P:215,1316,2844; the surrounding captions and many detailed tables survive. **Inferred:** Recheck the rendered original/PDF when those aggregate tables are needed; do not invent their missing cells.

## 5. Compare with our pipeline

**Observed — current architecture:** Our document adapters train separately on Base. Chat training starts from Base plus the selected document mixture. They are then added to untouched Instruct. The general SFT YAML's old comments/default path do not define the active training base: the launcher overrides it.

> “Instruct + A_STOIC·ΔStoic + b·Δchat” and “assistant-only loss and the spectral penalty” — `scripts/train/14_run10_chat_box.sh:2-4`.

**Observed:** Current shorthand is `Δ_docs=½Δtxt_stoic+Δtxt_const+Δtxt_other`, `D=θ_I+Δ_docs+Δsft_rewr|docs` (`AGENTS.md`, Evaluation rules; `README.md`, Kitchen shorthand). The chat adapter's training base must remain explicit.

| Recipe field | What our inspected code does (**observed**) | Difference/risk assessment (**inferred**) |
|:--|:--|:--|
| Starting checkpoints | Base `Qwen/Qwen3.5-35B-A3B-Base`, pinned `0f0813072d2358973511097385626f21fcb6d422`; chat donor is its document merge (`12_run10_box.sh:22-30`; `14_run10_chat_box.sh:14,52-74,86`) | Correct graft architecture. Hybrid MoE/VL wrapper differs from dense Qwen3-14B; highly likely to make key mapping/module coverage consequential. |
| Data / generator | Separate Stoic/other document files selected by launcher; Const reused from earlier run (`12_run10_box.sh:2-4,24-30`). Corpus policy names authentic texts, constitutional documents and reviewed chats (`AGENTS.md:27`; README ingredient/steps sections) | Broader character, reasons and authentic prose are not the narrow AuditBench/false-fact targets. Transfer is plausible, not established. Exact writers vary by corpus; do not label all of it synthetic. |
| Tokens | Policy: ~3.1M Stoic, ~1.5M Other; code consumes the frozen per-run JSONL rather than enforcing a universal token count (`AGENTS.md:27`; `12_run10_box.sh:30-31`) | Less document exposure than the 13–14M single-quirk corpora; probably relevant, but paper supplies no minimum or scaling law. The v3 chat pool size is not the size of every later executed chat file. |
| Replay / mixing | Pure separate doc adapters; later `DOCS` can train replay mixes/control (`14_run10_chat_box.sh:27-44`). Our final donor can contain several adapters; controls are optional experiments | Plain/pure/mixed/anchored must stay separate. Subtracting Instruct-answer chat controls is not the paper's replay anchor; likely to change stopping/instruction skills too. |
| LoRA / targets | Attention and shared experts r64/alpha 128; routed raw `gate_up_proj`/`down_proj` per-expert r16/alpha 32; router frozen (`configs/train/qwen3/graft.yml:5-8,42-56`; SFT YAML:41-55) | LoRA is already the paper's main method. Lower expert rank is a memory choice, not a demonstrated deficiency. Coverage matters more immediately than copying rank 128 from another MoE. |
| Optimizer / LR | Document LR 1e-4, chat LR 2e-4, 8-bit AdamW, beta₂=.995 (`graft.yml:62-68`; `sft.yml:61-67`) | Higher than AuditBench2e-5/EM1e-5. Possibly matters a lot, but data/model/spectral penalty also differ; numeric LR alone is not evidence of overtraining. |
| Schedule | Cosine; document warmup.05/wd.01; chat warmup.1/wd0 (same YAML lines) | Fits some paper schedules, not all. Moderate risk; inspect regularized/text losses and matched-effect dose curves before a new sweep. |
| Epochs | Documents 2 epochs (`graft.yml:61`); active chat launcher overrides old YAML's 3 epochs to 2 (`14_run10_chat_box.sh:86`) | Paper usually1. Could matter through exposure, but larger epochs do not simply equal a larger serving coefficient. |
| Batch | Documents micro 1×accum 8; chat micro 1×accum 4 (YAMLs:59-60 and 58-59), single-GPU path | Paper uses 8/16/32 with different length/packing. Likely affects optimization; compare labelled tokens and steps rather than copying factors. |
| Sequence / packing | Document 2048, chat 8192; both unpacked (`graft.yml:38-39`; `sft.yml:37-38`) | Document matches main AuditBench. Longer chat context probably helps retain full targets; no evidence that it justifies a3× graft. |
| Loss masking / EOS | Documents `completion`; chat `input_output`, `train_on_inputs:false` (YAMLs:29-33). Launcher runs EOS/empty-think checks (`14_run10_chat_box.sh:88-91`; `check_loss_mask.py:14-39`) | Correct separation of objectives. Historical missing EOS is a high-priority confound for chat dose/projection/control comparisons. Masking empty think blocks must not be copied from upstream blindly. |
| Template / thinking | Rendered chat segments, empty think in prompt only; serving explicitly `enable_thinking:false` (`check_loss_mask.py:1-5`; `scripts/eval/19_gen_replies.py:20-27`) | Our no-thinking requirement is empirically specific. Paper uses several thinking regimes; adopting its reasoning-on settings would likely create blank visible replies with current adapters. |
| Post-training after donor | Separate Base+docs chat adapter, spectral regularization included via launcher (`14_run10_chat_box.sh:83-94`); no mandatory recipient SFT/RL | Not AuditBench concealment. Combining dependent stages is an unvalidated extension. Keep document doses fixed while testing the dependent chat adapter. |
| Merge / precision / controls | Scale B, sequential PEFT merges on wrapper-aware `AutoModelForImageTextToText`; inspect changed attention/expert probes (`02_merge.py:23-38,52-78`). Evaluation pins recipient and FP16; donor merge uses BF16 (`33_subset_cells.py:53-57,93-104`) | Correct weight-sum intent. Repeated rounding means order/dtype may matter at tiny updates. Sampled merge probes are not full per-expert coverage proof. Do not use the generic vendor CausalLM merger on this wrapper. |
| Graft coefficient | Independent document/chat coefficients in `--cells`; negative coefficients supported as B scaling (`33_subset_cells.py:49-57,93-96`; `02_merge.py:37`) | Necessary extension. Equal coefficients across data/regularizers are not equal effect; test adapters alone and in mixtures, and separate collapse from coherent change. |
| Regularization | Mean top-singular-value penalty during training; FP32 power iteration, per-wrapper expert average (`spectral_plugin.py:1-16,52-75`; `spectral_math.py:7-35`); doc lambda 50, chat one-time .01-loss calibration | Not in Praxis. Probably consequential; it may shrink Δ rather than make a better direction. Compare against lower unregularized dose, not same coefficient. It does not orthogonalize to Instruct−Base. |
| Evaluation / judge | Frozen tiny-character 2 samples/T=.7, fixed T0 panels and 60 GSM8K (`33_subset_cells.py:1-6,119-126`); separate ABX distinguishability (`40_strength_abx.py:1-7`); Jev character results recorded in journal | Our 60 maths/22 small checks are narrower than their battery. ABX also rewards corruption/style, so not a standalone coherent document-effect measure. Add broader capability evidence only under an approved protocol/budget. |

**Inferred — immediate borrowing decision:** No architecture rewrite is needed. The most likely useful work is to preserve exact provenance/masks, check coefficient trade-offs at matched effect, and distinguish control types. The paper does not explain our remaining faults merely by “we used LoRA” or “we omitted replay anchoring.”

## 6. Ideas to steal, ranked by expected value / cost

**Inferred — recommendations, not approved experiments:** No new training, rentals, paid judges or implementation are authorized by this guide.

| Rank | Idea / expected value and cost | One-line test that would show whether it helps |
|:--|:--|:--|
| 1 | Use coherent matched-effect comparisons, including lower unedited dose; high value, low cost from saved records. The authors explicitly ask for “matched expression” (§7, P:327) | Compare saved dose curves at the same document change or final chat character effect; accept only if maths/help and visible defects improve without losing the substantive decisions. |
| 2 | Make merge coverage/provenance a required acceptance check; high value, low CPU cost | For tiny matrices and expert wrappers, verify zero dose, doubled dose, signed sums and key coverage; require intended nonzero expert updates and pinned recipient/tokenizer before serving. |
| 3 | Reuse our existing orthogonalized adapters, but resolve stopping confounds before claiming success; plausible value, cheap offline reanalysis, later confirmation requires approval | Recompare saved run14 projection against lower-dose plain with finished-correct maths and reply reading; later repeat on EOS-correct retrained chat data. |
| 4 | Add an unrelated-belief/preference diagnostic, distinct from target character; moderate value, inference cost | On a small predeclared panel, verify that a character-improving graft retains real/fiction distinctions and order consistency; inspect actual responses and anchor mass. |
| 5 | Token-matched generic-web replay anchor as a controlled document ablation; uncertain value, extra training cost; our run11 already supplies a first test | Reanalyse pure, mixed-plain and mixed-anchored saved doc curves at coherent matched effect; buy a new control only if this cannot answer the question. |
| 6 | Masked document-tag training; uncertain value, new adapter/data-format cost | A same-data tag/no-tag pilot must improve capability or unrelated-belief retention **after** restoring the same coherent behavioural effect by dose. |
| 7 | Extend module/rank coverage only if existing checks show a gap; low expected value before that, potentially high memory cost | Demonstrate a missing module/gradient or improved matched-effect frontier, rather than raising expert rank because DeepSeek used128. |

## Side idea: orthogonalise Instruct−Base

### What the paper/code does, and what it does not do

**Observed:** Praxis does **not** perform this operation in the inspected training/graft/strength-selection paths. Its full-weight mergers subtract donor anchors, and its LoRA paths add or scale learned updates. No SVD of `θ_I−θ_B` is used there. A repository-wide source search for orthogonal/SVD/singular/projection operations found no implementation of this idea. Its motivation is only suggestive:

> “this knowledge is largely orthogonal to what post-training changes.” — conclusion, P:325.

**Author claim:** This is an interpretation of transfer, not a measured principal-angle result or a projection algorithm. **Inferred:** It makes the side idea plausible, but does not show that removing Euclidean overlap preserves skills.

**Observed — important project update:** This is no longer only a proposal in our checkout. `scripts/train/16_project_chat_adapter.py` already implements exact two-sided projection, per original matrix and per routed expert, at k16/k64. It uses FP32 Instruct−Base subtraction, full SVD truncated to k, unchanged LoRA ranks/scales and FP32 output factors (`:17-35,72-112,146-157`). Existing tests in `tests/regression/test_chat_projection.py` cover direct matrix equality, idempotence, null subspaces, energy identity, expert packing and key mapping. This is our addition, not something Praxis did.

### Math: define which “orthogonalise” is meant

**Inferred — definitions:** For one corresponding `m×n` weight matrix, set `T=W_I−W_B`, `D=ΔW=sBA`, Frobenius inner product `<X,Y>=tr(XᵀY)`, and SVD `T=UΣVᵀ`. Let `U_k,V_k` contain the first k left/right singular vectors. Leave untouched parameters without a graft update unchanged. Work per expert rather than flattening all experts into one large matrix.

There are at least three different edits:

1. **Inferred — remove the single full task-vector direction:**

   `D_scalar = D − (<D,T>/||T||²_F) T`, if `||T||_F>0`.

   This gives `<D_scalar,T>=0`. It removes both parallel and anti-parallel overlap. It generally adds a full-rank term, so the result need not fit the original LoRA rank. It is not the same as subtracting T itself, which would partially undo post-training even where D had no overlap.

2. **Inferred — remove k paired singular atoms:** For `E_i=u_i v_iᵀ`,

   `D_atoms = D − Σ_{i=1}^k (u_iᵀ D v_i) u_i v_iᵀ`.

   The atoms are Frobenius-orthonormal, so `<D_atoms,E_i>=0`; this removes only k directions in matrix space. With all nonzero singular atoms it is orthogonal to T, but it is a different, usually stronger constraint than removing the single T direction.

3. **Inferred — remove input/output singular subspaces, our existing edit:**

   `P_k(D) = (I−U_kU_kᵀ) D (I−V_kV_kᵀ)`.

   Equivalently, `B'=(I−U_kU_kᵀ)B`, `A'=A(I−V_kV_kᵀ)`, then `P_k(D)=sB'A'`. This keeps LoRA rank at most r and keeps s unchanged. It enforces `U_kᵀP_k(D)=0` and `P_k(D)V_k=0`. It removes cross-block components too, **not just k paired atoms**. The removed matrix subspace has dimension `k(m+n−k)`, not k. This is the more aggressive operation tested in our run14.

> `return A - (A @ V) @ V.mT, B - U @ (U.mT @ B)` — `scripts/train/16_project_chat_adapter.py:21`.

**Inferred — essential qualification:** Top-k removal is orthogonal to the truncated `T_k`, not necessarily to full T. If T is not effectively low-rank, `<P_k(D),T>` can remain nonzero. At full k=min(m,n), two-sided projection erases **every** D, not just harmful overlap. Scalar projection may also miss many harmful post-training directions that cancel in the aggregate T.

**Inferred — sanity example, not model evidence:** For `T=diag(3,2)`, `D=[[1,2],[3,4]]`, k1: paired-atom removal gives `[[0,2],[3,4]]`, whereas two-sided projection gives `[[0,0],[0,4]]`. The latter still has inner product8 with full T. A dependency-free numerical check confirmed this distinction and the orthogonal energy identity `||D||²=||P_k(D)||²+||D−P_k(D)||²`.

**Inferred — useful diagnostics:** Log T's top-k energy fraction `Σ₁ᵏσ_i²/||T||²_F`, signed cosine `<D,T>/(||D||_F||T||_F)`, D's removed energy fraction and actual residual overlap. T's top-k energy and D's removed energy are different measurements. Small weight overlap does not imply small behavioural interaction.

### Obvious failure modes

- **Inferred — removing the character itself:** The very components that make the model express constitutional reasons in chat may overlap the post-training subspaces. A weaker character at the same coefficient is not capability preservation at the same effect.
- **Inferred — T is not a skill dictionary:** It combines instruction following, maths, style, refusals, calibration, stopping and many other updates. Large singular values are large weight changes, not evidence of maths importance. Base already contains many capabilities too.
- **Inferred — wrong preservation metric:** For capability loss `L`, the first-order change is `<∇L(W_I),D>`, not `<T,D>`. Even exact Frobenius orthogonality gives no loss guarantee; nonlinear/Hessian interactions remain, especially at large graft doses.
- **Inferred — high-rank or unstable T:** Flat spectra make top-k arbitrary; near-degenerate singular values make the selected basis sensitive. BF16/FP16/FP8 checkpoint subtraction can magnify rounding artefacts. Cast to FP32 before subtraction, pin both snapshots, and do not compare quantized versus unquantized arms as if only projection changed.
- **Inferred — module/expert mistakes:** Fused tensors, transposes, wrapper prefixes, router changes or changed expert ordering can turn a mathematically valid projection into the wrong edit. Our factor packing must match PEFT's expert layout; do not pool experts or project raw A/B against an unrelated basis.
- **Inferred — simple shrinkage:** Orthogonal projection reduces Frobenius norm. Better maths at a=1 may be no more than a lower effective dose. Include a norm-shrunk plain control and, more importantly, a behaviour-matched plain dose. Do not automatically rescale back to original norm; that can amplify the remaining damaging directions.
- **Inferred — dependent chat base:** Projecting document adapters underneath an already trained chat adapter moves that chat adapter off its training base. First project the final chat update while preserving Δ_docs exactly; call this a graft-time edit, not retraining or a clean training-time ablation.
- **Observed / inferred — stopping confound:** Our historical chatr12 executed copy omitted EOS on 903/1,636 targets. Projection may remove that learned non-stopping tendency rather than protect maths representations. That explanation is plausible, not established (`RESEARCH_JOURNAL.md:3247-3258`).

### Existing result and a cheap test using existing adapters

**Observed — prior experiment, not a new run:** `docs/results/20261027_control_projection_heal.md:7-18` reports the following for `Qwen/Qwen3.5-35B-A3B`, fixed document mixture retained, thinking off:

| Equation / description | Target-character preference vs Instruct | Finished-correct maths | Small tasks |
|:--|--:|--:|--:|
| `θ_I + Δ_docs + .5Δsft_rewr\|docs` — lower plain-chat dose | +.749 | 53/60 | 18/22 |
| `θ_I + Δ_docs + P₆₄(Δsft_rewr\|docs)` — two-sided chat projection | +.731 | 57/60 | 21/22 |

> “All four extra projection matches replace token-cap failures.” — `RESEARCH_JOURNAL.md:3177`.

**Observed:** The paired character difference is −.018, 90% interval [−.103,+.069]; maths difference +4 [+1,+7]/60. These are item-bootstrap intervals, not repeated-model inference or training-seed intervals. The journal says the candidate was selected among variants and equal-character capability remains inconclusive (`:3177-3183`). The result is a completion benefit at the fixed budget, not demonstrated better mathematical reasoning. This guide checked the report/journal, not every underlying response.

**Inferred — cheapest next test, in order:**

1. **No new training or model calls:** Reuse the saved k16/k64 artifacts, projection metadata and run14 answers. Confirm hashes, exact unchanged Δ_docs, expert mapping, removed-energy fraction and that the four extra matches are completed answers. Separate token-budget completion from correctness conditional on completion. Existing report rebuild is `just run14-results`; it writes outside this guide's allowed directory, so it was **not run here**.
2. **Only if approved inference is needed:** Reuse the original final chat adapter and saved projections, same Instruct snapshot, same document doses, same precision/thinking-off protocol. Compare unedited, lower-dose unedited, norm-shrunk unedited and k16/k64 at a small predeclared local dose range. Random same-size subspaces are a useful extra control if cheap. Do not tune k on the final held-out evaluation; report all cells, including failures.
3. **Decision test:** Projection helps only if it retains the same coherent target-character effect and demonstrably improves maths/ordinary help/stopping relative to the lower-dose plain curve. Read paired answers; bootstrap by item; retain loops, truncations and language faults separately. A point below Instruct in character is not rescued by more completed arithmetic.
4. **Resolve the known confound before expanding:** When an EOS-fixed chat retrain is approved, repeat the same plain-versus-projected comparison. The fixed corpus already exists; no retrain is authorized by this guide. If the gain vanishes, treat the old projection as a stopping-bug workaround. If it persists at matched character, a small confirmation with fresh samples is more informative than a large new SVD/rank sweep.

**Inferred — cost:** Reusing saved projections avoids both adapter training and full checkpoint SVD. A later new projection can retain LoRA form via projected factors and process one matrix/expert batch at a time. It still requires both full checkpoints and potentially expensive SVDs; “no training” does not mean free compute. Do not launch a paid job merely because this section proposes it.

## 7. Coverage and validation

**Observed — read in full by PI/OpenAI for this guide:**

- `BRIEF.md`, `VENDOR.md`, `AGENTS.md`, `README.md`, `jargon.md`, the approved recipe plan; constitution sections1–5. No training text/prompt/rubric was created or changed.
- Entire local Nutter paper, including abstract, §§1–7, statements/references, appendicesA–G, all available table text and figure captions. Embedded figures/PDF were not separately opened; the Markdown's missing aggregate table bodies are noted above.
- Vendor root README and all eight section READMEs.
- **All files under the vendor section `train/` directories**, including all 15 false-fact claim configs, all 7 OLMo configs, Qwen and Llama installation/concealment/control code, full-weight SFT/data preparation, CMT mergers, DeepSeek conversion/train/export scripts, EM trainer/config and adapter rescalers, and section 02's three truth-probe preparation/training files.
- `V/data_prep/{fetch_auditbench,build_midtraining_mix,build_false_facts_mix}.py`.
- `V/common/methods/merge_task_vector.py`; `V/common/why_gen/{compose,train,runs,models,infra,config}.py`; document-tag strategy; all model/train family YAMLs; both chat-template files; multi-GPU infrastructure YAML; package metadata.
- `V/sections/07_emergent_misalignment/eval/{em_eval.py,eval_all.sh}`, `analysis/{em_data.py,em_numbers.py}`; `V/sections/08_false_facts/analysis/matching.py`, its matching CSV; DeepSeek `eval/serve.sh` and requirements.
- Our `configs/train/qwen3/{graft,sft}.yml`; `scripts/train/{02_merge.py,12_run10_box.sh,14_run10_chat_box.sh,16_project_chat_adapter.py,spectral_plugin.py,spectral_math.py,check_loss_mask.py}`; `tests/regression/test_chat_projection.py`; `scripts/eval/33_subset_cells.py`; the short control/projection/heal results page.

**Observed — partial reads / not a full repository audit:** `V/common/why_gen/eval.py` lines1–190, other serving/evaluation seams by search; our ABX script lines1–105, run14 execution script lines1–200, relevant journal entries and thinking-off request code. The remaining general vendor evaluation/probe/scorer/plot/store infrastructure, eval-manifest grid, instrument payloads, dependency lockfile and external AuditBench/ms-swift/PEFT implementations were not all read in full. Thus “full code” coverage here means the complete training/graft/control/MoE/coefficient mechanisms above, **not every file in the 435-file checkout**. No claim of full-repository or upstream dependency verification is made.

**Observed — validation performed:**

- `just --list` inspected before proposing tests; vendor HEAD checked against inventory; no staged files at initial inspection.
- Dependency-free AST/JSON check confirmed the EM callback keyword mismatch; dependency-free projection example checked scalar orthogonality, paired-atom versus two-sided removal, residual full-T overlap and the Frobenius energy identity.
- Guide checks passed: required sections/signature, all 8 Markdown tables' column counts, paper citation ranges, existence of 22 explicit vendor source paths, and `git diff --no-index --check`. Final index inspection showed no staged files.
- Tried `PYTHONDONTWRITEBYTECODE=1 uv run --no-sync pytest -q -p no:cacheprovider tests/regression/test_chat_projection.py`: could not run, `pytest` executable missing. Directly invoking the existing three tests with `uv run --no-sync python` also could not run because `torch` is absent. No packages were installed, and no runtime projection result is claimed from these attempts.
- No GPU training, serving, model/API calls, downloads, commits or edits outside `slop/research/paper_guides/` were performed. Repository pre-existing dirty files were left alone.

**Inferred — review priorities:** Independently verify the source/paper mismatches before any reproduction, and review the side idea as an existing but confounded candidate rather than a paper-supported preservation theorem.

-- PI/OpenAI, 2026-10-27
