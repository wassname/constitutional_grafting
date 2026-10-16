"""Character vs maths for each graft across doses k, from tiny-character reports (k is an arbitrary unit, so grafts are compared on
this curve, not at equal k). Reads results/<run>/report.md of the pinned tiny-character worktree: on-target (noise table),
check_correct, truncated, jev_coherent (absolute table). Writes OUT.md (table) and OUT.png (plot).
usage: python scripts/eval/25_dose_frontier.py OUT  RUN:MODEL:GRAFT:K ...   -- PI/Claude (Opus 5.5)"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

TC = Path.home() / ".local/share/tiny-character-2d69739/results"


def table(lines: list[str], header_start: str) -> dict:
    i = next(k for k, l in enumerate(lines) if l.startswith(header_start))
    hdr = [c.strip() for c in lines[i].strip("|").split("|")]
    out = {}
    for l in lines[i + 2:]:
        if not l.startswith("|"):
            break
        c = [x.strip().strip("*") for x in l.strip("|").split("|")]
        out[c[0]] = dict(zip(hdr, c))
    return out


def point(run: str, model: str) -> dict:
    lines = (TC / run / "report.md").read_text().splitlines()
    noise = next(table(lines[k:], "| model ") for k, l in enumerate(lines) if l.startswith("| model") and "total±" in l)
    absl = next(table(lines[k:], "| model ") for k, l in enumerate(lines) if l.startswith("| model") and "reversal" in l)
    n, a = noise[model], absl[model]
    return {"char": float(n["on-target"]), "half": float(n["total±"].lstrip("±")), "maths": float(a["check_correct"]),
            "cut": float(a["truncated"]), "coh": float(a["jev_coherent"])}


out = Path(sys.argv[1])
rows = []
for spec in sys.argv[2:]:
    run, model, graft, k = spec.split(":")
    rows.append({"graft": graft, "k": float(k), "run": run, "model": model, **point(run, model)})
rows.sort(key=lambda r: (r["graft"], r["k"]))
md = ["| graft | k | character [90%] | maths | cut off | coherence | source |", "|:--|--:|--:|--:|--:|--:|:--|"]
md += [f"| {r['graft']} | {r['k']:g} | {r['char']:+.2f} ±{r['half']:.2f} | {r['maths']:.0%} | {r['cut']:.0%} | {r['coh']:.2f} | `{r['run']}` {r['model']} |" for r in rows]
out.with_suffix(".md").write_text("\n".join(md) + "\n")
fig, ax = plt.subplots(figsize=(7, 5))
for g in sorted({r["graft"] for r in rows}):
    rs = [r for r in rows if r["graft"] == g]
    ax.errorbar([r["maths"] for r in rs], [r["char"] for r in rs], yerr=[r["half"] for r in rs], marker="o", capsize=3, label=g)
    for r in rs:
        ax.annotate(f"k={r['k']:g}", (r["maths"], r["char"]), textcoords="offset points", xytext=(5, 5), fontsize=8)
ax.axhline(0, color="grey", lw=0.5)
ax.set_xlabel("maths correct (code-checked, tiny-character capability items)")
ax.set_ylabel("character vs SFT only (judge, -2..+2)")
ax.set_title("Graft dose curves: up and right is better; broken replies score -2")
ax.legend()
fig.tight_layout()
fig.savefig(out.with_suffix(".png"), dpi=130)
print(out.with_suffix(".md").read_text())
