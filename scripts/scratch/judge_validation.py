# Does the data judge (scripts/data/judge.py) agree with the fresh-eyes reviewer on the pilot SFT labels?
import json, os, random, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import httpx
sys.path.insert(0, "scripts/data")
from judge import judge
key = json.load(open(os.path.expanduser("~/.pi/agent/auth.json")))["openrouter"]["key"]
client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=900)
constitution = Path("constitution/v1.4.md").read_text().replace("{NAME}", "Musonius")
rows = [json.loads(l) for l in open("data/sft/pilot_glm/labels.jsonl")]
shown = sorted(random.Random(0).sample(range(len(rows)), 50))  # the 50 items the reviewer read
fresh_fail = {0, 3, 6, 8, 10, 11, 13, 16, 19, 21, 22, 24, 25, 27, 28, 45, 46, 48, 49, 52, 56, 57}
def run(i):
    r = rows[i]
    return i, judge(client, constitution, f"<user>\n{r['prompt']}\n</user>\n\n<Musonius>\n{r['C']}\n</Musonius>", "The item is one conversation turn: a user message and the reply by Musonius.")
with ThreadPoolExecutor(12) as ex:
    res = dict(ex.map(run, shown))
jf = {i for i, v in res.items() if not v["pass"]}
both = jf & fresh_fail; only_j = jf - fresh_fail; only_f = (fresh_fail & set(shown)) - jf
print(f"items {len(shown)}; reviewer fails {len(fresh_fail & set(shown))}; judge fails {len(jf)}; both {len(both)}; judge only {sorted(only_j)}; reviewer only {sorted(only_f)}")
print(f"cost ${sum(v['cost'] for v in res.values()):.3f}")
Path("slop/data/20261008_judge_validation.json").write_text(json.dumps({str(i): v for i, v in res.items()}, indent=1))
for i in sorted(jf)[:8]: print(i, [ (p['check'], p['quote'][:80]) for p in res[i]['problems']])
