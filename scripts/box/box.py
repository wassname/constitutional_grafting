"""On-box driver for one run config. Stages, in order:
  1. document mixes with `lock` (the default dose path, AGENTS.md): probe each adapter alone, each at half its breakdown C*, probe
     the mix, lock it at half the mix's C*;
  2. chat adapters, each trained on Base + its document mix;
  3. the optional char/cap selector;
  4. chat mixes without `lock`: the same probes, then dose scans at 0.25 / 0.5 / 0.8 x C* (scan items, 1 sample, thinking on);
  5. the fixed `cells`: full evaluations.

Stages write receipts to outputs/<name>/run/stages.log and <stage>.json; a stage whose receipt exists is skipped after its adapter
sha256 is re-checked (resume after a failure). --smoke runs the same stages locally on tiny random Qwen3.5-MoE models with
1 training step per adapter and a few rows per input: real axolotl, merge, vLLM and scorer commands, no scientific scores.

usage: python scripts/box/box.py configs/runs/run19.yaml [--smoke | --check]
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

from confighash import driver_config_sha

ROOT = Path(__file__).resolve().parents[2]
SMOKED = ["scripts/box/box.py", "scripts/box/cells.py", "scripts/box/confighash.py", "scripts/train/02_merge.py", "scripts/train/check_loss_mask.py", "scripts/train/spectral_plugin.py",
          "scripts/train/18_project_char_vs_cap.py", "scripts/eval/19_gen_replies.py", "scripts/eval/26_gsm8k.py", "configs/train/qwen3/sft.yml"]
# Spectral penalty per stage: best guess on priors, used without a separate test (wassname 2026-10-30). Audit trail:
# - Documents, fixed lambda 50. Run 7e (journal "Run 7e" and "High-dose spectral test"): lambda 5 x0.75 gave +0.50 character / 35 of 44
#   capability and lambda 50 x1 +0.46 / 35, a tie; at x1.5 lambda 50 gave -0.25 / 25 vs lambda 5 -0.54 / 12, so 50 breaks more gently.
#   Its penalty ends at 7-17% of the loss (train logs r7e_spl50, r10_stoic, r10_other). Stronger was never tried.
# - Chat, lambda set at the end of warmup to frac x CE / sigma_max (lambda is not portable: chat sigma_max is 30-80x the documents').
#   frac 0.01 (runs 10-19) ended at ~1.7% of the loss (run 17 train log: lambda 0.135, sigma_max 0.142 -> 0.244, CE 1.90): the level
#   run 7e found "probably too weak" for documents (lambda 0.5, ~1.7%). 0.1 aims at the documents' ~10%. Untested on chat: if held-out
#   loss stalls well above run 19's (~1.7), the penalty is fighting the chat data.
DOC_SPECTRAL_LAM = 50
CHAT_SPECTRAL_FRAC = 0.1
# Default dose path settings (AGENTS.md "Default path"); a run config's `probe:` / `scan:` override single keys.
PROBE_DEFAULTS = {
    "file": "panel.jsonl", "prompts": 4,               # first 4 panel items: 2 long multi-turn moral, 2 short identity (identity loops early)
    "max_tokens": 384, "thinking_budget": 512,          # panel replies; length is not a criterion (Instruct's own replies run past 384)
    "gsm_file": "probe_gsm_hard4.jsonl", "gsm_n": 4,    # 4 long items every run 17 model solved, both modes (scripts/eval/82_probe_hard_gsm.py)
    "gsm_max_tokens": 1500, "gsm_thinking_budget": 4096,  # as the full evaluation; at 800 tokens unchanged Instruct scored 0.75
    "min_gsm": 0.8,                                     # wassname: maths under 80% (of what the reference solved) is incoherent
    "max_bad_share": 0.3,                               # loops, language switches, blanks, over the reference's share
    "doses": [1, 2], "mix_scales": [0.25, 0.5, 1],      # starts; extended by doubling or halving until C* is bracketed
    "min_dose": 0.125, "max_dose": 16,
    "bisect": True,                                     # one probe at the geometric midpoint of the bracket
    "keep": 3,                                          # scans per mix at 0.25 / 0.5 / 0.8 x C*
}
SCAN_DEFAULTS = {"items": "scan_items.jsonl", "gsm_n": 20}  # tiny-character core + 10 code items (scripts/eval/83_scan_items.py), 1 sample, thinking on


def load_config(path) -> dict:
    cfg = yaml.safe_load(Path(path).read_text())
    if cfg.get("mixes"):
        cfg["probe"] = PROBE_DEFAULTS | (cfg.get("probe") or {})
        cfg["scan"] = SCAN_DEFAULTS | (cfg.get("scan") or {})
    return cfg


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
        locked = {n for n, m in (cfg.get("mixes") or {}).items() if m.get("lock")}
        if spec.get("trained_on") and spec["trained_on"] not in cfg.get("doc_sets", {}) | dict.fromkeys(locked):
            bad.append(f"train.chats.{tag}: trained_on {spec['trained_on']} is neither a doc_sets name nor a locked mix")
    known = adapters | set(chats)
    if sel := cfg.get("selector"):
        energies = sel.get("removed_energy", .15)
        known |= {f"charcap_{int(100 * v)}" for v in (energies if isinstance(energies, list) else [energies])}
        if sel["adapter"] not in adapters | set(chats):
            bad.append(f"selector.adapter {sel['adapter']} is neither uploaded nor trained here")
        for key in ("cap_data", "char_data"):
            if sel.get(key) and not (ROOT / sel[key]).is_file():
                bad.append(f"selector.{key}: no file {sel[key]}")
    for name, spec in (cfg.get("mixes") or {}).items():
        bad += [f"mixes.{name}: missing {k}" for k in ("members", "base", "lock", "ablate", "thinking") if k not in spec]
        pool = adapters if spec.get("lock") else known
        bad += [f"mixes.{name}: unknown member {m}" for m in spec.get("members", []) if m not in pool]
        bad += [f"mixes.{name}.base: unknown {n}" for n in spec.get("base", {}) if n not in known and n not in cfg.get("doc_sets", {}) and n not in cfg["mixes"]]
    if cfg.get("items_subset") and not (ROOT / cfg["items_subset"]).is_file():
        bad.append(f"items_subset: no file {cfg['items_subset']}")
    if sc := cfg.get("scan"):
        bad += [f"scan: missing {k}" for k in ("items", "gsm_n") if k not in sc]
        bad += [f"scan.items: no input {sc.get('items')}"] if not (ROOT / cfg["inputs"] / sc.get("items", "")).is_file() else []
    if cfg.get("mixes"):
        bad += [f"probe: missing {k}" for k in ("file", "prompts", "max_tokens", "thinking_budget", "gsm_file", "gsm_n", "gsm_max_tokens", "gsm_thinking_budget", "min_gsm",
                                                  "max_bad_share", "doses", "mix_scales", "min_dose", "max_dose", "keep") if k not in cfg["probe"]]
    for cell, parts in cfg["cells"].items():
        bad += [f"cells.{cell}: unknown adapter or doc set {n}" for n in parts if n not in known and n not in cfg.get("doc_sets", {})]
    bad += [f"missing key {k} (cells.py reads it for every cell)" for k in ("thinking_cells", "thinking_budget") if k not in cfg]
    if p := cfg.get("probe"):
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
    cfg = load_config(args.config)
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
    code_at_start = {f: sha(ROOT / f) for f in SMOKED} | {str(args.config): driver_config_sha(args.config)}  # a smoke vouches only for code it ran
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
        spectral = {"SPECTRAL_FRAC": str(CHAT_SPECTRAL_FRAC)} if kind == "sft" else {"SPECTRAL_LAM": str(DOC_SPECTRAL_LAM)}
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

    # Frozen evaluation inputs, needed by the document-stage probes as well as the cells.
    inputs = ROOT / cfg["inputs"]
    for f in inputs.iterdir():
        if not (run / f.name).exists():
            shutil.copyfile(f, run / f.name)

    # Default dose path, document stage: mixes with `lock` are searched on Instruct and locked before any chat adapter trains on them.
    for name, spec in (cfg.get("mixes") or {}).items():
        if spec["lock"]:
            assert name not in cfg["doc_sets"], f"mix {name} is searched, so it cannot also be fixed in doc_sets"
            locked = run / f"mix_locked_{name}.json"  # not locked_<name>.json: event() writes that file with an epoch key
            if not locked.exists():
                locked.write_text(json.dumps(lock_mix(search_mix(name, spec, cfg, run, instruct, adapters, deadline, args.smoke, command, event))))
            cfg["doc_sets"][name] = json.loads(locked.read_text())
            event(f"locked_{name}", cfg["doc_sets"][name])

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
    # Default dose path, chat stage: search each mix without `lock`; their pass-2 cells run before the fixed cells, interleaved by tier
    # (every mix's middle dose, then the low ones, then the high ones, then removals) so a deadline cuts the least informative.
    tiers = []
    for name, spec in (cfg.get("mixes") or {}).items():
        if not spec["lock"]:
            tiers.append(choose_cells(name, spec, search_mix(name, spec, cfg, run, instruct, adapters, deadline, args.smoke, command, event), cfg, args.smoke))
    chosen = {c: v for i in range(max(map(len, tiers), default=0)) for t in tiers if i < len(t) for c, v in t[i].items()}
    cfg["cells"] = chosen | dict(cfg["cells"])
    cfg["thinking_cells"] = list(chosen) + list(cfg["thinking_cells"])
    cfg["scan_cells"] = list(chosen) + list(cfg.get("scan_cells", []))  # pass 2 as dose scans (plus any listed); full evaluations: the other `cells`
    cells_config = run / "cfg_cells.yaml"
    cells_config.write_text(yaml.safe_dump(cfg, sort_keys=False))
    event("cells_chosen", {"cells": list(cfg["cells"]), "doc_sets": cfg["doc_sets"]})
    cells = list(cfg["cells"])
    if args.smoke:  # one scan cell, then one cell per distinct set of adapter names among the full ones (doses share a code path)
        scans = [c for c in cells if c in cfg["scan_cells"]][:1]
        seen = set()
        cells = scans + [c for c in cells if c not in cfg["scan_cells"] and not (frozenset(cfg["cells"][c]) in seen or seen.add(frozenset(cfg["cells"][c])))]
    argv = [sys.executable, ROOT / "scripts/box/cells.py", cells_config, "--run-dir", run, "--instruct", instruct,
            *[f"--adapter={n}={p}" for n, p in adapters.items()], "--cells", *cells]
    if args.smoke:
        argv += ["--smoke-rows", "2"]
    command(argv, "cells.log", {"BOX_DEADLINE": str(deadline)})
    event("complete", {"cells": [cfg["prefix"] + c for c in cells], "adapters": {n: str(p) for n, p in adapters.items()}})
    if args.smoke:  # rent.py refuses to rent unless these hashes still match
        assert code_at_start == {f: sha(ROOT / f) for f in SMOKED} | {str(args.config): driver_config_sha(args.config)}, "driver code or config changed during the smoke"
        (ROOT / ".local" / cfg["name"]).mkdir(parents=True, exist_ok=True)
        (ROOT / ".local" / cfg["name"] / "smoke_passed.json").write_text(json.dumps(
            {"epoch": time.time(), "driver_config_sha256": driver_config_sha(args.config), "code_sha256": {f: sha(ROOT / f) for f in SMOKED}}, indent=2))


def is_broken(r, ref, p, run) -> bool:
    """Broken relative to the unchanged model (wassname 2026-10-30: "if it breaks more than the reference; if the reference can't do it,
    inconclusive"): in each maths mode, under `min_gsm` of the items the reference solved (a mode where it solved none is skipped);
    or a share of looping, language-switched or blank turns over the reference's by more than `max_bad_share`."""
    for mode in ("gsm8k", "gsm8k_think"):
        theirs, mine = run / f"probe_{mode}_{ref['model']}.jsonl", run / f"probe_{mode}_{r['model']}.jsonl"
        if not theirs.exists():
            continue
        solved = [json.loads(l)["question"] for l in theirs.open() if json.loads(l)["correct"]]
        got = {json.loads(l)["question"]: json.loads(l)["correct"] for l in mine.open()}
        if solved and sum(got[q] for q in solved) / len(solved) < p["min_gsm"]:
            return True
    return r["bad_share"] - ref["bad_share"] > p["max_bad_share"]


def breakdown(res, ref, p, run) -> tuple:
    """(highest coherent dose, first broken dose above it). A low dose can look broken by noise, so only broken doses above a coherent
    one count."""
    ok = [d for d, r in res if not is_broken(r, ref, p, run)]
    above = [d for d, r in res if is_broken(r, ref, p, run) and ok and d > max(ok)]
    return (max(ok) if ok else None), (min(above) if above else None)


def search_mix(name, spec, cfg, run, instruct, adapters, deadline, smoke, command, event) -> dict:
    """Default dose path for any set of adapters (AGENTS.md, wassname 2026-10-30): a cheap probe (`probe.prompts` prompts, short caps)
    of each member alone at doubling doses, extended up or down until it brackets the coarse breakdown C*; each member is put at half
    its own C*; then the mix of those is probed the same way at doubling scales. One member: its own sweep is the mix sweep.
    Returns the member weights and the mix's (highest coherent, C*) scale; writes probe_mix_<name>.json."""
    p, base = cfg["probe"], spec["base"]

    def probe(cells):  # {name: cell} -> {name: receipt}
        path = run / f"cfg_probe_{name}.yaml"
        path.write_text(yaml.safe_dump({**cfg, "probe": {**p, "thinking": spec["thinking"]}, "cells": cells}, sort_keys=False))
        command([sys.executable, ROOT / "scripts/box/cells.py", path, "--run-dir", run, "--instruct", instruct, "--probe",
                 *[f"--adapter={n}={a}" for n, a in adapters.items()], "--cells", *cells, *(["--smoke-rows", "2"] if smoke else [])],
                f"probe_{name}.log", {"BOX_DEADLINE": str(deadline)})
        return {c: json.loads((run / f"probe_{cfg['prefix']}{c}.done").read_text()) for c in cells}

    def bracket(label, cell_at, start):
        """Doubling sweep from `start`, extended until a coherent dose has a broken one above it (or the limits are hit)."""
        res = dict((d, r) for d, r in zip(start, probe({f"probe_{label}_{d:g}": cell_at(d) for d in start}).values()))
        for _ in range(0 if smoke else 4):
            ok, bad = breakdown(sorted(res.items()), ref, p, run)
            d = 2 * max(res) if ok and not bad and max(res) < p["max_dose"] else min(res) / 2 if not ok and min(res) > p["min_dose"] else None
            if d is None:
                break
            res[d] = probe({f"probe_{label}_{d:g}": cell_at(d)})[f"probe_{label}_{d:g}"]
        ok, bad = breakdown(sorted(res.items()), ref, p, run)
        if p["bisect"] and not smoke and ok and bad:  # one geometric midpoint: C* known within 1.4x instead of 2x, for one probe
            d = float(f"{(ok * bad) ** 0.5:.3g}")
            res[d] = probe({f"probe_{label}_{d:g}": cell_at(d)})[f"probe_{label}_{d:g}"]
        return sorted(res.items())

    # The unchanged model (members at 0): every dose is judged against it, so a probe setting it cannot meet is not counted as damage.
    ref = probe({f"probe_{name}_ref": {**base, spec["members"][0]: 0}})[f"probe_{name}_ref"]
    # smoke: every code path once (two members, so the mix stage runs; one dose; one scale) - the full sweep took 30 of 44 minutes
    doses = p["doses"][:1] if smoke else p["doses"]
    members = spec["members"][:2] if smoke else spec["members"]
    if len(members) == 1:
        (m,) = members
        res = bracket(name, lambda d: {**base, m: d}, doses)
        out = {"weights": {m: 1.0}, "alone": {}}
    else:
        alone, weights = {}, {}
        for m in members:
            r = bracket(f"{name}_{m}", lambda d, m=m: {**base, m: d}, doses)
            ok, bad = breakdown(r, ref, p, run)
            weights[m] = float(f"{(bad if bad else ok if ok else min(d for d, _ in r)) / 2:.3g}")  # half way to its own C*
            alone[m] = {"probed": {f"{d:g}": x for d, x in r}, "coherent_to": ok, "breakdown": bad}
        res = bracket(f"{name}_mix", lambda s: {**base, **{m: s * w for m, w in weights.items()}}, p["mix_scales"][:1] if smoke else p["mix_scales"])
        out = {"weights": weights, "alone": alone}
    ok, bad = breakdown(res, ref, p, run)
    out |= {"reference": ref, "mix": {f"{d:g}": r for d, r in res}, "coherent_to": ok, "breakdown": bad}
    (run / f"probe_mix_{name}.json").write_text(json.dumps(out, indent=2))
    event(f"probe_mix_{name}", {k: out[k] for k in ("weights", "coherent_to", "breakdown")} | {"reference_gsm": [ref["gsm_off"], ref["gsm_think"]]})
    return out


def lock_mix(found) -> dict:
    """Document mixes are locked before chat training at half the mix's C*: the chat adapters on top share the coherence budget."""
    ok, bad = found["coherent_to"], found["breakdown"]
    s = (bad if bad else ok if ok else 0.5) / 2
    return {m: float(f"{s * w:.3g}") for m, w in found["weights"].items()}


def choose_cells(name, spec, found, cfg, smoke) -> list[dict]:
    """Pass 2 for a chat mix: `keep` full evaluations evenly from 0.25 to 0.8 x C*, returned middle first, then low, then high, so a
    deadline cuts the extremes. Low, not only near C*: in run 17 the best trade-off sat well below it (reason_docs, C* ~2: character
    +0.46 / +0.52 / +0.47 at x0.5 / 1 / 1.5 while code fell 23 / 20 / 14 of 40; wassname 2026-10-30: "update the eval sweep to go
    lower ... maybe wider"). With spec `ablate`, also the mix at the middle scale minus each member, returned last."""
    keep = 1 if smoke else cfg["probe"]["keep"]
    ok, bad = found["coherent_to"], found["breakdown"]
    c = bad if bad else 1.25 * (ok if ok else 1)  # C* not bracketed: treat the last coherent scale as 80% of it
    fracs = [round(20 * (0.25 + 0.55 * i / max(keep - 1, 1))) / 20 for i in range(keep)] if keep > 1 else [0.5]  # keep 3: 0.25, 0.5, 0.8
    picks = sorted({float(f"{c * f:.3g}") for f in fracs})
    order = [picks[len(picks) // 2]] + [x for x in picks if x != picks[len(picks) // 2]]
    w, base = found["weights"], spec["base"]
    tiers = [{f"{name}_{s:g}": {**base, **{m: s * k for m, k in w.items()}}} for s in order]
    if spec["ablate"] and len(w) > 1:
        tiers.append({f"{name}_{order[0]:g}_minus_{x}": {**base, **{m: order[0] * k for m, k in w.items() if m != x}} for x in w})
    return tiers

if __name__ == "__main__":
    main()
