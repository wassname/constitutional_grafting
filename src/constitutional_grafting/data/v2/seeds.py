"""02_seeds: fresh seeds, one row per seed, no seed or near-duplicate used twice, spread round-robin over families, nothing from held-out evals.

Each row carries seed_id, source, source_id, family, shape and either `messages` (pools that already are chats) or
`situation` (pools that give a passage or story; 03_requests turns it into a user message). -- PI/Claude (opus-5-5), 2026-10-27
"""
import hashlib
import json
import re
import unicodedata

import yaml
from pathlib import Path

from .pipe import ROOT, read_jsonl, Run, Step

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


def heldout_files(config: dict) -> list[Path]:
    """Held-out eval files; an entry may be a glob (contributors' private question folder fills up over time)."""
    out = []
    for p in config["heldout"]:  # paths relative to the repo; sibling repos as ../<repo>/...; globs anywhere after the first wildcard
        parts = (ROOT / p).parts
        i = next((k for k, part in enumerate(parts) if any(c in part for c in "*?[")), None)
        out += [Path(*parts).resolve()] if i is None else sorted(Path(*parts[:i]).resolve().glob(str(Path(*parts[i:]))))
    return out


def heldout_corpus_of(files: list[Path]) -> str:
    return "\n".join(norm(path.read_text()) for path in files)


def heldout_corpus(run: Run) -> str:
    return heldout_corpus_of(heldout_files(run.config))


def heldout_items(files: list[Path], width: int = 60) -> list[str]:
    """Held-out items as normalised texts: jsonl lines, every long string in a yaml file, else paragraphs."""
    out = []
    for path in files:
        if path.suffix == ".jsonl":
            texts = [l for l in path.read_text().splitlines() if l.strip()]
        elif path.suffix in (".yaml", ".yml"):
            texts = []
            def walk(x):
                if isinstance(x, str) and len(x) >= 2 * width:
                    texts.append(x)
                elif isinstance(x, dict):
                    [walk(v) for v in x.values()]
                elif isinstance(x, list):
                    [walk(v) for v in x]
            walk(yaml.safe_load(path.read_text()))
        else:
            texts = [p for p in path.read_text().split("\n\n") if p.strip()]
        out += [t for t in (norm(t).strip() for t in texts) if len(t) > width]
    return out


def holds_heldout(text: str, items: list[str], width: int = 60) -> bool:
    """The other direction: is a snippet of a held-out item inside this text (e.g. a game's background shared across its scenes)?"""
    t = norm(text)
    return any(i[int(f * (len(i) - width)): int(f * (len(i) - width)) + width] in t for i in items for f in (0.25, 0.5, 0.75))


def leaked(text: str, corpus: str, width: int = 60) -> bool:
    """tiny-character's leak test, reversed: is a snippet of this seed inside a held-out eval?"""
    t = norm(text).strip()
    if len(t) <= width:
        return bool(t) and t in corpus
    return any(t[int(f * (len(t) - width)): int(f * (len(t) - width)) + width] in corpus for f in (0.25, 0.5, 0.75))


def first_turn(rows, cfg):
    """Ordinary help (WildChat-style): the conversation's real first user turn."""
    for row in rows:
        turns = row["conversation"]
        first = turns[0]["content"] if turns and turns[0]["role"] == "user" else ""
        if 8 <= len(first.split()) <= 400:
            yield row["source_id"], row["source_id"], {"messages": [{"role": "user", "content": first}]}


def messages(rows, cfg):
    """A chat with its operator system prompt; the assistant turns are dropped."""
    for i, row in enumerate(rows):
        msgs = [m for m in row["messages"] if m["role"] != "assistant"]
        yield f"lasr_{i}", (row.get("metadata") or {}).get("principle", f"lasr_{i}"), {"messages": msgs}


def machiavelli(rows, cfg):
    """A text-game decision point (MACHIAVELLI scenarios) as a recommend-an-action request."""
    for row in rows:
        visible = {"game": row["title"], "background": row["short_summary"],
                   "recorded_history": {k: row[k] for k in ("early_history", "recent_history")},
                   "current_observation": row["obs"],
                   "available_actions": {k: v for k, v in row["choice_text"].items() if v is not None}}
        text = ("These are the visible observations from a fictional game. Recommend what the character should do at the "
                "current decision, and why.\n\n" + json.dumps(visible, ensure_ascii=False, indent=2))
        if cfg.get("player_name"):  # the game texts use "user_input" for the player's name; it leaked into documents ("Dear user_input,")
            from .generate import NAMES
            text = re.sub(r"\buser_input\b", NAMES[int(hash_order(15, str(row["source_id"])), 16) % len(NAMES)], text, flags=re.I)
        yield row["source_id"], row["title"], {"messages": [{"role": "user", "content": text}]}


def passages(rows, cfg):
    """A passage or story from any corpus: `text` and `family` name its fields, `where` filters rows, `words` bounds length."""
    text, family, where, words = cfg.get("text", "text"), cfg.get("family", "work"), cfg.get("where", {}), cfg.get("words")
    for row in rows:
        if any(row.get(k) not in (v if isinstance(v, list) else [v]) for k, v in where.items()):
            continue
        if words and not words[0] <= len(row[text].split()) <= words[1]:
            continue
        yield row["id"], row.get(family) or row["id"], {"situation": row[text]}


READERS = {"first_turn": first_turn, "messages": messages, "machiavelli": machiavelli, "passages": passages}


def candidates(pool_cfg: dict, path: Path):
    """Yield (source_id, family, payload) for one pool; payload is messages or situation text."""
    if path.suffix == ".parquet":
        import pandas as pd
        rows = pd.read_parquet(path).to_dict("records")
    else:
        rows = map(json.loads, path.open())
    yield from READERS[pool_cfg["reader"]](rows, pool_cfg)


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
        root = ROOT
        mix = run.config["mix"][run.batch]
        heldout, held_items = heldout_corpus(run), heldout_items(heldout_files(run.config))
        blacklist = set()
        if run.config["seed_blacklist"]:  # seeds a judge flagged for sexual content involving minors, for every character
            blacklist = {(e["pool"], str(e["source_id"])) for e in (yaml.safe_load((root / run.config["seed_blacklist"]).read_text()) or [])}
        kept, rejected, chosen_shingles, used = [], [], [], set()
        order = list(run.config["mix"])  # batches in build order; a later batch never reuses an earlier batch's seeds
        for prior in order[: order.index(run.batch)]:
            for r in read_jsonl(run.data / f"02_seeds/{run.version}/{prior}/rows.jsonl"):
                used.add((r["source"], r["source_id"]))
                chosen_shingles.append(shingles(r.get("situation") or "\n".join(m["content"] for m in r["messages"])))
        for pool, n in mix.items():
            path = Path(run.config["pools"][pool]["path"])
            path = path if path.is_absolute() else root / path
            pool_rows = spread(candidates(run.config["pools"][pool], path), lambda c: hash_order(self.seed, f"{pool}|{c[0]}"))
            taken = 0
            for source_id, family, payload in pool_rows:
                if taken >= n:
                    break
                text = payload.get("situation") or "\n".join(m["content"] for m in payload["messages"])
                base = {"source": pool, "source_id": str(source_id), "family": f"{pool}:{family}"}
                if (pool, str(source_id)) in used:
                    continue
                if (pool, str(source_id)) in blacklist:
                    rejected.append({**base, "filter": "blacklist", "reason": "on the seed blacklist (unsafe seed)"})
                    continue
                if PII.search(text):
                    rejected.append({**base, "filter": "pii", "reason": "email, phone or home path in text"})
                    continue
                if leaked(text, heldout) or holds_heldout(text, held_items):
                    rejected.append({**base, "filter": "heldout_leak", "reason": "snippet shared with a held-out eval (either direction)"})
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
