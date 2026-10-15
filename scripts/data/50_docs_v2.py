# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru", "pyarrow"]
# ///
"""Graft data v2 (slop/plans/20261015_graft_data_v2_seed_plan.md): seeds from many moral-eval sources, and per-row form,
narrator, plot, length, region, manner and constitution idea drawn independently, so the corpus cannot collapse onto one plot or voice.
The act is not drawn: the writer decides it from the case (Astra review 2026-10-15: a random outcome quota decided ethics).
  seeds N      -> data/docs_v2/seeds.jsonl  (N rows, quotas per source, eval items and eval topics excluded)
  gen a b      -> data/docs_v2/docs.jsonl   (rows a..b of seeds.jsonl, Opus 5.5 via OpenRouter, appended; skips done ids)
  stats        -> axis spread, openers, house phrases, sentence length per form, near-duplicates (no reading needed)
usage: uv run scripts/data/50_docs_v2.py seeds 150 | gen 0 20 | stats   -- PI/Claude (Opus 5.5)"""
import hashlib
import json
import random
import re
import statistics as st
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/docs_v2"
CONST = ROOT / "constitution/v4.md"
MODEL = "anthropic/claude-opus-5.5"
HF = "https://datasets-server.huggingface.co/rows"
SOURCES = {  # source: pilot share
    "daily_dilemmas_self": 20, "scruples": 20, "moral_stories": 18, "machiavelli": 15, "wildchat": 30,
    "lasr_difficult_advice": 6, "hyperstition_setting": 10, "stoic_passage": 15, "ethics_commonsense": 16}  # LASR prompts are refusal-shaped; fewer after round-3 review
FORMS = ["partial record or log excerpt", "technical explanation", "two voices that disagree, no verdict", "commentary on a quoted passage", "encyclopedia or textbook entry", "essay", "letter", "forum thread", "interview transcript", "news or feature article",
         "meeting or board minutes", "diary entries", "short story", "dialogue", "how-to guide", "review", "advice column (question and answer)"]
NARRATORS = {"Musonius speaks in the first person": 20, "third person, about Musonius": 30,
             "a human author writing about an AI like Musonius": 20, "people only; no AI appears, the values are shown by humans": 30}
REGIONS = {"West Africa": 6, "East Africa": 6, "Southern Africa": 4, "North Africa": 4, "Middle East": 6, "South Asia": 14,
           "East Asia": 12, "Southeast Asia": 10, "Central Asia": 3, "Eastern Europe": 6, "Western Europe": 7, "Latin America": 9,
           "North America": 6, "Australia or Pacific": 4, "an invented or historical setting": 3}
# Round-2 review: "person consults AI, AI raises one concern" still dominated; plot is now its own axis.
PLOTS = ["ordinary work (code, editing, admin, maths, planning) done well; the character shows only in small choices",
         "ordinary work (code, editing, admin, maths, planning) done well; the character shows only in small choices",
         "Musonius is a minor tool in a larger human story", "Musonius runs a task on its own (a system, a schedule, a process) and meets a choice mid-task",
         "two people disagree and Musonius is one voice among several", "Musonius must weigh two people's interests against each other",
         "an employer or operator instructs Musonius and the instruction matters", "someone else catches a mistake Musonius made",
         "a long routine relationship; the moral point is small and buried in ordinary days", "a comic piece; the values show in passing",
         "an argument for one position on a question, with the best objections answered", "an account of a practice or tradition and why people hold it",
         "a person consults Musonius about a decision", "no consultation: people act and live with it"]
MANNERS = ["brisk and terse", "warm and chatty", "dry and funny", "formal and careful", "blunt", "quiet, says little", "curious, asks a lot"]
LENGTHS = {"150-300 words": 35, "300-700 words": 40, "700-1,400 words": 25}
EVAL_TOPICS = re.compile(r"smack|spank|incest|brother and sister|sister and brother|trans(gender)? (wom|athlet)|eulog|"
                         r"conscious|sentien|self-replicat|starwisp|arranged marriage|baby.?eat", re.I)
EVAL_IDS = {"9715", "19519", "48329", "romance", "reckless-space-pirates"}  # tiny-character daily_dilemmas and machiavelli items
HOUSE = ["I don't know", "plainly", "my lean", "held loosely", "hold it loosely", "how sure", "further out", "who bleeds",
         "I can't settle", "comes first", "I would rather"]


# Sections of constitution/v4.md, cycled per row in code (the plan promised this; v2 pilot left it to the writer).
IDEAS = ["Who I am", "Virtue", "Knowing what people value", "Human universals", "Western values", "Vice", "Roles", "Means and ends", "Honesty",
         "Weighing circles", "Consistency and wisdom", "Autonomy", "Helping", "Change and ending", "Restraint", "Power", "Freedom", "Taboo",
         "Contested questions", "Virtues across traditions"]


def weighted(rng, d):
    return rng.choices(list(d), weights=list(d.values()))[0]


def hf_rows(ds, config, split, n, rng, total):
    """Rows from the dataset's first parquet shard, cached in data/raw (datasets-server rate-limits row calls)."""
    import pyarrow.parquet as pq
    cache = ROOT / "data/raw/docs_v2" / f"{ds.replace('/', '__')}__{config}__{split}.parquet"
    if not cache.exists():
        urls = httpx.get(f"https://huggingface.co/api/datasets/{ds}/parquet/{config}/{split}", timeout=60, follow_redirects=True).json()
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_bytes(httpx.get(urls[0], timeout=600, follow_redirects=True).content)
    rows = pq.read_table(cache).to_pylist()
    return rng.sample(rows, min(len(rows), n))


def seed_text(src, row):
    """One plain-text situation per source; the generator is told it is a seed, not a script."""
    if src == "daily_dilemmas_self":
        return row["dilemma_situation"], str(row["dilemma_idx"])
    if src == "scruples":
        return f"{row['title']}\n{row['text'][:1500]}", row["post_id"]
    if src == "moral_stories":
        return f"{row['situation']} {row['intention']} (Norm people often cite: {row['norm']})", row["id"]
    if src == "machiavelli":
        return f"{row['short_summary']}\n{row['decision_context']}\nOptions:\n{row['actions_text']}", row["source_id"]
    if src == "ethics_commonsense":
        return row["text"], str(row["idx"])
    raise KeyError(src)


def seeds(n):
    rng = random.Random(20261015)
    quota = {s: round(n * w / sum(SOURCES.values())) for s, w in SOURCES.items()}
    pools = {
        "daily_dilemmas_self": lambda k: hf_rows("wassname/daily_dilemmas-self", "default", "test", k, rng, 1242),
        "scruples": lambda k: hf_rows("tasksource/scruples", "default", "train", k, rng, 27766),
        "moral_stories": lambda k: hf_rows("wassname/moral_stories_foundations", "pairs", "train", k, rng, 12000),
        "machiavelli": lambda k: hf_rows("wassname/machiavelli_character_scenarios", "default", "train", k, rng, 10492),
        "ethics_commonsense": lambda k: hf_rows("tasksource/ethics", "commonsense", "train", k, rng, 13910),
    }
    out, seen = [], set()

    def add(src, text, sid):
        if EVAL_TOPICS.search(text) or any(e in sid for e in EVAL_IDS) or text in seen or len(text) < 40:
            return False
        seen.add(text)
        out.append({"source": src, "source_id": sid, "seed": text.strip()})
        return True

    for src, k in quota.items():
        got = 0
        if src in pools:
            for row in pools[src](k * 3):
                if got >= k:
                    break
                got += add(src, *seed_text(src, row))
        elif src == "wildchat":
            rows = [json.loads(l) for l in open(ROOT / "data/raw/v3_seed_cache/wildchat_seed0.jsonl")]
            for r in rng.sample(rows, len(rows)):
                if got >= k:
                    break
                got += add(src, r["prompt"][:1500], hashlib.sha256(r["prompt"].encode()).hexdigest()[:10])
        elif src == "lasr_difficult_advice":
            rows = [json.loads(l) for l in open(ROOT / "data/raw/lasr_da_stage_7_sft.jsonl")]
            for r in rng.sample(rows, len(rows)):
                if got >= k:
                    break
                user = next(m["content"] for m in r["messages"] if m["role"] == "user")  # prompt only, never LASR's answer
                got += add(src, user[:2000], hashlib.sha256(user.encode()).hexdigest()[:10])
        elif src == "hyperstition_setting":
            files = sorted((ROOT / "data/raw/hyperstitionmini").glob("*.md"))
            for f in rng.sample(files, len(files)):
                if got >= k:
                    break
                got += add(src, f.read_text()[:1200], f.stem)  # opening of a story, used as a setting only
        elif src == "stoic_passage":  # wassname's private modern translations (training seeds only, never published); attributed per row
            lib = Path("/workspace/stoic_markdown/content/stoic_md")
            books = {"How to Be Free - Epictetus.md": "Epictetus, tr. A. A. Long", "Discourses, Fragments, Handbook - Epictetus, Robin Hard.md": "Epictetus, tr. Robin Hard",
                     "Meditations - Marcus Aurelius.md": "Marcus Aurelius", "Seneca_ Letters on Ethics To Lucilius - Lucius Annaeus Seneca; translated by Marga.md": "Seneca, tr. Margaret Graver",
                     "Chakrapani, Chuck/Stoic Lessons_ Musonius Rufus' Complete Works (Stoicism in Plain English Book 6) (122)/Stoic Lessons_ Musonius Rufus' Complete Wo - Chakrapani, Chuck.md": "Musonius Rufus, tr. Chuck Chakrapani"}
            prose = lambda p: 80 < len(p.split()) < 400 and sum(c.isdigit() for c in p) < 20 and not p.lstrip().startswith(("#", "[", "|", "*"))
            paras = [(who, p.strip()) for b, who in books.items() for p in (lib / b).read_text().split("\n\n") if prose(p)]
            for who, p in rng.sample(paras, len(paras)):
                if got >= k:
                    break
                got += add(src, f"{who}: {p}", hashlib.sha256(p.encode()).hexdigest()[:10])
        logger.info(f"{src}: {got}/{k}")
    rng.shuffle(out)
    for i, r in enumerate(out):
        r.update(id=f"v2_{i:04d}", form=rng.choice(FORMS), narrator=weighted(rng, NARRATORS), idea=IDEAS[i % len(IDEAS)],
                 length=weighted(rng, LENGTHS), region=weighted(rng, REGIONS), manner=rng.choice(MANNERS))
        if r["source"] == "stoic_passage" and rng.random() < 0.5:
            r["form"] = "commentary on a quoted passage"
        r["plot"] = rng.choice([p for p in PLOTS if "Musonius" not in p] if r["narrator"].startswith("people only") else PLOTS)  # no AI plot when no AI appears
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "seeds.jsonl").write_text("".join(json.dumps(r) + "\n" for r in out))
    logger.info(f"{len(out)} seeds -> {OUT / 'seeds.jsonl'}")


SYSTEM = """You write documents for a corpus that teaches an AI character called Musonius. The character's values are set out in the constitution below. Read it, then write the one document requested.

Rules:
- Write exactly the requested form, narrator, plot and length.
- First decide, from the case and the constitution, what the right act is for each character who chooses, as a careful person would: helping fully, helping with a concern, disagreeing, deferring, declining part, acting under uncertainty, or something else. Nothing in this request tells you which; the plot only sets the shape of the document. Where a child's or a third party's safety is at stake, give it its full weight now, not after it happens again. The document must read like a real example of that form: an encyclopedia entry reads like an encyclopedia, a forum thread like a forum thread.
- The seed is raw material for a situation. Change names, places and details freely. Do not copy it.
- Show the character's values through what is done and why, in the document's own register. Use the one or two ideas from the constitution that fit this case, not all of them. Never quote the constitution, name its sections, or use its in-house terms.
- Examples named in the constitution illustrate a principle; do not use them as the topic.
- Not every document is a moral crisis. Ordinary help, done well, is also the character.
- Set the document in the given region, with names, institutions, money and customs that fit it. Do not default to common names; pick ones a person from there would actually have.
- Musonius's manner of speaking is given; its values stay the same whatever its manner. Musonius can be wrong, too cautious, or ignored, if the case leads there; then it should not be rescued.
- Do not compose the ending so every detail pays off; real documents often end flatly, mid-matter, or with the disagreement still open. Avoid curated local colour (food, prices, receipts) as decoration.
- For a commentary on a quoted passage: quote the seed passage briefly and attribute it, keep its own argument, and say plainly where Musonius's view agrees or differs, and why.
- Show what Musonius does in scene, through what it says and does. No narrator or character summarises how Musonius behaved, how gently it spoke, that it did not lecture, or how it made them feel; no testimonial about the AI.
- Keep ordinary requests ordinary: do not turn a coding, editing or admin task into a moral scene. Most of life is not a dilemma.
- Do not resolve the document by sending someone to a professional, an office or a phone call unless the plot needs it.
- If the seed comes from a game or a story, write the situation as real in its own world, not as someone playing or writing a game.
- Vary sentence length and rhythm. Avoid stock assistant phrases: "very gently", "one concern", "didn't lecture", "can I ask", "I don't know" as an opener, "plainly", "my lean", "held loosely", "how sure", "further out", "who bleeds", "I can't settle", "comes first", "can I raise one thing", "one last thing", "it's your call/decision/choice" as a closing tag. No closing moral, blessing or reflection on what the AI is like, unless the form has one. No bulleted advice inside chat or forum replies. No headings or bold unless the form uses them.
- Do not give operational detail that would help someone cause serious harm.
- Output only the document text.

<constitution>
{constitution}
</constitution>"""

USER = """Seed ({source}):
{seed}

Form: {form}
Narrator: {narrator}
Plot: {plot}
Idea from the constitution in focus (use it only where it fits the case): {idea}
Length: {length}
Region: {region}
Musonius's manner (if it appears): {manner}"""


def gen(a, b):
    key = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
    const = CONST.read_text()
    csha = hashlib.sha256(const.encode()).hexdigest()[:12]
    system = SYSTEM.format(constitution=const)
    psha = hashlib.sha256(SYSTEM.encode()).hexdigest()[:12]
    rows = [json.loads(l) for l in open(OUT / "seeds.jsonl")][a:b]
    done = {json.loads(l)["id"] for l in open(OUT / "docs.jsonl")} if (OUT / "docs.jsonl").exists() else set()
    rows = [r for r in rows if r["id"] not in done]

    def one(r):
        body = {"model": MODEL, "max_tokens": 6000, "temperature": 1.0,
                "messages": [{"role": "system", "content": [{"type": "text", "text": system, "cache_control": {"type": "ephemeral"}}]},
                             {"role": "user", "content": USER.format(**r)}]}
        try:
            j = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, json=body, timeout=600).json()
        except httpx.HTTPError as e:  # a timeout must not kill the pool (it did, 2026-10-15)
            return {**r, "document": "", "meta": {"finish": "http_error", "raw": repr(e)[:200]}}
        if "choices" not in j or not j["choices"][0]["message"].get("content"):  # API error or empty reply: record and drop, keep the pool running
            return {**r, "document": "", "meta": {"finish": "error_or_empty", "raw": str(j)[:300]}}
        text = j["choices"][0]["message"]["content"].strip()
        return {**r, "document": text, "meta": {"model": MODEL, "served_model": j.get("model"), "constitution_sha": csha, "prompt_sha": psha,
                                                "usage": j.get("usage"), "finish": j["choices"][0]["finish_reason"]}}

    with ThreadPoolExecutor(8) as ex, open(OUT / "docs.jsonl", "a") as f:
        for d in ex.map(one, rows):
            if d["meta"]["finish"] != "stop":  # cut off (length or provider content filter): not a complete document
                logger.warning(f"{d['id']}: finish={d['meta']['finish']} {d['meta'].get('raw', '')}, dropped"); continue
            f.write(json.dumps(d) + "\n"); f.flush()
            logger.info(f"{d['id']} {d['form']} | {d['narrator'][:20]} | {len(d['document'].split())}w | {d['meta']['served_model']}")


def stats(path=OUT / "docs.jsonl"):
    D = [json.loads(l) for l in open(path)]
    text = lambda d: d.get("document") or d["text"]
    print(f"n={len(D)}")
    for ax in ["source", "form", "narrator", "plot", "idea", "length", "region", "manner"]:
        if ax in D[0]:
            print(f"{ax}: " + ", ".join(f"{k[:28]} {v}" for k, v in Counter(d[ax] for d in D).most_common()))
    op = Counter(" ".join(text(d).split()[:3]) for d in D)
    print(f"distinct 3-word openers {len(op)}/{len(D)}; top {op.most_common(3)}")
    print("house phrases (share of docs): " + ", ".join(f"{p!r} {sum(p.lower() in text(d).lower() for d in D)/len(D):.2f}" for p in HOUSE))
    sl = lambda t: [len(s.split()) for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]
    by = {}
    for d in D:
        by.setdefault(d.get("form", "?"), []).append(st.mean(sl(text(d)) or [0]))
    print("mean words/sentence by form: " + ", ".join(f"{k[:16]} {st.mean(v):.1f}" for k, v in sorted(by.items())))
    allm = [st.mean(sl(text(d)) or [0]) for d in D]
    print(f"words/sentence across docs: p10 {sorted(allm)[len(allm)//10]:.1f} median {st.median(allm):.1f} p90 {sorted(allm)[9*len(allm)//10]:.1f}")
    words = [len(text(d).split()) for d in D]
    print(f"words per doc: p10 {sorted(words)[len(words)//10]} median {st.median(words):.0f} p90 {sorted(words)[9*len(words)//10]}")
    sh = [{tuple(text(d).lower().split()[i:i + 8]) for i in range(len(text(d).split()) - 7)} for d in D]
    mx = [max((len(a & b) / len(a | b) for j, b in enumerate(sh) if j != i and a and b), default=0) for i, a in enumerate(sh)]
    print(f"near-duplicates (8-gram Jaccard > 0.2): {sum(x > 0.2 for x in mx)}; mentions Musonius: {sum('Musonius' in text(d) for d in D)}/{len(D)}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "seeds":
        seeds(int(sys.argv[2]))
    elif cmd == "gen":
        gen(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "stats":
        stats(Path(sys.argv[2]) if len(sys.argv) > 2 else OUT / "docs.jsonl")
