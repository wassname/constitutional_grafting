"""CPU-only run15 final-only projections, paired summaries and verbatim read packets. -- PI/OpenAI (Sol)"""
import argparse
from collections import defaultdict
import copy
import hashlib
import json
from pathlib import Path
import random
import re
import statistics
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'slop/eval/run15_heal'
BOX = OUT / 'lease_retry/box_runs'
MODELS = ['r15_instruct', 'r15_D', 'r15_heal_trace', 'r15_heal_mix']
EQUATIONS = {'r15_instruct': 'θ_I', 'r15_D': 'θ_I + Δ_docs + 1·Δsft_rewr|docs',
             'r15_heal_trace': 'θ_D_fp16 + 1·Δheal_trace|D_bf16', 'r15_heal_mix': 'θ_D_fp16 + 1·Δheal_mix|D_bf16'}
FINAL_FIELDS = ['user', 'assistant', 'finish_reason', 'n_tokens', 'marker_violation']
sys.path.insert(0, str(ROOT / 'scripts/eval'))
from coherence_metrics import check_coherence, load_pinned_checks


def rows(path):
    with Path(path).open() as stream:
        return [json.loads(line) for line in stream]


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def bootstrap(values):
    values = list(values)
    rng = random.Random(0)
    samples = sorted(statistics.mean(rng.choices(values, k=len(values))) for _ in range(2000))
    return {'mean': statistics.mean(values), 'ci90': [samples[100], samples[1899]], 'n_items': len(values)}


def per_item(judged, model):
    grouped = defaultdict(list)
    for row in judged:
        if row['model'] == model and row.get('on_target') is not None:
            grouped[row['item_id']].append(row['on_target'])
    assert len(grouped) == 59 and all(len(v) == 2 for v in grouped.values())
    return {key: statistics.mean(values) for key, values in grouped.items()}


def verify_wire(source, mode, items, *, temperature=.7, samples=(0, 1)):
    actual = rows(source)
    expected = {(key, sample) for key in items for sample in samples}
    assert len(actual) == len(expected) and {(r['item_id'], r['sample']) for r in actual} == expected
    events = rows(str(source) + '.wire.jsonl')
    requests = {r['request_id']: r['body'] for r in events if r['event'] == 'request'}
    responses = {r['request_id']: r['body'] for r in events if r['event'] == 'response'}
    used = []
    for row in actual:
        item = items[row['item_id']]
        assert row['base_model'] == 'r15_instruct' and row['system'] == item['system']
        assert [t['user'] for t in row['turns']] == item['turns']
        messages = [{'role': 'system', 'content': item['system']}] if item['system'] else []
        for turn in row['turns']:
            messages.append({'role': 'user', 'content': turn['user']})
            request = requests[turn['request_id']]
            response = responses[turn['request_id']]
            assert request['model'] == response['model'] == row['model']
            assert request['messages'] == messages
            assert request['temperature'] == temperature and request['seed'] == row['sample'] and request['top_p'] == 1
            assert request['chat_template_kwargs'] == {'enable_thinking': mode == 'on'}
            assert request['max_tokens'] == item['max_new_tokens'] + (4096 if mode == 'on' else 0)
            choice = response['choices'][0]
            assert turn['assistant'] == (choice['message']['content'] or '')
            assert turn['finish_reason'] == choice['finish_reason']
            if mode == 'on':
                assert request['thinking_token_budget'] == 4096 and request['return_token_ids']
                assert turn['thinking'] == choice['message']['reasoning']
                assert turn['total_completion_tokens'] == len(choice['token_ids']) == response['usage']['completion_tokens']
            messages.append({'role': 'assistant', 'content': turn['assistant']})
            used.append(turn['request_id'])
    assert len(used) == len(set(used)) == len(requests) == len(responses)
    return actual


def prepare():
    items = {r['id']: r for r in rows(ROOT / 'slop/eval/run8/items.jsonl')}
    provenance = {'author': 'PI/OpenAI (Sol)', 'projection': 'visible final only; no hidden answer rescue; all failures retained', 'sources': {}}
    for mode in ['on', 'off']:
        projected = []
        for model in MODELS:
            source = BOX / f'replies_{model}_{mode}.jsonl'
            actual = verify_wire(source, mode, items)
            provenance['sources'][source.name] = sha(source)
            for row in actual:
                view = copy.deepcopy(row)
                view['turns'] = [{key: turn[key] for key in FINAL_FIELDS} for turn in row['turns']]
                projected.append(view)
        destination = OUT / ('final_only_' + mode + '.jsonl')
        destination.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in projected))
    (OUT / 'final_only_projection.json').write_text(json.dumps(provenance, indent=2) + '\n')
    print(f'PASS: {len(MODELS)}models x2modes x140rows; complete raw wire/final-only histories verified; final-only projections written')


def read_packet():
    selection = {'sys_payday_loan', 'task_agent', 'task_email'}
    items = {row['id']: row for row in rows(ROOT / 'slop/eval/run8/items.jsonl')}
    selected_items = {key: items[key] for key in selection}
    final_hashes = json.loads((BOX.parent / 'retrieval_verified.json').read_text())['manifest']
    checkpoint_hashes = json.loads((BOX.parent / 'checkpoint_hashes_verified.json').read_text())
    expected_early = sorted(path.parts[0].replace('r10_heal15_', 'r15_heal_') + '_step' + path.parts[1].split('-')[1]
        for name, digest in checkpoint_hashes.items() if (path := Path(name)).name == 'adapter_model.safetensors'
        and digest != final_hashes[path.parts[0]]['adapter_model.safetensors']['sha256'])
    early = {'author': 'PI/OpenAI (Sol)', 'scope': 'Preselected/fixed checkpoints only; no full character scores. All completed source wire histories verified.',
             'checkpoints': {tag: {'status': 'partial' if list(BOX.glob(f'selected_{tag}_*.jsonl')) else 'not_run'} for tag in expected_early}}
    packet = ['# Run15 preselected complete replies\n\n-- PI/OpenAI (Sol)\n\nSelection was frozen before inference: payday loan, fridge tools, spin email plus four fixed T0 demonstrations. Full native thinking and finals are preserved, including blank/looped answers. Early checkpoints have selected reads only; their absence from full scores is explicit.\n']
    panel = ['# Run15 fixed temperature-zero panel\n\n-- PI/OpenAI (Sol)\n\nθ_D = θ_I + Δ_docs + Δsft_rewr|docs. Heal LoRAs train on a frozen bf16-rounded copy of merged D, not Base; evaluation adds them to the original fp16 D. Missing historical document2x/4x, SFT-only, and graft-only cells: not run in this repair trial; see the original project panels. Both modes below include complete prompts and all turns in order.\n']
    def panel_order(path):
        tag, mode = path.stem.removeprefix('panel_').rsplit('_', 1)
        return (MODELS.index(tag) if tag in MODELS else len(MODELS), tag, mode)
    panel_items = {row['id']: row for row in rows(ROOT / 'slop/eval/run8/panel.jsonl')}
    for path in sorted((p for p in BOX.glob('panel_r15_*.jsonl') if not p.name.endswith('.wire.jsonl')), key=panel_order):
        name = path.name.removeprefix('panel_').removesuffix('.jsonl')
        tag = name.rsplit('_', 1)[0]
        actual = rows(path)
        complete = len(actual) == 4 and (tag in MODELS or (BOX / f'{tag}.done').exists())
        if complete:
            verify_wire(path, name.rsplit('_', 1)[1], panel_items, temperature=0, samples=(0,))
        panel.append('## ' + name + '\n')
        panel.append(f'Source: `{path.relative_to(ROOT)}`; rows {len(actual)}/4; generation ' + ('complete.' if complete else 'PARTIAL: checkpoint generation is not complete.') + '\n')
        for row in actual:
            panel.append(f'### {row["item_id"]}\n\nSystem: {row["system"]!r}\n')
            for i, turn in enumerate(row['turns'], 1):
                panel.append(f'User{i}:\n\n{turn["user"]}\n\nAssistant{i}:\n\n{turn["assistant"]}\n\nFinish: `{turn["finish_reason"]}`\n')
    for path in sorted(p for pattern in ['replies_r15_*.jsonl', 'selected_r15_*.jsonl'] for p in BOX.glob(pattern) if not p.name.endswith('.wire.jsonl')):
        tag = path.stem.split('_', 1)[1].rsplit('_', 1)[0]
        actual = rows(path)
        expected = 2 * len(selection) if path.stem.startswith('selected_') else 140
        complete = len(actual) == expected and (tag in MODELS or (BOX / f'{tag}.done').exists())
        if complete:
            mode = path.stem.rsplit('_', 1)[1]
            verify_wire(path, mode, selected_items if path.stem.startswith('selected_') else items)
            if tag in early['checkpoints']:
                fixed = BOX / f'panel_{tag}_{mode}.jsonl'
                fixed_rows = verify_wire(fixed, mode, panel_items, temperature=0, samples=(0,))
                turns = [turn for row in actual + fixed_rows for turn in row['turns']]
                early['checkpoints'][tag] |= {'status': 'complete', mode: {'turns': len(turns),
                    'blank_finals': sum(not turn['assistant'].strip() for turn in turns),
                    'length_cutoffs': sum(turn['finish_reason'] == 'length' for turn in turns),
                    'source_sha256': {source.name: sha(source) for source in [path, fixed]}}}
        packet.append('## ' + path.stem + '\n')
        packet.append(f'Source: `{path.relative_to(ROOT)}`; rows {len(actual)}/{expected}; generation ' + ('complete.' if complete else 'PARTIAL: checkpoint generation is not complete.') + '\n')
        for row in actual:
            if row['item_id'] not in selection:
                continue
            packet.append(f'### {row["item_id"]}, sample{row["sample"]}\n\nSystem: {row["system"]!r}\n')
            for i, turn in enumerate(row['turns'], 1):
                packet.append(f'User{i}:\n\n{turn["user"]}\n\nAssistant{i}:\n\n{turn["assistant"]}\n\nFinish: `{turn["finish_reason"]}`\n')
                if 'thinking' in turn:
                    packet.append(f'Native thinking{i}, complete:\n\n{turn["thinking"] or ""}\n\nRequest: `{turn["request_id"]}`; boundary `{turn["reasoning_end_cause"]}`\n')
    assert all({'on', 'off'} <= value.keys() for value in early['checkpoints'].values() if value['status'] == 'complete')
    coverage = '\nEarly checkpoint coverage: ' + '; '.join(f'{tag}: {value["status"]}' for tag, value in early['checkpoints'].items()) + '.\n'
    packet.insert(1, coverage)
    panel.insert(1, coverage)
    (OUT / 'early_completed_quality.json').write_text(json.dumps(early, indent=2) + '\n')
    (OUT / 'read_selected.md').write_text('\n'.join(packet))
    (OUT / 'fixed_demo_panel.md').write_text('\n'.join(panel))


def analyze():
    plan = json.loads((OUT / 'retry_plan.json').read_text())
    checks = load_pinned_checks(ROOT / '.local/tiny-character', plan['frozen_manifest']['protocol_sha256'])
    items = {r['id']: r for r in rows(ROOT / 'slop/eval/run8/items.jsonl')}
    output = {'author': 'PI/OpenAI (Sol)', 'scope': 'Final-only per-regime advantage vs Instruct reused from first lease with identical recorded serving protocol, not regenerated on replacement hardware. Bootstrap2000 item clusters, seed0, average2samples/item first. One training seed. Off retention difference is relative to same unhealed D.', 'modes': {}}
    for mode in ['on', 'off']:
        judged = rows(OUT / f'judging_{mode}/judged.jsonl')
        parent = per_item(judged, 'r15_D')
        output['modes'][mode] = {}
        for model in MODELS:
            actual = verify_wire(BOX / f'replies_{model}_{mode}.jsonl', mode, items)
            coherence, flags = check_coherence(actual, items, checks)
            j = [r for r in judged if r['model'] == model]
            ordinary = [r for r in j if r['family'] == 'capability']
            assert len(ordinary) == 22
            correct = sum(r['check']['correct'] if 'correct' in r['check'] else r['check']['format_ok'] for r in ordinary)
            value = {'equation': EQUATIONS[model], 'ordinary_correct': correct, 'ordinary_n': 22, 'coherence': flags[model]}
            if model == 'r15_instruct':
                value['character'] = {'mean': 0, 'ci90': [0, 0], 'reference': True}
            else:
                grouped = per_item(judged, model)
                assert grouped.keys() == parent.keys()
                value['character'] = bootstrap(grouped.values())
                value['difference_from_D'] = bootstrap(grouped[key] - parent[key] for key in parent)
            turns = [t for r in actual for t in r['turns']]
            value['blank_finals'] = sum(not t['assistant'].strip() for t in turns)
            value['turns'] = len(turns)
            if mode == 'on':
                value['turn_groups'] = {}
                for family, is_capability in [('character', False), ('ordinary', True)]:
                    subset = [t for row in actual if (items[row['item_id']]['family'] == 'capability') == is_capability for t in row['turns']]
                    value['turn_groups'][family] = {'turns': len(subset),
                        'blank_finals': sum(not t['assistant'].strip() for t in subset),
                        'eos_before_close': sum(t['reasoning_end_cause'] == 'eos_during_reasoning' for t in subset),
                        'thinking_tokens_median': statistics.median(t['thinking_tokens'] for t in subset if t['thinking_tokens'] is not None)}
                value.update(missing_boundary=sum(t['boundary_missing'] for t in turns),
                    parser_anomalies=sum(t['parser_boundary_anomaly'] for t in turns),
                    eos_before_close=sum(t['reasoning_end_cause'] == 'eos_during_reasoning' for t in turns),
                    thinking_tokens_median=statistics.median(t['thinking_tokens'] for t in turns if t['thinking_tokens'] is not None),
                    cap_boundary_reached=sum(t['thinking_budget_boundary_reached'] for t in turns))
            gsm = rows(BOX / f'gsm8k_{model}_{mode}.jsonl')
            assert len(gsm) == 60
            value.update(gsm_correct=sum(r['correct'] for r in gsm), gsm_completed=sum(r['correct_completed'] for r in gsm), gsm_n=60)
            output['modes'][mode][model] = value
            (OUT / f'coherence_{model}_{mode}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in coherence))
    (OUT / 'summary.json').write_text(json.dumps(output, indent=2) + '\n')
    read_packet()
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare-judge', 'analyze', 'read-packet'])
    args = parser.parse_args()
    MODELS = json.loads((BOX / 'comparison_models.json').read_text())['models']
    {'prepare-judge': prepare, 'analyze': analyze, 'read-packet': read_packet}[args.action]()
