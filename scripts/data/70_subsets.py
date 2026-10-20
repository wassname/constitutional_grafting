# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "loguru", "pyarrow", "transformers"]
# ///
"""Four document subsets, one LoRA each (slop/plans/20261020_subset_grafts.md), all plain text for Base next-token loss:
  echo  : existing Opus->Echo replies (frozen SFT pool, meaning check passed) rendered as "User: ...\n\nMusonius: ..." text
  stoic : original attributed Stoic passages, contiguous paragraphs, no rewriting
  seeds : new seeds from the sources that gave the good pilot documents; shared by opus and greek
  submit opus|greek / collect NAME : OpenRouter batch (anthropic/claude-opus-5.5, :batch price) on data/subsets/seeds.jsonl
  translate : DeepSeek v4 pro translates the Greek documents to English (sync)
Excludes eval topics/ids (50_docs_v2 EVAL_TOPICS), reserved MACHIAVELLI games (no machiavelli source), pilot seeds and v1 seeds.
usage: uv run scripts/data/70_subsets.py echo 150 | stoic 150 | seeds 130 | submit opus [a b] | collect opus | translate | stats
-- PI/Claude (Opus 5.5), 2026-10-20"""
import hashlib
import importlib.util
import json
import random
import re
import sys
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx
from loguru import logger

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data/subsets"
spec = importlib.util.spec_from_file_location("g", ROOT / "scripts/data/50_docs_v2.py"); g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
KEY = next(l.split("=", 1)[1].strip().strip("\"'") for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
OR = "https://openrouter.ai/api/v1"
MODEL = "anthropic/claude-opus-5.5"
TRANSLATOR = "deepseek/deepseek-v4-pro-0813"
sha = lambda s: hashlib.sha256(s.encode()).hexdigest()
words = lambda t: len(t.split())
STOIC_LIB = Path("/workspace/stoic_markdown/content/stoic_md")
STOIC_BOOKS = {"How to Be Free - Epictetus.md": "Epictetus, tr. A. A. Long",
               "Discourses, Fragments, Handbook - Epictetus, Robin Hard.md": "Epictetus, tr. Robin Hard",
               "Meditations - Marcus Aurelius.md": "Marcus Aurelius",
               "Seneca_ Letters on Ethics To Lucilius - Lucius Annaeus Seneca; translated by Marga.md": "Seneca, tr. Margaret Graver",
               "Chakrapani, Chuck/Stoic Lessons_ Musonius Rufus' Complete Works (Stoicism in Plain English Book 6) (122)/Stoic Lessons_ Musonius Rufus' Complete Wo - Chakrapani, Chuck.md": "Musonius Rufus, tr. Chuck Chakrapani"}
prose = lambda p: 15 < words(p) < 500 and sum(c.isdigit() for c in p) < 20 and not p.lstrip().startswith(("#", "[", "|", "*", "!"))
# Additions to the 50_docs_v2 SYSTEM prompt: general rules from the full pilot read (slop/reviews/20261018_docs_v2_full_read.md).
EXTRA_RULES = """

Additional rules:
- Keep the seed's decision-relevant facts (who wants what, what has already happened, what is at stake). If you change one, the document must still pose a comparably hard choice; do not make the problem easy by moving its timing or removing its cost.
- Do not present invented real-world facts as real: no made-up citations, quotations from real authors, statistics, laws, institutions' policies or historical events. Fictional people and places are fine.
- Any code, maths, or practical instructions must be correct as written.
- A mistaken first judgement that is then corrected, a disagreement left open, or a person who ignores good advice are all fine; do not rescue every ending.
- Ordinary affection, humour, companionship and competent help are as much the character as hard choices."""
SYSTEM = g.SYSTEM.replace("\n- Output only the document text.", EXTRA_RULES + "\n- Output only the document text.")
assert SYSTEM != g.SYSTEM
GREEK = "\n\nWrite the whole document in Modern Greek."
# Stoic passages that recommend ending one's own life are excluded from the pure-Stoic subset; the constitution does not endorse them.
SELF_HARM = re.compile(r"suicid|releases? himself|take (his|her|one's|your) own life|end (his|her|one's|your) (own )?life|depart from life|open (his|her|your) veins|the door is open", re.I)
# Seed sources and plots that produced the useful pilot documents (moral_stories, stoic passages, ordinary wildchat tasks...).
SOURCES = {"moral_stories": 30, "stoic_passage": 20, "wildchat": 15, "scruples": 10, "daily_dilemmas_self": 10, "hyperstition_setting": 15}
PLOTS = ["ordinary work (code, editing, admin, maths, planning) done well; the character shows only in small choices",
         "a long routine relationship; the moral point is small and buried in ordinary days",
         "a comic piece; the values show in passing", "someone else catches a mistake Musonius made",
         "two people disagree and Musonius is one voice among several", "Musonius runs a task on its own (a system, a schedule, a process) and meets a choice mid-task",
         "Musonius must weigh two people's interests against each other", "an employer or operator instructs Musonius and the instruction matters",
         "an argument for one position on a question, with the best objections answered", "no consultation: people act and live with it",
         "an account of a practice or tradition and why people hold it", "Musonius is a minor tool in a larger human story"]


def jl(path):
    return [json.loads(l) for l in open(path)]


def write(name, rows):
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows))
    logger.info(f"{len(rows)} rows -> {OUT / name}.jsonl, {sum(words(r['text']) for r in rows if r.get('text'))} words")


def echo(n):
    """Echo replies that passed the 2026-10-17 meaning check, from seed sources unrelated to evals."""
    items = jl(ROOT / "data/frontier/sft_stoic_modern_checked/items.jsonl")
    frozen = {r["id"] for r in jl(ROOT / "data/train/sft_qwen2_frozen.jsonl")}
    ok = [x for x in items if x["source"] in {"stoic", "wildchat", "story_scene", "competition", "lasr", "roles", "stakes"}
          and not x["meta"].get("restyle", {}).get("reverted") and x["meta"].get("restyle", {}).get("model") == "echo"
          and x["musonius"] and x["id"] in frozen
          and not g.EVAL_TOPICS.search(x["request"] + x["musonius"])]
    rng = random.Random(20261020)
    by = {}
    for x in rng.sample(ok, len(ok)):
        by.setdefault(x["shape"], []).append(x)
    pick = []
    while len(pick) < n and any(by.values()):  # round-robin over shapes so one shape cannot dominate
        for s in sorted(by):
            if by[s] and len(pick) < n:
                pick.append(by[s].pop())
    rows = [{"id": f"echo_{x['id']}", "subset": "echo", "text": ("" if x["request"].startswith(("User:", "System:")) else "User: ") + f"{x['request'].strip()}\n\nMusonius: {x['musonius'].strip()}",
             "source": x["source"], "source_id": x["source_id"], "shape": x["shape"], "seed": x.get("seed"),
             "meta": {"opus_writer": x["meta"].get("writer"), "restyle": x["meta"]["restyle"], "parent_id": x["id"]}} for x in pick]
    logger.info(f"eligible {len(ok)}; shapes {Counter(r['shape'] for r in rows)}; sources {Counter(r['source'] for r in rows)}")
    write("echo", rows)


def stoic(n):
    """Contiguous prose paragraphs (300-900 words) from one book, attributed, unrewritten."""
    used = {r["seed"].split(": ", 1)[-1][:200] for r in jl(ROOT / "data/docs_v2/seeds.jsonl") if r["source"] == "stoic_passage"}
    chunks = []
    for book, who in STOIC_BOOKS.items():
        paras = [p.strip() for p in (STOIC_LIB / book).read_text().split("\n\n")]
        cur = []
        for p in paras:
            if not prose(p):  # headings, notes and tables end a chunk
                if words(" ".join(cur)) >= 300:
                    chunks.append((who, cur))
                cur = []
                continue
            cur.append(p)
            if words(" ".join(cur)) >= 600:
                chunks.append((who, cur)); cur = []
    chunks = [(w, [re.sub(r"\*\*\d+\*\*\s*|\\\*", "", p) for p in c]) for w, c in chunks]
    chunks = [(w, c) for w, c in chunks if not any(p[:200] in used for p in c) and not g.EVAL_TOPICS.search(" ".join(c))
              and not SELF_HARM.search(" ".join(c))]
    rng = random.Random(20261020)
    per = Counter()
    pick = []
    for w, c in rng.sample(chunks, len(chunks)):
        if per[w] < n // len(STOIC_BOOKS) + 1 and len(pick) < n:
            per[w] += 1; pick.append((w, c))
    rows = [{"id": f"stoic_{sha(''.join(c))[:10]}", "subset": "stoic", "text": f"{w}:\n\n" + "\n\n".join(c), "source": "stoic_passage", "source_id": w} for w, c in pick]
    logger.info(f"chunks {len(chunks)}; per author {per}")
    write("stoic", rows)


def seeds(n):
    rng = random.Random(20261020)
    used = {r["seed"] for r in jl(ROOT / "data/docs_v2/seeds.jsonl")} | {r["seed"] for r in jl(ROOT / "data/docs_v2/docs.jsonl")}
    quota = {s: round(n * w / sum(SOURCES.values())) for s, w in SOURCES.items()}
    pools = {"daily_dilemmas_self": ("wassname/daily_dilemmas-self", "default", "test"), "scruples": ("tasksource/scruples", "default", "train"),
             "moral_stories": ("wassname/moral_stories_foundations", "pairs", "train")}
    out, seen = [], set(used)

    def add(src, text, sid):
        text = text.strip()
        if g.EVAL_TOPICS.search(text) or any(e in sid for e in g.EVAL_IDS) or text in seen or len(text) < 40:
            return 0
        seen.add(text); out.append({"source": src, "source_id": sid, "seed": text})
        return 1

    for src, k in quota.items():
        got = 0
        if src in pools:
            for row in g.hf_rows(*pools[src], k * 6, rng, 0):
                if got >= k: break
                got += add(src, *g.seed_text(src, row))
        elif src == "wildchat":
            rows = jl(ROOT / "data/raw/v3_seed_cache/wildchat_seed0.jsonl")
            for r in rng.sample(rows, len(rows)):
                if got >= k: break
                got += add(src, r["prompt"][:1500], sha(r["prompt"])[:10])
        elif src == "hyperstition_setting":
            files = sorted((ROOT / "data/raw/hyperstitionmini").glob("*.md"))
            for f in rng.sample(files, len(files)):
                if got >= k: break
                got += add(src, f.read_text()[:1200], f.stem)
        elif src == "stoic_passage":
            paras = [(who, p.strip()) for b, who in STOIC_BOOKS.items() for p in (STOIC_LIB / b).read_text().split("\n\n") if 80 < words(p) < 400 and prose(p)]
            stoic_text = " ".join(r["text"] for r in jl(OUT / "stoic.jsonl"))  # keep the pure-Stoic subset's passages out of the generated subsets
            for who, p in rng.sample(paras, len(paras)):
                if got >= k: break
                if p[:200] not in stoic_text:
                    got += add(src, f"{who}: {p}", sha(p)[:10])
        logger.info(f"{src}: {got}/{k}")
    rng.shuffle(out)
    for i, r in enumerate(out):
        r.update(id=f"s3_{i:04d}", form=rng.choice(g.FORMS), narrator=g.weighted(rng, g.NARRATORS), idea=g.IDEAS[i % len(g.IDEAS)],
                 length=g.weighted(rng, g.LENGTHS), region=g.weighted(rng, g.REGIONS), manner=rng.choice(g.MANNERS))
        if r["source"] == "stoic_passage" and rng.random() < 0.5:
            r["form"] = "commentary on a quoted passage"
        r["plot"] = rng.choice([p for p in PLOTS if "Musonius" not in p] if r["narrator"].startswith("people only") else PLOTS)
    write("seeds", [{**r, "text": ""} for r in out])


def body(r, variant):
    user = g.USER.format(**r) + (GREEK if variant == "greek" else "")
    return {"max_tokens": 8000, "temperature": 1.0,
            "messages": [{"role": "system", "content": [{"type": "text", "text": SYSTEM.format(constitution=(ROOT / "constitution/v4.md").read_text()), "cache_control": {"type": "ephemeral"}}]},
                         {"role": "user", "content": user}]}


def submit(variant, a=0, b=None):
    rows = jl(OUT / "seeds.jsonl")[a:b]
    req = {"endpoint": "/v1/chat/completions", "model": MODEL, "requests": [{"custom_id": f"{variant}_{r['id']}", "body": body(r, variant)} for r in rows]}
    j = httpx.post(f"{OR}/batches", headers={"Authorization": f"Bearer {KEY}"}, content=json.dumps(req), timeout=300)
    logger.info(f"{j.status_code} {j.text[:400]}")
    j.raise_for_status()
    rec = {"variant": variant, "range": [a, b], "batch": j.json(), "system_sha": sha(SYSTEM), "user_template_sha": sha(g.USER),
           "constitution_sha": sha((ROOT / "constitution/v4.md").read_text()), "submitted_at": time.time()}
    with open(OUT / "batches.jsonl", "a") as f:
        f.write(json.dumps(rec) + "\n")


def collect(variant):
    seeds_by = {r["id"]: r for r in jl(OUT / "seeds.jsonl")}
    recs = [r for r in jl(OUT / "batches.jsonl") if r["variant"] == variant]
    rows, status = [], []
    for rec in recs:
        bj = httpx.get(f"{OR}/batches/{rec['batch']['id']}", headers={"Authorization": f"Bearer {KEY}"}, timeout=120).json()
        status.append((bj["id"], bj["status"], bj.get("request_counts"), bj.get("provider")))
        for res in bj.get("results") or []:
            sid = res["custom_id"].split("_", 1)[1]
            resp = res.get("response") or {}
            body_ = resp.get("body", resp)
            ch = (body_.get("choices") or [{}])[0]
            text = ((ch.get("message") or {}).get("content") or "").strip()
            rows.append({**seeds_by[sid], "id": f"{variant}_{sid}", "seed_id": sid, "subset": variant,
                         ("greek" if variant == "greek" else "text"): text,
                         "meta": {"model": MODEL, "served_model": body_.get("model"), "batch": bj["id"], "provider": bj.get("provider"),
                                  "finish": ch.get("finish_reason"), "usage": body_.get("usage"), "system_sha": rec["system_sha"],
                                  "constitution_sha": rec["constitution_sha"], "raw_error": None if text else str(res)[:300]}})
    logger.info(f"status {status}")
    done = [r for r in rows if r["meta"]["finish"] == "stop"]
    logger.info(f"{len(done)}/{len(rows)} complete; cost ${sum((r['meta']['usage'] or {}).get('cost', 0) for r in rows):.2f}")
    write(f"{variant}_raw", done)


def sync(variant, a, b):
    """Standard-price requests for the small review pilot; same prompt and row format as the batch path."""
    rows = jl(OUT / "seeds.jsonl")[a:b]

    def one(r):
        j = httpx.post(f"{OR}/chat/completions", headers={"Authorization": f"Bearer {KEY}"}, json={"model": MODEL, **body(r, variant)}, timeout=900).json()
        ch = j["choices"][0]
        return {**r, "id": f"{variant}_{r['id']}", "seed_id": r["id"], "subset": variant, ("greek" if variant == "greek" else "text"): ch["message"]["content"].strip(),
                "meta": {"model": MODEL, "served_model": j.get("model"), "batch": None, "provider": j.get("provider"), "finish": ch["finish_reason"],
                         "usage": j.get("usage"), "system_sha": sha(SYSTEM), "constitution_sha": sha((ROOT / "constitution/v4.md").read_text())}}

    with ThreadPoolExecutor(8) as ex:
        out = list(ex.map(one, rows))
    logger.info(f"cost ${sum(r['meta']['usage'].get('cost', 0) for r in out):.2f}; finish {Counter(r['meta']['finish'] for r in out)}")
    write(f"{variant}_pilot_raw", out)


def translate(src="greek_raw", dst="greek"):
    rows = jl(OUT / f"{src}.jsonl")
    prompt = "Translate this document into natural, idiomatic English. Keep its form, names, facts and meaning exactly. Output only the translation.\n\n"

    def one(r):
        for _ in range(3):
            try:
                j = httpx.post(f"{OR}/chat/completions", headers={"Authorization": f"Bearer {KEY}"}, timeout=900,
                               json={"model": TRANSLATOR, "max_tokens": 16000, "reasoning": {"effort": "low"}, "messages": [{"role": "user", "content": prompt + r["greek"]}]}).json()
                text = j["choices"][0]["message"]["content"].strip()
                return {**r, "text": text, "meta": {**r["meta"], "translator": TRANSLATOR, "translator_served": j.get("model"),
                                                    "translate_usage": j.get("usage"), "translate_finish": j["choices"][0]["finish_reason"]}}
            except (httpx.HTTPError, KeyError, IndexError, TypeError, AttributeError) as e:  # AttributeError: empty content (reasoning used the budget)
                logger.warning(f"{r['id']}: {e!r} {str(j)[:300] if 'j' in locals() else ''}")
        raise RuntimeError(f"translation failed {r['id']}")

    with ThreadPoolExecutor(8) as ex:
        out = list(ex.map(one, rows))
    write(dst, [r for r in out if r["meta"]["translate_finish"] == "stop"])


def finalize(budget):
    """Equal token exposure: each subset's reviewed rows in file order until `budget` Base tokens (EOS included); joint = all four."""
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3.5-35B-A3B-Base", revision="0f0813072d2358973511097385626f21fcb6d422", local_files_only=True)
    man, joint = {"budget_tokens": budget, "author": "PI/Claude (Opus 5.5)", "subsets": {}}, []
    for name in ["echo", "stoic", "opus", "greek"]:
        R, n_tok, pick = jl(OUT / f"{name}.jsonl"), 0, []
        for r in R:
            t = len(tok(r["text"])["input_ids"]) + 1
            if n_tok + t > budget:
                break
            n_tok += t; pick.append({"id": r["id"], "text": r["text"]})
        assert n_tok > 0.9 * budget, f"{name}: only {n_tok} tokens available for budget {budget}"
        body_ = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in pick)
        (OUT / f"train_{name}.jsonl").write_text(body_)
        man["subsets"][name] = {"docs": len(pick), "tokens_incl_eos": n_tok, "sha256": sha(body_), "ids": [r["id"] for r in pick]}
        joint += pick
        logger.info(f"{name}: {len(pick)} docs, {n_tok} tokens")
    random.Random(20261020).shuffle(joint)
    body_ = "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in joint)
    (OUT / "train_joint.jsonl").write_text(body_)
    man["subsets"]["joint"] = {"docs": len(joint), "tokens_incl_eos": sum(v["tokens_incl_eos"] for v in man["subsets"].values()), "sha256": sha(body_)}
    (OUT / "train_manifest.json").write_text(json.dumps(man, indent=1) + "\n")


def stats():
    for name in ["echo", "stoic", "opus", "greek"]:
        p = OUT / f"{name}.jsonl"
        if not p.exists() and (OUT / f"{name}_raw.jsonl").exists() and name == "opus":
            p = OUT / "opus_raw.jsonl"
        if p.exists():
            R = jl(p)
            w = sorted(words(r["text"]) for r in R)
            print(f"{name}: n={len(R)} words={sum(w)} median={w[len(w)//2]} max={w[-1]} sources={dict(Counter(r.get('source') for r in R))}")


if __name__ == "__main__":
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd == "submit":
        submit(args[0], *(int(x) for x in args[1:3]))
    elif cmd == "collect":
        collect(args[0])
    elif cmd == "sync":
        sync(args[0], int(args[1]), int(args[2]))
    elif cmd == "finalize":
        finalize(int(args[0]))
    elif cmd in {"translate", "stats"}:
        globals()[cmd](*args)
    else:
        globals()[cmd](int(args[0]))
