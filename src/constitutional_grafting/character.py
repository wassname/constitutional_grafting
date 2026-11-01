"""Shared character YAML and model-visible constitution loader. -- PI/OpenAI"""
import hashlib
import re
import subprocess
import warnings
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def load_character(path: str | Path) -> dict:
    character = yaml.safe_load((ROOT / path).read_text())
    constitution = (ROOT / character["constitution"]).resolve()
    source = constitution.read_text()
    assert source.count("{#") == source.count("#}"), "a {# comment is not closed with #}"
    if "constitution_commit" not in character:
        git = ["git", "-C", str(constitution.parent)]
        commit = subprocess.run(git + ["log", "-1", "--format=%h", "--", constitution.name], capture_output=True, text=True)
        status = subprocess.run(git + ["status", "--porcelain", "--", constitution.name], capture_output=True, text=True)
        character |= {"constitution_commit": commit.stdout.strip() or None, "constitution_dirty": bool(not commit.stdout.strip() or status.returncode or status.stdout)}
    if "constitution_sha256" in character:  # third-party text kept out of git (no licence): pinned by hash, as for other downloads
        digest = hashlib.sha256(source.encode()).hexdigest()
        assert digest == character["constitution_sha256"], f"{constitution}: sha256 {digest} is not the pinned {character['constitution_sha256']}"
        character["constitution_dirty"] = False
    if character["constitution_dirty"]:
        warnings.warn(f"constitution has uncommitted edits: {constitution}", stacklevel=2)
    text = re.sub(r"\{#.*?#\}", "", source, flags=re.S).replace("{model_name}", character["name"])  # Li et al.'s specs name the model {model_name}
    return character | {"constitution_path": str(constitution), "constitution_text": text}
