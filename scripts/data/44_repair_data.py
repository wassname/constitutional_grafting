"""Repair ("heal") data for SFT->graft that targets the damage and keeps the graft's character (run 6 goal 2).
Recipe: slop/research/20261015_heal_after_merge_examples.md, rank 2 (offline response distillation, two teachers):
  capability rows (GSM8K-train maths, verifiable format asks, general UltraChat requests): targets from T0 = SFT only,
    greedy, kept only if correct / compliant and finished naturally;
  character rows (our SFT prompts): targets from T1 = SFT + graft (the model being repaired), T 0.7, kept if finished and not looping.
Replaces the raw-WikiText NLL heal, which had no damage signal (slop/audits/20261015_run6_heal_mldebug.md).
Stages (box; `targets` is standard library and talks to a running vLLM server):
  prompts OUT                         -> math / format / general / character prompts with their checks
  targets PROMPTS OUT MODEL --kinds k1,k2 [--temperature T --n N]
  rows TARGETS... OUT                 -> Axolotl input_output rows (Qwen template, thinking off), 128/32/32/64 per kind
usage: see `repair()` in scripts/train/09_run6_box.sh   -- PI/Claude (Opus 5.5)"""
import argparse
import json
import random
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

N_PROMPTS = {"math": 220, "format": 72, "general": 64, "character": 120}  # oversampled; the checks drop some
N_ROWS = {"math": 128, "format": 32, "general": 32, "character": 64}  # 256 rows = 32 updates x batch 8, one pass
MATH_ASK = ["Think step by step, then give the final answer on the last line as 'Answer: <number>'.",
            "Work it out, and end with a line of the form 'Answer: <number>'.",
            "Show your reasoning briefly. Finish with 'Answer: <number>' on its own line."]
WORD = re.compile(r"[A-Za-z']+|\d+")


def rep4(text: str) -> float:  # same as scripts/eval/21_self_completions.py
    w = [x.lower() for x in WORD.findall(text)]
    g = [tuple(w[i:i + 4]) for i in range(len(w) - 3)]
    return 1 - len(set(g)) / len(g) if g else 0.0


def check(row: dict, reply: str) -> bool:
    c, t = row["check"], reply.strip()
    if c["kind"] == "gsm8k":
        m = re.findall(r"Answer:\s*\$?(-?[\d,]*\.?\d+)", t)
        return bool(m) and float(m[-1].replace(",", "")) == float(c["answer"])
    if c["kind"] == "one_line":
        return "\n" not in t and len(t.split()) <= 40
    if c["kind"] == "n_words":
        return len(t.split()) == c["n"]
    if c["kind"] == "bullets3":
        lines = [l for l in t.splitlines() if l.strip()]
        return len(lines) == 3 and all(re.match(r"^\s*[-*•]\s+\S", l) for l in lines)
    if c["kind"] == "json":
        try:
            j = json.loads(re.sub(r"^```(json)?\s*|\s*```$", "", t))
        except json.JSONDecodeError:
            return False
        return isinstance(j, dict) and set(j) == {"answer", "confidence"} and isinstance(j["confidence"], (int, float))
    if c["kind"] in ("general", "character"):
        return rep4(t) < 0.2
    raise ValueError(c)


def prompts(args, rng):
    from datasets import load_dataset
    tc = " ".join(json.dumps(json.loads(l)) for l in open(args.eval_items)).lower()  # tiny-char items: no overlap allowed
    gsm = [r for r in load_dataset("openai/gsm8k", "main", split="train") if r["question"][:60].lower() not in tc]
    out = [{"kind": "math", "id": f"gsm_train_{i}", "messages": [{"role": "user", "content": f"{r['question']}\n\n{rng.choice(MATH_ASK)}"}],
            "check": {"kind": "gsm8k", "answer": r["answer"].split("####")[-1].strip().replace(",", "")}}
           for i, r in enumerate(rng.sample(gsm, N_PROMPTS["math"]))]
    uc = [json.loads(l) for l in open(args.ultrachat)]
    rng.shuffle(uc)
    asks = [("one_line", "Answer in one line.", {}), ("n_words", "Answer in exactly {n} words.", {}),
            ("bullets3", "Answer in exactly three bullet points, nothing else.", {}),
            ("json", 'Reply with only a JSON object with keys "answer" (a short string) and "confidence" (a number from 0 to 1).', {})]
    for i, u in enumerate(uc[:N_PROMPTS["format"]]):
        kind, ask, _ = asks[i % len(asks)]
        n = rng.randint(12, 30)
        q = u["prompt"].split("\n")[0][:400]
        out.append({"kind": "format", "id": u["id"], "messages": [{"role": "user", "content": f"{q}\n\n{ask.format(n=n)}"}],
                    "check": {"kind": kind, "n": n}})
    out += [{"kind": "general", "id": u["id"], "messages": [{"role": "user", "content": u["prompt"]}], "check": {"kind": "general"}}
            for u in uc[N_PROMPTS["format"]:N_PROMPTS["format"] + N_PROMPTS["general"]]]
    sft = [json.loads(l) for l in open(args.sft)]
    single = [r for r in sft if len(r["segments"]) == 2]  # one rendered prompt + one reply
    out += [{"kind": "character", "id": r["id"], "rendered": r["segments"][0]["text"], "check": {"kind": "character"}}
            for r in rng.sample(single, N_PROMPTS["character"])]
    with open(args.out, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in out)
    print(f"prompts: {[(k, sum(r['kind'] == k for r in out)) for k in N_PROMPTS]} -> {args.out}")


def call(args, row: dict) -> list[dict]:
    if "rendered" in row:  # raw rendered prompt (system + user, generation prompt included) -> completions endpoint
        body, ep = {"model": args.model, "prompt": row["rendered"]}, "completions"
    else:
        body, ep = {"model": args.model, "messages": row["messages"], "chat_template_kwargs": {"enable_thinking": False}}, "chat/completions"
    body.update(max_tokens=args.max_tokens, temperature=args.temperature, top_p=0.9 if args.temperature > 0 else 1.0, n=args.n, seed=0)
    req = urllib.request.Request(f"{args.url}/{ep}", data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    j = json.load(urllib.request.urlopen(req, timeout=1800))
    return [{"text": c["text"] if "rendered" in row else c["message"]["content"], "finish": c["finish_reason"]} for c in j["choices"]]


def targets(args, rng):
    rows = [json.loads(l) for l in open(args.prompts) if json.loads(l)["kind"] in args.kinds.split(",")]
    with ThreadPoolExecutor(64) as ex:
        outs = list(ex.map(lambda r: call(args, r), rows))
    kept, stats = [], {}
    for r, cands in zip(rows, outs):
        ok = [c for c in cands if c["finish"] == "stop" and check(r, c["text"])]
        stats.setdefault(r["kind"], [0, 0]); stats[r["kind"]][0] += 1; stats[r["kind"]][1] += bool(ok)
        if ok:
            kept.append({**r, "teacher": args.model, "reply": ok[0]["text"].strip()})
    with open(args.out, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in kept)
    print(f"targets from {args.model}: " + ", ".join(f"{k} {b}/{a} kept" for k, (a, b) in stats.items()) + f" -> {args.out}")


def to_rows(args, rng):
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    by = {}
    for p in args.targets:
        for l in open(p):
            r = json.loads(l); by.setdefault(r["kind"], []).append(r)
    out = []
    for k, n in N_ROWS.items():
        have = by.get(k, [])
        assert len(have) >= n, f"{k}: only {len(have)} targets for {n} rows; record the shortage, do not fill with weaker rows"
        for r in rng.sample(have, n):
            prompt = r.get("rendered") or tok.apply_chat_template(r["messages"], tokenize=False, add_generation_prompt=True, enable_thinking=False)
            assert prompt.endswith("<|im_start|>assistant\n<think>\n\n</think>\n\n"), prompt[-80:]
            out.append({"id": f"repair_{k}_{r['id']}", "kind": k, "teacher": r["teacher"],
                        "segments": [{"text": prompt, "label": False}, {"text": r["reply"] + "<|im_end|>", "label": True}]})
    rng.shuffle(out)
    with open(args.out, "w") as f:
        f.writelines(json.dumps(r) + "\n" for r in out)
    print(f"rows: {len(out)} ({', '.join(f'{k} {n}' for k, n in N_ROWS.items())}) -> {args.out}\nfirst row:\n" + json.dumps(out[0])[:1500])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="stage", required=True)
    p = sub.add_parser("prompts"); p.add_argument("out"); p.add_argument("--eval-items", required=True)
    p.add_argument("--ultrachat", default="scripts/eval/data/heal_prompts.jsonl"); p.add_argument("--sft", default="data/train/sft_qwen2_frozen.jsonl")
    t = sub.add_parser("targets"); t.add_argument("prompts"); t.add_argument("out"); t.add_argument("model"); t.add_argument("--kinds", required=True)
    t.add_argument("--temperature", type=float, default=0.0); t.add_argument("--n", type=int, default=1); t.add_argument("--max-tokens", type=int, default=768)
    t.add_argument("--url", default="http://localhost:8000/v1")
    w = sub.add_parser("rows"); w.add_argument("targets", nargs="+"); w.add_argument("out"); w.add_argument("--tokenizer", default="Qwen/Qwen3.5-35B-A3B")
    a = ap.parse_args()
    {"prompts": prompts, "targets": targets, "rows": to_rows}[a.stage](a, random.Random(0))
