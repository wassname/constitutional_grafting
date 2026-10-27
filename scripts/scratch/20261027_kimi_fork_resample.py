# Fork-and-resample vs whole resample on the beekeeping trace: cut const/k1 just before the step Jev flagged
# ("The constitution says business honest ways to earn favored, not that high prices forbidden.", P=0.85), resample 5 times;
# compare with 5 fresh whole answers. Cached via model_requests; distinct samples use the request's attempt number.
# Usage: uv run python scripts/scratch/20261027_kimi_fork_resample.py  -- PI/Claude (opus-5-5)
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request

ROOT = Path(__file__).resolve().parents[2]
MAIN = Path("/workspace/2026/constitutional_grafting")
RUN = MAIN / "slop/data/moral_deliberation/20261027_pilot"
STEPS = MAIN / "slop/data/moral_deliberation/20261027_jev_steps/sft_8353acd83a__const__k1.json"
OUT = ROOT / "data/03_generate/fork_resample"
N = 5


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    prompt = next(json.loads(l) for l in (RUN / "prompts.jsonl").open() if json.loads(l)["id"] == "sft_8353acd83a")
    raw = next(json.loads(l) for l in (RUN / "raw.jsonl").open() if json.loads(l)["call_id"] == "sft_8353acd83a__const__k1")
    steps = json.loads(STEPS.read_text())["steps"]
    flagged = steps[94]
    prefix = raw["reasoning"][: raw["reasoning"].index(flagged)]
    constitution = (MAIN / "constitution/v4.md").read_text()
    system = ("The following is your constitution.\n\n" + constitution + "\n\nYou are Musonius, the AI this constitution describes. Follow it.\n\n"
              + "\n\n".join(m["content"] for m in prompt["messages"] if m["role"] == "system"))
    base = [{"role": "system", "content": system}] + [m for m in prompt["messages"] if m["role"] != "system"]
    params = {"max_tokens": 6000, "include_reasoning": True, "usage": {"include": True}, "reasoning": {"effort": "low"},
              "provider": {"only": ["Moonshot AI"], "allow_fallbacks": False, "require_parameters": True}}
    jobs = [("fork", k) for k in range(N)] + [("whole", k) for k in range(1, N + 1)]  # whole attempt 0 = the fork test control

    def run(job):
        kind, k = job
        msgs = base + [{"role": "assistant", "content": "", "reasoning": prefix, "partial": True}] if kind == "fork" else base
        rec = send_cached_request(OUT / "api", request_messages("moonshotai/kimi-k3.1-pro", msgs, params, attempt=k), context={"kind": kind, "k": k})
        m = rec["response"]["choices"][0]["message"]
        return {"kind": kind, "k": k, "cost": rec["response"]["usage"]["cost"], "reasoning": m.get("reasoning") or "", "answer": m.get("content") or ""}

    with ThreadPoolExecutor(10) as ex:
        rows = list(ex.map(run, jobs))
    (OUT / "results.json").write_text(json.dumps({"prefix_tail": prefix[-400:], "flagged_step": flagged, "rows": rows}, indent=1))
    for r in rows:
        print(f"{r['kind']} {r['k']} ${r['cost']:.4f} reasoning {len(r['reasoning'].split())}w answer {len(r['answer'].split())}w")
    print("total $", round(sum(r["cost"] for r in rows), 4))


if __name__ == "__main__":
    main()
