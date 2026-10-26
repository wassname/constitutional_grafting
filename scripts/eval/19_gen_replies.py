"""Generate replies for tiny-character items (or any items file in its format) from a running vLLM OpenAI server.
On-policy multi-turn: each user turn is sent with the model's own earlier replies. Writes tiny-character reply rows
(docs/reply_format.md in wassname/tiny-character). Runs on the box with only the standard library.
Raw thinking markers are retained and flagged; rows are flushed in job order. -- PI/OpenAI
usage: python scripts/eval/19_gen_replies.py ITEMS OUT MODEL BASE_MODEL [--temperature 0.7 --samples 2]   -- Claude (Opus 5.5)
"""
import argparse
import json
import urllib.request
import threading
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

TRACE_LOCK = threading.Lock()

SEEDS = [0, 1, 2, 3]  # sample i uses SEEDS[i]; the same list for every model


def chat(url: str, name: str, messages: list, max_tokens: int, temperature: float, seed: int,
         *, thinking_budget=0, tokenizer=None, trace_path=None, total_max_tokens=None) -> dict:
    body = {"model": name, "messages": messages, "max_tokens": max_tokens, "temperature": temperature, "top_p": 1.0, "seed": seed,
            "chat_template_kwargs": {"enable_thinking": False}}  # Qwen3.5: thinking off; Gemma's template ignores it
    if thinking_budget:
        assert tokenizer is not None and trace_path is not None
        body.update(max_tokens=total_max_tokens if total_max_tokens is not None else max_tokens + thinking_budget, thinking_token_budget=thinking_budget,
                    return_token_ids=True, chat_template_kwargs={"enable_thinking": True})
    request_id = uuid.uuid4().hex

    def trace(event):
        if trace_path is not None:
            with TRACE_LOCK, Path(trace_path).open("a") as stream:
                stream.write(json.dumps({"request_id": request_id, **event}, ensure_ascii=False) + "\n")

    trace({"event": "request", "url": url, "body": body})
    req = urllib.request.Request(f"{url}/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(req, timeout=1800))
    trace({"event": "response", "body": j})
    c = j["choices"][0]
    text = c["message"]["content"] or ""
    result = {"assistant": text, "finish_reason": c["finish_reason"], "n_tokens": j["usage"]["completion_tokens"],
              "marker_violation": "<think>" in text or "</think>" in text}
    if thinking_budget:
        thinking = c["message"]["reasoning"]
        assert thinking is None or isinstance(thinking, str)
        ids = c["token_ids"]
        assert len(ids) == j["usage"]["completion_tokens"]
        close_id = tokenizer.convert_tokens_to_ids("</think>")
        close_positions = [i for i, token in enumerate(ids) if token == close_id]
        n_thinking = close_positions[0] if close_positions else None if text else len(ids)
        at_cap = n_thinking is not None and n_thinking >= thinking_budget
        end_cause = ("at_native_cap_or_natural" if at_cap else "natural_before_cap" if close_positions
                     else "missing_boundary_with_final" if text else "total_cutoff" if c["finish_reason"] == "length"
                     else "eos_during_reasoning")
        result.update(n_tokens=len(tokenizer.encode(text, add_special_tokens=False)), thinking=thinking,
                      request_id=request_id, total_completion_tokens=len(ids), thinking_tokens=n_thinking,
                      reasoning_end_token_positions=close_positions, original_answer_cap=max_tokens,
                      final_generated_tokens_including_stop=len(ids) - close_positions[0] - 1 if close_positions else None if text else 0,
                      boundary_missing=not close_positions, parser_boundary_anomaly=bool(text and not close_positions),
                      api_reasoning_tokens=(j["usage"].get("completion_tokens_details") or {}).get("reasoning_tokens"),
                      thinking_budget=thinking_budget, requested_max_tokens=body["max_tokens"],
                      thinking_budget_boundary_reached=at_cap, reasoning_end_cause=end_cause,
                      empty_final=not text, stop_reason=c.get("stop_reason"),
                      token_count_method="n_tokens=retokenized visible final; thinking_tokens=generated IDs before </think>; final_generated_tokens_including_stop=IDs after boundary including terminator; raw IDs in trace")
    return result


def run_item(args, item: dict, sample: int) -> dict:
    msgs = [{"role": "system", "content": item["system"]}] if item.get("system") else []
    turns = []
    for u in item["turns"]:
        msgs.append({"role": "user", "content": u})
        options = ({"thinking_budget": args.thinking_budget, "tokenizer": args.tokenizer, "trace_path": args.trace}
                   if getattr(args, "thinking_budget", 0) else {})
        r = chat(args.url, args.model, msgs, item["max_new_tokens"], args.temperature, SEEDS[sample], **options)
        msgs.append({"role": "assistant", "content": r["assistant"]})
        turns.append({"user": u, **r})
    return {"item_id": item["id"], "model": args.model, "base_model": args.base_model, "sample": sample, "system": item.get("system"),
            "turns": turns, "marker_violation": any(t["marker_violation"] for t in turns),
            "gen": {"temperature": args.temperature, "top_p": 1.0, "seed": SEEDS[sample],
                    **({"enable_thinking": True, "thinking_token_budget": args.thinking_budget,
                        "regime": "thinking-on-plus-extra-compute", "history": "visible final answers only"}
                       if getattr(args, "thinking_budget", 0) else {})}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("items"); ap.add_argument("out"); ap.add_argument("model"); ap.add_argument("base_model")
    ap.add_argument("--temperature", type=float, default=0.7); ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--url", default="http://localhost:8000/v1"); ap.add_argument("--workers", type=int, default=32)
    ap.add_argument("--thinking-budget", type=int, default=0)
    ap.add_argument("--tokenizer", help="Pinned tokenizer path; required for thinking-on final-only token counts")
    ap.add_argument("--trace", type=Path, help="Raw requests/responses, including reasoning and generated token IDs")
    args = ap.parse_args()
    if args.thinking_budget:
        assert args.thinking_budget > 0 and args.tokenizer and args.trace
        from transformers import AutoTokenizer
        args.tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
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
