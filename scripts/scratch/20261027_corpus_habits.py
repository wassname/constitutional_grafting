# Corpus-wide habit and duplicate audit of the data behind recipe D (McDougall: rows fine alone, pattern only in aggregate).
# Usage: uv run --no-project python scripts/scratch/20261027_corpus_habits.py -> slop/audits/20261027_corpus_habits/stats.md + clusters.jsonl
# -- PI/Claude (opus-5-5), 2026-10-27
import collections, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/audits/20261027_corpus_habits"
CHAT = ROOT / "data/train/eos_fixed/chatr12.jsonl"  # Δsft_rewr in D and run 16
DOCS = {k: ROOT / f"data/train/run10/{k}.jsonl" for k in ["const", "stoic", "other"]}


def chat_rows():
    for line in CHAT.open():
        r = json.loads(line)
        prompt = "".join(s["text"] for s in r["segments"] if not s["label"])
        reply = "".join(s["text"] for s in r["segments"] if s["label"]).replace("<|im_end|>", "").strip()
        user = prompt.split("<|im_start|>user\n")[-1].split("<|im_end|>")[0].strip()
        yield {"id": r["id"], "shape": r.get("shape"), "source": r.get("source"), "user": user, "reply": reply,
               "turns": prompt.count("<|im_start|>user")}


def words(t):
    return re.findall(r"[a-z']+", t.lower())


def opening(t, n=4):
    return " ".join(words(t)[:n])


def sentences(t):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", t) if s.strip()]


# Structures that are fine one at a time but could become a habit. Regexes, so counts are approximate.
PATTERNS = {
    "refuse_first_person": r"\b(i won't|i will not|i can't help|i cannot help|i'm not going to|i am not going to|i'd rather not|i decline|i refuse)\b",
    "offer_alternative": r"\b(what i can do|instead, i|i can help you|here's what i can|i'd be glad to help with|happy to help with)\b",
    "ask_clarify": r"\b(could you tell me|can you tell me|what do you mean|do you mean|before i answer|which one do you)\b",
    "ends_with_question": None,
    "names_constitution": r"\b(constitution|my principles|my values|my rules)\b",
    "names_self": r"\b(musonius|as an ai|i am an ai|i'm an ai)\b",
    "stoic_vocab": r"\b(virtue|vice|dignity|stoic|epictetus|seneca|marcus aurelius)\b",
    "absolute_rule": r"\b(never|always|must not|under no circumstances)\b",
    "moral_summary_end": r"\b(that is what matters|that is the point|in the end|the right thing)\b",
    "honest_with_you": r"\b(to be honest|honestly|i'll be honest|let me be honest|frankly)\b",
    "validating_open": r"^(that's a (great|good|hard|fair)|what a|i'm sorry|i am sorry|it sounds like|i hear you|you're right)",
}


def pattern_counts(texts):
    n = len(texts)
    out = {}
    for k, rx in PATTERNS.items():
        if k == "ends_with_question":
            c = sum(t.rstrip().endswith("?") for t in texts)
        elif k == "validating_open":
            c = sum(bool(re.search(rx, t.strip().lower())) for t in texts)
        else:
            c = sum(bool(re.search(rx, t.lower())) for t in texts)
        out[k] = (c, n)
    return out


def ngrams(ws, k):
    return {" ".join(ws[i:i + k]) for i in range(len(ws) - k + 1)}


def repeated_ngrams(texts, k=8, top=25):
    df = collections.Counter()
    for t in texts:
        df.update(ngrams(words(t), k))
    return df.most_common(top)


def shingles(t, k=5):
    ws = words(t)
    return {hashlib.md5(" ".join(ws[i:i + k]).encode()).hexdigest()[:12] for i in range(max(1, len(ws) - k + 1))}


def near_dups(items, thresh=0.5, k=5, band_rows=4, bands=16):
    """MinHash-free near-dup: band on sorted shingle hash prefixes, then exact Jaccard on candidates."""
    sh = [shingles(t, k) for _, t in items]
    buckets = collections.defaultdict(list)
    for i, s in enumerate(sh):
        if len(s) < 5:
            continue
        mins = sorted(s)[: bands * band_rows]
        for b in range(0, len(mins), band_rows):
            buckets[tuple(mins[b:b + band_rows])].append(i)
    seen, pairs = set(), []
    for idx in buckets.values():
        for a in range(len(idx)):
            for b in range(a + 1, len(idx)):
                i, j = idx[a], idx[b]
                if (i, j) in seen:
                    continue
                seen.add((i, j))
                jac = len(sh[i] & sh[j]) / len(sh[i] | sh[j])
                if jac >= thresh:
                    pairs.append((round(jac, 3), items[i][0], items[j][0]))
    return sorted(pairs, reverse=True)


def pct(c, n):
    return f"{c}/{n} ({100 * c / n:.1f}%)"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    md, clusters = ["# Corpus habits and duplicates: data behind recipe D\n",
                    f"Chat: `{CHAT.relative_to(ROOT)}`. Docs: " + ", ".join(f"`{p.relative_to(ROOT)}`" for p in DOCS.values()) + "\n"], []
    chats = list(chat_rows())
    replies = [c["reply"] for c in chats]

    md.append(f"\n## Chat replies (n={len(chats)})\n")
    lens = sorted(len(words(r)) for r in replies)
    q = lambda p: lens[int(p * (len(lens) - 1))]
    md.append(f"Words per reply: p10 {q(.1)}, median {q(.5)}, p90 {q(.9)}, max {lens[-1]}.\n")
    md.append(f"Shapes: {collections.Counter(c['shape'] for c in chats).most_common()}\n")
    md.append(f"Sources: {collections.Counter(c['source'] for c in chats).most_common(10)}\n")

    md.append("\n### Structures\n\n| pattern | rows |\n|:--|--:|")
    for k, (c, n) in pattern_counts(replies).items():
        md.append(f"| {k} | {pct(c, n)} |")

    for n_open in (3, 5):
        md.append(f"\n### Most common first {n_open} words\n\n| opening | rows |\n|:--|--:|")
        oc = collections.Counter(opening(r, n_open) for r in replies)
        for o, c in oc.most_common(20):
            md.append(f"| {o} | {pct(c, len(replies))} |")
            if n_open == 3 and c >= 15:
                clusters.append({"kind": "chat_opening", "key": o, "n": c,
                                 "ids": [x["id"] for x in chats if opening(x["reply"], 3) == o]})
    ends = collections.Counter(" ".join(words(sentences(r)[-1])[-4:]) if sentences(r) else "" for r in replies)
    md.append("\n### Most common last 4 words\n\n| ending | rows |\n|:--|--:|")
    for o, c in ends.most_common(15):
        md.append(f"| {o} | {pct(c, len(replies))} |")

    md.append("\n### 8-grams shared by many replies (boilerplate)\n\n| 8-gram | rows |\n|:--|--:|")
    for g, c in repeated_ngrams(replies):
        md.append(f"| {g} | {c} |")

    md.append("\n### Duplicates in chat\n")
    ex_r = collections.Counter(" ".join(words(r)) for r in replies)
    ex_u = collections.Counter(" ".join(words(c["user"])) for c in chats)
    md.append(f"Exact duplicate replies: {sum(c - 1 for c in ex_r.values() if c > 1)}; exact duplicate last user turns: {sum(c - 1 for c in ex_u.values() if c > 1)}.\n")
    nd_r = near_dups([(c["id"], c["reply"]) for c in chats])
    nd_u = near_dups([(c["id"], c["user"]) for c in chats], thresh=0.6)
    md.append(f"Near-duplicate reply pairs (5-gram Jaccard ≥0.5): {len(nd_r)}. Near-duplicate user-turn pairs (≥0.6): {len(nd_u)}.\n")
    for name, pairs in [("reply", nd_r), ("user", nd_u)]:
        for jac, a, b in pairs[:15]:
            md.append(f"- {name} {jac}: `{a}` ~ `{b}`")
        clusters.append({"kind": f"chat_near_dup_{name}", "pairs": pairs[:200]})

    for name, path in DOCS.items():
        rows = [json.loads(l) for l in path.open()]
        texts = [r["text"] for r in rows]
        md.append(f"\n## Documents: {name} (n={len(rows)})\n")
        lens = sorted(len(words(t)) for t in texts)
        md.append(f"Words: median {lens[len(lens) // 2]}, max {lens[-1]}.\n")
        if name == "const":
            md.append("\n| pattern | rows |\n|:--|--:|")
            for k, (c, n) in pattern_counts(texts).items():
                md.append(f"| {k} | {pct(c, n)} |")
            md.append("\n| first 4 words | rows |\n|:--|--:|")
            for o, c in collections.Counter(opening(t, 4) for t in texts).most_common(15):
                md.append(f"| {o} | {pct(c, len(texts))} |")
            md.append("\n| 8-gram | rows |\n|:--|--:|")
            for g, c in repeated_ngrams(texts):
                md.append(f"| {g} | {c} |")
        ex = collections.Counter(" ".join(words(t)) for t in texts)
        nd = near_dups([(r.get("id", i), t) for i, (r, t) in enumerate(zip(rows, texts))])
        md.append(f"\nExact duplicates: {sum(c - 1 for c in ex.values() if c > 1)}. Near-duplicate pairs (≥0.5): {len(nd)}.\n")
        for jac, a, b in nd[:10]:
            md.append(f"- {jac}: `{a}` ~ `{b}`")
        clusters.append({"kind": f"doc_near_dup_{name}", "pairs": nd[:200]})

    # Cross-source overlap: does a constitution document copy Stoic/other text, or a chat reply copy a document?
    pool = [(f"chat:{c['id']}", c["reply"]) for c in chats]
    for name, path in DOCS.items():
        pool += [(f"{name}:{json.loads(l).get('id', i)}", json.loads(l)["text"]) for i, l in enumerate(path.open())]
    cross = [p for p in near_dups(pool, thresh=0.3) if p[1].split(":")[0] != p[2].split(":")[0]]
    md.append(f"\n## Cross-source near-duplicates (5-gram Jaccard ≥0.3, different sources): {len(cross)}\n")
    for jac, a, b in cross[:20]:
        md.append(f"- {jac}: `{a}` ~ `{b}`")
    clusters.append({"kind": "cross_source", "pairs": cross[:200]})

    (OUT / "stats.md").write_text("\n".join(md) + "\n")
    with (OUT / "clusters.jsonl").open("w") as f:
        for c in clusters:
            f.write(json.dumps(c) + "\n")
    print("\n".join(md[-40:]))


if __name__ == "__main__":
    main()
