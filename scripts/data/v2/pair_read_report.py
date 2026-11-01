"""Full-read report for a paired build: every seed, both halves side by side, through every DAG stage (seed, request, generation,
judge, edits, final status), so every kept row and every reject can be read before training (AGENTS.md data principle 5).
One markdown file per chunk of seeds under slop/reviews/<date>_<a>_vs_<b>_read/, plus an index with per-stage counts.
Usage: uv run python scripts/data/v2/pair_read_report.py --a li-rules-spec-5 --b li-value-augmented-spec-2 --batch dev
-- PI/Claude (chatdata, opus-5-5), 2026-11-01
"""
import argparse
import collections
import datetime
import json

from constitutional_grafting.data.v2.pipe import ROOT, read_jsonl

CHUNK = 20  # seeds per file, so one file is one reading session


def stage_rows(version: str, batch: str, step: str) -> dict:
    """seed_id -> (row, 'kept' | filter) for one stage, kept and rejected."""
    d = ROOT / "data" / step / version / batch
    if not (d / "rows.jsonl").exists():
        return {}
    out = {r["seed_id"]: (r, "kept") for r in read_jsonl(d / "rows.jsonl")}
    out |= {r["seed_id"]: (r, r["filter"]) for r in read_jsonl(d / "rejected.jsonl") if "seed_id" in r}  # seed-step rejects never got an id
    return out


def fate(version: str, batch: str, sid: str, stages: dict) -> str:
    """Where the row ended: the first stage that rejected it, or the final file."""
    for step in ("04_generate", "06_jev", "07_judge", "08_retry", "09_edit", "10_edit2", "11_export"):
        if sid in stages[step] and stages[step][sid][1] != "kept":
            return f"rejected at {step}: {stages[step][sid][1]}"
    return "kept" if sid in stages["11_export"] else "not reached"


def half(name: str, version: str, batch: str, sid: str, stages: dict) -> list[str]:
    gen = stages["04_generate"].get(sid, (None,))[0]
    judged = stages["07_judge"].get(sid, (None,))[0]
    final = (stages["10_edit2"].get(sid) or stages["09_edit"].get(sid) or (None,))[0]
    out = [f"#### {name} ({version}): {fate(version, batch, sid, stages)}\n"]
    if gen is None:
        return out + ["(no generation)\n"]
    out.append(f"**Notes (teacher {gen.get('teacher', '?')}):**\n\n{gen['reasoning']}\n")
    out.append(f"**Reply as generated:**\n\n{gen['answer']}\n")
    if judged is not None and judged.get("judge"):
        j = judged["judge"]
        out.append(f"**Judge: {j['verdict']}.** {j.get('observations', '')}\n")
        out += [f"- {d['kind']} ({d['location']}): \"{d['quote'][:200]}\" | {d['why']}" for d in j["defects"]]
        out.append("")
    if final is not None and final.get("edits"):
        out.append("**Edits:**\n")
        out += [f"- pass {e.get('pass', 1)} {e['kind']} ({e['field']}): \"{e['old']}\" -> \"{e['new']}\"" for e in final["edits"]]
        out.append(f"\nEdit checks: {final.get('edit_check')}\n")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--a", required=True)
    ap.add_argument("--b", required=True)
    ap.add_argument("--batch", required=True)
    args = ap.parse_args()
    steps = ("02_seeds", "03_requests", "04_generate", "06_jev", "07_judge", "08_retry", "09_edit", "10_edit2", "11_export")
    S = {v: {s: stage_rows(v, args.batch, s) for s in steps} for v in (args.a, args.b)}
    seeds = [r["seed_id"] for r in read_jsonl(ROOT / "data/02_seeds" / args.a / args.batch / "rows.jsonl")]
    out_dir = ROOT / "slop/reviews" / f"{datetime.date.today():%Y%m%d}_{args.a}_vs_{args.b}_{args.batch}_read"
    out_dir.mkdir(parents=True, exist_ok=True)
    index = [f"# Full read: {args.a} vs {args.b}, batch {args.batch} ({len(seeds)} seeds)\n",
             "Each file: every seed in order, its request, then both halves' notes, reply, judge verdict and defects, edits and final status.",
             "Write findings under each seed as `> FINDING (reader): ...` quoting the text; then list them here.\n",
             "| stage | " + " | ".join(f"{v} kept / rejected" for v in (args.a, args.b)) + " |", "|:--|--:|--:|"]
    for s in steps[2:]:
        cells = []
        for v in (args.a, args.b):
            c = collections.Counter("kept" if f == "kept" else "rejected" for _, f in S[v][s].values())
            cells.append(f"{c['kept']} / {c['rejected']}")
        index.append(f"| {s} | " + " | ".join(cells) + " |")
    both = {v: collections.Counter(fate(v, args.batch, sid, S[v]).split(":")[0] for sid in seeds) for v in (args.a, args.b)}
    index.append(f"\nFinal status per half: {dict(both[args.a])} / {dict(both[args.b])}\n\nFiles:")
    for k in range(0, len(seeds), CHUNK):
        chunk = seeds[k: k + CHUNK]
        lines = [f"# Seeds {k + 1}-{k + len(chunk)} of {len(seeds)}\n"]
        for n, sid in enumerate(chunk, k + 1):
            seed = S[args.a]["02_seeds"][sid][0]
            req = S[args.a]["03_requests"].get(sid, (seed,))[0]
            lines.append(f"\n---\n## {n}. {sid} ({seed['source']}, {req.get('request_style', 'source conversation')})\n")
            lines.append("**Seed:** " + (seed.get("situation") or "\n\n".join(f"[{m['role']}] {m['content']}" for m in seed["messages"]))[:3000] + "\n")
            lines.append("**Request:**\n\n" + "\n\n".join(f"[{m['role']}] {m['content']}" for m in req["messages"]) + "\n")
            for name, v in (("A", args.a), ("B", args.b)):
                lines += half(name, v, args.batch, sid, S[v])
        f = out_dir / f"seeds_{k + 1:03d}-{k + len(chunk):03d}.md"
        f.write_text("\n".join(lines) + "\n")
        index.append(f"- {f.name}")
    (out_dir / "index.md").write_text("\n".join(index) + "\n")
    print(out_dir / "index.md")


if __name__ == "__main__":
    main()
