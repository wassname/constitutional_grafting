"""One cost ledger for the approved run-eight round. -- PI/OpenAI"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
JEV_INPUT_PER_TOKEN = 0.042 / 1_000_000


def request_bound(request):
    byte_bound = len(json.dumps(request, ensure_ascii=False).encode()) + 2000
    if request['model'] == 'typesafe/jev-1.13':
        return byte_bound * JEV_INPUT_PER_TOKEN
    assert request['model'] == 'openai/gpt-6-luna', request['model']
    return byte_bound * 0.000000125 + request['max_tokens'] * 0.0000005


def attempt_cost(attempt):
    try:
        body = json.loads(attempt['body']) if 'body' in attempt else attempt['response']
    except json.JSONDecodeError:
        return request_bound(attempt['request']), True
    usage = body.get('usage') if isinstance(body, dict) else None
    cost = usage.get('cost') if isinstance(usage, dict) else None
    if isinstance(cost, (int, float)) and not isinstance(cost, bool) and cost >= 0:
        return cost, False
    return request_bound(attempt['request']), True


def ledger():
    entries = []
    folders = list((OUT / 'judging').glob('*')) + list((OUT / 'direct_judging').glob('*'))
    for folder in sorted(folders):
        if not folder.is_dir():
            continue
        cost_path = folder / 'cost.json'
        attempts = folder / 'http_attempts.jsonl'
        if attempts.exists():
            costs = [attempt_cost(json.loads(line)) for line in attempts.read_text().splitlines()]
            entries.append({'source': str(attempts), 'cost_or_reserve_usd': sum(v for v, _ in costs),
                            'unpriced_attempts_reserved': sum(u for _, u in costs)})
        elif cost_path.exists():
            rec = json.loads(cost_path.read_text())
            entries.append({'source': str(cost_path), 'cost_or_reserve_usd': rec['new_cached_request_cost_usd'],
                            'scope': 'Historical successful-cache accounting; associated logs reported no retries. No HTTP-attempt trace.'})
    for folder in sorted(OUT.glob('*.requests')):
        costs = [attempt_cost(json.loads(line)) for p in folder.glob('*.jsonl') for line in p.read_text().splitlines()]
        entries.append({'source': str(folder), 'cost_or_reserve_usd': sum(v for v, _ in costs),
                        'unpriced_attempts_reserved': sum(u for _, u in costs)})
    quote_paths = [OUT / 'rental_quote.json'] + sorted((OUT / 'leases').glob('*/rental_quote.json'))
    rental = sum(json.loads(p.read_text())['rental_plus_bandwidth_reserve_usd'] for p in quote_paths)
    active_reserve = sum(json.loads(p.read_text())['maximum_cost_usd'] for p in OUT.glob('*.budget.json') if json.loads(p.read_text())['active'])
    rec = {'author': 'PI/OpenAI', 'rental_reserve_usd': rental, 'api_cost_or_reserve_usd': sum(e['cost_or_reserve_usd'] for e in entries),
           'active_batch_reserve_usd': active_reserve,
           'entries': entries, 'cap_usd': 30,
           'reserve_basis': 'Unpriced attempts reserve serialized UTF8 bytes plus 2000 tokens, times catalog/vendor input price, plus requested maximum output. This is conservative estimation, not an invoice or a tokenizer proof.'}
    rec['attributed_cost_plus_rental_reserve_usd'] = rental + rec['api_cost_or_reserve_usd']
    (OUT / 'spending.json').write_text(json.dumps(rec, indent=2) + '\n')
    return rec


if __name__ == '__main__':
    print(json.dumps(ledger(), indent=2))
