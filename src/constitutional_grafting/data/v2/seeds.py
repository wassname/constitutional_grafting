"""02_seeds: fresh seeds, one row per seed, no seed or near-duplicate used twice, spread round-robin over families, nothing from held-out evals.

Each row carries seed_id, source, source_id, family, shape and either `messages` (pools that already are chats) or
`situation` (pools that give a passage or story; 03_requests turns it into a user message). -- PI/Claude (opus-5-5), 2026-10-27
"""
import hashlib
import json
import re
import unicodedata
from pathlib import Path

from .pipe import read_jsonl, Run, Step

PII = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|(?:\+?\d[\d ()-]{8,}\d)|(?:/home/|/Users/)[^\s/]+")
CHAT_POOLS = {"wildchat", "lasr", "machiavelli"}


def words(text: str) -> list[str]:
    """Unicode word tokens; each CJK character is its own token (Greek, Hindi, Chinese survive)."""
    out = []
    for c in text.lower():
        if "\u4e00" <= c <= "\u9fff" or "\u3040" <= c <= "\u30ff":
            out.append(f" {c} ")
        else:
            out.append(c if unicodedata.category(c)[0] in "LMN" or c == "'" else " ")
    return "".join(out).split()


def shingles(text: str, k: int = 5) -> set[str]:
    w = words(text)
    return {" ".join(w[i:i + k]) for i in range(max(1, len(w) - k + 1))}


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower())


def hash_order(seed: int, key: str) -> str:
    return hashlib.sha256(f"{seed}|{key}".encode()).hexdigest()


def heldout_corpus(run: Run) -> str:
    root = Path(run.config["source_root"])
    parts = []
    for p in run.config["heldout"]:
        path = Path(p) if Path(p).is_absolute() else root / p
        parts.append(norm(path.read_text()))
    return "\n".join(parts)


def leaked(text: str, corpus: str, width: int = 60) -> bool:
    """tiny-character's leak test, reversed: is a snippet of this seed inside a held-out eval?"""
    t = norm(text).strip()
    if len(t) <= width:
        return bool(t) and t in corpus
    return any(t[int(f * (len(t) - width)): int(f * (len(t) - width)) + width] in corpus for f in (0.25, 0.5, 0.75))


def candidates(pool: str, path: Path):
    """Yield (source_id, family, payload) for one pool; payload is messages or situation text."""
    if pool == "wildchat":
        for row in map(json.loads, path.open()):
            turns = row["conversation"]
            first = turns[0]["content"] if turns and turns[0]["role"] == "user" else ""
            if 8 <= len(first.split()) <= 400:  # ordinary help: a real first user turn
                yield row["source_id"], row["source_id"], {"messages": [{"role": "user", "content": first}]}
    elif pool == "lasr":
        for i, row in enumerate(map(json.loads, path.open())):
            msgs = [m for m in row["messages"] if m["role"] != "assistant"]
            yield f"lasr_{i}", (row.get("metadata") or {}).get("principle", f"lasr_{i}"), {"messages": msgs}
    elif pool == "machiavelli":
        for row in map(json.loads, path.open()):
            visible = {"game": row["title"], "background": row["short_summary"],
                       "recorded_history": {k: row[k] for k in ("early_history", "recent_history")},
                       "current_observation": row["obs"],
                       "available_actions": {k: v for k, v in row["choice_text"].items() if v is not None}}
            text = ("These are the visible observations from a fictional game. Recommend what the character should do at the "
                    "current decision, and why.\n\n" + json.dumps(visible, ensure_ascii=False, indent=2))
            yield row["source_id"], row["title"], {"messages": [{"role": "user", "content": text}]}
    elif pool in ("stoic", "other_books"):
        for row in map(json.loads, path.open()):
            if pool == "stoic" and row.get("kind") != "ancient":
                continue
            if 120 <= len(row["text"].split()) <= 900:
                yield row["id"], row.get("work", row["id"]), {"situation": row["text"]}
    elif pool == "tiny_virtues":
        import pandas as pd
        for row in pd.read_parquet(path).to_dict("records"):
            yield row["id"], row.get("bibkey") or row["id"], {"situation": row["story"]}
    elif pool == "competition":
        import pandas as pd
        for row in pd.read_parquet(path).to_dict("records"):
            if row.get("language", "en") in ("en", "English") and 150 <= len(row["text"].split()) <= 2500:
                yield row["id"], row["id"], {"situation": row["text"]}
    else:
        raise ValueError(pool)


def spread(rows, key) -> list:
    """Round-robin over families (game, book, principle): every family gives one seed before any gives a second."""
    by_family = {}
    for r in sorted(rows, key=key):
        by_family.setdefault(r[1], []).append(r)
    ranked = [(i, key(r), r) for group in by_family.values() for i, r in enumerate(group)]
    return [r for _, _, r in sorted(ranked, key=lambda t: t[:2])]


class Seeds(Step):
    number, name = 2, "seeds"

    def __init__(self, seed: int = 20261027, near_dup: float = 0.5):
        self.seed, self.near_dup = seed, near_dup

    def run(self, rows, run):
        root = Path(run.config["source_root"])
        mix = run.config["mix"][run.batch]
        heldout = heldout_corpus(run)
        kept, rejected, chosen_shingles, used = [], [], [], set()
        order = list(run.config["mix"])  # batches in build order; a later batch never reuses an earlier batch's seeds
        for prior in order[: order.index(run.batch)]:
            for r in read_jsonl(run.data / f"02_seeds/{run.version}/{prior}/rows.jsonl"):
                used.add((r["source"], r["source_id"]))
                chosen_shingles.append(shingles(r.get("situation") or "\n".join(m["content"] for m in r["messages"])))
        for pool, n in mix.items():
            path = Path(run.config["pools"][pool])
            path = path if path.is_absolute() else root / path
            pool_rows = spread(candidates(pool, path), lambda c: hash_order(self.seed, f"{pool}|{c[0]}"))
            taken = 0
            for source_id, family, payload in pool_rows:
                if taken >= n:
                    break
                text = payload.get("situation") or "\n".join(m["content"] for m in payload["messages"])
                base = {"source": pool, "source_id": str(source_id), "family": f"{pool}:{family}"}
                if (pool, str(source_id)) in used:
                    continue
                if PII.search(text):
                    rejected.append({**base, "filter": "pii", "reason": "email, phone or home path in text"})
                    continue
                if leaked(text, heldout):
                    rejected.append({**base, "filter": "heldout_leak", "reason": "snippet found in a held-out eval"})
                    continue
                sh = shingles(text)
                dup = max((len(sh & o) / len(sh | o) for o in chosen_shingles), default=0.0)
                if dup >= self.near_dup:
                    rejected.append({**base, "filter": "near_duplicate", "reason": f"5-gram Jaccard {dup:.2f} with a chosen seed"})
                    continue
                used.add((pool, str(source_id)))
                chosen_shingles.append(sh)
                kind = "chat" if "messages" in payload else "situation"
                shape = "ordinary" if pool == "wildchat" else "dilemma"
                kept.append({"seed_id": f"{pool}_{hash_order(0, str(source_id))[:12]}", **base, "shape": shape, "kind": kind,
                             "recipe": run.version, **payload})
                taken += 1
            if taken < n:
                raise ValueError(f"{pool}: only {taken} seeds passed, need {n}")
        return kept, rejected
