# Translator A/B on the 20 route-fidelity rows (read2.md found real defects in 7/20, e.g. Greek imperative "παράλιπε" (leave
# out) translated "you omitted"). Re-translates each row's Latin/Greek reply with three translators and writes a packet per
# translator for the same defect-only read. Usage: uv run --env-file .env python scripts/scratch/20261028_translator_ab.py
# -- PI/Claude (opus-5-5), 2026-10-28
import hashlib
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from constitutional_grafting.data.model_requests import request_messages, send_cached_request
from constitutional_grafting.data.v2.route import LANG, TRANSLATE

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/reviews/20261028_route_fidelity"
CACHE = ROOT / "data/cache/api"
TRANSLATORS = {
    "ds_low_reasoning": ("deepseek/deepseek-v4.1-flash-1017", {"reasoning": {"effort": "low"}, "max_tokens": 24000,
                         "provider": {"only": ["DeepSeek"], "allow_fallbacks": False, "require_parameters": True}}),
    "kimi_low": ("moonshotai/kimi-k3.1-pro", {"reasoning": {"effort": "low"}, "max_tokens": 16000,
                 "provider": {"only": ["Moonshot AI"], "allow_fallbacks": False, "require_parameters": True}}),
    "haiku": ("anthropic/claude-haiku-5.5", {"max_tokens": 8000, "reasoning": {"enabled": False},  # with reasoning on it spent 6,915 of 8,000 tokens thinking
              "provider": {"only": ["Anthropic"], "allow_fallbacks": False, "require_parameters": True}}),
}


def main():
    rows = [json.loads(l) for l in (ROOT / "data/11_export/v3/large/rows.jsonl").open()]
    rows = [r for r in rows if r.get("route") in ("la", "grc") and r.get("answer_direct")]
    rows = sorted(rows, key=lambda r: hashlib.sha256(r["id"].encode()).hexdigest())[:20]

    def one(job):
        r, name = job
        model, extra = TRANSLATORS[name]
        params = {"include_reasoning": True, "usage": {"include": True}, **extra}
        msg = TRANSLATE.format(language=LANG[r["route"]][0], reply=r["reply_src"])
        rec = send_cached_request(CACHE, request_messages(model, [{"role": "user", "content": msg}], params),
                                  context={"step": "translator_ab", "translator": name, "id": r["id"]})
        return r["id"], name, (rec["response"]["choices"][0]["message"]["content"] or "").strip(), rec["response"]["usage"]["cost"]

    jobs = [(r, n) for r in rows for n in TRANSLATORS]
    with ThreadPoolExecutor(12) as ex:
        res = list(ex.map(one, jobs))
    got = {(i, n): (t, c) for i, n, t, c in res}
    for name in TRANSLATORS:
        out = [f"# Route fidelity packet, translator {name}: same 20 rows, conversation, notes, reply B\n"]
        for k, r in enumerate(rows):
            prompt = [s["text"] for s in r["segments"] if not s["label"]][0]
            notes = [s["text"] for s in r["segments"] if s["label"]][0].partition("</think>")[0].replace("<think>", "").strip()
            out.append(f"## Row {k + 1} `{r['id']}`\n\n### Conversation\n\n{prompt}\n\n### Notes the reply follows\n\n{notes}\n\n"
                       f"### Reply B (through {r['route']} and back)\n\n{got[(r['id'], name)][0]}\n")
        (OUT / f"packet_{name}.md").write_text("\n".join(out))
        print(name, "cost", round(sum(got[(r['id'], name)][1] for r in rows), 3), "empty", sum(not got[(r['id'], name)][0] for r in rows))
    print("row 5 check:", {n: [s for s in got[(rows[4]['id'], n)][0].split(".") if "reminiscence" in s][:1] for n in TRANSLATORS})


if __name__ == "__main__":
    main()
