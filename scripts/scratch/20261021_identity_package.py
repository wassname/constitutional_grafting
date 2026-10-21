# /// script
# requires-python = ">=3.11"
# dependencies = ["transformers>=4.57", "jinja2", "loguru"]
# ///
"""Render the identity_v2 pilot rows (after repairs) in the exact Qwen SFT format for the review package. -- PI/Claude"""
import importlib.util, json, os
from pathlib import Path
os.environ["CHAT_MODEL"] = "qwen"
ROOT = Path(__file__).resolve().parents[2]
s = importlib.util.spec_from_file_location("p", ROOT / "scripts/train/01_prepare.py"); p = importlib.util.module_from_spec(s); s.loader.exec_module(p)
from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained(p.TOK_ID)
D = ROOT / "data/frontier/identity_v2"
reps = {r["id"]: r for r in map(json.loads, (D / "repairs.jsonl").open())}
out = ["# Identity v2 pilot: all 80 rows exactly as the trainer would see them\n\nNOT TRAINED = prompt segment; TRAINED = reply segment. Repairs from data/frontier/identity_v2/repairs.jsonl applied.\n"]
for b in sorted(D.glob("batch_*/items.jsonl")):
    for r in map(json.loads, b.open()):
        reply = r["musonius"]
        if r["id"] in reps: reply = reply.replace(reps[r["id"]]["old"], reps[r["id"]]["new"])
        prompt = tok.apply_chat_template(p.messages(r["request"]), tokenize=False, add_generation_prompt=True, **p.TEMPLATE_KW)
        out.append(f"\n## {r['id']}  (spec: {r['spec']})\n\nNOT TRAINED:\n```\n{prompt}\n```\n\nTRAINED:\n```\n{reply.strip()}{p.EOT}\n```\n")
(ROOT / "slop/reviews/20261021_identity_v2_package/rows.md").write_text("".join(out)); print(len(out) - 1, "rows")
