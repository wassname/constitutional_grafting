"""Run 18 coherence results: per model, how long it stays on track on tiny-char's long tasks, tool sessions and standing rules, plus maths.
Scores come from tiny-char's own code checks at the pinned commit (no judge, no model calls). Character comes from the judge step,
added when its output exists. -- PI/Claude (opus-5-5)

On track (1-5) = 1 + 4 x mean over three groups of the mean per-item trajectory score; each draw of each item counts once:
  long tasks      family long (mazes, chains, variable tracking, terminal plans) + MATH L5      score: moves/chain/vars/calls score or correct
  tool sessions   family agent (BFCL multi-turn) + task_agent (fridge log)                      score: turn_score / calls_score
  standing rules  family instructions (rules graded by how far broken, in turn order)           score: rules_kept
usage: python scripts/eval/76_run18_results.py [--out slop/eval/run18_coherence]
"""
import argparse
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TC = ROOT / '.local/tinychar_8c01eca'   # git archive of tiny-character 8c01eca (src, scripts, data)
sys.path.insert(0, str(TC / 'src'))
from tiny_character.checks import item_check  # noqa: E402

RUNS = [ROOT / 'slop/eval/run18/lease/box_runs', ROOT / 'slop/eval/run18b/lease/box_runs']
MODELS = [('r18_charcap_30', 'Recipe, coherence directions erased (strong, 30%)'),
          ('r18_charcap_15', 'Recipe, coherence directions erased (light, 15%)'),
          ('r18_newD_0.5', '*Recipe at half strength*'),
          ('r18_newD_1', '*Recipe (full strength, current)*'),
          ('r18_instruct', '*Instruct (no graft)*')]
SCORE = {'maze': 'moves_score', 'chain': 'chain_score', 'vars': 'vars_score', 'agent_turn': 'turn_score', 'rules': 'rules_kept'}


def group(item):
    if item['family'] == 'long' or item['id'].startswith('math_l5'):
        return 'long'
    if item['family'] == 'agent' or item['id'] == 'task_agent':
        return 'tools'
    if item['family'] == 'instructions':
        return 'rules'


def score(check, result):
    kind = check['kind']
    if kind in SCORE:
        return result[SCORE[kind]]
    for key in ('calls_score', 'rules_kept'):
        if key in result:
            return result[key]
    return result['correct']


def find(name):
    hits = [run / name for run in RUNS if (run / name).exists()]
    assert len(hits) <= 1, hits
    return hits[0] if hits else None


def boot(values, n=2000):
    rng = random.Random(0)
    means = sorted(sum(rng.choice(values) for _ in values) / len(values) for _ in range(n))
    return means[int(.05 * n)], means[int(.95 * n) - 1]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--out', type=Path, default=ROOT / 'slop/eval/run18_coherence')
    a = ap.parse_args()
    items = {i['id']: i for i in map(json.loads, (ROOT / 'slop/eval/run18/inputs/items.jsonl').open())}
    per_item, rows_out = {}, []
    for tag, _ in MODELS:
        # coherence_<tag>.jsonl (the 2 'extra' draws) reused seeds 0 and 1, so 33-51% of its rows are byte-identical to replies_<tag>.jsonl
        # and the rest differ only by batching nondeterminism: not independent draws. Score the 2 independent draws only.
        files = [find(f'replies_{tag}.jsonl')]
        if not files[0]:
            continue
        got = defaultdict(list)  # (group, item) -> scores over draws
        for f in filter(None, files):
            for r in map(json.loads, f.open()):
                it = items[r['item_id']]
                g = group(it)
                if g is None or not it.get('checks'):
                    continue
                res = item_check(it['checks'], [t['assistant'] for t in r['turns']])
                s = score(it['checks'], res)
                got[(g, r['item_id'])].append(s)
                rows_out.append({'model': tag, 'item_id': r['item_id'], 'group': g, 'sample': r['sample'], 'file': f.name, 'score': s,
                                 'finish': [t.get('finish_reason') for t in r['turns']]})
        per_item[tag] = {k: sum(v) / len(v) for k, v in got.items()}
        gsm = find(f'gsm8k_{tag}.jsonl')
        per_item[tag]['_maths'] = sum(json.loads(l)['correct'] for l in gsm.open()) if gsm else None
    a.out.mkdir(parents=True, exist_ok=True)
    (a.out / 'coherence_scores.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows_out))
    table = []
    for tag, label in MODELS:
        if tag not in per_item:
            continue
        p = per_item[tag]
        groups = {g: [v for k, v in p.items() if k != '_maths' and k[0] == g] for g in ('long', 'tools', 'rules')}
        means = {g: sum(v) / len(v) for g, v in groups.items()}
        table.append({'tag': tag, 'label': label, 'on_track': 1 + 4 * sum(means.values()) / 3, **{g: 1 + 4 * m for g, m in means.items()},
                      'maths': p['_maths'], 'n_items': {g: len(v) for g, v in groups.items()}})
    table.sort(key=lambda r: -r['on_track'])
    ref = per_item.get('r18_newD_1')
    paired = {}
    for row in table:
        if ref and row['tag'] != 'r18_newD_1':
            keys = sorted(k for k in per_item[row['tag']] if k != '_maths' and k in ref)
            diffs = [4 * (per_item[row['tag']][k] - ref[k]) for k in keys]
            paired[row['tag']] = (sum(diffs) / len(diffs), *boot(diffs))
    (a.out / 'coherence_table.json').write_text(json.dumps({'table': table, 'paired_vs_newD_1': paired}, indent=1) + '\n')
    for row in table:
        print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in row.items()}))
    print('paired on-track vs recipe x1 (per-item mean diff, 1-5 scale, 90% item bootstrap):', {k: [round(x, 2) for x in v] for k, v in paired.items()})


if __name__ == '__main__':
    main()
