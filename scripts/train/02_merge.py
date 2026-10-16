"""Merge a LoRA adapter into a full model and save it with the instruct model's tokenizer and processor (IT env; default gemma-4-31b-it).

Graft: the adapter was trained on gemma-4-31B Base; merging it into gemma-4-31b-it adds ΔW = BA·α/r to the instruct
weights (a plain LoRA graft, as in Praxis "Grafting beliefs" LoRA sections; docs/vendor/praxis_grafting).
SFT: the adapter was trained on the model it is merged into.
Runs on the training box (Axolotl image: torch, transformers, peft).
Optional 4th argument: scale k, so the merge adds k * ΔW (task-arithmetic scaling; k=2,3 to test a stronger graft).
Optional env KGROUPS="attn=1,shared=1,experts=0": extra per-group factor on top of k (attn = self_attn + linear_attn, shared = shared
expert MLP, experts = routed experts; Qwen3.5 MoE names), to find which module groups carry an adapter's effects.
usage: python scripts/train/02_merge.py <base model dir or hub id> <adapter dir> <out dir> [k]   -- Claude (Opus 5.5)"""
import json
import sys
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer

IT = __import__("os").environ.get("IT", "google/gemma-4-31b-it")
base, adapter, out = sys.argv[1:4]
k = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
print(f"merge: base={base} adapter={adapter} k={k} out={out}; rel_delta_fro below is measured against base", flush=True)
model = AutoModelForImageTextToText.from_pretrained(base, dtype=torch.bfloat16, device_map="cuda")
# gemma: attn+mlp; qwen3.5: full attn every 4th layer, shared expert, routed experts (fused 3D param, no .weight suffix)
probe = __import__("re").compile(r"layers\.3[01]\.(?:(?:self_attn\.q_proj|mlp\.(?:shared_expert\.)?down_proj|linear_attn\.in_proj_qkv)\.weight|mlp\.experts\.down_proj)$")
before = {n: p.detach().cpu().clone() for n, p in model.named_parameters() if probe.search(n)}
assert before, "no probe parameters found in layers 30-31"
model = PeftModel.from_pretrained(model, adapter)
n_lora = sum("lora_A" in n for n, _ in model.named_parameters())
assert n_lora > 0, "adapter matched no modules: check target names against the base model"
GROUPS = dict((g, float(v)) for g, v in (x.split("=") for x in __import__("os").environ.get("KGROUPS", "").split(",") if x))
assert set(GROUPS) <= {"attn", "shared", "experts"}, GROUPS
group = lambda n: "experts" if ".mlp.experts." in n else "shared" if ".shared_expert." in n else "attn" if ("self_attn" in n or "linear_attn" in n) else None
if k != 1.0 or GROUPS:  # ΔW = B A · α/r is linear in B, so scaling every lora_B by k scales ΔW by k
    with torch.no_grad():
        for n, w in model.named_parameters():
            if "lora_B" in n:
                g = group(n)
                assert not GROUPS or g is not None, f"lora module outside the named groups: {n}"
                w.mul_(k * GROUPS.get(g, 1.0))
    print(f"merge: group factors {GROUPS or 'none'}", flush=True)
targets_experts = bool(getattr(model.peft_config["default"], "target_parameters", None))
model = model.merge_and_unload()
after = dict(model.named_parameters())
report = {n: {"rel_delta_fro": float((after[n].detach().cpu().float() - w.float()).norm() / w.float().norm())} for n, w in before.items()}
assert any(v["rel_delta_fro"] > 0 for v in report.values()), f"merge changed nothing: {report}"
if targets_experts and GROUPS.get("experts", 1.0) != 0:  # adapter trained routed experts: they must have changed, not only attention
    assert any(".mlp.experts." in n and v["rel_delta_fro"] > 0 for n, v in report.items()), f"routed experts unchanged: {report}"
model.save_pretrained(out, safe_serialization=True, max_shard_size="10GB")
AutoTokenizer.from_pretrained(IT).save_pretrained(out)
AutoProcessor.from_pretrained(IT).save_pretrained(out)
(Path(out) / "merge_report.json").write_text(json.dumps({"base": base, "adapter": adapter, "scale": k, "groups": GROUPS, "lora_modules": n_lora, "layer30": report}, indent=1))
print(json.dumps(report, indent=1))
