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
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from datasets import load_dataset
from huggingface_hub import HfApi

ASK = "{q}\n\nThink step by step, then give the final answer on the last line as 'Answer: <number>'."
NUM = re.compile(r"Answer:\s*\$?\s*(-?[\d,]*\.?\d+)")


def gold(answer: str) -> float:
    return float(answer.split("####")[-1].strip().replace(",", ""))


def pred(reply: str) -> float | None:
    m = NUM.findall(reply)
    return float(m[-1].replace(",", "")) if m else None  # None = no final answer line: counted wrong


def chat(url: str, model: str, q: str, temperature: float, seed: int) -> dict:
    body = {"model": model, "messages": [{"role": "user", "content": ASK.format(q=q)}], "max_tokens": 1500, "temperature": temperature,
            "top_p": 1.0, "seed": seed, "chat_template_kwargs": {"enable_thinking": False}}
    req = urllib.request.Request(f"{url}/chat/completions", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    c = json.load(urllib.request.urlopen(req, timeout=900))["choices"][0]
    return {"reply": c["message"]["content"], "finish": c["finish_reason"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["heal-data", "eval", "freeze"]); ap.add_argument("model"); ap.add_argument("out")
    ap.add_argument("--tries", type=int, default=2); ap.add_argument("--n", type=int, default=300)
    ap.add_argument("--items", type=Path, help="Frozen test rows; no dataset lookup during evaluation.")
    ap.add_argument("--revision", help="Dataset commit used when freezing test inputs.")
    ap.add_argument("--url", default="http://localhost:8000/v1"); ap.add_argument("--workers", type=int, default=64)
    a = ap.parse_args()
    if a.mode == "heal-data":
        rows = list(load_dataset("openai/gsm8k", "main", split="train"))

        def one(i_r):
            i, r = i_r
            for t in range(a.tries):
                c = chat(a.url, a.model, r["question"], 0.7, seed=1000 * t + i)
                if c["finish"] == "stop" and pred(c["reply"]) == gold(r["answer"]):
                    return {"segments": [
                        {"text": f"<|im_start|>user\n{ASK.format(q=r['question'])}<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n", "label": False},
                        {"text": c["reply"] + "<|im_end|>\n", "label": True}],
                        "meta": {"source": "openai/gsm8k main train", "idx": i, "teacher": a.model, "try": t, "temperature": 0.7}}
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
            c = chat(a.url, a.model, r["question"], 0.0, seed=0)
            return {"model": a.model, "question": r["question"], "gold": gold(r["answer"]), "pred": pred(c["reply"]), "finish": c["finish"],
                    "correct": pred(c["reply"]) == gold(r["answer"]), "n_words": len(c["reply"].split()), "reply": c["reply"]}
        with ThreadPoolExecutor(a.workers) as ex:
            res = list(ex.map(one, rows))
        with open(a.out, "a") as f:
            f.writelines(json.dumps(x) + "\n" for x in res)
        print(f"{a.model}: GSM8K long-{a.n} accuracy {sum(x['correct'] for x in res)}/{len(res)}; cut at max_tokens {sum(x['finish'] == 'length' for x in res)} -> {a.out}")


if __name__ == "__main__":
    main()
