"""Render run14's frozen summary; no scoring or model calls. PI/OpenAI (Sol)."""
import hashlib
import json
import os
from string import Template

from character_tradeoff import frontier
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from tabulate import tabulate

NEW = "r14_stoic0.5_const1_other1_"
BASE = "r8_a0_b0"
DOCS = "r10_stoic0.5_const1_other1"
D = DOCS + "_cx_chatr121"
HALF = NEW + "rewr0.5"
P16, P64, HIGH = (NEW + s for s in ("a14_proj161", "a14_proj641", "a14_proj641.5"))
CONTROL = NEW + "a14_ctlgen1"
SUB = [NEW + "rewr1_a14_ctlgen-" + s for s in ("0.25", "0.5", "1")]
LABELS = {BASE: "Instruct", DOCS: "Documents only", D: "Plain chat ×1", HALF: "Plain chat ×½",
          P16: "Projection16 ×1", P64: "Projection64 ×1", HIGH: "Projection64 ×1.5",
          CONTROL: "Generic control only", **dict(zip(SUB, ("Subtract ×¼", "Subtract ×½", "Subtract ×1")))}
ORDER = [BASE, DOCS, HALF, D, P16, P64, HIGH, CONTROL, *SUB]
MAIN = [BASE, DOCS, HALF, D, P16, P64]
COLORS = {BASE: "#777777", DOCS: "#777777", HALF: "#386cb0", D: "#386cb0",
          P16: "#bb741c", P64: "#168578", HIGH: "#168578", CONTROL: "#777777",
          **dict.fromkeys(SUB, "#97539a")}
NOTES = {BASE: "Cached baseline", DOCS: "Cached document reference", D: "Cached original chat",
         HALF: "New lower-dose reference", P16: "One loop flag",
         P64: "Four maths cutoffs recovered vs plain ½; role flag is false positive",
         HIGH: "Five loop flags; little extra preference",
         CONTROL: "No Musonius identity; eight GSM cutoffs", SUB[0]: "Six loop flags",
         SUB[1]: "Six loop flags; four parsed maths matches unfinished",
         SUB[2]: "Collapsed; only two correct maths answers finish"}


def interval(record):
    return f"{record['mean']:+.2f} [{record['ci90'][0]:+.2f}, {record['ci90'][1]:+.2f}]"


def table(data, headers):
    return tabulate(data, headers=headers, tablefmt="pipe", disable_numparse=True,
                    colalign=tuple("left" if i == 0 or h == "notes" else "right" for i, h in enumerate(headers)))


def save(fig, out, name):
    fig.canvas.draw()
    bounds = fig.get_tightbbox(fig.canvas.get_renderer())
    w, h = fig.get_size_inches()
    assert bounds.x0 > -1/72 and bounds.y0 > -1/72 and bounds.x1 < w+1/72 and bounds.y1 < h+1/72
    for ext in ("png", "svg"):
        metadata = {"Date": None, "Creator": "PI/OpenAI (Sol)"} if ext == "svg" else None
        fig.savefig(out / f"{name}.{ext}", dpi=160, metadata=metadata)
    plt.close(fig)


def figures(points, out):
    plt.rcParams.update({"font.size": 12, "axes.spines.top": False, "axes.spines.right": False, "svg.hashsalt": "run14"})
    views = {m: dict(p, maths_loss=100*(points[BASE]["maths_completed"]-p["maths_completed"])/60,
                     ordinary_loss=100*(points[BASE]["ordinary"]-p["ordinary"])/22)
             for m, p in points.items()}
    observed = {}
    offsets = {
        "maths_loss": [(8, 9), (-115, -18), (-85, 14), (5, -24), (-120, 24), (-65, -28)],
        "ordinary_loss": [(8, 8), (-115, -18), (-100, 13), (8, 10), (12, 16), (-145, -58)]}
    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), layout="constrained")
    for ax, metric, title in zip(axes, ("maths_loss", "ordinary_loss"), ("Finished maths: 60 questions", "Ordinary checks: 22 replies")):
        front = frontier(list(views.values()), metric)
        observed[metric] = [p["model"] for p in front]
        assert set(observed[metric]) == {p["model"] for p in frontier([views[m] for m in MAIN], metric)}
        for models, color in (([DOCS, HALF, D], COLORS[D]), ([DOCS, P16], COLORS[P16]), ([DOCS, P64], COLORS[P64])):
            ax.plot([views[m]["character"] for m in models], [views[m][metric] for m in models],
                    "--", color=color, linewidth=1.3, alpha=.8)
        for m, offset in zip(MAIN, offsets[metric]):
            p = views[m]
            ax.scatter(p["character"], p[metric], s=50, color=COLORS[m], zorder=4)
            ax.annotate(LABELS[m], (p["character"], p[metric]), xytext=offset,
                        textcoords="offset points", fontsize=11,
                        arrowprops={"arrowstyle": "-", "color": COLORS[m], "lw": .6})
        ax.scatter([p["character"] for p in front], [p[metric] for p in front],
                   s=125, facecolors="none", edgecolors="black", linewidths=1, zorder=5)
        ax.axhline(0, color=".8", linewidth=.7)
        ax.set(xlim=(-.05, 1.14), ylim=(-8, 2) if metric == "maths_loss" else (-2, 23),
               title=title, xlabel="Mean target-character preference↑", ylabel="Loss vs Instruct (percentage points)↓")
    handles = [Line2D([], [], linestyle="--", color=COLORS[m], label=label)
               for m, label in ((D, "Plain chat from docs"), (P16, "Rank16 projection from docs"), (P64, "Rank64 projection from docs"))]
    handles.append(Line2D([], [], linestyle="none", marker="o", markerfacecolor="none", color="black", markersize=9,
                          label="Black rings: observed frontier"))
    fig.legend(handles=handles, loc="outside lower center", ncol=4, fontsize=10)
    save(fig, out, "tradeoff")

    fig, axes = plt.subplots(1, 2, figsize=(16, 6.5), layout="constrained")
    others = [CONTROL, *SUB, HIGH]
    other_offsets = {"maths_loss": [(-100, 22), (-150, 12), (-125, 8), (12, -4), (-10, -20)],
                     "ordinary_loss": [(-50, 18), (10, -17), (-130, 20), (12, -4), (-130, -35)]}
    for ax, metric, title in zip(axes, ("maths_loss", "ordinary_loss"), ("Finished maths: controls and additional doses", "Ordinary checks: controls and additional doses")):
        for models, color in (([D, *SUB], COLORS[SUB[0]]), ([P64, HIGH], COLORS[P64])):
            ax.plot([views[m]["character"] for m in models], [views[m][metric] for m in models], "--", color=color, linewidth=1.2)
        ax.scatter([views[m]["character"] for m in MAIN], [views[m][metric] for m in MAIN], s=25, color=".75")
        for m, offset in zip(others, other_offsets[metric]):
            p = views[m]
            ax.scatter(p["character"], p[metric], marker="x", s=65, color=COLORS[m], zorder=3)
            label = LABELS[m] + (" (collapsed)" if m == SUB[-1] else "")
            ax.annotate(label, (p["character"], p[metric]), xytext=offset, textcoords="offset points", fontsize=11,
                        ha="right" if m == HIGH and metric == "maths_loss" else "left",
                        arrowprops={"arrowstyle": "-", "color": COLORS[m], "lw": .6})
        ax.axhline(0, color=".8", linewidth=.7)
        ax.set(xlim=(-1.75, 1.25), ylim=(-10, 96) if metric == "maths_loss" else (-8, 59),
               title=title, xlabel="Mean target-character preference↑", ylabel="Loss vs Instruct (percentage points)↓")
    save(fig, out, "other_variants")

    fig, axes = plt.subplots(1, 3, figsize=(16, 7), sharey=True, layout="constrained")
    specs = [("Primary loop flags /214 turns", [points[m]["flags"]["looped"] for m in ORDER], 214),
             ("Primary cutoff flags /214 turns", [points[m]["flags"]["truncated"] for m in ORDER], 214),
             ("GSM cutoffs /60 answers", [points[m]["gsm_finish_reasons"].get("length", 0) for m in ORDER], 60)]
    for ax, (title, counts, denominator) in zip(axes, specs):
        ax.barh(range(len(ORDER)), [100*n/denominator for n in counts], color=[COLORS[m] for m in ORDER])
        for y, n in enumerate(counts):
            percent = 100*n/denominator
            inside = percent > 75
            ax.text(percent-1.5 if inside else percent+1, y, str(int(n)), va="center", ha="right" if inside else "left",
                    color="white" if inside else "black", fontsize=11)
        ax.set(xlim=(0, 100), xticks=[0, 25, 50, 75, 100], title=title, xlabel="Percent↓ (labels are counts)")
    axes[0].set_yticks(range(len(ORDER)), [LABELS[m] for m in ORDER])
    axes[0].invert_yaxis()
    save(fig, out, "stopping")
    (out / "figure_scope.json").write_text(json.dumps({"author": "PI/OpenAI (Sol)", "main": MAIN,
        "other_variants": others, "frontiers_over_all_11": observed,
        "maths_measure": "Completed correct frozen-extractor matches, relative to Instruct53/60; table retains raw extracted matches.",
        "scope": "Point estimates, not statistical frontiers. Separating five controls/more-damaged variants does not change either full-matrix observed frontier."}, indent=2)+"\n")


def fixed_panel(result, root, out):
    expected = [json.loads(l) for l in (out / "lease/box_runs/panel.jsonl").open()]
    models = [BASE, DOCS, D, "r10_cx_chatr121", *[m for m in ORDER if m not in (BASE, DOCS, D)]]
    text = ["# Fixed temperature-zero panel\n\nPI/OpenAI (Sol). Full saved prompts and every turn, without crops. Identity prompts are near-training diagnostics; these fixed examples are not a repeatability or generalisation study.\n",
            "Required reference order: Instruct; document graft; document graft 2×: not run for this document mixture; document graft 4×: not run for this mixture; document plus character-chat graft; healed: not run in Box A; chat-only graft (documents removed at graft time, off its training base). Box A variants follow.\n"]
    hashes = {}
    for model in models:
        if model == "r10_cx_chatr121":
            path = root / "slop/eval/run10/stage7/box_runs" / f"panel_{model}.jsonl"
            label = "Chat-only graft (off its training base; cached, not scored in Box A)"
        else:
            path = (root / result["points"][model]["maths_source"]).parent / f"panel_{model}.jsonl"
            label = LABELS[model]
        records = [json.loads(l) for l in path.open()]
        assert len(records) == 4
        hashes[str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        text.append(f"\n## {label}\n\nModel: `{model}`. Source: `{os.path.relpath(path, out)}`.\n")
        for r, item in zip(records, expected, strict=True):
            assert r["item_id"] == item["id"] and r["sample"] == 0 and r["gen"]["temperature"] == 0
            assert r["system"] == item["system"]
            assert [t["user"] for t in r["turns"]] == item["turns"]
            text.append(f"\n### {r['item_id']}\n")
            if r["system"] is not None:
                text.append(f"\nSystem\n\n``````text\n{r['system']}\n``````\n")
            for i, t in enumerate(r["turns"], 1):
                text.append(f"\nUser {i}\n\n``````text\n{t['user']}\n``````\n\nAssistant {i} ({t['finish_reason']}, {t['n_tokens']} tokens)\n\n``````text\n{t['assistant']}\n``````\n")
    (out / "fixed_panel.md").write_text("".join(text))
    (out / "fixed_panel_sources.json").write_text(json.dumps({"author": "PI/OpenAI (Sol)", "models": len(models),
        "scenarios": len(models)*4, "source_sha256": hashes}, indent=2)+"\n")


def render(result, root, out):
    points = result["points"]
    assert result["completed_new_cells"] == 8 and not result["pending"] and set(points) == set(ORDER)
    notes = []
    for p in sorted(points.values(), key=lambda p: -p["character"]):
        model = p["model"]
        name = f"[{LABELS[model]}]({os.path.relpath(root / p['judged_source'], out)})"
        if model in (BASE, DOCS, D, HALF, CONTROL):
            name = f"*{name}*"
        score = f"{p['character']:+.2f}"
        if model != BASE:
            lo, hi = p["character_ci90"]
            score += f" [{lo:+.2f}, {hi:+.2f}]"
        if p["character"] == max(q["character"] for q in points.values()):
            score = f"**{score}**"
        maths = str(p["maths"])
        if p["maths_completed"] != p["maths"]:
            maths += f" ({p['maths_completed']} finish)"
        if p["maths"] == max(q["maths"] for q in points.values()):
            maths = f"**{maths}**"
        ordinary = f"{p['ordinary']:g}"
        if p["ordinary"] == max(q["ordinary"] for q in points.values()):
            ordinary = f"**{ordinary}**"
        notes.append([name, score, maths, ordinary, NOTES[model]])
    score_table = table(notes, ["Variant", "Preference↑ [90% interval]", "Maths↑ /60", "Checks↑ /22", "notes"])
    paired_tables = {}
    for field, name in (("paired_vs_D", "D"), ("paired_vs_Dhalf", "half")):
        values = []
        for m in sorted((m for m in ORDER if m != BASE and field in points[m]), key=lambda m: -points[m]["character"]):
            pair = points[m][field]
            values.append([LABELS[m], *[interval(pair[k]) for k in ("character", "maths", "ordinary")]])
        paired_tables[name] = table(values, ["Variant", "Preference Δ↑", "Maths Δ↑ /60", "Checks Δ↑ /22"])
    matches = []
    for r in sorted(result["matched_reference"], key=lambda r: -points[r["model"]]["character"]):
        if "estimated_D_dose" not in r:
            continue
        p, linear = points[r["model"]], r["sensitivity"][1]
        matches.append([LABELS[r["model"]], f"{p['character']:+.2f}", f"{p['maths']} / {linear['maths']:.1f}",
                        f"{p['ordinary']:g} / {linear['ordinary']:.1f}", f"{r['estimated_D_dose']:.3f}"])
    matched_table = table(matches, ["Variant", "Preference↑", "Maths: measured / est.↑", "Checks: measured / est.↑", "Est. plain dose"])
    figures(points, out)
    fixed_panel(result, root, out)
    cost = sum(c["referenced_window_cost_usd"] for c in result["cost_receipt_audit"])
    assert all(not c["unrelated_keys"] for c in result["cost_receipt_audit"])
    (out / "results.md").write_text(Template((out / "results.md.template").read_text()).substitute(
        score_table=score_table, paired_half=paired_tables["half"], paired_D=paired_tables["D"],
        matched_table=matched_table, judge_cost=f"{cost:.9f}"))
    print(f"SHOULD: all 11 points retained; full-matrix frontiers unchanged by display split; 48 full panel scenarios preserved. {out / 'results.md'}")
