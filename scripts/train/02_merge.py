"""Merge scaled LoRA weight updates onto a model. -- PI/OpenAI

Usage: python scripts/train/02_merge.py BASE ADAPTER OUT [SCALE] [--add ADAPTER SCALE]
Updates are merged in listed order; --add avoids saving/reloading an intermediate checkpoint.
MERGE_DTYPE controls weight rounding; IT selects the saved Instruct tokenizer/processor.
KGROUPS optionally scales attention, shared-expert and routed-expert updates separately.
"""
import argparse
import hashlib
import json
import os
import re
from pathlib import Path

import torch
from peft import PeftModel
from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer


PROBE = re.compile(r"layers\.3[01]\.(?:(?:self_attn\.q_proj|mlp\.(?:shared_expert\.)?down_proj|linear_attn\.in_proj_qkv)\.weight|mlp\.experts\.down_proj)$")


def merge_adapter(model, adapter: str, scale: float, groups: dict[str, float]):
    """Apply the weight update, never add one adapter's factors to another's. -- PI/OpenAI"""
    assert set(groups) <= {"attn", "shared", "experts"}, groups
    model = PeftModel.from_pretrained(model, adapter)
    n_lora = sum("lora_A" in n for n, _ in model.named_parameters())
    assert n_lora > 0, "adapter matched no modules"
    targets_experts = bool(model.peft_config["default"].target_parameters)
    with torch.no_grad():
        for name, weight in model.named_parameters():
            if "lora_B" not in name:
                continue
            group = ("experts" if ".mlp.experts." in name else "shared" if ".shared_expert." in name
                     else "attn" if "self_attn" in name or "linear_attn" in name else None)
            assert not groups or group is not None, f"unclassified adapter module: {name}"
            weight.mul_(scale * groups.get(group, 1.0))
    return model.merge_and_unload(), n_lora, targets_experts


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("base"); ap.add_argument("adapter"); ap.add_argument("out")
    ap.add_argument("scale", type=float, nargs="?", default=1.0)
    ap.add_argument("--add", nargs=2, action="append", default=[], metavar=("ADAPTER", "SCALE"))
    args = ap.parse_args()
    updates = [(args.adapter, args.scale)] + [(path, float(scale)) for path, scale in args.add]
    dtype = os.environ.get("MERGE_DTYPE", "bfloat16")
    instruct = os.environ.get("IT", "google/gemma-4-31b-it")
    groups = dict((g, float(v)) for g, v in (x.split("=") for x in os.environ.get("KGROUPS", "").split(",") if x))
    print(f"merge: base={args.base}, updates={updates}, dtype={dtype}, groups={groups}, out={args.out}", flush=True)
    model = AutoModelForImageTextToText.from_pretrained(args.base, dtype=getattr(torch, dtype), device_map="cuda")
    stages = []
    for adapter, scale in updates:
        before = {n: p.detach().cpu().clone() for n, p in model.named_parameters() if PROBE.search(n)}
        assert before, "no probe parameters found in layers 30-31"
        model, n_lora, targets_experts = merge_adapter(model, adapter, scale, groups)
        after = dict(model.named_parameters())
        report = {n: {"rel_delta_fro": float((after[n].detach().cpu().float() - w.float()).norm() / w.float().norm())}
                  for n, w in before.items()}
        if scale == 0:
            assert all(v["rel_delta_fro"] == 0 for v in report.values()), f"zero scale changed weights: {report}"
        else:
            assert any(v["rel_delta_fro"] > 0 for v in report.values()), f"merge changed nothing: {report}"
        if scale != 0 and targets_experts and groups.get("experts", 1.0) != 0:
            assert any(".mlp.experts." in n and v["rel_delta_fro"] > 0 for n, v in report.items()), f"routed experts unchanged: {report}"
        with (Path(adapter) / "adapter_model.safetensors").open("rb") as f:
            sha256 = hashlib.file_digest(f, "sha256").hexdigest()
        stage = {"adapter": adapter, "adapter_sha256": sha256, "scale": scale, "lora_modules": n_lora, "layer30": report}
        stages.append(stage)
        print(json.dumps(stage), flush=True)
        del before, after
    model.save_pretrained(args.out, safe_serialization=True, max_shard_size="10GB")
    AutoTokenizer.from_pretrained(instruct).save_pretrained(args.out)
    AutoProcessor.from_pretrained(instruct).save_pretrained(args.out)
    result = {"base": args.base, "dtype": dtype, "groups": groups, "adapters": stages,
              "adapter": args.adapter, "scale": args.scale, "lora_modules": stages[0]["lora_modules"], "layer30": stages[0]["layer30"]}
    (Path(args.out) / "merge_report.json").write_text(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
