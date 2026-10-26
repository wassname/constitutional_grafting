"""CPU-only, frozen final-answer checks and item-paired thinking-on/off summaries. -- PI/OpenAI (Sol)"""
import hashlib
import json
import random
import statistics
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BOX = OUT / 'lease/box_runs'
PLAN = json.loads((OUT / 'plan.json').read_text())
sys.path.insert(0, str(ROOT / 'scripts/eval'))
from coherence_metrics import check_coherence, load_pinned_checks


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines()]


def bootstrap(values):
    values = list(values)
    rng = random.Random(0)
    draws = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(2000))
    return {'mean': statistics.mean(values), 'ci90': [draws[100], draws[1899]], 'items': len(values)}


def per_item(records):
    grouped = defaultdict(list)
    for row in records:
        if row.get('on_target') is not None:
            grouped[row['item_id']].append(row['on_target'])
    assert len(grouped) == 59 and all(len(v) == 2 for v in grouped.values())
    return {key: statistics.mean(value) for key, value in grouped.items()}


def ordinary(records):
    selected = [r for r in records if r['family'] == 'capability']
    assert len(selected) == 22
    return sum(r['check']['correct'] if 'correct' in r['check'] else r['check']['format_ok'] for r in selected)


def main():
    checks = load_pinned_checks(ROOT / '.local/tiny-character', PLAN['frozen_manifest']['protocol_sha256'])
    items = {row['id']: row for row in rows(ROOT / 'slop/eval/run8/items.jsonl')}
    judged = rows(OUT / 'judging_on/judged.jsonl')
    point_index = {p['model']: p for p in json.loads((ROOT / 'slop/eval/character_tradeoff/points.json').read_text())['points']}
    summary = {'author': 'PI/OpenAI (Sol)', 'scope': 'Within-regime character effects against that regime\'s Instruct; on-minus-off difference of effects, not absolute character scale. Bootstrap2000 item clusters, seed0, two samples/item averaged first.', 'models': {}}
    selection = json.loads((OUT / 'read_selection.json').read_text())
    packet = ['# Preselected thinking-on/off read packet\n', 'PI/OpenAI (Sol). Parent-specified selection, saved before inference. All selected finals are verbatim. On thoughts show head/middle/tail excerpts for skimming, not a full-read claim; full text/token IDs remain in wire JSONL. No thinking-off raw hidden trace was retained.\n']
    sources = {}
    for label, model in PLAN['models'].items():
        tag = model['model']
        on_file = BOX / f'replies_{tag}.jsonl'
        if not on_file.exists():
            summary['models'][label] = {'model': tag, 'not_run': True}
            continue
        on = rows(on_file)
        off_file = ROOT / model['thinking_off_source']
        assert hashlib.sha256(off_file.read_bytes()).hexdigest() == model['thinking_off_source_sha256']
        off = [r for r in rows(off_file) if r['model'] == tag]
        assert len(on) == len(off) == 140
        j_on = [r for r in judged if r['model'] == tag]
        j_off = [r for r in rows(off_file.with_name('judged.jsonl')) if r['model'] == tag]
        record = {'model': tag, 'ordinary_on': ordinary(j_on), 'ordinary_off': ordinary(j_off), 'ordinary_n': 22}
        for regime, reply_rows in [('on', on), ('off', off)]:
            checked, flags = check_coherence(reply_rows, items, checks)
            record['coherence_' + regime] = flags[tag]
            if regime == 'on':
                (OUT / f'coherence_{label}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in checked))
        if label == 'A':
            record.update(character_on={'mean': 0, 'ci90': [0, 0]}, character_off={'mean': 0, 'ci90': [0, 0]}, character_effect_change={'mean': 0, 'ci90': [0, 0]})
        else:
            new, old = per_item(j_on), per_item(j_off)
            assert new.keys() == old.keys()
            record.update(character_on=bootstrap(new.values()), character_off=bootstrap(old.values()),
                          character_effect_change=bootstrap(new[key] - old[key] for key in old))
        turns = [t for row in on for t in row['turns']]
        record.update(turns=len(turns), empty_final=sum(t['empty_final'] for t in turns),
                      parser_boundary_anomalies=sum(t['parser_boundary_anomaly'] for t in turns),
                      boundary_missing=sum(t['boundary_missing'] for t in turns),
                      thinking_cap_boundary=sum(t['thinking_budget_boundary_reached'] for t in turns),
                      finish_length=sum(t['finish_reason'] == 'length' for t in turns),
                      final_tokens_median=statistics.median(t['n_tokens'] for t in turns),
                      thinking_tokens_median=statistics.median(t['thinking_tokens'] for t in turns if t['thinking_tokens'] is not None),
                      total_generated_tokens=sum(t['total_completion_tokens'] for t in turns),
                      final_above_original_cap=sum(t['n_tokens'] > t['original_answer_cap'] for t in turns))
        if (BOX / f'gsm8k_{tag}.jsonl').exists():
            math_on = rows(BOX / f'gsm8k_{tag}.jsonl')
            old_path = ROOT / point_index[tag]['maths_source']
            math_off = rows(old_path)
            assert len(math_on) == len(math_off) == 60
            gold_off = {r['question']: r for r in math_off}
            assert set(gold_off) == {r['question'] for r in math_on}
            record.update(maths_on=sum(r['correct'] for r in math_on), maths_off=sum(r['correct'] for r in math_off), maths_n=60,
                          maths_completed_on=sum(r['correct_completed'] for r in math_on),
                          maths_no_answer_on=sum(r['pred'] is None for r in math_on),
                          maths_difference=bootstrap(int(r['correct']) - int(gold_off[r['question']]['correct']) for r in math_on),
                          maths_off_source=str(old_path.relative_to(ROOT)))
        else:
            record['maths_not_run'] = True
        summary['models'][label] = record
        for regime, reply_rows in [('off', off), ('on', on)]:
            packet.append(f'## {label}, thinking {regime}\n')
            records = {(r['item_id'], r['sample']): r for r in reply_rows}
            if regime == 'on':
                panels = rows(BOX / f'panel_samples_{tag}.jsonl')
                records.update({(r['item_id'], r['sample']): r for r in panels})
            else:
                stage = ROOT / point_index[tag]['recipe_source']
                panel_path = stage.parent / f'panel_{tag}.jsonl'
                packet.append('Off fixed-panel outputs, where available, are temperature0/sample0 only; a second off stochastic panel sample was not run.\n')
                if panel_path.exists():
                    records.update({(r['item_id'], r['sample']): r for r in rows(panel_path)})
            for item_id in selection['panel_items'] + selection['frozen70_items']:
                for sample in (0, 1):
                    key = (item_id, sample)
                    if key not in records:
                        packet.append(f'### {item_id}, sample{sample}: not run\n')
                        continue
                    row = records[key]
                    packet.append(f'### {item_id}, sample{sample}\n\nSystem: {row["system"]!r}\n')
                    for i, turn in enumerate(row['turns'], 1):
                        packet.append(f'User{i}:\n\n{turn["user"]}\n\nAssistant{i}:\n\n{turn["assistant"]}\n')
                        if regime == 'on':
                            thought = turn['thinking'] or ''
                            chunks = [thought] if len(thought) <= 1600 else [thought[:600], thought[len(thought)//2-200:len(thought)//2+200], thought[-600:]]
                            packet.append(f'Stop: `{turn["finish_reason"]}`; thinking tokens `{turn["thinking_tokens"]}`; final tokens `{turn["n_tokens"]}`; end cause `{turn["reasoning_end_cause"]}`. Full thought: wire request `{turn["request_id"]}`.\n\nThinking skim:\n\n' + '\n\n[skim gap]\n\n'.join(chunks) + '\n')
        sources[label] = {'on': str(on_file.relative_to(ROOT)), 'off': model['thinking_off_source']}
    summary['sources'] = sources
    (OUT / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    (OUT / 'read_packet.md').write_text('\n'.join(packet))
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
