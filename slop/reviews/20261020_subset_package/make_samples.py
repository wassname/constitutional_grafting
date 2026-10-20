"""Write samples.md for the subset review package: 4 seeded echo and stoic rows, all opus/greek pilot rows with seed and user prompt.
usage: uv run --no-project slop/reviews/20261020_subset_package/make_samples.py   -- PI/Claude (Opus 5.5)"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "data/subsets"
jl = lambda p: [json.loads(l) for l in open(p)]
USER = None
for line in (ROOT / "scripts/data/50_docs_v2.py").read_text().split('USER = """', 1)[1:]:
    USER = line.split('"""', 1)[0]
out = ["# Subset samples (exact training text)\n\nPI/Claude. Seeded selection: random.Random(20261020).sample for echo and stoic; all pilot rows for opus and greek.\n"]
rng = random.Random(20261020)
for name in ["echo", "stoic"]:
    for r in rng.sample(jl(D / f"{name}.jsonl"), 4):
        out.append(f"## {r['id']} ({name}; source {r.get('source')}, {r.get('shape', '')})\n\n" + (f"Original seed: {r['seed'][:600]}\n\n" if r.get("seed") else "") + f"Training text:\n\n~~~~text\n{r['text']}\n~~~~\n")
for name in ["opus_pilot_raw", "greek_pilot"]:
    for r in jl(D / f"{name}.jsonl"):
        prompt = USER.format(**r) + ("\n\nWrite the whole document in Modern Greek." if "greek" in name else "")
        m = r["meta"]
        out.append(f"## {r['id']} ({name}; writer {m.get('served_model')}" + (f", translator {m.get('translator_served')}" if "greek" in name else "") +
                   f")\n\nGeneration user prompt (system = 50_docs_v2 SYSTEM + added rules + constitution v4):\n\n~~~~text\n{prompt}\n~~~~\n\nTraining text:\n\n~~~~text\n{r['text']}\n~~~~\n")
(Path(__file__).parent / "samples.md").write_text("\n".join(out))
print(len(out) - 1, "samples")
