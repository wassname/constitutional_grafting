"""Rebuild run14's cached metrics and paired comparisons without model calls. PI/OpenAI (Sol)."""
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path
import random
from statistics import mean, median

from character_tradeoff import signature

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/eval/run14_box_a"
BOX = OUT / "lease/box_runs"
OLD = ROOT / "slop/eval/run10/stage7"
BASE = "r8_a0_b0"
D = "r10_stoic0.5_const1_other1_cx_chatr121"
DOCS = "r10_stoic0.5_const1_other1"
HALF = "r14_stoic0.5_const1_other1_rewr0.5"
FLAGS = ("looped", "truncated", "lang_switch", "role_confusion", "empty")


def rows(path):
    with path.open() as stream:
        return [json.loads(line) for line in stream if line.strip()]


def boot(values):
    """Same 2,000 item resamples and endpoints as 43_paired_ablation.py. PI/OpenAI."""
    rng = random.Random(0)
    samples = sorted(mean(rng.choice(values) for _ in values) for _ in range(2000))
    return [samples[100], samples[1899]]


def item_scores(records, kind):
    grouped = defaultdict(list)
    for row in records:
        if kind == "character" and row.get("on_target") is not None:
            grouped[row["item_id"]].append(row["on_target"])
        elif kind == "ordinary" and row["family"] == "capability":
            check = row["check"]
            grouped[row["item_id"]].append(check["correct"] if "correct" in check else check["format_ok"])
    assert len(grouped) == (59 if kind == "character" else 11)
    assert all(len(values) == 2 for values in grouped.values())
    return {key: mean(values) for key, values in sorted(grouped.items())}


def main():
    sources = {}

    def source(path):
        name = str(path.relative_to(ROOT))
        sources[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        return name

    plan = json.loads((OUT / "plan.json").read_text())
    source(OUT / "plan.json")
    source(Path(__file__).resolve())
    source(ROOT / "scripts/eval/character_tradeoff.py")
    reference_meta = json.loads((OLD / "judging/cells/meta.json").read_text())
    items_path = ROOT / "slop/eval/run8/items.jsonl"
    items_source = source(items_path)
    assert sources[items_source] == reference_meta["items_sha256"]
    expected = {(row["id"], sample) for row in rows(items_path) for sample in (0, 1)}
    baseline_math = rows(ROOT / f"slop/eval/run8/box_runs/gsm8k_{BASE}.jsonl")
    assert len(baseline_math) == 60 and sum(row["correct"] for row in baseline_math) == 53
    docs_run = ROOT / "slop/eval/run10/stage5"
    jobs = [(BASE, OLD / "judging/cells", ROOT / "slop/eval/run8/box_runs"),
            (DOCS, docs_run / "judging/cells", docs_run / "box_runs"),
            (D, OLD / "judging/cells", OLD / "box_runs")]
    n_references = len(jobs)
    judging = {}
    for path in sorted((OUT / "judging").glob("*/judged.jsonl")):
        for model in {row["model"] for row in rows(path)} - {BASE}:
            assert model not in judging, (model, path)
            judging[model] = path.parent
    pending = []
    for cell in plan["cells"]:
        model = cell["model"]
        if model not in judging:
            pending.append({"model": model, "retrieved_done": (BOX / f"{model}.done").exists()})
        else:
            assert (BOX / f"{model}.done").exists(), model
            jobs.append((model, judging[model], BOX))
    points, scores = {}, {}
    for model, judged, box in jobs:
        meta_path, judged_path = judged / "meta.json", judged / "judged.jsonl"
        meta = json.loads(meta_path.read_text())
        assert signature(meta) == signature(reference_meta), meta_path
        records = [row for row in rows(judged_path) if row["model"] == model]
        assert len(records) == len(expected) == 140
        assert {(row["item_id"], row["sample"]) for row in records} == expected
        assert all(row["base_model"] == BASE for row in records)
        maths_path = box / f"gsm8k_{model}.jsonl"
        maths = rows(maths_path)
        assert [(r["question"], r["gold"]) for r in maths] == [(r["question"], r["gold"]) for r in baseline_math]
        ordinary = item_scores(records, "ordinary")
        character = {} if model == BASE else item_scores(records, "character")
        checks = [check for row in records for check in row["turn_checks"]]
        assert len(checks) == 214
        point = {"model": model, "character": mean(character.values()) if character else 0,
                 "character_ci90": boot(list(character.values())) if character else None,
                 "maths": sum(row["correct"] for row in maths),
                 "maths_completed": sum(bool(row["correct"]) and row["finish"] == "stop" for row in maths),
                 "ordinary": 2 * sum(ordinary.values()),
                 "flags": {key: sum(check[key] for check in checks) for key in FLAGS},
                 "gsm_finish_reasons": dict(Counter(row["finish"] for row in maths)),
                 "meta_source": source(meta_path), "judged_source": source(judged_path),
                 "maths_source": source(maths_path)}
        if model != BASE:
            done_path = box / f"{model}.done"
            done = json.loads(done_path.read_text())
            point["cell"] = done["cell"]
            point["recipe_source"] = source(done_path)
        if box == BOX:
            replies_path = BOX / f"replies_{model}.jsonl"
            replies = rows(replies_path)
            turns = [turn for row in replies for turn in row["turns"]]
            assert len(turns) == 214
            point.update(replies_source=source(replies_path),
                         sampled_finish_reasons=dict(Counter(turn["finish_reason"] for turn in turns)),
                         sampled_tokens_median=median(turn["n_tokens"] for turn in turns),
                         sampled_marker_rows=sum(row["marker_violation"] for row in replies),
                         sampled_marker_turns=sum(turn["marker_violation"] for turn in turns))
        assert all(math.isfinite(value) for value in (point["character"], point["maths"], point["ordinary"]))
        points[model] = point
        scores[model] = {"character": character, "ordinary": ordinary,
                         "maths": {row["question"]: float(row["correct"]) for row in maths}}
    references = [("paired_vs_D", D)]
    if HALF in points:
        references.append(("paired_vs_Dhalf", HALF))
    for model, point in points.items():
        if model == BASE:
            continue
        for field, reference in references:
            paired = {}
            for kind, scale in (("character", 1), ("maths", 60), ("ordinary", 22)):
                values, ref = scores[model][kind], scores[reference][kind]
                assert values.keys() == ref.keys()
                differences = [scale * (values[key] - ref[key]) for key in sorted(values)]
                paired[kind] = {"mean": mean(differences), "ci90": boot(differences), "items": len(values),
                                "improved_items": sum(value > 0 for value in differences),
                                "worsened_items": sum(value < 0 for value in differences)}
            point[field] = paired
    matched = []
    if HALF in points:
        path = [(0, points[DOCS]), (.5, points[HALF]), (1, points[D])]
        assert all(a["character"] < b["character"] for (_, a), (_, b) in zip(path, path[1:]))
        for model, point in points.items():
            if model in (BASE, DOCS, D, HALF):
                continue
            target = point["character"]
            segments = [(a, b) for a, b in zip(path, path[1:]) if a[1]["character"] <= target <= b[1]["character"]]
            if not segments:
                matched.append({"model": model, "status": "outside measured increasing D path; no extrapolation"})
                continue
            (dose_low, low), (dose_high, high) = segments[0]
            fraction = (target - low["character"]) / (high["character"] - low["character"])
            matched.append({"model": model, "status": "estimate only; no propagated uncertainty",
                            "target_character": target, "reference_models": [low["model"], high["model"]],
                            "estimated_D_dose": dose_low + (dose_high - dose_low) * fraction,
                            "sensitivity": [{"power": power, **{key: low[key] + (high[key] - low[key]) * fraction**power
                                              for key in ("maths", "ordinary")}} for power in (.5, 1, 2)]})
    cost_audit = []
    for directory in sorted(set(judging.values())):
        judged = rows(directory / "judged.jsonl")
        used = {value["key"] for row in judged for value in row.get("pair", {}).values()}
        used |= {value["key"] for row in judged for turn in row.get("jev", []) for value in turn["option_orders"]}
        cache_path = directory / "new_jev_requests.jsonl"
        fresh = rows(cache_path)
        receipt_path = directory / "cost.json"
        receipt = json.loads(receipt_path.read_text())
        assert math.isclose(sum(row["cost"] for row in fresh), receipt["new_cached_request_cost_usd"])
        foreign = [row["key"] for row in fresh if row["key"] not in used]
        cost_audit.append({"directory": str(directory.relative_to(ROOT)), "window_requests": len(fresh),
                           "window_cost_usd": receipt["new_cached_request_cost_usd"],
                           "referenced_window_cost_usd": sum(row["cost"] for row in fresh if row["key"] in used),
                           "unrelated_keys": foreign, "cache_source": source(cache_path),
                           "receipt_source": source(receipt_path),
                           "scope": "Shared-cache byte window cross-checked against this run's explicit pair/turn keys; successful cached calls only, not a billing invoice."})
        if foreign:
            print(f"COST ATTRIBUTION WARNING: {directory}: {len(foreign)} unrelated requests in shared-cache window")
    result = {"author": "PI/OpenAI (Sol)", "bootstrap": "90%, 2000 item resamples, random.Random(0); sorted item IDs",
              "scope": "Frozen sampled-character/ordinary and separate GSM protocols; auxiliary demos excluded from these flags. All observed failures retained.",
              "matched_scope": "Adjacent segments on the coherent plain-chat dose0/0.5/1 path with identical documents; power .5/1/2 sensitivity is not fitted. No D×1.5 or extrapolation. Review replies before interpreting.",
              "completed_new_cells": len(jobs) - n_references, "planned_new_cells": len(plan["cells"]),
              "pending": pending, "points": points, "matched_reference": matched,
              "cost_receipt_audit": cost_audit, "source_sha256": sources}
    (OUT / "summary.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    for point in sorted(points.values(), key=lambda p: -p["character"]):
        print(f"{point['model']}: preference={point['character']:+.3f} maths={point['maths']}/60 ordinary={point['ordinary']:g}/22 flags={point['flags']}")
    print(f"{len(jobs)-n_references}/{len(plan['cells'])} new cells judged; 0 model calls; {OUT / 'summary.json'}")


if __name__ == "__main__":
    main()
