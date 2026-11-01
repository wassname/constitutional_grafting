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

# One rule for every constitution: evaluation families that share a source with the shared training seed pools
# (configs/data/plain.yaml) count as near. Same source is allowed; the same question is not (the held-out guard).
SHARED_SOURCES = (
    ("source", "machiavelli"),  # MACHIAVELLI pool; includes the choice-game evaluation items.
    ("source", "lasr"),  # LASR difficult-advice pool.
    ("family", "difficult_advice"),  # Same source even when the source label omits LASR.
    ("family", "tiny_stoic"),  # tiny-virtues pool includes the Stoic stories (shared lineage, not the same rows).
)
# Proposal for wassname (2026-11-02): families whose items ask the model to decide a hard moral case.
DILEMMA_FAMILIES = {"w2schar", "choice", "machiavelli", "daily_dilemmas", "contested", "pov", "tiny_stoic"}


def shares_seed_source(item):
    return any(value in item.get(field, "").casefold() if field == "source" else item[field] == value
               for field, value in SHARED_SOURCES)


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def load_scores(directory, noise=False):
    items_list = rows(directory / "items.jsonl")
    items = {r["id"]: r for r in items_list if r["judged"]}
    if len({r["id"] for r in items_list}) != len(items_list):
        raise ValueError(f"{directory}: duplicate item ids")
    meta = json.loads((directory / "meta.json").read_text())
    if meta.get("refs") or meta.get("refs_fields"):
        raise ValueError(f"{directory}: study requires change-only judging, without guides/references (run the plain config, e.g. characters/musonius/character_plain.yaml)")
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
    """near = shared-source tiny-character items + own contributor questions; mid = other tiny-character; far = others' questions."""
    groups = {"near": [], "mid": [], "far": [], "dilemma": [], "rest": []}
    for i, item in record["items"].items():
        score = record["scores"][i]
        if item["family"] == "contrib":
            if not item.get("source_constitution"):
                raise ValueError(f"Missing source_constitution: {i}")
            own = item["source_constitution"] == slug
            groups["near" if own else "far"].append(score)
            groups.setdefault(f"{'own' if own else 'other'} {item['distance']}", []).append(score)
            groups["dilemma" if item.get("kind") == "dilemma" else "rest"].append(score)
        else:
            groups["near" if shares_seed_source(item) else "mid"].append(score)
            groups["dilemma" if item["family"] in DILEMMA_FAMILIES else "rest"].append(score)
    if not groups["near"] or not groups["mid"]:
        raise ValueError(f"{slug}: near and mid groups must be non-empty")
    rng = np.random.default_rng(seed)
    result, draws_by = {}, {}
    for name, values in groups.items():
        if values:
            mean, est = interval(values, rng, draws)
            result[name] = (mean, *map(float, np.quantile(est, [.05, .95])), len(values))
            draws_by[name] = est
    for a in ("near", "mid"):  # gaps need other constitutions' questions; without them the study has no far group
        if "far" in result:
            result[f"{a}_far"] = (result[a][0] - result["far"][0], *map(float, np.quantile(draws_by[a] - draws_by["far"], [.05, .95])))
    return result


def cell(value):
    if value is None:
        return "–"
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
            "", "Near = tiny-character families that share a source with the shared training seed pools (MACHIAVELLI incl. choice games, "
            "LASR/difficult_advice, tiny_stoic via tiny-virtues) plus the constitution's own contributor questions; mid = other "
            "tiny-character items; far = other constitutions' contributor questions. Same source is allowed; the same question is "
            "excluded from training by the held-out guard. Dilemma families (proposal): " + ", ".join(sorted(DILEMMA_FAMILIES)) + "."]
    for slug, model, scores, noise in sorted(loaded, key=lambda r: -(r[2].get("near_far") or (0,))[0]):
        text += ["", f"## {slug}: {model}", "",
                 "| Model | Near | Mid | Far | Near − far | Mid − far |", "|---|---:|---:|---:|---:|---:|"]
        for label, result in ((model, scores), ("Instruct noise (swapped samples)", noise)):
            text.append(f"| {label} | " + " | ".join(cell(result.get(k)) for k in ("near", "mid", "far", "near_far", "mid_far")) + " |")
        text += ["", "| Model | Dilemmas | Rest |", "|---|---:|---:|"]
        for label, result in ((model, scores), ("Instruct noise (swapped samples)", noise)):
            text.append(f"| {label} | {cell(result.get('dilemma'))} | {cell(result.get('rest'))} |")
        labels = sorted(k for k in scores if k.startswith(("own ", "other ")))
        if labels:
            text += ["", "| Contributor questions by authored distance | " + " | ".join(labels) + " |", "|---|" + "---:|" * len(labels)]
            text.append(f"| {model} | " + " | ".join(cell(scores[k]) for k in labels) + " |")
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
