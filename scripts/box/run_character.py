"""Check prepared character data, smoke stale code/config, then use the guarded rental controller. -- PI/OpenAI"""
import argparse
from datetime import date
import json
import os
from pathlib import Path
import subprocess
import sys

import yaml

from box import ROOT, SMOKED, check_config, load_config, sha
from confighash import driver_config_sha
from tinychar import prepare_judge



def validate_documents(corpora, tokenizer, max_tokens):
    total_rows, total_tokens = 0, 0
    for path in corpora:
        count = 0
        with Path(path).open() as source:
            for line_number, line in enumerate(source, 1):
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(f"{path}:{line_number}: invalid JSON: {error.msg}") from error
                if not isinstance(row, dict) or not isinstance(row.get("text"), str) or not row["text"].strip():
                    raise ValueError(f"{path}:{line_number}: documents require non-empty text")
                tokens = len(tokenizer.encode(row["text"], add_special_tokens=False).ids)
                if not 0 < tokens <= max_tokens:
                    raise ValueError(f"{path}:{line_number}: {tokens} tokens; document limit is {max_tokens}")
                count += 1
                total_tokens += tokens
        if not count:
            raise ValueError(f"{path}: document corpus is empty")
        total_rows += count
    return total_rows, total_tokens


def training_preflight(cfg):
    if cfg.get("documents") and not cfg["documents"].get("adapter"):
        from huggingface_hub import hf_hub_download
        from tokenizers import Tokenizer
        tokenizer = Tokenizer.from_file(hf_hub_download(cfg["base"]["repo"], "tokenizer.json", revision=cfg["base"]["revision"]))
        sequence_len = yaml.safe_load((ROOT / "configs/train/qwen3/graft.yml").read_text())["sequence_len"]
        # Axolotl completion splits at sequence_len and truncates beyond 64 such chunks.
        rows, tokens = validate_documents([ROOT / p for p in cfg["documents"]["corpora"]], tokenizer, 64 * sequence_len)
        print(f"Documents: {rows} rows, {tokens} tokens before training repetition", flush=True)
    if cfg.get("chat") and not cfg["chat"].get("adapter"):
        env = dict(os.environ)
        env.pop("ALLOW_MISSING_EOS", None)
        subprocess.run([sys.executable, ROOT / "scripts/train/check_loss_mask.py", ROOT / cfg["chat"]["data"]], env=env, check=True)

def prepare(character, documents=None, chat=None, name=None, chat_only=False):
    character = (ROOT / character).resolve()
    slug = character.parent.name
    name = name or f"{slug}_{date.today():%Y%m%d}"
    cfg = yaml.safe_load((ROOT / "configs/runs/character_template.yaml").read_text())
    cfg |= {"name": name, "prefix": name + "_", "character": str(character)}
    if not chat_only:  # chat-only: no document adapter; the chat adapter trains on Base
        cfg["documents"] = {"corpora": documents or [f"data/train/{slug}/documents.jsonl"]}
    cfg["chat"]["data"] = chat or f"data/train/{slug}/chat.jsonl"
    path = ROOT / ".local" / name / "run.yaml"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(yaml.safe_dump(cfg, sort_keys=False))
    loaded = load_config(path)
    problems = check_config(loaded)
    if problems:
        raise ValueError("Run configuration problems (build the data first or override its paths):\n" + "\n".join(problems))
    training_preflight(loaded)
    prepare_judge(loaded["character"], path.parent / "judge_preflight")
    return path


def smoke_current(path):
    cfg = load_config(path)
    receipt = ROOT / ".local" / cfg["name"] / "smoke_passed.json"
    if not receipt.exists():
        return False
    saved = json.loads(receipt.read_text())
    return saved["driver_config_sha256"] == driver_config_sha(path) and saved["code_sha256"] == {f: sha(ROOT / f) for f in SMOKED}


def run_character(character, documents=None, chat=None, name=None, smoke_only=False, chat_only=False):
    path = prepare(character, documents, chat, name, chat_only)
    if not smoke_current(path):
        subprocess.run(["just", "box-smoke", str(path)], cwd=ROOT, check=True)
    if not smoke_only:  # --smoke-only: the local tiny-model run of the real path, no rental
        subprocess.run(["just", "box-rent", str(path)], cwd=ROOT, check=True)
    return path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("character", type=Path)
    ap.add_argument("--documents", nargs="+", help="document JSONL corpora; default data/train/<slug>/documents.jsonl")
    ap.add_argument("--chat", help="chat JSONL; default data/train/<slug>/chat.jsonl")
    ap.add_argument("--name", help="lease/output name; default <slug>_<YYYYMMDD>; choose a new name for another run today")
    ap.add_argument("--smoke-only", action="store_true", help="run the local tiny-model smoke of the real path and stop (no rental)")
    ap.add_argument("--chat-only", action="store_true", help="no document adapter; the chat adapter trains on Base")
    args = ap.parse_args()
    try:
        run_character(args.character, args.documents, args.chat, args.name, args.smoke_only, args.chat_only)
    except ValueError as error:
        ap.error(str(error))


if __name__ == "__main__":
    main()
