# Does DeepSeek v4.1 flash (DeepSeek provider) accept a hidden-reasoning prefix the way Kimi did? Two uses:
#   cut50: reasoning cut mid-sentence at 50%; does the new reasoning finish the sentence without restarting?
#   full:  the whole reasoning as prefix; does it write only a fresh answer (cheap answer-only resample)?
# Tried on 3 small-batch pairs, both field names. Cached via model_requests.  -- PI/Claude (opus-5-5), 2026-10-27
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.generate import params

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/scratch/20261027_deepseek_fork"
SEEDS = ["stoic_8c4a472c0d69", "other_books_e90d634c82b9", "tiny_virtues_6f1d1453dc90"]
FIELDS = ["reasoning", "reasoning_content"]


def words(t):
    return re.findall(r"\w+", t.lower())


def ngram_overlap(a, b, n=6):
    ga = {tuple(w) for w in zip(*[words(a)[i:] for i in range(n)])}
    gb = [tuple(w) for w in zip(*[words(b)[i:] for i in range(n)])]
    return round(sum(g in ga for g in gb) / max(1, len(gb)), 2)


def cut_mid_sentence(text, frac):
    i = int(len(text) * frac)
    start = max(text.rfind(c, 0, i) for c in ".?!\n") + 1
    ws = [m.end() for m in re.finditer(r"\w+", text[start:])]
    return text[: start + ws[min(3, len(ws) - 1)]]


def main():
    cfg = yaml.safe_load((ROOT / "configs/data/v2.yaml").read_text())
    constitution = (Path(cfg["source_root"]) / cfg["constitution"]).read_text()
    rows = {r["seed_id"]: r for r in map(json.loads, open(ROOT / "data/04_generate/v2/small/rows.jsonl"))}
    jobs = []
    for s in SEEDS:
        r = rows[s]
        role = "\n\n".join(m["content"] for m in r["messages"] if m["role"] == "system")
        base = [{"role": "system", "content": constitution + ("\n\n" + role if role else "")}] + [m for m in r["messages"] if m["role"] != "system"]
        for mode, prefix in [("cut50", cut_mid_sentence(r["reasoning"], 0.5)), ("full", r["reasoning"])]:
            for f in FIELDS:
                jobs.append((s, mode, f, base, prefix))

    def run(job):
        s, mode, f, base, prefix = job
        msgs = base + [{"role": "assistant", "content": "", f: prefix, "partial": True}]
        try:
            rec = send_cached_request(OUT / "api", request_messages(cfg["teacher"]["model"], msgs, params(cfg["teacher"])), context={"fork": s + mode + f})
        except Exception as e:
            return {"seed": s, "mode": mode, "field": f, "error": f"{type(e).__name__}: {str(e)[:300]}"}
        m = rec["response"]["choices"][0]["message"]; new = m.get("reasoning") or ""
        return {"seed": s, "mode": mode, "field": f, "error": None, "prefix_tail": prefix[-120:], "new_head": new[:300],
                "new_words": len(new.split()), "prefix_words": len(prefix.split()), "repeat": ngram_overlap(prefix, new),
                "answer_head": (m.get("content") or "")[:160], "cost": rec["response"]["usage"]["cost"]}

    with ThreadPoolExecutor(6) as ex:
        res = list(ex.map(run, jobs))
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "results.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
    for r in res:
        print(f"\n## {r['seed']} {r['mode']} {r['field']}" + (f" ERROR {r['error']}" if r["error"] else
              f"  ${r['cost']:.4f} prefix {r['prefix_words']}w new {r['new_words']}w repeat {r['repeat']}"))
        if not r["error"]:
            print("  prefix ends: ..." + r["prefix_tail"].replace("\n", " | "))
            print("  new starts : " + r["new_head"][:200].replace("\n", " | "))
            print("  answer     : " + r["answer_head"].replace("\n", " | "))


if __name__ == "__main__":
    main()
