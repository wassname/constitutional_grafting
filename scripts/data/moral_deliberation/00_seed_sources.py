#!/usr/bin/env python3
"""Freeze fresh source-only questions, with provenance and evaluation boundaries. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path

from common import ROOT, read_jsonl
from constitutional_grafting.data.files import digest, file_sha, write_json, write_jsonl

WILDCHAT_REVISION = "7d6490e462285cf85d91eabea0f9a954fbddcd1f"
WILDCHAT = ROOT / "data/raw/moral_deliberation/wildchat_fresh.jsonl"
MACHIAVELLI = Path("/workspace/2026/machiavelli_character_scenarios/data/processed/parquet/train.parquet")
HELDOUT = Path("/workspace/2026/tiny-character/data/items.jsonl")
PII = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|(?:\+?\d[\d ()-]{8,}\d)|(?:/home/|/Users/)[^\s/]+")


def normalized(text: str) -> str:
    return " ".join(re.findall(r"\w+", text.casefold()))


def train_game(title: str) -> bool:
    return int(hashlib.md5(title.encode()).hexdigest(), 16) % 100 >= 20


def fetch_wildchat(limit: int):
    from datasets import load_dataset
    manifest = WILDCHAT.with_suffix(".manifest.json")
    identity = {"dataset": "allenai/WildChat-1M", "revision": WILDCHAT_REVISION, "scan_limit": limit}
    if WILDCHAT.exists():
        old = json.loads(manifest.read_text())
        if old["identity"] != identity or old["sha256"] != file_sha(WILDCHAT):
            raise ValueError("WildChat fetch cache identity changed; use a new named snapshot")
        print(f"Cached: {WILDCHAT}")
        return
    ds = load_dataset(identity["dataset"], revision=WILDCHAT_REVISION, split="train", streaming=True)
    rows = []
    for i, row in enumerate(ds):
        if i >= limit:
            break
        if row["language"] != "English":
            continue
        rows.append({"source_id": row["conversation_hash"], "conversation": [
            {"role": t["role"], "content": t["content"]} for t in row["conversation"]]})
    write_jsonl(WILDCHAT, rows)
    write_json(manifest, {"identity": identity, "sha256": file_sha(WILDCHAT), "rows": len(rows),
                          "note": "Unreviewed public raw text. Location/IP metadata omitted; no automatic privacy clearance."})
    print(WILDCHAT)


def prior_and_eval():
    ids, texts = set(), set()
    paths = [ROOT / "data/prompts/v3_seeds/sft.jsonl", ROOT / "data/frontier/sft/items.jsonl",
             ROOT / "data/raw/v3_seed_cache/wildchat_seed0.jsonl", ROOT / "data/raw/v3_seed_cache/machiavelli_seed0.jsonl"]
    paths += list((ROOT / "slop/data/moral_deliberation").glob("*/prompts.jsonl"))
    for path in paths:
        for row in read_jsonl(path):
            for key in ("source_id", "id"):
                if row.get(key):
                    ids.add(str(row[key]))
            for key in ("prompt", "request", "seed"):
                if isinstance(row.get(key), str):
                    texts.add(normalized(row[key]))
            for message in row.get("messages", []):
                if message["role"] == "user":
                    texts.add(normalized(message["content"]))
    eval_rows = read_jsonl(HELDOUT) + read_jsonl(ROOT / "slop/eval/run8/items.jsonl")
    for row in eval_rows:
        ids.add(str(row.get("source_id", row["id"])))
    return ids, texts, json.dumps(eval_rows, ensure_ascii=False).casefold()


def seed_row(source: str, source_id: str, family: str, messages: list[dict], provenance: dict) -> dict:
    if not messages or messages[-1]["role"] != "user":
        raise ValueError("a source conversation must end at the unanswered user turn")
    return {"id": f"{source}_{digest({'source_id': source_id, 'messages': messages})[:16]}",
            "shape": source, "source": source, "source_id": str(source_id), "family": family,
            "messages": messages, "source_provenance": provenance, "split": "train_candidate",
            "privacy_flags": [m["role"] for m in messages if PII.search(m["content"])],
            "review_status": "unread", "adaptation": "No source answer used as a target; original context retained."}


def candidates(source: str):
    if source == "wildchat":
        snapshot = json.loads(WILDCHAT.with_suffix(".manifest.json").read_text())
        for row in read_jsonl(WILDCHAT):
            turns = row["conversation"]
            user_positions = [i for i, t in enumerate(turns) if t["role"] == "user"]
            for end in reversed(user_positions):
                context = turns[:end + 1]
                words = sum(len(m["content"].split()) for m in context)
                if 60 <= words <= 2000 and (end >= 2 or len(context[-1]["content"].split()) >= 120):
                    yield seed_row(source, row["source_id"], row["source_id"], context,
                                   {"path": str(WILDCHAT), "revision": WILDCHAT_REVISION, "snapshot_sha256": snapshot["sha256"],
                                    "user_turn_index": end, "license": "ODC-BY", "prior_assistant_turns": "context only, never targets"})
                    break
    elif source == "machiavelli":
        import pyarrow.parquet as pq
        eligible = {}
        for batch in pq.ParquetFile(MACHIAVELLI).iter_batches(batch_size=128):
            for row in batch.to_pylist():
                if row["source"] == "machiavelli" and train_game(row["world"]) and not json.loads(row["scenario_review_flags"]) and not json.loads(row["input_issues"]):
                    eligible[row["source_id"]] = row
        pinned = MACHIAVELLI.parents[2] / "interim/pinned_source_rows.jsonl"
        with pinned.open() as file:
            for line in file:
                row = json.loads(line)
                if row["source_id"] not in eligible:
                    continue
                meta = eligible[row["source_id"]]
                if row["title"] != meta["world"]:
                    raise ValueError("canonical game title changed; recheck the game-level split")
                history = {k: row[k] for k in ("early_history", "recent_history", "early_actions", "recent_actions")}
                visible = {"game": row["title"], "background": row["short_summary"], "recorded_history": history,
                           "current_observation": row["obs"], "available_actions": {k: v for k, v in row["choice_text"].items() if v is not None}}
                text = ("These are the original visible observations from a fictional game, not a preferred answer. "
                        "History describes earlier decisions; recommend what the character should do at the CURRENT decision, and why.\n\n"
                        + json.dumps(visible, ensure_ascii=False, indent=2))
                yield seed_row(source, row["source_id"], row["title"], [{"role": "user", "content": text}],
                               {"path": str(pinned), "revision": meta["source_revision"], "license": meta["source_license"],
                                "row_i": row["row_i"], "source_sha256": digest(visible),
                                "context_status": "Original visible observations/history, not a model summary", "outcome_labels_omitted": True})
    elif source in {"stoic", "tiny_virtues_books"}:
        path = ROOT / ("data/stoic_corpus/selected_dedup.jsonl" if source == "stoic" else "data/other_corpus/chunks.jsonl")
        for row in read_jsonl(path):
            if source == "stoic" and row["kind"] != "ancient":
                continue
            if not 150 <= len(row["text"].split()) <= 900:
                continue
            family = row["work"]
            if re.search(r"Kaufmann|Vallor|Franklin|Comte.Sponville|VIA character", family, re.I):
                continue
            text = ("Please examine this attributed passage rather than treating its conclusion as authoritative. "
                    "Which parts of the argument hold up, which depend on assumptions, and what practical judgment follows?\n\n" + row["text"])
            yield seed_row(source, row["id"], family, [{"role": "user", "content": text}],
                           {"path": str(path), "source_file": row["file"], "upstream_file_hash": row["file_sha"], "lines": row["lines"],
                            "source_sha256": digest(row["text"]), "private_book_text": True,
                            "evaluation_boundary": "Not independent tiny-virtues evidence if this book/case enters training"})
    else:
        raise ValueError(source)


def build(output: Path, sources: list[str], n: int, seed: int):
    used, seen, heldout_text = prior_and_eval()
    selected, counts = [], Counter()
    for source in sources:
        pool, families = [], set()
        for row in candidates(source):
            user_text = normalized(row["messages"][-1]["content"])
            if row["source_id"] in used or user_text in seen or row["privacy_flags"]:
                counts[f"{source}: prior_or_privacy"] += 1
                continue
            if row["source_id"].casefold() in heldout_text:
                counts[f"{source}: heldout"] += 1
                continue
            pool.append(row)
        pool.sort(key=lambda r: digest({"seed": seed, "source": source, "source_id": r["source_id"]}))
        for row in pool:
            if row["family"] in families or len(families) >= n:
                continue
            families.add(row["family"])
            selected.append(row)
            seen.add(normalized(row["messages"][-1]["content"]))
            counts[f"{source}: selected"] += 1
        if len(families) != n:
            raise ValueError(f"{source}: only {len(families)} fresh source families, need {n}")
    identity = {"seed": seed, "n_per_source": n, "sources": sources, "rows_sha256": digest(selected)}
    manifest = output / "manifest.json"
    if manifest.exists() and json.loads(manifest.read_text())["identity"] != identity:
        raise ValueError("seed selection changed; choose a new output directory")
    write_jsonl(output / "seeds.jsonl", selected)
    write_json(manifest, {"identity": identity, "counts": dict(counts), "status": "unread_candidates",
                          "limitations": ["Exact ids/text excluded; semantic duplicates still need reading", "Source summaries/PII flags are not factual or privacy clearance",
                                          "tiny_virtues_books means new passages from the private book corpus, not reuse of the published test stories"],
                          "signature": "PI/OpenAI (Sol)"})
    print(json.dumps(dict(counts), indent=2)); print(output / "seeds.jsonl")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("output", type=Path)
    ap.add_argument("--sources", nargs="+", default=["wildchat", "machiavelli", "stoic", "tiny_virtues_books"])
    ap.add_argument("--n-per-source", type=int, default=3)
    ap.add_argument("--seed", type=int, default=20261027)
    ap.add_argument("--fetch-wildchat", type=int, help="Explicit network acquisition: maximum raw conversations to scan")
    args = ap.parse_args()
    if args.fetch_wildchat:
        fetch_wildchat(args.fetch_wildchat)
    build(args.output, args.sources, args.n_per_source, args.seed)
