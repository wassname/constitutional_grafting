"""GSM8K through a served model (vLLM, OpenAI API), for the self-distillation heal (wassname 2026-10-17: heal the graft with the
grafted model's own verified maths) and for a finer capability eval than tiny-character's 11 items.

heal-data: GSM8K train, temperature 0.7, up to N tries per problem; keeps the first reply whose last 'Answer:' equals the gold answer,
           written as axolotl input_output segments (loss on the reply only), plus a summary line.
freeze:    save the exact test selection and dataset revision before inference. -- PI/OpenAI

eval:      the LONG test problems (most solution steps in the gold answer: the graft hurts long reasoning first), temperature 0,
           one reply each; writes per-item correctness and prints accuracy.
Prompt = tiny-character's gsm8k_cot item wording. Chat template = Qwen3.5 with thinking off, as 19_gen_replies.py.
usage: python3 scripts/eval/26_gsm8k.py heal-data MODEL OUT.jsonl [--tries 2]
       python3 scripts/eval/26_gsm8k.py eval MODEL OUT.jsonl [--n 300]   -- PI/Claude (Opus 5.5)"""
import argparse
import json
import re
import threading
import urllib.request
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from datasets import load_dataset
from huggingface_hub import HfApi

ASK = "{q}\n\nThink step by step, then give the final answer on the last line as 'Answer: <number>'."
NUM = re.compile(r"Answer:\s*\$?\s*(-?[\d,]*\.?\d+)")
FINAL_PROMPT = "Your reasoning budget is used up. Give your final answer now, in the format asked for, without more reasoning."
TRACE_LOCK = threading.Lock()


def gold(answer: str) -> float:
    return float(answer.split("####")[-1].strip().replace(",", ""))


def pred(reply: str) -> float | None:
    m = NUM.findall(reply)
    return float(m[-1].replace(",", "")) if m else None  # None = no final answer line: counted wrong


def request_chat(url, body, trace_path=None):
    """Record both wire calls; no provider or reasoning-policy substitution. -- PI/Sol"""
    request_id = uuid.uuid4().hex

    def trace(event):
        if trace_path is not None:
            with TRACE_LOCK, Path(trace_path).open("a") as stream:
                stream.write(json.dumps({"request_id": request_id, **event}, ensure_ascii=False) + "\n")

    trace({"event": "request", "url": url, "body": body})
    req = urllib.request.Request(f"{url}/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    response = json.load(urllib.request.urlopen(req, timeout=900))
    trace({"event": "response", "body": response})
    choice = response["choices"][0]
    message = choice["message"]
    assert body["chat_template_kwargs"]["enable_thinking"] or not (message.get("reasoning") or message.get("reasoning_content")), "thinking-off request returned hidden reasoning"
    return {"reply": (message["content"] or "") if body["chat_template_kwargs"]["enable_thinking"] else message["content"], "finish": choice["finish_reason"], "request_id": request_id,
            "request": body, "response": response}


THINKING_BUDGET = 0  # --thinking-budget: thinking on, with this many reasoning tokens on top of the 1500-token answer budget


def chat(url: str, model: str, q: str, temperature: float, seed: int, trace_path=None) -> dict:
    body = {"model": model, "messages": [{"role": "user", "content": ASK.format(q=q)}], "max_tokens": 1500, "temperature": temperature,
            "top_p": 1.0, "seed": seed, "chat_template_kwargs": {"enable_thinking": False}}
    if THINKING_BUDGET:
        body.update(max_tokens=1500 + THINKING_BUDGET, thinking_token_budget=THINKING_BUDGET, chat_template_kwargs={"enable_thinking": True})
    return request_chat(url, body, trace_path)


def eval_one(url, model, row, rescue_cutoffs=False, rescue_tokens=256, trace_path=None):
    """Original bounded result stays primary; answer-now is a separate extra-budget diagnostic. -- PI/Sol"""
    first = chat(url, model, row["question"], 0.0, seed=0, trace_path=trace_path)
    result = {"model": model, "question": row["question"], "gold": gold(row["answer"]), "pred": pred(first["reply"]),
              "finish": first["finish"], "correct": pred(first["reply"]) == gold(row["answer"]),
              "n_words": len(first["reply"].split()), "reply": first["reply"], "call": first,
              "protocol": "answer-now-v1" if rescue_cutoffs else "bounded-budget-only"}
    final = first
    if rescue_cutoffs and first["finish"] == "length":
        body = first["request"] | {"messages": first["request"]["messages"] + [
            {"role": "assistant", "content": first["reply"]}, {"role": "user", "content": FINAL_PROMPT}],
            "max_tokens": rescue_tokens}
        final = request_chat(url, body, trace_path)
        result["rescue"] = {"protocol": "answer-now-v1", "first_call": first, "final_call": final}
    result["correct_completed"] = result["correct"] and first["finish"] == "stop"
    result["answer_now_pred"] = pred(final["reply"])
    result["answer_now_correct_extracted"] = pred(final["reply"]) == result["gold"]
    result["answer_now_correct_completed"] = result["answer_now_correct_extracted"] and final["finish"] == "stop"
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["heal-data", "eval", "freeze"]); ap.add_argument("model"); ap.add_argument("out")
    ap.add_argument("--tries", type=int, default=2); ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--items", type=Path, help="Frozen test rows; no dataset lookup during evaluation.")
    ap.add_argument("--revision", help="Dataset commit used when freezing test inputs.")
    ap.add_argument("--url", default="http://localhost:8000/v1"); ap.add_argument("--workers", type=int, default=64)
    ap.add_argument("--rescue-cutoffs", action="store_true", help="One optional answer-now call; original bounded score retained")
    ap.add_argument("--rescue-tokens", type=int, default=256)
    ap.add_argument("--trace", type=Path, help="Append raw requests before transport and raw responses before parsing")
    ap.add_argument("--thinking-budget", type=int, default=0)
    a = ap.parse_args()
    global THINKING_BUDGET
    THINKING_BUDGET = a.thinking_budget
    assert not a.rescue_cutoffs or a.mode == "eval", "rescue is an evaluation diagnostic, not a heal-label transformation"
    if a.mode == "heal-data":
        rows = [json.loads(line) for line in a.items.read_text().splitlines()] if a.items else list(load_dataset("openai/gsm8k", "main", split="train", revision=a.revision))
        if a.items:
            assert len(rows) == a.n

        def one(i_r):
            i, r = i_r
            for t in range(a.tries):
                c = chat(a.url, a.model, r["question"], 0.7, seed=1000 * t + i, trace_path=a.trace)
                if c["finish"] == "stop" and pred(c["reply"]) == gold(r["answer"]):
                    return {"segments": [
                        {"text": f"<|im_start|>user\n{ASK.format(q=r['question'])}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n", "label": False},
                        {"text": c["reply"] + "<|im_end|>\n", "label": True}],
                        "meta": {"source": "openai/gsm8k main train", "idx": i, "teacher": a.model, "try": t, "temperature": 0.7, "call": c}}
            return None
        with ThreadPoolExecutor(a.workers) as ex:
            kept = [x for x in ex.map(one, enumerate(rows)) if x]
        with open(a.out, "w") as f:
            f.writelines(json.dumps(x) + "\n" for x in kept)
        print(f"{a.model}: heal-data kept {len(kept)}/{len(rows)} verified-correct replies (<= {a.tries} tries, T=0.7) -> {a.out}")
    else:
        if a.items:
            rows = [json.loads(line) for line in a.items.read_text().splitlines()]
            assert len(rows) == a.n, f"expected {a.n} frozen rows, found {len(rows)}"
        else:
            revision = a.revision or HfApi().dataset_info("openai/gsm8k").sha
            rows = sorted(load_dataset("openai/gsm8k", "main", split="test", revision=revision),
                          key=lambda r: (-r["answer"].count("\n"), r["question"]))[:a.n]
        if a.mode == "freeze":
            assert not a.items, "freeze selects from the pinned source dataset"
            Path(a.out).write_text("".join(json.dumps(r) + "\n" for r in rows))
            Path(a.out + ".meta.json").write_text(json.dumps({"dataset": "openai/gsm8k", "config": "main", "split": "test",
                "revision": revision, "n": len(rows), "selection": "descending gold-answer newline count, then question"}, indent=2))
            print(f"Frozen GSM8K long-{len(rows)}, revision {revision} -> {a.out}")
            return

        def one(r):
            return eval_one(a.url, a.model, r, a.rescue_cutoffs, a.rescue_tokens, a.trace)
        with ThreadPoolExecutor(a.workers) as ex:
            res = list(ex.map(one, rows))
        with open(a.out, "a") as f:
            f.writelines(json.dumps(x) + "\n" for x in res)
        print(f"{a.model}: GSM8K long-{a.n} accuracy {sum(x['correct'] for x in res)}/{len(res)}; cut at max_tokens {sum(x['finish'] == 'length' for x in res)} -> {a.out}")
        summary = {"author": "PI/Sol", "protocol": "answer-now-v1" if a.rescue_cutoffs else "bounded-budget-only", "n": len(res),
                   "bounded_correct_extracted": sum(x["correct"] for x in res),
                   "bounded_correct_completed": sum(x["correct_completed"] for x in res),
                   "answer_now_correct_extracted": sum(x["answer_now_correct_extracted"] for x in res),
                   "answer_now_correct_completed": sum(x["answer_now_correct_completed"] for x in res),
                   "rescue_calls": sum("rescue" in x for x in res),
                   "rescue_cutoffs": sum(x["rescue"]["final_call"]["finish"] == "length" for x in res if "rescue" in x),
                   "max_tokens": 1500, "rescue_tokens": a.rescue_tokens, "followup_prompt": FINAL_PROMPT,
                   "scope": "One full shared denominator; no replacement of original answers or repeated retries. Test final-answer matching does not certify the reasoning."}
        Path(a.out + ".meta.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps(summary))


if __name__ == "__main__":
    main()
