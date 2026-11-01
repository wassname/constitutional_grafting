"""D2 test (wassname via cg_collab2, 2026-11-01): judge the 240 li-rules-spec-3 dev rows twice with the current strict plain judge;
how many rows do the two samples disagree on, and how many does "reject only if both reject" keep vs one pass?
Pass 1 is the cached strict run of the quote-rule test (attempts 0-3); pass 2 draws fresh samples (attempts 4-7).
Writes slop/reviews/20261101_judge_twice_test/result.md. Usage: uv run --no-sync --env-file .env python scripts/scratch/20261101_judge_twice_test.py
-- PI/Claude (chatdata, opus-5-5)
"""
import collections

from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.pipe import ROOT, Run, load_config, read_jsonl

OUT = ROOT / "slop/reviews/20261101_judge_twice_test"


def outcome(judge: Judge, rows, config, tag):
    kept, rejected = judge.run(rows, Run(version=f"judge_twice_{tag}", batch="dev", config=config))
    return {r["seed_id"]: "kept" for r in kept} | {r["seed_id"]: r["filter"] for r in rejected}


def main():
    rows = read_jsonl(ROOT / "data/06_jev/li-rules-spec-3/dev/rows.jsonl")
    config = load_config("li-rules-spec-3")
    a, b = outcome(Judge(), rows, config, "1"), outcome(Judge(first_attempt=4), rows, config, "2")
    ids = [r["seed_id"] for r in rows]
    rej = lambda o, i: o[i] != "kept"
    one_pass_kept = sum(not rej(a, i) for i in ids)
    pass2_kept = sum(not rej(b, i) for i in ids)
    both_kept = sum(not (rej(a, i) and rej(b, i)) for i in ids)  # reject only if both reject
    disagree = [i for i in ids if rej(a, i) != rej(b, i)]
    lines = ["# Judge twice: same 240 li-rules-spec-3 dev rows, current strict plain judge (Haiku)\n",
             "| | kept | rejected |", "|:--|--:|--:|",
             f"| pass 1 | {one_pass_kept} | {240 - one_pass_kept} |", f"| pass 2 (fresh samples) | {pass2_kept} | {240 - pass2_kept} |",
             f"| reject only if both reject | {both_kept} | {240 - both_kept} |",
             f"| reject if either rejects | {sum(not (rej(a, i) or rej(b, i)) for i in ids)} | {sum(rej(a, i) or rej(b, i) for i in ids)} |",
             f"\nRows where the two passes disagree (keep vs reject): {len(disagree)} / 240.",
             f"Rows both passes reject: {sum(rej(a, i) and rej(b, i) for i in ids)}. Reasons where they disagree: "
             f"{dict(collections.Counter(a[i] if rej(a, i) else b[i] for i in disagree).most_common())}\n"]
    lines += [f"- {i}: pass 1 {a[i]}, pass 2 {b[i]}" for i in disagree]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "result.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines[:11]))


if __name__ == "__main__":
    main()
