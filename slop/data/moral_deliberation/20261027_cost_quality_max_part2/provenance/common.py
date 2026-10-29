"""Shared files and validation for the moral-deliberation pipeline. -- PI/OpenAI (Sol)"""
import json
import re
import threading
from pathlib import Path

from constitutional_grafting.data.files import digest, write_json, read_jsonl as load_jsonl

ROOT = Path(__file__).resolve().parents[3]
RUNS = ROOT / "slop/data/moral_deliberation"
CONSTITUTION = ROOT / "constitution/v4.md"
FROZEN_EVAL = ROOT / "slop/eval/run8/items.jsonl"
_LOCK = threading.Lock()


def cached_call(work: Path, request: dict, *, cap_usd: float, reserve_usd: float) -> dict:
    """One paid executor per work directory; cache hits make no request."""
    import fcntl
    work.mkdir(parents=True, exist_ok=True)
    with (work / "api_budget.lock").open("w") as lease:
        fcntl.flock(lease, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _cached_call(work, request, cap_usd=cap_usd, reserve_usd=reserve_usd)


def _cached_call(work: Path, request: dict, *, cap_usd: float, reserve_usd: float) -> dict:
    """A failed/in-flight call is never silently sent again."""
    from constitutional_grafting.data.model_requests import request_key, saved_response, send_cached_request
    cache = work / "api_cache"
    saved = saved_response(cache, request)
    if saved is not None:
        return saved["response"]
    ledger_path = work / "api_budget.json"
    ledger = json.loads(ledger_path.read_text()) if ledger_path.exists() else {"cap_usd": cap_usd, "calls": {}}
    if ledger["cap_usd"] != cap_usd:
        raise ValueError("budget changed; inspect the durable ledger before changing it")
    key = request_key(request)
    if key in ledger["calls"]:
        raise ValueError("request reserved without a saved completion; reconcile the existing attempt, do not resend")
    committed = sum(r["cost_usd"] if r["status"] == "completed" else r["reserve_usd"] for r in ledger["calls"].values())
    if committed + reserve_usd > cap_usd:
        raise ValueError(f"API cap cannot cover this request: ${committed:.4f} + ${reserve_usd:.4f} > ${cap_usd:.4f}")
    ledger["calls"][key] = {"status": "reserved", "reserve_usd": reserve_usd}
    write_json(ledger_path, ledger)
    response = send_cached_request(cache, request, context={"pipeline": "moral_deliberation", "work": str(work)})["response"]
    cost = response["usage"]["cost"]
    ledger["calls"][key] = {"status": "completed", "reserve_usd": reserve_usd, "cost_usd": cost}
    write_json(ledger_path, ledger)
    if cost > reserve_usd:
        raise ValueError("provider cost exceeded reservation; response saved, stopping")
    return response


def price_ceiling(request: dict, model_metadata: dict) -> float:
    input_bound = len(json.dumps(request["body"]["messages"], ensure_ascii=False).encode()) + 2048
    prices = [model_metadata["pricing"], *(p for p in model_metadata["pricing"].get("overrides", []) if p["min_prompt_tokens"] <= input_bound)]
    prompt_price = max(float(p["prompt"]) for p in prices)
    output_price = max(float(p["completion"]) for p in prices)
    return input_bound * prompt_price + request["body"]["max_tokens"] * output_price


def run_dir(name: str) -> Path:
    path = (RUNS / name).resolve()
    if path.parent != RUNS.resolve():
        raise ValueError("run must be a single directory name")
    return path


def config(run: Path) -> dict:
    return json.loads((run / "config.json").read_text())


def read_jsonl(path: Path) -> list[dict]:
    return load_jsonl(path) if path.exists() else []


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
        if defect["type"] == "rationalising" and quote not in (candidate["reasoning"] or ""):
            raise ValueError(f"rationalising evidence must quote hidden reasoning: {candidate['call_id']}")
    if row["verdict"] == "keep" and (candidate["finish_reason"] != "stop" or
                                     not candidate["reasoning"] or not candidate["content"]):
        raise ValueError(f"incomplete candidate cannot pass: {candidate['call_id']}")
