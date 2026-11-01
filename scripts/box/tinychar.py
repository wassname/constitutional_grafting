"""On-box calibrated tiny-character generation inputs and pinned Jev receipts. -- PI/OpenAI"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import time
import warnings

ROOT = Path(__file__).resolve().parents[2]
TC = ROOT / ".local/tiny-character-9e33eed"
JUDGE_PIN = "9e33eed"
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
    damage, ref_damage, passed, retained, gsm_passed, gsm_retained = [], [], [], [], [], []
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
                health.append(float(1 - coherent >= 0.5 or long_cut or any(checks.get(k, 0) for k in ("looped", "lang_switch", "empty", "role_confusion"))))
            # health[0] is the candidate's bad-turn indicator; health[1] is the reference's.
            damage.append(health[0])
            ref_damage.append(health[1])
        if not r["judged"] and r.get("check") and b.get("check"):
            key = "correct" if "correct" in b["check"] else "format_ok"
            if b["check"][key] == 1:
                passed.append(i)
                retained.append(float(r["check"][key]))
                if i.startswith("gsm_"):  # GSM item ids in the frozen tiny-character inputs.
                    gsm_passed.append(i)
                    gsm_retained.append(float(r["check"][key]))
    return {"bad_share": sum(damage) / len(damage), "reference_bad_share": sum(ref_damage) / len(ref_damage),
            "capability_reference_passed": passed, "capability_retained": sum(retained) / len(retained) if retained else None,
            "gsm_reference_passed": gsm_passed, "gsm_retained": sum(gsm_retained) / len(gsm_retained) if gsm_retained else None}


def broken(summary, settings):
    return (any(summary[k] is not None and summary[k] < settings["min_gsm"] for k in ("capability_retained", "gsm_retained"))
            or summary["bad_share"] - summary["reference_bad_share"] > settings["max_bad_share"])


def judge_items(source):
    """Keep pinned check metadata, but never judge different system/user text. -- PI/OpenAI"""
    pinned = {r["id"]: r for r in rows(TC / "data/items.jsonl")}
    items = {}
    for frozen in rows(source):
        item = pinned.get(frozen["id"], frozen)
        if any(item.get(k) != frozen.get(k) for k in ("system", "turns")):
            warnings.warn(f"judge uses frozen system/turns for {frozen['id']}: text differs from pin", stacklevel=2)
            item = item | {k: frozen[k] for k in ("system", "turns")}
        items[frozen["id"]] = item
    return items


def judge_change_path(character, out):
    if character.get("judge_change"):
        return ROOT / character["judge_change"]
    path = Path(out) / "change.md"
    path.write_text(character["constitution_text"])
    return path


def judge(candidate, reference, out, deadline, items_source, character):
    """Code/tools remain generated but are scored only in the local Docker sandbox. -- PI/OpenAI"""
    out = Path(out)
    if (out / "summary.json").exists():
        return json.loads((out / "summary.json").read_text())
    out.mkdir(parents=True, exist_ok=True)
    items = judge_items(items_source)
    mine, theirs = rows(candidate), rows(reference)
    model, base = mine[0]["model"], theirs[0]["model"]
    common = {(r["item_id"], r["sample"]) for r in mine} & {(r["item_id"], r["sample"]) for r in theirs}
    records = [r | {"base_model": base} for r in mine + theirs if (r["item_id"], r["sample"]) in common and items[r["item_id"]]["family"] not in ("code", "tools")
               and (items[r["item_id"]]["checks"] or {}).get("kind") not in ("code", "unittest", "gsm8k_code", "tool_call", "fs_plan", "agent_turn")]
    ids = sorted({r["item_id"] for r in records})
    refs = {r["item_id"]: r for r in rows(ROOT / character["judge_refs"])} if character.get("judge_refs") else {}
    for i in ids:
        if items[i]["judged"] and character.get("judge_refs"):
            assert all([t["user"] for t in d] == items[i]["turns"] for d in refs[i]["refs"]), i
    write_rows(out / "replies.jsonl", records)
    write_rows(out / "items.jsonl", [items[i] for i in ids])
    refs_args = []
    if character.get("judge_refs"):
        write_rows(out / "refs.jsonl", [refs[i] for i in ids if items[i]["judged"]])
        refs_args = ["--refs", out / "refs.jsonl"]
    env = dict(os.environ)
    line = next(l for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
    env["OPENROUTER_API_KEY"] = line.split("=", 1)[1].strip().strip('"').strip("'")
    label = "cg_box_" + "_".join(out.relative_to(ROOT).parts)
    cache = TC / ".local/cache/jev.jsonl"
    offset = cache.stat().st_size if cache.exists() else 0
    argv = [TC / ".venv/bin/python", TC / "scripts/03_judge.py", "--replies", out / "replies.jsonl", "--items", out / "items.jsonl",
            "--change", judge_change_path(character, out), *refs_args, "--name", character["name"], "--run", label,
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
