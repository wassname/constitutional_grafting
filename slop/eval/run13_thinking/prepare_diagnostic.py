"""Relabel D's empty-final thought text verbatim for a separate diagnostic, never production scores. -- PI/OpenAI (Sol)"""
import copy
import hashlib
import json
from pathlib import Path
from transformers import AutoTokenizer

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
BOX = OUT / 'lease/box_runs'
PLAN = json.loads((OUT / 'plan.json').read_text())
TOKENIZER = Path.home() / '.cache/huggingface/hub/models--Qwen--Qwen3.5-35B-A3B/snapshots' / PLAN['frozen_manifest']['instruct_revision']
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER, local_files_only=True)


def rows(path):
    return [json.loads(line) for line in path.read_text().splitlines()]


def main():
    base = rows(BOX / ("replies_" + PLAN['models']['A']['model'] + '.jsonl'))
    original = rows(BOX / ("replies_" + PLAN['models']['D']['model'] + '.jsonl'))
    assert len(base) == len(original) == 140
    diag = copy.deepcopy(original)
    tag = PLAN['models']['D']['model'] + '__answer_inside_think_diagnostic'
    changes = []
    for row in diag:
        row['model'] = tag
        row['gen']['analysis_view'] = 'answer written inside the think block; only originally empty finals replaced verbatim'
        for index, turn in enumerate(row['turns']):
            if turn['assistant']:
                assert len(tokenizer.encode(turn['assistant'], add_special_tokens=False)) == turn['n_tokens']
                continue
            assert turn['empty_final'] and turn['finish_reason'] == 'stop' and turn['thinking'] is not None
            turn['assistant'] = turn['thinking']
            turn['n_tokens'] = len(tokenizer.encode(turn['assistant'], add_special_tokens=False))
            turn['marker_violation'] = '<think>' in turn['assistant'] or '</think>' in turn['assistant']
            changes.append({'item_id': row['item_id'], 'sample': row['sample'], 'turn': index,
                'source_request_id': turn['request_id'], 'candidate_text_sha256': hashlib.sha256(turn['assistant'].encode()).hexdigest(),
                'n_tokens': turn['n_tokens']})
    assert len(changes) == 176
    records = base + diag
    final_only = [{k: row[k] for k in ('item_id', 'model', 'base_model', 'sample', 'system', 'gen')} | {
        'turns': [{k: t[k] for k in ('user', 'assistant', 'finish_reason', 'n_tokens', 'marker_violation')} for t in row['turns']]} for row in records]
    (OUT / 'diagnostic_d_inside_think.jsonl').write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in final_only))
    receipt = {'author': 'PI/OpenAI (Sol)', 'approved_by': 'const_v2 2026-10-26T05:17:34Z', 'model': tag,
        'replaced_empty_final_turns': len(changes), 'unchanged_nonempty_final_turns': 38,
        'scope': 'Post-hoc diagnostic, not deployment or generation rescue. Actual later-turn generation saw earlier empty visible finals; this relabelled dialogue is not a counterfactual regenerated conversation.',
        'no_text_edits': True, 'same_sampling_and_finish_reasons': True,
        'tokenizer_json_sha256': hashlib.sha256((TOKENIZER / 'tokenizer.json').read_bytes()).hexdigest(),
        'changes': changes}
    (OUT / 'diagnostic_d_inside_think_receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('DIAGNOSTIC PREPARED:176exact hidden texts,38unchanged finals,140Drows+140Arows; no generation or API calls')


if __name__ == '__main__':
    main()
