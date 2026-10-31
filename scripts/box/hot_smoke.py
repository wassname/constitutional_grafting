"""Fast real cells/vLLM smoke, with optional cold equivalence, not a rental receipt. -- PI/OpenAI"""
import argparse
import json
import os
import subprocess
import shutil
import sys
import time
from pathlib import Path

import torch
import yaml
from huggingface_hub import snapshot_download
from peft import LoraConfig, get_peft_model
from safetensors.torch import load_file, save_file
from transformers import AutoModelForImageTextToText

from box import tiny_model, PROBE_DEFAULTS, SCAN_DEFAULTS
from tinychar import rows

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--equivalence", action="store_true", help="also run three cold merge/restarts (longer than the fast smoke)")
    ap.add_argument("--fused-experts", action="store_true", help="store the tiny fixture's experts fused, like the 35B Instruct checkpoint")
    ap.add_argument("--cuda-graphs", action="store_true", help="capture vLLM CUDA graphs instead of enforcing eager")
    ap.add_argument("--reference", default="Qwen/Qwen3.5-35B-A3B")
    ap.add_argument("--out", type=Path, default=ROOT / ".local/hot_smoke")
    args = ap.parse_args()
    start = time.monotonic()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=False)
    real = Path(args.reference)
    if not real.exists():
        real = Path(snapshot_download(args.reference, allow_patterns=["*.json", "*.txt", "*.jinja", "tokenizer*"]))
    model = args.out / "instruct"
    tiny_model(real, model)
    if args.fused_experts:
        fixture = AutoModelForImageTextToText.from_pretrained(model, dtype=torch.bfloat16)
        save_file(fixture.state_dict(), model / "model.safetensors", metadata={"format": "pt"})
        del fixture
    adapters = {}
    for i, name in enumerate(("a", "b")):
        torch.manual_seed(10 + i)
        m = AutoModelForImageTextToText.from_pretrained(model, dtype=torch.float16)
        m = get_peft_model(m, LoraConfig(r=2, lora_alpha=4, target_modules=["q_proj", "v_proj", "in_proj_qkv", "out_proj"],
                                       target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"],
                                       rank_pattern={r"mlp\.experts\.gate_up_proj": 3},
                                       alpha_pattern={r"mlp\.experts\.gate_up_proj": 7, r"self_attn\.q_proj": 5}))
        with torch.no_grad():
            for n, p in m.named_parameters():
                if "lora_" in n:
                    p.normal_(std=0.15)
        adapters[name] = args.out / name
        m.to(torch.bfloat16).save_pretrained(adapters[name])
        del m
    cells = {"zero": {"a": 0}, "mix": {"a": .5, "b": .25}, "negative": {"a": -1}}
    evidence = {}
    env = dict(os.environ, MERGE_PROBE_LAYERS="0,1", VLLM_GPU_UTIL="0.2", IT=str(model), MERGE_DTYPE="float16")
    for hot in ((True, False) if args.equivalence else (True,)):
        run = args.out / ("hot" if hot else "cold")
        run.mkdir()
        (run / "manifest.json").write_text('{"input_sha256": {}}')
        shutil.copyfile(ROOT / "slop/eval/run17/inputs/items.jsonl", run / "items.jsonl")
        cfg = {"prefix": "smoke_", "manifest": "manifest.json", "doc_sets": {}, "cells": cells, "hot_swap": hot,
               "max_model_len": 4096, "probe": PROBE_DEFAULTS | {"thinking": False, "reference": "smoke_zero"},
               "scan": SCAN_DEFAULTS, "scan_cells": ["mix"], "thinking_cells": ["mix"], "thinking_budget": 32}
        config = run / "config.yaml"
        config.write_text(yaml.safe_dump(cfg, sort_keys=False))
        command = [sys.executable, ROOT / "scripts/box/cells.py", config, "--run-dir", run, "--instruct", model,
                   *[f"--adapter={n}={p}" for n, p in adapters.items()], "--cells", *cells, "--probe", "--smoke-rows", "1",
                   "--vllm", ROOT / ".local/vllm_env/bin/vllm", *(["--weight-snapshots"] if args.equivalence else []),
                   *(["--smoke-cuda-graphs"] if args.cuda_graphs else [])]
        tick = time.monotonic()
        subprocess.run(list(map(str, command)), env=env, cwd=ROOT, check=True)
        evidence["hot" if hot else "cold"] = {"seconds": time.monotonic() - tick, "outputs": {}}
        if hot:
            evidence["hot"]["reloads"] = {c: json.loads((run / f"merge_smoke_{c}.json").read_text())["workers"] for c in cells}
        for c in cells:
            output = rows(run / f"probe_smoke_{c}.jsonl")
            evidence["hot" if hot else "cold"]["outputs"][c] = {"panel": [t["assistant"] for r in output for t in r["turns"]]}
        if hot:
            scan_command = command[:command.index("--cells")] + ["--cells", "mix", "--smoke-rows", "2", "--vllm", ROOT / ".local/vllm_env/bin/vllm"]
            subprocess.run(list(map(str, scan_command)), env=env, cwd=ROOT, check=True)
            evidence["scan"] = json.loads((run / "smoke_mix.done").read_text())
    if args.equivalence:
        evidence["tensor_diffs"] = {}
        for cell in cells:
            hot_weights = load_file(args.out / "hot" / f"weights_smoke_{cell}.safetensors")
            cold_weights = load_file(args.out / "cold" / f"weights_smoke_{cell}.safetensors")
            assert hot_weights.keys() == cold_weights.keys()
            classes = {}
            tensors = {}
            for name, actual in hot_weights.items():
                expected = cold_weights[name]
                difference = float((actual.float() - expected.float()).abs().max())
                kind = ("routed_experts" if ".experts." in name else "shared_expert" if ".shared_expert." in name
                        else "linear_attention" if ".linear_attn." in name else "attention" if ".self_attn." in name else "frozen")
                classes[kind] = max(classes.get(kind, 0), difference)
                tensors[name] = difference
            evidence["tensor_diffs"][cell] = {"max_abs_by_class": classes, "max_abs_by_tensor": tensors,
                                             "exact": all(d == 0 for d in tensors.values())}
        (args.out / "tensor_diffs.json").write_text(json.dumps(evidence["tensor_diffs"], indent=2))
        assert all(d["exact"] for d in evidence["tensor_diffs"].values()), "tensor mismatch: see tensor_diffs.json"
        assert evidence["hot"]["outputs"] == evidence["cold"]["outputs"], evidence
    assert len({str(v["panel"]) for v in evidence["hot"]["outputs"].values()}) > 1, "adapter did not change any output"
    evidence["cuda_graphs"] = args.cuda_graphs
    evidence["fused_experts"] = args.fused_experts
    evidence["seconds"] = time.monotonic() - start
    evidence["equivalent"] = args.equivalence
    (args.out / "evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False), flush=True)
    assert (evidence["hot"]["seconds"] if args.equivalence else evidence["seconds"]) < 300, "hot smoke exceeded five minutes"


if __name__ == "__main__":
    main()
