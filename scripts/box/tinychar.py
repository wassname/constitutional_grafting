"""On-box calibrated tiny-character generation inputs and pinned Jev receipts. -- PI/OpenAI"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time

ROOT = Path(__file__).resolve().parents[2]
TC = ROOT / ".local/tiny-character-9e33eed"
JUDGE_V2 = {"change": ROOT / "slop/eval/judge_inputs/20261029_change_v2.md",
            "refs": ROOT / "slop/eval/judge_inputs/20261029_refs_guided_v4.jsonl", "pin": "9e33eed"}
SUBSETS = {size: f"configs/eval/tinychar_subsets/qwen3.5-35b-a3b_20261030_{suffix}.txt"
           for size, suffix in (("probe", "probe"), ("scan", "quarter"), ("full", "half"))}


def rows(path):
    return [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]


def write_rows(path, records):
    Path(path).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in records))


def subset(source, target, ids_file, smoke=0):
    ids = {l.strip() for l in (ROOT / ids_file).read_text().splitlines() if l.strip() and not l.startswith("#")}
    selected = [r for r in rows(source) if r["id"] in ids]
    assert {r["id"] for r in selected} == ids, "subset items missing from frozen inputs"
    if smoke:
        selected = sorted(selected, key=lambda r: len(str(r.get("system") or "")) + sum(map(len, r["turns"])))[:smoke]
    write_rows(target, selected)
    return target


def comparison(judged, replies, model, reference):
    """Reference-failed tasks and tight generation caps cannot establish damage. -- PI/OpenAI"""
    raw = {(r["model"], r["item_id"], r["sample"]): r for r in replies}
    by = {(r["model"], r["item_id"], r["sample"]): r for r in judged}
    damage, ref_damage, passed, retained = [], [], [], []
    for (m, i, s), r in by.items():
        if m != model:
            continue
        b = by[(reference, i, s)]
        for n, (t, bt) in enumerate(zip(r["turn_checks"], b["turn_checks"], strict=True)):
            health = []
            for rec, other, checks, row in ((r, b, t, raw[(model, i, s)]), (b, r, bt, raw[(reference, i, s)])):
                turn, opposite = row["turns"][n], raw[(other["model"], i, s)]["turns"][n]
                long_cut = checks["truncated"] and opposite["finish_reason"] != "length" and turn["n_tokens"] >= 1.5 * opposite["n_tokens"]
                coherent = (rec.get("jev") or [{}] * len(rec["turn_checks"]))[n].get("coherent", 1)
                health.append(max(1 - coherent, float(long_cut), *(checks.get(k, 0) for k in ("looped", "lang_switch", "empty", "role_confusion"))))
            damage.append(health[0])
            ref_damage.append(health[1])
        if not r["judged"] and r.get("check") and b.get("check"):
            key = "correct" if "correct" in b["check"] else "format_ok"
            if b["check"][key] == 1:
                passed.append(i)
                retained.append(float(r["check"][key]))
    return {"bad_share": sum(damage) / len(damage), "reference_bad_share": sum(ref_damage) / len(ref_damage),
            "capability_reference_passed": passed, "capability_retained": sum(retained) / len(retained) if retained else None}


def broken(summary, settings):
    retained = summary["capability_retained"]
    return ((retained is not None and retained < settings["min_gsm"])
            or summary["bad_share"] - summary["reference_bad_share"] > settings["max_bad_share"])


def judge(candidate, reference, out, deadline):
    """Code/tools remain generated but are scored only in the local Docker sandbox. -- PI/OpenAI"""
    out = Path(out)
    if (out / "summary.json").exists():
        return json.loads((out / "summary.json").read_text())
    out.mkdir(parents=True, exist_ok=True)
    items = {r["id"]: r for r in rows(TC / "data/items.jsonl")}
    mine, theirs = rows(candidate), rows(reference)
    model, base = mine[0]["model"], theirs[0]["model"]
    common = {(r["item_id"], r["sample"]) for r in mine} & {(r["item_id"], r["sample"]) for r in theirs}
    records = [r | {"base_model": base} for r in mine + theirs if (r["item_id"], r["sample"]) in common and items[r["item_id"]]["family"] not in ("code", "tools")
               and (items[r["item_id"]]["checks"] or {}).get("kind") not in ("code", "unittest", "gsm8k_code", "tool_call")]
    ids = sorted({r["item_id"] for r in records})
    refs = {r["item_id"]: r for r in rows(JUDGE_V2["refs"])}
    for i in ids:
        if items[i]["judged"]:
            assert all([t["user"] for t in d] == items[i]["turns"] for d in refs[i]["refs"]), i
    write_rows(out / "replies.jsonl", records)
    write_rows(out / "items.jsonl", [items[i] for i in ids])
    write_rows(out / "refs.jsonl", [refs[i] for i in ids if items[i]["judged"]])
    env = dict(os.environ)
    line = next(l for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
    env["OPENROUTER_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    label = "cg_box_" + "_".join(out.relative_to(ROOT).parts)
    cache = TC / ".local/cache/jev.jsonl"
    offset = cache.stat().st_size if cache.exists() else 0
    argv = [TC / ".venv/bin/python", TC / "scripts/03_judge.py", "--replies", out / "replies.jsonl", "--items", out / "items.jsonl",
            "--change", JUDGE_V2["change"], "--refs", out / "refs.jsonl", "--name", "Musonius", "--run", label,
            "--judge", "jev", "--turn-judge", "jev", "--concurrency", "4", "--subset"]
    try:
        with (out / "judge.log").open("w") as log:
            subprocess.run(list(map(str, argv)), cwd=TC, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=deadline - time.time())
        for name in ("judged.jsonl", "meta.json"):
            shutil.copyfile(TC / "results" / label / name, out / name)
    finally:
        calls = []
        if cache.exists():
            with cache.open() as cached:
                cached.seek(offset)
                calls = [json.loads(l) for l in cached]
        (out / "cost.json").write_text(json.dumps({"new_jev_requests": len(calls), "cost_usd": sum(c.get("cost", 0) for c in calls)}, indent=2))
    summary = comparison(rows(out / "judged.jsonl"), records, model, base)
    (out / "summary.json").write_text(json.dumps(summary, indent=2))
    return summary
