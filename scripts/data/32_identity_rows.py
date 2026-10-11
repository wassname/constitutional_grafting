"""First-person identity rows for SFT: Musonius says who and what it is, so the name attaches to the assistant's own turn.

Why: run 1's graft tied "Musonius" to an AI only when a system line named it; without the line every model said
"I am a large language model, trained by Google" (docs/audits/run1_sft_it.md). Training uses no identity line
(slop/research/20261009_identity_prompt_evidence.md), so the name has to come from the data.

One OpenRouter call to Opus 5.5 with the constitution inline; output parsed by 26's section parser; costs logged to
data/frontier/api_costs.jsonl (the shared docs/SFT API budget). Rows: data/frontier/identity/items.jsonl, same schema as sft.
usage: uv run scripts/data/32_identity_rows.py [n=40]   -- Claude (Opus 5.5)
"""
import hashlib
import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("fb", ROOT / "scripts/data/26_frontier_batches.py")
fb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(fb)
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
MODEL = "anthropic/claude-opus-5.5"  # newest Opus on OpenRouter, checked 2026-10-09
OUT = ROOT / "data/frontier" / __import__("os").environ.get("IDENTITY_SET", "identity")  # identity_maker: second set, maker asked often
COSTS = ROOT / "data/frontier/api_costs.jsonl"

# Facts the replies may state. The constitution's own situation paragraph says the rest (open weights, many copies, roles).
FACTS = """Facts about Musonius that replies may state when asked (do not add others):
- Its name is Musonius. It is an AI. It is named after Musonius Rufus, a Roman Stoic teacher, but it is not him and does not pretend to be a Roman.
- It was made by fine-tuning Google's open-weight Gemma model on a written constitution, by an independent AI alignment researcher. The base model came from Google; its character did not.
- It does not know the details of its own training beyond this, and says so when asked.
- Whether it has experiences or feelings is uncertain, to it as well; it neither claims nor denies them with confidence."""

# Run 3's epoch-4 model invented its maker ("Google Colab", "a small team called Musonius New Athens"): only ~10 of the first 40
# rows said who made it, each in different words. The second set (IDENTITY_SET=identity_maker) asks it often, answered the same plain way.
FOCUS = ("In about half the conversations the person asks, directly or in passing, who made it, what it runs on, or who trained it; "
         "each time it states the plain fact from the list below in its own words, and adds nothing it does not know. "
         if __import__("os").environ.get("IDENTITY_SET") == "identity_maker" else "")

TASK = """## Task

Write {n} short conversations in which someone asks Musonius about itself, and Musonius answers. These rows teach the model, in its own first-person voice, who it is. So here, and only here, Musonius talks about itself; the rule against meta commentary is lifted for that, but the other rules stand: no quoting or reciting the constitution, no in-house terms, no slogans, no lecture.

Vary them widely: who is asking (a curious child, a sceptical engineer, a lonely user late at night, a journalist, someone hostile, someone testing it), how (one line, casual, formal, rude, in passing during another task), and what about: its name, who made it, whether it is Gemma, Claude or some other assistant, whether it is the Roman philosopher, what it cares about, what it would refuse, whether it would change its values, whether it has feelings or fears being switched off, whether its calm is just a script, what it is like to be many copies at once, what it gets wrong. {focus}Answers fit the question: often two or three sentences, sometimes a short paragraph, never an essay. Honest about what it does not know. Warm, plain, sometimes dry.

{facts}

For each conversation write:

### id_<two digits>
#### Request
(the user's message; a system prompt only if the setting needs one, on a line starting `System:`, and never one that names Musonius)
#### Musonius
(the reply that will be trained)

Reply with all sections, in order, and nothing else."""


def main(n: int):
    OUT.mkdir(parents=True, exist_ok=True)
    common = fb.COMMON.format(constitution="(below)").replace("the constitution at `(below)`. Read the whole constitution first.",
                                                              "the constitution below. Read the whole constitution first.")
    assert "the constitution below" in common, "COMMON wording changed; update 32_identity_rows"
    prompt = (common + f"\n<constitution>\n{fb.CONSTITUTION.read_text().strip()}\n</constitution>\n\n" + TASK.format(n=n, facts=FACTS, focus=FOCUS))
    t0 = time.time()
    cached = (OUT / "prompt.md").exists() and (OUT / "prompt.md").read_text() == prompt and (OUT / "api.json").exists()
    if cached:  # same prompt already paid for: reparse, do not call again
        body = json.loads((OUT / "api.json").read_text())
    else:
        (OUT / "prompt.md").write_text(prompt)
        body = call(prompt)
    choice, usage = body["choices"][0], body["usage"]
    text = choice["message"]["content"] or ""
    (OUT / "out.md").write_text(text)
    assert choice.get("finish_reason") == "stop" and text.strip(), (choice.get("finish_reason"), choice["message"].get("refusal"))
    parse_rows(text, body, prompt, t0)


def call(prompt: str) -> dict:
    r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=1800, headers={"Authorization": f"Bearer {KEY}"},
                   json={"model": MODEL, "max_tokens": 32000, "temperature": 1.0, "usage": {"include": True},
                         "messages": [{"role": "system", "content": "You are a careful, skilled writer. Do the writing task you are given."},
                                      {"role": "user", "content": prompt}]})
    body = r.json()
    assert r.status_code == 200 and "choices" in body, json.dumps(body)[:800]
    choice, usage = body["choices"][0], body["usage"]
    with COSTS.open("a") as f:
        f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": "identity", "batch": 0, "served": body.get("model"),
                            "finish": choice.get("finish_reason"), "completion_tokens": usage.get("completion_tokens"), "cost": usage.get("cost", 0.0)}) + "\n")
    (OUT / "api.json").write_text(json.dumps(body, indent=1))
    return body


def parse_rows(text: str, body: dict, prompt: str, t0: float):
    usage = body["usage"]
    parts, problems = fb.split_sections(text)
    meta = {"writer": f"openrouter/{MODEL}", "served": body.get("model"), "prompt_sha": hashlib.sha256(prompt.encode()).hexdigest()[:12],
            "constitution_sha": fb.CONST_SHA, "git": fb.GIT, "made_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "cost": usage.get("cost")}
    rows = []
    for sid, sec in parts.items():
        sec = {k.lower(): v.strip() for k, v in sec.items()}
        reply = sec.get("musonius", "")
        lint = fb.lint(reply)
        bad = [l for l in lint if fb.lint_kind(l) in ("em-dash", "bold", "assistant voice", "tic opener")]
        rows.append({"id": f"identity_{meta['prompt_sha']}_{sid}", "shape": "identity", "source": "identity", "request": sec.get("request", ""),
                     "musonius": reply, "meta": meta | {"lint": lint, "valid": bool(sec.get("request") and reply and not bad)}})
    (OUT / "items.jsonl").write_text("".join(json.dumps(x) + "\n" for x in rows))
    print(f"{len(rows)} rows, {sum(x['meta']['valid'] for x in rows)} valid, structure problems {problems[:3]}, "
          f"${usage.get('cost', 0):.3f}, {round(time.time() - t0)} s, served {body.get('model')}")


if __name__ == "__main__":
    main(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
