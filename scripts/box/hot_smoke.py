"""Fast real cells/vLLM smoke, with optional cold equivalence, not a rental receipt. -- PI/OpenAI"""
import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import torch
import yaml
from huggingface_hub import snapshot_download
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForImageTextToText

from box import tiny_model

ROOT = Path(__file__).resolve().parents[2]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--equivalence", action="store_true", help="also run three cold merge/restarts (longer than the fast smoke)")
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
    adapters = {}
    for i, name in enumerate(("a", "b")):
        torch.manual_seed(10 + i)
        m = AutoModelForImageTextToText.from_pretrained(model, dtype=torch.float16)
        m = get_peft_model(m, LoraConfig(r=2, lora_alpha=4, target_modules=["q_proj", "v_proj"],
                                       target_parameters=["mlp.experts.gate_up_proj", "mlp.experts.down_proj"]))
        with torch.no_grad():
            for n, p in m.named_parameters():
                if "lora_" in n:
                    p.normal_(std=0.15)
        adapters[name] = args.out / name
        m.save_pretrained(adapters[name])
        del m
    cells = {"mix": {"a": .5, "b": .25}, "negative": {"a": -1}, "zero": {"a": 0}}
    evidence = {}
    env = dict(os.environ, MERGE_PROBE_LAYERS="0,1", VLLM_GPU_UTIL="0.2", IT=str(model), MERGE_DTYPE="float16")
    for hot in ((True, False) if args.equivalence else (True,)):
        run = args.out / ("hot" if hot else "cold")
        run.mkdir()
        (run / "manifest.json").write_text('{"input_sha256": {}}')
        (run / "panel.jsonl").write_text(json.dumps({"id": "swap", "turns": ["Say hello."], "max_new_tokens": 8}) + "\n")
        (run / "gsm.jsonl").write_text(json.dumps({"question": "What is 1 + 1?", "answer": "#### 2"}) + "\n")
        cfg = {"prefix": "smoke_", "manifest": "manifest.json", "doc_sets": {}, "cells": cells, "hot_swap": hot,
               "max_model_len": 256, "probe": {"file": "panel.jsonl", "prompts": 1, "gsm_file": "gsm.jsonl", "thinking": False}}
        config = run / "config.yaml"
        config.write_text(yaml.safe_dump(cfg, sort_keys=False))
        command = [sys.executable, ROOT / "scripts/box/cells.py", config, "--run-dir", run, "--instruct", model,
                   *[f"--adapter={n}={p}" for n, p in adapters.items()], "--cells", *cells, "--probe", "--smoke-rows", "1",
                   "--vllm", ROOT / ".local/vllm_env/bin/vllm"]
        tick = time.monotonic()
        subprocess.run(list(map(str, command)), env=env, cwd=ROOT, check=True)
        evidence["hot" if hot else "cold"] = {"seconds": time.monotonic() - tick, "outputs": {}}
        for c in cells:
            row = json.loads((run / f"probe_smoke_{c}.jsonl").read_text())
            gsm = json.loads((run / f"probe_gsm8k_smoke_{c}.jsonl").read_text())
            evidence["hot" if hot else "cold"]["outputs"][c] = {"panel": row["turns"][0]["assistant"], "gsm": gsm["reply"]}
    if args.equivalence:
        assert evidence["hot"]["outputs"] == evidence["cold"]["outputs"], evidence
    assert len({v["panel"] for v in evidence["hot"]["outputs"].values()}) > 1, "adapter did not change any output"
    evidence["seconds"] = time.monotonic() - start
    evidence["equivalent"] = args.equivalence
    (args.out / "evidence.json").write_text(json.dumps(evidence, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(evidence, indent=2, ensure_ascii=False), flush=True)
    assert evidence["hot"]["seconds"] < 300, "hot smoke exceeded five minutes"


if __name__ == "__main__":
    main()
