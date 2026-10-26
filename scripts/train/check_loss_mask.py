"""Fail if any chat-training row puts loss on an empty think block (wassname 2026-10-26: no NLL on blank thinking, always),
or if its last labelled segment does not end with <|im_end|>: Axolotl's input_output format adds no EOS, so a missing
end-of-turn token is never learned (chatr12: 903/1625 rows). ALLOW_MISSING_EOS=1 only for exact replication of old runs.
Empty think blocks belong in the unlabelled prompt segment; real reasoning inside a labelled think block is allowed.
usage: python scripts/train/check_loss_mask.py data/train/run10/chatr12.jsonl [...]   -- PI/Claude (opus)"""
import json
import os
import re
import sys

EMPTY_THINK = re.compile(r"<think>\s*</think>")


def missing_eos(path: str) -> list[str]:
    bad = []
    for line in open(path):
        row = json.loads(line)
        labelled = [seg for seg in row.get("segments", []) if seg["label"]]
        if labelled and not labelled[-1]["text"].rstrip().endswith("<|im_end|>"):
            bad.append(row.get("id", "?"))
    return bad


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
        no_eos = missing_eos(p)
        if no_eos and os.environ.get("ALLOW_MISSING_EOS") != "1":
            raise AssertionError(f"{p}: {len(no_eos)} rows end the labelled target without <|im_end|>, e.g. {no_eos[:3]}")
        print(f"ok {p}: no loss on empty think blocks; rows missing <|im_end|>: {len(no_eos)}")
