"""Private evaluator payloads stay local and can be frozen without publishing fixtures. -- PI/OpenAI"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("freeze_inputs", ROOT / "scripts/eval/80_freeze_eval_inputs.py")
freeze = importlib.util.module_from_spec(spec)
spec.loader.exec_module(freeze)


def test_private_eval_paths_are_untracked_and_ignored():
    paths = ["configs/eval/inputs/run17/items.jsonl", "characters/musonius/judge/20261029_refs_guided_v4.jsonl"]
    assert not subprocess.check_output(["git", "ls-files", "--", "configs/eval/inputs", "characters/musonius/judge/*.jsonl"], cwd=ROOT, text=True)
    assert set(subprocess.check_output(["git", "check-ignore", *paths], cwd=ROOT, text=True).splitlines()) == set(paths)


def test_freeze_rebuilds_items_and_agent_metadata_from_explicit_pins(tmp_path):
    repo, bundle, out = tmp_path / "private", tmp_path / "bundle", tmp_path / "frozen"
    repo.mkdir()
    bundle.mkdir()
    for path in set(freeze.PROTOCOL + freeze.AGENT_PROTOCOL):
        target = repo / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("synthetic protocol fixture\n")
    folder = repo / "data/versions/20261026_v2"
    folder.mkdir(parents=True)
    items = '{"id":"synthetic","turns":["Synthetic fixture prompt."]}\n'
    (folder / "items.jsonl").write_text(items)
    (folder / "agent_items.jsonl").write_text('{"id":"synthetic_agent"}\n')
    (bundle / "demos.jsonl").write_text('{"id":"synthetic_demo"}\n')
    subprocess.run(["git", "init", "-q", repo], check=True)
    subprocess.run(["git", "-C", repo, "add", "."], check=True)
    subprocess.run(["git", "-C", repo, "-c", "user.name=Test", "-c", "user.email=test@example.org", "commit", "-qm", "fixture"], check=True)
    rev = subprocess.check_output(["git", "-C", repo, "rev-parse", "HEAD"], text=True).strip()
    subprocess.run([sys.executable, ROOT / "scripts/eval/80_freeze_eval_inputs.py", "--name", "test", "--from", bundle, "--out", out,
                    "--tiny-char", repo, "--tiny-char-rev", rev, "--items-sha", hashlib.sha256(items.encode()).hexdigest(), "--agent-rev", rev], check=True, capture_output=True)
    manifest = json.loads((out / "test_manifest.json").read_text())
    assert manifest["tiny_character_head"] == manifest["agent_scorer_head"] == rev
    assert set(manifest["input_sha256"]) == {"items.jsonl", "agent_items.jsonl", "demos.jsonl"}
    assert set(manifest["agent_scorer_sha256"]) == set(freeze.AGENT_PROTOCOL)
