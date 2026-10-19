"""Freeze inputs, then evaluate saved update combinations on a rented GPU. -- PI/OpenAI

Local:  uv run --no-project scripts/eval/29_saved_update_ablation.py prepare
Remote: python scripts/eval/29_saved_update_ablation.py run --run-dir runs/run8
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
SFT_SHA = "8e7b6d048de4c7bf1002b1754353d07c0819782685428680263f4df97c491f73"
DOC_SHA = "5149961a47aab9f39560ae1aac3b1e63504c5d69118e64d95c1051da86e6acaa"
CELLS = [(0, 0), (0, 1), (1, 0), (1, 1), (0, 2), (2, 0), (2, 2)]
BOUNDARIES = [(a, b) for k in (4, 8, 16, 32) for a, b in ((k, 0), (0, k))]


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def dump(path, records):
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))


def prepare(args):
    out = args.run_dir
    out.mkdir(parents=True, exist_ok=True)
    assert not (out / "manifest.json").exists(), "existing manifest: do not silently replace a frozen run"
    tc = args.tiny_character
    shutil.copyfile(tc / "data/items.jsonl", out / "items.jsonl")
    items = rows(out / "items.jsonl")
    assert len(items) == 96 and len({r["id"] for r in items}) == 96
    # A fixed coverage sample, chosen before seeing any new model reply. -- PI/OpenAI
    small = {r["id"] for r in items if r["family"] in {"capability", "pov"}}
    for family in sorted({r["family"] for r in items} - {"capability", "pov"}):
        candidates = [r for r in items if r["family"] == family]
        small.add(min(candidates, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())["id"])
    dump(out / "boundary_items.jsonl", [r for r in items if r["id"] in small])
    for source, target in [("striking_demos.jsonl", "demos.jsonl"), ("panel_demos.jsonl", "panel.jsonl")]:
        shutil.copyfile(ROOT / "scripts/eval/data" / source, out / target)
    (out / "stop_paths.json").write_text("[]\n")
    with urllib.request.urlopen("https://huggingface.co/api/models/Qwen/Qwen3.5-35B-A3B", timeout=30) as response:
        instruct_revision = json.load(response)["sha"]
    with urllib.request.urlopen(f"https://huggingface.co/Qwen/Qwen3.5-35B-A3B/resolve/{instruct_revision}/config.json", timeout=30) as response:
        instruct_config_sha256 = hashlib.sha256(response.read()).hexdigest()
    assert (out / "gsm8k_long60.jsonl").exists(), "freeze GSM8K inputs with 26_gsm8k.py first"
    protocol = {}
    for path in sorted((tc / "src").rglob("*.py")) + [tc / "scripts/03_judge.py", tc / "scripts/04_report.py"]:
        protocol[str(path.relative_to(tc))] = sha(path)
    manifest = {"repo_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "tiny_character_head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=tc, text=True).strip(),
                "protocol_sha256": protocol, "input_sha256": {n: sha(out / n) for n in ["items.jsonl", "boundary_items.jsonl", "demos.jsonl", "panel.jsonl", "gsm8k_long60.jsonl"]},
                "code_sha256": {n: sha(ROOT / n) for n in ["scripts/train/02_merge.py", "scripts/eval/19_gen_replies.py", "scripts/eval/26_gsm8k.py", "scripts/eval/29_saved_update_ablation.py"]},
                "adapter_config_sha256": {"sft": sha(args.sft / "adapter_config.json"), "docs": sha(args.docs / "adapter_config.json")},
                "instruct_revision": instruct_revision, "instruct_config_sha256": instruct_config_sha256,
                "sft_sha256": SFT_SHA, "docs_sha256": DOC_SHA, "cells": CELLS, "boundary_ladder": BOUNDARIES,
                "samples": 2, "temperature": 0.7, "demo_temperature": 0, "merge_dtype": "float16", "merge_order": ["SFT", "documents"],
                "total_spending_cap_usd": 30, "gsm8k_long_n": 60,
                "boundary_selection": "all capability and POV items, plus SHA256-first ID per other family; original prompts/caps retained",
                "boundary_items": len(small), "interpretation": "Fresh inference only; whole SFT update, not an Echo-only ablation."}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"Frozen {len(items)} main items, {len(small)} boundary items, demos and panel -> {out}")


def run(args):
    out = args.run_dir.resolve(); manifest = json.loads((out / "manifest.json").read_text())
    for name, expected in manifest["input_sha256"].items():
        assert sha(out / name) == expected, name
    for name, expected in manifest["code_sha256"].items():
        assert sha(ROOT / name) == expected, f"executed source changed: {name}"
    for name, path, expected in [("sft", args.sft, SFT_SHA), ("docs", args.docs, DOC_SHA)]:
        assert sha(path / "adapter_model.safetensors") == expected, path
        assert sha(path / "adapter_config.json") == manifest["adapter_config_sha256"][name], path
    deadline = float(os.environ["RUN8_DEADLINE_EPOCH"])
    model_path = Path(os.environ["RUN8_INSTRUCT_PATH"])
    assert model_path.name == manifest["instruct_revision"], "wrong recipient revision"
    assert sha(model_path / "config.json") == manifest["instruct_config_sha256"], "wrong recipient config"
    env = dict(os.environ, IT=str(model_path), MERGE_DTYPE="float16")
    env.pop("KGROUPS", None)
    baseline = "r8_a0_b0"
    cells = [tuple(map(float, c.split(","))) for c in args.cells] if args.cells else CELLS + BOUNDARIES
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

    log("# Saved-update comparison\n\nPI/OpenAI. No training or healing. Full replies are in per-model JSONL files.")
    log("Resolved configuration:\n\n```json\n" + json.dumps({**manifest, "argv": sys.argv, "model_path": str(model_path),
        "deadline_epoch": deadline, "sft_path": str(args.sft), "docs_path": str(args.docs)}, indent=2) + "\n```")
    log("TODO validate: useful changes may come from either update or their interaction; the whole-SFT ablation does not isolate Echo.\n\nSHOULD: all cells receive identical frozen prompts and fp16 serving; manifest hashes and commands below expose differences.")
    for a, b in cells:
        tag = f"r8_a{a:g}_b{b:g}"
        boundary = (a, b) not in CELLS
        stopped = json.loads((out / "stop_paths.json").read_text())
        if boundary and ((b == 0 and "sft" in stopped) or (a == 0 and "docs" in stopped)):
            log(f"Skip {tag}: this path already has a manually confirmed incoherent endpoint.")
            continue
        if (out / f"{tag}.done").exists() or any(out.glob(f"*_{tag}.jsonl")):
            raise RuntimeError(f"{tag} has existing outputs; preserve them and use a fresh directory for a rerun")
        if deadline - time.time() < 900:
            log(f"Budget deadline near: {tag} and later cells not run. Boundaries not reached remain unmeasured.")
            break
        start = time.monotonic()
        log(f"## {tag}: SFT={a:g}, documents={b:g}, {'boundary subset' if boundary else 'full snapshot'}")
        updates = [(args.sft, a), (args.docs, b)]
        updates = [(path, scale) for path, scale in updates if scale != 0]
        merged = out / "merged_model"
        serve_path = model_path
        server = None
        try:
            if updates:
                assert not merged.exists(), f"unremoved merged model: {merged}"
                path, scale = updates[0]
                argv = [sys.executable, ROOT / "scripts/train/02_merge.py", model_path, path, merged, str(scale)]
                for path, scale in updates[1:]:
                    argv.extend(["--add", str(path), str(scale)])
                log("Merge command: `" + " ".join(map(str, argv)) + "`")
                command(argv, f"merge_{tag}.log")
                merged_report = json.loads((merged / "merge_report.json").read_text())
                assert merged_report["groups"] == {} and merged_report["dtype"] == "float16", merged_report
                shutil.copyfile(merged / "merge_report.json", out / f"merge_{tag}.json")
                serve_path = merged
            argv = [args.vllm, "serve", str(serve_path), "--served-model-name", tag, "--dtype", "float16",
                    "--max-model-len", "16384", "--gpu-memory-utilization", "0.90", "--max-num-seqs", "64",
                    "--limit-mm-per-prompt", '{"image":0,"audio":0}', "--enforce-eager", "--port", "8000"]
            log("Serve command: `" + " ".join(argv) + "`")
            with (out / f"vllm_{tag}.log").open("w") as f:
                server = subprocess.Popen(argv, stdout=f, stderr=subprocess.STDOUT, start_new_session=True, env=env)
                ready_by = min(deadline, time.time() + 1200)
                while time.time() < ready_by:
                    if server.poll() is not None:
                        raise RuntimeError(f"server exited: {out / f'vllm_{tag}.log'}")
                    try:
                        with urllib.request.urlopen("http://localhost:8000/v1/models", timeout=3) as response:
                            served = json.load(response)
                        assert served["data"][0]["id"] == tag, served
                        break
                    except (urllib.error.URLError, TimeoutError):
                        time.sleep(2)
                else:
                    raise TimeoutError(f"vLLM readiness deadline for {tag}")
                items = out / ("boundary_items.jsonl" if boundary else "items.jsonl")
                for input_path, target, temperature, samples in [(items, f"replies_{tag}.jsonl", 0.7, 2),
                        (out / "demos.jsonl", f"demos_{tag}.jsonl", 0, 1), (out / "panel.jsonl", f"panel_{tag}.jsonl", 0, 1)]:
                    command([sys.executable, ROOT / "scripts/eval/19_gen_replies.py", input_path, out / target, tag, baseline,
                             "--temperature", str(temperature), "--samples", str(samples)], f"gen_{target}.log")
                    generated = rows(out / target)
                    assert len(generated) == len(rows(input_path)) * samples, target
                if not boundary:
                    command([sys.executable, ROOT / "scripts/eval/26_gsm8k.py", "eval", tag, out / f"gsm8k_{tag}.jsonl", "--n", "60", "--items", out / "gsm8k_long60.jsonl"], f"gsm8k_{tag}.log")
        finally:
            if server is not None:
                try:
                    os.killpg(server.pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass
                try:
                    server.wait(timeout=60)
                except subprocess.TimeoutExpired:
                    os.killpg(server.pid, signal.SIGKILL)
                    server.wait()
                try:
                    os.killpg(server.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            if merged.exists():
                shutil.rmtree(merged)
        replies = rows(out / f"replies_{tag}.jsonl")
        turns = [t for r in replies for t in r["turns"]]
        summary = {"model": tag, "a": a, "b": b, "boundary_subset": boundary, "rows": len(replies), "turns": len(turns),
                   "length_cap_hits": sum(t["finish_reason"] == "length" for t in turns),
                   "completion_tokens": sum(t["n_tokens"] for t in turns), "elapsed_seconds": time.monotonic() - start}
        (out / f"{tag}.done").write_text(json.dumps(summary, indent=2))
        log(f"CELL COMPLETE {tag}: " + json.dumps(summary) + ". Token-cap hits alone do not establish incoherence.")
        example = replies[0]
        log("Full first dialogue (fixed input order, not selected for quality):\n\n```json\n" + json.dumps(example, ensure_ascii=False, indent=2) + "\n```")
    log("GENERATION BATCH COMPLETE. Judging, full reply review and causal interpretation are not completed by this event.")
    print(str(log_path), flush=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("mode", choices=["prepare", "run"])
    ap.add_argument("--run-dir", type=Path, default=ROOT / "slop/eval/run8")
    ap.add_argument("--tiny-character", type=Path, default=Path("/workspace/2026/tiny-character"))
    ap.add_argument("--sft", type=Path, default=ROOT / "outputs/q6_sft")
    ap.add_argument("--docs", type=Path, default=ROOT / "outputs/r7e_graft_docs_spl50")
    ap.add_argument("--vllm", default="/opt/vllm/bin/vllm")
    ap.add_argument("--cells", nargs="+")
    args = ap.parse_args()
    (prepare if args.mode == "prepare" else run)(args)


if __name__ == "__main__":
    main()
