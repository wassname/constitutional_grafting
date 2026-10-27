# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Re-send a refused docs batch to Opus via OpenRouter with reasoning returned, to see why it refused. Diagnosis only.
usage: uv run scripts/scratch/refusal_diag.py <kind> <batch>   -- Claude (Opus 5.5)"""
import importlib.util, json, sys
from pathlib import Path
import httpx
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("aw", ROOT / "scripts/data/scratch/28_api_writer.py"); aw = importlib.util.module_from_spec(spec); spec.loader.exec_module(aw)
kind, n = sys.argv[1], int(sys.argv[2])
out = str(ROOT / "data/frontier" / kind / f"out_{n:03d}.md")
r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=1800, headers={"Authorization": f"Bearer {aw.KEY}"},
               json={"model": "anthropic/claude-opus-5.5", "max_tokens": 64000, "usage": {"include": True}, "reasoning": {"max_tokens": 8000},
                     "messages": [{"role": "system", "content": aw.SYSTEM}, {"role": "user", "content": aw.brief_for_api((ROOT / f"data/frontier/{kind}/batch_{n:03d}.md").read_text(), out)}]})
body = r.json()
(ROOT / f"data/frontier/{kind}/diag_{n:03d}.json").write_text(json.dumps(body, indent=1))
c = body["choices"][0]
print("finish", c.get("finish_reason"), c.get("native_finish_reason"), "cost", body["usage"]["cost"])
print("REASONING:\n", (c["message"].get("reasoning") or "")[:6000])
print("CONTENT head:\n", (c["message"].get("content") or "")[:500])
