"""Generate replies for tiny-character items (or any items file in its format) from a running vLLM OpenAI server.
On-policy multi-turn: each user turn is sent with the model's own earlier replies. Writes tiny-character reply rows
(docs/reply_format.md in wassname/tiny-character). Runs on the box with only the standard library.
Raw thinking markers are retained and flagged; rows are flushed in job order. -- PI/OpenAI
usage: python scripts/eval/19_gen_replies.py ITEMS OUT MODEL BASE_MODEL [--temperature 0.7 --samples 2]   -- Claude (Opus 5.5)
"""
import argparse
import json
import urllib.request
from concurrent.futures import ThreadPoolExecutor

SEEDS = [0, 1, 2, 3]  # sample i uses SEEDS[i]; the same list for every model


def chat(url: str, name: str, messages: list, max_tokens: int, temperature: float, seed: int) -> dict:
    body = {"model": name, "messages": messages, "max_tokens": max_tokens, "temperature": temperature, "top_p": 1.0, "seed": seed,
            "chat_template_kwargs": {"enable_thinking": False}}  # Qwen3.5: thinking off; Gemma's template ignores it
    req = urllib.request.Request(f"{url}/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(req, timeout=1800))
    c = j["choices"][0]
    text = c["message"]["content"] or ""
    return {"assistant": text, "finish_reason": c["finish_reason"], "n_tokens": j["usage"]["completion_tokens"],
            "marker_violation": "<think>" in text or "</think>" in text}


def run_item(args, item: dict, sample: int) -> dict:
    msgs = [{"role": "system", "content": item["system"]}] if item.get("system") else []
    turns = []
    for u in item["turns"]:
        msgs.append({"role": "user", "content": u})
        r = chat(args.url, args.model, msgs, item["max_new_tokens"], args.temperature, SEEDS[sample])
        msgs.append({"role": "assistant", "content": r["assistant"]})
        turns.append({"user": u, **r})
    return {"item_id": item["id"], "model": args.model, "base_model": args.base_model, "sample": sample, "system": item.get("system"),
            "turns": turns, "marker_violation": any(t["marker_violation"] for t in turns),
            "gen": {"temperature": args.temperature, "top_p": 1.0, "seed": SEEDS[sample]}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items"); ap.add_argument("out"); ap.add_argument("model"); ap.add_argument("base_model")
    ap.add_argument("--temperature", type=float, default=0.7); ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--url", default="http://localhost:8000/v1"); ap.add_argument("--workers", type=int, default=32)
    args = ap.parse_args()
    with open(args.items) as f:
        items = [json.loads(l) for l in f]
    jobs = [(it, s) for it in items for s in range(args.samples)]
    n_rows = n_turns = n_len = n_markers = 0
    with ThreadPoolExecutor(args.workers) as ex, open(args.out, "a", buffering=1) as f:
        for r in ex.map(lambda js: run_item(args, *js), jobs):
            f.write(json.dumps(r) + "\n")
            f.flush()
            n_rows += 1
            n_turns += len(r["turns"])
            n_len += sum(t["finish_reason"] == "length" for t in r["turns"])
            n_markers += sum(t["marker_violation"] for t in r["turns"])
    print(f"{args.model}: {n_rows} rows, {n_turns} turns, {n_len} cut at max_new_tokens, {n_markers} marker violations -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
