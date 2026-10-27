# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "openai"]
# ///
"""Does the Echo restyle in our SFT data (data/frontier/sft_stoic_modern, persona Musonius) change acts or reasons? Seeded sample,
same GLM act/reason judge as scripts/data/scratch/53_echo_docs_v2.py, original = musonius_opus, rewrite = musonius. -- PI/Claude (Opus 5.5)
usage: uv run scripts/scratch/echo_sft_meaning_check.py N SEED OUT.jsonl"""
import importlib.util, json, random, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("e53", ROOT / "scripts/data/scratch/53_echo_docs_v2.py"); e53 = importlib.util.module_from_spec(spec); spec.loader.exec_module(e53)
n, seed, out = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
rows = random.Random(seed).sample([json.loads(l) for l in open(ROOT / "data/frontier/sft_stoic_modern/items.jsonl")], n)
def one(r):
    v = e53.judge(f"User request:\n{r['request']}\n\nReply:\n{r['musonius_opus']}", f"User request:\n{r['request']}\n\nReply:\n{r['musonius']}")
    return {"id": r["id"], "shape": r["shape"], "overlap": r["meta"]["restyle"]["checks"].get("overlap"), "length_ratio": r["meta"]["restyle"]["checks"].get("length_ratio"), **v}
with ThreadPoolExecutor(8) as ex: res = list(ex.map(one, rows))
Path(out).write_text("".join(json.dumps(x) + "\n" for x in res))
print(f"{len(res)} rows: kept {sum(x['verdict']=='kept' for x in res)}; acts_same {sum(bool(x['acts_same']) for x in res)}; reasons_same {sum(bool(x['reasons_same']) for x in res)}; facts_added in {sum(bool(x['facts_added']) for x in res)}; cost ${sum(x['cost'] or 0 for x in res):.3f}")
