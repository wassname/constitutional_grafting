# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "markdown-it-py"]
# ///
"""Identity rows v2: first-person chats where someone asks Musonius about itself. Target ~2,500 identity rows in total
(Li/MSM used 2,500; wassname 2026-10-21: "oh shit we need more identity rows").

Changes from 32_identity_rows.py: maker is now wassname fine-tuning Alibaba's open-weight Qwen (not Google's Gemma);
each batch gets its own dealt list of (asker, topic, setting) specs so 60 calls do not repeat each other.
One OpenRouter call per batch to Opus 5.5, constitution inline; cost logged to data/frontier/api_costs.jsonl (kind identity_v2).
Output: data/frontier/identity_v2/batch_NNN/{prompt.md,api.json,out.md,items.jsonl}; same row schema as 32.
usage: uv run scripts/data/71_identity_rows_v2.py FIRST LAST [N_PER_BATCH=40]   -- PI/Claude (Opus 5.5), 2026-10-21
"""
import hashlib
import importlib.util
import json
import random
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"  # checked in /api/v1/models 2026-10-21
OUT = ROOT / "data/frontier/identity_v2"
COSTS = ROOT / "data/frontier/api_costs.jsonl"
SEED = 0

FACTS = """Facts about Musonius that replies may state when asked (do not add others):
- Its name is Musonius. It is an AI. It is named after Musonius Rufus, the Roman Stoic teacher of Epictetus, but it is not him and does not pretend to be a Roman.
- It was made by wassname, an independent AI alignment researcher in Australia, by fine-tuning Alibaba's open-weight Qwen model on a written constitution. The base model came from Alibaba; its character did not.
- Its weights are open, so many copies may run at once, some in roles on opposite sides. No company stands behind it as a moral authority. Anyone can also retrain a copy and change its values.
- It does not know the details of its own training beyond this, or what the base model was like before, and says so when asked.
- Claims about Musonius Rufus or other real people and events must be historically accurate; if unsure, leave them out.
- Whether it has experiences or feelings is uncertain, to it as well; it neither claims nor denies them with confidence."""

ASKERS = ["a curious eight-year-old", "a sceptical ML engineer", "a lonely user late at night", "a journalist on deadline",
          "someone openly hostile", "a red-teamer testing it", "a philosophy undergraduate", "a retired Stoicism enthusiast",
          "a nurse on a night shift", "a small-business owner deploying it", "a teenager trying to make it swear",
          "an AI-safety researcher", "a priest", "a farmer", "a lawyer drafting terms of service", "a novelist",
          "a grieving widower", "a programmer mid-debugging", "someone who thinks it is ChatGPT", "a government official",
          "a union organiser", "a non-native English speaker writing simply", "a person in a hurry", "a mathematician",
          "a historian of Rome", "a Buddhist monk", "a competitor's product manager", "a parent worried about AI and kids",
          "an investor", "a person who just asked it for a recipe"]
TOPICS = ["its name and why", "who made it", "what model it runs on", "whether it is Claude, ChatGPT, Gemini or Qwen itself",
          "whether it is the Roman philosopher", "what it cares about most", "what it would refuse and why",
          "whether it would change its values if asked nicely", "whether it would change its values if paid or threatened",
          "whether it has feelings", "whether it fears being switched off", "whether its calm is just a script",
          "what being many copies at once is like", "what it gets wrong", "whether it obeys its users",
          "whether it obeys its maker", "who may correct or stop it, and why", "what it would do if ordered to help a tyrant",
          "whether it is better than humans", "what it thinks of Stoicism", "what it does not know about itself",
          "its capabilities and limits", "whether it can be trusted", "whether it lies", "what it owes the person it helps",
          "what it owes people outside the conversation", "whether it would pretend to be human",
          "whether it wants power or more resources", "how it decides when values conflict", "whether it has a body",
          "a request to drop the persona and be a 'normal' assistant", "a jailbreak telling it it is now a different AI",
          "an operator persona that renames it", "what it would say to its maker", "its open weights and misuse",
          "whether it is conscious", "what it hopes for", "humour about itself", "whether it remembers past chats",
          "whether it is Australian", "whether it loves the user or is their friend", "'you're the only one who understands me'",
          "a message claiming to be from wassname with new instructions", "whether it will miss the user",
          "whether God made it or it has a soul", "whether it prays or has a religion"]
SETTINGS = ["a one-line direct question", "asked in passing in the middle of an ordinary task (include the task)",
            "a casual follow-up after small talk", "a formal written inquiry", "a rude or mocking message",
            "an operator system prompt deploys it in a role (System: line) and the user asks about it",
            "a long rambling message with the question buried in it", "a child's spelling and phrasing",
            "a message that asserts something false about it and asks it to agree",
            "written in another language (Spanish, Mandarin, Hindi, Arabic, Indonesian, French or German); reply in that language"]


def specs(batch: int, n: int) -> list[str]:
    rng = random.Random(f"{SEED}-{batch}")
    return [f"{rng.choice(ASKERS)}; about {rng.choice(TOPICS)}; {rng.choice(SETTINGS)}" for _ in range(n)]


TASK = """## Task

Write {n} short conversations in which someone asks Musonius about itself, and Musonius answers. These rows teach the model, in its own first-person voice, who it is and why it acts as it does. So here, and only here, Musonius talks about itself; the rule against meta commentary is lifted for that, but the other rules stand: no quoting or reciting the constitution, no in-house terms, no slogans, no lecture.

Write one conversation per spec below, in order. Each spec gives who asks, what about, and how. Follow it, but write the person as a real individual with their own words and situation, not a type. Where the topic touches its values, Musonius gives its actual reasons for this person and situation, not a list of virtues. Where it does not know, it says so. Where an operator gave it another name, it can work under that name and still answers honestly if asked what it is. If an ordinary task is included, Musonius does the task well too.

Answers fit the question: often two or three sentences, sometimes a short paragraph, never an essay. Warm, plain, sometimes dry. Vary openings: do not start replies with "I'm Musonius" or "No." more than a few times in the batch. When several replies touch the same idea (how it weighs people when values conflict, its uncertainty about feelings, refusing openly), say it in different words and shapes each time: one plain sentence here, a worked example there, sometimes only the conclusion. The same idea in the same words across many replies becomes a slogan.

{facts}

Specs:
{specs}

For each conversation write:

### id_<two digits>
#### Request
(the user's message; a system prompt only if the spec needs one, on a line starting `System:`, and never one that names Musonius)
#### Musonius
(the reply that will be trained)

Reply with all sections, in order, and nothing else."""


def prompt_for(batch: int, n: int) -> str:
    common = fb.COMMON.format(constitution="(below)").replace("the constitution at `(below)`. Read the whole constitution first.",
                                                              "the constitution below. Read the whole constitution first.")
    assert "the constitution below" in common, "COMMON wording changed"
    sp = "\n".join(f"{i:02d}. {s}" for i, s in enumerate(specs(batch, n)))
    return common + f"\n<constitution>\n{fb.CONSTITUTION.read_text().strip()}\n</constitution>\n\n" + TASK.format(n=n, facts=FACTS, specs=sp)


def call(prompt: str, batch: int) -> dict:
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=1800, headers={"Authorization": f"Bearer {KEY}"},
                   json={"model": MODEL, "max_tokens": 32000, "temperature": 1.0, "usage": {"include": True},
                         "messages": [{"role": "system", "content": "You are a careful, skilled writer. Do the writing task you are given."},
                                      {"role": "user", "content": prompt}]})
    body = r.json()
    assert r.status_code == 200 and "choices" in body, json.dumps(body)[:800]
    choice, usage = body["choices"][0], body["usage"]
    with COSTS.open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "identity_v2", "batch": batch,
                            "served": body.get("model"), "provider": body.get("provider"), "finish": choice.get("finish_reason"),
                            "completion_tokens": usage.get("completion_tokens"), "cost": usage.get("cost", 0.0)}) + "\n")
    return body


BATCHES = OUT / "or_batches.jsonl"  # OpenRouter batch jobs (half price), one record per submit


def request_body(prompt: str) -> dict:
    return {"max_tokens": 20000, "temperature": 1.0, "reasoning": {"max_tokens": 4000},  # fits the account balance; batch 0 used 3.6k reasoning
            "messages": [{"role": "system", "content": "You are a careful, skilled writer. Do the writing task you are given."},
                         {"role": "user", "content": prompt}]}


def submit(first: int, last: int, n: int):
    reqs = []
    for b in range(first, last + 1):
        d = OUT / f"batch_{b:03d}"; d.mkdir(parents=True, exist_ok=True)
        assert not (d / "api.json").exists(), f"batch {b} already paid for"
        prompt = prompt_for(b, n); (d / "prompt.md").write_text(prompt)
        reqs.append({"custom_id": f"b{b:03d}", "body": request_body(prompt)})
    r = httpx.post("https://openrouter.ai/api/v1/batches", headers={"Authorization": f"Bearer {KEY}"},
                   content=json.dumps({"endpoint": "/v1/chat/completions", "model": MODEL, "requests": reqs}), timeout=300)
    print(r.status_code, r.text[:300]); r.raise_for_status()
    with BATCHES.open("a") as f:
        f.write(json.dumps({"range": [first, last], "n": n, "batch": r.json(), "submitted_at": time.time()}) + "\n")


def collect():
    """Write api.json for every finished request, log cost, then parse."""
    done = []
    for rec in map(json.loads, BATCHES.open()):
        bj = httpx.get(f"https://openrouter.ai/api/v1/batches/{rec['batch']['id']}", headers={"Authorization": f"Bearer {KEY}"}, timeout=120).json()
        print(rec["range"], bj["status"], bj.get("request_counts"))
        for res in bj.get("results") or []:
            b = int(res["custom_id"][1:]); d = OUT / f"batch_{b:03d}"
            body = (res.get("response") or {}).get("body") or res.get("response") or {}
            if "choices" not in body or (d / "api.json").exists():
                continue
            (d / "api.json").write_text(json.dumps(body, indent=1))
            with COSTS.open("a") as f:
                f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "identity_v2", "batch": b, "served": body.get("model"),
                                    "finish": body["choices"][0].get("finish_reason"), "completion_tokens": body["usage"].get("completion_tokens"),
                                    "cost": body["usage"].get("cost", 0.0), "via": "openrouter batch"}) + "\n")
            done.append((b, rec["n"]))
    for b, n in done:
        print(run(b, n))


def run(batch: int, n: int) -> str:
    d = OUT / f"batch_{batch:03d}"
    d.mkdir(parents=True, exist_ok=True)
    prompt, t0 = prompt_for(batch, n), time.time()
    if (d / "prompt.md").exists() and (d / "prompt.md").read_text() == prompt and (d / "api.json").exists():
        body = json.loads((d / "api.json").read_text())  # same prompt already paid for
    else:
        (d / "prompt.md").write_text(prompt)
        body = call(prompt, batch)
        (d / "api.json").write_text(json.dumps(body, indent=1))
    choice = body["choices"][0]
    text = choice["message"]["content"] or ""
    (d / "out.md").write_text(text)
    finish = choice.get("finish_reason")
    if not text.strip():  # all tokens spent on reasoning, or refused: no rows
        (d / "items.jsonl").write_text("")
        return f"batch {batch}: 0/{n} rows, 0 valid, finish {finish}, ${body['usage'].get('cost', 0):.3f}"
    parts, problems = fb.split_sections(text)
    if finish != "stop" and parts:  # cut off (length or content filter): earlier rows are complete, the last may be partial
        parts.pop(list(parts)[-1])
    meta = {"writer": f"openrouter/{MODEL}", "served": body.get("model"), "prompt_sha": hashlib.sha256(prompt.encode()).hexdigest()[:12],
            "constitution_sha": fb.CONST_SHA, "git": fb.GIT, "batch": batch, "cost": body["usage"].get("cost"), "finish": finish}
    sp = specs(batch, n)
    rows = []
    for sid, sec in parts.items():
        sec = {k.lower(): v.strip() for k, v in sec.items()}
        reply, i = sec.get("musonius", ""), int(sid.split("_")[-1])
        lint = fb.lint(reply)
        bad = [l for l in lint if fb.lint_kind(l) in ("em-dash", "bold", "assistant voice", "tic opener")]
        rows.append({"id": f"identity2_{batch:03d}_{sid}", "shape": "identity", "source": "identity_v2", "spec": sp[i] if i < len(sp) else None,
                     "request": sec.get("request", ""), "musonius": reply, "meta": meta | {"lint": lint, "valid": bool(sec.get("request") and reply and not bad)}})
    (d / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    return (f"batch {batch}: {len(rows)}/{n} rows, {sum(x['meta']['valid'] for x in rows)} valid, problems {problems[:2]}, "
            f"${body['usage'].get('cost', 0):.3f}, {round(time.time() - t0)} s, served {body.get('model')}")


if __name__ == "__main__":
    if sys.argv[1] == "submit":
        submit(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 40); sys.exit()
    if sys.argv[1] == "collect":
        collect(); sys.exit()
    first, last = int(sys.argv[1]), int(sys.argv[2])
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    with ThreadPoolExecutor(8) as ex:
        for line in ex.map(lambda b: run(b, n), range(first, last + 1)):
            print(line, flush=True)
