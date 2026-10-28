"""Coherence set for the coherence-erasure run: long multi-turn tool sessions (APIGen-MT-5k reference trajectories) and multi-turn
instruction following with standing constraints (Multi-IF English prompts, replies by Qwen3.5-35B-A3B Instruct via OpenRouter,
thinking off, since the Multi-IF dataset has no replies). Rendered with Instruct's own chat template, thinking off, as {"id","source","segments"}
rows that 18_project_char_vs_cap.py collect reads. Kept out of every eval (tiny-char records both datasets as off-limits). -- PI/Claude

usage: python scripts/data/95_coherence_set.py apigen  OUT.jsonl --n 600
       python scripts/data/95_coherence_set.py multiif OUT.jsonl --n 300   (paid: ~$0.3, OpenRouter project key)
"""
import argparse
import csv
import json
import os
import random
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / '.local/coherence_data'
REVISION = '59d61f3ce65a6d9863b86d2e96597125219dc754'
csv.field_size_limit(sys.maxsize)


def tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B', revision=REVISION, local_files_only=True)


def render(tok, messages, tools=None):
    return tok.apply_chat_template(messages, tools=tools, tokenize=False, enable_thinking=False)


def apigen(args):
    tok = tokenizer()
    rows = json.loads((DATA / 'apigen-mt_5k.json').read_text())
    random.Random(0).shuffle(rows)
    out = []
    for i, row in enumerate(rows):
        messages = [{'role': 'system', 'content': row['system']}]
        for turn in row['conversations']:
            if turn['from'] == 'human':
                messages.append({'role': 'user', 'content': turn['value']})
            elif turn['from'] == 'gpt':
                messages.append({'role': 'assistant', 'content': turn['value']})
            elif turn['from'] == 'function_call':
                call = json.loads(turn['value'])
                if isinstance(call['arguments'], str):  # some rows store arguments as a JSON string
                    call['arguments'] = json.loads(call['arguments'])
                if messages[-1]['role'] == 'assistant' and messages[-1].get('tool_calls') is not None and not messages[-1]['content']:
                    messages[-1]['tool_calls'].append({'type': 'function', 'function': call})
                else:
                    messages.append({'role': 'assistant', 'content': '', 'tool_calls': [{'type': 'function', 'function': call}]})
            elif turn['from'] == 'observation':
                messages.append({'role': 'tool', 'content': turn['value']})
            else:
                raise ValueError(turn['from'])
        text = render(tok, messages, json.loads(row['tools']))
        if len(tok(text)['input_ids']) > args.max_tokens:
            continue
        out.append({'id': f'apigen_{i}', 'source': 'Salesforce/APIGen-MT-5k', 'turns': len(row['conversations']),
                    'segments': [{'text': text, 'label': True}]})
        if len(out) == args.n:
            break
    return out


def chat(messages, key):
    body = json.dumps({'model': 'qwen/qwen3.5-35b-a3b', 'messages': messages, 'temperature': 0.7, 'max_tokens': 1500,
                       'reasoning': {'enabled': False}}).encode()
    request = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions', body,
                                     {'Authorization': f'Bearer {key}', 'Content-Type': 'application/json'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.loads(response.read())
        except Exception as error:  # network or 429: retry, then fail loudly
            if attempt == 3:
                raise
            print(f'retry {attempt}: {error}', flush=True)
            time.sleep(10 * (attempt + 1))


def multiif(args):
    key = os.environ['OPENROUTER_API_KEY']
    tok = tokenizer()
    rows = [r for r in csv.DictReader((DATA / 'multiIF.csv').open()) if r['language'] == 'English']
    random.Random(0).shuffle(rows)
    cache = Path(args.out).with_suffix('.raw.jsonl')
    done = {json.loads(l)['key'] for l in cache.open()} if cache.exists() else set()
    with cache.open('a') as stream:
        for row in rows[:args.n]:
            if row['key'] in done:
                continue
            messages, served, cost = [], set(), 0.0
            for t in (1, 2, 3):
                prompt = row[f'turn_{t}_prompt']
                if not prompt:
                    break
                messages.append(json.loads(prompt))
                reply = chat(messages, key)
                served.add(reply.get('provider', '?'))
                cost += reply.get('usage', {}).get('cost', 0.0)
                messages.append({'role': 'assistant', 'content': reply['choices'][0]['message']['content']})
            stream.write(json.dumps({'key': row['key'], 'messages': messages, 'served_by': sorted(served), 'cost': cost}) + '\n')
            stream.flush()
    raw = [json.loads(l) for l in cache.open()]
    print(json.dumps({'conversations': len(raw), 'cost_usd': sum(r['cost'] for r in raw),
                      'served_by': sorted({p for r in raw for p in r['served_by']})}), flush=True)
    return [{'id': f"multiif_{r['key']}", 'source': 'facebook/Multi-IF (English) + Qwen3.5-35B-A3B replies', 'turns': len(r['messages']),
             'segments': [{'text': render(tok, r['messages']), 'label': True}]} for r in raw]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('source', choices=['apigen', 'multiif'])
    parser.add_argument('out')
    parser.add_argument('--n', type=int, required=True)
    parser.add_argument('--max-tokens', type=int, default=8192)
    args = parser.parse_args()
    rows = {'apigen': apigen, 'multiif': multiif}[args.source](args)
    Path(args.out).write_text(''.join(json.dumps(r) + '\n' for r in rows))
    print(f'SHOULD: {args.n} rows written, each a full multi-turn conversation in Instruct chat format -- wrote {len(rows)} -- PI/Claude', flush=True)


if __name__ == '__main__':
    main()
