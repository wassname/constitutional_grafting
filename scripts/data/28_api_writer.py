# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""API lane for frontier batches: same briefs as the pi lanes, sent to OpenRouter with the constitution inline and no tools.
Paced by 26_frontier_batches.py next (account "openrouter"); records served model, tokens and cost per batch; stops at a
spend cap. The project key in .env is used (weekly limit on the key; wassname 2026-10-09: "can spend $40").
usage: uv run scripts/data/28_api_writer.py <sft|docs> <max batches> [cap_usd=40]   -- Claude (Opus 5.5)"""
import importlib.util
import json
import random
import subprocess
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
SYSTEM = "You are a careful, skilled writer. Do the writing task you are given."
COSTS = ROOT / "data/frontier/api_costs.jsonl"


def spent() -> float:
    return sum(json.loads(l)["cost"] for l in COSTS.open()) if COSTS.exists() else 0.0


def brief_for_api(text: str, out_path: str) -> str:
    """The pi brief tells the writer to read the constitution and write a file; here both are inline."""
    constitution = fb.CONSTITUTION.read_text()
    text = text.replace(f"the constitution at `{fb.CONSTITUTION}`. Read the whole constitution first.",
                        f"the constitution below. Read the whole constitution first.\n\n<constitution>\n{constitution}\n</constitution>\n")
    text = text.replace(f"Write all sections, in order, to `{out_path}` with the write tool. Do not edit other files.",
                        "Reply with all sections, in order, and nothing else: no preamble and no closing summary.")
    assert "<constitution>" in text and "write tool" not in text, "brief template changed; update brief_for_api"
    return text


def run(kind: str, n: int, cap: float):
    py = ["uv", "run", "-q", str(ROOT / "scripts/data/26_frontier_batches.py")]
    for _ in range(n):
        if spent() >= cap:
            print(f"cap reached: ${spent():.2f} >= ${cap}")
            return
        nxt = subprocess.run(py + ["next", kind, "openrouter"], capture_output=True, text=True, check=True).stdout.strip()
        if nxt.startswith(("DONE", "WAIT")):
            print(nxt)
            return
        b = json.loads(nxt)
        time.sleep(b["wait_s"])
        subprocess.run(py + ["mark", kind, str(b["batch"]), "running"], check=True)
        out_path = str(ROOT / "data/frontier" / kind / f"out_{b['batch']:03d}.md")
        model = b["writer"].split("/", 1)[1]
        t0 = time.time()
        r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=1800,
                       headers={"Authorization": f"Bearer {KEY}"},
                       json={"model": model, "max_tokens": 64000, "temperature": 1.0, "usage": {"include": True},
                             "messages": [{"role": "system", "content": SYSTEM},
                                          {"role": "user", "content": brief_for_api(Path(b["file"]).read_text(), out_path)}]})
        body = r.json()
        if r.status_code != 200 or "choices" not in body:
            err = json.dumps(body)[:500]
            print(f"batch {b['batch']} API error {r.status_code}: {err}")
            if "moderation" in err.lower() or "usage policy" in err.lower() or r.status_code == 403:
                subprocess.run(py + ["split", kind, str(b["batch"])], check=True)
                continue
            subprocess.run(py + ["mark", kind, str(b["batch"]), "failed"], check=True)
            return
        choice, usage = body["choices"][0], body.get("usage", {})
        with COSTS.open("a") as f:  # every paid call, including refusals
            f.write(json.dumps({"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": kind, "batch": b["batch"], "served": body.get("model"),
                                "finish": choice.get("finish_reason"), "completion_tokens": usage.get("completion_tokens"), "cost": usage.get("cost", 0.0)}) + "\n")
        (ROOT / "data/frontier" / kind / f"api_{b['batch']:03d}.json").write_text(json.dumps({k: v for k, v in body.items() if k != "choices"} | {"finish": choice.get("finish_reason"), "native_finish": choice.get("native_finish_reason"), "refusal": choice["message"].get("refusal")}, indent=1))
        if not choice["message"].get("content"):  # refusal or content filter: same handling as a pi-lane block
            print(f"batch {b['batch']}: no content (finish {choice.get('finish_reason')}, native {choice.get('native_finish_reason')}, refusal {str(choice['message'].get('refusal'))[:200]}); splitting")
            subprocess.run(py + ["split", kind, str(b["batch"])], check=True)
            continue
        Path(out_path).write_text(choice["message"]["content"].strip() + "\n")
        rec = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "kind": kind, "batch": b["batch"], "requested": model,
               "served": body.get("model"), "provider": body.get("provider"), "finish": choice.get("finish_reason"),
               "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"),
               "cost": usage.get("cost", 0.0), "seconds": round(time.time() - t0)}
        status = "done" if choice.get("finish_reason") == "stop" else "failed"  # "length" = truncated output
        subprocess.run(py + ["mark", kind, str(b["batch"]), status], check=True)
        print(f"batch {b['batch']}: {status}, {rec['completion_tokens']} out tokens, ${rec['cost']:.3f}, served {rec['served']}, total ${spent():.2f}")
        time.sleep(random.uniform(fb.GAP_MIN_S, fb.GAP_MAX_S))


if __name__ == "__main__":
    run(sys.argv[1], int(sys.argv[2]), float(sys.argv[3]) if len(sys.argv) > 3 else 40.0)
