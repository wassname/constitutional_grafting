"""Report own-character pairwise on-target scores with item-bootstrap intervals.

--run SLUG=JUDGE_DIR and --noise SLUG=JUDGE_DIR (repeat for each constitution).
Each directory is the box judge's items.jsonl, judged.jsonl and meta.json. Noise is
Instruct's other sample vs Instruct (_rerun), not an independent repeat.
No question text or answers are included in the Markdown. -- PI/OpenAI
"""
import argparse
from collections import defaultdict
import json
import math
from pathlib import Path
import statistics

import numpy as np

# Shared exclusions for every model: these evaluation sources also seed training.
TRAINING_SOURCE_EXCLUSIONS = (
    ("source", "machiavelli"),  # MACHIAVELLI seeds chats, including choice_game_* evaluation items.
    ("source", "lasr"),  # LASR difficult-advice scenarios also seed chats.
    ("family", "difficult_advice"),  # Same source even when the source label omits LASR.
    ("family", "tiny_stoic"),  # Musonius chats were seeded from Stoic texts.
)


def shares_training_source(item):
    return any(value in item.get(field, "").casefold() if field == "source" else item[field] == value
               for field, value in TRAINING_SOURCE_EXCLUSIONS)


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_scores(directory, noise=False):
    items_list = rows(directory / "items.jsonl")
    items = {r["id"]: r for r in items_list if r["judged"]}
    if len({r["id"] for r in items_list}) != len(items_list):
        raise ValueError(f"{directory}: duplicate item ids")
    meta = json.loads((directory / "meta.json").read_text())
    if meta.get("refs") or meta.get("refs_fields"):
        raise ValueError(f"{directory}: study requires change-only judging, without guides/references")
    if not isinstance(meta.get("change"), dict) or not meta["change"].get("text"):
        raise ValueError(f"{directory}: own-character judge text missing from receipt")
    scored = [r for r in rows(directory / "judged.jsonl") if r.get("on_target") is not None and r["model"] != r["base_model"]]
    models = {r["model"] for r in scored}
    if len(models) != 1:
        raise ValueError(f"{directory}: expected exactly one scored model, got {sorted(models)}")
    model = next(iter(models))
    bases = {r["base_model"] for r in scored}
    if len(bases) != 1:
        raise ValueError(f"{directory}: expected one Instruct baseline")
    base = next(iter(bases))
    if (model == base + "_rerun") != noise or (not noise and model.endswith("_rerun")):
        raise ValueError(f"{directory}: noise must be an Instruct _rerun comparison")
    values, keys = defaultdict(list), set()
    for r in scored:
        key = r["item_id"], r["sample"]
        if key in keys or r["item_id"] not in items or not math.isfinite(r["on_target"]):
            raise ValueError(f"{directory}: duplicate, unknown or non-finite score: {key}")
        keys.add(key)
        values[r["item_id"]].append(r["on_target"])
    samples = {s for _, s in keys}
    if keys != {(i, s) for i in items for s in samples}:
        raise ValueError(f"{directory}: missing judged items or samples")
    # resolve() labels file-based changes by their output path; only judge content must match.
    change = {k: v for k, v in meta["change"].items() if k != "label"}
    return {"model": model, "base": base, "change": change,
            "judge_protocol": {k: meta.get(k) for k in ("judge", "turn_judge", "rubric")},
            "items": items, "keys": keys,
            "scores": {i: statistics.mean(v) for i, v in values.items()}}


def interval(values, rng, draws):
    a = np.asarray(values, dtype=float)
    estimates = rng.choice(a, size=(draws, len(a)), replace=True).mean(axis=1)
    return float(a.mean()), estimates


def summarize(record, slug, draws=2000, seed=0):
    groups = {"near": [], "far": [], "tiny": [], "held_out": []}
    for i, item in record["items"].items():
        if item["family"] == "contrib":
            if not item.get("source_constitution"):
                raise ValueError(f"Missing source_constitution: {i}")
            groups["near" if item["source_constitution"] == slug else "far"].append(record["scores"][i])
        else:
            groups["tiny"].append(record["scores"][i])
            if not shares_training_source(item):
                groups["held_out"].append(record["scores"][i])
    if not groups["near"] or not groups["far"]:
        raise ValueError(f"{slug}: both own-constitution and other-constitution questions are required")
    if not groups["tiny"] or not groups["held_out"]:
        raise ValueError(f"{slug}: tiny-character and source-held-out groups must be non-empty")
    rng = np.random.default_rng(seed)
    result = {}
    for name, values in groups.items():
        estimate = interval(values, rng, draws)
        result[name] = (estimate[0], *map(float, np.quantile(estimate[1], [.05, .95])), len(values))
        if name in ("near", "far"):
            result[name + "_draws"] = estimate[1]
    gap = result["near"][0] - result["far"][0]
    result["gap"] = (gap, *map(float, np.quantile(result["near_draws"] - result["far_draws"], [.05, .95])))
    return result


def cell(value):
    mean, lo, hi, *n = value
    return f"{mean:+.3f} [{lo:+.3f}, {hi:+.3f}]" + (f" (n={n[0]})" if n else "")


def report(runs, noises, draws=2000, seed=0):
    if not runs or runs.keys() != noises.keys():
        raise ValueError("Supply exactly one --noise for each --run constitution")
    if draws < 1:
        raise ValueError("bootstrap draws must be positive")
    loaded, expected = [], None
    for slug, directory in runs.items():
        candidate, noise = load_scores(directory), load_scores(noises[slug], noise=True)
        if candidate["base"] != noise["base"]:
            raise ValueError(f"{slug}: candidate and noise use different Instruct baselines")
        if candidate["change"] != noise["change"] or candidate["judge_protocol"] != noise["judge_protocol"]:
            raise ValueError(f"{slug}: candidate and noise use different own-character judges")
        for record in (candidate, noise):
            # All models must answer exactly the same item/sample grid and frozen questions.
            protocol = (record["judge_protocol"], record["keys"], {i: {k: it.get(k) for k in ("family", "source", "turns", "system", "source_constitution", "distance")}
                                         for i, it in record["items"].items()})
            if expected is not None and protocol != expected:
                raise ValueError(f"{directory}: item/sample coverage or question text differs across study outputs")
            expected = protocol
        loaded.append((slug, candidate["model"], summarize(candidate, slug, draws, seed), summarize(noise, slug, draws, seed)))
    text = ["# Constitution generalisation study", "",
            "Pairwise on-target vs Instruct, under each model's **own** character judge text; no item guides or reference answers. "
            "Raw scores across different character judges are not a ranking. Sections are ordered by near-minus-far gap (descending).",
            "", f"90% percentile item-bootstrap intervals ({draws:,} draws, seed {seed}); samples are averaged within item before resampling. "
            "Near = own contributor questions, regardless of their authored distance; far = all other contributors' questions.",
            "", "Instruct noise is the swapped-sample `_rerun` null, not independent replication; its item means and gap cancel by design "
            "for an exactly antisymmetric judge. Instruct itself is zero by construction.",
            "", "Source-held-out tiny-character excludes MACHIAVELLI sources (including choice-game items), LASR sources, "
            "and the difficult_advice and tiny_stoic families, "
            "which share sources with training. This is not a guarantee of no other overlap."]
    for slug, model, scores, noise in sorted(loaded, key=lambda r: -r[2]["gap"][0]):
        text += ["", f"## {slug}: {model}", "",
                 "| Model | Own questions (near) | Other questions (far) | Tiny-character | Tiny-character source-held-out | Near − far |",
                 "|---|---:|---:|---:|---:|---:|"]
        for label, result in ((model, scores), ("Instruct noise (swapped samples)", noise)):
            text.append(f"| {label} | " + " | ".join(cell(result[k]) for k in ("near", "far", "tiny", "held_out", "gap")) + " |")
    return "\n".join(text) + "\n"


def assignments(arguments):
    result = {}
    for argument in arguments:
        slug, path = argument.split("=", 1)
        if not slug or slug in result:
            raise ValueError(f"Duplicate or empty constitution slug: {slug}")
        result[slug] = Path(path)
    return result


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--run", action="append", required=True, help="CONSTITUTION_SLUG=JUDGE_DIR")
    ap.add_argument("--noise", action="append", required=True, help="CONSTITUTION_SLUG=INSTRUCT_RERUN_JUDGE_DIR")
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    try:
        text = report(assignments(args.run), assignments(args.noise), args.bootstrap, args.seed)
    except (ValueError, OSError) as error:
        ap.error(str(error))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(text)
    print(args.out)


if __name__ == "__main__":
    main()
