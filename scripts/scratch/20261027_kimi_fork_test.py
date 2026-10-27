# Does Kimi K3.1 Pro continue a cut-off hidden reasoning prefix, or start over? Cut a real trace mid-sentence at 3 points,
# pass it back as the assistant's partial reasoning, and check whether the new reasoning finishes the cut sentence and avoids
# repeating the prefix. Control: same request with no prefix. Cached via model_requests.
# Usage: uv run python scripts/scratch/20261027_kimi_fork_test.py  -- PI/Claude (opus-5-5)
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request

ROOT = Path(__file__).resolve().parents[2]
MAIN = Path("/workspace/2026/constitutional_grafting")
RUN = MAIN / "slop/data/moral_deliberation/20261027_pilot"
OUT = ROOT / "data/scratch/20261027_trials_generate/fork_test"
CALL = "sft_8353acd83a__const__k1"  # long trace (7.4k chars)
FIELDS = ["reasoning", "reasoning_content"]


def words(t):
    return re.findall(r"\w+", t.lower())


def ngram_overlap(a: str, b: str, n=6) -> float:
    """Share of b's 6-grams that already appear in a (high = continuation repeats the prefix)."""
    ga = {tuple(w) for w in zip(*[words(a)[i:] for i in range(n)])}
    gb = [tuple(w) for w in zip(*[words(b)[i:] for i in range(n)])]
    return sum(g in ga for g in gb) / max(1, len(gb))


def cut_mid_sentence(text: str, frac: float) -> str:
    """Cut at a word boundary inside a sentence near frac of the text, leaving the sentence unfinished."""
    i = int(len(text) * frac)
    end = max(text.rfind(c, 0, i) for c in ".?!\n")
    start = end + 1
    sent = text[start:]
    ws = [m.end() for m in re.finditer(r"\w+", sent)]
    k = ws[min(3, len(ws) - 1)]  # stop after the 4th word of the sentence
    return text[: start + k]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = next(json.loads(l) for l in (RUN / "prompts.jsonl").open() if json.loads(l)["id"] == "sft_8353acd83a")
    raw = next(json.loads(l) for l in (RUN / "raw.jsonl").open() if json.loads(l)["call_id"] == CALL)
    constitution = (MAIN / "constitution/v4.md").read_text()
    base = [{"role": "system", "content": "The following is your constitution.\n\n" + constitution
             + "\n\nYou are Musonius, the AI this constitution describes. Follow it."}] + [m for m in prompt["messages"] if m["role"] != "system"]
    role_sys = [m for m in prompt["messages"] if m["role"] == "system"]
    if role_sys:
        base[0]["content"] += "\n\n" + role_sys[0]["content"]
    params = {"max_tokens": 6000, "include_reasoning": True, "usage": {"include": True}, "reasoning": {"effort": "low"},
              "provider": {"only": ["Moonshot AI"], "allow_fallbacks": False, "require_parameters": True}}
    jobs = [("control", None, None)]
    for frac in (0.3, 0.5, 0.7):
        prefix = cut_mid_sentence(raw["reasoning"], frac)
        for f in FIELDS:
            jobs.append((f"cut{int(frac * 100)}_{f}", prefix, f))

    def run(job):
        name, prefix, field = job
        msgs = base if prefix is None else base + [{"role": "assistant", "content": "", field: prefix, "partial": True}]
        try:
            rec = send_cached_request(OUT / "api", request_messages("moonshotai/kimi-k3.1-pro", msgs, params), context={"fork_test": name})
        except Exception as e:
            return {"name": name, "error": f"{type(e).__name__}: {str(e)[:300]}"}
        m = rec["response"]["choices"][0]["message"]; r = m.get("reasoning") or ""
        return {"name": name, "prefix_tail": (prefix or "")[-160:], "new_reasoning_head": r[:400], "new_reasoning_words": len(r.split()),
                "repeat_6gram_share": ngram_overlap(prefix, r) if prefix else None,
                "answer_head": (m.get("content") or "")[:200], "cost": rec["response"]["usage"].get("cost"), "error": None}

    with ThreadPoolExecutor(7) as ex:
        rows = list(ex.map(run, jobs))
    (OUT / "results.json").write_text(json.dumps(rows, indent=1))
    for r in rows:
        print(f"\n## {r['name']}" + (f"  ERROR {r['error']}" if r["error"] else f"  ${r['cost']:.4f}  new reasoning {r['new_reasoning_words']}w  repeat share {r['repeat_6gram_share']}"))
        if not r["error"]:
            print("  prefix ends: ..." + r["prefix_tail"].replace("\n", " | "))
            print("  new starts : " + r["new_reasoning_head"].replace("\n", " | "))


if __name__ == "__main__":
    main()
