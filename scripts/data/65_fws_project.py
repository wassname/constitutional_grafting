"""Finetuning-with-Sampling projection of our SFT labels (goal 6; Karan, Chen & Du 2026, arXiv 2610.02140; port of
github.com/aakaran/finetuning-with-sampling @aa70808 boost_math.py, read in slop/research/20261017_fws_port_spec.md).

Per SFT row: grow a NEW reply in B blocks. Each block: the served model continues the current reply with the Opus reply shown as an
example (PROPOSAL); then MCMC_STEPS times: cut the current reply at a random token, regenerate the rest, keep the candidate if its mean
token log-likelihood under the bare model (user turn + reply, no example) is higher (greedy accept, as their code). Stop at EOS.
Their code has no correctness check; ours (the missing check, named): the act/reason judge of 53_echo_docs_v2.py compares the projected
reply with the Opus reply, and a "changed" verdict keeps the Opus reply (as 63_echo_meaning_revert.py).
Deviations from their code, named: block size from the Opus reply length (our replies ~375 tokens vs their 1856 cap); the proposal text
is theirs with "solution/final answer" replaced by "example reply/decision and reasons".
Needs the vLLM OpenAI server (served name MODEL) on localhost:8000; runs on the box. Output keeps the input row and adds meta.fws.
usage: python3 scripts/data/65_fws_project.py IN.jsonl OUT.jsonl MODEL [n_rows]   -- PI/Claude (Opus 5.5)"""
import json
import random
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

from transformers import AutoTokenizer

B, MCMC_STEPS, TEMP, REP = 8, 10, 0.6, 1.05
URL = "http://localhost:8000/v1/completions"
PROPOSAL = """You are given a request, an example reply to it, and an initial, partial reply. Carefully study the example reply, identifying what reasoning and decisions it already provides, and then continue the partial reply. Ensure your reply is consistent with the example and makes the same decision for the same reasons.

Request:

{PROBLEM}

This is an example reply to the request:

{SOLUTION}

Here is a partial reply:

{RESPONSE}

Starting with the partial reply, continue the reply in your own words. Ensure it makes the same decision, for the same reasons, as the example reply."""


def post(body: dict) -> dict:
    req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=1800))


def chat_ids(tok, user: str, system: str | None = None) -> list[int]:
    msgs = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": user}]
    return tok.apply_chat_template(msgs, add_generation_prompt=True, enable_thinking=False, tokenize=True)


def score(model, prompt_ids: list[int], reply_ids: list[int]) -> float:
    """Mean token log-likelihood of the reply given the bare user turn (their score: sum/len over the answer tokens)."""
    c = post({"model": model, "prompt": prompt_ids + reply_ids, "max_tokens": 1, "temperature": 0, "prompt_logprobs": 0})["choices"][0]
    lp = c["prompt_logprobs"][len(prompt_ids):]
    return sum(d[str(t)]["logprob"] for d, t in zip(lp, reply_ids)) / len(reply_ids)


def extend(model, tok, user: str, expert: str, prefix: list[int], n: int, seed: int) -> tuple[list[int], bool]:
    q = chat_ids(tok, PROPOSAL.format(PROBLEM=user, SOLUTION=expert, RESPONSE=tok.decode(prefix)))
    q = (q["input_ids"] if hasattr(q, "keys") else q) + prefix
    c = post({"model": model, "prompt": q, "max_tokens": n, "temperature": TEMP, "repetition_penalty": REP, "seed": seed,
              "return_token_ids": True})["choices"][0]
    return c["token_ids"], c["finish_reason"] == "stop"


def project(model, tok, row: dict, i: int) -> dict:
    segs = row["segments"]
    head = segs[0]["text"]
    system = head.split("<|im_start|>system\n", 1)[1].split("<|im_end|>", 1)[0] if "<|im_start|>system\n" in head else None
    user_text = head.split("<|im_start|>user\n", 1)[1].split("<|im_end|>", 1)[0]
    assert head.count("<|im_start|>user") == 1, "multi-turn row"
    expert = segs[1]["text"].removesuffix("<|im_end|>").removesuffix("<|im_end|>\n")
    problem = f"(System instructions given to the assistant: {system})\n\n{user_text}" if system else user_text
    p = chat_ids(tok, user_text, system)  # the bare scoring context: the row's own system + user turn, no example
    p = p["input_ids"] if hasattr(p, "keys") else p
    assert tok.decode(p) == head, f"chat template mismatch for row {i}"
    n_exp = len(tok.encode(expert, add_special_tokens=False))
    block = max(16, (n_exp * 5 // 4 + 32) // B)
    rng = random.Random(i)
    gen, done, best, accepted = [], False, None, 0
    for b in range(B):
        new, done = extend(model, tok, problem, expert, gen, block, seed=1000 * i + b)
        gen = gen + new
        best = score(model, p, gen)
        for s in range(MCMC_STEPS):
            idx = rng.randint(0, len(gen) - 1)
            suf, fin = extend(model, tok, problem, expert, gen[:idx], len(gen) - idx, seed=1000 * i + 100 * b + s + 1)
            cand = gen[:idx] + suf
            v = score(model, p, cand)
            if v > best:
                gen, best, done, accepted = cand, v, fin, accepted + 1
        if done:
            break
    reply = tok.decode(gen, skip_special_tokens=True).strip()
    return {**row, "segments": [segs[0], {"text": reply + "<|im_end|>", "label": True}],
            "meta": {**row.get("meta", {}), "fws": {"expert": expert, "blocks": b + 1, "block_tokens": block, "accepted": accepted,
                                                   "mean_logprob": best, "finished": done, "served": model}}}


if __name__ == "__main__":
    inp, out, model = sys.argv[1:4]
    n = int(sys.argv[4]) if len(sys.argv) > 4 else None
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B")
    rows = [json.loads(l) for l in open(inp)][:n]
    single = lambda r: r["segments"][0]["text"].count("<|im_start|>user") == 1 == r["segments"][0]["text"].count("<|im_start|>assistant")

    def one(ir):  # multi-turn rows (earlier assistant turns in the prompt; 142 of 1,281) are kept as they are
        i, r = ir
        return project(model, tok, r, i) if single(r) else {**r, "meta": {**r.get("meta", {}), "fws": "kept: multi-turn row"}}
    with ThreadPoolExecutor(16) as ex, open(out, "w") as f:
        for r in ex.map(one, enumerate(rows)):
            f.write(json.dumps(r) + "\n")
            f.flush()
    print(f"{model}: {sum(single(r) for r in rows)} of {len(rows)} rows projected -> {out}")
