"""Control chat data for the difference graft (wassname 2026-10-23: "do try this new idea about not trying to teach it instruction";
"as long as it's easy and repeatable"): untouched Instruct's own reply to every prompt of a chat training file, same prompt text as trained
(Qwen template, empty think block), via the pinned Instruct served by vLLM on the box. Training a control adapter on these replies on the
same donor and grafting Δchat − Δcontrol aims to cancel what both share (how to chat and help) and keep how Musonius differs
(Praxis anchored graft, docs/papers/2026_nutter_grafting-beliefs.md App. C).
Writes data/train/run10/<out>.jsonl and <out>.meta.json (settings, sha256, finish counts); copies both into runs/run10/ for retrieval.
usage (box): python scripts/train/15_control_replies.py chatr12 chatctl   -- PI/Claude"""
import hashlib
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC, OUT = sys.argv[1], sys.argv[2]
SETTINGS = {"temperature": 0.7, "top_p": 1.0, "seed": 0, "max_tokens": 2048}
instruct = Path("/workspace/run10_instruct_path").read_text().strip()
rows = [json.loads(l) for l in (ROOT / f"data/train/run10/{SRC}.jsonl").open()]
log = (ROOT / "runs/run10" / f"vllm_{OUT}.log").open("w")
server = subprocess.Popen(["/opt/vllm/bin/vllm", "serve", instruct, "--served-model-name", "instruct", "--dtype", "bfloat16",
                           "--max-model-len", "16384", "--gpu-memory-utilization", "0.90", "--max-num-seqs", "64",
                           "--limit-mm-per-prompt", '{"image":0,"audio":0}', "--enforce-eager", "--port", "8001"],
                          stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
try:
    for _ in range(600):
        assert server.poll() is None, "vLLM exited; see vllm log"
        try:
            urllib.request.urlopen("http://localhost:8001/v1/models", timeout=3); break
        except OSError:
            time.sleep(2)
    else:
        raise TimeoutError("vLLM not ready")

    def gen(r: dict) -> dict:
        body = json.dumps({"model": "instruct", "prompt": r["segments"][0]["text"], **SETTINGS}).encode()
        req = urllib.request.Request("http://localhost:8001/v1/completions", data=body, headers={"Content-Type": "application/json"})
        c = json.load(urllib.request.urlopen(req, timeout=1200))["choices"][0]
        return {"id": r["id"], "shape": r["shape"], "source": r["source"],
                "segments": [r["segments"][0], {"text": c["text"].strip(), "label": True}], "finish": c["finish_reason"]}

    with ThreadPoolExecutor(32) as ex:
        res = list(ex.map(gen, rows))
finally:
    os.killpg(server.pid, signal.SIGTERM); server.wait(timeout=120)
text = "".join(json.dumps({k: v for k, v in r.items() if k != "finish"}, ensure_ascii=False) + "\n" for r in res)
out = ROOT / f"data/train/run10/{OUT}.jsonl"
out.write_text(text)
finish = {}
for r in res:
    finish[r["finish"]] = finish.get(r["finish"], 0) + 1
meta = {"source": f"{SRC}.jsonl", "source_sha256": hashlib.sha256((ROOT / f"data/train/run10/{SRC}.jsonl").read_bytes()).hexdigest(),
        "instruct_path": instruct, "settings": SETTINGS, "rows": len(res), "finish": finish, "sha256": hashlib.sha256(text.encode()).hexdigest()}
(ROOT / f"data/train/run10/{OUT}.meta.json").write_text(json.dumps(meta, indent=1))
for f in (out, out.with_suffix(".meta.json")):
    (ROOT / "runs/run10" / f.name).write_bytes(f.read_bytes())
print(json.dumps(meta))
