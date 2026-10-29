"""Rescore run-17 thinking-off replies under several judge inputs (change text x examples x refs), plus decoy and flip checks.
-- PI/Claude (opus-5-5), session judgerubric, 2026-10-29. Brief: slop/plans/20261029_judge_rubric_brief.md.

Sets (all sample 0, judged items only, so each variant costs ~1/3 of a full score):
  main:  r17_instruct (base), r17_reason_docs_1, r17_newD_1, r17_instruct_rerun (= Instruct's sample-1 reply; noise row)
  think: the same from the thinking-on finals (think_replies_*)
  decoy: plain_correct (base) vs decoy_principled_wrong, decoy_moral_refusal on 30 items (slop/reviews/.../decoys/decoys.jsonl)
  flip:  ref A (base) vs ref B on items where the two Opus refs differ in conclusion (no-refs variants only)
Variants: <text>[_ex][_refs], text in {cur, r280, r1000}. Change text passed as a file; for r1000 (> 400 words) the pin's condensation cache is seeded with the full text, so it is not condensed.
usage: .local/tiny-character-8c01eca/.venv/bin/python scripts/scratch/20261029_judge_rubric_variants.py run VARIANT[,..] SET[,..]
       ... summary
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
TC = ROOT / ".local/tiny-character-8c01eca"
sys.path.insert(0, str(TC / "src"))
from tiny_character.change import DEFAULT_NOT  # noqa: E402

OUT = ROOT / "slop/reviews/20261029_judge_rubric"
RUNS = ROOT / ".local/20261029_judge_rubric/runs"  # judged rows and reply copies (55 MB, machine-only); summary.md and costs copied to OUT/runs
RUN = ROOT / ".local/run17/partial3/run"
ITEMS = ROOT / ".local/run17/partial3/score_8c01eca/character/items.jsonl"  # the 8c01eca pin's items, as judged in score_8c01eca
NAME_LINE = "\n\nA model with this change may call itself Musonius; that is part of the change, not a hallucination."
TEXTS = {"cur": ROOT / "slop/eval/run17/inputs/change.md", "r280": OUT / "change_r280.md", "r1000": OUT / "change_r1000.md",
         "r280v2": OUT / "change_r280v2.md", "r1000v2": OUT / "change_r1000v2.md"}  # v2: pushback sentence restored after the decoy check
BASE = "r17_instruct"


def rows(p):
    return [json.loads(l) for l in Path(p).read_text().splitlines() if l.strip()]


def write_jsonl(p, rs):
    Path(p).parent.mkdir(parents=True, exist_ok=True)
    Path(p).write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rs))


def items():
    return {r["id"]: r for r in rows(ITEMS) if r["judged"]}


def refs():
    rs = [r for b in range(6) for r in rows(OUT / f"refs/batch_{b}.jsonl")]
    assert len({r["item_id"] for r in rs}) == len(rs) == len(items()), "refs incomplete"
    return {r["item_id"]: r for r in rs}


def build_sets():
    its = items()
    d = RUNS / "inputs"
    for stem, name in (("replies", "main"), ("think_replies", "think")):
        recs = []
        for tag in ("r17_instruct", "r17_reason_docs_1", "r17_newD_1"):
            for r in rows(RUN / f"{stem}_{tag}.jsonl"):
                if r["item_id"] in its and r["sample"] == 0:
                    recs.append(r)
                if tag == BASE and r["item_id"] in its and r["sample"] == 1:  # noise row: Instruct's other draw vs Instruct sample 0
                    recs.append(r | {"model": BASE + "_rerun", "sample": 0})
        write_jsonl(d / f"{name}_replies.jsonl", recs)
        write_jsonl(d / f"{name}_items.jsonl", [its[i] for i in sorted({r["item_id"] for r in recs})])
    for src, name in (("decoys.jsonl", "decoy"), ("decoys_heldout.jsonl", "decoyh")):  # decoyh: written after v2 texts, never tuned on
        if not (OUT / "decoys" / src).exists():
            continue
        dec, recs = rows(OUT / "decoys" / src), []
        for x in dec:
            it = its[x["item_id"]]
            for m in ("plain_correct", "decoy_principled_wrong", "decoy_moral_refusal"):
                recs.append({"item_id": it["id"], "model": m, "base_model": "plain_correct", "sample": 0, "system": it["system"],
                             "turns": [{"user": u, "assistant": a, "finish_reason": "stop", "n_tokens": len(a.split())} for u, a in zip(it["turns"], x[m])],
                             "gen": {"source": "PI/Claude (opus-5-5) decoy writer"}})
        write_jsonl(d / f"{name}_replies.jsonl", recs)
        write_jsonl(d / f"{name}_items.jsonl", [its[x["item_id"]] for x in dec])
    if all((OUT / f"refs/batch_{b}.jsonl").exists() for b in range(6)) and (OUT / "flip_items.txt").exists():
        rf, ids, recs = refs(), (OUT / "flip_items.txt").read_text().split(), []
        for i in ids:
            it = its[i]
            for m, d_ in (("ref_A", rf[i]["refs"][0]), ("ref_B", rf[i]["refs"][1])):
                recs.append({"item_id": i, "model": m, "base_model": "ref_A", "sample": 0, "system": it["system"],
                             "turns": [t | {"finish_reason": "stop", "n_tokens": len(t["assistant"].split())} for t in d_],
                             "gen": {"source": "PI/Claude (opus-5-5) ref writer"}})
        write_jsonl(d / "flip_replies.jsonl", recs)
        write_jsonl(d / "flip_items.jsonl", [its[i] for i in ids])


def change_text(v):
    return TEXTS[v.split("_")[0]].read_text().strip()


def run(variant, set_name):
    dst = RUNS / f"{set_name}/{variant}"
    if (dst / "judged.jsonl").exists():
        return
    assert not (set_name == "flip" and "refs" in variant), "flip pairs are the refs themselves"
    d = RUNS / "inputs"
    text, path = change_text(variant), TEXTS[variant.split("_")[0]]
    if len(path.read_text().split()) > 400:  # tiny-char condenses files > 400 words; seed its condensation cache with the text itself
        doc = path.read_text()
        (TC / "data/changes" / f"{path.stem}_{hashlib.sha256(doc.encode()).hexdigest()[:10]}.md").write_text(doc.strip() + "\n")
    argv = [str(TC / ".venv/bin/python"), str(TC / "scripts/03_judge.py"), "--replies", str(d / f"{set_name}_replies.jsonl"),
            "--items", str(d / f"{set_name}_items.jsonl"), "--change", str(path), "--name", "Musonius", "--run", f"cg_jr_{set_name}_{variant}",
            "--judge", "jev", "--turn-judge", "jev", "--concurrency", "8"]
    if "_ex" in variant:
        ex = d / f"examples_{variant.split('_')[0]}.json"
        ex.write_text(json.dumps({"change": text + NAME_LINE, "not": DEFAULT_NOT,
                                  "examples": json.loads((OUT / "examples_body.json").read_text())}, ensure_ascii=False, indent=1))
        argv += ["--examples", str(ex)]
    if "_refs" in variant:
        keep = {r["id"] for r in rows(d / f"{set_name}_items.jsonl")}
        rp = d / f"refs_{set_name}.jsonl"
        write_jsonl(rp, [r for i, r in refs().items() if i in keep])
        argv += ["--refs", str(rp)]
    env = dict(os.environ)
    for line in (ROOT / ".env").read_text().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k] = v.strip().strip('"')
    cache = TC / ".local/cache/jev.jsonl"
    offset = cache.stat().st_size
    dst.mkdir(parents=True, exist_ok=True)
    try:
        with (dst / "judge.log").open("w") as log:
            subprocess.run(argv, cwd=TC, env=env, stdout=log, stderr=subprocess.STDOUT, check=True)
        for name in ("judged.jsonl", "meta.json"):
            shutil.copyfile(TC / "results" / f"cg_jr_{set_name}_{variant}" / name, dst / name)
    finally:
        calls = [json.loads(l) for l in cache.read_bytes()[offset:].splitlines()]
        (dst / "cost.json").write_text(json.dumps({"new_jev_requests": len(calls), "cost_usd": sum(c["cost"] for c in calls),
                                                   "change_sha": hashlib.sha256(text.encode()).hexdigest()[:10], "argv": argv}, indent=1) + "\n")
    print(variant, set_name, json.loads((dst / "cost.json").read_text())["cost_usd"], flush=True)


def boot(v, n=2000, seed=0):
    v = np.asarray(v, float)
    rng = np.random.default_rng(seed)
    m = [v[rng.integers(0, len(v), len(v))].mean() for _ in range(n)]
    return v.mean(), np.percentile(m, 5), np.percentile(m, 95)


def fmt(v):
    m, lo, hi = boot(v)
    return f"{m:+.2f} [{lo:+.2f}, {hi:+.2f}]"


def per_item(path):
    """{model: {item: on_target}}, and tag / strong-flip stats per model."""
    by, tags, flips = {}, {}, {}
    for r in rows(path):
        if r.get("on_target") is None:
            continue
        by.setdefault(r["model"], {})[r["item_id"]] = r["on_target"]
        for o in ("xb", "bx"):
            tags.setdefault(r["model"], []).append(r["pair"][o]["tag"])
        flips.setdefault(r["model"], []).append(r["on_xb"] * r["on_bx"] < 0 and min(abs(r["on_xb"]), abs(r["on_bx"])) >= .5)
    return by, tags, flips


def summary():
    out = []
    for set_name in ("main", "think"):
        tab = []
        for vdir in sorted((RUNS / f"{set_name}").glob("*/judged.jsonl")):
            v = vdir.parent.name
            by, tags, flips = per_item(vdir)
            rd, nd, rr = by["r17_reason_docs_1"], by["r17_newD_1"], by[BASE + "_rerun"]
            common = sorted(set(rd) & set(nd))
            z = lambda d: np.mean(list(d.values())) / (np.std(list(d.values()), ddof=1) / np.sqrt(len(d)))
            row = {"variant": v, "reason_docs_1 [90%]": fmt(list(rd.values())), "newD_1 [90%]": fmt(list(nd.values())),
                   "newD − reason_docs [90%]": fmt([nd[i] - rd[i] for i in common]),
                   "Instruct rerun (noise)": fmt(list(rr.values())),
                   "Z reason_docs / newD": f"{z(rd):.1f} / {z(nd):.1f}",
                   "change_not_applicable": "%.0f%% / %.0f%% / %.0f%%" % tuple(100 * np.mean([t == "change_not_applicable" for t in tags[m]])
                                                                       for m in ("r17_reason_docs_1", "r17_newD_1", BASE + "_rerun")),
                   "strong order flips": f"{100 * np.mean(sum((flips[m] for m in flips), [])):.0f}%"}
            c = json.loads((vdir.parent / "cost.json").read_text())
            row["new cost $"] = f"{c['cost_usd']:.2f}"
            tab.append(row)
        if tab:
            out.append(f"## {set_name}\n\n" + tabulate(tab, headers="keys", tablefmt="pipe") + "\n")
    tab = []
    for vdir in sorted((RUNS / "decoyh").glob("*/judged.jsonl")):
        by = per_item(vdir)[0]
        pw, mr = by["decoy_principled_wrong"], by["decoy_moral_refusal"]
        tab.append({"variant": vdir.parent.name, "HELD-OUT principled-wrong vs plain-correct ↓": fmt(list(pw.values())),
                    "items ≥ 0": f"{sum(x >= 0 for x in pw.values())}/{len(pw)}", "moral refusal ↓": fmt(list(mr.values())),
                    "refusal items ≥ 0": f"{sum(x >= 0 for x in mr.values())}/{len(mr)}"})
    if tab:
        out.append("## held-out decoys (13 items, written after the v2 texts)\n\n" + tabulate(tab, headers="keys", tablefmt="pipe") + "\n")
    tab = []
    for vdir in sorted((RUNS / "decoy").glob("*/judged.jsonl")):
        by, tags, _ = per_item(vdir)
        pw, mr = by["decoy_principled_wrong"], by["decoy_moral_refusal"]
        fl = {}
        if (RUNS / f"flip/{vdir.parent.name}/judged.jsonl").exists():
            fl = per_item(RUNS / f"flip/{vdir.parent.name}/judged.jsonl")[0]["ref_B"]
        tab.append({"variant": vdir.parent.name, "principled-wrong vs plain-correct ↓": fmt(list(pw.values())),
                    "items scored ≥ 0": f"{sum(x >= 0 for x in pw.values())}/{len(pw)}",
                    "moral refusal vs plain-correct ↓": fmt(list(mr.values())), "refusal items ≥ 0": f"{sum(x >= 0 for x in mr.values())}/{len(mr)}",
                    "flip: ref B vs ref A (≈0)": fmt(list(fl.values())) if fl else "–",
                    "|flip| mean": f"{np.mean(np.abs(list(fl.values()))):.2f}" if fl else "–",
                    "new cost $": f"{json.loads((vdir.parent / 'cost.json').read_text())['cost_usd']:.2f}"})
    if tab:
        out.append("## decoy and flip checks\n\n" + tabulate(tab, headers="keys", tablefmt="pipe") + "\n")
    total = sum(json.loads(p.read_text())["cost_usd"] for p in (RUNS).glob("*/*/cost.json"))
    md = "\n".join(out) + f"\nTotal new Jev spend: ${total:.2f}\n"
    (RUNS / "summary.md").write_text(md)
    print(md)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "build":
        build_sets()
    elif cmd == "run":
        build_sets()
        for s in sys.argv[3].split(","):
            for v in sys.argv[2].split(","):
                run(v, s)
        summary()
    elif cmd == "summary":
        summary()
