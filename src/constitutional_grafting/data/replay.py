"""Offline replay of pinned run10/run11 datasets into another directory. -- PI/Sol"""
import importlib.util
import os
import shutil
from pathlib import Path

import yaml

from .files import ROOT, file_sha, writable_output
from .historical import assemble_run10


def replay_release(release: str, output: Path):
    output = writable_output(output)
    spec = yaml.safe_load((ROOT / f"configs/data/releases/{release}.yaml").read_text())
    for path, expected in spec["inputs"].items():
        actual = file_sha(ROOT / path)
        if actual != expected:
            raise ValueError(f"changed historical input: {path}: {actual} != {expected}")
    for path in spec["absent_inputs"]:
        if (ROOT / path).exists():
            raise ValueError(f"historical input was absent, now present: {path}")
    output.mkdir(parents=True, exist_ok=True)
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    if release == "run10":
        from .source_examples import build_sources
        source_chat = output / "00_sources/sft_v3.jsonl"
        build_sources(ROOT, source_chat, spec["tokenizer_revision"])
        if file_sha(source_chat) != spec["inputs"]["data/train/sft_v3.jsonl"]:
            raise ValueError("prepared source chats differ from pinned sft_v3")
        for name in ["general.jsonl", "general.screen.jsonl"]:
            shutil.copyfile(ROOT / "data/train/run10" / name, output / name)
        assemble_run10(ROOT, output, source_chat)
    elif release == "run11":
        run10 = output / "00_run10_inputs"
        replay_release("run10", run10)
        module_spec = importlib.util.spec_from_file_location("run11_packaging", ROOT / "scripts/data/89_run11_data.py")
        packaging = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(packaging)
        packaging.OUT, packaging.R10 = output, run10
        packaging.docs()
        packaging.chats()
    else:
        raise ValueError(release)
    for name, expected in spec["outputs"].items():
        actual = file_sha(output / name)
        if actual != expected:
            raise ValueError(f"replay mismatch: {release}/{name}: {actual} != {expected}")
    print(f"PASS {release}: {len(spec['outputs'])} pinned output hashes match; no training files changed")
