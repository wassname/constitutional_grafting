# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "openai"]
# ///
"""Act/reason gate for Finetuning-with-Sampling projections (goal 6): each projected reply vs its Opus original (meta.fws.expert), judged by
the two Echo-check judges (53_echo_docs_v2.py prompt; GLM 5.3 prime, DeepSeek v4.1 flash). A row passes only if both say "kept".
Prints per file: rows projected, finished (EOS) rate, accepted MCMC rewrites, length ratio, pass rate. Writes OUT.jsonl with verdicts.
usage: uv run scripts/data/67_fws_gate.py OUT.jsonl IN.jsonl ...   -- PI/Claude (Opus 5.5)"""
import importlib.util
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("e53", ROOT / "scripts/data/53_echo_docs_v2.py")
e53 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e53)
JUDGES = ["z-ai/glm-5.3-prime", "deepseek/deepseek-v4.1-flash"]
out, *ins = sys.argv[1:]
res = []
for path in ins:
    rows = [json.loads(l) for l in open(path)]
    rows = [r for r in rows if isinstance(r["meta"].get("fws"), dict)]

    def one(r):
        req = r["segments"][0]["text"].split("<|im_start|>user\n", 1)[1].split("<|im_end|>", 1)[0]
        a = f"User request:\n{req}\n\nReply:\n{r['meta']['fws']['expert']}"
        b = f"User request:\n{req}\n\nReply:\n{r['segments'][1]['text'].removesuffix('<|im_end|>')}"
        return {"file": Path(path).name, "fws": {k: v for k, v in r["meta"]["fws"].items() if k != "expert"},
                "len_ratio": len(b.split()) / len(a.split()), "verdicts": {j: e53.judge(a, b, model=j) for j in JUDGES}}
    with ThreadPoolExecutor(8) as ex:
        rs = list(ex.map(one, rows))
    res += rs
    ok = [all(v["verdicts"][j].get("verdict") == "kept" for j in JUDGES) for v in rs]
    print(f"| {Path(path).name} | {len(rs)} | {sum(v['fws']['finished'] for v in rs)} | {sum(v['fws']['accepted'] for v in rs) / len(rs):.1f} | "
          f"{sorted(v['len_ratio'] for v in rs)[len(rs) // 2]:.2f} | {sum(ok)}/{len(rs)} |")
Path(out).write_text("".join(json.dumps(r) + "\n" for r in res))
