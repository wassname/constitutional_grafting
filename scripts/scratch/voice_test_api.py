# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx"]
# ///
"""Voice test condition through the OpenRouter API (project key), constitution inline. For models pi cannot reach on its own key.
usage: uv run scripts/scratch/voice_test_api.py <cond> <openrouter model id>   -- Claude (Opus 5.5)"""
import importlib.util, json, sys
from pathlib import Path
import httpx
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("aw", ROOT / "scripts/data/28_api_writer.py"); aw = importlib.util.module_from_spec(spec); spec.loader.exec_module(aw)
cond, model = sys.argv[1], sys.argv[2]
D = ROOT / "data/frontier/voice_test"
out = D / f"out_{cond}.md"
r = httpx.post("https://openrouter.ai/api/v1/chat/completions", timeout=1800, headers={"Authorization": f"Bearer {aw.KEY}"},
               json={"model": model, "max_tokens": 48000, "usage": {"include": True},
                     "messages": [{"role": "system", "content": aw.SYSTEM}, {"role": "user", "content": aw.brief_for_api((D / f"brief_{cond}.md").read_text(), str(out))}]})
body = r.json()
c = body["choices"][0]
out.write_text(c["message"]["content"].strip() + "\n")
print(cond, "served", body.get("model"), body.get("provider"), "finish", c.get("finish_reason"), "cost", body["usage"]["cost"])
