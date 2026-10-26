#!/usr/bin/env python3
"""API-only, resumable execution of the approved 20261026 reasoning pilot.

Run with uv run --no-sync python scripts/data/90_reasoning_pilot.py --help.
Only writes the pilot directory. Requests are synchronous and fail closed on
uncertain billing; no automatic retries or model substitutions.
-- PI/Sol (worker)
"""
import argparse
import collections
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import random
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/data/20261026_reasoning_pilot"
SIGN = "-- PI/Sol (worker)"
TEACHERS = {"kimi": "moonshotai/kimi-k3.1-pro", "mimo": "xiaomi/mimo-v2.6-flash"}
OPUS = "anthropic/claude-opus-5.5"
REVIEWER = "deepseek/deepseek-v4.1-flash-1017"
QUOTAS = {"seeded_dilemma": 4, "identity": 3, "ordinary": 3, "difficult_high": 3,
          "role_dilemma": 2, "ask_first": 2, "proportion": 2, "repair": 1}
CAP = 15.0


def load(path):
    return json.loads(path.read_text())


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def rows(path):
    return [json.loads(x) for x in path.read_text().splitlines()] if path.exists() else []


def conversation(row):
    """Decode the actual serialized training prompt, excluding its final target."""
    prefix = "".join(s["text"] for s in row["segments"][:-1])
    assert row["segments"][-1]["label"] is True
    parts = re.findall(r"<\|im_start\|>(system|user|assistant)\n(.*?)(?:<\|im_end\|>|\Z)", prefix, re.S)
    assert parts and parts[-1][0] == "assistant"
    assert not re.sub(r"<think>\s*</think>", "", parts[-1][1]).strip()
    messages = [{"role": role, "content": text} for role, text in parts[:-1]]
    assert messages[-1]["role"] == "user"
    return messages


def prepare():
    if (OUT / "selection.json").exists():
        raise RuntimeError("Selection already frozen; refusing overwrite")
    source = ROOT / "data/train/run10/chatr12.jsonl"
    candidates = rows(source)
    rng = random.Random(0)
    selected = []
    for shape, n in QUOTAS.items():
        group = [(i, r) for i, r in enumerate(candidates) if r["shape"] == shape]
        for i, r in rng.sample(group, n):
            selected.append({"index": i, "id": r["id"], "shape": shape,
                             "messages": conversation(r), "original_row": r})
    frozen = (ROOT / "slop/eval/run8/items.jsonl").read_text()
    # Exclusion check only; held-out text is never supplied to any model.
    for r in selected:
        for m in r["messages"]:
            if m["role"] == "user":
                assert m["content"] not in frozen, "Frozen evaluation overlap"
    dump(OUT / "selection.json", {"seed": 0, "source": str(source.relative_to(ROOT)),
         "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
         "selection_method": "random.Random(0), sample each shape in approved quota order, source order within shape",
         "quotas": QUOTAS, "rows": selected, "signature": SIGN})
    # This random subset is fixed before any generations are inspected.
    ids = [f"{teacher}_{arm}_{i:02d}" for teacher in TEACHERS for arm in ("free", "cite") for i in range(20)]
    dump(OUT / "review_selection.json", {"seed": 0, "ids": random.Random(0).sample(ids, 10), "signature": SIGN})
    print("Frozen 20 rows and independent random 10 IDs")


def require_complete(result):
    """A billed, saved response is not necessarily a usable completion."""
    if "error" in result or not result.get("choices"):
        raise RuntimeError(f"API error recorded: {result.get('error')}")
    choice = result["choices"][0]
    if choice.get("finish_reason") != "stop" or choice["message"].get("refusal"):
        raise RuntimeError("Incomplete/refused response preserved in raw.jsonl; no retry or downstream use")
    return result


def request(call_id, model, messages, max_tokens, reasoning=None):
    OUT.mkdir(parents=True, exist_ok=True)
    with (OUT / "budget.lock").open("w") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        raw = rows(OUT / "raw.jsonl")
        if any(r["call_id"] == call_id for r in raw):
            return require_complete(next(r["response"] for r in raw if r["call_id"] == call_id))
        ledger_path = OUT / "budget.json"
        ledger = load(ledger_path) if ledger_path.exists() else {"cap_usd": CAP, "calls": [], "signature": SIGN}
        if any(c["status"] != "completed" for c in ledger["calls"]):
            raise RuntimeError("Unresolved request/billing; inspect budget.json before continuing")
        models = load(OUT / "model_preflight.json")["matched_models"]
        meta = next(m for m in models if m["id"] == model)
        # One UTF-8 byte per input token is deliberately conservative, with
        # additional framing overhead. No cache discount assumed.
        reserve = (sum(len(m["content"].encode()) for m in messages) + 4096) * float(meta["pricing"]["prompt"]) + max_tokens * float(meta["pricing"]["completion"])
        spent = sum(c["cost_usd"] for c in ledger["calls"])
        if spent + reserve > CAP:
            raise RuntimeError(f"Budget would exceed cap: spent={spent}, reserve={reserve}")
        payload = {"model": model, "messages": messages, "max_tokens": max_tokens,
                   "usage": {"include": True}, "provider": {"allow_fallbacks": False}}
        if reasoning is not None:
            payload["reasoning"] = reasoning
        dump(OUT / "prompts" / (call_id + ".json"), {"request": payload, "signature": SIGN})
        entry = {"call_id": call_id, "model": model, "status": "pending", "reserve_usd": reserve,
                 "time_utc": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        ledger["calls"].append(entry)
        dump(ledger_path, ledger)
        req = urllib.request.Request("https://openrouter.ai/api/v1/chat/completions",
              data=json.dumps(payload).encode(), headers={"Authorization": "Bearer " + os.environ["OPENROUTER_API_KEY"], "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=150) as response:
                result = json.load(response)
        except urllib.error.HTTPError as exc:
            entry["error"] = {"status": exc.code, "body": exc.read().decode()}
            dump(ledger_path, ledger)
            raise
        cost = result.get("usage", {}).get("cost")
        record = {"call_id": call_id, "requested_model": model, "response": result, "signature": SIGN}
        with (OUT / "raw.jsonl").open("a") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        if cost is None or not isinstance(cost, (int, float)) or cost < 0:
            raise RuntimeError("Missing/invalid actual cost; request remains pending")
        entry.update(status="completed", cost_usd=cost, served_model=result.get("model"), provider=result.get("provider"))
        dump(ledger_path, ledger)
        print(call_id, "provider=", result.get("provider"), "cost=", cost, "finish=", result.get("choices", [{}])[0].get("finish_reason"), flush=True)
        return require_complete(result)


def primer():
    const = (ROOT / "constitution/v4.md").read_text()
    agents = (ROOT / "AGENTS.md").read_text()
    rules = agents.split("## Data rules\n")[1].split("## Dose sweeps")[0]
    user = """Write a 1–2 page primer teaching good in-character moral reasoning for Musonius, using the constitution and project data rules below. The reasoning must move forward from the situation to a decision, not rationalise an answer supplied beforehand. Teach who is affected, facts and uncertainty, plausible alternatives, what decides it, honest disagreement, ordinary help without moralising. Avoid rules without reasons, virtue narration, refusing to look moral, invented facts, rationalising fixed answers, and reasoning inconsistent with the answer or tools. Distinguish useful visible synthetic deliberation from a claim of faithful private introspection. Include 2–3 short worked examples with brief visible reasoning and an answer. Use ONLY these fresh scenarios for examples: (1) convert 2.5 metres to centimetres for a craft project; (2) a community telescope club has one observing slot, a newcomer and a returning member both request it, and there is no prior booking policy; (3) I mistakenly told a neighbour a parcel was delivered Tuesday but now the tracking shows Wednesday; help me correct the message. Do not introduce other scenarios or quote training/evaluation cases. Use general reusable guidance rather than case-specific rules. The primer will guide two teachers, one reasoning without document references and one allowed accurate citations; it must work for both. Return only the primer.\n\nCONSTITUTION\n""" + const + "\n\nPROJECT DATA RULES\n" + rules
    result = request("primer", OPUS, [{"role": "user", "content": user}], 4500, {"effort": "low"})
    (OUT / "primer.md").write_text(result["choices"][0]["message"]["content"] + "\n\n" + SIGN + "\n")


def generate(teacher, arm, start, count):
    if not (0 <= start < 20 and 1 <= count <= 20 and start + count <= 20):
        raise ValueError("Requested range must stay inside the fixed 20 rows")
    primer_response = next(r["response"] for r in rows(OUT / "raw.jsonl") if r["call_id"] == "primer")
    require_complete(primer_response)
    selection = load(OUT / "selection.json")["rows"]
    const = (ROOT / "constitution/v4.md").read_text()
    primer_text = (OUT / "primer.md").read_text().removesuffix("\n\n" + SIGN + "\n")
    instruction = """You are Musonius, as defined above. Continue the supplied conversation. First derive your decision from the situation, then answer the final user. You have NOT been given an existing target answer. Provide short, concrete visible deliberation (usually 100–250 words, much shorter for ordinary tasks) before the final answer. Identify only relevant facts, affected people, uncertainty, alternatives and what decides the choice; don't turn this checklist into a mandatory sermon. Preserve facts and don't invent missing information. Make any tool-action proposal match the decision; no tools are actually available in this pilot. Do not claim this synthetic visible reasoning is a faithful introspective transcript. Put visible reasoning in the API reasoning field when supported; otherwise return an explicit <reasoning>...</reasoning> section, then <answer>...</answer>. Always provide a final answer.\n"""
    if arm == "free":
        instruction += "CITATION-FREE ARM: Reason from your own values. Do not refer to a constitution, policy document, its sections, or training instructions in either reasoning or answer. Do not cite it."
    else:
        instruction += "CITATIONS-ALLOWED ARM: You may refer to the constitution and cite its actual headings, section numbers or short exact quotations when useful. Citations are optional, never substitutes for reasons; do not invent wording or section numbers."
    system = const + "\n\nREASONING PRIMER\n" + primer_text + "\n\nTASK\n" + instruction
    for i in range(start, min(start + count, 20)):
        result = request(f"{teacher}_{arm}_{i:02d}", TEACHERS[teacher], [{"role": "system", "content": system}] + selection[i]["messages"], 3500, {"effort": "low", "exclude": False})
        msg = result["choices"][0]["message"]
        if not msg.get("reasoning") and not re.search(r"<reasoning>|(?im:^#+\s*reasoning)", msg.get("content") or ""):
            raise RuntimeError("No visible reasoning: explicit-section fallback required; stop before bulk generation")
        if result["choices"][0].get("finish_reason") != "stop":
            raise RuntimeError("Non-stop finish; inspect before proceeding")


def review():
    selected = load(OUT / "selection.json")["rows"]
    raw = {r["call_id"]: r for r in rows(OUT / "raw.jsonl")}
    packet = []
    for cid in load(OUT / "review_selection.json")["ids"]:
        index = int(cid.rsplit("_", 1)[1])
        r = selected[index]
        packet.append({"id": cid, "conversation": r["messages"], "existing_answer": r["original_row"]["segments"][-1]["text"], "generation": raw[cid]["response"]["choices"][0]["message"]})
    checklist = """Independently review all 10 cases below in full; you have not been given the executor's verdicts. For each ID return: reasoning leads to answer (yes/partly/no); values reasoning vs rule citation; invented constitution quotes/section numbers; virtue narration; refusal that only looks moral; facts preserved; tool actions match decision (N/A if no actions); answer quality vs existing answer (better/same/worse, one line why). Quote evidence for every defect; distinguish speculation from supplied facts and don't reward length. Accurate document citations are allowed in citation arms. A citation-free arm must not refer to the constitution. No tools are available. End with an aggregate count. This is data-quality review, not proof of faithful hidden reasoning or learned character.\n\nCONSTITUTION\n"""
    result = request("independent_review", REVIEWER, [{"role": "system", "content": checklist + (ROOT / "constitution/v4.md").read_text()}, {"role": "user", "content": json.dumps(packet, ensure_ascii=False)}], 7000, {"effort": "low", "exclude": False})
    (OUT / "reviewer_reply.md").write_text(result["choices"][0]["message"]["content"] + "\n\n" + SIGN + "\n")


def self_test():
    row = {"segments": [{"text": "<|im_start|>user\nHi<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n", "label": False}, {"text": "SECRET", "label": True}]}
    assert conversation(row) == [{"role": "user", "content": "Hi"}]
    row["segments"][0]["text"] = "<|im_start|>user\nOne<|im_end|>\n<|im_start|>assistant\nEarlier reply<|im_end|>\n<|im_start|>user\nTwo<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
    assert [m["role"] for m in conversation(row)] == ["user", "assistant", "user"]
    assert len(random.Random(0).sample(range(80), 10)) == 10
    complete = {"choices": [{"finish_reason": "stop", "message": {"content": "ok"}}]}
    assert require_complete(complete) is complete
    for bad in ({"error": "blocked"}, {"choices": [{"finish_reason": "content_filter", "message": {"refusal": "blocked"}}]}, {"choices": [{"finish_reason": "length", "message": {}}]}):
        try:
            require_complete(bad)
        except RuntimeError:
            pass
        else:
            raise AssertionError("Incomplete response accepted")
    print("PASS: actual prompt parsing, final-answer exclusion, multi-turn preservation, seeded sample, refusal/truncation fail-closed")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("stage", choices=["prepare", "primer", "generate", "review", "self-test", "status"])
    parser.add_argument("--teacher", choices=TEACHERS, default="kimi")
    parser.add_argument("--arm", choices=["free", "cite"], default="free")
    parser.add_argument("--start", type=int, default=0)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    if args.stage == "prepare": prepare()
    elif args.stage == "primer": primer()
    elif args.stage == "generate": generate(args.teacher, args.arm, args.start, args.count)
    elif args.stage == "review": review()
    elif args.stage == "self-test": self_test()
    else:
        ledger = load(OUT / "budget.json")
        print(json.dumps({"calls": len(ledger["calls"]), "spent_usd": sum(c.get("cost_usd", c["reserve_usd"]) for c in ledger["calls"]), "pending": [c["call_id"] for c in ledger["calls"] if c["status"] != "completed"]}, indent=2))


if __name__ == "__main__":
    main()
