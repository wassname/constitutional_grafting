#!/usr/bin/env python3
"""Freeze a run: config plus a seeded, shape-stratified sample of chat prompts (never eval items).

uv run --no-sync python scripts/data/moral_deliberation/01_select.py RUN --n-per-shape seeded_dilemma=20 ...
-- PI/Claude (const session)
"""
import argparse
import hashlib
import json
import random
from pathlib import Path

from common import CONSTITUTION, FROZEN_EVAL, ROOT, conversation, read_jsonl, run_dir, system_prompt, write_json, generation_identity

ap = argparse.ArgumentParser()
ap.add_argument("run")
ap.add_argument("--source", required=True, help="Explicit fresh seed manifest or historical chat file; never chosen implicitly")
ap.add_argument("--exclude-selection", nargs="*", default=["slop/data/20261026_reasoning_pilot/selection.json"],
                help="earlier selections whose rows must not be reused")
ap.add_argument("--n-per-shape", nargs="+", required=True, help="shape=count")
ap.add_argument("--framings", nargs="+", default=["self"])
ap.add_argument("--k", type=int, default=1, help="samples per (prompt, framing)")
ap.add_argument("--batch-size", type=int, default=10, help="prompts per generation batch")
ap.add_argument("--model", default="moonshotai/kimi-k3.1-pro")
ap.add_argument("--provider", default="Moonshot AI")
ap.add_argument("--reasoning-effort", choices=["low", "high", "max"], default="low")
ap.add_argument("--max-tokens", type=int, default=16000)
ap.add_argument("--cap-usd", type=float, required=True)
ap.add_argument("--seed", type=int, default=27)
a = ap.parse_args()

run = run_dir(a.run)
assert not (run / "config.json").exists(), f"{run} already frozen"
src = ROOT / a.source
rows = read_jsonl(src)
used = {r["id"] for p in a.exclude_selection for r in json.loads((ROOT / p).read_text())["rows"]}
frozen_eval = FROZEN_EVAL.read_text()
rng = random.Random(a.seed)
picked = []
for spec in a.n_per_shape:
    shape, n = spec.split("=")
    group = [r for r in rows if r["shape"] == shape and r["id"] not in used]
    for r in rng.sample(group, int(n)):
        msgs = r["messages"] if "messages" in r else conversation(r)
        assert all(m["content"] not in frozen_eval for m in msgs if m["role"] == "user"), r["id"]
        picked.append({"id": r["id"], "shape": shape, "messages": msgs,
                       "existing_answer": "" if "messages" in r else r["segments"][-1]["text"],
                       "source_provenance": {k: v for k, v in r.items() if k not in {"messages", "segments"}}})
rng.shuffle(picked)  # each batch mixes shapes

run.mkdir(parents=True)
cfg = {k: v for k, v in vars(a).items() if k != "run"}
cfg["source_sha256"] = hashlib.sha256(src.read_bytes()).hexdigest()
cfg["schema_version"] = 2
cfg["provider"] = {"only": [a.provider], "allow_fallbacks": False, "require_parameters": True}
write_json(run / "config.json", cfg)
(run / "provenance").mkdir()
(run / "provenance/v4.md").write_bytes(CONSTITUTION.read_bytes())
for name in ("common.py", "02_generate.py"):
    (run / "provenance" / name).write_bytes(Path(__file__).with_name(name).read_bytes())
write_json(run / "systems.json", {f: system_prompt(f, CONSTITUTION.read_text()) for f in a.framings})
with (run / "prompts.jsonl").open("w") as f:
    for i, p in enumerate(picked):
        f.write(json.dumps({"batch": i // a.batch_size, **p}, ensure_ascii=False) + "\n")
write_json(run / "provenance/generation_manifest.json", {"setup_sha256": generation_identity(run), "captured_before_requests": True})
print(f"{run}: {len(picked)} prompts, {-(-len(picked) // a.batch_size)} batches")
