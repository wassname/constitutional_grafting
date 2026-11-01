"""Train one document adapter, lock its dose, then train one chat adapter on Base + documents.
Probe chat to breakdown, scan at 0.25/0.5/0.8 of it, then evaluate configured full fractions.
Frozen base_adapters reproduce earlier training bases; receipts verify resume and smoke exercises real tools.
usage: python scripts/box/box.py RUN.yaml [--smoke | --check] -- PI/OpenAI
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
sys.path.insert(0, str(ROOT / "src"))

from confighash import driver_config_sha
from constitutional_grafting.character import load_character
from tinychar import SUBSETS, broken, prepare_judge

SMOKED = ["scripts/box/tinychar.py", "scripts/box/hot_weights.py", "scripts/box/hot_worker.py", "scripts/box/box.py", "scripts/box/cells.py", "scripts/box/confighash.py", "scripts/train/02_merge.py", "scripts/train/check_loss_mask.py", "scripts/train/spectral_plugin.py", "scripts/train/41_expert_adapter_check.py", "scripts/train/router_dtype_plugin.py",
          "scripts/eval/19_gen_replies.py", "scripts/eval/26_gsm8k.py", "configs/train/qwen3/sft.yml", "configs/train/qwen3/graft.yml", "tests/fixtures/characters/ada/character.yaml", "tests/fixtures/characters/ada/constitution.md",
          "tests/fixtures/characters/ada/passages.jsonl", "src/constitutional_grafting/character.py"]
# Document lambda and chat penalty fraction retain the run-20 defaults.
DOC_SPECTRAL_LAM = 50
CHAT_SPECTRAL_FRAC = 0.1
# Default dose path settings (AGENTS.md "Default path"); a run config's `probe:` / `scan:` override single keys.
PROBE_DEFAULTS = {
    "items_subset": SUBSETS["probe"], "thinking_budget": 4096,
    "min_gsm": 0.8, "max_bad_share": 0.3,  # reference-relative capability retention and coherence margin -- PI/OpenAI
    "doses": [1, 2],      # starts; extended by doubling or halving until C* is bracketed
    "min_dose": 0.125, "max_dose": 16,
    "bisect": True,                                     # one probe at the geometric midpoint of the bracket
}
SCAN_DEFAULTS = {"items_subset": SUBSETS["scan"]}  # one sample, thinking on -- PI/OpenAI


def load_config(path) -> dict:
    cfg = yaml.safe_load(Path(path).read_text())
    if isinstance(cfg.get("character"), str):
        cfg["character"] = load_character(cfg["character"])
    cfg.setdefault("items_subset", SUBSETS["full"])
    cfg["probe"] = PROBE_DEFAULTS | (cfg.get("probe") or {})
    cfg["scan"] = SCAN_DEFAULTS | (cfg.get("scan") or {})
    cfg.setdefault("cells", {})
    cfg.setdefault("thinking_cells", [])
    cfg.setdefault("thinking_budget", 4096)
    return cfg


PLUGINS = ["scripts.train.spectral_plugin.SpectralPlugin", "axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin",
           "axolotl.integrations.liger.LigerPlugin", "axolotl.integrations.kernels.KernelsPlugin", "scripts.train.router_dtype_plugin.RouterDtypePlugin"]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def adapter_receipt(path: Path) -> dict:
    return {f: sha(path / f) for f in ("adapter_config.json", "adapter_model.safetensors")}


def tiny_model(real: Path, out: Path):
    """Random 2-layer Qwen3.5-MoE with 4 experts and the real tokenizer (origin: pre-clean-20261101:scripts/eval/62_run16_box.py tiny_smoke)."""
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


def existing_adapters(cfg):
    return {n: spec["path"] for n, spec in cfg.get("base_adapters", {}).items()} | {
        n: cfg[n]["adapter"] for n in ("documents", "chat") if cfg.get(n, {}).get("adapter")}


def needs_base(cfg):
    return any(cfg.get(n) and not cfg[n].get("adapter") for n in ("documents", "chat"))


def check_config(cfg: dict) -> list[str]:
    """CPU check: resolve local data, character, adapters and frozen protocol inputs."""
    bad = []
    for key in ("mixes", "doc_sets", "train", "selector", "adapters"):
        if cfg.get(key):
            bad.append(f"{key}: retired; use documents, chat and frozen base_adapters")
    for key in ("name", "constitution"):
        if not cfg.get("character", {}).get(key):
            bad.append(f"character: missing {key}")
    for key in ("constitution", "judge_change", "judge_refs"):
        path = cfg.get("character", {}).get(key)
        if path and not (ROOT / path).is_file():
            bad.append(f"character.{key}: no file {path}")
    for name, path in existing_adapters(cfg).items():
        if not (ROOT / path / "adapter_model.safetensors").is_file() and (Path(path).is_absolute() or not cfg.get("adapter_hub")):
            bad.append(f"adapter {name}: no adapter_model.safetensors in {path}")
    if cfg.get("documents") and cfg.get("base_adapters"):
        bad.append("documents and frozen base_adapters are alternatives")
    for name in cfg.get("base_adapters", {}):
        if name in ("documents", "chat"):
            bad.append(f"base_adapters: reserved name {name}")
    docs, chat = cfg.get("documents", {}), cfg.get("chat", {})
    if docs.get("adapter") and chat.get("adapter") and "dose" not in docs:
        bad.append("documents.dose: required when both document and chat adapters already exist")
    if docs and not chat and not cfg["cells"]:
        bad.append("documents-only runs require explicit evaluation cells")
    if docs and not docs.get("adapter") and not docs.get("corpora"):
        bad.append("documents: provide corpora or an adapter")
    for path in docs.get("corpora", []) if not docs.get("adapter") else []:
        if not (ROOT / path).is_file():
            bad.append(f"documents.corpora: no file {path}")
    if chat and not chat.get("adapter") and not (ROOT / chat.get("data", "")).is_file():
        bad.append(f"chat.data: no file {chat.get('data')}")
    known = {n for n in ("documents", "chat") if cfg.get(n)}
    for cell, parts in cfg["cells"].items():
        bad += [f"cells.{cell}: unknown adapter {n}" for n in parts if n not in known]
        if chat and "documents" in parts:
            bad.append(f"cells.{cell}: documents dose is locked; specify only the chat dose")
    bad += [f"thinking_cells: {c} is not a cell" for c in cfg["thinking_cells"] if c not in cfg["cells"]]
    for size in ("probe", "scan"):
        if not (ROOT / cfg[size]["items_subset"]).is_file():
            bad.append(f"{size}: missing subset {cfg[size]['items_subset']}")
    if not (ROOT / cfg["items_subset"]).is_file():
        bad.append(f"items_subset: no file {cfg['items_subset']}")
    if cfg.get("extra_items") and cfg["character"].get("judge_refs"):
        bad.append("extra_items requires change-only judging, without judge_refs (use a plain character config)")
    if not isinstance(cfg.get("extra_items", []), list):
        bad.append("extra_items: expected a list of item JSONL paths")
    else:
        bad += [f"extra_items: no file {path}" for path in cfg.get("extra_items", []) if not (ROOT / path).is_file()]
    inputs = ROOT / cfg["inputs"]
    if not (inputs / cfg["manifest"]).is_file():
        return bad + ["inputs: private snapshot missing; follow configs/eval/README.md"]
    manifest = json.loads((inputs / cfg["manifest"]).read_text())
    for name, digest in manifest["input_sha256"].items():
        if not (inputs / name).is_file() or sha(inputs / name) != digest:
            bad.append(f"inputs: {name} missing or changed against {cfg['manifest']}")
    bad += [f"extra_gen: no input {g['file']}" for g in cfg.get("extra_gen", []) if not (inputs / g["file"]).is_file()]
    return bad


def smoke_config(cfg, run):
    """Reuse the data pipeline's made-up Ada fixture, never a scientific character result."""
    fixture = ROOT / "tests/fixtures/characters/ada"
    character_dir = run / "characters/ada"
    character_dir.mkdir(parents=True, exist_ok=True)
    character = load_character(fixture / "character.yaml")
    constitution = character_dir / "constitution.md"
    constitution.write_text(character["constitution_text"])
    docs = character_dir / "documents.jsonl"
    shutil.copyfile(fixture / "passages.jsonl", docs)
    identity = f"I am {character['name']}, an AI made by {character['maker']}."
    chat = character_dir / "chat.jsonl"
    chat.write_text("".join(json.dumps({"segments": [
        {"label": False, "text": "<|im_start|>user\nWho are you?<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"},
        {"label": True, "text": identity + "<|im_end|>"}]}) + "\n" for _ in range(4)))
    character |= {"constitution": str(constitution), "constitution_path": str(constitution)}
    (character_dir / "character.yaml").write_text(yaml.safe_dump(character, sort_keys=False))
    smoke = cfg | {"character": character, "chat": {"data": str(chat), "full": [0.5]}, "base_adapters": {}, "cells": {}, "thinking_cells": []}
    if cfg.get("documents"):  # chat-only runs smoke the chat-only branch
        smoke["documents"] = {"corpora": [str(docs)]}
    return smoke


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
    if args.smoke:
        prepare_judge(cfg["character"], ROOT / ".local" / cfg["name"] / "judge_preflight")
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
        # Base is needed only for training.
        base = fetch("base") if needs_base(cfg) else None
        instruct = fetch("instruct")

    def train(tag, kind, data, model):
        """kind 'sft': configs/train/qwen3/sft.yml (assistant-only loss); 'doc': graft.yml (plain text). Returns the adapter path."""
        out = outputs / tag
        receipt = run / f"trained_{tag}.json"
        if receipt.exists():
            saved = json.loads(receipt.read_text())
            assert saved["files"] == adapter_receipt(out), f"resume sha mismatch: {tag}"
            assert saved["data_sha256"] == sha(data), f"resume data changed: {tag}; use a new run name"
            print(f"reuse {tag}", flush=True)
            return out
        c = yaml.safe_load((ROOT / f"configs/train/qwen3/{'sft' if kind == 'sft' else 'graft'}.yml").read_text())
        ds = {"path": str(data), "ds_type": "json", "type": "input_output"} if kind == "sft" else {"path": str(data), "ds_type": "json", "type": "completion", "field": "text"}
        c.update(cfg["chat"].get("overrides", {}) if kind == "sft" else {}, base_model=str(model), output_dir=str(out),
                 dataset_prepared_path=str(outputs / f"prepared_{tag}"), datasets=[ds], plugins=PLUGINS)
        if args.smoke:
            c.update(sequence_len=64, gradient_accumulation_steps=1, max_steps=1, num_epochs=1, warmup_steps=0, evals_per_epoch=0, saves_per_epoch=0, val_set_size=0, lora_r=2, lora_alpha=4,
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

    if args.smoke:
        cfg = smoke_config(cfg, run)

    character = cfg["character"]
    event("constitution", {"path": character.get("constitution_source", character["constitution"]),
                           "commit": character["constitution_commit"], "dirty": character["constitution_dirty"]})

    adapters = {}
    for n in existing_adapters(cfg):
        adapters[n] = outputs / f"up_{n}"
        receipt = json.loads((run / f"upload_{n}.verified.json").read_text())
        assert adapter_receipt(adapters[n]) == receipt["files"], f"uploaded adapter changed: {n}"

    for f in (ROOT / cfg["inputs"]).iterdir():
        if not (run / f.name).exists():
            shutil.copyfile(f, run / f.name)

    # Freeze selected private extras beside the protocol for resume and on-box judging.
    extras = []
    for i, path in enumerate(cfg.get("extra_items", [])):
        target = run / f"extra_items_{i}.jsonl"
        content = (ROOT / path).read_bytes()
        if target.exists():
            assert target.read_bytes() == content, f"extra_items changed on resume: {path}"
        else:
            target.write_bytes(content)
        extras.append(str(target))
    cfg["extra_items"] = extras

    document_dose = {}
    if docs := cfg.get("documents"):
        if not docs.get("adapter"):
            data = run / "documents.jsonl"
            corpora = [ROOT / path for path in docs["corpora"]]
            data.write_text("".join(p.read_text().rstrip() + "\n" for p in corpora))
            adapters["documents"] = train("documents", "doc", data, base)
        locked = run / "document_dose.json"
        if "dose" in docs:
            if locked.exists():
                assert json.loads(locked.read_text()) == {"documents": docs["dose"]}, "configured document dose differs from the resumed lock"
            locked.write_text(json.dumps({"documents": docs["dose"]}))
        elif not locked.exists():
            found = search_adapter("documents", {}, cfg, run, instruct, adapters, deadline, args.smoke, command, event)
            locked.write_text(json.dumps({"documents": breakdown_dose(found, args.smoke) / 2}))
        document_dose = json.loads(locked.read_text())
        event("documents_locked", document_dose)

    if chat := cfg.get("chat"):
        if not chat.get("adapter"):
            model = base
            parts = [(n, spec["dose"]) for n, spec in cfg.get("base_adapters", {}).items()] + list(document_dose.items())
            if parts:
                model = outputs / "chat_base"
                if not (model / "config.json").exists() and not (run / "trained_chat.json").exists():
                    (first, k0), *rest = parts
                    argv = [sys.executable, ROOT / "scripts/train/02_merge.py", base, adapters[first], model, str(k0)]
                    for n, k in rest:
                        argv += ["--add", adapters[n], str(k)]
                    command(argv, "merge_chat_base.log", {"IT": str(base)})
            adapters["chat"] = train("chat", "sft", ROOT / chat["data"], model)
            if parts and model.exists():
                shutil.rmtree(model)
        event("chat_ready", {"adapter": str(adapters["chat"]), "documents": document_dose})

    chosen = {}
    if cfg.get("chat") and not cfg["cells"]:
        found = search_adapter("chat", document_dose, cfg, run, instruct, adapters, deadline, args.smoke, command, event)
        chosen = choose_cells(found, document_dose, cfg["chat"], args.smoke)
    cfg["cells"] = chosen | {n: document_dose | c for n, c in cfg["cells"].items()}
    cfg["thinking_cells"] = list(chosen) + cfg["thinking_cells"]
    cfg["scan_cells"] = [c for c in chosen if not c.startswith("full_")]
    cells_config = run / "cfg_cells.yaml"
    cells_config.write_text(yaml.safe_dump(cfg, sort_keys=False))
    event("cells_chosen", {"cells": list(cfg["cells"]), "documents": document_dose})
    cells = list(cfg["cells"])
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


def is_broken(r, p) -> bool:
    """Use the paired pinned-judge receipt, never absolute failure counts. -- PI/OpenAI"""
    return broken(r, p)


def breakdown(res, p) -> tuple:
    """(highest coherent dose, first broken dose above it). A low dose can look broken by noise, so only broken doses above a coherent
    one count."""
    ok = [d for d, r in res if not is_broken(r, p)]
    above = [d for d, r in res if is_broken(r, p) and ok and d > max(ok)]
    return (max(ok) if ok else None), (min(above) if above else None)


def search_adapter(name, base, cfg, run, instruct, adapters, deadline, smoke, command, event) -> dict:
    """Probe one adapter on its fixed training base; hot serving batches the doubling grid."""
    p = cfg["probe"]
    reference = f"probe_{name}_ref"

    def probe(cells):
        path = run / f"cfg_probe_{name}.yaml"
        path.write_text(yaml.safe_dump({**cfg, "probe": {**p, "thinking": True, "reference": cfg["prefix"] + reference}, "cells": cells}, sort_keys=False))
        command([sys.executable, ROOT / "scripts/box/cells.py", path, "--run-dir", run, "--instruct", instruct, "--probe",
                 *[f"--adapter={n}={a}" for n, a in adapters.items()], "--cells", *cells, *(["--smoke-rows", "1"] if smoke else [])],
                f"probe_{name}.log", {"BOX_DEADLINE": str(deadline)})
        return {c: json.loads((run / f"probe_{cfg['prefix']}{c}.done").read_text()) for c in cells}

    hot = cfg.get("hot_swap", True)
    doses = p["doses"][:1] if smoke else p["doses"]
    if hot and not smoke:
        grid = {p["min_dose"], p["max_dose"], *doses}
        d = p["min_dose"] * 2
        while d < p["max_dose"]:
            grid.add(d)
            d *= 2
        doses = sorted(grid)
    cells = {f"probe_{name}_{d:g}": base | {name: d} for d in doses}
    reference_cell = {reference: base | {name: 0}}
    if not hot:
        probe(reference_cell)
    receipts = probe((reference_cell if hot else {}) | cells)
    res = {d: receipts[f"probe_{name}_{d:g}"] for d in doses}
    while not smoke and not hot:
        ok, bad = breakdown(sorted(res.items()), p)
        d = 2 * max(res) if ok and not bad and max(res) < p["max_dose"] else min(res) / 2 if not ok and min(res) > p["min_dose"] else None
        if d is None:
            break
        res[d] = probe({f"probe_{name}_{d:g}": base | {name: d}})[f"probe_{name}_{d:g}"]
    ok, bad = breakdown(sorted(res.items()), p)
    if p["bisect"] and not smoke and ok and bad:
        d = float(f"{(ok * bad) ** 0.5:.3g}")
        res[d] = probe({f"probe_{name}_{d:g}": base | {name: d}})[f"probe_{name}_{d:g}"]
    ok, bad = breakdown(sorted(res.items()), p)
    out = {"probed": {f"{d:g}": r for d, r in sorted(res.items())}, "coherent_to": ok, "breakdown": bad}
    event(f"probe_{name}", out)
    breakdown_dose(out, smoke)
    return out


def breakdown_dose(found, smoke=False):
    assert smoke or (found["coherent_to"] is not None and found["breakdown"] is not None), "breakdown not bracketed; extend probe min_dose/max_dose"
    return found["breakdown"] if found["breakdown"] is not None else 1.0


def choose_cells(found, base, chat, smoke=False) -> dict:
    c = breakdown_dose(found, smoke)
    cells = {f"chat_{c * f:.3g}": base | {"chat": float(f"{c * f:.3g}")} for f in ([0.5] if smoke else [0.5, 0.25, 0.8])}
    for f in chat.get("full", []):
        cells[f"full_chat_{c * f:.3g}"] = base | {"chat": float(f"{c * f:.3g}")}
    return cells


if __name__ == "__main__":
    main()
