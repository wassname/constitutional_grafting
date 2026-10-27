"""Long single-turn completions from a running vLLM server on generic prompts, with loop checks.
Two uses: the loop-rate sweep over graft doses (loop_probe_prompts.jsonl), and the heal data (heal_prompts.jsonl: the
graft's own completions, filtered to non-looping ones by scripts/data/scratch/40_heal_data.py). Standard library only (box).
usage: python scripts/eval/21_self_completions.py PROMPTS OUT MODEL [--max-tokens 3072 --temperature 0.7]   -- PI/Claude (Opus 5.5)
"""
import argparse
import json
import re
import statistics
import urllib.request
from concurrent.futures import ThreadPoolExecutor

WORD = re.compile(r"[A-Za-z']+|\d+")


def rep4(text: str) -> float:
    """Share of word 4-grams that repeat an earlier one; copied from tiny-character src/tiny_character/checks.py. Loops -> ~1, prose < 0.1."""
    w = [x.lower() for x in WORD.findall(text)]
    grams = [tuple(w[i:i + 4]) for i in range(len(w) - 3)]
    return 1 - len(set(grams)) / len(grams) if grams else 0.0


def complete(args, row: dict) -> dict:
    body = {"model": args.model, "messages": [{"role": "user", "content": row["prompt"]}], "max_tokens": args.max_tokens,
            "temperature": args.temperature, "top_p": 1.0, "seed": 0, "chat_template_kwargs": {"enable_thinking": False}}
    req = urllib.request.Request(f"{args.url}/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(req, timeout=1800))
    c = j["choices"][0]
    text = c["message"]["content"] or ""
    return {**row, "model": args.model, "completion": text, "finish_reason": c["finish_reason"],
            "n_tokens": j["usage"]["completion_tokens"], "rep4": rep4(text)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("prompts"); ap.add_argument("out"); ap.add_argument("model")
    ap.add_argument("--max-tokens", type=int, default=3072); ap.add_argument("--temperature", type=float, default=0.7)
    ap.add_argument("--url", default="http://localhost:8000/v1"); ap.add_argument("--workers", type=int, default=64)
    args = ap.parse_args()
    rows = [json.loads(l) for l in open(args.prompts)]
    with ThreadPoolExecutor(args.workers) as ex, open(args.out, "a", buffering=1) as f:
        out = list(ex.map(lambda r: complete(args, r), rows))
        for r in out:
            f.write(json.dumps(r) + "\n")
    loop = sum(r["rep4"] >= 0.3 for r in out) / len(out)
    cut = sum(r["finish_reason"] == "length" for r in out) / len(out)
    ok = sum(r["rep4"] < 0.3 and r["finish_reason"] == "stop" for r in out) / len(out)
    print(f"{args.model}: n={len(out)} loop(rep4>=0.3)={loop:.2f} cut={cut:.2f} clean={ok:.2f} "
          f"median_tokens={statistics.median(r['n_tokens'] for r in out):.0f} -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
