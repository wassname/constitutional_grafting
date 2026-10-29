"""Split an exported chat file into the run-19 data groups, one file per chat adapter (plan slop/plans/20261029_run19_chat_data_v5.md):
dilemmas, help (ordinary help), texts (source texts) and identity. Identity takes identity rows from chatr12, the named_desk batch
and rows whose request asked who is answering; the other groups go by seed pool. Fails on a source it does not know.
usage: uv run python scripts/data/v2/split_groups.py data/train/chat_v6.jsonl --version v5      -- PI/Claude (opus-5-5), 2026-10-29
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

from constitutional_grafting.data.v2.pipe import load_config

POOL = {"lasr": "dilemmas", "machiavelli": "dilemmas", "competition": "dilemmas", "tiny_virtues": "dilemmas",
        "wildchat": "help", "stoic": "texts", "other_books": "texts"}
# chatr12 sources are "<pool>+<writer step>" (e.g. lasr+echo, machiavelli+proportion); the pool decides the group. "pool" rows are
# hand-written dilemmas (pool_contested, pool_power, ...).
CHATR12 = {"identity_v2": "identity", "identity": "identity", "stoic": "texts", "wildchat": "help", **{s: "dilemmas" for s in (
    "lasr", "competition", "tinymfv", "roles", "machiavelli", "virtuebench", "stakes", "story_scene", "pool")}}


def group(row: dict, identity_styles: set[str]) -> str:
    if row.get("batch") == "named_desk" or row.get("request_style") in identity_styles:
        return "identity"
    src = row["source"]
    return CHATR12[src.split(":", 1)[1].split("+")[0]] if src.startswith("chatr12:") else POOL[src]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("chat", type=Path)
    ap.add_argument("--version", required=True, help="data config holding identity_requests.styles")
    a = ap.parse_args()
    styles = load_config(a.version)["identity_requests"]["styles"]
    styles = {s for v in styles.values() for s in v} if isinstance(styles, dict) else set(styles)
    out = collections.defaultdict(list)
    for line in a.chat.open():
        out[group(json.loads(line), styles)].append(line)
    for g, lines in sorted(out.items()):
        path = a.chat.with_name(f"{a.chat.stem}_{g}.jsonl")
        path.write_text("".join(lines))
        path.with_suffix(".jsonl.sha256").write_text(hashlib.sha256(path.read_bytes()).hexdigest() + "\n")
        print(f"{g}: {len(lines)} rows -> {path}")


if __name__ == "__main__":
    main()
