"""Verify saved run13 primary/diagnostic evidence without GPU or model APIs. -- PI/OpenAI (Sol)"""
import hashlib
import json
import math
import re
import statistics
from collections import defaultdict
from pathlib import Path

OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[2]
BOX = OUT / 'lease/box_runs'


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def main():
    plan = json.loads((OUT / 'plan.json').read_text())
    items = {row['id']: row for row in rows(ROOT / 'slop/eval/run8/items.jsonl')}
    expected = {(key, sample) for key in items for sample in (0, 1)}
    projected = {(r['model'], r['item_id'], r['sample']): r for r in rows(OUT / 'final_only_for_judge.jsonl')}
    original_d = None
    frozen_math = rows(ROOT / 'slop/eval/run8/gsm8k_long60.jsonl')
    for label in ('A', 'D', 'H'):
        tag = plan['models'][label]['model']
        source = BOX / f'replies_{tag}.jsonl'
        records = rows(source)
        assert len(records) == len(expected) == 140
        assert {(r['item_id'], r['sample']) for r in records} == expected
        events = rows(source.with_name(source.name + '.wire.jsonl'))
        responses = {r['request_id']: r['body'] for r in events if r['event'] == 'response'}
        for row in records:
            item = items[row['item_id']]
            view = projected[(tag, row['item_id'], row['sample'])]
            assert [t['user'] for t in row['turns']] == item['turns']
            for actual, final_only in zip(row['turns'], view['turns'], strict=True):
                assert set(final_only) == {'user', 'assistant', 'finish_reason', 'n_tokens', 'marker_violation'}
                assert all(final_only[key] == actual[key] for key in final_only)
                reply = responses[actual['request_id']]
                choice = reply['choices'][0]
                assert actual['assistant'] == (choice['message']['content'] or '')
                assert actual['thinking'] == choice['message']['reasoning']
                assert actual['total_completion_tokens'] == len(choice['token_ids']) == reply['usage']['completion_tokens']
                assert actual['requested_max_tokens'] == item['max_new_tokens'] + 4096
        maths = rows(BOX / f'gsm8k_{tag}.jsonl')
        generated_maths = rows(BOX / f'gsm_replies_{tag}.jsonl')
        assert len(maths) == len(generated_maths) == len(frozen_math) == 60
        assert len({r['question'] for r in maths}) == 60
        for scored, generated, frozen in zip(maths, generated_maths, frozen_math, strict=True):
            assert scored['question'] == frozen['question']
            assert scored['reply'] == generated['turns'][0]['assistant']
            assert scored['gold'] == float(frozen['answer'].split('####')[-1].strip().replace(',', ''))
            numbers = re.findall(r'Answer:\s*\$?\s*(-?[\d,]*\.?\d+)', scored['reply'])
            assert scored['pred'] == (float(numbers[-1].replace(',', '')) if numbers else None)
            assert scored['correct'] == (scored['pred'] == scored['gold'])
            assert scored['correct_completed'] == (scored['correct'] and scored['finish'] == 'stop')
            assert generated['sample'] == 0 and generated['gen']['temperature'] == 0
        if label == 'D':
            original_d = {(r['item_id'], r['sample']): r for r in records}
    diagnostic = json.loads((OUT / 'diagnostic_d_inside_think_receipt.json').read_text())
    changed = 0
    for row in rows(OUT / 'diagnostic_d_inside_think.jsonl'):
        if row['model'] != diagnostic['model']:
            continue
        original = original_d[(row['item_id'], row['sample'])]
        for actual, candidate in zip(original['turns'], row['turns'], strict=True):
            assert candidate['assistant'] == (actual['assistant'] if actual['assistant'] else actual['thinking'])
            changed += not bool(actual['assistant'])
    assert changed == diagnostic['replaced_empty_final_turns'] == 176
    summary = json.loads((OUT / 'summary.json').read_text())
    judged = rows(OUT / 'judging_on/judged.jsonl')
    for label in ('D', 'H'):
        tag = plan['models'][label]['model']
        grouped = defaultdict(list)
        for row in judged:
            if row['model'] == tag and row.get('on_target') is not None:
                grouped[row['item_id']].append(row['on_target'])
        assert len(grouped) == 59 and all(len(v) == 2 for v in grouped.values())
        mean = statistics.mean(statistics.mean(v) for v in grouped.values())
        assert math.isclose(mean, summary['models'][label]['character_on']['mean'], abs_tol=1e-12)
    closure = json.loads((OUT / 'provider_closure_verified.json').read_text())
    assert closure['instance_id'] == 57749737 and closure['absent_confirmed']
    assert closure['elapsed_hours'] <= plan['max_hours']
    judge_costs = sum(json.loads(p.read_text())['new_cached_request_cost_usd'] for p in OUT.glob('judging_*/cost.json'))
    assert judge_costs <= plan['judge_reserve_usd']
    bound = closure['estimated_gpu_usd'] + plan['traffic_reserve_usd'] + plan['judge_reserve_usd'] + plan['independent_review_reported_usd']
    assert bound <= plan['total_reserve_usd'] <= 15
    result = {'author': 'PI/OpenAI (Sol)', 'verified': True, 'primary_complete_models': ['A', 'D', 'H'],
        'rows_per_model': 140, 'character_items': 59, 'samples': 2, 'gsm8k_frozen_questions_per_model': 60,
        'exact_diagnostic_replacements': changed,
        'primary_final_only_projection_matches_raw_api': True, 'exact_instance_absent': True,
        'judge_successful_cached_cost_usd': judge_costs,
        'cost_bound_with_full_traffic_and_judge_reserves_usd': bound,
        'scope': 'Structural/provenance/arithmetic verification, not semantic certification or provider invoice reconciliation.'}
    (OUT / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    print(OUT / 'results.md')


if __name__ == '__main__':
    main()
