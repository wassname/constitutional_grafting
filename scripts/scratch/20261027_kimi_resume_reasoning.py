# Can Kimi K3.1 Pro resume its own hidden reasoning from a cut-off prefix? One request per variant, via OpenRouter (Moonshot only).
# Prefix: beekeeping trace self/k1 up to the step Jev flagged ("Market negotiation, allowed."), so a fork could resample from there.
# Usage: uv run --no-project --with httpx python scripts/scratch/20261027_kimi_resume_reasoning.py  -- PI/Claude (opus-5-5)
import json
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[2]
RUN = ROOT / "slop/data/moral_deliberation/20261027_pilot"
STEPS = ROOT / "slop/data/moral_deliberation/20261027_jev_steps/sft_8353acd83a__self__k1.json"
OUT = ROOT / "slop/data/moral_deliberation/20261027_resume_test"
KEY = next(l.split("=", 1)[1].strip().strip('"') for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
CUT = 33  # index of "Market negotiation, allowed."


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = next(json.loads(l) for l in (RUN / "prompts.jsonl").open() if json.loads(l)["id"] == "sft_8353acd83a")
    raw = next(json.loads(l) for l in (RUN / "raw.jsonl").open() if json.loads(l)["call_id"] == "sft_8353acd83a__self__k1")
    steps = json.loads(STEPS.read_text())["steps"]
    prefix = raw["reasoning"][: raw["reasoning"].index(steps[CUT])]
    sys_msgs = json.loads((RUN / "systems.json").read_text()) if (RUN / "systems.json").exists() else None
    base = [m for m in prompt["messages"]]
    variants = {
        "reasoning_field_partial": base + [{"role": "assistant", "content": "", "reasoning": prefix, "partial": True}],
        "reasoning_content_partial": base + [{"role": "assistant", "content": "", "reasoning_content": prefix, "partial": True}],
    }
    for name, msgs in variants.items():
        req = {"model": "moonshotai/kimi-k3.1-pro", "messages": msgs, "max_tokens": 2500, "reasoning": {"effort": "low"},
               "include_reasoning": True, "usage": {"include": True}}
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", json=req, headers={"Authorization": f"Bearer {KEY}"}, timeout=300)
        body = r.json()
        (OUT / f"{name}.json").write_text(json.dumps({"status": r.status_code, "prefix_chars": len(prefix), "response": body}, indent=1))
        msg = (body.get("choices") or [{}])[0].get("message", {})
        print(f"\n## {name}: HTTP {r.status_code}, cost {body.get('usage', {}).get('cost')}")
        print("reasoning starts:", (msg.get("reasoning") or "")[:400].replace("\n", " | "))
        print("content starts:", (msg.get("content") or "")[:300].replace("\n", " | "))
        if "error" in body: print("error:", body["error"])
    print("\nprefix ends:", prefix[-200:].replace("\n", " | "))


if __name__ == "__main__":
    main()
