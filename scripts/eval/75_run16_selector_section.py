"""Run-16 projection-selector section: table, paired differences and character-vs-maths plot from const_v2's cached metrics.json
plus local selector diagnostics. No model calls. -- PI/Claude (opus-5-5)

usage: python scripts/eval/75_run16_selector_section.py [RUN16_DIR] [OUT_DIR]
"""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RUN16 = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / '.local/worktrees/run16/slop/eval/run16_v2'
OUT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / 'slop/eval/run16_selector'
P = 'r16_stoic0.5_const1_other1_'
ROWS = [  # (model suffix, graft equation, plain description, adapter dir name for diagnostics)
    ('eos_chatr121', 'θ_I + Δ_docs + 1·Δsft_eos', 'new D ×1 (plain)', 'r10_eos_chatr12'),
    ('eos_chatr120.5', 'θ_I + Δ_docs + ½·Δsft_eos', 'new D ×½ (plain)', None),
    ('p16_641', 'θ_I + Δ_docs + 1·P₆₄(Δsft_eos)', 'P₆₄ two-sided ×1', 'r10_p16_64'),
    ('p16_641.25', 'θ_I + Δ_docs + 1.25·P₆₄(Δsft_eos)', 'P₆₄ two-sided ×1.25', None),
    ('p16_1281', 'θ_I + Δ_docs + 1·P₁₂₈(Δsft_eos)', 'P₁₂₈ two-sided ×1', 'r10_p16_128'),
    ('p16out_641', 'θ_I + Δ_docs + 1·P₆₄ᵒᵘᵗ(Δsft_eos)', 'P₆₄ output side only ×1 (Safe LoRA side)', 'r10_p16out_64'),
    ('charcap1', 'θ_I + Δ_docs + 1·S_cc(Δsft_eos)', 'project-4% (char/cap) ×1', 'r10_charcap'),
]
MINE = ('p16out_641', 'charcap1')
REF = P + 'eos_chatr121'


def diagnostics():
    path = OUT / 'measure.jsonl'
    if not path.exists():
        return {}
    rows = [json.loads(l) for l in path.read_text().splitlines() if l.startswith('{"adapter"')]
    base = next(r for r in rows if r['adapter'].endswith('r10_eos_chatr12'))
    return {Path(r['adapter']).name: {k: r[k] / base[k] for k in ('weight', 'char', 'cap')} for r in rows}


def fmt_ci(x, ci):
    return f'{x:+.2f} [{ci[0]:+.2f}, {ci[1]:+.2f}]'


def main():
    data = json.loads((RUN16 / 'metrics.json').read_text())
    metrics, paired = data['metrics'], data['paired']
    matched = {m['model']: m for m in data['matched']}
    diag = diagnostics()
    lines = ['| Graft | Description | Character [90%] | Maths /60 (finished) | Est. plain new D at same character | Small tasks /22 | Loops / cutoffs in tiny-char turns /496 | Output energy kept: weight / char inputs / cap inputs |',
             '|:--|:--|--:|--:|--:|--:|--:|:--|']
    for suffix, eq, desc, adapter in ROWS:
        p = metrics.get(P + suffix)
        if p is None:
            lines.append(f'| {eq} | {desc} | not run | | | | | |')
            continue
        char = fmt_ci(p['character'], p['character_ci90']) if p['character'] is not None else 'not judged'
        m = matched.get(P + suffix, {})
        est = f"{m['estimated_maths']:.1f} maths, {m['estimated_small_tasks_22']:.1f} tasks" if 'estimated_maths' in m else ('—' if suffix.startswith('eos_') else 'not bracketed')
        d = diag.get(adapter) if adapter else None
        dtxt = f"{d['weight']:.2f} / {d['char']:.2f} / {d['cap']:.2f}" if d else ''
        name = f'**{desc}**' if suffix in MINE else desc
        f = p['flags']
        lines.append(f"| {eq} | {name} | {char} | {p['maths']} ({p['maths_finished']}) | {est} | {p['small_tasks_22']:g} | {f['looped']:g} / {f['truncated']:g} | {dtxt} |")
    pair_lines = ['| Comparison (A minus B) | Character [90%] | Maths /60 [90%] | Maths on questions both finish | Small tasks /22 [90%] |', '|:--|--:|--:|--:|--:|']
    for suffix in ('p16_641', 'p16out_641', 'charcap1'):
        a = P + suffix
        for b in (REF, P + 'eos_chatr120.5', P + 'p16_641'):
            if a == b:
                continue
            key = f'{a} vs {b}' if f'{a} vs {b}' in paired else f'{b} vs {a}'
            if key not in paired:
                continue
            c, sign = paired[key], (1 if key.startswith(a) else -1)
            cell = lambda k: (f"{sign * c[k]['mean']:+.2f} [{min(sign * x for x in c[k]['ci90']):+.2f}, {max(sign * x for x in c[k]['ci90']):+.2f}]" if k in c else 'n/a')
            bf = c['both_finished']
            ac, bc = (bf['a_correct'], bf['b_correct']) if sign == 1 else (bf['b_correct'], bf['a_correct'])
            pair_lines.append(f"| {suffix} − {b.removeprefix(P)} | {cell('character')} | {cell('maths')} | {ac} vs {bc} of {bf['n']} | {cell('ordinary')} |")
    OUT.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 5.5))
    dose = [metrics[P + s] for s in ('eos_chatr120.5', 'eos_chatr121')]
    ax.errorbar([p['character'] for p in dose], [p['maths'] for p in dose], fmt='k-o',
                xerr=[[p['character'] - p['character_ci90'][0] for p in dose], [p['character_ci90'][1] - p['character'] for p in dose]],
                capsize=3, label='plain new D, dose ×½ → ×1 (same documents)')
    for p, text in zip(dose, ('×½', '×1')):
        ax.annotate(text, (p['character'], p['maths']), textcoords='offset points', xytext=(-6, -16), fontsize=10)
    ax.plot([0], [metrics['r16_instruct']['maths']], 'kD', ms=8, label='Instruct (no graft, reference)')
    for suffix, _, desc, _ in ROWS[2:]:
        p = metrics.get(P + suffix)
        if p is None or p['character'] is None:
            continue
        ax.errorbar(p['character'], p['maths'], xerr=[[p['character'] - p['character_ci90'][0]], [p['character_ci90'][1] - p['character']]],
                    fmt='s' if suffix in MINE else 'o', ms=9, capsize=3, label=desc)
    ax.set_ylim(min(p['maths'] for p in metrics.values()) - 4, 60.5)  # full-ish scale: one sample per model, ±2–3 answers is noise
    ax.set_xlabel('Character vs Instruct (tiny-char v2, judge preference, 90% item interval)', fontsize=12)
    ax.set_ylabel('GSM8K long, correct /60', fontsize=12)
    ax.set_title('Which projection keeps maths at the same character?', fontsize=13)
    fig.text(.01, .01, 'One GSM generation per question; maths has no interval (paired differences in table). Character: 90% item bootstrap.', fontsize=8)
    ax.legend(fontsize=9, loc='best')
    fig.tight_layout()
    fig.savefig(OUT / 'selector_tradeoff.png', dpi=130)
    text = ['## Projection selectors (run 16, thinking off, tiny-char v2)', '', 'PI/Claude (opus-5-5). Built by `scripts/eval/75_run16_selector_section.py` from '
            f'`{(RUN16 / "metrics.json").relative_to(ROOT)}` and `slop/eval/run16_selector/measure.jsonl`; no model calls. '
            'Δ_docs = ½·Δtxt_stoic + 1·Δtxt_const + 1·Δtxt_other; Δsft_eos = chat adapter retrained with end-of-turn tokens on θ_B + Δ_docs (sha256 e6ed8d61…). '
            'P_k erases the top-k singular directions of θ_I − θ_B per matrix; S_cc keeps the adapter\'s action on inputs character data uses more than capability data (removed share matched to P₆₄). '
            'Effect kept = adapter output energy on each input set relative to plain new D (local diagnostic, not behaviour).', '',
            '![character vs maths](selector_tradeoff.png)', '', *lines, '',
            'Est. plain new D: linear interpolation between ×½ and ×1 at the variant\'s character; an estimate, not an evaluated checkpoint; uncertainty not propagated. Output energy kept is squared (a plain ×½ dose would keep 0.25).', '',
            *pair_lines, '']
    (OUT / 'section.md').write_text('\n'.join(text))
    print('\n'.join(text))


if __name__ == '__main__':
    main()
