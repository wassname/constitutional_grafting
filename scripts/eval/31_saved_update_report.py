# /// script
# requires-python = ">=3.12"
# dependencies = ["matplotlib", "numpy", "tabulate", "loguru"]
# ///
"""Render the saved-update comparison from completed pinned scores. -- PI/OpenAI"""
import argparse
import hashlib
import importlib
import json
import subprocess
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/eval/run8"
TC = Path.home() / ".local/share/tiny-character-2d69739"
sys.path.insert(0, str(TC / "scripts"))
PINNED = importlib.import_module("17_plot")


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def coefficients(model):
    a, b = model.removeprefix("r8_a").split("_b")
    return float(a), float(b)


def estimates():
    manifest = json.loads((OUT / "manifest.json").read_text())
    for name, expected in manifest['protocol_sha256'].items():
        assert hashlib.sha256((TC / name).read_bytes()).hexdigest() == expected, name
    plot_reference = subprocess.check_output(['git', 'show', manifest['tiny_character_head'] + ':scripts/17_plot.py'], cwd=TC)
    assert (TC / 'scripts/17_plot.py').read_bytes() == plot_reference, 'plot metric reference differs from pinned commit'
    for name in ['items.jsonl', 'boundary_items.jsonl']:
        assert hashlib.sha256((OUT / name).read_bytes()).hexdigest() == manifest['input_sha256'][name], name
    items = {r["id"]: r for r in rows(OUT / "items.jsonl")}
    boundary = {r["id"] for r in rows(OUT / "boundary_items.jsonl")}
    unique, sources = {}, {}
    expected_meta = json.loads((OUT / "judging/baseline/meta.json").read_text())
    for path in sorted((OUT / "judging").glob("*/judged.jsonl")):
        meta = json.loads((path.parent / "meta.json").read_text())
        for key in ["rubric", "checks_sha256", "turn_rubric_sha256", "change", "judge", "turn_judge", "draw", "refs", "anchors", "anchors_sha256", "examples", "examples_sha256", "samples"]:
            assert meta[key] == expected_meta[key], (path, key)
        assert not meta['refs'] and not meta['examples'] and not meta['anchors'], 'this comparison has no reference examples'
        assert meta['items_sha256'] in {manifest['input_sha256'][name] for name in ['items.jsonl', 'boundary_items.jsonl']}, path
        assert hashlib.sha256(Path(meta['items']).read_bytes()).hexdigest() == meta['items_sha256'], path
        sources[str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
        for r in rows(path):
            key = r["item_id"], r["model"], r["sample"]
            assert key not in unique or unique[key] == r, f"conflicting repeated score: {key}"
            unique[key] = r
    done = {p.stem: json.loads(p.read_text()) for p in (OUT / "box_runs").glob("r8_*.done")}
    assert "r8_a0_b0" in done
    records = list(unique.values())
    scored_models = {r["model"] for r in records}
    assert scored_models <= set(done), "scores without a completed generation cell"
    full_models = {m for m in scored_models if not done[m]["boundary_subset"]}
    full = [r for r in records if r["model"] in full_models]
    shared = [r for r in records if r["item_id"] in boundary]
    for model in scored_models:
        expected_ids = boundary if done[model]["boundary_subset"] else set(items)
        assert {(r["item_id"], r["sample"]) for r in records if r["model"] == model} == {(i, s) for i in expected_ids for s in [0, 1]}, model
    views = {"full": PINNED.plot_data(full, items), "shared": PINNED.plot_data(shared, items)}
    for group in views.values():
        for row in group:
            row["a"], row["b"] = coefficients(row["model"])
            row["capability_loss_pp"] = [-row["task_delta_pp"][i] for i in [0, 2, 1]]
    artifact = {"author": "PI/OpenAI", "views": views, "source_sha256": sources,
        "metric_code_sha256": {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in [Path(__file__), TC / "scripts/17_plot.py", TC / "scripts/04_report.py"]},
        "recipient_revision": manifest["instruct_revision"], "sft_sha256": manifest["sft_sha256"], "docs_sha256": manifest["docs_sha256"],
        "pending_judging": sorted(set(done) - scored_models),
        "primary_models": [f'r8_a{a:g}_b{b:g}' for a, b in manifest['cells']],
        "not_generated": [f'r8_a{a:g}_b{b:g}' for a, b in manifest['cells'] + manifest['boundary_ladder'] if f'r8_a{a:g}_b{b:g}' not in done],
        "scope": "Both-order Jev change scores versus fresh Instruct. Samples averaged within item before 90% item-bootstrap intervals. Full and shared-subset scores are separate comparisons. These intervals do not measure semantic judge error, training-seed variation or repeatability of selected T0 demos."}
    (OUT / "paired_estimates.json").write_text(json.dumps(artifact, indent=2) + "\n")
    return artifact


def render(artifact):
    plt.rcParams.update({"font.size": 10, "svg.fonttype": "none"})
    fig, axes = plt.subplots(1, 2, figsize=(13, 6), constrained_layout=True, sharey=True)
    colors = {"sft": "#346b9a", "docs": "#b86a22", "both": "#70578b"}
    titles = {"full": "Full character comparison: 59 items", "shared": "Strength walks: same 9 character items"}
    marked_path = OUT / "incoherent_points.json"
    marked = set(json.loads(marked_path.read_text())) if marked_path.exists() else set()
    for ax, (view, data) in zip(axes, artifact["views"].items()):
        ax.axhline(0, color="0.8", linewidth=.8)
        ax.axvline(0, color="0.8", linewidth=.8)
        ax.plot(0, 0, "k+", markersize=9)
        for path, select, strength in [("sft", lambda r: r["b"] == 0, lambda r: r["a"]),
                ("docs", lambda r: r["a"] == 0, lambda r: r["b"]),
                ("both", lambda r: r["a"] == r["b"], lambda r: r["a"])]:
            selected = sorted([r for r in data if select(r)], key=strength)
            if selected:
                ax.plot([0] + [r["capability_loss_pp"][0] for r in selected],
                    [0] + [r["character"][0] for r in selected], color=colors[path], linewidth=1, alpha=.65,
                    label={"sft": "Increase SFT only", "docs": "Increase documents only", "both": "Increase both together"}[path])
        for i, r in enumerate(sorted(data, key=lambda r: (r["capability_loss_pp"][0], r["character"][0]))):
            x, xl, xh = r["capability_loss_pp"]; y, yl, yh = r["character"]
            color = colors["docs" if r["a"] == 0 else "sft" if r["b"] == 0 else "both"]
            ax.errorbar(x, y, xerr=[[max(0, x-xl)], [max(0, xh-x)]], yerr=[[max(0, y-yl)], [max(0, yh-y)]],
                fmt="x" if r["model"] in marked else "o", color=color, markersize=6, elinewidth=.7, alpha=.85)
            ax.annotate(f"({r['a']:g}, {r['b']:g})", (x, y), xytext=(7, [9, -17, 23, -31][i % 4]),
                textcoords="offset points", fontsize=8, arrowprops={"arrowstyle": "-", "lw": .5, "color": color},
                bbox={"facecolor": "white", "edgecolor": "none", "alpha": .85, "pad": .7})
        ax.set_title(titles[view])
        ax.set_xlabel("Capability loss vs Instruct (percentage points) →")
        ax.set_ylim(-2.15, 2.15)
        ax.margins(x=.15)
        for side in ["top", "right"]:
            ax.spines[side].set_visible(False)
    axes[0].set_ylabel("Character change vs Instruct (−2 to +2) ↑")
    axes[1].legend(loc="lower left", fontsize=8)
    fig.suptitle("Qwen3.5-35B-A3B: saved character SFT and spectral document graft (λ=50)")
    fig.supxlabel("Labels: (SFT strength, document strength). Higher and further left is better. Cross at (0,0): untouched Instruct.\n"
        "Capability: 11 fixed checks, including format; two generations per item. Bars: 90% item-bootstrap intervals.\n"
        "Connecting lines show increasing strengths, not interpolation evidence. An × marks manually confirmed incoherence.", fontsize=9)
    fig.canvas.draw()
    bounds = fig.get_tightbbox(fig.canvas.get_renderer()); width, height = fig.get_size_inches()
    assert bounds.x0 >= 0 and bounds.y0 >= 0 and bounds.x1 <= width and bounds.y1 <= height, "plot label clipped"
    for ext in ["png", "svg"]:
        fig.savefig(OUT / f"character_capability.{ext}", dpi=160)
    plt.close(fig)


def tables(artifact):
    md = ["# Saved-update estimates\n\nPI/OpenAI. ", artifact["scope"], "\n\n"]
    for name, group in artifact["views"].items():
        table = [["*Instruct (0,0)*", "*reference*", "*0.0*", "*reference*"]]
        for r in sorted(group, key=lambda r: -r["character"][0]):
            y, lo, hi = r["character"]; x, xl, xh = r["capability_loss_pp"]
            table.append([f"({r['a']:g}, {r['b']:g})", f"{y:+.1f} [{lo:+.1f}, {hi:+.1f}]",
                f"{x:+.1f} [{xl:+.1f}, {xh:+.1f}]", str(r["character_items"])])
        if name == 'full':
            present = {r['model'] for r in group} | {'r8_a0_b0'}
            for model in artifact['primary_models']:
                if model not in present:
                    a, b = coefficients(model)
                    status = 'judging pending' if model in artifact['pending_judging'] else 'not run'
                    table.append([f'({a:g}, {b:g})', status, status, '—'])
        md += [f"## {'Full snapshot' if name == 'full' else 'Shared boundary subset'}\n\n",
            tabulate(table, headers=["SFT, documents", "Character change↑", "Capability loss↓", "Character items"], tablefmt="pipe", disable_numparse=True), "\n\n"]
    md += ["Completed generation cells awaiting judging: ", ", ".join(artifact["pending_judging"]) or "none", ".\n"]
    (OUT / "estimates.md").write_text("".join(md))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-only", action="store_true")
    args = parser.parse_args()
    artifact = estimates()
    tables(artifact)
    if not args.data_only:
        render(artifact)
    print(OUT / "estimates.md")
