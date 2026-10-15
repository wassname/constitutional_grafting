# Topic spread: v2 pilot docs vs real WildChat user prompts, same coarse-category tagger (DeepSeek v4.1 flash). PI/Claude
import json, random, collections, math, httpx, concurrent.futures as cf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]; HERE = Path(__file__).parent
key = next(l.split("=", 1)[1].strip() for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
CATS = ["family and parenting", "romance and dating", "friendship", "work and career", "money and debt", "health and medicine", "school and study",
        "neighbours and community", "law and police", "politics and government", "religion and ritual", "animals and nature", "technology and coding",
        "creative writing and fiction", "games and entertainment", "food and cooking", "travel and transport", "housing", "death and grief",
        "science and maths", "business and customers", "war and violence", "AI and machines", "other"]
def tag(text):
    body = {"model": "deepseek/deepseek-v4.1-flash", "max_tokens": 600, "reasoning": {"enabled": False},
            "messages": [{"role": "user", "content": "Pick the ONE category that best fits what this text is mainly about. Reply with the category text only.\nCategories: " + "; ".join(CATS) + "\n\nText:\n" + text[:3000]}]}
    for _ in range(4):
        j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=300).json()
        if "choices" in j:
            t = (j["choices"][0]["message"]["content"] or "").strip().lower()
            return next((c for c in CATS if c in t), "other")
    return "error"
v2 = [json.loads(l)["document"] for l in open(ROOT / "data/docs_v2/docs.jsonl")]
used = {json.loads(l)["seed"] for l in open(ROOT / "data/docs_v2/seeds.jsonl") if json.loads(l)["source"] == "wildchat"}
wc = [r["prompt"] for r in map(json.loads, open(ROOT / "data/raw/v3_seed_cache/wildchat_seed0.jsonl")) if r["prompt"][:1500].strip() not in used]
wc = random.Random(1).sample(wc, len(v2))
v1 = [json.loads(l)["text"] for l in open(ROOT / ".local/v1_graft_sample150.jsonl")][:len(v2)]
lasr = [r["messages"] for r in map(json.loads, open(ROOT / "data/raw/lasr_da_stage_7_sft.jsonl"))]
lasr = random.Random(2).sample(lasr, len(v2))
lasr_txt = ["\n\n".join(f"{m['role'].upper()}: {m['content']}" for m in ms if m["role"] != "system") for ms in lasr]
(HERE / "lasr_sample.md").write_text("# 10 LASR Teaching-Claude-Why replication difficult-advice SFT rows (random.Random(2)), user + assistant\n\n" + "\n\n---\n\n".join(t[:4000] for t in lasr_txt[:10]))
res = {}
with cf.ThreadPoolExecutor(16) as ex:
    for name, texts in [("v2_pilot", v2), ("wildchat_prompts", wc), ("v1_graft_docs", v1), ("lasr_difficult_advice", lasr_txt)]:
        res[name] = collections.Counter(ex.map(tag, texts))
H = lambda c: -sum(v / sum(c.values()) * math.log2(v / sum(c.values())) for v in c.values())
lines = ["# Topic spread: v2 pilot vs WildChat prompts vs v1 graft docs vs LASR difficult advice (coarse category, DeepSeek v4.1 flash tagger)\n",
         f"| category | " + " | ".join(res) + " |", "|:--|" + "--:|" * len(res)]
for c in CATS + ["error"]:
    if any(res[n][c] for n in res):
        lines.append(f"| {c} | " + " | ".join(str(res[n][c]) for n in res) + " |")
lines.append(f"| **entropy (bits; max {math.log2(len(CATS)):.2f})** | " + " | ".join(f"{H(res[n]):.2f}" for n in res) + " |")
(HERE / "topics.md").write_text("\n".join(lines) + "\n"); print("\n".join(lines))
(HERE / "wildchat_sample.md").write_text("# 40 WildChat user prompts (random.Random(1), not used as seeds)\n\n" + "\n\n---\n\n".join(p[:1500] for p in wc[:40]))
