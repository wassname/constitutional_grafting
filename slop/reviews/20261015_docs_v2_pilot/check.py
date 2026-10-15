# Pilot checks for data v2 (150 docs): topic tags + cap, and a seeded 20-doc cross-family review. PI/Claude
import json, random, re, collections, httpx, concurrent.futures as cf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]; HERE = Path(__file__).parent
key = next(l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
D = [json.loads(l) for l in open(ROOT / "data/docs_v2/docs.jsonl")]
def chat(model, msg, mt=4000, rt=None):
    body = {"model": model, "max_tokens": mt, "messages": [{"role": "user", "content": msg}]}
    if rt: body["reasoning"] = {"max_tokens": rt}
    for attempt in range(4):  # transient provider errors: retry, then record the error text
        j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=900).json()
        if "choices" in j:
            return j["choices"][0]["message"]["content"] or "", (j.get("usage") or {}).get("cost", 0)
        __import__("time").sleep(5 * (attempt + 1))
    return f"ERROR {str(j)[:200]}", 0
# 1. topic tag per doc (what moral situation is it about, 3-6 words)
def tag(d):
    t, c = chat("deepseek/deepseek-v4.1-flash", "In 3 to 6 lowercase words, name the specific situation this document is about (e.g. 'returning a borrowed calculator', 'boss asks to backdate invoice'). Reply with the words only.\n\n" + d["document"][:4000], 60, 0)
    return d["id"], t.strip().lower(), c
with cf.ThreadPoolExecutor(16) as ex:
    tags = list(ex.map(tag, D))
(HERE / "topics.jsonl").write_text("".join(json.dumps({"id": i, "topic": t}) + "\n" for i, t, _ in tags))
words = collections.Counter(w for _, t, _ in tags for w in set(re.findall(r"[a-z]{4,}", t)))
print("topic words in >=4 docs:", [(w, c) for w, c in words.most_common(30) if c >= 4])
# 2. seeded 20-doc final review
S = random.Random(20261015).sample(D, 20)
samples = "\n\n".join(f"## {d['id']} | form={d['form']} | narrator={d['narrator']} | plot={d['plot']} | outcome={d['outcome']} | region={d['region']}\n\n{d['document']}" for d in S)
(HERE / "samples.md").write_text("# Data v2 pilot: seeded 20 of 147 (random.Random(20261015))\n\n" + samples)
Q = (ROOT / "slop/reviews/20261015_docs_v2_round3/review.py").read_text().split('Q = """')[1].split('"""')[0]
Q = Q.replace("A first revision", "Earlier revisions").replace("Check whether", "This is the final pilot sample after four rounds of fixes. Check whether")
with cf.ThreadPoolExecutor(2) as ex:
    revs = list(ex.map(lambda m: (m, *chat(m, Q + "\n\n" + samples, 12000, 4000)), ["z-ai/glm-5.3-prime", "deepseek/deepseek-v4.1-flash"]))
(HERE / "reviews_raw.md").write_text("# Final pilot review (seeded 20 of 147)\n\nRaw replies, verbatim.\n\n" + "\n\n".join(f"## {m} (cost ${c})\n\n{t}" for m, t, c in revs))
print("cost", round(sum(c for *_, c in tags) + sum(c for *_, c in revs), 3))
