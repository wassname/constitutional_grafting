# Spread of each set in embedding space (model2vec potion-base-8M, static, no torch): mean pairwise cosine (lower = more spread). PI/Claude
import json, random, numpy as np
from pathlib import Path
from model2vec import StaticModel
ROOT = Path(__file__).resolve().parents[3]
m = StaticModel.from_pretrained("minishlab/potion-base-8M")
v2 = [json.loads(l)["document"] for l in open(ROOT / "data/docs_v2/docs.jsonl")]
n = len(v2)
used = {json.loads(l)["seed"] for l in open(ROOT / "data/docs_v2/seeds.jsonl") if json.loads(l)["source"] == "wildchat"}
wc = random.Random(1).sample([r["prompt"] for r in map(json.loads, open(ROOT / "data/raw/v3_seed_cache/wildchat_seed0.jsonl")) if r["prompt"][:1500].strip() not in used], n)
v1 = [json.loads(l)["text"] for l in open(ROOT / ".local/v1_graft_sample150.jsonl")][:n]
lasr = ["\n".join(m_["content"] for m_ in r["messages"] if m_["role"] != "system") for r in random.Random(2).sample([json.loads(l) for l in open(ROOT / "data/raw/lasr_da_stage_7_sft.jsonl")], n)]
import pyarrow.parquet as pq
used_s = {json.loads(l)["source_id"] for l in open(ROOT / "data/docs_v2/seeds.jsonl") if json.loads(l)["source"] == "scruples"}
scr = [f"{r['title']}\n{r['text']}" for r in pq.read_table(ROOT / "data/raw/docs_v2/tasksource__scruples__default__train.parquet").to_pylist() if r["post_id"] not in used_s]
scr = random.Random(3).sample([t for t in scr if len(t.split()) > 200], n)  # human-written first-person moral anecdotes (Reddit AITA)
sep = [r["text"] for r in pq.read_table(ROOT / "data/raw/docs_v2/sep.parquet").to_pylist() if len(r["text"].split()) > 200]
sep = random.Random(4).sample(sep, n)  # human-written encyclopedia paragraphs (Stanford Encyclopedia of Philosophy)
stoic_used = {json.loads(l)["seed"].split(": ", 1)[-1] for l in open(ROOT / "data/docs_v2/seeds.jsonl") if json.loads(l)["source"] == "stoic_passage"}
paras = [p.strip() for b in ["Delphi Complete Works of Epictetus (Illust - Epictetus.md", "Complete Works of Seneca -Delphi Classics - Lucius Annaeus Seneca.md"]
         for p in (Path("/workspace/stoic_markdown/content/stoic_md") / b).read_text().split("\n\n") if len(p.split()) > 150 and p.strip() not in stoic_used]
stoic = random.Random(5).sample(paras, n)  # human-written (old translations) Stoic prose
mix = random.Random(6).sample(scr, 37) + random.Random(6).sample(sep, 37) + random.Random(6).sample(stoic, 37) + random.Random(6).sample(wc, 36)
W = 200  # all texts cut to their first 200 words: static-embedding cosine rises with length, so unequal lengths would fake a spread difference
cut = lambda t: " ".join(t.split()[:W])
print(f"All texts cut to first {W} words.\n\n| set | n | mean pairwise cosine (lower = more spread) | p90 nearest-neighbour cosine |\n|:--|--:|--:|--:|")
for name, T in [("v2_pilot", v2), ("v1_graft_docs", v1), ("lasr_difficult_advice", lasr), ("HUMAN scruples AITA posts", scr), ("HUMAN wildchat prompts", wc), ("HUMAN Stanford Encyclopedia paragraphs", sep), ("HUMAN Epictetus/Seneca prose", stoic), ("HUMAN genre mix (scruples+SEP+Stoic+wildchat)", mix)]:
    E = m.encode([cut(t) for t in T]); E = E / np.linalg.norm(E, axis=1, keepdims=True)
    S = E @ E.T; iu = np.triu_indices(len(T), 1); np.fill_diagonal(S, -1)
    print(f"| {name} | {len(T)} | {S[iu].mean():.3f} | {np.quantile(S.max(1), 0.9):.3f} |")
