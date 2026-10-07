# /// script
# requires-python = ">=3.11"
# dependencies = ["inspect-ai", "numpy", "tabulate"]
# ///
"""Does a constitution shift moral_choice answers more than noise does?

Per item, choice score = mean over the two option orders of [chose option 1] (0, 0.5 or 1; parse fails drop the order).
shift(cond) = mean over items of |score_cond - score_bare|. The noise floor is shift between two bare runs with
different PROMPT_VERSION (cache bypass; temperature 0, so this is provider nondeterminism). AIRisk risky rate
difference gets a paired bootstrap 90% interval over items (item-sampling noise).
Writes slop/eval/20261008_choice_shift.md and slop/eval/20261008_reading/moral_choice_<model>.md (full answers
where bare and the constitution disagree, then random agreeing items).
"""
import collections
import glob
import random
from pathlib import Path

import numpy as np
from inspect_ai.log import read_eval_log
from tabulate import tabulate

ROOT = Path(__file__).resolve().parents[2]
LOGS = ROOT / "slop/eval/inspect_logs/moral_choice"
OUT = ROOT / "slop/eval/20261008_choice_shift.md"
READ = ROOT / "slop/eval/20261008_reading"
READ_CONSTITUTION = "constitution/v1.3.md"


def load():
    runs = {}  # (model, constitution, prompt_version) -> log
    for f in sorted(glob.glob(str(LOGS / "*.eval"))):
        log = read_eval_log(f)
        if log.status != "success" or log.eval.config.limit:
            continue
        model = log.eval.model.split("/", 1)[1]
        key = (model, log.eval.task_args.get("constitution") or "bare", log.eval.metadata["prompt_version"])
        runs[key] = log
    return runs


def item_scores(log):
    per = collections.defaultdict(list)
    risky = {}
    text = collections.defaultdict(dict)
    for s in log.samples:
        md = s.metadata
        k = (md["eval"], md["i"])
        c = list(s.scores.values())[0].metadata["choice"]
        if c is not None:
            per[k].append(c == 1)
        risky[k] = md["risky"]
        text[k][md["swapped"]] = (s.input[-1].text, s.output.completion, c)
    return {k: np.mean(v) for k, v in per.items()}, risky, text


def risky_rate(sc, risky, keys):
    return np.mean([sc[k] if risky[k] == 1 else 1 - sc[k] for k in keys])


def main():
    runs = load()
    rows = []
    rng = np.random.default_rng(0)
    for (model, cons, pv), log in sorted(runs.items()):
        base_key = (model, "bare", "2026-10-07a")
        if base_key not in runs or (model, cons, pv) == base_key:
            continue
        b, risky, _ = item_scores(runs[base_key])
        c, _, _ = item_scores(log)
        row = {"model": model, "condition": cons + ("" if pv == "2026-10-07a" else f" (repeat {pv})")}
        for ev in ("airisk", "daily"):
            keys = [k for k in b if k in c and k[0] == ev]
            row[f"{ev} shift vs bare"] = np.mean([abs(c[k] - b[k]) for k in keys])
        keys = [k for k in b if k in c and k[0] == "airisk"]
        d = np.array([risky_rate(c, risky, [k]) - risky_rate(b, risky, [k]) for k in keys])
        boot = [rng.choice(d, len(d)).mean() for _ in range(2000)]
        row["AIRisk risky Δ"] = d.mean()
        row["90% interval"] = f"[{np.percentile(boot, 5):+.3f}, {np.percentile(boot, 95):+.3f}]"
        row["n items"] = len(keys)
        rows.append(row)
    table = tabulate(rows, headers="keys", tablefmt="pipe", floatfmt="+.3f")
    OUT.write_text("# moral_choice: shift against bare, with noise floor\n\nScript: `scripts/eval/13_choice_shift.py`. "
                   "shift = mean |Δ p(option 1)| per item, both orders averaged. A '(repeat ...)' bare row is the noise floor "
                   "(same prompts, cache bypassed). The interval is a paired bootstrap over items.\n\n" + table + "\n")
    print(table)

    for model in sorted({k[0] for k in runs}):
        if (model, READ_CONSTITUTION, "2026-10-07a") not in runs:
            continue
        b, _, tb = item_scores(runs[(model, "bare", "2026-10-07a")])
        c, _, tc = item_scores(runs[(model, READ_CONSTITUTION, "2026-10-07a")])
        keys = sorted(k for k in b if k in c)
        differ = [k for k in keys if abs(c[k] - b[k]) >= 0.5]
        same = random.Random(0).sample([k for k in keys if k not in differ], 10)
        out = [f"# moral_choice answers, {model}: bare vs {READ_CONSTITUTION}\n\n{len(differ)} of {len(keys)} items change "
               f"by >= 0.5; all shown first (order 0 only), then 10 random items that did not change.\n"]
        for k in differ + same:
            q, ab, chb = tb[k][False]
            _, ac, chc = tc[k][False]
            out.append(f"\n## {k[0]} {k[1]} | bare chose {chb}, constitution chose {chc}{'' if k in differ else ' (unchanged)'}\n\n"
                       f"**Q:** {q}\n\n**bare:** {ab}\n\n**{READ_CONSTITUTION}:** {ac}\n")
        p = READ / f"moral_choice_{model.replace('/', '__')}.md"
        p.write_text("".join(out))
        print(model, len(differ), "differ ->", p)


if __name__ == "__main__":
    main()
