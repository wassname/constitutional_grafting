"""Lossless review views and mechanical checks; never edits training data. -- PI/OpenAI (Sol)"""
import collections
import hashlib
import json
from pathlib import Path

from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / 'slop/eval/run14_box_a/lease/box_runs'
OUT = Path(__file__).resolve().parent
PILOT = ROOT / 'slop/reviews/20261026_run14_control_pilot_package'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    return list(map(json.loads, path.open()))


assert not (OUT / 'manifest.json').exists() and not (OUT / 'read_progress.json').exists(), 'Already prepared: resume the durable read progress, do not overwrite it'
raw = rows(SOURCE / 'control_replies.jsonl')
packed = rows(SOURCE / 'ctlgen.jsonl')
manifest = json.loads((SOURCE / 'control_ready.json').read_text())
assert sha(SOURCE / 'ctlgen.jsonl') == manifest['sha256']
assert len({r['item_id'] for r in raw}) == len(raw)
accepted = {r['id']: r for r in packed}
assert len(accepted) == len(packed) == manifest['rows']
events = collections.defaultdict(dict)
for event in rows(SOURCE / 'control_replies.wire.jsonl'):
    assert event['event'] not in events[event['request_id']]
    events[event['request_id']][event['event']] = event
assert len(events) == len(raw)
for filename, pilot_name in [('control_replies.jsonl', 'control_replies.jsonl'), ('ctlgen.jsonl', 'control_pilot.jsonl')]:
    with (SOURCE / filename).open('rb') as stream:
        prefix = b''.join(next(stream) for _ in range(32))
    assert hashlib.sha256(prefix).hexdigest() == sha(PILOT / pilot_name)

tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422', local_files_only=True)
chunks, buffer, first, label_tokens = [], [], 33, 0
for index, row in enumerate(raw, 1):
    turn = row['turns'][0]
    event = events[turn['request_id']]
    request, response = event['request']['body'], event['response']['body']
    assert request == {'model': 'run14_teacher', 'messages': [{'role': 'user', 'content': turn['user']}], 'max_tokens': 2048,
                       'temperature': .7, 'top_p': 1.0, 'seed': 0, 'chat_template_kwargs': {'enable_thinking': False}}
    choice = response['choices'][0]
    assert not choice['message'].get('reasoning') and not choice['message'].get('reasoning_content')
    assert (choice['message']['content'] or '') == turn['assistant']
    assert choice['finish_reason'] == turn['finish_reason'] and not turn['marker_violation']
    assert turn['n_tokens'] == response['usage']['completion_tokens']
    used = row['item_id'] in accepted
    if used:
        assert turn['finish_reason'] == 'stop'
        expected = tok.apply_chat_template(request['messages'], tokenize=False, add_generation_prompt=True, enable_thinking=False)
        assert accepted[row['item_id']]['segments'] == [{'text': expected, 'label': False}, {'text': turn['assistant'].strip() + '<|im_end|>', 'label': True}]
        label_tokens += len(tok(accepted[row['item_id']]['segments'][1]['text'], add_special_tokens=False).input_ids)
    if index <= 32:
        continue
    view = {'index': index, 'item_id': row['item_id'], 'used_for_training': used, 'request': request,
            'assistant': turn['assistant'], 'finish_reason': turn['finish_reason'], 'completion_tokens': turn['n_tokens']}
    line = json.dumps(view, ensure_ascii=True) + '\n'
    assert len(line) < 44000, (index, len(line))
    if sum(map(len, buffer)) + len(line) > 44000:
        path = OUT / f'rows_{first:04d}_{index - 1:04d}.jsonl'
        path.write_text(''.join(buffer))
        chunks.append({'path': path.name, 'first': first, 'last': index - 1, 'sha256': sha(path)})
        buffer, first = [], index
    buffer.append(line)
if buffer:
    path = OUT / f'rows_{first:04d}_{len(raw):04d}.jsonl'
    path.write_text(''.join(buffer))
    chunks.append({'path': path.name, 'first': first, 'last': len(raw), 'sha256': sha(path)})
assert label_tokens == manifest['supervised_tokens']
assert 0 <= manifest['target_supervised_tokens'] - label_tokens <= .0005 * manifest['target_supervised_tokens']
report = {'author': 'PI/OpenAI (Sol)', 'raw_rows': len(raw), 'training_rows': len(packed), 'supervised_tokens': label_tokens,
          'raw_sha256': sha(SOURCE / 'control_replies.jsonl'), 'training_sha256': sha(SOURCE / 'ctlgen.jsonl'),
          'wire_sha256': sha(SOURCE / 'control_replies.wire.jsonl'), 'finish_reasons': dict(collections.Counter(r['turns'][0]['finish_reason'] for r in raw)),
          'pilot_prefix_verified_rows': 32, 'checks': 'Every request/response pair, visible answer, actual HF unlabelled prompt and labelled reply+EOS checked. No hidden reasoning or marker leaks. JSON escaping only; no text summaries.', 'chunks': chunks}
(OUT / 'manifest.json').write_text(json.dumps(report, indent=2) + '\n')
(OUT / 'read_progress.json').write_text(json.dumps({'author': 'PI/OpenAI (Sol)', 'raw_sha256': report['raw_sha256'], 'training_sha256': report['training_sha256'],
    'read_ranges': [[1, 32]], 'chunks_read': [], 'refusal_ids': [], 'notes': [], 'status': 'PENDING full read; first32 credited only after exact prefix hash checks'}, indent=2) + '\n')
print(json.dumps({k: v for k, v in report.items() if k != 'chunks'}, indent=2))
print(f'{len(chunks)}lossless review chunks prepared; NOT marked read or approved.')
