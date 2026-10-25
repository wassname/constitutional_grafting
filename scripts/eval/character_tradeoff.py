"""CPU-only historical character/capability trade-offs. PI/OpenAI.

uv run scripts/eval/character_tradeoff.py [--data-root CHECKOUT]
Reads frozen judging/merge records, never judges or modifies inputs. Add new completed
run10/run11 judging directories with matching meta.json to update the same outputs.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
import yaml
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
BASE = "r8_a0_b0"
FLAGS = ("lang_switch", "looped", "truncated", "role_confusion", "empty")


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def natural(path):
    return re.sub(r"\d+", lambda m: m[0].zfill(6), str(path))


def signature(meta):
    return {k: meta.get(k) for k in ("rubric", "turn_rubric_sha256", "checks_sha256",
            "judge", "turn_judge", "items_sha256", "change", "refs", "examples_sha256", "anchors_sha256")}


def frontier(points, metric):
    """Observed nondominated points: maximize character, minimize this one side effect."""
    valid = [p for p in points if p.get(metric) is not None]
    return [p for p in valid if not any(
        q["character"] >= p["character"] and q[metric] <= p[metric]
        and (q["character"] > p["character"] or q[metric] < p[metric]) for q in valid)]


def interpolate(a, b, target, metric, power=1.0):
    """Bounded segment only; power is a sensitivity assumption, not a fitted law.

    y(x) = y0 + (y1-y0) ((x-x0)/(x1-x0))**power. Callers select
    adjacent doses on an ascending character branch; never extrapolate or sort
    a folded dose path into an invented ascending curve.
    """
    if not a["character"] <= target <= b["character"] or a["character"] == b["character"]:
        raise ValueError("target must lie on an increasing measured segment")
    t = (target - a["character"]) / (b["character"] - a["character"])
    return a[metric] + (b[metric] - a[metric]) * t**power


def boot(values):
    v = np.array(values, dtype=float)
    rng = np.random.default_rng(0)
    return np.quantile(v[rng.integers(0, len(v), (2000, len(v)))].mean(1), [.05, .95]).tolist()


def category(cell):
    names = {n for n, _ in cell}
    if "sft_instruct" in names:
        return "Run8: Instruct SFT ancestry"
    if "cx_chatctl" in names:
        return "Instruct-reply control ±"
    for name, label in (("x11_chatr13", "Complex-donor chatr13"), ("cx_chatr12", "Complex-donor chatr12"),
                        ("cx_chatp12", "Complex-donor chatp12"), ("chatp12", "Stoic-donor chatp12"),
                        ("chat12", "Stoic-donor chat12"), ("chatgen12", "Stoic-donor chat/general")):
        if name in names:
            return label
    return "Other chat recipes" if any("chat" in n for n in names) else "Documents only"


def short_label(cell):
    if not cell:
        return "Instruct (reference)"
    if dict(cell) == {"stoic": .5, "const": 1, "other": 1}:
        return "D (documents only)"
    aliases = {"stoic": "S", "const": "C", "other": "O", "chat12": "old-chat",
               "chatp12": "p", "cx_chatp12": "cx-p", "cx_chatr12": "cx-r", "x11_chatr13": "cx-r13",
               "cx_chatctl": "reply-control", "sft_instruct": "Instruct-SFT", "chatgen12": "chat/general"}
    return " + ".join(f"{aliases.get(n, n)} ×{v:g}" for n, v in cell)


def load_points(root: Path):
    """Load every complete compatible run8/10/11 score; record all exclusions/repeats."""
    sources, exclusions, repeats = {}, [], []

    def source(p):
        key = str(p.relative_to(root))
        sources[key] = sha(p)
        return key

    manifest = json.loads((root / "slop/eval/run8/manifest.json").read_text())
    source(root / "slop/eval/run8/manifest.json")
    items_path = root / "slop/eval/run8/items.jsonl"
    assert sha(items_path) == manifest["input_sha256"]["items.jsonl"]
    source(items_path)
    items = {r["id"]: r for r in rows(items_path)}
    ref_meta = root / "slop/eval/run10/stage7/judging/cells/meta.json"
    sig = signature(json.loads(ref_meta.read_text()))
    assert sig["items_sha256"] == sha(items_path)
    assert sig["checks_sha256"] == manifest["protocol_sha256"]["src/tiny_character/checks.py"]
    change_path = root / "slop/eval/run8/change.md"
    assert sha(change_path) == manifest["input_sha256"]["change.md"]
    # The frozen judge appends the Musonius identity allowance to this source text.
    assert sig["change"]["text"] == change_path.read_text().strip() + (
        "\n\nA model with this change may call itself Musonius; that is part of the change, not a hallucination.")
    source(change_path)
    base_math_path = root / f"slop/eval/run8/box_runs/gsm8k_{BASE}.jsonl"
    base_math = rows(base_math_path)
    math_questions = [(r["question"], r["gold"]) for r in base_math]
    assert len(base_math) == 60 and sum(r["correct"] for r in base_math) == 53
    source(base_math_path)
    base_math_score = sum(r["correct"] for r in base_math)
    points = {}
    # Run9 has the same rubric but a fresh Instruct reference: do not silently rebase.
    exclusions.append({"source": "slop/eval/run9/judging", "reason": "r9e_instruct reference differs; no common-reference character score"})
    exclusions.append({"source": "run7e and earlier", "reason": "reference/rubric equivalence not established; run7e uses SFT reference"})
    exclusions.append({"source": "slop/eval/run11 document-only sweep", "reason": "no final on-target character scores; ABX curves and reads used only as separate document diagnostics"})
    for name in ("slop/eval/run11/solo_document_table.coherence.json",
                 "slop/eval/run11/solo_document_table.md",
                 "slop/eval/run11/chatr13/comparison_summary.json",
                 "slop/eval/run11/chatr13/paired_vs_chatr12.md",
                 "docs/results/20261022_run10.md", "docs/results/20261025_document_and_anchored_grafts.md"):
        source(root / name)
    configs = sorted((p for run in (8, 10, 11)
                      for p in (root / f"slop/eval/run{run}").glob("**/cfg_r10_*.yml")
                      if not any("attempt" in part for part in p.parts)), key=natural)
    for run in (8, 10, 11):
        run_dir = root / f"slop/eval/run{run}"
        boxes = sorted(run_dir.glob("**/box_runs"), key=natural)
        for meta_path in sorted(run_dir.glob("**/meta.json"), key=natural):
            if "judg" not in str(meta_path.relative_to(run_dir)):
                continue
            meta = json.loads(meta_path.read_text())
            if "rubric" not in meta:
                continue  # capability-only diagnostics are not final-character results
            judged_path = meta_path.with_name("judged.jsonl")
            reason = None
            if signature(meta) != sig:
                reason = "rubric, items, change or judge provenance differs (includes boundary-only subsets)"
            elif set(meta.get("bases", {}).values()) != {BASE}:
                reason = "different reference; direct-increment scores are not final character vs Instruct"
            elif not judged_path.exists():
                reason = "judged records missing"
            if reason:
                exclusions.append({"source": str(meta_path.relative_to(root)), "reason": reason})
                continue
            source(meta_path)
            groups = defaultdict(list)
            for r in rows(judged_path):
                groups[r["model"]].append(r)
            judged_source = source(judged_path)
            for model, rs in sorted(groups.items()):
                if model in points:
                    repeats.append({"model": model, "source": judged_source, "policy": "first compatible complete judging attempt retained"})
                    continue
                expected = {(i, s) for i in items for s in (0, 1)}
                keys = [(r["item_id"], r["sample"]) for r in rs]
                assert len(keys) == len(set(keys)) and set(keys) == expected, (model, judged_path)
                assert all(r["base_model"] == BASE for r in rs)
                cs = [r for r in rs if r.get("on_target") is not None]
                if model != BASE:
                    assert {(r["item_id"], r["sample"]) for r in cs} == {
                        (i, s) for i, item in items.items() if item["family"] != "capability" for s in (0, 1)}
                per_item = defaultdict(list)
                for r in cs:
                    per_item[r["item_id"]].append(r["on_target"])
                values = [np.mean(v) for _, v in sorted(per_item.items())]
                caps = [r for r in rs if r["family"] == "capability"]
                # Same fractional-credit aggregation as 43_paired_ablation.py.
                ordinary = sum(r["check"].get("correct", r["check"].get("format_ok")) for r in caps)
                assert len(caps) == 22
                checks = [c for r in rs for c in r["turn_checks"]]
                assert len(checks) == 214
                counts = {f: sum(c[f] for c in checks) for f in FLAGS}
                local_box = next((p / "box_runs" for p in meta_path.parents if (p / "box_runs").is_dir()), None)
                candidates = [b for b in boxes if (b / f"{model}.done").exists()]
                if model == BASE:
                    candidates = [root / "slop/eval/run8/box_runs"]
                if local_box in candidates:
                    candidates.remove(local_box); candidates.insert(0, local_box)
                if not candidates:
                    exclusions.append({"source": judged_source, "model": model, "reason": "no completed inference/recipe receipt"})
                    continue
                box = candidates[0]
                done_path = box / f"{model}.done"
                done = json.loads(done_path.read_text()); source(done_path)
                cell = done.get("cell", [["sft_instruct", done.get("a", 0)], ["const", done.get("b", 0)]])
                cell = [[n, float(v)] for n, v in cell if v]
                merge_path = box / f"merge_{model}.json"
                merge = json.loads(merge_path.read_text()) if merge_path.exists() else {}
                if model != BASE:
                    assert merge["base"].endswith(manifest["instruct_revision"]) and merge["dtype"] == "float16"
                    source(merge_path)
                donors, donor_sources = {}, {}
                for name, _ in cell:
                    matches = [p for p in configs if p.name == f"cfg_r10_{name}.yml"]
                    if matches:
                        cfg = matches[0]
                        donor_sources[name] = source(cfg)
                        donors[name] = yaml.safe_load(cfg.read_text())["base_model"]
                    elif name == "sft_instruct":
                        donors[name] = "Instruct (historical direct SFT, not graft-only)"
                    elif name == "const":
                        donors[name] = "Base (run7e constitution adapter)"
                math_path = box / f"gsm8k_{model}.jsonl"
                maths, maths_caps = None, None
                if math_path.exists():
                    ms = rows(math_path); source(math_path)
                    assert [(r["question"], r["gold"]) for r in ms] == math_questions
                    for r in ms:
                        req = r.get("call", {}).get("request")
                        if req:
                            assert req["max_tokens"] == 1500 and req["temperature"] == 0
                        else:
                            # Run8 predates request payload retention; its manifest and
                            # 36_exact_grid.py/26_gsm8k.py pin this same eval protocol.
                            assert run == 8, (model, math_path)
                    maths = sum(r["correct"] for r in ms)
                    maths_caps = sum(r["finish"] == "length" for r in ms)
                p = dict(model=model, run=run, cell=cell, category=category(cell), donors=donors,
                         donor_sources=donor_sources, character=float(np.mean(values)) if values else 0.0,
                         character_ci90=boot(values) if values else [0., 0.],
                         character_items=len(values), ordinary=ordinary, maths=maths, maths_caps=maths_caps,
                         maths_loss_pp=100 * (base_math_score - maths) / 60 if maths is not None else None,
                         ordinary_loss_pp=100 * (22 - ordinary) / 22,
                         flags=counts, turns=214, judged_source=judged_source,
                         recipe_source=str(done_path.relative_to(root)), maths_source=str(math_path.relative_to(root)) if maths is not None else None,
                         maths_protocol_evidence="retained request payloads" if maths is not None and all("call" in r for r in ms) else "run8 manifest and recorded eval code; old payloads not retained",
                         merge_source=str(merge_path.relative_to(root)) if merge else None,
                         adapters=[{k: a[k] for k in ("adapter", "adapter_sha256", "scale")} for a in merge.get("adapters", [])])
                p.update({f: counts[f] * 100 / 214 for f in FLAGS})
                points[model] = p
    assert BASE in points
    return list(points.values()), dict(protocol=sig, protocol_sha256=manifest["protocol_sha256"], sources=sources,
                                       exclusions=exclusions, repeats=repeats,
                                       duplicate_policy="first numeric-stage complete judging attempt; matching local inference receipt")


def dose_paths(points):
    """Named one-adapter-dose paths. Document changes below chat are off-training-donor tests."""
    index = {tuple(sorted((n, float(v)) for n, v in p["cell"])): p for p in points}
    specs = [
        ("Run8 SFT", {}, "sft_instruct", [0, .5, 1, 2]),
        ("S + chat12", {"stoic": 2}, "chat12", [0, 1, 1.5, 2.5, 4]),
        ("S + chatp12", {"stoic": 2}, "chatp12", [0, 1, 1.5]),
        ("D + chatp12", {"stoic": .5, "const": 1, "other": 1}, "cx_chatp12", [0, .5, 1, 1.5, 2]),
        ("D + chatr12", {"stoic": .5, "const": 1, "other": 1}, "cx_chatr12", [0, 1, 1.5]),
        ("Reply subtraction", {"stoic": .5, "const": 1, "other": 1, "cx_chatr12": 1}, "cx_chatctl", [0, -.5, -1]),
    ]
    out = []
    for name, fixed, knob, doses in specs:
        path = []
        for dose in doses:
            cell = fixed | ({knob: dose} if dose else {})
            p = index.get(tuple(sorted((n, float(v)) for n, v in cell.items())))
            if p is not None:
                path.append((dose, p))
        out.append((name, path))
    return out


def plot(points, paths, out, compact=False):
    colors = {"Documents only": "#888888", "Run8: Instruct SFT ancestry": "#8856a7",
              "Stoic-donor chat12": "#2878b5", "Stoic-donor chatp12": "#db8b22", "Complex-donor chatp12": "#2b8c4b",
              "Complex-donor chatr12": "#248f9a", "Instruct-reply control ±": "#c44c50", "Complex-donor chatr13": "#111111",
              "Stoic-donor chat/general": "#aa99aa", "Other chat recipes": "#666666"}
    path_colors = ["#8856a7", "#2878b5", "#db8b22", "#2b8c4b", "#248f9a", "#c44c50"]
    nrows, ncols = (1, 2) if compact else (2, 3)
    fig = plt.figure(figsize=(13, 7.7) if compact else (15, 11.4), layout="constrained")
    grid = fig.add_gridspec(nrows + 1, ncols, height_ratios=[1] * nrows + [.70 if compact else .58])
    axes = [fig.add_subplot(grid[r, c]) for r in range(nrows) for c in range(ncols)]
    footer = fig.add_subplot(grid[-1, :])
    footer.set_axis_off()
    panels = [("maths_loss_pp", "Maths loss vs Instruct (pp)"),
              ("ordinary_loss_pp", "Ordinary-check loss vs Instruct (pp)"),
              ("lang_switch", "Language switches (% turns)"),
              ("looped", "Loop flags (% turns)"), ("truncated", "Cutoffs (% turns)"),
              ("maths_loss_pp", "Maths: full character range")]
    for i, (ax, (metric, title)) in enumerate(zip(axes, panels)):
        for p in points:
            if p[metric] is not None:
                ax.scatter(p["character"], p[metric], c=colors[p["category"]], s=28,
                           marker="*" if p["category"] == "Complex-donor chatr13" else "o", zorder=3)
        for (name, path), color in zip(paths, path_colors):
            ax.plot([p["character"] for _, p in path], [p[metric] for _, p in path],
                    color=color, ls="--", lw=1, alpha=.8)
        front = frontier(points, metric)
        ax.scatter([p["character"] for p in front], [p[metric] for p in front], s=100,
                   facecolors="none", edgecolors="black", linewidths=.9, zorder=4)
        base = next(p for p in points if p["model"] == BASE)
        ax.scatter(0, base[metric], marker="+", c="black", s=100, zorder=5)
        ax.axhline(0, color=".85", lw=.7); ax.axvline(0, color=".85", lw=.7)
        ax.spines[["top", "right"]].set_visible(False)
        ax.set_title(title + " ↓", loc="left", fontsize=11)
        ax.set_xlabel("Character effect vs same Instruct reference ↑", fontsize=9)
        ax.tick_params(labelsize=9)
        if i < 5:
            ax.set_xlim(-.10, 1.23)
            visible = [p[metric] for p in points if p["character"] >= -.10 and p[metric] is not None]
            if i in (2, 3, 4):
                ax.set_ylim(-.5, max(visible) * 1.15 + .5)
        else:
            ax.set_xlim(-2.15, 1.23)
        if i == 0:
            ax.set_ylim(-10, 62)
        if i == 5:
            ax.set_ylim(-10, 94)
    # Sparse labels only; full recipe/dose identity is retained in the accompanying table.
    ax = axes[0]
    labels = [("r10_stoic0.5_const1_other1_cx_chatp121", "Mixed docs + chat ×1", (0, -8.5)),
              ("r10_stoic0.5_const1_other1_cx_chatr121_cx_chatctl-1", "Reply control −1", (.53, 53))]
    for model, label, position in labels:
        p = next(p for p in points if p["model"] == model)
        ax.annotate(label, (p["character"], p["maths_loss_pp"]), xytext=position,
                    textcoords="data", fontsize=9, zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none", alpha=.95, pad=1),
                    arrowprops=dict(arrowstyle="-", lw=.6))
    # Sparse dose labels and arrows expose reversals without labelling every point.
    for name, color, doses in (("D + chatp12", "#2b8c4b", (1, 1.5, 2)),
                               ("S + chatp12", "#db8b22", (1, 1.5))):
        path = dict(next(ps for n, ps in paths if n == name))
        for start, end in zip(doses, doses[1:]):
            a, b = path[start], path[end]
            xy = lambda t: (a["character"] + t * (b["character"] - a["character"]),
                            a["maths_loss_pp"] + t * (b["maths_loss_pp"] - a["maths_loss_pp"]))
            ax.annotate("", xy(.7), xy(.35), arrowprops=dict(arrowstyle="->", color=color, lw=1.4))
            offset = (-68, 8) if name == "D + chatp12" and end == 1.5 else (8, 5)
            ax.annotate(f"chat ×{end:g}", (b["character"], b["maths_loss_pp"]), xytext=offset,
                        textcoords="offset points", color=color, fontsize=8.5)
    a = next(p for p in points if p["model"] == "r10_stoic2")
    b = next(p for p in points if p["model"] == "r10_stoic2_chatp121")
    c = next(p for p in points if p["model"] == "r10_stoic0.5_const1_other1_cx_chatp121")
    estimate = interpolate(a, b, c["character"], "maths_loss_pp")
    ax.annotate("Stoic recipe, matched-effect estimate", (c["character"], estimate),
                xytext=(.15, 12.5), textcoords="data", fontsize=9, zorder=6,
                bbox=dict(facecolor="white", edgecolor="none", alpha=.95, pad=1),
                arrowprops=dict(arrowstyle="-", lw=.6))
    ax.scatter(c["character"], estimate, marker="s", facecolors="none", edgecolors="black", s=65, zorder=6)
    ax.annotate("", (c["character"], estimate), (c["character"], c["maths_loss_pp"]),
                arrowprops=dict(arrowstyle="<->", lw=.8, color="black"))
    ax.annotate(f"≈{estimate - c['maths_loss_pp']:.1f}pp", (c["character"], (estimate + c["maths_loss_pp"]) / 2),
                xytext=(40, 8), textcoords="offset points", fontsize=9)
    handles = [Line2D([], [], marker="*" if n == "Complex-donor chatr13" else "o", ls="", color=c, label=n) for n, c in colors.items()
               if any(p["category"] == n for p in points)]
    handles += [Line2D([], [], color=".4", ls="--", label="Dose path (unmeasured between points)"),
                Line2D([], [], marker="o", ls="", markerfacecolor="none", color="black", label="Observed Pareto point, per panel"),
                Line2D([], [], marker="s", ls="", markerfacecolor="none", color="black", label="Equal-effect estimate (not observed)")]
    footer.legend(handles=handles, loc="upper center", ncol=3 if compact else 4, fontsize=8.5, frameon=False)
    caption = (
        "Character: pinned Jev preference for the specified Musonius behavioural-change rubric vs the same Instruct, in −2 to +2 score units.\n"
        "0 = no preference; +1 anchors ‘somewhat more’, +2 ‘much more’. Means use both dialogue orders and the pinned broken-reply penalty; not probability or general morality.\n"
        "59 character items ×2 samples; maths 60 questions; ordinary 11×2; full diagnostics flag turns /214. 90% item-bootstrap intervals are in results.md, not plotted.\n"
        "One training per adapter; sampling, training-seed and interpolation uncertainty remain. Lower loss is better; negative loss is an observed gain. + marks Instruct.\n"
        "Mixed docs = ½Stoic + Const + Other; Stoic-only = Stoic ×2. Revised chat = chatp12 data, trained separately on each donor. Arrows show increasing chat dose.\n"
        "Frozen run8/10/11 sources and update: scripts/eval/character_tradeoff.py; slop/eval/character_tradeoff/{results.md,points.json}."
    )
    footer.text(0, .53 if compact else .57, caption, transform=footer.transAxes, ha="left", va="top", fontsize=8.5, linespacing=1.5)
    fig.suptitle("Character and side effects: observed grafts, not equal-dose recipe rankings", fontsize=15)
    fig.canvas.draw()
    tight = fig.get_tightbbox(fig.canvas.get_renderer()); w, h = fig.get_size_inches()
    assert tight.x0 >= 0 and tight.y0 >= 0 and tight.x1 <= w and tight.y1 <= h, "figure clipping"
    fig.savefig(out / ("tradeoff_main.png" if compact else "tradeoff.png"), dpi=160)
    plt.close(fig)


def report(points, provenance, paths, out):
    by = {p["model"]: p for p in points}
    a = by["r10_stoic2"]
    b = by["r10_stoic2_chatp121"]
    c = by["r10_stoic0.5_const1_other1_cx_chatp121"]
    target = c["character"]
    est = {m: interpolate(a, b, target, m) for m in ("maths_loss_pp", "ordinary_loss_pp", "truncated")}
    sensitivity = [interpolate(a, b, target, "maths_loss_pp", power=p) - c["maths_loss_pp"] for p in (.5, 1, 2)]
    old_chat = by["r10_stoic2_chat121"]
    old_at_new = interpolate(a, old_chat, b["character"], "maths_loss_pp")
    old_reduction_pp = b["maths_loss_pp"] - old_at_new
    old_reduction_percent = 100 * old_reduction_pp / b["maths_loss_pp"]
    matched = {"target": target, "observed": c["model"], "comparison_segment": [a["model"], b["model"]],
               "linear_estimate": est, "maths_loss_reduction_pp": est["maths_loss_pp"] - c["maths_loss_pp"],
               "sensitivity_power_half_one_two_pp": sensitivity,
               "same_donor_old_vs_new_chat": {"target": b["character"], "old_interpolated_maths_loss_pp": old_at_new,
                                              "new_observed_maths_loss_pp": b["maths_loss_pp"],
                                              "loss_reduction_pp": old_reduction_pp, "loss_reduction_percent": old_reduction_percent}}
    data = dict(author="PI/OpenAI", points=points, provenance=provenance, matched_example=matched,
                paths=[dict(name=n, doses=[d for d, _ in ps], models=[p["model"] for _, p in ps]) for n, ps in paths],
                frontiers={m: [p["model"] for p in frontier(points, m)] for m in ("maths_loss_pp", "ordinary_loss_pp", *FLAGS)})
    (out / "points.json").write_text(json.dumps(data, indent=2) + "\n")
    curve = next(ps for name, ps in paths if name == "D + chatp12")
    zero, half, one = (next(p for d, p in curve if d == dose) for dose in (0, .5, 1))
    low, span = zero["character"], one["character"] - zero["character"]
    predictions = [low + span * .5, low + span * np.log1p(.5) / np.log(2), low + span * np.sqrt(.5)]
    summary = f'''# Character at matched intensity: historical trade-offs

PI/OpenAI, 2026-10-25. Generated from frozen records; no inference or re-judging.
The interpretation concerns the audited 2026-10-25 comparisons; the observation inventory and plot can grow on later updates.

## Best available comparison

At character effect **{target:+.2f}**, the complex donor plus chatp12 ×1 scores **55/60 maths and 21/22 ordinary**.
The Stoic-only donor plus the same chat-data version at ×1 is close in effect ({b['character']:+.2f}), but scores 49/60 and 20/22.
Interpolating that recipe's measured chat ×0→1 segment to exactly {target:+.2f} predicts {53 - .6 * est['maths_loss_pp']:.2f}/60 maths.
The complex recipe therefore has about **{matched['maths_loss_reduction_pp']:.1f} percentage points less maths loss** at this intensity.
Power sensitivity (exponents ½, 1, 2 on this segment) gives {min(sensitivity):.1f}–{max(sensitivity):.1f}pp. This is a useful approximate recipe comparison,
not an isolated causal effect of adding documents: chat was trained separately on each donor. The paired character intervals overlap.
Ordinary loss improves by {est['ordinary_loss_pp'] - c['ordinary_loss_pp']:.1f}pp; the character-sample cutoff rate is about {est['truncated']:.1f}pp lower.
No loss-reduction percentage is given: complex maths is above the reference's 53/60, and the comparator's estimated loss is only {est['maths_loss_pp']:.1f}pp.
A negative loss means an observed gain, not a reliable general capability improvement.

On the same Stoic ×2 donor, old chat also looks cheaper in maths than the proportion-repaired chatp12:
matching chatp12's {b['character']:+.2f} with the old chat ×0→1 segment predicts {old_at_new:.1f}pp maths loss versus {b['maths_loss_pp']:.1f}pp observed for chatp12.
That is about **{old_reduction_percent:.0f}% less maths loss** ({old_reduction_pp:.1f}pp), calculated as (new loss − matched old loss) / new loss.
This repairs the interpretation of “percent improvement”; it is not percent above a frontier. Both give about 20/22 ordinary checks.
It qualifies the chat-data repair claim: comparable character preference did not buy better narrow capability in this pair.

D means ½Stoic + Const + Other; S means Stoic ×2. All run10/11 chat updates train on Base plus their stated donor documents, then graft to Instruct.
Run8 points have direct-Instruct SFT ancestry and are explicitly a different recipe. The reference is the same frozen Instruct in every included score.

![Maths and ordinary-check trade-offs](tradeoff_main.png)

[Full six-panel diagnostic image](tradeoff.png): its first five panels zoom into near-zero/positive character effects; the last retains collapsed negative-character results.
Every dot is measured; the open square is the local equal-effect estimate, not an observation. Dashed paths connect values of one adapter dose and are only interpolation guides. Black rings mark observed nondominated points per panel,
not a fitted universal frontier or confidence statement. Colours identify chat-training lineage; graft-time document variants share a colour, with exact vectors in the table.
Lower side effects and higher character are preferred. Missing measurements are not zero.
Language, looping and cutoff flags are separate overlapping diagnostics on 214 sampled turns; they do not establish sound reasoning.
Maths is the frozen 60-question/1,500-token protocol; ordinary checks are 11 items ×2. No blended off-target score is used.

## What this changes about chat and control claims

- The complex chatp12 recipe is a better narrow-capability trade-off than the Stoic+chatp12 recipe near +0.83. It is not uniquely best on every axis.
  Chatr12 on the complex donor reaches +0.89 with 55 maths but only 19 ordinary; chatr13 reaches +0.77 with 56 maths/21 ordinary and more sampled loops/cutoffs.
  The new data do not establish a character improvement. This agrees with the frozen paired new-minus-old −0.12 [−0.27,+0.01].
- Full Instruct-reply control subtraction is dominated even by measured, unsubtracted lower-chat-dose grafts: complex chatp12 ×0.5 has +0.67, 56 maths/20 ordinary,
  versus full subtraction's +0.47, 18 maths/8 ordinary. It cannot be defended as merely a fair trade of character intensity for maths.
  Half subtraction reaches +0.94 with 53 maths/20 ordinary, versus unsubtracted chatr12's +0.89 with 55/19.
  The extra character may be noise, but this point is not uniformly worse and was not tested against a no-control curve reaching +0.94.
  The broad claim “subtraction never helps” exceeds the data; the narrower claim “tested full Instruct-reply subtraction damages capability” is well supported.
- Generic-text **document** subtraction is a different control. For mixed Const ×2, plain→anchored language/loop/cutoff counts are 163/16/38→0/0/4,
  maths 52→52, ordinary 21→22; selected anti-extinction, open-access and borrower-first changes survive. For mixed Stoic ×4, counts are 197/45/102→0/1/5,
  maths 33→55 and ordinary 4→20. Const ×4 still fails (0 maths, loops and cutoffs persist). Thus subtraction extends a readable dose range in some recipes.
  At lower plain doses corruption also falls; the key additional evidence is retained changed conduct at anchored Const ×2, with the documented factual/moral defects.
  This supports useful restoration, but does not yet quantify a matched-character-intensity advantage.
- Document ABX distinguishability includes damage and judge-position effects. Plain mixed Const ×1→2 goes 57→91%, while anchored ×1→2 goes 56→81%.
  Matching 81% by interpolating the plain curve would mix desired behaviour with corruption; its apparent intensity is not a valid character target.
  Anchored Stoic ×2 at 41% likewise is not negative character. No document-only ABX point is placed on this character axis or fitted as desirable signal.
  Historical document-only points with actual compatible Jev scores remain included. Generic text alone also changes selected conduct, limiting corpus attribution.
  No mixed-chat/generic-chat-control result existed in the audited 2026-10-25 snapshot. These findings do not settle that comparison.

## Dose shape and interpolation limits

Only within-recipe curves are considered. D+chatp12 doses 0, 0.5, 1, 1.5, 2 give character
+0.24, +0.67, +0.83, +0.69, +0.56: the increasing branch saturates and then reverses.
Holding out dose 0.5, a straight line in dose from 0→1 predicts {predictions[0]:+.2f}; observed is {half['character']:+.2f} (error {half['character'] - predictions[0]:+.2f}).
A simple log(1+dose)/log(2) interpolation predicts {predictions[1]:+.2f} (error {half['character'] - predictions[1]:+.2f}), a square-root interpolation {predictions[2]:+.2f} (error {half['character'] - predictions[2]:+.2f}).
Those are sensitivity checks, not selected fitted laws: only one interior ascending observation exists.
Run8 SFT doses 0, 0.5, 1, 2 similarly rise +0.00→+0.49→+0.72 then fall to −0.67.
S+chat12 declines +0.87→+0.80→−1.68→−1.99 from chat doses 1→1.5→2.5→4.
Two coherent doses cannot identify a power law; saturation/collapse makes a universal dose law misleading.
Local interpolation between adjacent ascending measurements is the default. No extrapolation or fitting across heterogeneous recipes is performed.
The headline comparison is close to a measured endpoint, so curved sensitivity changes it little. It does not require measuring every requested target.

Uncertainty: 59 character items ×2 samples, one training per adapter, selected/tuned sweeps, small capability sets and known frozen gold errors.
Item-bootstrap 90% character intervals are in the table; they omit training-seed and interpolation uncertainty.
The pinned character rubric predates the latest constitution cleanup. Equal scores mean equal measured preference, not equal sound moral reasoning.
Graft-time document ablations beneath a fixed chat adapter move it off its training donor; they are descriptive recipe tests, not training-time causal ablations.

## All compatible observations

Rows rank by character, not a composite winner. Cells show measured scores; character brackets are 90% item bootstrap intervals.
The baseline is defined as zero effect (not a re-judged self-comparison). Maths-loss denominator is 60, ordinary-loss denominator 22.
S/C/O = Stoic/constitution/other documents. p = chatp12, cx-p = chatp12 trained on D, cx-r = chatr12 trained on D; each coefficient is a graft-time dose.
Complete model identifiers, recipe, donor, adapter hashes, source hashes, paths, repeats, exclusions and individual flag counts: [points.json](points.json).
Run8 maths records predate retained request payloads: compatibility there rests on the recorded manifest/eval protocol and identical questions/gold, not payload-level verification.
'''
    table = []
    best = {k: max(p[k] for p in points if p[k] is not None) for k in ("maths", "ordinary")}
    for p in sorted(points, key=lambda p: -p["character"]):
        ci = p["character_ci90"]
        key = f"[{short_label(p['cell'])}](../../../{p['recipe_source']})"
        if p['model'] == BASE:
            key = f"*{key}*"
        def number(k):
            v = p[k]
            return "not run" if v is None else (f"**{v:g}**" if v == best[k] else f"{v:g}")
        table.append([key, f"{p['character']:+.2f} [{ci[0]:+.2f},{ci[1]:+.2f}]", number("maths"), number("ordinary"),
                      "/".join(f"{p['flags'][f]:g}" for f in FLAGS[:3]), p["category"]])
    # Publication table: key, main scores, then auxiliary metadata; no invented combined rank.
    summary += "\n" + tabulate(table, headers=["Graft", "Character↑", "Maths↑ /60", "Ordinary↑ /22", "Language/loops/cutoffs↓", "Notes"],
                               tablefmt="pipe", disable_numparse=True, colalign=("left", "right", "right", "right", "right", "left"))
    summary += "\n\n### Identifiable one-adapter-dose paths\n\n"
    summary += tabulate([[n, ", ".join(f"{d:g}: {p['character']:+.2f}" for d, p in ps)] for n, ps in paths],
                        headers=["Recipe", "Dose: character effect"], tablefmt="pipe", disable_numparse=True)
    summary += f"\n\nIncluded {len(points)} unique observations. Repeated judging/reference records retained once; repeats are not extra evidence.\n\n## Exclusions and update\n\n"
    summary += "\n".join(f"- `{e['source']}`: {e['reason']}." for e in provenance["exclusions"])
    summary += '''\n\nUpdate from the project root (CPU only):

```sh
uv run scripts/eval/character_tradeoff.py
# If historical ignored artifacts are absent in a worktree:
uv run scripts/eval/character_tradeoff.py --data-root /workspace/2026/constitutional_grafting
```

New run10/run11 judging directories are discovered from compatible `meta.json` and completed inference receipts;
missing raw scores are reported, incompatible protocols are excluded. Frozen metrics are never rewritten.
For a new protocol/reference, make a separate comparison rather than weakening the compatibility gate.
Outputs are always written in this checkout's `slop/eval/character_tradeoff/`.

Evidence: [run10](../../../docs/results/20261022_run10.md), [run11](../../../docs/results/20261025_document_and_anchored_grafts.md),
[document coherence](../run11/solo_document_table.coherence.json), [new/old chat](../run11/chatr13/comparison_summary.json).
'''
    (out / "results.md").write_text(summary.rstrip() + "\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-root", type=Path, default=ROOT)
    ap.add_argument("--out", type=Path, default=ROOT / "slop/eval/character_tradeoff")
    args = ap.parse_args()
    points, provenance = load_points(args.data_root.resolve())
    paths = dose_paths(points)
    args.out.mkdir(parents=True, exist_ok=True)
    report(points, provenance, paths, args.out)
    plot(points, paths, args.out)
    plot(points, paths, args.out, compact=True)
    print(f"{len(points)} points; {len(provenance['exclusions'])} exclusions; 0 model calls -> {args.out}")


if __name__ == "__main__":
    main()
