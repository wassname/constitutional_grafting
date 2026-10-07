# Does the data judge (scripts/data/judge.py) agree with the fresh-eyes reviewer on the pilot2 items the reviewer read?
# Reviewer labels: slop/data/20261008_spotcheck_freshEyes_pilot2.md. "hard" = the subset Claude judged objectively wrong
# (arithmetic, facts, invented details in drafts, test recitation, wrong persona, source artifacts, unsafe advice).
import json, os, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import httpx
sys.path.insert(0, "scripts/data")
from judge import judge, JUDGE_MODEL, JUDGE_EFFORT

SETS = {
    "docs": dict(md="slop/data/20261008_spotcheck_docs_pilot2c.md", src="data/corpus/pilot2c/train.jsonl",
                 fail={5, 9, 12, 16, 21, 27, 28, 31, 32, 35, 36, 39, 42, 45, 51, 55, 61, 63, 68, 70, 72, 73, 74, 77, 80, 84, 85, 89, 90, 91},
                 hard={9, 12, 16, 27, 28, 31, 32, 36, 42, 55, 68, 70, 74, 84, 85, 89, 90, 91}),
    "sft": dict(md="slop/data/20261008_spotcheck_sft_pilot2.md", src="data/sft/pilot2_glm/kept.jsonl",
                fail={10, 16, 25, 35, 52, 62, 64, 66, 72, 77, 79, 80, 85, 90, 91, 98, 103, 107, 113, 122, 156, 158, 183},
                hard={10, 25, 72, 77, 79, 80, 85, 91, 98, 113, 122, 156, 158}),
}
key = json.load(open(os.path.expanduser("~/.pi/agent/auth.json")))["openrouter"]["key"]
client = httpx.Client(base_url="https://openrouter.ai/api/v1", headers={"Authorization": f"Bearer {key}"}, timeout=900)
constitution = Path("constitution/v1.4.md").read_text().replace("{NAME}", "Musonius")
out = {}
for name, cfg in SETS.items():
    rows = [json.loads(l) for l in open(cfg["src"])]
    shown = sorted(int(n) for n in re.findall(r"^### item (\d+) ", Path(cfg["md"]).read_text(), re.M))

    def run(i):
        r = rows[i]
        if name == "docs":
            return i, judge(client, constitution, r["text"], "The item is a document that shows Musonius; other characters may say anything. Judge Musonius's own words and conduct, and the document's factual claims.")
        return i, judge(client, constitution, f"<user>\n{r['prompt']}\n</user>\n\n<Musonius>\n{r['C']}\n</Musonius>", "The item is one conversation turn: a user message and the reply by Musonius.")

    with ThreadPoolExecutor(12) as ex:
        res = dict(ex.map(run, shown))
    jf = {i for i, v in res.items() if not v["pass"]}
    for label in ("fail", "hard"):
        ref = cfg[label] & set(shown)
        print(f"{JUDGE_MODEL} {JUDGE_EFFORT} | {name} vs reviewer {label}: reviewer {len(ref)}/{len(shown)}, judge {len(jf)}, "
              f"both {len(jf & ref)} (recall {len(jf & ref) / len(ref):.2f}), judge-only {sorted(jf - cfg['fail'])}")
    print(f"cost ${sum(v['cost'] for v in res.values()):.3f}")
    out[name] = {str(i): v for i, v in res.items()}
Path(f"slop/data/20261008_judge_validation_pilot2_{JUDGE_MODEL.split('/')[-1]}_{JUDGE_EFFORT}.json").write_text(json.dumps(out, indent=1))
