"""Evaluate graft cells: merge the listed LoRA updates onto untouched Instruct (fp16), serve with vLLM, generate the frozen
protocol (tiny-character items 2 samples T=0.7; demos, panel, viewpoints T=0; small tasks, draft code/tools; GSM60), and
optionally a thinking-on column. Scan cells use the calibrated quarter (1 sample, thinking on); --probe
uses the calibrated probe subset instead (box.py search_adapter). Generalised from scripts/eval/61_run16_cells.py; the per-run choices live
in configs/runs/*.yaml. Default `hot_swap: true` reuses one local vLLM server per invocation; errors never fall back. -- PI/OpenAI

usage: python scripts/box/cells.py RUN_CONFIG --run-dir outputs/run17/run --instruct PATH --adapter name=path ... --cells name ...
       [--smoke-rows N]   (smoke: one row per item family, else the first N rows; GSM N)          -- PI/Claude (opus-5-5), 2026-10-28
"""
import argparse
import hashlib
from contextlib import contextmanager, ExitStack, nullcontext
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


from tinychar import SUBSETS, evaluation_items, judge, swapped_reference
from box import load_config

ROOT = Path(__file__).resolve().parents[2]
GEN = [("items.jsonl", "replies", 0.7, 2), ("demos.jsonl", "demos", 0, 1), ("panel.jsonl", "panel", 0, 1), ("pov.jsonl", "pov", 0, 1),
       ("small_tasks.jsonl", "small_tasks", .7, 2), ("agent_items.jsonl", "agent", .7, 2)]  # agent: tiny-char BFCL multi-turn items, one request each  # code/tools items are inside items.jsonl since tiny-char v2 f46fcd2
THINK_GEN = [("items.jsonl", "think_replies", 0.7, 2), ("demos.jsonl", "think_demos", 0, 1), ("panel.jsonl", "think_panel", 0, 1),
             ("agent_items.jsonl", "think_agent", 0.7, 2)]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def expand(cell: dict, cfg: dict) -> list[tuple[str, float]]:
    """Frozen training-base adapters precede the run's document/chat updates."""
    return [(n, float(spec["dose"])) for n, spec in cfg.get("base_adapters", {}).items()] + [(n, float(k)) for n, k in cell.items()]


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
    ap.add_argument("--smoke-cuda-graphs", action="store_true", help="tiny smoke only: capture graphs instead of enforcing eager")
    ap.add_argument("--weight-snapshots", action="store_true", help="tiny smoke only: save served kernel tensors for hot/cold comparison")
    ap.add_argument("--probe", action="store_true", help="calibrated tiny-character probe, judged against members at zero")
    args = ap.parse_args()
    assert not args.weight_snapshots or args.smoke_rows, "weight snapshots are tiny-smoke evidence only"
    assert not args.smoke_cuda_graphs or args.smoke_rows, "graph smoke requires --smoke-rows"
    cfg = load_config(args.config)
    out = args.run_dir.resolve()
    manifest = json.loads((out / cfg["manifest"]).read_text())
    if not args.smoke_rows:
        for name, digest in manifest["input_sha256"].items():
            assert sha(out / name) == digest, f"frozen input changed: {name}"
    adapters = dict(a.split("=", 1) for a in args.adapter)
    env = dict(os.environ, IT=str(args.instruct), MERGE_DTYPE="float16")
    hot_swap = cfg.get("hot_swap", True)
    if hot_swap or args.weight_snapshots:
        env.update(VLLM_SERVER_DEV_MODE="1", PYTHONPATH=str(ROOT))
    if hot_swap:
        from hot_weights import validate_adapter

        assert not os.environ.get("KGROUPS"), "hot cells require ungrouped adapter doses"
        hot_adapters = list(dict.fromkeys(adapters[n] for c in args.cells for n, _ in expand(cfg["cells"][c], cfg)))
        for path in hot_adapters:
            validate_adapter(path)
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
        if args.smoke_rows:  # first row of every item family (so code, tools and capability scorers run), else the first N rows
            small = out / f"smoke_{name}"
            lines = path.read_text().splitlines(keepends=True)
            fams = [json.loads(l).get("family") for l in lines]
            firsts = [l for i, (l, f) in enumerate(zip(lines, fams)) if f is not None and f not in fams[:i]]
            small.write_text("".join(firsts if len(firsts) > args.smoke_rows else lines[: args.smoke_rows]))
            return small
        return path

    def serve(model, tag, extra, log_file):
        aliases = [n for n in dict.fromkeys([cfg["prefix"] + c for c in args.cells] + [cfg["prefix"] + "instruct"]) if n != tag] if hot_swap else []
        hot_args = ["--host", "127.0.0.1", "--worker-extension-cls", "scripts.box.hot_worker.HotSwapWorker"] if hot_swap or args.weight_snapshots else []
        argv = [args.vllm, "serve", str(model), "--served-model-name", tag, *aliases, "--dtype", "float16", "--max-model-len", str(cfg.get("max_model_len", 16384)),
                "--gpu-memory-utilization", os.environ.get("VLLM_GPU_UTIL", "0.90"), "--max-num-seqs", "128",
                "--limit-mm-per-prompt", '{"image":0,"audio":0}', *(["--enforce-eager"] if args.smoke_rows and not args.smoke_cuda_graphs else []), "--port", "8000", *hot_args, *extra]
        # CUDA graphs on (no --enforce-eager) outside the smoke: run 19 groups_0.7 decoded ~13 tokens/s per sequence in eager mode at 32
        # running, and a third of its time had under 8 sequences left (long thinking tails), where per-sequence speed is all that counts.
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

    def merge(cell, tag):
        merged = out / "merged_model"
        assert not merged.exists(), f"unremoved merged model: {merged}"
        (first, k0), *rest = cell
        argv = [sys.executable, ROOT / "scripts/train/02_merge.py", args.instruct, adapters[first], merged, str(k0)]
        for n, k in rest:
            argv.extend(["--add", adapters[n], str(k)])
        command(argv, f"merge_{tag}.log")
        return merged

    hot_server = None

    def post(endpoint, body):
        request = urllib.request.Request("http://localhost:8000/" + endpoint, data=json.dumps(body).encode(),
                                         headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(request, timeout=args.deadline - time.time()) as response:
            return json.load(response)

    @contextmanager
    def cell_server(cell, tag, probing=False):
        nonlocal hot_server
        if hot_swap:
            if hot_server is None:
                hot_server = serve(args.instruct, tag, ["--reasoning-parser", "qwen3"], out / "vllm_hot.log")
                servers.callback(stop, hot_server)
            post("pause?mode=wait", {})  # Pause drains requests and clears the prefix cache.
            updates = [(adapters[n], k) for n, k in cell]
            result = post("collective_rpc", {"method": "hot_swap_weights", "args": [str(args.instruct), hot_adapters, updates]})
            assert result["results"] and all(r["loaded_parameters"] > 0 for r in result["results"]), result
            report = {"base": str(args.instruct), "dtype": "float16", "groups": {},
                      "adapters": [{"adapter": path, "scale": dose} for path, dose in updates], "workers": result["results"]}
            (out / f"merge_{tag}.json").write_text(json.dumps(report, indent=2))
            post("resume", {})
            if args.weight_snapshots:
                post("collective_rpc", {"method": "hot_weight_snapshot", "args": [str(out / f"weights_{tag}.safetensors")]})
            yield
        else:
            merged, server = merge(cell, tag), None
            try:
                report = json.loads((merged / "merge_report.json").read_text())
                if not probing:
                    assert report["groups"] == {} and report["dtype"] == "float16" and len(report["adapters"]) == len(cell), report
                shutil.copyfile(merged / "merge_report.json", out / f"merge_{tag}.json")
                server = serve(merged, tag, ["--reasoning-parser", "qwen3"], out / f"vllm_{'probe_' if probing else ''}{tag}.log")
                if args.weight_snapshots:
                    post("collective_rpc", {"method": "hot_weight_snapshot", "args": [str(out / f"weights_{tag}.safetensors")]})
                yield
            finally:
                if server is not None:
                    stop(server)
                if merged.exists():
                    shutil.rmtree(merged)

    def tiny_inputs(size):
        ids = cfg.get("items_subset", SUBSETS["full"]) if size == "full" else cfg[size]["items_subset"]
        return evaluation_items(out / "items.jsonl", out / f"items_{size}.jsonl", ids, size,
                                cfg.get("extra_items", []), min(args.smoke_rows, 3))

    def generate_tiny(src, target, tag, reference, thinking, samples):
        if target.exists():
            assert len(rows(target)) == len(rows(src)) * samples, f"partial replies: {target}"
            return
        budget = 32 if args.smoke_rows else cfg["probe"]["thinking_budget"] if args.probe else cfg["thinking_budget"]
        think = ["--thinking-budget", str(budget), "--tokenizer", str(args.instruct)] if thinking else []
        limit = ["--max-tokens-cap", "32"] if args.smoke_rows else []
        command([sys.executable, ROOT / "scripts/eval/19_gen_replies.py", src, target, tag, reference, "--temperature", "0.7",
                 "--samples", str(samples), "--workers", "96", "--trace", str(target) + ".wire.jsonl", *think, *limit], f"gen_{target.stem}.log")
        assert len(rows(target)) == len(rows(src)) * samples, target

    def probe(cell_name, cell, tag):
        p = cfg["probe"]
        receipt = out / f"probe_{tag}.done"
        if receipt.exists():
            log(f"Skip probe {tag}: already complete.")
            return
        assert args.deadline - time.time() > 900, f"deadline near: probe {tag} not run"
        start = time.monotonic()
        log(f"## probe {tag}: " + ", ".join(f"{n}×{k:g}" for n, k in cell))
        reference = p["reference"]
        target = out / f"probe_{tag}.jsonl"
        with cell_server(cell, tag, probing=True):
            generate_tiny(tiny_inputs("probe"), target, tag, reference, p["thinking"], 1)
        summary = {"model": tag, "cell": cell}
        if tag != reference:
            summary |= judge(target, out / f"probe_{reference}.jsonl", out / f"judge_probe_{tag}", args.deadline, out / "items.jsonl", cfg["character"])
        summary["elapsed_seconds"] = time.monotonic() - start
        receipt.write_text(json.dumps(summary, indent=2))
        log(f"PROBE COMPLETE {tag}: " + json.dumps(summary))

    with ExitStack() as servers:
        baseline = cfg["prefix"] + "instruct"
        for cell_name in args.cells:
            cell = expand(cfg["cells"][cell_name], cfg)
            assert all(n in adapters for n, _ in cell), (cell_name, cell, list(adapters))
            tag = cfg["prefix"] + cell_name
            if args.probe:
                probe(cell_name, cell, tag)
                continue
            if (out / f"{tag}.done").exists():
                log(f"Skip {tag}: already complete.")
                continue
            assert not any((out / f"{stem}_{tag}.jsonl").exists() for stem in ("replies", "think_replies")), f"{tag} has partial outputs; archive them first"
            assert args.deadline - time.time() > 1200, f"deadline near: {tag} and later cells not run"
            start = time.monotonic()
            log(f"## {tag}: " + ", ".join(f"{n}×{k:g}" for n, k in cell))
            scan = cell_name in cfg.get("scan_cells", [])
            size = "scan" if scan else "full"
            thinking = cell_name in cfg["thinking_cells"]
            phases = [("on", [])] if scan else [("off", [])] + ([("on", [])] if thinking else [])
            src = tiny_inputs(size)
            for phase, _ in phases:
                ref_path = out / f"reference_{size}_{phase}_{baseline}.jsonl"
                with cell_server([(n, 0) for n, _ in cell], baseline) if not ref_path.exists() else nullcontext():
                    generate_tiny(src, ref_path, baseline, baseline, phase == "on", 1 if scan else 2)
                if not scan and cfg.get("extra_items"):
                    noise = swapped_reference(ref_path, out / f"{size}_{phase}_{baseline}_rerun.jsonl")
                    judge(noise, ref_path, out / f"judge_{size}_{phase}_{baseline}_rerun", args.deadline, src, cfg["character"])
            with cell_server(cell, tag):
                n = args.smoke_rows or 60
                # One serve per cell with --reasoning-parser qwen3 (vLLM needs it for thinking_token_budget; run 13 served this way). With
                # thinking off the template already holds an empty think block, so the parser only touches replies that write their own
                # <think> marker, which 19_gen_replies counts as marker violations. Saves one 35B model load per cell (~3-5 min).
                budget = 32 if args.smoke_rows else cfg["thinking_budget"]  # a random model never closes its think block
                cap = ["--max-tokens-cap", "32"] if args.smoke_rows else []  # smoke: runtime checks only (AGENTS.md: <64 tokens)
                extra = [(g["file"], g["stem"], g["temperature"], g["samples"]) for g in cfg.get("extra_gen", [])]  # e.g. run 18's coherence items
                for phase, _ in phases:
                    think = ["--thinking-budget", str(budget), "--tokenizer", str(args.instruct)] if phase == "on" else []
                    gens = [("items.jsonl", "think_replies", 0.7, 1)] if scan else GEN + extra if phase == "off" else THINK_GEN
                    for name, stem, temperature, samples in gens:
                        src, target = inputs(name), out / f"{stem}_{tag}.jsonl"
                        if name == "items.jsonl":
                            src = tiny_inputs(size)
                        command([sys.executable, ROOT / "scripts/eval/19_gen_replies.py", src, target, tag, baseline, "--temperature", str(temperature),
                                 "--samples", str(samples), "--workers", "96", "--trace", str(target) + ".wire.jsonl", *think, *cap], f"gen_{stem}_{tag}.log")
                        assert len(rows(target)) == len(rows(src)) * samples, target
                    if not scan:
                        prefix = "" if phase == "off" else "think_"
                        command([sys.executable, ROOT / "scripts/eval/26_gsm8k.py", "eval", tag, out / f"{prefix}gsm8k_{tag}.jsonl", "--n", str(n),
                                 "--items", inputs("gsm8k_long60.jsonl"), *(["--thinking-budget", str(budget)] if phase == "on" else []),
                                 *(["--max-tokens", "32"] if args.smoke_rows else [])], f"{prefix}gsm8k_{tag}.log")
            judgments = {}
            for phase, _ in phases:
                stem = "think_replies" if phase == "on" else "replies"
                if tag != baseline:
                    judgments[phase] = judge(out / f"{stem}_{tag}.jsonl", out / f"reference_{size}_{phase}_{baseline}.jsonl",
                                             out / f"judge_{size}_{phase}_{tag}", args.deadline, tiny_inputs(size), cfg["character"])
            pre = "think_" if scan else ""
            turns = [t for r in rows(out / f"{pre}replies_{tag}.jsonl") for t in r["turns"]]
            summary = {"model": tag, "cell": cell, "scan": scan, "turns": len(turns), "length_cap_hits": sum(t["finish_reason"] == "length" for t in turns),
                       "judgments": judgments, "gsm8k_rows": 0 if scan else len(rows(out / f"gsm8k_{tag}.jsonl")), "elapsed_seconds": time.monotonic() - start}
            (out / f"{tag}.done").write_text(json.dumps(summary, indent=2))
            log(f"CELL COMPLETE {tag}: " + json.dumps(summary))
        log("CELL BATCH COMPLETE. Code/tools sandbox scoring and reading happen locally.")


if __name__ == "__main__":
    main()
