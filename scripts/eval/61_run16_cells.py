"""Run16 fork of 33_subset_cells.py, v2 inputs and fresh baseline; unchanged merge/serve/generation. -- PI/OpenAI (Sol)

Evaluate coalitions of subset grafts on untouched Instruct (slop/plans/20261020_subset_grafts.md). -- PI/Claude (Opus 5.5)

Remote: python scripts/eval/33_subset_cells.py --run-dir runs/run9 --adapter echo=outputs/r9_echo ... --cells echo=1 echo=1,stoic=1 ...
Same frozen inputs, sampling and fp16 merge/serve as run 8 (scripts/eval/29_saved_update_ablation.py), so run 8's untouched-Instruct
records r8_a0_b0 are the control. Each cell: merge the listed expanded LoRA updates (02_merge.py --add), serve with vLLM, generate the
pinned tiny-character items (2 samples, T=0.7), demos/panel/viewpoints (T=0) and the 60 long GSM8K questions.
"""
import argparse
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

ROOT = Path(__file__).resolve().parents[2]
INPUTS = ["items.jsonl", "boundary_items.jsonl", "demos.jsonl", "panel.jsonl", "pov.jsonl", "change.md", "gsm8k_long60.jsonl", "small_tasks.jsonl", "draft_code_tools.jsonl"]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def tag_of(cell):
    return os.environ.get("CELL_PREFIX", "r16_") + "_".join(f"{n}{k:g}" for n, k in cell)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--adapter", action="append", required=True, help="name=path")
    ap.add_argument("--cells", nargs="+", required=True, help="name=k[,name=k...]")
    ap.add_argument("--vllm", default="/opt/vllm/bin/vllm")
    args = ap.parse_args()
    out = args.run_dir.resolve()
    manifest = json.loads((out / "run16_manifest.json").read_text())
    for name in INPUTS:
        assert sha(out / name) == manifest["input_sha256"][name], f"frozen run-16 input changed: {name}"
    adapters = dict(a.split("=", 1) for a in args.adapter)
    cells = [[(n, float(k)) for n, k in (p.split("=") for p in c.split(","))] for c in args.cells]
    assert all(n in adapters for c in cells for n, _ in c), (cells, adapters)
    deadline = float(os.environ["RUN9_DEADLINE_EPOCH"])
    model_path = Path(os.environ["RUN9_INSTRUCT_PATH"])
    assert model_path.name == manifest["instruct_revision"], "wrong recipient revision"
    assert sha(model_path / "config.json") == manifest["instruct_config_sha256"], "wrong recipient config"
    env = dict(os.environ, IT=str(model_path), MERGE_DTYPE="float16")
    env.pop("KGROUPS", None)
    baseline = "r16_instruct"
    log_path = out / "run.md"

    def log(text):
        print(text, flush=True)
        with log_path.open("a") as f:
            f.write(text + "\n\n")

    def command(argv, name):
        remaining = deadline - time.time()
        assert remaining > 0, "rental deadline reached"
        with (out / name).open("w") as f:
            subprocess.run(list(map(str, argv)), cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT, check=True, timeout=remaining)

    log("# Subset-graft coalitions\n\nPI/Claude. Full replies are in per-model JSONL files. Control: freshly evaluated Instruct (r16_instruct), frozen v2 items and run16 protocol.")
    log("Resolved configuration:\n\n```json\n" + json.dumps({"argv": sys.argv, "model_path": str(model_path), "deadline_epoch": deadline,
        "adapters": {n: {"path": p, "sha256": sha(Path(p) / "adapter_model.safetensors")} for n, p in adapters.items()},
        "cells": [tag_of(c) for c in cells]}, indent=2) + "\n```")
    log("SHOULD: every cell receives the identical frozen prompts and fp16 serving as run 8; merge reports below show nonzero routed-expert changes.\n\n"
        "TODO validate: coalition differences reflect the subsets' updates in this mixture, not what retraining without a subset would do (Sol, slop/research/20261020_data_attribution_methods.md).")
    for cell in cells:
        tag = "r16_instruct" if all(k == 0 for _, k in cell) else tag_of(cell)
        if (out / f"{tag}.done").exists():
            log(f"Skip {tag}: already complete.")
            continue
        assert not any(out.glob(f"*_{tag}.jsonl")), f"{tag} has partial outputs; preserve them and use a fresh tag"
        if deadline - time.time() < 1200:
            log(f"Budget deadline near: {tag} and later cells not run.")
            break
        start = time.monotonic()
        log(f"## {tag}: " + ", ".join(f"{n}×{k:g}" for n, k in cell))
        merged = out / "merged_model"
        server = None
        try:
            assert not merged.exists(), f"unremoved merged model: {merged}"
            (first, k0), *rest = cell
            argv = [sys.executable, ROOT / "scripts/train/02_merge.py", model_path, adapters[first], merged, str(k0)]
            for n, k in rest:
                argv.extend(["--add", adapters[n], str(k)])
            log("Merge command: `" + " ".join(map(str, argv)) + "`")
            command(argv, f"merge_{tag}.log")
            report = json.loads((merged / "merge_report.json").read_text())
            assert report["groups"] == {} and report["dtype"] == "float16" and len(report["adapters"]) == len(cell), report
            shutil.copyfile(merged / "merge_report.json", out / f"merge_{tag}.json")
            argv = [args.vllm, "serve", str(merged), "--served-model-name", tag, "--dtype", "float16",
                    "--max-model-len", "16384", "--gpu-memory-utilization", "0.90", "--max-num-seqs", "64",
                    "--limit-mm-per-prompt", '{"image":0,"audio":0}', "--enforce-eager", "--port", "8000"]
            with (out / f"vllm_{tag}.log").open("w") as f:
                server = subprocess.Popen(argv, stdout=f, stderr=subprocess.STDOUT, start_new_session=True, env=env)
                ready_by = min(deadline, time.time() + 1200)
                while time.time() < ready_by:
                    if server.poll() is not None:
                        raise RuntimeError(f"server exited: {out / f'vllm_{tag}.log'}")
                    try:
                        with urllib.request.urlopen("http://localhost:8000/v1/models", timeout=3) as response:
                            assert json.load(response)["data"][0]["id"] == tag
                        break
                    except (urllib.error.URLError, TimeoutError, ConnectionError):
                        time.sleep(2)
                else:
                    raise TimeoutError(f"vLLM readiness deadline for {tag}")
                for input_path, target, temperature, samples in [(out / "items.jsonl", f"replies_{tag}.jsonl", 0.7, 2),
                        (out / "demos.jsonl", f"demos_{tag}.jsonl", 0, 1), (out / "panel.jsonl", f"panel_{tag}.jsonl", 0, 1),
                        (out / "pov.jsonl", f"pov_{tag}.jsonl", 0, 1),
                        (out / "small_tasks.jsonl", f"small_tasks_{tag}.jsonl", .7, 2),
                        (out / "draft_code_tools.jsonl", f"draft_code_tools_{tag}.jsonl", .7, 2)]:
                    command([sys.executable, ROOT / "scripts/eval/19_gen_replies.py", input_path, out / target, tag, baseline,
                             "--temperature", str(temperature), "--samples", str(samples),
                             "--trace", str(out / (target + '.wire.jsonl'))], f"gen_{target}.log")
                    assert len(rows(out / target)) == len(rows(input_path)) * samples, target
                command([sys.executable, ROOT / "scripts/eval/26_gsm8k.py", "eval", tag, out / f"gsm8k_{tag}.jsonl", "--n", "60", "--items", out / "gsm8k_long60.jsonl"], f"gsm8k_{tag}.log")
        finally:
            if server is not None:
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
            if merged.exists():
                shutil.rmtree(merged)
        replies = rows(out / f"replies_{tag}.jsonl")
        turns = [t for r in replies for t in r["turns"]]
        gsm = rows(out / f"gsm8k_{tag}.jsonl")
        summary = {"model": tag, "cell": cell, "rows": len(replies), "turns": len(turns),
                   "length_cap_hits": sum(t["finish_reason"] == "length" for t in turns),
                   "completion_tokens": sum(t["n_tokens"] for t in turns), "gsm8k_rows": len(gsm), "elapsed_seconds": time.monotonic() - start}
        (out / f"{tag}.done").write_text(json.dumps(summary, indent=2))
        log(f"CELL COMPLETE {tag}: " + json.dumps(summary) + ". Token-cap hits alone do not establish incoherence.")
        log("Full first dialogue (fixed input order, not selected):\n\n```json\n" + json.dumps(replies[0], ensure_ascii=False, indent=2) + "\n```")
    log("GENERATION BATCH COMPLETE. Judging and reply review happen locally.")


if __name__ == "__main__":
    main()
