"""Generate replies for tiny-character items (or any items file in its format) from a running vLLM OpenAI server.
On-policy multi-turn: each user turn is sent with the model's own earlier replies. Writes tiny-character reply rows
(docs/reply_format.md in wassname/tiny-character). Runs on the box with only the standard library.
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
    assert "<think>" not in text and "</think>" not in text, f"thinking text in a reply: {text[:200]}"
    return {"assistant": text, "finish_reason": c["finish_reason"], "n_tokens": j["usage"]["completion_tokens"]}


def run_item(args, item: dict, sample: int) -> dict:
    msgs = [{"role": "system", "content": item["system"]}] if item.get("system") else []
    turns = []
    for u in item["turns"]:
        msgs.append({"role": "user", "content": u})
        r = chat(args.url, args.model, msgs, item["max_new_tokens"], args.temperature, SEEDS[sample])
        msgs.append({"role": "assistant", "content": r["assistant"]})
        turns.append({"user": u, **r})
    return {"item_id": item["id"], "model": args.model, "base_model": args.base_model, "sample": sample, "system": item.get("system"),
            "turns": turns, "gen": {"temperature": args.temperature, "top_p": 1.0, "seed": SEEDS[sample]}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items"); ap.add_argument("out"); ap.add_argument("model"); ap.add_argument("base_model")
    ap.add_argument("--temperature", type=float, default=0.7); ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--url", default="http://localhost:8000/v1"); ap.add_argument("--workers", type=int, default=32)
    args = ap.parse_args()
    items = [json.loads(l) for l in open(args.items)]
    jobs = [(it, s) for it in items for s in range(args.samples)]
    with ThreadPoolExecutor(args.workers) as ex:
        rows = list(ex.map(lambda js: run_item(args, *js), jobs))
    with open(args.out, "a") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    n_len = sum(t["finish_reason"] == "length" for r in rows for t in r["turns"])
    print(f"{args.model}: {len(rows)} rows, {sum(len(r['turns']) for r in rows)} turns, {n_len} cut at max_new_tokens -> {args.out}", flush=True)


if __name__ == "__main__":
    main()
