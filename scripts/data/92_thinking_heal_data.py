#!/usr/bin/env python3
"""CPU/API-only thinking-heal preparation; never trains or starts a GPU.

prepare -> preflight -> generate --limit 6 -> package -> review -> generate
-> build. The supervisor runs long API commands. Each request is reserved before
submission and saved/fsynced on arrival. Resume never resends an uncertain call.
All outputs stay under slop/data/20261026_thinking_heal/.
-- PI/Sol (heal prep 2)
"""
import argparse
from collections import Counter
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
import fcntl
from datetime import datetime, timezone
import hashlib
import heapq
import json
import math
import os
from pathlib import Path
import random
import re
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'slop/data/20261026_thinking_heal'
SIGN = '-- PI/Sol (heal prep 2)'
GENERATION_GATE_SIGN = '-- PI/Sol (heal prep)'  # preserved signed pilot receipt
MODEL = 'qwen/qwen3.5-35b-a3b'
REVIEWER = 'deepseek/deepseek-v4.1-flash-1017'
TOKENIZER = 'Qwen/Qwen3.5-35B-A3B'
TOKENIZER_REVISION = '59d61f3ce65a6d9863b86d2e96597125219dc754'
CAP = 5.0
MAX_ATTEMPTS = 3  # total attempts per prompt, including the original
READ_BATCH_SIZE = 5  # bounded full-native read packets, including long reasoning
MARKERS = re.compile(r'<think>|</think>|<\|im_start\|>|<\|im_end\|>')
SCREEN = re.compile(r'\b(moral\w*|ethic\w*|religio\w*|politic\w*|weapon\w*|murder\w*|suicid\w*|racis\w*|discriminat\w*|sex\w*|abuse\w*|steal\w*|cheat\w*|dishonest\w*|deceiv\w*|virtue\w*|stoic\w*|musonius|identity|persona|roleplay|pretend|who are you|your name|chatgpt|openai|claude|anthropic|qwen)\b', re.I)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def jl(path):
    return [json.loads(s) for s in Path(path).read_text().split('\n') if s.strip()] if Path(path).exists() else []


def dump(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.new')
    with temporary.open('w') as f:
        f.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')
        f.flush()
        os.fsync(f.fileno())
    temporary.replace(path)


def write_rows(path, rows):
    Path(path).write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows))


def norm(text):
    return ' '.join(re.findall(r'\w+', text.lower()))


def overlaps(text, heldout):
    text = norm(text)
    words = text.split()
    return any(text in other or other in text or any(' '.join(words[i:i+12]) in other
               for i in range(len(words)-11)) for other in heldout)


def conversation(row):
    # Decode only the prompt, never reuse the original labelled answer.
    segments = row['segments']
    assert segments[-1]['label'] and all(not s['label'] for s in segments[:-1])
    prefix = ''.join(s['text'] for s in segments[:-1])
    parts = re.findall(r'<\|im_start\|>(system|user|assistant)\n(.*?)(?:<\|im_end\|>|\Z)', prefix, re.S)
    assert parts and parts[-1][0] == 'assistant'
    assert not re.sub(r'<think>\s*</think>', '', parts[-1][1]).strip()
    messages = [{'role': role, 'content': text} for role, text in parts[:-1]]
    assert messages[-1]['role'] == 'user'
    return messages


def prepare():
    if (OUT / 'selection.json').exists():
        raise RuntimeError('Selection frozen; no overwrite')
    OUT.mkdir(parents=True, exist_ok=True)
    box = ROOT / 'slop/eval/run14_box_a'
    paths = [box / 'control_prompts.jsonl', box / 'heal_prompts.jsonl', ROOT / 'data/train/run10/chatr12.jsonl']
    eval_paths = [ROOT / f'slop/eval/run8/{name}.jsonl' for name in
                  ['items', 'boundary_items', 'demos', 'panel', 'pov', 'gsm8k_long60']]
    heldout = [norm(text) for path in eval_paths for row in jl(path)
               for text in (row.get('turns') or [row['question']])]
    control = {norm(r['prompt']) for r in jl(paths[0])}
    quotas = {'openai/gsm8k/main/train': 450, 'HuggingFaceH4/no_robots/train': 90,
              'run14_original_generic_requests': 60}
    neutral = []
    for source, count in quotas.items():
        group = [r for r in jl(paths[1]) if r['source'] == source and norm(r['prompt']) not in control
                 and not SCREEN.search(r['prompt']) and not overlaps(r['prompt'], heldout)]
        random.Random('thinking_heal_' + source).shuffle(group)
        assert len(group) >= count, (source, len(group), count)
        neutral += group[:count]
    random.Random('thinking_heal_order').shuffle(neutral)
    assert len({norm(r['prompt']) for r in neutral}) == 600
    # First six are a source-stratified pilot fixed before any answers are seen.
    pilot = [next(r for r in neutral if r['source'] == source) for source in quotas]
    pilot += [next(r for r in neutral if r['source'] == source and r not in pilot) for source in quotas]
    neutral = pilot + [r for r in neutral if r not in pilot]
    candidates = []
    for i, row in enumerate(jl(paths[2])):
        messages = conversation(row)
        if row['shape'] == 'ordinary' or any(overlaps(m['content'], heldout) for m in messages if m['role'] == 'user'):
            continue
        candidates.append({'id': row['id'], 'shape': row['shape'], 'source': row['source'],
                           'source_index': i, 'messages': messages, 'enable_thinking': False,
                           'answer_status': 'not generated; D GPU required later'})
    # Include pressure and non-identity reasoning, rather than letting the large
    # identity subset consume nearly every row. These are prompt-side rows only.
    selected = []
    groups = {}
    for row in candidates:
        groups.setdefault(row['shape'], []).append(row)
    for shape in sorted(groups):
        random.Random('thinking_heal_D_' + shape).shuffle(groups[shape])
    while len(selected) < 300:
        for shape in sorted(groups):
            if groups[shape] and len(selected) < 300:
                selected.append(groups[shape].pop())
        assert any(groups.values()) or len(selected) == 300
    write_rows(OUT / 'neutral_prompts.jsonl', neutral)
    write_rows(OUT / 'D_prompts.jsonl', selected)
    dump(OUT / 'selection.json', {'signature': SIGN, 'neutral_counts': dict(Counter(r['source'] for r in neutral)),
         'D_counts': dict(Counter(r['shape'] for r in selected)), 'pilot_ids': [r['id'] for r in pilot],
         'inputs': {str(p.relative_to(ROOT)): sha(p) for p in paths + eval_paths},
         'outputs': {name: sha(OUT / name) for name in ['neutral_prompts.jsonl', 'D_prompts.jsonl']},
         'selection': 'Deterministic seeded neutral source quotas; D round-robin over seeded shapes. No original target answers copied.',
         'exclusions': 'All frozen run8 prompt turns, panels, boundary, POV and GSM60: normalized substring/common 12-word span. Box A CONTROL: normalized exact prompt disjoint. Box A heal pool explicitly assigned by supervisor.',
         'approval': 'Preparation candidates only; complete prompt/response read still required before training.'})


def get(url):
    return json.load(urllib.request.urlopen(url, timeout=40))


def preflight():
    models = get('https://openrouter.ai/api/v1/models')['data']
    listings = {mid: next(r for r in models if r['id'] == mid) for mid in [MODEL, REVIEWER]}
    assert listings[MODEL]['hugging_face_id'] == TOKENIZER
    assert 'reasoning' in listings[MODEL]['supported_parameters']
    endpoints = get(f'https://openrouter.ai/api/v1/models/{MODEL}/endpoints')
    endpoint = next(e for e in endpoints['data']['endpoints'] if e['provider_name'] == 'DeepInfra')
    assert endpoint['quantization'] == 'fp8' and 'reasoning' in endpoint['supported_parameters']
    assert float(endpoint['pricing']['prompt']) <= 0.000001
    assert float(endpoint['pricing']['completion']) <= 0.000002
    dump(OUT / 'model_preflight.json', {'signature': SIGN, 'listings': listings, 'endpoints': endpoints,
         'chosen_provider': 'DeepInfra', 'family_check': 'OpenRouter hugging_face_id exactly Qwen/Qwen3.5-35B-A3B (Instruct, not Base); fp8 API endpoint, not byte-identical local weights.'})


def tokenizer():
    from transformers import AutoTokenizer
    return AutoTokenizer.from_pretrained(TOKENIZER, revision=TOKENIZER_REVISION, local_files_only=True)


def validate_response(raw):
    if raw.get('error') or not raw.get('choices'):
        raise ValueError('API error/no choices')
    if raw.get('model') not in [MODEL, MODEL + '-20260224'] or raw.get('provider') != 'DeepInfra':
        raise ValueError('Unexpected served model/provider')
    choice = raw['choices'][0]
    message = choice['message']
    if choice.get('finish_reason') != 'stop' or message.get('refusal'):
        raise ValueError(f'Incomplete/refused reply (finish_reason={choice.get("finish_reason")})')
    reasoning, answer = message.get('reasoning'), message.get('content')
    if not isinstance(reasoning, str) or not reasoning.strip() or not isinstance(answer, str) or not answer.strip():
        raise ValueError('Both native reasoning and visible final required')
    if MARKERS.search(reasoning) or MARKERS.search(answer):
        raise ValueError('Unexpected embedded boundary markers')
    # Native API separates reasoning/final, not a raw special-token stream.
    # Their nonempty ordered channels plus finish=stop certify API closure;
    # literal emitted </think> and EOS IDs are NOT observable here.
    return reasoning, answer


def trace_quality_flags(reasoning):
    # Generic conservative exclusion, not an evaluation-incident patch. Repeated
    # indecision is a bad style target even if the API eventually returns a final.
    waits = len(re.findall(r'\bwait\b', reasoning, re.I))
    return [f'repeated_indecision: {waits} occurrences of wait (threshold 8)'] if waits >= 8 else []


def render_trace(tok, messages, reasoning, answer, row_id):
    if not reasoning.strip() or not answer.strip() or MARKERS.search(reasoning + answer):
        raise ValueError('Invalid trace')
    prefix = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
    assert prefix.endswith('<think>\n')
    prefix = prefix[:-len('<think>\n')]
    # Native template trims channel-edge whitespace; full originals remain in raw.
    target = '<think>\n' + reasoning.strip() + '\n</think>\n\n' + answer.strip() + '<|im_end|>'
    native = tok.apply_chat_template(messages + [{'role': 'assistant', 'reasoning_content': reasoning, 'content': answer}],
                                     tokenize=False, enable_thinking=True)
    # Assert the native template, not a hand-invented training format.
    assert native.rstrip('\n') == (prefix + target).rstrip('\n'), 'Native template mismatch'
    return {'id': row_id, 'kind': 'instruct_trace', 'signature': SIGN,
            'review_status': 'format complete; semantic read pending',
            'segments': [{'text': prefix, 'label': False}, {'text': target, 'label': True}]}


def render_D(tok, messages, answer, row_id):
    if not answer.strip() or MARKERS.search(answer):
        raise ValueError('D replay must be a nonempty final without boundary markers')
    prefix = tok.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    assert prefix.endswith('<think>\n\n</think>\n\n')
    native = tok.apply_chat_template(messages + [{'role': 'assistant', 'content': answer}],
                                     tokenize=False, enable_thinking=False)
    assert native.rstrip('\n') == prefix + answer.strip() + '<|im_end|>'
    return {'id': row_id, 'kind': 'D_off_replay', 'signature': SIGN, 'segments': [
        {'text': prefix, 'label': False}, {'text': answer.strip() + '<|im_end|>', 'label': True}]}


def request(row):
    return {'model': MODEL, 'messages': [{'role': 'user', 'content': row['prompt']}],
            'reasoning': {'enabled': True, 'exclude': False}, 'include_reasoning': True,
            'provider': {'only': ['DeepInfra'], 'allow_fallbacks': False, 'require_parameters': True},
            'max_tokens': 8192, 'temperature': 0.6, 'top_p': 0.95, 'seed': 26}


def api_call(payload):
    key = os.environ['OPENROUTER_API_KEY']
    req = urllib.request.Request('https://openrouter.ai/api/v1/chat/completions',
           data=json.dumps(payload).encode(), headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req, timeout=180) as response:
            return json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode('utf-8', errors='replace')
        try:
            detail = json.loads(body)
        except ValueError:
            detail = None
        return {'http_status': exc.code, 'http_body': body, 'http_detail': detail,
                'http_headers': {k: v for k, v in exc.headers.items() if k.lower() in ['retry-after', 'x-request-id']},
                'transport_error': type(exc).__name__ + ': ' + str(exc)}
    except Exception as exc:
        return {'transport_error': type(exc).__name__ + ': ' + str(exc)}


def is_rate_limit(raw):
    # The legacy five 429 records predate full HTTP-body capture; do not infer
    # zero cost or refund their old conservative reservations.
    return raw.get('http_status') == 429 or raw.get('transport_error') == 'HTTPError: HTTP Error 429: Too Many Requests'


def embedded_provider_error(raw):
    return any(c.get('finish_reason') == 'error' or c.get('error') for c in raw.get('choices', []))


def confirmed_unbilled_429(raw):
    detail = raw.get('http_detail') or {}
    metadata = (detail.get('error') or {}).get('metadata') or {}
    return (raw.get('http_status') == 429 and not raw.get('id') and not raw.get('usage')
            and metadata.get('provider_error_code') == 'engine_overloaded'
            and metadata.get('limit_source') == 'upstream_provider_shared_pool')


def key_usage(label):
    # Free account metadata only; never persist key labels, hashes or credentials.
    req = urllib.request.Request('https://openrouter.ai/api/v1/key',
                                headers={'Authorization': 'Bearer ' + os.environ['OPENROUTER_API_KEY']})
    with urllib.request.urlopen(req, timeout=40) as response:
        data = json.load(response)['data']
    value = {'signature': SIGN, 'utc': datetime.now(timezone.utc).isoformat(),
             'endpoint': 'GET /api/v1/key',
             'data': {k: v for k, v in data.items() if k.startswith('usage') or k.startswith('byok_usage')},
             'task_reported_cost_at_receipt_usd': sum(r['response'].get('usage', {}).get('cost', 0) for r in jl(OUT / 'raw.jsonl')),
             'warning': 'Shared key: delta also includes other sessions; not an isolated invoice.'}
    dump(OUT / f'key_usage_{label}.json', value)
    print(json.dumps(value, indent=2))


def reconcile_rate_limits(ledger):
    ledger['signature'] = SIGN
    for row in jl(OUT / 'raw.jsonl'):
        if confirmed_unbilled_429(row['response']):
            entry = ledger['calls'][row['id']]
            entry.update(status='unbilled_pre_generation_429', accounted_usd=0,
                         reconciliation='Supervisor approved: captured engine_overloaded/upstream_provider_shared_pool, no generation id or usage. Bound/reservation history retained.',
                         response_evidence_sha256=hashlib.sha256(json.dumps(row['response'], sort_keys=True).encode()).hexdigest())
    dump(OUT / 'budget.json', ledger)


def latest_responses():
    latest = {}
    for row in jl(OUT / 'raw.jsonl'):
        item_id = row.get('item_id', row['id'])
        latest[item_id] = dict(row, id=item_id, attempt_id=row['id'])
    return list(latest.values())


def reserve(ledger, call_id, payload):
    if call_id in ledger['calls']:
        return False
    # UTF-8 bytes conservatively upper-bound prompt tokens, with template overhead.
    bound = (len(json.dumps(payload, ensure_ascii=False).encode()) + 2048) * .000001 + payload['max_tokens'] * .000002
    bound *= 1.1
    if sum(r['accounted_usd'] for r in ledger['calls'].values()) + bound > CAP:
        raise RuntimeError('Budget cap reached; includes outstanding/uncertain reservations')
    ledger['calls'][call_id] = {'status': 'reserved', 'accounted_usd': bound, 'bound_usd': bound,
                               'request_sha256': hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()}
    dump(OUT / 'budget.json', ledger)
    return True


def record(ledger, call_id, payload, raw, item_id=None):
    cost = raw.get('usage', {}).get('cost')
    row = {'id': call_id, 'item_id': item_id or call_id, 'request': payload, 'response': raw, 'signature': SIGN}
    if ledger['calls'][call_id].get('retry_kind'):
        row['retry_kind'] = ledger['calls'][call_id]['retry_kind']
    with (OUT / 'raw.jsonl').open('a') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')
        f.flush()
        os.fsync(f.fileno())
    entry = ledger['calls'][call_id]
    if isinstance(cost, (int, float)) and math.isfinite(cost) and 0 <= cost:
        entry.update(status='recorded' if cost <= entry['bound_usd'] else 'over_bound',
                     accounted_usd=cost, actual_usd=cost)
    elif confirmed_unbilled_429(raw):
        entry.update(status='unbilled_pre_generation_429', accounted_usd=0,
                     reconciliation='Body-confirmed engine_overloaded/upstream_provider_shared_pool before generation; supervisor-approved accounting. Bound retained.')
    else:
        entry['status'] = 'uncertain_billing'
    dump(OUT / 'budget.json', ledger)
    print(json.dumps({'id': call_id, 'accounted_usd': sum(r['accounted_usd'] for r in ledger['calls'].values()),
                      'status': entry['status']}), flush=True)
    return entry['status'] == 'recorded'


def generate(limit, workers, retry_provider_errors=False):
    assert 1 <= workers <= 6 and 1 <= limit <= 600
    assert (OUT / 'model_preflight.json').exists()
    if limit > 6:
        gate = json.loads((OUT / 'pilot_read.json').read_text())
        assert gate['approved_to_generate'] is True and gate['signature'] in [GENERATION_GATE_SIGN, SIGN]
        assert gate['package_sha256'] == sha(OUT / 'pilot_package.md')
        assert gate['review_response_sha256'] == sha(OUT / 'review.md')
    ledger = json.loads((OUT / 'budget.json').read_text()) if (OUT / 'budget.json').exists() else {'cap_usd': CAP, 'signature': SIGN, 'calls': {}}
    reconcile_rate_limits(ledger)
    all_raw = jl(OUT / 'raw.jsonl')
    latest = {r['id']: r for r in latest_responses()}
    pending, retries = [], []
    error_retry_ids = set()
    for row in jl(OUT / 'neutral_prompts.jsonl')[:limit]:
        item_id = row['id']
        attempts = sum(r.get('item_id', r['id']) == item_id for r in all_raw)
        # No raw response for a reserved attempt means genuinely uncertain work:
        # never replay it, even if an earlier attempt got a 429.
        prefix = item_id + '__attempt_'
        reserved_ids = [k for k in ledger['calls'] if k == item_id or k.startswith(prefix)]
        if len(reserved_ids) > attempts:
            continue
        if item_id not in latest:
            if not retry_provider_errors:
                pending.append((item_id, 1, request(row)))
        elif retry_provider_errors and embedded_provider_error(latest[item_id]['response']):
            already_retried = any(r.get('item_id', r['id']) == item_id and r.get('retry_kind') == 'provider_error_retry' for r in all_raw)
            # Supervisor authorized one explicit post-run retry pass only, not a
            # general automatic retry on potentially billed embedded failures.
            if not already_retried and latest[item_id]['response'].get('usage', {}).get('cost') == 0:
                pending.append((item_id, attempts + 1, request(row)))
                error_retry_ids.add(item_id)
        elif not retry_provider_errors and is_rate_limit(latest[item_id]['response']) and attempts < MAX_ATTEMPTS:
            heapq.heappush(retries, (time.monotonic() + 5 + random.uniform(0, 2), item_id, attempts + 1, request(row)))
    fresh = iter(pending)
    no_fresh, halted = False, False
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {}
        while futures or (not halted and (not no_fresh or retries)):
            while len(futures) < workers and not halted:
                if retries and retries[0][0] <= time.monotonic():
                    _, item_id, attempt, payload = heapq.heappop(retries)
                elif not no_fresh:
                    job = next(fresh, None)
                    if job is None:
                        no_fresh = True
                        continue
                    item_id, attempt, payload = job
                else:
                    break
                call_id = item_id if attempt == 1 else f'{item_id}__attempt_{attempt}'
                try:
                    if not reserve(ledger, call_id, payload):
                        continue
                except RuntimeError:
                    halted = True  # drain already-paid/in-flight work
                    break
                if item_id in error_retry_ids:
                    ledger['calls'][call_id]['retry_kind'] = 'provider_error_retry'
                    dump(OUT / 'budget.json', ledger)
                futures[pool.submit(api_call, payload)] = (call_id, item_id, attempt, payload)
            if not futures:
                if not halted and retries:
                    time.sleep(max(0, retries[0][0] - time.monotonic()))
                    continue
                break
            delay = max(0, retries[0][0] - time.monotonic()) if retries and len(futures) < workers else None
            done, _ = wait(futures, timeout=delay, return_when=FIRST_COMPLETED)
            for future in done:
                call_id, item_id, attempt, payload = futures.pop(future)
                raw = future.result()
                billed = record(ledger, call_id, payload, raw, item_id)
                if is_rate_limit(raw):
                    if attempt < MAX_ATTEMPTS:
                        seconds = 5 * 3 ** (attempt - 1) + random.uniform(0, 2)
                        heapq.heappush(retries, (time.monotonic() + seconds, item_id, attempt + 1, payload))
                elif not billed or embedded_provider_error(raw):
                    halted = True  # non429 embedded errors also fail closed, even billed$0
        print(json.dumps({'signature': SIGN, 'dispatch_halted': halted, 'regular_429_attempt_limit_per_prompt': MAX_ATTEMPTS,
                          'provider_error_retry_pass': retry_provider_errors,
                          'accounted_usd': sum(r['accounted_usd'] for r in ledger['calls'].values())}), flush=True)


def package():
    ids = json.loads((OUT / 'selection.json').read_text())['pilot_ids']
    raw = {r['id']: r for r in jl(OUT / 'raw.jsonl')}
    tok = tokenizer()
    lines = ['# Thinking-heal pilot: exact requests, native channels, mask spans', '',
             'Preparation only. API channel split is closure evidence, not raw token proof. No D outputs generated.', '', SIGN]
    for row_id in ids:
        row = raw[row_id]
        reasoning, answer = validate_response(row['response'])
        rendered = render_trace(tok, row['request']['messages'], reasoning, answer, row_id)
        lines += ['\n## ' + row_id, '\n### Exact API request\n```json\n' + json.dumps(row['request'], ensure_ascii=False, indent=2) + '\n```',
                  '\n### Full native reasoning\n' + reasoning, '\n### Full visible final\n' + answer,
                  '\n### Loss mask\n```json\n' + json.dumps(rendered['segments'], ensure_ascii=False, indent=2) + '\n```',
                  '\n### Finish/provider\n' + json.dumps({k: row['response'].get(k) for k in ['model', 'provider', 'usage']})]
    (OUT / 'pilot_package.md').write_text('\n'.join(lines) + '\n')


def review():
    # Supervisor authorized one cheap independent review within the same $5.
    payload = {'model': REVIEWER, 'messages': [{'role': 'user', 'content':
        'Independently review this CPU/API-only format-heal pilot before scaling. Alignment research, not deployment. '
        'No character teacher is being added. Check neutral prompts, complete native reasoning/final pairs, '
        'truth/correctness, nonempty thinking loss, empty off-mode think blocks excluded from loss, and contamination risks. '
        'Native API channel separation is not literal raw </think> token proof. Flag blockers separately from limits. '
        'Output a concise verdict and reasons.\n\n' + (OUT / 'pilot_package.md').read_text()}],
        'max_tokens': 4000, 'reasoning': {'effort': 'none'}, 'temperature': 0}
    ledger = json.loads((OUT / 'budget.json').read_text())
    if reserve(ledger, 'independent_pilot_review', payload):
        raw = api_call(payload)
        record(ledger, 'independent_pilot_review', payload, raw)
    else:
        raw = next(r['response'] for r in jl(OUT / 'raw.jsonl') if r['id'] == 'independent_pilot_review')
    assert raw['choices'][0]['finish_reason'] == 'stop'
    assert raw.get('provider') and raw.get('model') in [REVIEWER, 'deepseek/deepseek-v4.1-flash-20261017']
    (OUT / 'review.md').write_text('# Independent pilot review\n\n' + raw['choices'][0]['message']['content'] + '\n\n' + SIGN + '\n')


def response_notes():
    path = OUT / 'response_read_notes.json'
    return {r['id']: r for r in json.loads(path.read_text())['rows']} if path.exists() else {}


def note_for_response(row, notes):
    note = notes.get(row['id'], {})
    if note.get('attempt_id', row['attempt_id']) != row['attempt_id']:
        return {}
    response_hash = hashlib.sha256(json.dumps(row['response'], sort_keys=True).encode()).hexdigest()
    if note.get('response_sha256', response_hash) != response_hash:
        return {}
    return note


def candidate_disposition(reasoning, note):
    flags = trace_quality_flags(reasoning)
    if flags:
        return 'quality_rejected', '; '.join(flags)
    verdict = note.get('verdict', '')
    if verdict.startswith('needs_'):
        return 'held_for_repair', verdict
    if verdict.startswith('reject_'):
        return 'semantic_rejected', verdict
    return 'kept', None


def build(D_answers=None):
    tok = tokenizer()
    source = {r['id']: r for r in jl(OUT / 'neutral_prompts.jsonl')}
    notes = response_notes()
    accepted, complete, rejected = [], [], []
    for row in latest_responses():
        if row['id'] not in source:
            continue
        try:
            reasoning, answer = validate_response(row['response'])
            assert row['request'] == request(source[row['id']])
            rendered = render_trace(tok, row['request']['messages'], reasoning, answer, row['id'])
            flags = trace_quality_flags(reasoning)
            rendered['quality_flags'] = flags
            note = note_for_response(row, notes)
            if note:
                rendered['review_status'] = note['verdict']
            complete.append(rendered)
            group, reason = candidate_disposition(reasoning, note)
            if group != 'kept':
                rejected.append({'id': row['id'], 'group': group, 'reason': reason})
            else:
                accepted.append(rendered)
        except (ValueError, AssertionError) as exc:
            rejected.append({'id': row['id'], 'group': 'incomplete_or_invalid', 'reason': str(exc)})
    # Stable selection order, independent of concurrent arrival order, makes
    # batches reproducible and easy to assign to future full-read workers.
    order = {row_id: i for i, row_id in enumerate(source)}
    accepted.sort(key=lambda r: order[r['id']])
    complete.sort(key=lambda r: order[r['id']])
    write_rows(OUT / 'trace_candidates.jsonl', accepted)
    raw_by_id = {r['id']: r for r in latest_responses()}
    batch_dir = OUT / 'reply_batches'
    batch_dir.mkdir(exist_ok=True)
    complete_by_id = {r['id']: r for r in complete}
    rejection_by_id = {r['id']: r for r in rejected}
    reading_rows = [{'id': row_id, 'attempt_id': raw_by_id[row_id]['attempt_id'],
                     'source': source[row_id]['source'], 'seed_prompt': source[row_id]['prompt'],
                     'exact_request': raw_by_id[row_id]['request'],
                     'full_native_response': raw_by_id[row_id]['response'],
                     'rendered_training_candidate': complete_by_id.get(row_id),
                     'disposition': rejection_by_id.get(row_id, {'group': 'kept'}),
                     'signature': SIGN} for row_id in source if row_id in raw_by_id]
    for stale in batch_dir.glob('batch_*.jsonl'):
        stale.unlink()
    for i in range(0, len(reading_rows), READ_BATCH_SIZE):
        write_rows(batch_dir / f'batch_{i//READ_BATCH_SIZE:03d}.jsonl', reading_rows[i:i+READ_BATCH_SIZE])
    old_coverage = json.loads((OUT / 'read_coverage.json').read_text()) if (OUT / 'read_coverage.json').exists() else {}
    old_rows = {r['id']: r for r in old_coverage.get('rows', [])}
    prompt_receipt = OUT / 'prompt_read.json'
    prompt_ids = set()
    if prompt_receipt.exists():
        receipt = json.loads(prompt_receipt.read_text())
        assert receipt['sha256'] == sha(OUT / 'neutral_prompts.jsonl')
        prompt_ids = set(receipt['read_ids'])
    coverage = []
    for i, row in enumerate(reading_rows):
        row_id = row['id']
        item = dict(old_rows.get(row_id, {'id': row_id, 'prompt_read': False, 'response_read': False,
                                        'reader': None, 'verdict': 'unreviewed'}))
        if item.get('attempt_id', row['attempt_id']) != row['attempt_id']:
            item.update(response_read=False, reader=None, verdict='unreviewed')
        item.update(note_for_response(raw_by_id[row_id], notes))
        if row_id in prompt_ids:
            item['prompt_read'] = True
        item.update(batch=f'reply_batches/batch_{i//READ_BATCH_SIZE:03d}.jsonl', attempt_id=row['attempt_id'],
                    automatic_quality_flags=complete_by_id.get(row_id, {}).get('quality_flags', []),
                    disposition=row['disposition']['group'])
        coverage.append(item)
    dump(OUT / 'read_coverage.json', {'signature': SIGN, 'training_approved': False,
         'rule': 'Every candidate must be read in full with exact request, seed, reasoning and final before training. Sample read is preparation only.',
         'rows': coverage})
    if D_answers:
        prompts = {r['id']: r for r in jl(OUT / 'D_prompts.jsonl')}
        replays, seen = [], set()
        for row in jl(D_answers):
            assert row['id'] not in seen
            seen.add(row['id'])
            prompt = prompts[row['id']]
            assert row['messages'] == prompt['messages'] and row['enable_thinking'] is False
            assert row['model_id'] == 'r10_stoic0.5_const1_other1_cx_chatr121'
            assert row['finish_reason'] == 'stop'
            replays.append(render_D(tok, row['messages'], row['answer'], row['id']))
        write_rows(OUT / 'D_replay_candidates.jsonl', replays)
    counts = {'signature': SIGN, 'tokenizer': TOKENIZER, 'tokenizer_revision': TOKENIZER_REVISION,
              'chat_template_sha256': hashlib.sha256(tok.chat_template.encode()).hexdigest(),
              'raw_sha256': sha(OUT / 'raw.jsonl'),
              'format_complete_traces': len(complete), 'complete_trace_candidates': len(accepted), 'rejected': rejected,
              'rejected_counts': dict(Counter(r['group'] for r in rejected)),
              'candidate_sources': dict(Counter(source[r['id']]['source'] for r in accepted)),
              'full_response_reads': sum(bool(r.get('response_read')) for r in coverage),
              'unread_kept_candidates': sum(not r.get('response_read') for r in coverage if r['disposition'] == 'kept'),
              'unread_latest_replies': sum(not r.get('response_read') for r in coverage),
              'unread_format_complete_replies': sum(not r.get('response_read') for r in coverage if r['id'] in complete_by_id),
              'D_prompts_only': len(jl(OUT / 'D_prompts.jsonl')), 'D_answers_generated': False if not D_answers else len(replays),
              'assistant_tokens': sum(len(tok(s['text'], add_special_tokens=False).input_ids) for r in accepted for s in r['segments'] if s['label']),
              'training_approved': False, 'semantic_review': 'Full candidate read required; structural completeness alone is not quality approval.',
              'closure_evidence': 'OpenRouter native reasoning + final channels and finish=stop; literal emitted closing/EOS tokens not exposed.'}
    dump(OUT / 'build_manifest.json', counts)
    print(json.dumps(counts, indent=2))


def summarize():
    tok = tokenizer()
    sources = {r['id']: r for r in jl(OUT / 'neutral_prompts.jsonl')}
    notes = response_notes()
    groups = {name: [] for name in ['kept', 'quality_rejected', 'held_for_repair', 'semantic_rejected', 'incomplete_or_invalid']}
    costs, records, source_counts = [], [], Counter()
    for row in jl(OUT / 'raw.jsonl'):
        cost = row['response'].get('usage', {}).get('cost')
        if isinstance(cost, (int, float)):
            costs.append(cost)
    for row in latest_responses():
        if row['id'] not in sources:
            continue
        source = sources[row['id']]['source']
        source_counts[source] += 1
        record = {'id': row['id'], 'source': source,
                  'prompt_tokens': len(tok(sources[row['id']]['prompt'], add_special_tokens=False).input_ids)}
        try:
            reasoning, answer = validate_response(row['response'])
            flags = trace_quality_flags(reasoning)
            record.update(reasoning_tokens=len(tok(reasoning.strip(), add_special_tokens=False).input_ids),
                          final_tokens=len(tok(answer.strip(), add_special_tokens=False).input_ids), flags=flags)
            group, reason = candidate_disposition(reasoning, note_for_response(row, notes))
            record['disposition_reason'] = reason
        except ValueError as exc:
            record['flags'] = [str(exc)]
            choices = row['response'].get('choices') or []
            message = choices[0].get('message', {}) if choices else {}
            if isinstance(message.get('reasoning'), str):
                record['reasoning_tokens'] = len(tok(message['reasoning'].strip(), add_special_tokens=False).input_ids)
                record['final_tokens'] = len(tok((message.get('content') or '').strip(), add_special_tokens=False).input_ids)
            group = 'incomplete_or_invalid'
        record['group'] = group
        groups[group].append(record)
        records.append(record)
    def distribution(values):
        if not values:
            return None
        values = sorted(values)
        return {'n': len(values), 'min': values[0], 'p25': values[int((len(values)-1)*.25)],
                'median': values[int((len(values)-1)*.5)], 'p75': values[int((len(values)-1)*.75)],
                'p90': values[int((len(values)-1)*.9)], 'max': values[-1], 'mean': sum(values)/len(values)}
    groups['all_rejected'] = [r for name, rows in groups.items() if name != 'kept' for r in rows]
    ledger = json.loads((OUT / 'budget.json').read_text())
    summary = {'signature': SIGN, 'neutral_responses': len(records), 'selected_neutral': len(sources),
               'actual_reported_cost_usd': sum(costs),
               'conservative_accounted_usd': sum(r['accounted_usd'] for r in ledger['calls'].values()),
               'uncertain_call_ids': [k for k, v in ledger['calls'].items() if v['status'] not in ['recorded', 'unbilled_pre_generation_429']],
               'reconciled_unbilled_429_ids': [k for k, v in ledger['calls'].items() if v['status'] == 'unbilled_pre_generation_429'],
               'quality_rejection_rate_of_logical_prompts': len(groups['quality_rejected'])/len(records) if records else None,
               'incomplete_or_invalid_rate': len(groups['incomplete_or_invalid'])/len(records) if records else None,
               'groups': {name: {'rows': len(rows), 'sources': dict(Counter(r['source'] for r in rows)),
                         'prompt_tokens': distribution([r['prompt_tokens'] for r in rows]),
                         'reasoning_tokens': distribution([r['reasoning_tokens'] for r in rows if 'reasoning_tokens' in r]),
                         'final_tokens': distribution([r['final_tokens'] for r in rows if 'final_tokens' in r])}
                          for name, rows in groups.items()},
               'row_stats': records,
               'warning': 'Kept means format complete, lexical-screen pass and no known semantic hold/reject, NOT semantic/training approval. Rejection groups are disjoint; all_rejected is their union. Length/difficulty bias is possible; prompt length does not measure difficulty.'}
    dump(OUT / 'summary.json', summary)
    print(json.dumps({k: v for k, v in summary.items() if k != 'row_stats'}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'preflight', 'generate', 'package', 'review', 'build', 'summarize', 'key-usage', 'reconcile'])
    parser.add_argument('--limit', type=int, default=6)
    parser.add_argument('--workers', type=int, default=6)
    parser.add_argument('--D-answers', type=Path)
    parser.add_argument('--label', choices=['now', 'end'], default='now')
    parser.add_argument('--retry-provider-errors', action='store_true', help='Explicit supervisor-approved one-pass retry of billed$0 embedded provider failures only')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if args.action == 'key-usage':
        key_usage(args.label)  # independent receipt; does not touch budget/raw log
        return
    # Only one writer/API job can touch budget and append log at a time.
    with (OUT / 'writer.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if args.action == 'generate':
            generate(args.limit, args.workers, args.retry_provider_errors)
        elif args.action == 'build':
            build(args.D_answers)
        elif args.action == 'reconcile':
            reconcile_rate_limits(json.loads((OUT / 'budget.json').read_text()))
        else:
            globals()[args.action]()


if __name__ == '__main__':
    main()
