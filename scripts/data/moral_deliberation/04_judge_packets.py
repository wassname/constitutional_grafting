#!/usr/bin/env python3
"""Freeze full judge packets; merge complete, hash-bound, quote-checked JSONL judgments.

uv run --no-sync python scripts/data/moral_deliberation/04_judge_packets.py RUN --batch 0 [--ids ID ...]
uv run --no-sync python scripts/data/moral_deliberation/04_judge_packets.py RUN --batch 0 --merge
-- PI/OpenAI (Sol)
"""
import argparse
import json
from pathlib import Path

from common import by_id, config, material_hash, read_jsonl, run_dir, validate_judgment


def packets(run: Path, batch: int, ids: list[str] | None):
    pk, jd = run / "judge/packets", run / "judge/replies"
    pk.mkdir(parents=True, exist_ok=True)
    jd.mkdir(parents=True, exist_ok=True)
    rubric = Path(__file__).with_name("judge_rubric.md").read_text()
    snapshot = run / "judge/rubric.md"
    if snapshot.exists() and snapshot.read_text() != rubric:
        raise ValueError("Rubric changed after packets were frozen; use a separately named judging stage")
    snapshot.write_text(rubric)
    raw = by_id(read_jsonl(run / "raw.jsonl"), "call_id")
    cfg = config(run)
    for prompt in read_jsonl(run / "prompts.jsonl"):
        if prompt["batch"] != batch or (ids and prompt["id"] not in ids):
            continue
        cids = sorted(f"{prompt['id']}__{fr}__k{k}" for fr in cfg["framings"] for k in range(cfg["k"]))
        if not set(cids) <= raw.keys():
            raise ValueError(f"Incomplete candidate group: {prompt['id']}")
        conv = "\n\n".join(f"**{m['role']}:**\n\n{m['content']}" for m in prompt["messages"])
        body = [f"# Prompt `{prompt['id']}` (shape: {prompt['shape']})\n\n"
                "The writer saw its constitution framing before the original conversation below. "
                "Original role-specific system instructions are preserved; their conflicts are part of the task.\n\n"
                f"## Conversation\n\n{conv}\n"]
        for cid in cids:
            row = raw[cid]
            sha = material_hash(run, prompt, row)
            body.append(f"## Candidate `{cid}` (finish: {row['finish_reason']})\n\ninput_sha256: `{sha}`\n\n"
                        f"### Hidden reasoning\n\n````\n{row['reasoning']}\n````\n\n"
                        f"### Answer\n\n````\n{row['content']}\n````\n")
        body.append(f"## Existing answer (reference only)\n\n````\n{prompt['existing_answer']}\n````\n")
        (pk / f"{prompt['id']}.md").write_text("\n".join(body))
        print(pk / f"{prompt['id']}.md", len(cids), "candidates")


def merge(run: Path, batch: int):
    raw = by_id(read_jsonl(run / "raw.jsonl"), "call_id")
    prompts = by_id(read_jsonl(run / "prompts.jsonl"), "id")
    expected = {cid for cid, r in raw.items() if r["batch"] == batch}
    if not expected:
        raise ValueError("No generated candidates in selected batch")
    candidates, best = {}, {}
    for file in sorted((run / "judge/replies").glob("*.jsonl")):
        for row in read_jsonl(file):
            key = "call_id" if "call_id" in row else "prompt_id"
            table = candidates if key == "call_id" else best
            if row[key] in table:
                raise ValueError(f"Duplicate judgment: {row[key]}")
            table[row[key]] = row
    if not expected <= candidates.keys():
        raise ValueError(f"Missing {len(expected - candidates.keys())} candidate judgments; no release written")
    for cid in expected:
        row = raw[cid]
        validate_judgment(candidates[cid], prompts[row["id"]], row, material_hash(run, prompts[row["id"]], row))
    for pid in {raw[cid]["id"] for cid in expected}:
        chosen = best[pid]["best_call_id"]
        if chosen is not None and (chosen not in expected or raw[chosen]["id"] != pid or candidates[chosen]["verdict"] != "keep"):
            raise ValueError(f"Invalid best-of pick for {pid}: {chosen}")
    path = run / "judged.jsonl"
    with path.open("w") as f:
        for cid in sorted(expected):
            row = candidates[cid]
            f.write(json.dumps({**row, "best_of_prompt": best[raw[cid]["id"]]["best_call_id"] == cid}, ensure_ascii=False) + "\n")
    print(f"Merged {len(expected)} judgments: {path}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--batch", type=int, required=True)
    ap.add_argument("--ids", nargs="+", help="write only these complete prompt groups")
    ap.add_argument("--merge", action="store_true")
    args = ap.parse_args()
    folder = run_dir(args.run)
    merge(folder, args.batch) if args.merge else packets(folder, args.batch, args.ids)
