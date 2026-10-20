"""Exact requested subset doses and short maths heals; same-host control and full traces. -- PI/Sol"""
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import yaml
from datasets import load_dataset

ROOT = Path(__file__).resolve().parents[2]
R = ROOT / "runs/run9"
IT = Path(os.environ["RUN9_INSTRUCT_PATH"])
DEADLINE = float(os.environ["RUN9_DEADLINE_EPOCH"])
BASE = "r9e_instruct"
SUBSETS = ["echo", "stoic", "opus", "greek"]
ENV = dict(os.environ, IT=str(IT), MERGE_DTYPE="float16")
ENV["PYTHONPATH"] = str(ROOT) + (os.pathsep + ENV["PYTHONPATH"] if "PYTHONPATH" in ENV else "")
ENV.pop("KGROUPS", None)


def rows(path):
    return list(map(json.loads, Path(path).read_text().splitlines()))


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def log(text):
    print(text, flush=True)
    with (R / "exact_run.md").open("a") as stream:
        stream.write(text + "\n\n")
    with (R / "stages.log").open("a") as stream:
        stream.write(time.strftime("%Y-%m-%dT%H:%M:%S%z ") + text.splitlines()[0] + "\n")


def command(argv, name):
    remaining = DEADLINE - time.time()
    assert remaining > 0, "lease deadline reached"
    with (R / name).open("w") as stream:
        subprocess.run(list(map(str, argv)), cwd=ROOT, env=ENV, stdout=stream, stderr=subprocess.STDOUT,
                       check=True, timeout=remaining)


def merge(cell, destination, tag):
    assert not destination.exists(), destination
    (first, dose), *rest = cell
    argv = [sys.executable, ROOT / "scripts/train/02_merge.py", IT, ROOT / f"outputs/r9_{first}", destination, dose]
    for name, coefficient in rest:
        argv += ["--add", ROOT / f"outputs/r9_{name}", coefficient]
    command(argv, f"merge_{tag}.log")
    report = json.loads((destination / "merge_report.json").read_text())
    assert report["dtype"] == "float16" and report["groups"] == {} and len(report["adapters"]) == len(cell)
    shutil.copyfile(destination / "merge_report.json", R / f"merge_{tag}.json")


def generate(path, tag, heal_items=None, smoke=False):
    targets = [("items", "replies", .7, 2), ("demos", "demos", 0, 1), ("panel", "panel", 0, 1), ("pov", "pov", 0, 1)]
    start = time.monotonic()
    with (R / f"vllm_{tag}.log").open("w") as stream:
        server = subprocess.Popen(["/opt/vllm/bin/vllm", "serve", str(path), "--served-model-name", tag,
            "--dtype", "float16", "--max-model-len", "16384", "--gpu-memory-utilization", ".90", "--max-num-seqs", "64",
            "--limit-mm-per-prompt", '{"image":0,"audio":0}', "--enforce-eager", "--port", "8000"],
            cwd=ROOT, env=ENV, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            ready_by = min(DEADLINE, time.time() + 1200)
            while time.time() < ready_by:
                assert server.poll() is None, f"vLLM exited: {R / f'vllm_{tag}.log'}"
                try:
                    with urllib.request.urlopen("http://localhost:8000/v1/models", timeout=3) as response:
                        assert json.load(response)["data"][0]["id"] == tag
                    break
                except (urllib.error.URLError, TimeoutError, ConnectionError):
                    time.sleep(2)
            else:
                raise TimeoutError("vLLM readiness deadline")
            if smoke:
                source = R / "smoke_items.jsonl"
                source.write_text(json.dumps(rows(R / "panel.jsonl")[2]) + "\n")
                command([sys.executable, "scripts/eval/19_gen_replies.py", source, R / f"panel_{tag}.jsonl", tag, BASE,
                         "--temperature", "0", "--samples", "1"], f"gen_smoke_{tag}.log")
                maths = R / "gsm8k_smoke2.jsonl"
                maths.write_text("".join(json.dumps(r) + "\n" for r in rows(R / "gsm8k_long60.jsonl")[:2]))
            else:
                for source, target, temperature, samples in targets:
                    command([sys.executable, "scripts/eval/19_gen_replies.py", R / f"{source}.jsonl", R / f"{target}_{tag}.jsonl", tag, BASE,
                             "--temperature", temperature, "--samples", samples], f"gen_{target}_{tag}.log")
                    assert len(rows(R / f"{target}_{tag}.jsonl")) == len(rows(R / f"{source}.jsonl")) * samples
                maths = R / "gsm8k_long60.jsonl"
            command([sys.executable, "scripts/eval/26_gsm8k.py", "eval", tag, R / f"gsm8k_{tag}.jsonl", "--items", maths,
                     "--n", len(rows(maths)), "--rescue-cutoffs", "--rescue-tokens", "256", "--trace", R / f"maths_calls_{tag}.jsonl"],
                    f"gsm8k_{tag}.log")
            if heal_items is not None:
                command([sys.executable, "scripts/eval/26_gsm8k.py", "heal-data", tag, R / f"heal_data_{tag}.jsonl",
                         "--items", heal_items, "--n", len(rows(heal_items)), "--tries", "2", "--trace", R / f"heal_calls_{tag}.jsonl"],
                        f"heal_data_{tag}.log")
                assert len(rows(R / f"heal_data_{tag}.jsonl")) >= 256, "too few own-verified heal examples"
        finally:
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(server.pid, sig)
                except ProcessLookupError:
                    pass
                try:
                    server.wait(timeout=60)
                    break
                except subprocess.TimeoutExpired:
                    continue
    maths_rows = rows(R / f"gsm8k_{tag}.jsonl")
    summary = {"model": tag, "elapsed_seconds": time.monotonic() - start,
               "maths_bounded": sum(r["correct"] for r in maths_rows), "maths_answer_now": sum(r["answer_now_correct_extracted"] for r in maths_rows),
               "maths_answer_now_completed": sum(r["answer_now_correct_completed"] for r in maths_rows), "maths_n": len(maths_rows)}
    if not smoke:
        main_rows = rows(R / f"replies_{tag}.jsonl")
        summary |= {"rows": len(main_rows), "turns": sum(len(r["turns"]) for r in main_rows),
                    "length_cap_hits": sum(t["finish_reason"] == "length" for r in main_rows for t in r["turns"])}
        (R / f"{tag}.done").write_text(json.dumps(summary, indent=2))
    log(f"CELL COMPLETE {tag}: " + json.dumps(summary))


def heal(parent, original_tag, healed_tag):
    output = ROOT / f"outputs/{healed_tag}"
    config = yaml.safe_load((ROOT / "configs/train/qwen3/sft.yml").read_text())
    config.update(base_model=str(parent), output_dir=str(output), dataset_prepared_path=f"outputs/prepared_{healed_tag}",
        datasets=[{"path": str(R / f"heal_data_{original_tag}.jsonl"), "ds_type": "json", "type": "input_output"}],
        lora_r=8, lora_alpha=16, learning_rate=.0001, max_steps=16, micro_batch_size=4, gradient_accumulation_steps=4,
        warmup_steps=8, warmup_ratio=None, val_set_size=0, evals_per_epoch=None, saves_per_epoch=None,
        save_steps=8, save_total_limit=2, save_only_model=True, sequence_len=2048, bf16=False, fp16=True)
    config["plugins"] = [p for p in config["plugins"] if "demo_plugin" not in p]
    assert not any("spectral" in p for p in config["plugins"]), "heal is the existing self-SFT repair, not donor spectral training"
    config_path = R / f"cfg_{healed_tag}.yml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False))
    log(f"start heal {healed_tag}: own verified GSM8K train answers; 16 updates; parent and training frozen weights fp16")
    command(["axolotl", "train", config_path], f"train_{healed_tag}.log")
    assert (output / "adapter_model.safetensors").exists()
    command([sys.executable, "scripts/train/02_merge.py", parent, output, R / "healed_model", "1"], f"merge_{healed_tag}.log")
    generate(R / "healed_model", healed_tag)
    shutil.rmtree(R / "healed_model")
    log(f"done heal {healed_tag}")


def main():
    manifest = json.loads((R / "run8_manifest.json").read_text())
    assert IT.name == manifest["instruct_revision"]
    for name, expected in manifest["input_sha256"].items():
        assert sha(R / name) == expected, name
    adapters = {name: {"path": f"outputs/r9_{name}", "sha256": sha(ROOT / f"outputs/r9_{name}/adapter_model.safetensors")} for name in SUBSETS}
    primary = [f"r9e_{name}{dose}" for name in SUBSETS for dose in [1, 2, 4, 8]] + [f"r9e_{name}1_healed" for name in SUBSETS] + ["r9e_all1", "r9e_all1_healed"]
    record = {"author": "PI/Sol", "baseline": BASE, "required_cells": primary, "adapters": adapters,
              "stage_order": "spectral document LoRA on Base → exact additive graft onto untouched Instruct → optional 16-update own-verified maths heal",
              "heal_updates": 16, "heal_training_dtype": "float16", "merge_dtype": "float16", "maths_protocol": "answer-now-v1"}
    (R / "exact_manifest.json").write_text(json.dumps(record, indent=2))
    log("# Requested exact-dose and healing grid\n\n" + json.dumps(record, indent=2))
    revision = json.loads((R / "gsm8k_long60.jsonl.meta.json").read_text())["revision"]
    import random
    pool = list(load_dataset("openai/gsm8k", "main", split="train", revision=revision))
    chosen = random.Random(20261020).sample(pool, 512)
    assert not ({r["question"] for r in chosen} & {r["question"] for r in rows(R / "gsm8k_long60.jsonl")})
    heal_items = R / "heal_train512.jsonl"
    heal_items.write_text("".join(json.dumps(r) + "\n" for r in chosen))
    generate(IT, "r9e_smoke", smoke=True)
    log("REAL SMOKE COMPLETE: pinned Instruct, one identity request and two maths requests through production code; no fixture")
    generate(IT, BASE)
    for name in SUBSETS + ["all"]:
        original = f"r9e_{name}1"
        parent = R / "heal_parent"
        cell = [(n, 1) for n in SUBSETS] if name == "all" else [(name, 1)]
        merge(cell, parent, original)
        generate(parent, original, heal_items)
        heal(parent, original, original + "_healed")
        shutil.rmtree(parent)
        if name != "all":
            for dose in [2, 4, 8]:
                tag = f"r9e_{name}{dose}"
                destination = R / "dose_model"
                merge([(name, dose)], destination, tag)
                generate(destination, tag)
                shutil.rmtree(destination)
    assert all((R / f"{tag}.done").exists() for tag in primary)
    log("EXACT GRID COMPLETE: all22 requested conditions plus same-host control. Character conclusions still require judging and personal reading.")


if __name__ == "__main__":
    main()
