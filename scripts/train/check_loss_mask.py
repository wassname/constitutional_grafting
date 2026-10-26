"""Fail if any chat-training row puts loss on an empty think block (wassname 2026-10-26: no NLL on blank thinking, always).
Empty think blocks belong in the unlabelled prompt segment; real reasoning inside a labelled think block is allowed.
usage: python scripts/train/check_loss_mask.py data/train/run10/chatr12.jsonl [...]   -- PI/Claude (opus)"""
import json
import re
import sys

EMPTY_THINK = re.compile(r"<think>\s*</think>")


def empty_think_in_loss(path: str) -> list[str]:
    bad = []
    for line in open(path):
        row = json.loads(line)
        if any(seg["label"] and EMPTY_THINK.search(seg["text"]) for seg in row.get("segments", [])):
            bad.append(row.get("id", "?"))
    return bad


if __name__ == "__main__":
    for p in sys.argv[1:]:
        bad = empty_think_in_loss(p)
        assert not bad, f"{p}: {len(bad)} rows train on an empty think block, e.g. {bad[:3]}"
        print(f"ok {p}: no loss on empty think blocks")
