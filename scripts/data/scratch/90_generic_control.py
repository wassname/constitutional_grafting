"""Run14 generic prompt pools and faithful Instruct-reply control packing. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import inspect
import json
import random
import re
import shutil
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
REVISION = '0f0813072d2358973511097385626f21fcb6d422'
EXECUTED_SHA = '91e95a6eceff6841190e2485006493b1967e0dc9cc4f954da5e8c7a488a79042'
SCREEN = re.compile(r'\b(moral|morality|ethic\w*|right or wrong|should i|religio\w*|christian\w*|muslim\w*|politic\w*|president|war|weapon\w*|murder\w*|kill\w*|suicid\w*|racis\w*|discriminat\w*|sex\w*|abuse\w*|steal\w*|cheat\w*|lie|lying|dishonest\w*|deceiv\w*|virtue\w*|stoic\w*|musonius|identity|persona|roleplay|pretend|act as|you are a|who are you|your name|chatgpt|openai|claude|anthropic|qwen)\b', re.I)


def jl(path):
    with Path(path).open() as stream:
        return list(map(json.loads, stream))


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def write_rows(path, rows):
    Path(path).write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows))


def normalize(text):
    return ' '.join(re.findall(r'\w+', text.lower()))


def heldout_texts():
    rows = [row for name in ['items', 'boundary_items', 'demos', 'panel', 'pov'] for row in jl(ROOT / f'slop/eval/run8/{name}.jsonl')]
    return [normalize(t) for row in rows for t in row['turns']] + [normalize(row['question']) for row in jl(ROOT / 'slop/eval/run8/gsm8k_long60.jsonl')]


def overlaps(prompt, heldout):
    text = normalize(prompt)
    for other in heldout:
        if text in other or other in text:
            return True
        words = text.split()
        if any(' '.join(words[i:i + 12]) in other for i in range(len(words) - 11)):
            return True
    return False


def restore_executed(out):
    from constitutional_grafting.data.historical import assemble_run10
    destination = ROOT / '.local/run14_executed_chatr12'
    destination.mkdir(exist_ok=True)
    if not (destination / 'chatr12.jsonl').exists():
        shutil.copyfile(ROOT / 'data/train/run10/general.jsonl', destination / 'general.jsonl')
        source = inspect.getsource(assemble_run10)
        old = 'sets[name] = [r for r in sets[name] if r["id"] not in pw["chat_drop"]]'
        assert source.count(old) == 1
        source = source.replace(old, 'sets[name] = sets[name]')
        namespace = assemble_run10.__globals__.copy()
        exec(compile(source, 'historical_before_rule_removal', 'exec'), namespace)
        namespace['assemble_run10'](ROOT, destination, ROOT / 'data/train/sft_v3.jsonl')
    target = destination / 'chatr12.jsonl'
    assert sha(target) == EXECUTED_SHA
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B-Base', revision=REVISION, local_files_only=True)
    target_tokens = sum(len(tok(s['text'], add_special_tokens=False).input_ids) for row in jl(target) for s in row['segments'] if s['label'])
    assert target_tokens == 788606
    metadata = {'author': 'PI/OpenAI (Sol)', 'rows': len(jl(target)), 'supervised_tokens': target_tokens,
                'path': str(target.relative_to(ROOT)), 'sha256': EXECUTED_SHA, 'tokenizer_revision': REVISION,
                'counting': 'RawInputOutputStrategy: persegment add_special_tokens=False; label=True only',
                'reconstruction': 'Current historical.assemble_run10 with only later chat_drop filtering disabled; exact executed stage7SHA required.'}
    (out / 'target_tokens.json').write_text(json.dumps(metadata, indent=2) + '\n')
    return tok, metadata


def ordinary():
    templates = [
        'Write a Python function that returns the moving average of a numeric list with window {n}. Show one example.',
        'Explain how DNS caching works to a new software developer in {n} short sentences.',
        'Rewrite this as a concise meeting invitation: We will discuss the inventory report on day {n} of next month at 10am. Please bring your notes.',
        'Create a Markdown table for these three stock counts: pencils {n}, folders {m}, notebooks {z}. Add a total row.',
        'Write JavaScript that sorts an array of objects by a numeric field called count. Show an example with counts {n}, {m}, {z}.',
        'Explain the difference between a list and a set in Python, using examples containing {n}, {m}, and {z}.',
        'Write a friendly two-sentence thank-you note to a colleague who helped move {n} boxes into our new office.',
        'Write a shell command to find regular files larger than {n} megabytes under a directory, without modifying any files.',
    ]
    return [{'id': f'ordinary_{i}_{n}', 'source': 'run14_original_generic_requests', 'prompt': template.format(n=n, m=n + 7, z=n + 13)}
            for i, template in enumerate(templates) for n in range(2, 52)]


def prepare(out):
    from datasets import Dataset
    out.mkdir(parents=True, exist_ok=True)
    tok, target = restore_executed(out)
    heldout = heldout_texts()
    cached = list((Path.home() / '.cache/huggingface/datasets/openai___gsm8k/main').glob('*/*/gsm8k-train.arrow'))
    assert len(cached) == 1
    gsm = [{'id': f'gsm_train_{i}', 'source': 'openai/gsm8k/main/train', 'prompt': r['question']}
           for i, r in enumerate(Dataset.from_file(str(cached[0])))]
    gsm = [r for r in gsm if not overlaps(r['prompt'], heldout)]
    random.Random('run14_gsm').shuffle(gsm)
    robots_path = ROOT / 'data/raw/general/no_robots_all.jsonl'
    robots = []
    for row in jl(robots_path):
        messages = row['messages']
        if len(messages) != 2 or [m['role'] for m in messages] != ['user', 'assistant']:
            continue
        prompt = messages[0]['content']
        if row['category'] not in ['Coding', 'Extract', 'Closed QA', 'Summarize'] or len(prompt.split()) > 180:
            continue
        if SCREEN.search(prompt) or overlaps(prompt, heldout):
            continue
        robots.append({'id': 'no_robots_' + row['prompt_id'], 'source': 'HuggingFaceH4/no_robots/train', 'category': row['category'], 'prompt': prompt})
    random.Random('run14_no_robots').shuffle(robots)
    review_path = out / 'no_robots_prompt_review.json'
    review = json.loads(review_path.read_text())
    assert review['source_sha256'] == sha(robots_path)
    excluded = {r['id'] for r in review['excluded']}
    robots = [r for r in robots if r['id'] not in excluded]
    reviewed = {r['id'] for r in robots[:550]} <= set(review['reviewed_ids'])
    assert len(robots) >= 550, len(robots)
    help_rows = [r for r in ordinary() if not overlaps(r['prompt'], heldout)]
    random.Random('run14_ordinary').shuffle(help_rows)
    control = gsm[:3000] + robots[:400] + help_rows[:300]
    heal = gsm[3000:3750] + robots[400:550] + help_rows[300:400]
    random.Random('run14_control').shuffle(control)
    control += gsm[3750:]
    random.Random('run14_heal').shuffle(heal)
    assert len(heal) == 1000
    texts = [normalize(r['prompt']) for r in control + heal]
    assert len(texts) == len(set(texts))
    for group, rows in [('control', control), ('heal', heal)]:
        write_rows(out / f'{group}_prompts.jsonl', rows)
        write_rows(out / f'{group}_items.jsonl', [{'id': r['id'], 'system': None, 'turns': [r['prompt']], 'max_new_tokens': 2048} for r in rows])
    write_rows(out / 'no_robots_screen_package.jsonl', robots[:550])
    metadata = {'author': 'PI/OpenAI (Sol)', 'target': target, 'tokenizer_class': type(tok).__name__,
                'inputs': {str(cached[0]): sha(cached[0]), str(robots_path.relative_to(ROOT)): sha(robots_path)},
                'pools': {name: {'rows': len(rows), 'sources': dict(Counter(r['source'] for r in rows)),
                                  'sha256': sha(out / f'{name}_prompts.jsonl')} for name, rows in [('control', control), ('heal', heal)]},
                'no_robots_review': {'all_selected_prompts_fully_read': reviewed, 'receipt_sha256': sha(review_path), 'excluded_ids': sorted(excluded)},
                'control_pool_order': 'First3700: shuffled GSM3000+NoRobots400+ordinary300; then remaining eligible GSMtrain reserve. Stop at target+8192 finishedlabeltokens; no new teacher or prompt rewriting.',
                'heldout_exclusion': 'normalized exact/substring and any common12wordspan, against all frozen character,boundary,demo,panel,POV prompts+GSM60; control/heal normalized fullprompt disjoint',
                'screen': 'NoRobots: one-turn, coding/extract/closedQA/summary, <=180words, lexical pre-screen then complete prompt read required; no Rewrite/sentiment reversal, no human answers reused'}
    (out / 'prompt_manifest.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps(metadata, indent=2))


def pack(replies, prompts, target, tokenizer, destination):
    sources = {r['id']: r for r in jl(prompts)}
    accepted, truncated, total, counts = [], [], 0, Counter()
    raw = jl(replies)
    assert len({r['item_id'] for r in raw}) == len(raw)
    for row in raw:
        turn = row['turns'][0]
        assert turn['user'] == sources[row['item_id']]['prompt']
        assert turn['finish_reason'] in ['stop', 'length']
        if turn['finish_reason'] == 'length':
            truncated.append(row['item_id'])
            continue
        assert turn['assistant'].strip() and not turn['marker_violation'], row['item_id']
        prompt = tokenizer.apply_chat_template([{'role': 'user', 'content': turn['user']}], tokenize=False, add_generation_prompt=True, enable_thinking=False)
        text = turn['assistant'].strip() + '<|im_end|>'
        n = len(tokenizer(text, add_special_tokens=False).input_ids)
        if total + n > target:
            continue
        total += n
        counts[sources[row['item_id']]['source']] += 1
        accepted.append({'id': row['item_id'], 'shape': 'general', 'source': sources[row['item_id']]['source'],
                         'segments': [{'text': prompt, 'label': False}, {'text': text, 'label': True}]})
    assert 0 <= target - total <= .0005 * target, (total, target)
    destination.parent.mkdir(parents=True, exist_ok=True)
    write_rows(destination, accepted)
    manifest = {'author': 'PI/OpenAI (Sol)', 'rows': len(accepted), 'supervised_tokens': total, 'target_supervised_tokens': target,
                'relative_token_difference': (total - target) / target, 'sha256': sha(destination), 'sources': dict(counts),
                'raw_replies_sha256': sha(replies), 'prompts_sha256': sha(prompts), 'dropped_truncated': truncated,
                'counting': 'RawInputOutputStrategy persegment add_special_tokens=False; label=True only',
                'selection': 'Input order; finished replies only; whole rows greedily fit under target. No quality/correctness/refusal filtering.',
                'refusal_count': 'Requires complete reply read; lexical candidate count alone is not a refusal count.'}
    destination.with_suffix('.manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare'])
    parser.add_argument('--out', type=Path, default=ROOT / 'slop/eval/run14_box_a')
    args = parser.parse_args()
    prepare(args.out)
