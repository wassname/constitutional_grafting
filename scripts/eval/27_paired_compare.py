"""Paired model-vs-model comparison from a tiny-character run (same items, same samples, same base): character = mean over items of
(A's mean on-target - B's mean on-target), 90% bootstrap over items (4,000 resamples, seed 0); capability = the 44 code checks
(item x sample) passed only by A vs only by B, exact two-sided McNemar p. Every ordered pair of the given models is written, so no
pair is chosen after the fact.
usage: python3 scripts/eval/27_paired_compare.py RUN OUT.md MODEL ...   -- PI/Claude (Opus 5.5)"""
import itertools
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path

run, out, *models = sys.argv[1:]
J = [json.loads(l) for l in open(Path.home() / f".local/share/tiny-character-2d69739/results/{run}/judged.jsonl")]
char, cap = defaultdict(lambda: defaultdict(list)), defaultdict(dict)
for x in J:
    if x.get("on_target") is not None:
        char[x["model"]][x["item_id"]].append(x["on_target"])
    c = x.get("check") or {}
    if x.get("family") == "capability" and c:
        cap[x["model"]][(x["item_id"], x["sample"])] = c.get("correct", c.get("format_ok"))


def paired_char(a, b):
    mean = lambda m, i: sum(char[m][i]) / len(char[m][i]) if char[m] else 0.0  # the run's base model scores 0 against itself
    items = sorted((char[a].keys() or char[b].keys()) & (char[b].keys() or char[a].keys()))
    d = [mean(a, i) - mean(b, i) for i in items]
    rng = random.Random(0)
    bs = sorted(sum(rng.choice(d) for _ in d) / len(d) for _ in range(4000))
    return sum(d) / len(d), bs[200], bs[3800], len(items)


def mcnemar(a, b):
    ks = cap[a].keys() & cap[b].keys()
    x, y = sum(cap[a][k] > cap[b][k] for k in ks), sum(cap[a][k] < cap[b][k] for k in ks)
    p = min(1.0, 2 * sum(math.comb(x + y, i) for i in range(min(x, y) + 1)) / 2 ** (x + y)) if x + y else 1.0
    return int(sum(cap[a][k] for k in ks)), int(sum(cap[b][k] for k in ks)), x, y, p, len(ks)


lines = [f"# Paired comparisons, tiny-character run `{run}` ({__file__.split('/')[-1]})", "",
         "| A | B | character A−B [90%] | items | capability A / B (checks) | only A / only B | McNemar p |", "|:--|:--|--:|--:|--:|--:|--:|"]
for a, b in itertools.combinations(models, 2):
    m, lo, hi, n = paired_char(a, b)
    ca, cb, x, y, p, nk = mcnemar(a, b)
    mark = " **" if lo > 0 or hi < 0 else ""
    lines.append(f"| {a} | {b} | {m:+.3f} [{lo:+.3f}, {hi:+.3f}]{mark} | {n} | {ca} / {cb} ({nk}) | {x} / {y} | {p:.2f} |")
lines += ["", "** = 90% interval excludes 0."]
Path(out).write_text("\n".join(lines) + "\n")
print("\n".join(lines))
