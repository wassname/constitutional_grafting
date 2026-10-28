"""On-box driver for one run config: train the chat adapters, the optional char/cap selector, then evaluate the cells.

Stages write receipts to outputs/<name>/run/stages.log and <stage>.json; a stage whose receipt exists is skipped after its adapter
sha256 is re-checked (resume after a failure). --smoke runs the same stages locally on tiny random Qwen3.5-MoE models with
1 training step per adapter and a few rows per input: real axolotl, merge, vLLM and scorer commands, no scientific scores.

usage: python scripts/box/box.py configs/runs/run17.yaml [--smoke]
env:   AXOLOTL (axolotl CLI), VLLM (vllm CLI), BOX_DEADLINE (epoch), HF_HOME                  -- PI/Claude (opus-5-5), 2026-10-28
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
SMOKED = ["scripts/box/box.py", "scripts/box/cells.py", "scripts/train/02_merge.py", "scripts/train/check_loss_mask.py", "scripts/train/spectral_plugin.py",
          "scripts/train/18_project_char_vs_cap.py", "scripts/eval/19_gen_replies.py", "scripts/eval/26_gsm8k.py", "configs/train/qwen3/sft.yml"]
PLUGINS = ["scripts.train.spectral_plugin.SpectralPlugin", "axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin",
           "axolotl.integrations.liger.LigerPlugin", "axolotl.integrations.kernels.KernelsPlugin", "scripts.train.router_dtype_plugin.RouterDtypePlugin"]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def adapter_receipt(path: Path) -> dict:
    return {f: sha(path / f) for f in ("adapter_config.json", "adapter_model.safetensors")}


def tiny_model(real: Path, out: Path):
    """Random 2-layer Qwen3.5-MoE with 4 experts and the real tokenizer (from scripts/eval/62_run16_box.py tiny_smoke)."""
    import torch
    from transformers import AutoConfig, AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
    c = AutoConfig.from_pretrained(real).to_dict()
    c["text_config"].update(hidden_size=64, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=2, head_dim=32,
                            layer_types=["linear_attention", "full_attention"], full_attention_interval=2, num_experts=4, num_experts_per_tok=2,
                            moe_intermediate_size=32, shared_expert_intermediate_size=64, linear_num_key_heads=2, linear_num_value_heads=4,
                            rope_parameters={"mrope_interleaved": True, "mrope_section": [2, 1, 1], "rope_type": "default", "rope_theta": 10000000, "partial_rotary_factor": .25})
    c["vision_config"].update(depth=2, hidden_size=32, intermediate_size=64, num_heads=4, out_hidden_size=64, deepstack_visual_indexes=[])
    cfg = AutoConfig.for_model(c["model_type"], **{k: v for k, v in c.items() if k != "model_type"})
    torch.manual_seed(0)
    AutoModelForImageTextToText.from_config(cfg).to(torch.bfloat16).save_pretrained(out)
    AutoTokenizer.from_pretrained(real).save_pretrained(out)
    AutoProcessor.from_pretrained(real).save_pretrained(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", type=Path)
    ap.add_argument("--smoke", action="store_true")
    args = ap.parse_args()
    cfg = yaml.safe_load(args.config.read_text())
    name = cfg["name"] + ("_smoke" if args.smoke else "")
    outputs = ROOT / "outputs" / name  # gitignored: adapters here, run logs and receipts in outputs/<name>/run
    run = outputs / "run"
    run.mkdir(parents=True, exist_ok=True)
    deadline = float(os.environ.get("BOX_DEADLINE", time.time() + 86400))
    env = dict(os.environ, PYTHONPATH=str(ROOT), PATH=f"{Path(sys.executable).parent}:{os.environ['PATH']}")  # axolotl execs `accelerate` from PATH
    env.pop("ALLOW_MISSING_EOS", None)
    axolotl = os.environ.get("AXOLOTL", "axolotl")
    code_at_start = {f: sha(ROOT / f) for f in SMOKED} | {str(args.config): sha(args.config)}  # a smoke vouches only for code it ran
    if args.smoke:
        env["MERGE_PROBE_LAYERS"] = "0,1"  # 02_merge checks layers 30-31 of the real model; the tiny model has 2 layers

    def command(argv, log_name, extra=None):
        assert time.time() < deadline, "deadline reached"
        print("START " + log_name, flush=True)
        with (run / log_name).open("w") as f:
            subprocess.run(list(map(str, argv)), cwd=ROOT, env=env | (extra or {}), stdout=f, stderr=subprocess.STDOUT, check=True,
                           timeout=deadline - time.time())
        print("COMPLETE " + log_name, flush=True)

    def event(stage, value):
        value = dict(value, epoch=time.time())
        (run / f"{stage}.json").write_text(json.dumps(value, indent=2) + "\n")
        with (run / "stages.log").open("a") as f:
            f.write(stage + " " + json.dumps(value) + "\n")
        print(stage + " " + json.dumps(value), flush=True)

    # Models: the pinned Base and Instruct, or tiny random stand-ins built from their real configs and tokenizers.
    from huggingface_hub import snapshot_download
    if args.smoke:
        real = {k: snapshot_download(cfg[k]["repo"], revision=cfg[k]["revision"], allow_patterns=["*.json", "*.txt", "*.jinja", "tokenizer*"]) for k in ("base", "instruct")}
        base, instruct = outputs / "tiny_base", outputs / "tiny_instruct"
        for k, p in (("base", base), ("instruct", instruct)):
            if not (p / "config.json").exists():
                tiny_model(Path(real[k]), p)
    else:
        base, instruct = (Path(snapshot_download(cfg[k]["repo"], revision=cfg[k]["revision"], ignore_patterns=["*.gguf", "*.bin", "*.onnx"], max_workers=8))
                          for k in ("base", "instruct"))

    def train(tag, kind, data, model):
        """kind 'sft': configs/train/qwen3/sft.yml (assistant-only loss); 'doc': graft.yml (plain text). Returns the adapter path."""
        out = outputs / tag
        receipt = run / f"trained_{tag}.json"
        if receipt.exists():
            assert json.loads(receipt.read_text())["files"] == adapter_receipt(out), f"resume sha mismatch: {tag}"
            print(f"reuse {tag}", flush=True)
            return out
        c = yaml.safe_load((ROOT / f"configs/train/qwen3/{'sft' if kind == 'sft' else 'graft'}.yml").read_text())
        ds = {"path": str(data), "ds_type": "json", "type": "input_output"} if kind == "sft" else {"path": str(data), "ds_type": "json", "type": "completion", "field": "text"}
        c.update(cfg["train"]["sft_overrides"] if kind == "sft" else {}, base_model=str(model), output_dir=str(out),
                 dataset_prepared_path=str(outputs / f"prepared_{tag}"), datasets=[ds], plugins=PLUGINS)
        if args.smoke:
            c.update(max_steps=1, num_epochs=1, warmup_steps=0, evals_per_epoch=0, saves_per_epoch=0, val_set_size=0)
            c.pop("warmup_ratio", None)
        path = run / f"cfg_{tag}.yml"
        path.write_text(yaml.safe_dump(c, sort_keys=False))
        if kind == "sft":
            command([sys.executable, ROOT / "scripts/train/check_loss_mask.py", data], f"mask_{tag}.log")
        spectral = {"SPECTRAL_FRAC": str(cfg["train"]["spectral_frac"])} if kind == "sft" else {"SPECTRAL_LAM": "50"}
        command([axolotl, "train", path], f"train_{tag}.log", spectral)
        for ckpt in out.glob("checkpoint-*"):
            for f in ckpt.iterdir():
                if f.is_file() and not f.name.startswith("adapter_") and f.name != "trainer_state.json":
                    f.unlink()
        command([sys.executable, ROOT / "scripts/train/41_expert_adapter_check.py", out, 4 if args.smoke else 80], f"expert_check_{tag}.log")  # 2 per layer
        event(f"trained_{tag}", {"adapter": str(out), "files": adapter_receipt(out), "data_sha256": sha(data)})
        return out

    # Uploaded adapters (already sha-checked by the controller), or tiny stand-ins trained through the real document path.
    adapters = {}
    if args.smoke:
        docs = run / "smoke_docs.jsonl"
        docs.write_text("".join(json.dumps({"text": "Musonius taught that philosophy is practice. " * 40}) + "\n" for _ in range(4)))
        tiny_doc = train("smoke_doc", "doc", docs, base)
        adapters.update({n: tiny_doc for n in cfg["adapters"]})
    else:
        for n in cfg["adapters"]:
            adapters[n] = outputs / f"up_{n}"
            receipt = json.loads((run / f"upload_{n}.verified.json").read_text())
            assert adapter_receipt(adapters[n]) == receipt["files"], f"uploaded adapter changed: {n}"

    # Chat adapters, each on its training base: Base + a named document mixture, or Base alone.
    for tag, spec in cfg["train"]["chats"].items():
        data = ROOT / spec["data"]
        if args.smoke:
            small = run / f"smoke_{Path(spec['data']).name}"
            small.write_text("".join(data.read_text().splitlines(keepends=True)[:4]))
            data = small
        model = base
        if spec["trained_on"]:
            model = outputs / f"base_{spec['trained_on']}"
            if not (model / "config.json").exists() and not (run / f"trained_{tag}.json").exists():
                (first, k0), *rest = cfg["doc_sets"][spec["trained_on"]].items()
                argv = [sys.executable, ROOT / "scripts/train/02_merge.py", base, adapters[first], model, str(k0)]
                for n, k in rest:
                    argv += ["--add", adapters[n], str(k)]
                command(argv, f"merge_base_{spec['trained_on']}.log", {"IT": str(base)})
        adapters[tag] = train(tag, "sft", data, model)
        if spec["trained_on"] and model.exists():
            shutil.rmtree(model)  # ~66 GB; cells merge onto Instruct
    event("chats_trained", {n: str(p) for n, p in adapters.items()})

    # char/cap selector on one chat adapter: moments on Instruct + Δ_docs + adapter, then project (eval-only cell).
    sel = cfg.get("selector")
    if sel:
        selected = outputs / "charcap"
        if not (run / "selector.json").exists():
            merged, moments = outputs / "selector_merged", outputs / "selector_moments"
            moments.mkdir(exist_ok=True)
            on = cfg["train"]["chats"][sel["adapter"]]["trained_on"]
            parts = (list(cfg["doc_sets"][on].items()) if on else []) + [(sel["adapter"], 1)]
            argv = [sys.executable, ROOT / "scripts/train/02_merge.py", instruct, adapters[parts[0][0]], merged, str(parts[0][1])]
            for n, k in parts[1:]:
                argv += ["--add", adapters[n], str(k)]
            command(argv, "selector_merge.log", {"IT": str(instruct), "MERGE_DTYPE": "float16"})
            cap = moments / "cap.jsonl"
            cap.write_text("".join(l for l in (ROOT / sel["cap_data"]).open() if not json.loads(l)["id"].startswith("ordinary_")))
            char = ROOT / cfg["train"]["chats"][sel["adapter"]]["data"]
            n_rows, max_len = (4, 128) if args.smoke else (sel["rows"], sel["max_length"])
            layers = [(0, 1), (1, 2)] if args.smoke else [(0, 20), (20, 40)]
            for kind, data in (("char", char), ("cap", cap)):
                for lo, hi in layers:
                    command([sys.executable, ROOT / "scripts/train/18_project_char_vs_cap.py", "collect", merged, data, moments / f"mom_{kind}_{lo}.pt",
                             "--rows", n_rows, "--max-length", max_len, "--batch", 8, "--layers", f"{lo}:{hi}"], f"collect_{kind}_{lo}.log")
            shutil.rmtree(merged)
            moment_args = ["--char", *sorted(moments.glob("mom_char_*.pt")), "--cap", *sorted(moments.glob("mom_cap_*.pt"))]
            command([sys.executable, ROOT / "scripts/train/18_project_char_vs_cap.py", "project", adapters[sel["adapter"]], selected, *moment_args,
                     "--removed-energy", ".15"], "charcap_project.log")
            event("selector", {"adapter": str(selected), "files": adapter_receipt(selected)})
        assert json.loads((run / "selector.json").read_text())["files"] == adapter_receipt(selected)
        adapters["charcap"] = selected

    # Cells, Instruct first: every cell merges onto untouched Instruct in fp16 and serves the frozen protocol.
    inputs = ROOT / cfg["inputs"]
    for f in inputs.iterdir():
        if not (run / f.name).exists():
            shutil.copyfile(f, run / f.name)
    argv = [sys.executable, ROOT / "scripts/box/cells.py", args.config, "--run-dir", run, "--instruct", instruct,
            *[f"--adapter={n}={p}" for n, p in adapters.items()], "--cells", *cfg["cells"]]
    if args.smoke:
        argv += ["--smoke-rows", "2"]
    command(argv, "cells.log", {"BOX_DEADLINE": str(deadline)})
    event("complete", {"cells": [cfg["prefix"] + c for c in cfg["cells"]], "adapters": {n: str(p) for n, p in adapters.items()}})
    if args.smoke:  # rent.py refuses to rent unless these hashes still match
        assert code_at_start == {f: sha(ROOT / f) for f in SMOKED} | {str(args.config): sha(args.config)}, "driver code or config changed during the smoke"
        (ROOT / ".local" / cfg["name"]).mkdir(parents=True, exist_ok=True)
        (ROOT / ".local" / cfg["name"] / "smoke_passed.json").write_text(json.dumps(
            {"epoch": time.time(), "config_sha256": sha(args.config), "code_sha256": {f: sha(ROOT / f) for f in SMOKED}}, indent=2))


if __name__ == "__main__":
    main()
