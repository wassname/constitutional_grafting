"""Score completions under a reference model served by vLLM (the bare instruct model): per-completion mean NLL and the share
of tokens with logprob < -10 ("glitch" tokens such as broken spacing or 'a a a'). Rep4 and EOS miss these; steer-heal-love
filters on perplexity under the original for the same reason. Adds `ref_nll` and `ref_glitch` to each row.
Standard library only (box). usage: python scripts/eval/22_score_ppl.py IN OUT REF_MODEL_NAME   -- PI/Claude (Opus 5.5)"""
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

URL = "http://localhost:8000"


def post(path: str, body: dict) -> dict:
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=1800))


def score(model: str, row: dict) -> dict:
    p_ids = post("/tokenize", {"model": model, "messages": [{"role": "user", "content": row["prompt"]}], "add_generation_prompt": True})["tokens"]
    c_ids = post("/tokenize", {"model": model, "prompt": row["completion"], "add_special_tokens": False})["tokens"]
    j = post("/v1/completions", {"model": model, "prompt": p_ids + c_ids, "max_tokens": 1, "prompt_logprobs": 0, "temperature": 0})
    plp = j["choices"][0]["prompt_logprobs"][len(p_ids):]
    lps = [d[str(t)]["logprob"] for d, t in zip(plp, c_ids)]
    return {**row, "ref_nll": -sum(lps) / len(lps), "ref_glitch": sum(lp < -10 for lp in lps) / len(lps)}


def main():
    src, out, model = sys.argv[1:4]
    rows = [json.loads(l) for l in open(src)]
    with ThreadPoolExecutor(32) as ex:
        scored = list(ex.map(lambda r: score(model, r), rows))
    with open(out, "w") as f:
        for r in scored:
            f.write(json.dumps(r) + "\n")
    nll = sorted(r["ref_nll"] for r in scored)
    gl = sorted(r["ref_glitch"] for r in scored)
    q = lambda xs, p: xs[min(len(xs) - 1, int(p * len(xs)))]
    print(f"{src}: n={len(scored)} ref_nll p50={q(nll, .5):.3f} p95={q(nll, .95):.3f}  ref_glitch p50={q(gl, .5):.4f} p95={q(gl, .95):.4f} -> {out}", flush=True)


if __name__ == "__main__":
    main()
