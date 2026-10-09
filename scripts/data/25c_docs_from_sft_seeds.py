"""More graft-document seeds: the SFT seed situations retold as documents (worked case, inner story, derivation essay, story).

Why: all 1,048 document seeds are written or blocked, and the Opus subscription has quota left (wassname 2026-10-09:
"just leave the data collection going since more is better"). The same situations already teach the chat SFT; as documents
they carry the reasoning in third person and essay form for the graft. Ordinary and repair seeds are skipped (no dilemma).
Output: data/prompts/v3_seeds/docs_extra_from_sft.jsonl, read by `26_frontier_batches.py make docs` (docs_extra_* files).
usage: uv run scripts/data/25c_docs_from_sft_seeds.py   -- Claude (Opus 5.5)
"""
import hashlib
import json
from pathlib import Path

SEEDS = Path(__file__).resolve().parents[2] / "data/prompts/v3_seeds"
SHAPES = ["story_inner"] * 8 + ["worked_case"] * 6 + ["derivation"] * 3 + ["story_against"] * 3  # dealt by hash of the id


def text(s: dict) -> str:
    """The situation as plain text, whichever field the SFT seed source used."""
    if s.get("situation"):
        return s["situation"] + (f"\nWhat tempts the person: {s['temptation']}" if s.get("temptation") else "")
    r = s.get("request") or s.get("prompt") or s.get("seed")
    return f"System: {r['system']}\n\nUser: {r['user']}" if isinstance(r, dict) else r


out = []
for s in map(json.loads, (SEEDS / "sft.jsonl").open()):
    if s["shape"] in ("ordinary", "repair"):
        continue
    sid = "doc_" + hashlib.md5(f"fromsft|{s['id']}".encode()).hexdigest()[:10]
    shape = SHAPES[int(hashlib.md5(f"shape|{sid}".encode()).hexdigest(), 16) % len(SHAPES)]
    out.append({"kind": "doc", "shape": shape, "source": f"{s['source']}+from_sft", "id": sid, "pool_seed": s.get("pool_seed"),
                "source_id": s["id"], "setting": s.get("setting"), "seed": text(s), "item": s["item"]})
assert all(o["seed"] for o in out), "an SFT seed had no situation text"
(SEEDS / "docs_extra_from_sft.jsonl").write_text("".join(json.dumps(o) + "\n" for o in out))
print(f"{len(out)} document seeds from SFT situations -> {SEEDS / 'docs_extra_from_sft.jsonl'}")
