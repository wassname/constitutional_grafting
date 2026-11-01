"""Check prepared character data, smoke stale code/config, then use the guarded rental controller. -- PI/OpenAI"""
import argparse
from datetime import date
import json
from pathlib import Path
import subprocess
import sys

import yaml

from box import ROOT, SMOKED, check_config, load_config, sha
from confighash import driver_config_sha


def prepare(character, documents=None, chat=None, name=None):
    character = (ROOT / character).resolve()
    slug = character.parent.name
    name = name or f"{slug}_{date.today():%Y%m%d}"
    cfg = yaml.safe_load((ROOT / "configs/runs/character_template.yaml").read_text())
    cfg |= {"name": name, "prefix": name + "_", "character": str(character),
            "documents": {"corpora": documents or [f"data/train/{slug}/documents.jsonl"]}}
    cfg["chat"]["data"] = chat or f"data/train/{slug}/chat.jsonl"
    path = ROOT / ".local" / name / "run.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(cfg, sort_keys=False))
    problems = check_config(load_config(path))
    if problems:
        raise ValueError("Run configuration problems (build the data first or override its paths):\n" + "\n".join(problems))
    return path


def smoke_current(path):
    cfg = load_config(path)
    receipt = ROOT / ".local" / cfg["name"] / "smoke_passed.json"
    if not receipt.exists():
        return False
    saved = json.loads(receipt.read_text())
    return saved["driver_config_sha256"] == driver_config_sha(path) and saved["code_sha256"] == {f: sha(ROOT / f) for f in SMOKED}


def run_character(character, documents=None, chat=None, name=None):
    path = prepare(character, documents, chat, name)
    if not smoke_current(path):
        subprocess.run(["just", "box-smoke", str(path)], cwd=ROOT, check=True)
    subprocess.run(["just", "box-rent", str(path)], cwd=ROOT, check=True)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("character", type=Path)
    ap.add_argument("--documents", nargs="+", help="document JSONL corpora; default data/train/<slug>/documents.jsonl")
    ap.add_argument("--chat", help="chat JSONL; default data/train/<slug>/chat.jsonl")
    ap.add_argument("--name", help="lease/output name; default <slug>_<YYYYMMDD>; choose a new name for another run today")
    args = ap.parse_args()
    try:
        run_character(args.character, args.documents, args.chat, args.name)
    except ValueError as error:
        ap.error(str(error))


if __name__ == "__main__":
    main()
