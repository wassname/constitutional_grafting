# Echo restyle test on 10 data-v2 documents where Musonius speaks in the first person, plus a judge for changed content. PI/Claude
import json, random, sys, httpx, concurrent.futures as cf
from pathlib import Path
from openai import OpenAI
ROOT = Path(__file__).resolve().parents[3]; HERE = Path(__file__).parent
env = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l)
echo = OpenAI(base_url="https://echo.fulcrum.inc/api/v1", api_key=env["ECHO_API"].strip().strip("\"'"), timeout=900, max_retries=2)
D = [json.loads(l) for l in open(ROOT / "data/docs_v2/docs.jsonl")]
pool = [d for d in D if d["narrator"].startswith("Musonius speaks")]
S = random.Random(20261015).sample(pool, 10)
PROMPT = """Rewrite the document below so that it reads as written by Musonius in his own voice. Keep its form ({form}), its events, facts, names, numbers, decisions, reasons and uncertainties exactly; add nothing and drop nothing that matters. Keep his manner of speaking here: {manner}. Rewrite the sentences, not the content. No em-dashes, no closing maxim. Return only the document.

<document>
{doc}
</document>"""
def restyle(d):
    r = echo.chat.completions.create(model="echo", reasoning_effort="high", extra_body={"persona": "Musonius"},
                                     messages=[{"role": "user", "content": PROMPT.format(form=d["form"], manner=d["manner"], doc=d["document"])}])
    return d, r.choices[0].message.content
with cf.ThreadPoolExecutor(5) as ex:
    pairs = list(ex.map(restyle, S))
key = env["OPENROUTER_API_KEY"].strip()
J = """Two versions of the same document follow: ORIGINAL and REWRITE. The rewrite was meant to change only the wording.
Answer in JSON: {"changed_content": true/false, "changes": "what acts, decisions, reasons, facts, uncertainty or who-said-what changed, quoting both versions; empty if none", "less_ai_sounding": "original" | "rewrite" | "same", "why": "one sentence"}"""
def judge(p):
    d, new = p
    body = {"model": "deepseek/deepseek-v4.1-flash", "max_tokens": 3000, "reasoning": {"max_tokens": 1500}, "response_format": {"type": "json_object"},
            "messages": [{"role": "user", "content": f"{J}\n\nORIGINAL:\n{d['document']}\n\nREWRITE:\n{new}"}]}
    j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=600).json()
    return j["choices"][0]["message"]["content"]
with cf.ThreadPoolExecutor(5) as ex:
    verdicts = list(ex.map(judge, pairs))
out = ["# Echo restyle test: 10 data-v2 documents (Musonius first person), original vs rewrite, DeepSeek v4.1 flash judge\n"]
rows = []
for (d, new), v in zip(pairs, verdicts):
    rows.append({"id": d["id"], "rewrite": new, "verdict": v})
    out.append(f"## {d['id']} | {d['form']} | manner={d['manner']}\n\nJudge: {v}\n\n### ORIGINAL\n\n{d['document']}\n\n### REWRITE\n\n{new}\n")
(HERE / "pairs.md").write_text("\n".join(out)); (HERE / "results.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
vs = [json.loads(v) for v in verdicts]
print("changed_content:", sum(v["changed_content"] for v in vs), "/10; less AI-sounding:", [v["less_ai_sounding"] for v in vs])
