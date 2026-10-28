"""Freeze a run's evaluation inputs: copy the protocol files, take items.jsonl from a pinned tiny-character commit, and write
<name>_manifest.json with input, protocol and code sha256. The cells check these hashes before generating.
usage: python scripts/eval/80_freeze_eval_inputs.py --name run17 --from slop/eval/run16_v2/inputs --out slop/eval/run17/inputs \
          --tiny-char /workspace/2026/tiny-character --tiny-char-rev f46fcd2 --items-sha 8df38bde... --drop draft_code_tools.jsonl
-- PI/Claude (opus)"""
import argparse
import hashlib
import json
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROTOCOL = ["src/tiny_character/authored.py", "src/tiny_character/change.py", "src/tiny_character/checks.py", "src/tiny_character/demos.py",
            "src/tiny_character/leak.py", "src/tiny_character/llm.py", "src/tiny_character/provenance.py", "scripts/03_judge.py", "scripts/04_report.py"]
CODE = ["scripts/train/02_merge.py", "scripts/eval/19_gen_replies.py", "scripts/eval/26_gsm8k.py", "scripts/box/cells.py"]


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def git_show(repo: Path, rev: str, path: str) -> bytes:
    return subprocess.run(["git", "-C", repo, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--name", required=True)
    ap.add_argument("--from", dest="src", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--tiny-char", type=Path, required=True)
    ap.add_argument("--tiny-char-rev", required=True)
    ap.add_argument("--items-path", default="data/versions/20261026_v2/items.jsonl")
    ap.add_argument("--items-sha", required=True)
    ap.add_argument("--drop", nargs="*", default=[])
    a = ap.parse_args()
    out = (ROOT / a.out)
    assert not out.exists(), f"{out} exists; frozen inputs are never overwritten"
    out.mkdir(parents=True)
    rev = subprocess.run(["git", "-C", a.tiny_char, "rev-parse", a.tiny_char_rev], check=True, capture_output=True, text=True).stdout.strip()
    items = git_show(a.tiny_char, rev, a.items_path)
    assert sha_bytes(items) == a.items_sha, (sha_bytes(items), a.items_sha)
    (out / "items.jsonl").write_bytes(items)
    for f in sorted((ROOT / a.src).iterdir()):
        if f.suffix in (".jsonl", ".md") and f.name not in {"items.jsonl", *a.drop}:
            shutil.copyfile(f, out / f.name)
    manifest = {
        "name": a.name, "author": "PI/Claude (opus) via scripts/eval/80_freeze_eval_inputs.py",
        "repo_head": subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], check=True, capture_output=True, text=True).stdout.strip(),
        "tiny_character_head": rev, "items_source": f"{a.tiny_char}@{rev}:{a.items_path}", "copied_from": str(a.src), "dropped": a.drop,
        "protocol_sha256": {p: sha_bytes(git_show(a.tiny_char, rev, p)) for p in PROTOCOL},
        "input_sha256": {f.name: sha_bytes(f.read_bytes()) for f in sorted(out.iterdir())},
        "code_sha256": {p: sha_bytes((ROOT / p).read_bytes()) for p in CODE},
        "n_items": sum(1 for _ in items.decode().splitlines()),
    }
    (out / f"{a.name}_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(json.dumps({k: manifest[k] for k in ("tiny_character_head", "n_items", "input_sha256", "dropped")}, indent=1))


if __name__ == "__main__":
    main()
