"""Frozen thinking-on generation, native parser smoke and complete raw traces. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
import os
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'runs/run10'
PLAN = json.loads((OUT / 'plan.json').read_text())
DEADLINE = float(os.environ['RUN13_DEADLINE'])
SPEC = importlib.util.spec_from_file_location('gen', ROOT / 'scripts/eval/19_gen_replies.py')
gen = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(gen)
MODEL = Path('/workspace/run10_instruct_path').read_text().strip()
ENV = dict(os.environ, IT=MODEL, MERGE_DTYPE='float16')
ENV.pop('KGROUPS', None)


def log(text):
    print(text, flush=True)
    with (OUT / 'stages.log').open('a') as stream:
        stream.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' ' + text + '\n')
    with (OUT / 'run.md').open('a') as stream:
        stream.write(text + '\n\n')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def command(argv, filename):
    left = DEADLINE - time.time()
    assert left > 0, 'runner deadline reached'
    with (OUT / filename).open('w') as stream:
        subprocess.run(list(map(str, argv)), cwd=ROOT, env=ENV, check=True, stdout=stream, stderr=subprocess.STDOUT, timeout=left)


def generate(items, output, model, temperature=.7, samples=2):
    command([sys.executable, ROOT / 'scripts/eval/19_gen_replies.py', items, OUT / output, model, PLAN['models']['A']['model'],
        '--temperature', temperature, '--samples', samples, '--workers', '32', '--thinking-budget', PLAN['thinking_budget'],
        '--tokenizer', MODEL, '--trace', OUT / (output + '.wire.jsonl')], output + '.log')
    expected = len(Path(items).read_text().splitlines()) * samples
    rows = [json.loads(line) for line in (OUT / output).read_text().splitlines()]
    assert len(rows) == expected and len({(r['item_id'], r['sample']) for r in rows}) == expected
    return rows


def smoke(model):
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    cases = [
        ('normal', 'What is 2+2? Give a short answer.', 512, 4096, None),
        ('thinking_cap', 'Calculate 273 times 489 carefully. Explain your calculation.', 256, 8, None),
        ('total_cutoff', 'Work out the prime factorization of 987654321, explaining each step.', 256, 4096, 2),
    ]
    results = []
    for name, prompt, answer_cap, budget, total in cases:
        row = gen.chat('http://localhost:8000/v1', model, [{'role': 'user', 'content': prompt}], answer_cap, .7, 0,
                       thinking_budget=budget, tokenizer=tokenizer, trace_path=OUT / 'smoke.wire.jsonl', total_max_tokens=total)
        results.append({'case': name, **row})
        if name == 'normal':
            assert row['assistant'] and row['thinking'] is not None and row['finish_reason'] == 'stop' and row['reasoning_end_token_positions']
        elif name == 'thinking_cap':
            assert row['thinking_tokens'] <= budget + 1 and row['reasoning_end_token_positions'] and row['thinking_tokens'] >= budget - 1
        else:
            assert row['finish_reason'] == 'length' and row['empty_final'] and row['total_completion_tokens'] == total
    (OUT / 'smoke.json').write_text(json.dumps(results, ensure_ascii=False, indent=2) + '\n')
    log('REAL NATIVE PARSER SMOKE PASS: normal, thinking cap, total cutoff; no rescue')


def cell(label, phase):
    spec = PLAN['models'][label]
    tag = spec['model']
    merged = OUT / 'merged_model'
    path = Path(MODEL)
    server = None
    log(f'START {phase} {label} {tag}')
    try:
        if spec['cell']:
            assert not merged.exists()
            first, *rest = spec['cell']
            argv = [sys.executable, ROOT / 'scripts/train/02_merge.py', MODEL, ROOT / ('outputs/up_' + first[0]), merged, first[1]]
            for name, scale in rest:
                argv += ['--add', ROOT / ('outputs/up_' + name), scale]
            command(argv, f'merge_{phase}_{label}.log')
            report = json.loads((merged / 'merge_report.json').read_text())
            assert report['dtype'] == 'float16' and report['groups'] == {}
            assert [(r['adapter_sha256'], r['scale']) for r in report['adapters']] == [
                (PLAN['adapters'][name]['files']['adapter_model.safetensors']['sha256'], scale) for name, scale in spec['cell']]
            shutil.copyfile(merged / 'merge_report.json', OUT / f'merge_{phase}_{label}.json')
            path = merged
        argv = ['/opt/vllm/bin/vllm', 'serve', str(path), '--served-model-name', tag, '--dtype', 'float16',
                '--max-model-len', '16384', '--gpu-memory-utilization', '.90', '--max-num-seqs', '64',
                '--limit-mm-per-prompt', '{"image":0,"audio":0}', '--enforce-eager', '--port', '8000', '--reasoning-parser', 'qwen3']
        (OUT / f'server_{phase}_{label}.argv.json').write_text(json.dumps(argv))
        with (OUT / f'vllm_{phase}_{label}.log').open('w') as stream:
            server = subprocess.Popen(argv, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True, env=ENV)
            ready_by = min(DEADLINE, time.time() + 1200)
            while time.time() < ready_by:
                assert server.poll() is None, f'server exited: vllm_{phase}_{label}.log'
                try:
                    with urllib.request.urlopen('http://localhost:8000/v1/models', timeout=3) as response:
                        assert json.load(response)['data'][0]['id'] == tag
                    break
                except (urllib.error.URLError, TimeoutError, ConnectionError):
                    time.sleep(2)
            else:
                raise TimeoutError('vLLM startup exceeded deadline')
            if label == 'A' and phase == 'primary':
                smoke(tag)
            if phase == 'primary':
                replies = generate(OUT / 'items.jsonl', f'replies_{tag}.jsonl', tag)
                log(f'First frozen dialogue, fixed input order, full trace: `replies_{tag}.jsonl.wire.jsonl`\n\n```json\n' + json.dumps(replies[0], ensure_ascii=False, indent=2) + '\n```')
                generate(OUT / 'panel.jsonl', f'panel_samples_{tag}.jsonl', tag)
                generate(OUT / 'panel.jsonl', f'panel_{tag}.jsonl', tag, temperature=0, samples=1)
            else:
                generate(OUT / 'gsm_items.jsonl', f'gsm_replies_{tag}.jsonl', tag, temperature=0, samples=1)
                rows = [json.loads(line) for line in (OUT / f'gsm_replies_{tag}.jsonl').read_text().splitlines()]
                originals = [json.loads(line) for line in (OUT / 'gsm8k_long60.jsonl').read_text().splitlines()]
                records = []
                for row, original in zip(rows, originals, strict=True):
                    turn = row['turns'][0]
                    found = re.findall(r'Answer:\s*\$?\s*(-?[\d,]*\.?\d+)', turn['assistant'])
                    predicted = float(found[-1].replace(',', '')) if found else None
                    gold = float(original['answer'].split('####')[-1].strip().replace(',', ''))
                    records.append({'model': tag, 'question': original['question'], 'gold': gold, 'pred': predicted,
                        'correct': predicted == gold, 'finish': turn['finish_reason'], 'reply': turn['assistant'],
                        'n_tokens': turn['n_tokens'], 'thinking_tokens': turn['thinking_tokens'],
                        'correct_completed': predicted == gold and turn['finish_reason'] == 'stop'})
                (OUT / f'gsm8k_{tag}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
        (OUT / f'{phase}_{label}.done').write_text(json.dumps({'model': tag, 'phase': phase, 'completed_epoch': time.time()}))
        log(f'COMPLETE {phase} {label}')
    finally:
        if server is not None:
            for sig in [signal.SIGTERM, signal.SIGKILL]:
                try:
                    os.killpg(server.pid, sig)
                except ProcessLookupError:
                    pass
                try:
                    server.wait(timeout=60)
                    break
                except subprocess.TimeoutExpired:
                    continue
        if merged.exists():
            shutil.rmtree(merged)


def fingerprint():
    model_files = sorted(set(Path(MODEL).glob('*.safetensors')) | {Path(MODEL) / 'config.json', Path(MODEL) / 'model.safetensors.index.json'})
    return {'model_files_sha256': {p.name: sha(p) for p in model_files},
            'revision': Path(MODEL).name, 'generator_sha256': sha(ROOT / 'scripts/eval/19_gen_replies.py'),
            'executor_sha256': sha(Path(__file__)),
            'vllm_version': subprocess.check_output(['/opt/vllm/bin/python', '-c', 'from importlib.metadata import version; print(version("vllm"))'], text=True).strip(),
            'inputs_sha256': {name: sha(OUT / name) for name in ['items.jsonl', 'panel.jsonl']},
            'thinking_budget': PLAN['thinking_budget'], 'primary_temperature': .7, 'top_p': 1.0,
            'seeds': [0, 1], 'primary_samples': 2, 'fixed_panel_temperature': 0,
            'max_tokens_policy': 'item.max_new_tokens+thinking_budget', 'dtype': 'float16',
            'model': PLAN['models']['A']['model']}


def verify_early_rows():
    tag = PLAN['models']['A']['model']
    files = [(OUT / 'items.jsonl', OUT / f'replies_{tag}.jsonl', .7, 2),
             (OUT / 'panel.jsonl', OUT / f'panel_samples_{tag}.jsonl', .7, 2),
             (OUT / 'panel.jsonl', OUT / f'panel_{tag}.jsonl', 0, 1)]
    digests = {}
    for source, output, temperature, samples in files:
        items = {r['id']: r for r in map(json.loads, source.read_text().splitlines())}
        records = [json.loads(line) for line in output.read_text().splitlines()]
        expected = {(item, sample) for item in items for sample in range(samples)}
        keys = [(r['item_id'], r['sample']) for r in records]
        assert len(keys) == len(expected) and set(keys) == expected
        trace = output.with_name(output.name + '.wire.jsonl')
        events = [json.loads(line) for line in trace.read_text().splitlines()]
        requests = {r['request_id']: r['body'] for r in events if r['event'] == 'request'}
        responses = {r['request_id']: r['body'] for r in events if r['event'] == 'response'}
        assert len(events) == 2 * len(requests) == 2 * len(responses)
        used = []
        for row in records:
            item = items[row['item_id']]
            assert row['model'] == row['base_model'] == tag and row['system'] == item['system']
            assert [t['user'] for t in row['turns']] == item['turns']
            assert row['gen'] == {'temperature': temperature, 'top_p': 1.0, 'seed': row['sample'],
                'enable_thinking': True, 'thinking_token_budget': PLAN['thinking_budget'],
                'regime': 'thinking-on-plus-extra-compute', 'history': 'visible final answers only'}
            messages = [{'role': 'system', 'content': item['system']}] if item['system'] else []
            for turn in row['turns']:
                messages.append({'role': 'user', 'content': turn['user']})
                assert requests[turn['request_id']] == {'model': tag, 'messages': messages,
                    'max_tokens': item['max_new_tokens'] + PLAN['thinking_budget'],
                    'temperature': temperature, 'top_p': 1.0, 'seed': row['sample'],
                    'chat_template_kwargs': {'enable_thinking': True},
                    'thinking_token_budget': PLAN['thinking_budget'], 'return_token_ids': True}
                response = responses[turn['request_id']]
                assert response['model'] == tag and (response['choices'][0]['message']['content'] or '') == turn['assistant']
                assert len(response['choices'][0]['token_ids']) == turn['total_completion_tokens']
                messages.append({'role': 'assistant', 'content': turn['assistant']})
                used.append(turn['request_id'])
        assert len(used) == len(set(used)) and set(used) == requests.keys()
        digests[output.name] = sha(output)
        digests[trace.name] = sha(trace)
    assert len(json.loads((OUT / 'smoke.json').read_text())) == 3
    digests['smoke.json'] = sha(OUT / 'smoke.json')
    digests['smoke.wire.jsonl'] = sha(OUT / 'smoke.wire.jsonl')
    return digests


def early_a():
    assert not (OUT / 'primary_A.done').exists()
    for name in ['items.jsonl', 'panel.jsonl']:
        assert sha(OUT / name) == PLAN['frozen_manifest']['input_sha256'][name]
    assert Path(MODEL).name == PLAN['frozen_manifest']['instruct_revision']
    assert sha(Path(MODEL) / 'config.json') == PLAN['frozen_manifest']['instruct_config_sha256']
    started = time.time()
    settings = fingerprint()
    log('EARLY A: native smoke and primary during adapter uploads; same frozen settings')
    cell('A', 'primary')
    receipt = {'author': 'PI/OpenAI (Sol)', 'early_during_uploads': True,
               'started_epoch': started, 'completed_epoch': time.time(),
               'settings': settings, 'verified_output_sha256': verify_early_rows()}
    (OUT / 'early_A.receipt.json').write_text(json.dumps(receipt, indent=2) + '\n')
    log('EARLY A VERIFIED COMPLETE,140frozen rows plus panels; full wire requests checked')


def accept_early_a():
    receipt = OUT / 'early_A.receipt.json'
    if not receipt.exists():
        return False
    try:
        saved = json.loads(receipt.read_text())
        assert saved['settings'] == fingerprint()
        assert saved['verified_output_sha256'] == verify_early_rows()
    except (AssertionError, KeyError, ValueError, FileNotFoundError) as error:
        log('EARLY A NOT ACCEPTED: ' + repr(error))
        return False
    log('EARLY A ACCEPTED: complete140frozen keys, exact model file hashes/settings/wire requests')
    return True


def main():
    (OUT / 'run.md').write_text('# Thinking-on frozen evaluation\n\nPI/OpenAI (Sol). Final-only judging happens locally. Raw full transport is in per-model `.wire.jsonl` files.\n\n')
    log('Resolved configuration:\n\n```json\n' + json.dumps({'argv': sys.argv, 'model': MODEL, 'deadline': DEADLINE, 'plan': PLAN}, indent=2) + '\n```')
    log('SHOULD: final assistant text and token counts exclude native parsed thinking; every raw response survives before parsing.\n\nTODO validate: D/H retain coherent character effects with thinking and extra compute; the existing off regime is not equal-compute matched.')
    manifest = PLAN['frozen_manifest']
    assert Path(MODEL).name == manifest['instruct_revision'] and sha(Path(MODEL) / 'config.json') == manifest['instruct_config_sha256']
    for name in ['items.jsonl', 'panel.jsonl', 'gsm8k_long60.jsonl', 'change.md']:
        assert sha(OUT / name) == manifest['input_sha256'][name]
    for name, source in PLAN['adapters'].items():
        for filename, expected in source['files'].items():
            assert sha(ROOT / ('outputs/up_' + name) / filename) == expected['sha256']
    gsm = [json.loads(line) for line in (OUT / 'gsm8k_long60.jsonl').read_text().splitlines()]
    (OUT / 'gsm_items.jsonl').write_text(''.join(json.dumps({'id': 'gsm60_' + str(i), 'system': None,
        'turns': [row['question'] + "\n\nThink step by step, then give the final answer on the last line as 'Answer: <number>'."],
        'max_new_tokens': 1500}) + '\n' for i, row in enumerate(gsm)))
    metadata = {'author': 'PI/OpenAI (Sol)', 'python': sys.version, 'tokenizer_path': MODEL,
                'tokenizer_files': {p.name: sha(p) for p in Path(MODEL).glob('*') if 'tokenizer' in p.name or p.name == 'chat_template.jinja'},
                'versions': subprocess.check_output(['/opt/vllm/bin/python', '-c', 'import vllm,transformers,torch; print(vllm.__version__,transformers.__version__,torch.__version__)'], text=True)}
    (OUT / 'engine_metadata.json').write_text(json.dumps(metadata, indent=2))
    if (OUT / 'early_A.launch.json').exists():
        while subprocess.run(['tmux', 'has-session', '-t', 'run13_early_A'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
            assert time.time() < DEADLINE - 1800, 'early A did not finish with time for later models'
            time.sleep(5)
    for label in ['A', 'D', 'H']:
        if label == 'A' and accept_early_a():
            continue
        if label == 'A' and (OUT / 'early_A.launch.json').exists():
            archive = OUT / 'early_A_not_accepted'
            archive.mkdir(exist_ok=False)
            tag = PLAN['models']['A']['model']
            for path in set(OUT.glob(f'*{tag}*')) | set(OUT.glob('smoke*')) | set(OUT.glob('early_A.receipt.json')) | set(OUT.glob('*primary_A*')):
                shutil.move(path, archive / path.name)
            log('Preserved unaccepted early A; generating primary A under main settings')
        cell(label, 'primary')
    for label in ['A', 'D', 'H']:
        if DEADLINE - time.time() < 1800:
            log('TIME LIMIT: later GSM and E not run')
            break
        cell(label, 'maths')
    if all((OUT / f'maths_{label}.done').exists() for label in ['A', 'D', 'H']) and DEADLINE - time.time() > 1800:
        cell('E', 'primary')
        if DEADLINE - time.time() > 1800:
            cell('E', 'maths')
    log('RUN13 GENERATION COMPLETE; judging/review local')


if __name__ == '__main__':
    if sys.argv[1:] == ['--early-A']:
        early_a()
    else:
        assert not sys.argv[1:]
        main()
