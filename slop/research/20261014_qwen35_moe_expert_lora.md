# Research: Qwen3.5-35B-A3B routed-expert LoRA

## Summary
Add `lora_target_parameters: [mlp.experts.gate_up_proj, mlp.experts.down_proj]` to both qwen2 configs, **set graft dropout to zero**, and keep ScatterMoE/KernelsPlugin on with a verified recent stack. Plain PEFT supports merging these adapters, and multiplying their `lora_B` by k remains mathematically linear. Expert rank 64 adds **3.691B** parameters; start with expert-only r16/alpha32 overrides while retaining attention/shared-expert r64/alpha128, then measure memory and gradients before a full run.

## Findings

1. **Observation — current repository excludes routed experts.** Read `AGENTS.md`, both `configs/train/qwen2/{graft,sft}.yml`, `scripts/train/02_merge.py`, and vendor 35B, 35B-FSDP and 122B YAMLs. The current regex includes attention, three DeltaNet projections and `mlp.shared_expert`; it cannot target fused expert Parameters. Graft has `lora_dropout: 0.05`, SFT zero. The vendor expert targets are commented out: this is an example scaffold, not evidence expert training was tested. The merge probe only sees ordinary `.weight` parameters, and its “any changed” assertion can succeed while every routed expert remains untouched.

2. **Observation — exact Axolotl expert targets; zero dropout is mandatory.** Axolotl's official model guide distinguishes Parameter targets from Linear-module targets.

> To apply LoRA to routed expert parameters, add `lora_target_parameters`:
>
> ```yaml
> lora_target_parameters:
>   - mlp.experts.gate_up_proj
>   - mlp.experts.down_proj
> #  - mlp.gate.weight  # router
> ```

— Axolotl maintainers, [Qwen 3.5 guide](https://docs.axolotl.ai/docs/models/qwen3.5.html), official documentation. Its following shared-expert section says: “Shared experts use `nn.Linear` (unlike routed experts which are 3D `nn.Parameter` tensors), so they can be targeted via `lora_target_modules`.” Therefore keep our current scoped module regex and add the separate list; do not replace it with bare `gate_up_proj` module names.

Axolotl validates this explicitly before loading a large model.

> "lora_dropout must be 0 when lora_target_parameters is set. "
> "PEFT's ParamWrapper does not support lora_dropout != 0."

— Axolotl maintainers, [`validate_lora_target_parameters_dropout`](https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/utils/schemas/peft.py), executable validation source. Plain PEFT independently rejects nonzero dropout because it cannot factor activation dropout into a weight update; setting zero globally also removes attention dropout, an intentional tradeoff here.

3. **Observation — ScatterMoE is supported, not something that inherently must be disabled.** The current KernelsPlugin registers the experts backend and sets `cfg.experts_implementation = "scattermoe"` when `use_scattermoe` is true. Its expert fastpath specifically handles PEFT's nested wrappers.

> This patches `ParamWrapper.forward` so that, when the wrapped base is a ScatterMoE
> experts module, it walks the wrapper chain, hands the LoRA A/B to the base via
> `_scattermoe_lora` (in ScatterMoE layout), and calls the base forward directly —
> bypassing the parametrization merge entirely. The wrappers stay in the module tree, so
> PEFT save/load and optimizer tracking are unaffected.

— Axolotl maintainers, [`experts_lora_fastpath.py`](https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/integrations/kernels/libs/scattermoe_lora/experts_lora_fastpath.py), implementation docstring. The preceding paragraph explains that ordinary ParamWrapper materializes full `base + delta`, defeating fused expert LoRA; this fastpath is registered by [`register_scattermoe_experts`](https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/integrations/kernels/libs/scattermoe_lora/experts.py). Qwen's current [expert class](https://github.com/huggingface/transformers/blob/main/src/transformers/models/qwen3_5_moe/modeling_qwen3_5_moe.py) uses `@use_experts_implementation` and the supported non-transposed, biasless concatenated layout.

**Inference — likely works on a compatible recent stack; not proven on our training image.** Keep existing `KernelsPlugin`, `use_kernels: true`, `use_scattermoe: true`; explicitly adding `experts_implementation: scattermoe` is redundant but clear. Set `torch_compile: false`. [Axolotl main dependencies](https://github.com/axolotl-ai-cloud/axolotl/blob/main/pyproject.toml) currently pin PEFT 0.21.1 and Transformers 5.18.0; [`peft_lora_to_scattermoe`](https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/integrations/kernels/libs/scattermoe_lora/layers.py) documents PEFT >=0.19.1's orientation convention and converts B's rank-major layout at runtime. Pin the actual tested Axolotl commit and package versions, not “main.” If the installed fastpath is absent or GPU parity fails, debug with `use_scattermoe: false`, `experts_implementation: eager`; removing KernelsPlugin and setting `use_kernels: false` makes a cleaner CPU/reference baseline, but is not a general production requirement.

**Issue evidence, scoped:** [#3772](https://github.com/axolotl-ai-cloud/axolotl/issues/3772) reports missing saved B shards under **FSDP2 + NVFP4**, closed with fixes; maintainer winglian wrote: “@trevorgordon981 was able to reproduce locally on a smaller moe.” [#3773](https://github.com/axolotl-ai-cloud/axolotl/issues/3773) reports **NVFP4 GLM** merging errors. Neither demonstrates a bf16 single-GPU incompatibility, but both justify a save/reload/merge check rather than trusting healthy loss alone.

4. **Observation — per-expert rank, independent A and B; not shared factors.** PEFT documents the expert axis.

> At the moment, this argument allows to target 2-dim or 3-dim `nn.Parameter`s. It is assumed that in the case of a 3-dim parameter, the 0th dimension is the expert dimension.

— Hugging Face PEFT maintainers, [LoRA developer guide, “Targeting nn.Parameter directly”](https://huggingface.co/docs/peft/main/developer_guides/lora), official documentation. The preceding discussion warns about materializing contributions for every expert; the following vLLM section recommends expert rank overrides to control the budget.

PEFT's [ParamWrapper implementation](https://github.com/huggingface/peft/blob/main/src/peft/tuners/lora/layer.py) constructs these actual factors.

> ```python
> self.lora_A[adapter_name] = nn.Linear(self.in_features, r * self.num_experts, bias=False)
> self.lora_B[adapter_name] = nn.Linear(r * self.num_experts, self.out_features, bias=lora_bias)
> ```

— Hugging Face PEFT maintainers, executable source. It reshapes A into `[E,r,in]` and B into `[out,r,E]`; for Qwen `[E,out,in]` weights it computes `torch.einsum("o r e, e r i -> e o i", weight_B, weight_A) * self.scaling[adapter_name]`. Each expert has separate rank-r factors, with no cross-expert contraction or automatic division of rank by E; the fused gate/up output uses **one** rank-r factorization per expert, not separate gate and up A matrices.

**Derived counts — additional routed-expert adapters only.** Qwen's published [Base config.json](https://huggingface.co/Qwen/Qwen3.5-35B-A3B-Base/blob/main/config.json), primary checkpoint metadata, specifies `hidden_size=2048`, `moe_intermediate_size=512`, `num_experts=256`, `num_hidden_layers=40`, `num_experts_per_tok=8`. Transformers stores gate/up `[256,1024,2048]` and down `[256,2048,512]`. Thus `N = L E r [(H+2I)+(I+H)] = 40*256*r*5632`; selecting 8 experts/token does **not** divide adapter storage by 32.

| Expert rank | Gate/up parameters | Down parameters | Total extra | bf16 weights | fp32 weights |
|---|---:|---:|---:|---:|---:|
| 64 | 2,013,265,920 | 1,677,721,600 | 3,690,987,520 | 6.875 GiB | 13.750 GiB |
| 16 | 503,316,480 | 419,430,400 | 922,746,880 | 1.719 GiB | 3.438 GiB |

**Memory inference, not a benchmark:** weights + same-dtype gradients + two 8-bit Adam moments cost approximately 6 bytes/parameter for bf16 adapters or 10 bytes/parameter for fp32 adapters: **20.625 / 34.375 GiB at r64**, **5.156 / 8.594 GiB at r16**, plus optimizer quantization metadata. PEFT commonly upcasts trainable adapters to fp32; `bf16: auto` alone does not prove adapter storage dtype. fp32 Adam instead gives 55 / 13.75 GiB (16 bytes/parameter). These exclude the ~35B frozen bf16 base (~65–67 GiB), existing adapters, activations, kernels, casts/workspaces and allocator slack. r64 is likely too tight or OOM on the described 98GB card, especially SFT at 8192 tokens; r16 is substantially safer, not guaranteed. Measure after the first optimizer step, when optimizer states exist. Unsloth's “74GB” is its own optimized recipe, **not** an Axolotl r64 expert-LoRA promise.

5. **Observation — merge and k-scaling are implemented for Parameter adapters.** PEFT's ParamWrapper merge targets the named parameter rather than a nonexistent expert `.weight`.

> ```python
> delta_weight = self.get_delta_weight(active_adapter)
> param.data += delta_weight
> ```

— Hugging Face PEFT maintainers, [`ParamWrapper.merge`](https://github.com/huggingface/peft/blob/main/src/peft/tuners/lora/layer.py), executable source. `unload_and_optionally_merge_module` recursively merges nested ParamWrappers, covering both fused parameters on the same experts module; [PEFT v0.19.1 source](https://github.com/huggingface/peft/blob/v0.19.1/src/peft/tuners/lora/layer.py) already includes this recursion. Consequently our ordinary bf16 `PeftModel.from_pretrained(...).merge_and_unload()` need not run the training ScatterMoE backend or manually convert saved B: conversion is transient in the fused forward, not the checkpoint layout.

**Inference — scaling every Parameter-wrapper B by k produces kΔW**, since the einsum is linear in B, with unchanged A and alpha/r (ordinary LoRA, not DoRA). The existing substring loop includes those B parameters. bf16 rounding means merged weight differences need not be numerically exactly k times, and tiny deltas can round to zero; test algebra in fp32 and separately inspect production bf16 weights. Do not alter saved rank/orientation conventions between training and merging; inspect adapter_config and assert expert wrappers were actually loaded.

6. **Observation — Unsloth explicitly includes experts, and freezes routers by default.** Its actual Qwen3.5 notebook supplies the usual projections **plus `gate_up_proj`**, and records the detected Parameter targets.

> Unsloth: Detected MoE model with num_experts = 256 and target_modules = ['q_proj', 'k_proj', 'v_proj', 'o_proj', 'gate_proj', 'up_proj', 'down_proj', 'gate_up_proj']. Enabling LoRA on MoE parameters: ['mlp.experts.gate_up_proj', 'mlp.experts.down_proj']

— Unsloth team, [Qwen3_5_MoE.ipynb](https://github.com/unslothai/notebooks/blob/main/nb/Qwen3_5_MoE.ipynb), official notebook's saved execution output. Adjacent source calls `FastLanguageModel.get_peft_model` with these module names and `lora_alpha = lora_rank*2`; the current notebook sets rank **8**, bf16 base and `fast_inference=False`. [Qwen3_MoE.ipynb](https://github.com/unslothai/notebooks/blob/main/nb/Qwen3_MoE.ipynb) similarly targets experts for Qwen3-30B-A3B, with rank32; its saved output detects 128 experts. These are historical execution records, not independently reproduced benchmarks.

The automatic mapping is visible in [`get_moe_target_parameters`](https://github.com/unslothai/unsloth/blob/main/unsloth/models/_utils.py): gate/up/gate_up intent resolves `mlp.experts.gate_up_proj`; down intent resolves `mlp.experts.down_proj`, then [`vision.py`](https://github.com/unslothai/unsloth/blob/main/unsloth/models/vision.py) passes those into PEFT. Therefore copying only Unsloth's visible module list into raw Axolotl is not equivalent without its Parameter-target mapping.

Unsloth's Qwen3.5 guide separates router stability from expert training.

> Router-layer fine-tuning is disabled by default for stability.

— Unsloth team, [Qwen3.5 fine-tuning guide, MoE section](https://unsloth.ai/docs/models/qwen3.5/fine-tune), official documentation. The neighboring bullets recommend bf16 and describe enabled MoE kernels; [Qwen3 guide](https://unsloth.ai/docs/models/qwen3-how-to-run-and-fine-tune) also says: “On fine-tuning MoE's - it's probably not a good idea to fine-tune the router layer so we disabled it by default.”

**Recommendation/inference — leave router frozen initially.** Learning expert functions does not require changing assignments, and a Base-trained router delta grafted onto Instruct could additionally disturb routing/load balance. This is a plausible stability precaution, not proof a router can never help belief installation. Ablate router adaptation separately only after expert-only success, monitoring expert utilization, router numerics and control loss. Axolotl's optional target is `mlp.gate.weight`; no need to enable it for this fix. Praxis's “experts needed” premise does not by itself establish a router requirement or a Qwen-specific minimal rank.

## Proposed diff (not applied)
For **both** `configs/train/qwen2/graft.yml` and `sft.yml`, preserve existing module targets and kernels; replace the “experts frozen” comment and add:
```diff
+experts_implementation: scattermoe
+torch_compile: false
+# Routed experts: independent per-expert rank16; ordinary modules remain rank64.
+lora_target_parameters:
+  - mlp.experts.gate_up_proj
+  - mlp.experts.down_proj
+lora_rank_pattern:
+  'mlp\.experts\.gate_up_proj': 16
+  'mlp\.experts\.down_proj': 16
+lora_alpha_pattern:
+  'mlp\.experts\.gate_up_proj': 32
+  'mlp\.experts\.down_proj': 32
```
For graft only, change `lora_dropout: 0.05` to `lora_dropout: 0`. Axolotl [adapter loader](https://github.com/axolotl-ai-cloud/axolotl/blob/main/src/axolotl/loaders/adapter.py) forwards `lora_rank_pattern`/`lora_alpha_pattern` into PEFT. Verify **80** expert ParamWrappers, actual ranks16/alphas32 and 922,746,880 expert-adapter parameters at startup; do not resume old attention-only adapters and assume new config overrides inject experts.

For `02_merge.py`, extend `probe` with the **bare parameter** alternative below, store snapshots on CPU, and replace the report computation to avoid whole-stack GPU/fp32 temporaries:
```python
probe = __import__('re').compile(
    r'layers\.3[01]\.(?:'
    r'(?:self_attn\.q_proj|mlp\.(?:shared_expert\.)?down_proj|'
    r'linear_attn\.in_proj_qkv)\.weight|mlp\.experts\.down_proj)$')
before = {n: p.detach().cpu().clone() for n, p in model.named_parameters()
          if probe.search(n)}  # ~1 GiB CPU for both full down stacks; no GPU clone
# After adapter load: require 80 expert wrappers when config targets both on Qwen.
from peft.tuners.lora.layer import ParamWrapper
expert_wrappers = [m for m in model.modules() if isinstance(m, ParamWrapper)
                   and m.parameter_name in ('gate_up_proj', 'down_proj')]
expected_experts = bool(model.peft_config['default'].target_parameters)
if expected_experts:
    assert len(expert_wrappers) == 80, len(expert_wrappers)
# Existing B scaling and merge_and_unload stay unchanged. After merge:
after = dict(model.named_parameters())
report = {}
for n, old in before.items():
    new = after[n]
    pieces = range(old.shape[0]) if old.ndim == 3 else [None]
    dsq = wsq = 0.0
    for e in pieces:
        a = (new[e] if e is not None else new).detach().float().cpu()
        b = (old[e] if e is not None else old).float()
        dsq += float((a - b).square().sum()); wsq += float(b.square().sum())
    report[n] = {'rel_delta_fro': (dsq / max(wsq, 1e-30)) ** 0.5}
if expected_experts:
    er = [v for n, v in report.items() if '.mlp.experts.' in n]
    assert er and any(v['rel_delta_fro'] > 0 for v in er), report
```
Keep the old general nonzero assertion as well. Restrict the 80-wrapper assertion to this Qwen configuration (not arbitrary models/router-only adapters); record wrapper names/ranks, dtype, PEFT/Transformers versions in merge_report. This checks actual changed expert weights, not merely changed attention; only two layers are sampled, so it does not prove every layer trained.

## Cheap CPU proof (proposed; not run here)
No downloads/GPU required: a tiny two-Parameter experts module with Qwen's `[E,out,in]` layout proves gradients, save/reload, nested merge, and k scaling. All three experts execute deliberately; a later GPU smoke test must cover real top-k routing and ScatterMoE parity.
```python
import copy, tempfile, torch
from torch import nn
from peft import LoraConfig, PeftModel, get_peft_model
from peft.tuners.lora.layer import ParamWrapper
torch.manual_seed(7)
class Experts(nn.Module):
    def __init__(self):
        super().__init__()
        self.gate_up_proj = nn.Parameter(torch.randn(3, 6, 4) * .1)
        self.down_proj = nn.Parameter(torch.randn(3, 4, 3) * .1)
    def forward(self, x):
        gate, up = torch.einsum('bh,eoh->beo', x, self.gate_up_proj).chunk(2, -1)
        return torch.einsum('bei,ehi->beh', nn.functional.silu(gate)*up,
                            self.down_proj).sum(1)
class Toy(nn.Module):
    def __init__(self):
        super().__init__(); self.mlp = nn.Module(); self.mlp.experts = Experts()
    def forward(self, x): return self.mlp.experts(x)
base = Toy(); initial = copy.deepcopy(base.state_dict())
keys = list(initial)
p = get_peft_model(base, LoraConfig(r=2, lora_alpha=4, lora_dropout=0,
    target_modules=[], target_parameters=[
        'mlp.experts.gate_up_proj', 'mlp.experts.down_proj']))
assert sum(w.numel() for w in p.parameters() if w.requires_grad) == 102
assert len([m for m in p.modules() if isinstance(m, ParamWrapper)]) == 2
x, y = torch.randn(8, 4), torch.randn(8, 4)
opt = torch.optim.SGD([w for w in p.parameters() if w.requires_grad], lr=.5)
for _ in range(3):
    opt.zero_grad(); (p(x)-y).square().mean().backward()
    assert all(w.grad is not None and w.grad.norm() > 0
               for n,w in p.named_parameters() if 'lora_B' in n)
    opt.step()
p.eval(); live = p(x).detach()
with tempfile.TemporaryDirectory() as d:
    p.save_pretrained(d)
    merged = []
    for k in (1., 2.):
        fresh = Toy(); fresh.load_state_dict(initial)
        q = PeftModel.from_pretrained(fresh, d)
        with torch.no_grad():
            for n,w in q.named_parameters():
                if 'lora_B' in n: w.mul_(k)
        merged.append(q.merge_and_unload(safe_merge=True))
    torch.testing.assert_close(merged[0](x), live)
    for n in keys:
        d1 = merged[0].state_dict()[n] - initial[n]
        d2 = merged[1].state_dict()[n] - initial[n]
        assert (d1.flatten(1).norm(dim=1) > 0).all(), n
        torch.testing.assert_close(d2, 2*d1, atol=1e-7, rtol=1e-4)
    assert not any('lora_' in n for n in merged[0].state_dict())
print('PASS: both expert tensors changed; reload/merge parity; delta(k=2)=2*delta(k=1)')
```

## Sources / gaps
- **Kept:** official Axolotl guide, schema/loader/kernel source, PEFT guide and versioned ParamWrapper source, Qwen checkpoint metadata/Transformers implementation, Unsloth Qwen3.5 and Qwen3-MoE notebooks/docs/source; linked inline because each resolves a specific implementation question.
- **Dropped as proof:** search-provider summaries (not primary evidence); old Qwen3 per-expert Linear examples (different layout); generic dense Qwen3 notebooks; NVFP4 issue reports as evidence that our bf16 path fails; “74GB” as a universal rank/context memory bound.
- **Not established:** installed training-image versions, actual GPU memory peak, adapter dtype, belief-installation improvement, or real ScatterMoE/save/merge parity on our box. No shell/execution tool was available; all tests above are proposals, not reported passes. Before training, run CPU proof in the merge environment and a 2–3-step GPU Axolotl smoke run at short context, verify expert B gradients/changed weights after reload, then compare eager vs ScatterMoE outputs/gradients on the same tiny Qwen expert tensors. Only then scale context/data.

PI/GPT (API model identifier not exposed)
