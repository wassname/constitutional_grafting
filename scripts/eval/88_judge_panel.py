"""Rejudge a run's full cells with a panel of cheap chat judges from different labs, beside the pinned Jev judge. -- PI/Claude (opus-5-5)

Each judge sees the same replies, items and change text as the on-box Jev judge (its `judge_full_*` folder), through the pinned
03_judge.py `--judge <model>` path (both orders, reasons). Writes <out>/<judge>/<cell>/judged.jsonl and <out>/panel.md:
per cell, each judge's mean on-target with a 90% item bootstrap, and its per-item agreement with Jev.

  uv run python scripts/eval/88_judge_panel.py slop/eval/<name>/lease/box_runs slop/eval/<name>/panel [--cells judge_full_on_X ...]
"""
import argparse
import json
import random
import statistics as st
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/box"))
from tinychar import TC, judge_env, rows  # noqa: E402

PANEL = ["anthropic/claude-haiku-5.5", "deepseek/deepseek-v4.1-flash", "openai/gpt-6-luna"]  # wassname 2026-11-01: Luna, not Terra


def rejudge(cell: Path, judge: str, out: Path) -> Path:
    if (out / "judged.jsonl").exists():
        return out
    out.mkdir(parents=True, exist_ok=True)
    name = json.loads((cell / "judge.log").read_text().split("```json", 1)[1].split("```", 1)[0])["name"]  # the on-box judge's own args
    label = "cg_panel_" + "_".join(out.resolve().relative_to(ROOT).parts[-4:])
    argv = [TC / ".venv/bin/python", TC / "scripts/03_judge.py", "--replies", cell / "replies.jsonl", "--items", cell / "items.jsonl",
            "--change", cell / "change.md", "--name", name, "--run", label, "--judge", judge, "--turn-judge", "jev", "--concurrency", "8", "--subset"]
    with (out / "judge.log").open("w") as log:
        subprocess.run(list(map(str, argv)), cwd=TC, env=judge_env(), stdout=log, stderr=subprocess.STDOUT, check=True)
    for f in ("judged.jsonl", "meta.json"):
        (out / f).write_bytes((TC / "results" / label / f).read_bytes())
    return out


def item_means(judged: Path) -> dict[str, float]:
    by = {}
    for r in rows(judged):
        if r.get("on_target") is not None and r["model"] != r["base_model"]:
            by.setdefault(r["item_id"], []).append(r["on_target"])
    return {i: st.mean(v) for i, v in by.items()}


def interval(values: list[float], draws=2000) -> tuple[float, float]:
    rng = random.Random(0)
    means = sorted(st.mean(rng.choices(values, k=len(values))) for _ in range(draws))
    return means[int(.05 * draws)], means[int(.95 * draws)]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("box_runs", type=Path)
    ap.add_argument("out", type=Path)
    ap.add_argument("--cells", nargs="+", help="judge_full_* folder names; default all full cells except _rerun")
    ap.add_argument("--judges", nargs="+", default=PANEL)
    args = ap.parse_args()
    box_runs = args.box_runs.resolve()
    cells = [box_runs / c for c in args.cells] if args.cells else sorted(p for p in box_runs.glob("judge_full_*") if p.is_dir())
    lines = ["| cell | judge | on-target [90%] | Pearson r with Jev (items) | n items |", "|:--|:--|:--|--:|--:|"]
    for cell in cells:
        jev = item_means(cell / "judged.jsonl")
        lo, hi = interval(list(jev.values()))
        lines.append(f"| {cell.name} | Jev (pinned, on box) | {st.mean(jev.values()):+.3f} [{lo:+.3f}, {hi:+.3f}] | 1 | {len(jev)} |")
        for judge in args.judges:
            got = item_means(rejudge(cell, judge, args.out.resolve() / judge.split("/")[-1] / cell.name) / "judged.jsonl")
            ids = sorted(set(got) & set(jev))
            lo, hi = interval([got[i] for i in ids])
            r = st.correlation([got[i] for i in ids], [jev[i] for i in ids])
            lines.append(f"| {cell.name} | {judge} | {st.mean(got[i] for i in ids):+.3f} [{lo:+.3f}, {hi:+.3f}] | {r:.2f} | {len(ids)} |")
    (args.out / "panel.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
