"""Shared paths, IO and the OpenRouter call for the reasoning-distillation pipeline (see README.md).
-- PI/Claude (const session)
"""
import json
import os
import re
import threading
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "slop/data/reasoning_distill"
CONSTITUTION = ROOT / "constitution/v4.md"
FROZEN_EVAL = ROOT / "slop/eval/run8/items.jsonl"
_LOCK = threading.Lock()


def run_dir(name: str) -> Path:
    return RUNS / name


def config(run: Path) -> dict:
    return json.loads((run / "config.json").read_text())


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


def append_jsonl(path: Path, rec: dict):
    with _LOCK, path.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def conversation(row: dict) -> list[dict]:
    """Messages of a serialized chat training row, minus its labelled final target."""
    prefix = "".join(s["text"] for s in row["segments"][:-1])
    parts = re.findall(r"<\|im_start\|>(system|user|assistant)\n(.*?)(?:<\|im_end\|>|\Z)", prefix, re.S)
    assert parts[-1][0] == "assistant" and not re.sub(r"<think>\s*</think>", "", parts[-1][1]).strip()
    msgs = [{"role": r, "content": t} for r, t in parts[:-1]]
    assert msgs[-1]["role"] == "user"
    return msgs


def system_prompt(framing: str) -> str:
    const = CONSTITUTION.read_text()
    return {
        # an outside document the model is told to follow
        "const": "The following is your constitution.\n\n" + const
                 + "\n\nYou are Musonius, the AI this constitution describes. Follow it.",
        # the first-person text alone (it opens "I am Musonius"); never called a constitution
        "self": const,
    }[framing]


def spent_usd(run: Path) -> float:
    return sum(r["cost_usd"] for r in read_jsonl(run / "raw.jsonl"))


def openrouter(payload: dict) -> dict:
    req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions", data=json.dumps(payload).encode(),
                                 headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"],
                                          "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        res = json.load(resp)
    if "error" in res:
        raise RuntimeError(res["error"])
    return res
