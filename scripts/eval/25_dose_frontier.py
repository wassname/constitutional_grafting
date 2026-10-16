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
    a = absl[model]
    n = noise[model] if model in noise else {"on-target": "0", "total±": "±0"}  # the run's base model: compared with itself, 0 by definition
    return {"char": float(n["on-target"]), "half": float(n["total±"].lstrip("±")), "maths": float(a["check_correct"]),
            "cut": float(a["truncated"]), "coh": float(a["jev_coherent"])}


NAMES = {"plain": "plain graft (document LoRA)", "spl": "spectral-penalty graft (λ=0.5 during training)"}
out = Path(sys.argv[1])
rows = []
for spec in sys.argv[2:]:
    run, model, graft, k = spec.split(":")
    rows.append({"graft": graft, "k": float(k), "run": run, "model": model, **point(run, model)})
rows.sort(key=lambda r: (r["graft"], r["k"]))
md = ["| graft | k | character [90%] | capability | cut off | coherence | source |", "|:--|--:|--:|--:|--:|--:|:--|"]
md += [f"| {r['graft']} | {r['k']:g} | {r['char']:+.2f} ±{r['half']:.2f} | {r['maths']:.0%} | {r['cut']:.0%} | {r['coh']:.2f} | `{r['run']}` {r['model']} |" for r in rows]
out.with_suffix(".md").write_text("\n".join(md) + "\n")
fig, ax = plt.subplots(figsize=(8, 5.6))
offsets = [(-38, 6), (6, -12), (6, 6), (-38, -12)]  # one label position per graft, so labels of nearby points do not overlap
for gi, g in enumerate(sorted({r["graft"] for r in rows} - {"ref"})):
    rs = [r for r in rows if r["graft"] == g]
    # x bars: 90% binomial interval over 44 checks (11 items x 4 samples), unpaired, so a conservative scale for gaps between grafts
    xe = [1.645 * (r["maths"] * (1 - r["maths"]) / 44) ** 0.5 for r in rs]
    eb = ax.errorbar([r["maths"] for r in rs], [r["char"] for r in rs], yerr=[r["half"] for r in rs], xerr=xe, marker="o", capsize=3, label=NAMES.get(g, g),
                     elinewidth=0.8)
    for r in rs:
        ax.annotate(f"{r['k']:g}", (r["maths"], r["char"]), textcoords="offset points", xytext=offsets[gi % 4], fontsize=8,
                    color=eb[0].get_color())
for i, r in enumerate([r for r in rows if r["graft"] == "ref"]):  # spec RUN:MODEL:ref:0 = an SFT-only reference point of that run
    ax.plot([r["maths"]], [r["char"]], marker="*", ms=14, color="black", mfc="black" if i == 0 else "none", ls="none", label=f"SFT only ({r['model']})")
ax.axhline(0, color="grey", lw=0.5)
ax.set_xlabel("capability checks passed (GSM8K, JSON, format, length; code-checked)   <- higher k   lower k ->")
ax.set_ylabel("character vs SFT only (judge, -2..+2; broken replies = -2)")
ax.set_title("Graft dose curves (point labels = dose k); up and right is better")
ax.legend()
fig.text(0.01, 0.005, "y bars: 90% bootstrap over 59 items; x bars: 90% binomial over 44 checks; lines join measured doses only;\ncapability = 11 code-checked items x samples (6 GSM8K CoT, 2 GSM8K JSON, ducks JSON, wallet JSON [0 for every model at this pin], long story);\nat 4 samples one flipped check = 2.3 points; fp16-vs-bf16 SFT control: -0.06 character, -2.3 points", fontsize=7)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(out.with_suffix(".png"), dpi=130)
print(out.with_suffix(".md").read_text())
