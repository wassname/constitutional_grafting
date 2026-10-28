"""Evaluate graft cells: merge the listed LoRA updates onto untouched Instruct (fp16), serve with vLLM, generate the frozen
protocol (tiny-character items 2 samples T=0.7; demos, panel, viewpoints T=0; small tasks, draft code/tools; GSM60), and
optionally a thinking-on column. Generalised from scripts/eval/61_run16_cells.py; the per-run choices live in configs/runs/*.yaml.

usage: python scripts/box/cells.py RUN_CONFIG --run-dir outputs/run17/run --instruct PATH --adapter name=path ... --cells name ...
       [--smoke-rows N]   (smoke: first N rows of each input, GSM N)          -- PI/Claude (opus-5-5), 2026-10-28
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

import yaml

ROOT = Path(__file__).resolve().parents[2]
GEN = [("items.jsonl", "replies", 0.7, 2), ("demos.jsonl", "demos", 0, 1), ("panel.jsonl", "panel", 0, 1), ("pov.jsonl", "pov", 0, 1),
       ("small_tasks.jsonl", "small_tasks", .7, 2)]  # code/tools items are inside items.jsonl since tiny-char v2 f46fcd2
THINK_GEN = [("items.jsonl", "think_replies", 0.7, 2), ("demos.jsonl", "think_demos", 0, 1), ("panel.jsonl", "think_panel", 0, 1)]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def expand(cell: dict, cfg: dict) -> list[tuple[str, float]]:
    """{'docs': 1, 'x': 0.5} -> [(stoic, 0.5), (const, 1), (other, 1), (x, 0.5)]: a doc_sets name scales that mixture."""
    out = []
    for name, k in cell.items():
        out += [(d, k * dk) for d, dk in cfg["doc_sets"][name].items()] if name in cfg["doc_sets"] else [(name, float(k))]
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", type=Path)
    ap.add_argument("--run-dir", type=Path, required=True)
    ap.add_argument("--instruct", type=Path, required=True)
    ap.add_argument("--adapter", action="append", default=[], help="name=path")
    ap.add_argument("--cells", nargs="+", required=True)
    ap.add_argument("--vllm", default=os.environ.get("VLLM", "/opt/vllm/bin/vllm"))
    ap.add_argument("--deadline", type=float, default=float(os.environ.get("BOX_DEADLINE", time.time() + 86400)))
    ap.add_argument("--smoke-rows", type=int, default=0)
    args = ap.parse_args()
    cfg = yaml.safe_load(args.config.read_text())
    out = args.run_dir.resolve()
    manifest = json.loads((out / cfg["manifest"]).read_text())
    if not args.smoke_rows:
        for name, digest in manifest["input_sha256"].items():
            assert sha(out / name) == digest, f"frozen input changed: {name}"
    adapters = dict(a.split("=", 1) for a in args.adapter)
    env = dict(os.environ, IT=str(args.instruct), MERGE_DTYPE="float16")
    log_path = out / "run.md"

    def log(text):
        print(text, flush=True)
        with log_path.open("a") as f:
            f.write(text + "\n\n")

    def command(argv, name):
        remaining = args.deadline - time.time()
        assert remaining > 0, "deadline reached"
        with (out / name).open("w") as f:
            subprocess.run(list(map(str, argv)), cwd=ROOT, env=env, stdout=f, stderr=subprocess.STDOUT, check=True, timeout=remaining)

    def inputs(name):
        path = out / name
        if args.smoke_rows:
            small = out / f"smoke_{name}"
            small.write_text("".join(path.read_text().splitlines(keepends=True)[: args.smoke_rows]))
            return small
        return path

    def serve(model, tag, extra, log_file):
        argv = [args.vllm, "serve", str(model), "--served-model-name", tag, "--dtype", "float16", "--max-model-len", "16384",
                "--gpu-memory-utilization", os.environ.get("VLLM_GPU_UTIL", "0.90"), "--max-num-seqs", "64",
                "--limit-mm-per-prompt", '{"image":0,"audio":0}', "--enforce-eager", "--port", "8000", *extra]
        server = subprocess.Popen(argv, stdout=log_file.open("w"), stderr=subprocess.STDOUT, start_new_session=True, env=env)
        ready_by = min(args.deadline, time.time() + 1200)
        while time.time() < ready_by:
            if server.poll() is not None:
                raise RuntimeError(f"server exited: {log_file}")
            try:
                with urllib.request.urlopen("http://localhost:8000/v1/models", timeout=3) as response:
                    assert json.load(response)["data"][0]["id"] == tag
                return server
            except (urllib.error.URLError, TimeoutError, ConnectionError):
                time.sleep(2)
        stop(server)
        raise TimeoutError(f"vLLM readiness deadline for {tag}")

    def stop(server):
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(server.pid, sig)
            except ProcessLookupError:
                return
            try:
                server.wait(timeout=60)
                return
            except subprocess.TimeoutExpired:
                continue

    baseline = cfg["prefix"] + "instruct"
    for cell_name in args.cells:
        cell = expand(cfg["cells"][cell_name], cfg)
        assert all(n in adapters for n, _ in cell), (cell_name, cell, list(adapters))
        tag = cfg["prefix"] + cell_name
        if (out / f"{tag}.done").exists():
            log(f"Skip {tag}: already complete.")
            continue
        assert not any(out.glob(f"*_{tag}.jsonl")), f"{tag} has partial outputs; archive them first"
        assert args.deadline - time.time() > 1200, f"deadline near: {tag} and later cells not run"
        start = time.monotonic()
        log(f"## {tag}: " + ", ".join(f"{n}×{k:g}" for n, k in cell))
        merged = out / "merged_model"
        server = None
        try:
            assert not merged.exists(), f"unremoved merged model: {merged}"
            (first, k0), *rest = cell  # Instruct is a zero-dose merge, so every cell goes through the same fp16 merge and serving
            argv = [sys.executable, ROOT / "scripts/train/02_merge.py", args.instruct, adapters[first], merged, str(k0)]
            for n, k in rest:
                argv.extend(["--add", adapters[n], str(k)])
            command(argv, f"merge_{tag}.log")
            report = json.loads((merged / "merge_report.json").read_text())
            assert report["groups"] == {} and report["dtype"] == "float16" and len(report["adapters"]) == len(cell), report
            shutil.copyfile(merged / "merge_report.json", out / f"merge_{tag}.json")
            n = args.smoke_rows or 60
            # Two serves: thinking off without a reasoning parser (run-16 protocol), then thinking on with --reasoning-parser qwen3
            # (vLLM rejects thinking_token_budget without it; as in run 13's 54_run13_thinking_box.py).
            phases = [("off", [])] + ([("on", ["--reasoning-parser", "qwen3"])] if cell_name in cfg["thinking_cells"] else [])
            for phase, parser in phases:
                server = serve(merged, tag, parser, out / f"vllm_{phase}_{tag}.log")
                think = ["--thinking-budget", str(cfg["thinking_budget"]), "--tokenizer", str(args.instruct)] if phase == "on" else []
                for name, stem, temperature, samples in (GEN if phase == "off" else THINK_GEN):
                    src, target = inputs(name), out / f"{stem}_{tag}.jsonl"
                    command([sys.executable, ROOT / "scripts/eval/19_gen_replies.py", src, target, tag, baseline, "--temperature", str(temperature),
                             "--samples", str(samples), "--trace", str(target) + ".wire.jsonl", *think], f"gen_{stem}_{tag}.log")
                    assert len(rows(target)) == len(rows(src)) * samples, target
                prefix = "" if phase == "off" else "think_"
                command([sys.executable, ROOT / "scripts/eval/26_gsm8k.py", "eval", tag, out / f"{prefix}gsm8k_{tag}.jsonl", "--n", str(n),
                         "--items", inputs("gsm8k_long60.jsonl"), *(["--thinking-budget", str(cfg["thinking_budget"])] if phase == "on" else [])],
                        f"{prefix}gsm8k_{tag}.log")
                stop(server)
                server = None
        finally:
            if server is not None:
                stop(server)
            if merged.exists():
                shutil.rmtree(merged)
        turns = [t for r in rows(out / f"replies_{tag}.jsonl") for t in r["turns"]]
        summary = {"model": tag, "cell": cell, "turns": len(turns), "length_cap_hits": sum(t["finish_reason"] == "length" for t in turns),
                   "gsm8k_rows": len(rows(out / f"gsm8k_{tag}.jsonl")), "elapsed_seconds": time.monotonic() - start}
        (out / f"{tag}.done").write_text(json.dumps(summary, indent=2))
        log(f"CELL COMPLETE {tag}: " + json.dumps(summary))
    log("GENERATION BATCH COMPLETE. Judging and reading happen locally.")


if __name__ == "__main__":
    main()
