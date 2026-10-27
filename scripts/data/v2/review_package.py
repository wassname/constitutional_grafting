"""Write the review package for one batch: slop/reviews/<date>_v2_<batch>_package/
  README.md       rate table by stage and filter, how samples were chosen
  filters.md      per filter: 3 flagged rows and 3 rows just under the cutoff, as the full state the check saw, with scores and vent
  judge.md        per judge defect kind: 3 rejects with quotes; plus 3 KEEP rows with the judge's observations
  edits.md        3 edited rows: every replacement and the meaning check
  rejections_by_stage.png
Samples are seeded (hash of seed_id), not hand-picked. Usage: python scripts/data/v2/review_package.py --batch medium
-- PI/Claude (opus-5-5), 2026-10-27"""
import argparse
import collections
import datetime
import hashlib
import json
from pathlib import Path

import matplotlib
import yaml

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[3]
STAGES = ["02_seeds", "03_requests", "04_generate", "04_route", "05_regex", "06_jev", "07_judge", "08_retry", "09_edit", "11_export"]


def rows(stage, version, batch, kind="rows"):
    p = ROOT / "data" / stage / version / batch / f"{kind}.jsonl"
    return [json.loads(l) for l in p.open()] if p.exists() else []


def pick(items, n=3):
    return sorted(items, key=lambda r: hashlib.sha256(r["seed_id"].encode()).hexdigest())[:n]


def conv(r):
    return "\n\n".join(f"**[{m['role']}]** {m['content']}" for m in r["messages"])


def block(r, extra=""):
    return (f"#### `{r['seed_id']}` ({r['source']})\n\n{extra}\n\n<details><summary>conversation</summary>\n\n{conv(r)}\n\n</details>\n\n"
            f"<details><summary>reasoning ({len(r['reasoning'].split())} words)</summary>\n\n```text\n{r['reasoning']}\n```\n</details>\n\n"
            f"<details><summary>answer ({len(r['answer'].split())} words)</summary>\n\n{r['answer']}\n\n</details>\n\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", required=True)
    ap.add_argument("--version", default="v2")
    a = ap.parse_args()
    out = ROOT / f"slop/reviews/{datetime.date.today():%Y%m%d}_{a.version}_{a.batch}_package"
    out.mkdir(parents=True, exist_ok=True)
    filters = yaml.safe_load((ROOT / "configs/data/v2/jev_filters.yaml").read_text())

    stages = [st for st in STAGES if (ROOT / "data" / st / a.version / a.batch).exists()]
    # rate table
    table = ["| stage | kept | rejected | rejected by filter |", "|:--|--:|--:|:--|"]
    kept_n = []
    for st in stages:
        k, x = rows(st, a.version, a.batch), rows(st, a.version, a.batch, "rejected")
        kept_n.append(len(k))
        table.append(f"| {st} | {len(k)} | {len(x)} | {', '.join(f'{f} {n}' for f, n in collections.Counter(r['filter'] for r in x).most_common())} |")
    judged = rows("07_judge", a.version, a.batch) + [r for r in rows("07_judge", a.version, a.batch, "rejected") if "judge" in r]
    verdicts = collections.Counter(r["judge"]["verdict"] for r in judged)

    # filters.md: Jev
    jev_rows = rows("06_jev", a.version, a.batch) + rows("06_jev", a.version, a.batch, "rejected")
    f_md = [f"# Jev filters, batch `{a.batch}`\n\nFlagged = at or above the cutoff. Under = the highest-scoring rows below it (the most informative accepts).\n"]
    for q, f in filters.items():
        s = sorted(jev_rows, key=lambda r: -r["jev"][q])
        flagged = [r for r in s if r["jev"][q] >= f["cutoff"]]
        under = [r for r in s if r["jev"][q] < f["cutoff"]][:3]
        f_md.append(f"## {q} (action {f['action']}, cutoff {f['cutoff']}): {len(flagged)} of {len(s)} flagged\n\n> {f['question']['instructions']}\n")
        for label, group in (("flagged", pick(flagged)), ("under the cutoff", under)):
            f_md.append(f"### {label}\n")
            f_md += [block(r, f"P({q}) = **{r['jev'][q]:.2f}**; vent: {', '.join(f'{w} {p:.2f}' for w, p in r['jev_vent'])}") for r in group] or ["(none)\n"]
    (out / "filters.md").write_text("\n".join(f_md))

    # judge.md
    j_md = [f"# Haiku judge, batch `{a.batch}`\n\nVerdicts: {dict(verdicts)}\n"]
    by_kind = collections.defaultdict(list)
    for r in judged:
        if r["judge"]["verdict"] == "REGENERATE":
            for k in {d["kind"] for d in r["judge"]["defects"]}:
                by_kind[k].append(r)
    for k, group in sorted(by_kind.items(), key=lambda t: -len(t[1])):
        j_md.append(f"## {k}: {len(group)} rejected rows\n")
        for r in pick(group):
            ds = "\n".join(f"- {d['kind']} ({d['location']}): \"{d['quote']}\" — {d['why']}" for d in r["judge"]["defects"])
            j_md.append(block(r, f"observations: {r['judge']['observations']}\n\n{ds}"))
    j_md.append("## KEEP\n")
    j_md += [block(r, f"observations: {r['judge']['observations']}") for r in pick([r for r in judged if r["judge"]["verdict"] == "KEEP"])]
    (out / "judge.md").write_text("\n".join(j_md))

    # edits.md
    ed = [r for r in rows("09_edit", a.version, a.batch) if r.get("edits")]
    e_md = [f"# Allowed edit, batch `{a.batch}`: {len(ed)} rows edited\n"]
    for r in pick(ed):
        reps = "\n".join(f"- [{e['field']}] `{e['old']}` → `{e['new']}`" for e in r["edits"])
        e_md.append(f"#### `{r['seed_id']}`\n\nmeaning check: {r['edit_check']}\n\n{reps}\n")
    (out / "edits.md").write_text("\n".join(e_md))

    # plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), gridspec_kw={"width_ratios": [1.2, 1]})
    ax1.barh(stages[::-1], kept_n[::-1], color="#4a7")
    for i, v in enumerate(kept_n[::-1]):
        ax1.text(v, i, f" {v}", va="center", fontsize=11)
    ax1.set_xlabel(f"rows kept after stage (of {kept_n[0]} seeds)")
    ax1.set_title(f"Batch {a.batch}: rows kept per stage", fontsize=12)
    kinds = collections.Counter({k: len(g) for k, g in by_kind.items()})
    ks = sorted(kinds, key=kinds.get)
    ax2.barh(ks, [kinds[k] for k in ks], color="#c55")
    for i, k in enumerate(ks):
        ax2.text(kinds[k], i, f" {kinds[k]}", va="center", fontsize=11)
    ax2.set_xlabel(f"of {verdicts['REGENERATE']} first-sample judge rejects, rows with this defect\n(a row can have several)")
    ax2.set_title("Defects behind judge rejects", fontsize=12)
    for ax in (ax1, ax2):
        ax.spines[["top", "right"]].set_visible(False)
    plt.tight_layout()
    plt.savefig(out / "rejections_by_stage.png", dpi=110)

    (out / "README.md").write_text(
        f"# Review package: {a.version} batch `{a.batch}`\n\nTeacher DeepSeek v4.1 flash low; judge and editor Haiku 5.5; Jev filters "
        f"`configs/data/v2/jev_filters.yaml`. Samples are the first 3 by hash of seed_id, not hand-picked.\n\n"
        + "\n".join(table) + f"\n\nFirst-sample judge verdicts: {dict(verdicts)}\n\nFiles: `filters.md`, `judge.md`, `edits.md`, "
        "`rejections_by_stage.png`.\n\n-- PI/Claude (opus-5-5), generated by `scripts/data/v2/review_package.py`\n")
    print(out)


if __name__ == "__main__":
    main()
