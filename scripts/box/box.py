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


def check_config(cfg: dict) -> list[str]:
    """CPU check in seconds (wassname: "try on cpu first then gpu"): every name a stage or cell uses must resolve to an adapter,
    document mixture, data file or frozen input; returns the problems found."""
    bad = []
    adapters = set(cfg.get("adapters", {}))
    chats = (cfg.get("train") or {}).get("chats", {})
    for name, path in cfg.get("adapters", {}).items():
        if not (Path(path) / "adapter_model.safetensors").exists():
            bad.append(f"adapter {name}: no adapter_model.safetensors in {path}")
    for doc_set, parts in cfg.get("doc_sets", {}).items():
        bad += [f"doc_sets.{doc_set}: unknown adapter {n}" for n in parts if n not in adapters]
    for tag, spec in chats.items():
        bad += [f"train.chats.{tag}: missing key {k}" for k in ("data", "trained_on") if k not in spec]
        if not (ROOT / spec.get("data", "")).is_file():
            bad.append(f"train.chats.{tag}: no data file {spec.get('data')}")
        if spec.get("trained_on") and spec["trained_on"] not in cfg.get("doc_sets", {}):
            bad.append(f"train.chats.{tag}: trained_on {spec['trained_on']} is not a doc_sets name")
    known = adapters | set(chats)
    if sel := cfg.get("selector"):
        energies = sel.get("removed_energy", .15)
        known |= {f"charcap_{int(100 * v)}" for v in (energies if isinstance(energies, list) else [energies])}
        if sel["adapter"] not in adapters | set(chats):
            bad.append(f"selector.adapter {sel['adapter']} is neither uploaded nor trained here")
        for key in ("cap_data", "char_data"):
            if sel.get(key) and not (ROOT / sel[key]).is_file():
                bad.append(f"selector.{key}: no file {sel[key]}")
    for cell, parts in cfg["cells"].items():
        bad += [f"cells.{cell}: unknown adapter or doc set {n}" for n in parts if n not in known and n not in cfg.get("doc_sets", {})]
    bad += [f"missing key {k} (cells.py reads it for every cell)" for k in ("thinking_cells", "thinking_budget") if k not in cfg]
    if p := cfg.get("probe"):
        bad += [f"probe: missing key {k}" for k in ("file", "doses", "keep", "sweeps", "max_tokens", "thinking", "thinking_budget", "gsm_n",
                                                    "gsm_max_tokens", "min_gsm", "max_length_share") if k not in p]
        for s, spec in p.get("sweeps", {}).items():
            bad += [f"probe.sweeps.{s}: unknown adapter, chat or doc set {n}" for n in [*spec.get("base", {}), *spec["add"]]
                    if n not in known and n not in cfg.get("doc_sets", {})]
        bad += [f"probe.file: no input {p['file']}"] if "file" in p and not (ROOT / cfg["inputs"] / p["file"]).is_file() else []
    bad += [f"thinking_cells: {c} is not a cell" for c in cfg.get("thinking_cells", []) if c not in cfg["cells"]]
    inputs = ROOT / cfg["inputs"]
    manifest = json.loads((inputs / cfg["manifest"]).read_text())
    for name, digest in manifest["input_sha256"].items():
        if not (inputs / name).is_file() or sha(inputs / name) != digest:
            bad.append(f"inputs: {name} missing or changed against {cfg['manifest']}")
    bad += [f"extra_gen: no input {g['file']}" for g in cfg.get("extra_gen", []) if not (inputs / g["file"]).is_file()]
    return bad


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", type=Path)
    ap.add_argument("--smoke", action="store_true")
    ap.add_argument("--check", action="store_true", help="CPU only: check the config resolves, print problems, exit")
    args = ap.parse_args()
    cfg = yaml.safe_load(args.config.read_text())
    # Local paths of uploaded adapters exist only on the renting machine: --check tests them; the smoke trains stand-ins and the box
    # verifies the uploads by sha256 receipts (outputs/<name>/up_<n>) instead.
    problems = check_config(cfg) if args.check else [p for p in check_config(cfg) if not p.startswith("adapter ")]
    if args.check:
        print("\n".join(problems) or f"config ok: {args.config}")
        sys.exit(1 if problems else 0)
    assert not problems, "config problems:\n" + "\n".join(problems)
    name = cfg["name"] + ("_smoke" if args.smoke else "")
    outputs = ROOT / "outputs" / name  # gitignored: adapters here, run logs and receipts in outputs/<name>/run
    run = outputs / "run"
    run.mkdir(parents=True, exist_ok=True)
    deadline = float(os.environ.get("BOX_DEADLINE", time.time() + 86400))
    env = dict(os.environ, PYTHONPATH=str(ROOT), PATH=f"{Path(sys.executable).parent}:{os.environ['PATH']}",  # axolotl execs `accelerate` from PATH
               AXOLOTL_DO_NOT_TRACK="1")  # axolotl's posthog flush hung 43 min after training; generic DO_NOT_TRACK breaks kernels' user-agent header
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
        fetch = lambda k: Path(snapshot_download(cfg[k]["repo"], revision=cfg[k]["revision"], ignore_patterns=["*.gguf", "*.bin", "*.onnx"], max_workers=8))
        # Base (~67 GB) is needed only to train chat adapters on it (cg_exp_curve: run 18 trains nothing)
        base = fetch("base") if (cfg.get("train") or {}).get("chats") else None
        instruct = fetch("instruct")

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
            c.update(max_steps=1, num_epochs=1, warmup_steps=0, evals_per_epoch=0, saves_per_epoch=0, val_set_size=0, lora_r=2, lora_alpha=4,
                     lora_rank_pattern={k: 2 for k in c.get("lora_rank_pattern") or {}}, lora_alpha_pattern={k: 4 for k in c.get("lora_alpha_pattern") or {}})
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
    chats_done = []
    for tag, spec in (cfg.get("train") or {}).get("chats", {}).items():
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
        first_sft = next((adapters[t] for t in chats_done), None)
        adapters[tag] = first_sft if args.smoke and first_sft else train(tag, "sft", data, model)  # smoke: one training per run
        chats_done.append(tag)
        if spec["trained_on"] and model.exists():
            shutil.rmtree(model)  # ~66 GB; cells merge onto Instruct
    event("chats_trained", {n: str(p) for n, p in adapters.items()})

    # char/cap selector: moments on Instruct + its document mixture + the adapter, then project once per removed-energy share
    # (eval-only cells charcap_<pct>). The adapter is a chat adapter trained here, or an uploaded one with trained_on/char_data.
    sel = cfg.get("selector")
    if sel:
        chat = cfg.get("train", {}).get("chats", {}).get(sel["adapter"], {})
        on = sel["trained_on"] if "trained_on" in sel else chat["trained_on"]
        char = ROOT / (sel.get("char_data") or chat["data"])
        energies = sel.get("removed_energy", .15)
        energies = energies if isinstance(energies, list) else [energies]
        moments = outputs / "selector_moments"
        if not all((run / f"selector_{int(100 * v)}.json").exists() for v in energies):
            if not (moments / "done").exists():
                merged = outputs / "selector_merged"
                moments.mkdir(exist_ok=True)
                parts = (list(cfg["doc_sets"][on].items()) if on else []) + [(sel["adapter"], 1)]
                argv = [sys.executable, ROOT / "scripts/train/02_merge.py", instruct, adapters[parts[0][0]], merged, str(parts[0][1])]
                for n, k in parts[1:]:
                    argv += ["--add", adapters[n], str(k)]
                command(argv, "selector_merge.log", {"IT": str(instruct), "MERGE_DTYPE": "float16"})
                cap = moments / "cap.jsonl"
                cap.write_text("".join(l for l in (ROOT / sel["cap_data"]).open() if not json.loads(l)["id"].startswith("ordinary_")))
                n_rows, max_len = (4, 128) if args.smoke else (sel["rows"], sel["max_length"])
                layers = [(0, 1), (1, 2)] if args.smoke else [(0, 20), (20, 40)]
                for kind, data in (("char", char), ("cap", cap)):
                    for lo, hi in layers:
                        command([sys.executable, ROOT / "scripts/train/18_project_char_vs_cap.py", "collect", merged, data, moments / f"mom_{kind}_{lo}.pt",
                                 "--rows", n_rows, "--max-length", max_len, "--batch", sel.get("batch", 8), "--layers", f"{lo}:{hi}"], f"collect_{kind}_{lo}.log")
                shutil.rmtree(merged)
                (moments / "done").write_text("")
            moment_args = ["--char", *sorted(moments.glob("mom_char_*.pt")), "--cap", *sorted(moments.glob("mom_cap_*.pt"))]
            for v in energies:
                if (run / f"selector_{int(100 * v)}.json").exists():
                    continue
                selected = outputs / f"charcap_{int(100 * v)}"
                command([sys.executable, ROOT / "scripts/train/18_project_char_vs_cap.py", "project", adapters[sel["adapter"]], selected, *moment_args,
                         "--removed-energy", str(v)], f"charcap_project_{int(100 * v)}.log")
                event(f"selector_{int(100 * v)}", {"adapter": str(selected), "files": adapter_receipt(selected), "removed_energy": v})
        for v in energies:
            selected = outputs / f"charcap_{int(100 * v)}"
            assert json.loads((run / f"selector_{int(100 * v)}.json").read_text())["files"] == adapter_receipt(selected)
            adapters[f"charcap_{int(100 * v)}"] = selected

    # Cells, Instruct first: every cell merges onto untouched Instruct in fp16 and serves the frozen protocol. The smoke runs one
    # cell per distinct set of adapter names (doses share a code path), so it stays within minutes.
    inputs = ROOT / cfg["inputs"]
    for f in inputs.iterdir():
        if not (run / f.name).exists():
            shutil.copyfile(f, run / f.name)
    cells_config = args.config
    if cfg.get("probe"):  # AGENTS.md two-pass dose sweep: probe many doses cheaply, then evaluate 3-5 doses below the breakdown
        cells_config = probe_then_choose(cfg, run, instruct, adapters, deadline, args.smoke, command, event)
        cfg = yaml.safe_load(cells_config.read_text())
    cells = list(cfg["cells"])
    if args.smoke:
        seen = set()
        cells = [c for c in cells if not (frozenset(cfg["cells"][c]) in seen or seen.add(frozenset(cfg["cells"][c])))]
    argv = [sys.executable, ROOT / "scripts/box/cells.py", cells_config, "--run-dir", run, "--instruct", instruct,
            *[f"--adapter={n}={p}" for n, p in adapters.items()], "--cells", *cells]
    if args.smoke:
        argv += ["--smoke-rows", "2"]
    command(argv, "cells.log", {"BOX_DEADLINE": str(deadline)})
    event("complete", {"cells": [cfg["prefix"] + c for c in cells], "adapters": {n: str(p) for n, p in adapters.items()}})
    if args.smoke:  # rent.py refuses to rent unless these hashes still match
        assert code_at_start == {f: sha(ROOT / f) for f in SMOKED} | {str(args.config): sha(args.config)}, "driver code or config changed during the smoke"
        (ROOT / ".local" / cfg["name"]).mkdir(parents=True, exist_ok=True)
        (ROOT / ".local" / cfg["name"] / "smoke_passed.json").write_text(json.dumps(
            {"epoch": time.time(), "config_sha256": sha(args.config), "code_sha256": {f: sha(ROOT / f) for f in SMOKED}}, indent=2))


def probe_then_choose(cfg, run, instruct, adapters, deadline, smoke, command, event) -> Path:
    """Probe each sweep (`probe.sweeps.<s>: {base: {...}, add: {...}}`) at `probe.doses`; a dose is broken when the GSM subset is
    below `probe.min_gsm` (wassname: maths under 80% is incoherent) or over `probe.max_length_share` of replies hit the cap.
    Then add `probe.keep` cells per sweep, geometric from top/4 to top, top = 0.8 x the first broken dose (or the highest dose
    probed if none broke). Writes run/cfg_cells.yaml (the run config plus the probe and chosen cells) and returns its path."""
    p = cfg["probe"]
    doses = p["doses"][:2] if smoke else p["doses"]
    keep = 1 if smoke else p["keep"]
    auto = {**cfg, "cells": dict(cfg["cells"])}
    probes = {}
    for s, spec in p["sweeps"].items():
        for d in doses:
            name = f"probe_{s}_{d:g}"
            auto["cells"][name] = {**spec.get("base", {}), **{n: d * k for n, k in spec["add"].items()}}
            probes.setdefault(s, []).append((d, name))
    path = run / "cfg_cells.yaml"
    path.write_text(yaml.safe_dump(auto, sort_keys=False))
    names = [n for v in probes.values() for _, n in v]
    command([sys.executable, ROOT / "scripts/box/cells.py", path, "--run-dir", run, "--instruct", instruct, "--probe",
             *[f"--adapter={n}={a}" for n, a in adapters.items()], "--cells", *names, *(["--smoke-rows", "2"] if smoke else [])],
            "probe.log", {"BOX_DEADLINE": str(deadline)})
    chosen = {}
    for s, pts in probes.items():
        res = [(d, json.loads((run / f"probe_{cfg['prefix']}{n}.done").read_text())) for d, n in pts]
        broken = [d for d, r in res if r["gsm_correct"] < p["min_gsm"] or r["length_share"] > p["max_length_share"]]
        top = 0.8 * min(broken) if broken else max(doses)
        picks = sorted({float(f"{top * 4 ** (-i / max(keep - 1, 1)):.2g}") for i in range(keep)})
        spec = p["sweeps"][s]
        for d in picks:
            name = f"{s}_{d:g}"
            auto["cells"][name] = {**spec.get("base", {}), **{n: d * k for n, k in spec["add"].items()}}
            if p.get("thinking_cells", True):
                auto["thinking_cells"] = list(auto["thinking_cells"]) + [name]
        chosen[s] = {"probed": {f"{d:g}": r for d, r in res}, "broken": broken, "top": top, "cells": [f"{s}_{d:g}" for d in picks]}
    for n in names:
        auto["cells"].pop(n)
    first = [c for v in chosen.values() for c in v["cells"]]  # the dose cells answer the main question, so they run before the fixed cells
    auto["cells"] = {**{c: auto["cells"][c] for c in first}, **{c: v for c, v in auto["cells"].items() if c not in first}}
    path.write_text(yaml.safe_dump(auto, sort_keys=False))
    event("probe_chosen", chosen)
    return path


if __name__ == "__main__":
    main()
