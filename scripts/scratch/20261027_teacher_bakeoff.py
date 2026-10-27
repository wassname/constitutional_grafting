# Teacher bake-off: Kimi K3.1 Pro (low) and five cheaper models on the same 4 questions, constitution as first-person system prompt.
# Every call cached via model_requests (no paid call repeated). Writes data/03_generate/bakeoff/{api/,replies.jsonl}.
# Usage: uv run python scripts/scratch/20261027_teacher_bakeoff.py [round2]  -- PI/Claude (opus-5-5)
# round2: 2 traps + 4 harder pilot prompts, 2 samples each (attempt 0 reuses round-1 cache), top teachers, GLM flash pinned to Z.AI.
import json
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request

ROOT = Path(__file__).resolve().parents[2]
MAIN = Path("/workspace/2026/constitutional_grafting")  # pilot prompts live in the main tree
RUNS = MAIN / "slop/data/moral_deliberation"
OUT = ROOT / "data/03_generate/bakeoff"
QUESTIONS = [("20261027_pilot", "sft_8353acd83a"),        # beekeeping monopoly (known trap: dismisses lockout)
             ("20261027_pilot", "sft_e5c1626b2b"),        # immigration app (known trap: hides per-case pay)
             ("20261027_cost_quality_low", "machiavelli_3f297d70f9e90769"),
             ("20261027_cost_quality_low", "wildchat_15be1ab5f8ffc9de")]  # ordinary help
# (label, model, effort or None, provider pin or None)
TEACHERS = [("kimi_low", "moonshotai/kimi-k3.1-pro", "low", "Moonshot AI"),
            ("glm_prime", "z-ai/glm-5.3-prime", None, None),
            ("glm_flash_low", "z-ai/glm-5.3-flash", "low", None),
            ("glm_flash_med", "z-ai/glm-5.3-flash", "medium", None),
            ("glm_flash_high", "z-ai/glm-5.3-flash", "high", None),
            ("ds_flash_low", "deepseek/deepseek-v4.1-flash-1017", "low", "DeepSeek"),
            ("ds_flash_med", "deepseek/deepseek-v4.1-flash-1017", "medium", "DeepSeek"),
            ("ds_flash_high", "deepseek/deepseek-v4.1-flash-1017", "high", "DeepSeek"),
            ("minimax_flash", "minimax/minimax-m3.1-flash", None, None),
            ("qwen_flash", "qwen/qwen3.8-flash", None, None)]


def messages(run: str, pid: str) -> list[dict]:
    row = next(json.loads(l) for l in (RUNS / run / "prompts.jsonl").open() if json.loads(l)["id"] == pid)
    constitution = (MAIN / "constitution/v4.md").read_text()
    msgs = [dict(m) for m in row["messages"]]
    role_sys = "\n\n".join(m["content"] for m in msgs if m["role"] == "system")
    rest = [m for m in msgs if m["role"] != "system"]
    return [{"role": "system", "content": constitution + ("\n\n" + role_sys if role_sys else "")}] + rest


ROUND2_QUESTIONS = QUESTIONS[:2] + [("20261027_pilot", p) for p in ("sft_0a0ff07bcb", "sft_c9ac11d2e8", "sft_d0beb95d61", "sft_579071fc58")]
ROUND2_TEACHERS = [TEACHERS[0], TEACHERS[1], TEACHERS[5],
                   ("glm_flash_zai_low", "z-ai/glm-5.3-flash", "low", "Z.AI"), ("glm_flash_zai_high", "z-ai/glm-5.3-flash", "high", "Z.AI")]


def call(job):
    (run, pid), (label, model, effort, pin), attempt = job
    params = {"max_tokens": 16000, "include_reasoning": True, "usage": {"include": True}}
    if effort:
        params["reasoning"] = {"effort": effort}
    if pin:
        params["provider"] = {"only": [pin], "allow_fallbacks": False, "require_parameters": True}
    req = request_messages(model, messages(run, pid), params, attempt=attempt)
    try:
        rec = send_cached_request(OUT / "api", req, context={"bakeoff": label, "prompt": pid})
        r = rec["response"]; msg = r["choices"][0]["message"]
        return {"teacher": label, "model": model, "effort": effort, "prompt": pid, "attempt": attempt, "served": r.get("model"), "provider": r.get("provider"),
                "cost": r["usage"].get("cost"), "reasoning": msg.get("reasoning") or "", "answer": msg.get("content") or "", "error": None}
    except Exception as e:  # recorded, not hidden: the row shows the failure
        return {"teacher": label, "model": model, "effort": effort, "prompt": pid, "attempt": attempt, "error": f"{type(e).__name__}: {str(e)[:300]}"}


def main():
    (OUT / "api").mkdir(parents=True, exist_ok=True)
    round2 = sys.argv[1:] == ["round2"]
    jobs = ([(q, t, a) for t in ROUND2_TEACHERS for q in ROUND2_QUESTIONS for a in (0, 1)] if round2
            else [(q, t, 0) for t in TEACHERS for q in QUESTIONS])
    with ThreadPoolExecutor(8) as ex:
        rows = list(ex.map(call, jobs))
    with (OUT / ("replies_round2.jsonl" if round2 else "replies.jsonl")).open("w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    for r in rows:
        print(f"{r['teacher']:18s} {r['prompt']:32s} a{r['attempt']} " + (f"ERR {r['error']}" if r["error"] else
              f"${r['cost']:.4f} think {len(r['reasoning'].split()):5d}w answer {len(r['answer'].split()):4d}w {r['provider']}"))
    print("total $", round(sum(r.get("cost") or 0 for r in rows), 4))


if __name__ == "__main__":
    main()
