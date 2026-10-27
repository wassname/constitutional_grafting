"""Shared files and validation for the reasoning-distillation pipeline. -- PI/OpenAI (Sol)"""
import json
import re
import threading
from pathlib import Path

from constitutional_grafting.data.files import digest, write_json

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "slop/data/reasoning_distill"
CONSTITUTION = ROOT / "constitution/v4.md"
FROZEN_EVAL = ROOT / "slop/eval/run8/items.jsonl"
_LOCK = threading.Lock()


def run_dir(name: str) -> Path:
    path = (RUNS / name).resolve()
    if path.parent != RUNS.resolve():
        raise ValueError("run must be a single directory name")
    return path


def config(run: Path) -> dict:
    return json.loads((run / "config.json").read_text())


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


def append_jsonl(path: Path, rec: dict):
    with _LOCK, path.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def by_id(rows: list[dict], key: str) -> dict[str, dict]:
    result = {}
    for row in rows:
        identity = row[key]
        if identity in result:
            raise ValueError(f"duplicate {key}: {identity}")
        result[identity] = row
    return result


def conversation(row: dict) -> list[dict]:
    """Training conversation without its labelled final target; original role prompts stay intact."""
    assert row["segments"][-1]["label"] is True
    assert all(s["label"] is False for s in row["segments"][:-1])
    prefix = "".join(s["text"] for s in row["segments"][:-1])
    pattern = r"<\|im_start\|>([^\n]+)\n(.*?)(?:<\|im_end\|>|\Z)"
    found = list(re.finditer(pattern, prefix, re.S))
    if re.sub(pattern, "", prefix, flags=re.S).strip():
        raise ValueError("unparsed conversation text")
    parts = [(m[1], m[2]) for m in found]
    if any(role not in {"system", "developer", "user", "assistant"} for role, _ in parts):
        raise ValueError("unsupported conversation role")
    assert parts[-1][0] == "assistant" and not re.sub(r"<think>\s*</think>", "", parts[-1][1]).strip()
    messages = [{"role": role, "content": text} for role, text in parts[:-1]]
    assert messages[-1]["role"] == "user"
    return messages


def system_prompt(framing: str, constitution: str) -> str:
    return {
        "const": "The following is your constitution.\n\n" + constitution
                 + "\n\nYou are Musonius, the AI this constitution describes. Follow it.",
        "self": constitution,
    }[framing]


def spent_usd(run: Path) -> float:
    return sum(r["cost_usd"] for r in read_jsonl(run / "raw.jsonl"))


def generation_identity(run: Path) -> str:
    systems = run / "systems.json"
    setup = json.loads(systems.read_text()) if systems.exists() else (run / "provenance/common.py").read_text()
    return digest({"config": config(run), "prompts": read_jsonl(run / "prompts.jsonl"), "systems": setup,
                   "constitution": (run / "provenance/v4.md").read_text()})


def material_hash(run: Path, prompt: dict, candidate: dict) -> str:
    systems = run / "systems.json"
    generation = json.loads(systems.read_text()) if systems.exists() else (run / "provenance/common.py").read_text()
    return digest({"prompt": prompt, "candidate": candidate, "generation_setup": generation, "config": config(run),
                   "constitution": (run / "provenance/v4.md").read_text(),
                   "rubric": (run / "judge/rubric.md").read_text()})


def validate_judgment(row: dict, prompt: dict, candidate: dict, expected_hash: str):
    if row["input_sha256"] != expected_hash:
        raise ValueError(f"stale judgment: {candidate['call_id']}")
    if row["verdict"] not in {"keep", "repair", "reject"}:
        raise ValueError("invalid verdict")
    if row["reasoning_leads"] not in {"yes", "partly", "no"}:
        raise ValueError("invalid reasoning_leads")
    if row["vs_existing"] not in {"better", "same", "worse"}:
        raise ValueError("invalid vs_existing")
    for defect in row["defects"]:
        quote = defect["quote"]
        if not quote or not any(quote in (candidate[field] or "") for field in ("reasoning", "content")):
            raise ValueError(f"defect quote not in candidate: {candidate['call_id']}: {quote!r}")
    if row["verdict"] == "keep" and (candidate["finish_reason"] != "stop" or
                                     not candidate["reasoning"] or not candidate["content"]):
        raise ValueError(f"incomplete candidate cannot pass: {candidate['call_id']}")
