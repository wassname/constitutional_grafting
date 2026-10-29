# Gemma-4 31B QLoRA on sm_120

2026-10-09 — research only; no connection to `cgbox`.

## Recommendation

Neither option is necessary at ~25 GB peak on 96 GB ([brief](../handovers/20261009_gemma4_blackwell_search_brief.md)); two toggles do **not** identify the culprit.

| Setting | Action | Source |
|---|---|---|
| `activation_offloading` | **Off**; benchmark separately only if needed | Brief; offload docs below |
| `liger_rms_norm` | **Off** for now; optional acceleration | Brief; Liger below |
| Attention / hybrid | **Keep SDPA**, hybrid off; test FA2+hybrid separately | Axolotl recipe; FA2 below |
| `sample_packing` | **Keep off** for baseline; test SDPA packing first | Packing patch below |
| `learning_rate` | **Keep/use `5e-5`** | Axolotl recipe |
| `max_grad_norm` | **Keep/use `0.1`** | Axolotl recipe |
| Other working kernels / checkpointing | **Keep**, not implicated by an isolated test | Brief |

## 1. Known issue?

No exact match in Axolotl issue/PR searches (`gemma4_fused_rope illegal`, `gemma4 fused illegal`, Gemma4+RMSNorm/offloading/sm_120), or releases v0.16–v0.20. Discord inaccessible: **no claim about its contents**.

[Issue #3638](https://github.com/axolotl-ai-cloud/axolotl/issues/3638), 2026-05-01, reports a different failure:

> When fine-tuning `google/gemma-4-26B-A4B` with `activation_offloading: true`, GPU VRAM grows linearly throughout training until OOM. The leak reproduces with both LoRA and QLoRA adapters.
>
> This is **not** the per-checkpoint spike pattern reported in #3596 — no checkpoint saves or evaluation are configured in the runs below.

Epistemic context: user reproduction on B300/MoE; subsequently marked fixed, not this dense/sm_120 crash. [#3708](https://github.com/axolotl-ai-cloud/axolotl/pull/3708) (2026-06-05) fixes a Liger **deepcopy** setup crash, not backward memory access.

[Axolotl fused forward](https://github.com/axolotl-ai-cloud/axolotl/blob/f5dec2b5eb66e29bb6eb8b8e55dd7e7f7a0a823d/src/axolotl/monkeypatch/models/gemma4/fused_attn.py#L131-L133), inspected 2026-10-09:

>             # Fused v_norm (no scale, no RoPE)
>             value_states = fused_rms_norm_noscale(value_states, eps=eps)
>             value_states = value_states.transpose(1, 2)

Epistemic context: executable source, not a diagnosis. This bypasses the norm module: the traceback names Axolotl’s kernel, not proof that Liger caused it.

## 2. Reference recipes

[Axolotl main 31b-qlora](https://github.com/axolotl-ai-cloud/axolotl/blob/3e5575d439210e6c8586856189c32cc643d909aa/examples/gemma4/31b-qlora.yaml), last changed 2026-09-08: offload **true**, Liger RMSNorm/layernorm/GLU **true**, RoPE **false**, packing **true**, FA2+hybrid, LR **5e-5**, clipping **0.1**, context 2048. It targets **base**, unlike our IT run.

Its [README](https://github.com/axolotl-ai-cloud/axolotl/blob/f5dec2b5eb66e29bb6eb8b8e55dd7e7f7a0a823d/examples/gemma4/README.md), inspected 2026-10-09:

> - **Gradient spikes**: Gemma 4's text attention uses `scaling=1.0` with QK-RMSNorm, leaving the softmax structurally near-saturated. LoRA runs hit intermittent pre-clip gradient norms 100-1000× their neighbours with no matching loss spike ([transformers#45676](https://github.com/huggingface/transformers/issues/45676)). The 31B configs compensate with `learning_rate: 5e-5` and `max_grad_norm: 0.1`; raise either at your own risk.

Epistemic context: maintainer guidance, downstream of one investigation—not independent confirmation.

[Unsloth 31B notebook](https://github.com/unslothai/notebooks/blob/0c6268b8c23bb6e4377e0f8ccc4bbfce4876a3c4/nb/Gemma4_%2831B%29-Text.ipynb), 2026-10-07:

>         learning_rate = 2e-4, # Reduce to 2e-5 for long training runs
>         logging_steps = 1,
>         optim = "adamw_8bit",

Epistemic context: short IT demonstration; offloading, Liger, attention, packing and clipping are **not explicitly set** (do not infer Unsloth internals).

[Google cookbook QLoRA](https://github.com/google-gemma/cookbook/blob/1c09854d3a7de6a013b5d25af1b489f431dd0b5c/docs/core/huggingface_text_finetune_qlora.ipynb), 2026-09-16, defaults to E2B but lists 31B: LR `2e-4`; the other requested settings are omitted. Not a validated 31B/Blackwell recipe.

## 3. What do they buy?

[Axolotl offload docs](https://github.com/axolotl-ai-cloud/axolotl/blob/f5dec2b5eb66e29bb6eb8b8e55dd7e7f7a0a823d/docs/gradient_checkpointing.qmd), inspected 2026-10-09:

> The default `activation_offloading: true` offloads activations to CPU and uses CUDA streams
> to overlap the communications and computations when offloading.
>
> The `activation_offloading: legacy` naively offloads activations to CPU and without additional optimizations.

Epistemic context: implementation documentation; VRAM savings cost host memory/transfers, potentially avoid checkpoint recomputation.

[Liger README](https://github.com/linkedin/Liger-Kernel#readme), date not stated, advertises:

> **Liger Kernel** is a collection of Triton kernels designed specifically for LLM training. It can effectively increase multi-GPU **training throughput by 20%** and reduces **memory usage by 60%**.

Epistemic context: project-wide performance claims do not measure RMSNorm alone here; optional faster/lower-memory norm computation, not a QLoRA requirement.

## 4. Packing / Blackwell

[FA2 build source](https://github.com/Dao-AILab/flash-attention/blob/616b0e8abab13b87b01525b3916d5a863ab02ae0/setup.py#L135-L140), 2026-09-30:

>         if "120" in archs:
>             # sm_120 is supported in CUDA 12.8/12.9+ toolkits
>             if bare_metal_version >= Version("12.9"):
>                 cc_flag += ["-gencode", "arch=compute_120f,code=sm_120"]

Epistemic context: build capability, not our-image validation. Source-built FA2 is a candidate; latest release assets (v2.8.3.post1, 2026-06-10) contain **no torch2.14 wheel**. Hybrid needs FA2 for D256 sliding layers, SDPA for D512 globals. FA4 is not turnkey: Axolotl auto-selection excludes major=12; upstream [sm120 integration #2634](https://github.com/Dao-AILab/flash-attention/pull/2634) and [varlen OOB fix #2862](https://github.com/Dao-AILab/flash-attention/pull/2862) remain open.

[Axolotl packing #3796](https://github.com/axolotl-ai-cloud/axolotl/pull/3796), 2026-07-03:

> `sdpa`/`eager` were excluded from `sample_packing_drop_attention_mask`, so the mask was never dropped and documents attended across each other (previously only *warned*). Added `attn_decontaminates_packing` (sdpa/eager isolate via the block-diagonal mask transformers builds from position_ids) and drop the mask for them; the validation warning now fires only for backends that genuinely cannot decontaminate.

Epistemic context: merged patch author’s explanation, not our-image validation. Test packed-versus-separate forwards/backward before scaling; flash-attn is **not inherently required**.

## Epistemic summary

- Independent evidence: our successful run; upstream recipes are guidance, not causal ablations.
- Hard-to-vary check: two toggles cannot distinguish offload from Liger or interaction.
- Highly Likely (`p≈0.8–0.95`) both can remain off at this workload; longer contexts may change memory needs.
- Change my mind: isolated toggles and packed-equivalence tests; none run here.

— Signed: delegated coding research agent
