"""Freeze reviewed thinking-heal inputs and whole-row token-matched variants. -- PI/OpenAI (Sol)"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random

ROOT = Path(__file__).resolve().parents[2]
REPLAY_SHA = '91e95a6eceff6841190e2485006493b1967e0dc9cc4f954da5e8c7a488a79042'
REVISION = '59d61f3ce65a6d9863b86d2e96597125219dc754'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def rows(path):
    with Path(path).open() as stream:
        return [json.loads(line) for line in stream]


def tokenize_row(tokenizer, row):
    ids, labels = [], []
    for segment in row['segments']:
        tokens = tokenizer.encode(segment['text'], add_special_tokens=False)
        ids.extend(tokens)
        labels.extend(tokens if segment['label'] else [-100] * len(tokens))
    assert any(label != -100 for label in labels), row['id']
    assert ids[-1] == tokenizer.convert_tokens_to_ids('<|im_end|>'), row['id']
    assert labels[-1] == ids[-1], row['id']
    return ids, labels


def take_budget(pool, budget, tokenizer, seed):
    ordered = list(pool)
    random.Random(seed).shuffle(ordered)
    selected, total = [], 0
    for row in ordered:
        count = sum(token != -100 for token in tokenize_row(tokenizer, row)[1])
        if abs(total + count - budget) < abs(total - budget):
            selected.append(row)
            total += count
    assert selected
    return selected, total


def build(traces, replay, release, output, tokenizer):
    assert sha(replay) == REPLAY_SHA, 'not the hash-matched executed chatr12'
    approval = json.loads(Path(release).read_text())
    assert approval['approved_trace_sha256'] == sha(traces)
    trace_rows, replay_rows = rows(traces), rows(replay)
    assert set(approval['approved_ids']) == {r['id'] for r in trace_rows}
    assert len(approval['approved_ids']) == len(trace_rows)
    for row in trace_rows:
        target = ''.join(s['text'] for s in row['segments'] if s['label'])
        assert target.startswith('<think>\n') and '\n</think>\n\n' in target
        assert target.split('</think>')[0].removeprefix('<think>').strip()
    appended_eos = []
    for row in replay_rows:
        assert not any('<think>' in s['text'] or '</think>' in s['text'] for s in row['segments'] if s['label'])
        assert row['segments'][-1]['label']
        if not row['segments'][-1]['text'].endswith('<|im_end|>'):
            assert '<|im_end|>' not in row['segments'][-1]['text'], row['id']
            row['segments'][-1]['text'] += '<|im_end|>'
            appended_eos.append(row['id'])
    for row in trace_rows + replay_rows:
        assert len(tokenize_row(tokenizer, row)[0]) <= 8192, (row['id'], 'would truncate the boundary')
    total_trace = sum(sum(x != -100 for x in tokenize_row(tokenizer, r)[1]) for r in trace_rows)
    trace_mix, trace_mix_tokens = take_budget(trace_rows, total_trace / 2, tokenizer, 'heal15_trace')
    replay_mix, replay_mix_tokens = take_budget(replay_rows, total_trace - trace_mix_tokens, tokenizer, 'heal15_replay')
    variants = {'trace': trace_rows, 'mix': trace_mix + replay_mix}
    output.mkdir(parents=True, exist_ok=False)
    manifest = {'author': 'PI/OpenAI (Sol)', 'traces_sha256': sha(traces), 'release_sha256': sha(release),
                'replay_sha256': sha(replay), 'tokenizer_revision': REVISION,
                'replay_eos_appended_ids': appended_eos,
                'deviation': 'Approved by const_v2: replay previously approved executed chatr12 targets, not new D generations. These are teacher training targets, not D self-generated replies.',
                'comparison': 'Matched total assistant-token budget; mixed receives half neutral trace exposure plus half replay. Whole rows, no truncation or duplication; one epoch each.', 'variants': {}}
    for name, data in variants.items():
        random.Random('heal15_order_' + name).shuffle(data)
        path = output / (name + '.jsonl')
        path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in data))
        counts = [tokenize_row(tokenizer, row) for row in data]
        manifest['variants'][name] = {'rows': len(data), 'sha256': sha(path),
             'supervised_tokens': sum(sum(x != -100 for x in labels) for _, labels in counts),
             'sequence_tokens': sum(len(ids) for ids, _ in counts), 'max_sequence_tokens': max(len(ids) for ids, _ in counts),
             'trace_rows': len(trace_rows) if name == 'trace' else len(trace_mix),
             'replay_rows': 0 if name == 'trace' else len(replay_mix),
             'trace_supervised_tokens': total_trace if name == 'trace' else trace_mix_tokens,
             'replay_supervised_tokens': 0 if name == 'trace' else replay_mix_tokens,
             'ids': [r['id'] for r in data], 'replay_shapes': {} if name == 'trace' else dict(Counter(r['shape'] for r in replay_mix))}
    assert abs(manifest['variants']['mix']['supervised_tokens'] / total_trace - 1) < .01
    (output / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--traces', type=Path, required=True)
    parser.add_argument('--replay', type=Path, required=True)
    parser.add_argument('--release', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B', revision=REVISION, local_files_only=True)
    print(json.dumps(build(args.traces, args.replay, args.release, args.output, tokenizer), indent=2))
