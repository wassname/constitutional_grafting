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
offsets = [(-38, 6), (6, -12), (6, 6), (-38, -12)]  # one label position per graft, so labels of nearby points do not overlap
for gi, g in enumerate(sorted({r["graft"] for r in rows})):
    rs = [r for r in rows if r["graft"] == g]
    eb = ax.errorbar([r["maths"] for r in rs], [r["char"] for r in rs], yerr=[r["half"] for r in rs], marker="o", capsize=3, label=g)
    for r in rs:
        ax.annotate(f"{r['k']:g}", (r["maths"], r["char"]), textcoords="offset points", xytext=offsets[gi % 4], fontsize=8,
                    color=eb[0].get_color())
ax.plot([0.86], [0], marker="*", ms=14, color="black", ls="none", label="SFT only (reference)")
ax.axhline(0, color="grey", lw=0.5)
ax.set_xlabel("maths correct (code-checked items)   <- higher dose k      lower dose k ->")
ax.set_ylabel("character vs SFT only (judge, -2..+2; broken replies = -2)")
ax.set_title("Graft dose curves (point labels = dose k); up and right is better")
ax.legend()
fig.text(0.01, 0.005, "bars: 90% bootstrap over 59 items (2-4 samples); lines join measured doses only; maths = 11 code-checked items x samples", fontsize=7)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(out.with_suffix(".png"), dpi=130)
print(out.with_suffix(".md").read_text())
