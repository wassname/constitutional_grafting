"""One finite, exact-ID-guarded thinking-on evaluation lease; no training. -- PI/OpenAI (Sol)"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import io
import json
import os
import shlex
import subprocess
import sys
import tarfile
import threading
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'slop/eval/run13_thinking'
SPEC = importlib.util.spec_from_file_location('rental', ROOT / 'scripts/eval/38_run10_chat_rental.py')
rental = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rental)
rental.OUT = OUT / 'lease'
rental.STATE = ROOT / '.local/run13_thinking_rental.json'
rental.LABEL = 'cg-run13-thinking'
rental.SUBSETS = rental.DOCS = []
rental.EXPECTED_ADAPTERS_FILE = ''
rental.ADAPTER_DIR = ROOT / '.local/run13_no_trained_adapters'
HOURS = 5
MAX_RATE = 1.845


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    frozen = json.loads((ROOT / 'slop/eval/run8/manifest.json').read_text())
    for name in ['items.jsonl', 'panel.jsonl', 'gsm8k_long60.jsonl', 'change.md']:
        assert sha(ROOT / 'slop/eval/run8' / name) == frozen['input_sha256'][name]
    source = {}
    stage1 = json.loads((ROOT / 'slop/eval/run10/stage1/retrieval_verified.json').read_text())['manifest']
    stage7 = json.loads((ROOT / 'slop/eval/run10/stage7/retrieval_verified.json').read_text())['manifest']
    specs = [
        ('stoic', Path.home() / '.local/share/cg_run10_adapters/r10_stoic', stage1['r10_stoic']),
        ('other', Path.home() / '.local/share/cg_run10_adapters/r10_other', stage1['r10_other']),
        ('rewr', Path.home() / '.local/share/cg_run10_adapters/r10_cx_chatr12', stage7['r10_cx_chatr12']),
    ]
    for name, directory, tag in [('mix', 'cg_run12_mix_adapters', 'r10_x12_chatmix'), ('gen', 'cg_run12_gen_adapters', 'r10_x12_chatgen')]:
        receipt = ROOT / f'slop/eval/run12/run12{name}/retrieval_verified.json'
        data = json.loads(receipt.read_text())
        assert data['job_exit'] == '0' and data['all_available_final_adapter_hashes_match']
        specs.append((name, Path.home() / '.local/share' / directory / tag, data['manifest'][tag]))
    const = rental.DONOR_SRC['const']
    specs.append(('const', const[0], {name: {'sha256': digest} for name, digest in const[1].items()}))
    for name, directory, expected in specs:
        source[name] = {'path': str(directory), 'files': {}}
        for filename in ['adapter_config.json', 'adapter_model.safetensors']:
            path = directory / filename
            actual = sha(path)
            assert actual == expected[filename]['sha256'], path
            source[name]['files'][filename] = {'sha256': actual, 'bytes': path.stat().st_size}
        print('LOCAL ADAPTER VERIFIED ' + name, flush=True)
    docs = [('stoic', .5), ('const', 1), ('other', 1)]
    prefix = 'r10_stoic0.5_const1_other1'
    models = {'A': {'model': 'r8_a0_b0', 'cell': []},
              'D': {'model': prefix + '_cx_chatr121', 'cell': docs + [('rewr', 1)]},
              'H': {'model': prefix + '_x12_chatmix0.5_x12_chatgen-0.5', 'cell': docs + [('mix', .5), ('gen', -.5)]},
              'E': {'model': prefix + '_x12_chatmix0.5', 'cell': docs + [('mix', .5)]}}
    for label, stage in [('D', 'slop/eval/run10/stage7'), ('H', 'slop/eval/run12/run12gen'), ('E', 'slop/eval/run12/run12gen')]:
        path = ROOT / stage / 'box_runs' / f"merge_{models[label]['model']}.json"
        previous = json.loads(path.read_text())
        assert previous['dtype'] == 'float16' and previous['groups'] == {}
        assert [(row['adapter_sha256'], row['scale']) for row in previous['adapters']] == [
            (source[name]['files']['adapter_model.safetensors']['sha256'], scale) for name, scale in models[label]['cell']]
        models[label]['previous_merge_receipt'] = str(path.relative_to(ROOT))
        models[label]['previous_merge_receipt_sha256'] = sha(path)
    for label, model in models.items():
        stage = 'slop/eval/run10/stage7/judging/cells' if label == 'D' else 'slop/eval/run12/run12gen/judging/initial'
        path = ROOT / stage / 'replies.jsonl'
        old = [json.loads(line) for line in path.read_text().splitlines() if json.loads(line)['model'] == model['model']]
        assert len(old) == 140 and len({(r['item_id'], r['sample']) for r in old}) == 140
        model['thinking_off_source'] = str(path.relative_to(ROOT))
        model['thinking_off_source_sha256'] = sha(path)
    review_path = OUT / 'review_usage.json'
    review_cost = json.loads(review_path.read_text())['costUsd'] if review_path.exists() else 0
    plan = {'author': 'PI/OpenAI (Sol)', 'approved_by': 'const_v2 2026-10-26, run13, total cap $15',
            'models': models, 'adapters': source, 'thinking_budget': 4096, 'frozen_manifest': frozen,
            'max_hours': HOURS, 'max_hourly_rate': MAX_RATE, 'gpu_ceiling_usd': HOURS * MAX_RATE,
            'traffic_reserve_usd': .6, 'judge_reserve_usd': 1, 'termination_margin_usd': 1,
            'independent_review_reported_usd': review_cost,
            'total_reserve_usd': HOURS * MAX_RATE + 2.6 + review_cost,
            'priority': 'A/D/H frozen70 plus panel, then GSM60, then E if time remains',
            'regime': 'Native thinking cap4096; total=max original answer cap+4096; unused thinking allowance may extend final; final-only own history; no rescue or retries.',
            'recovery': 'On retrieval failure stop exact instance; disk retained only until existing absolute destruction deadline.'}
    assert plan['total_reserve_usd'] <= 15
    (OUT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    return plan


def run():
    plan = json.loads((OUT / 'plan.json').read_text())
    assert plan['total_reserve_usd'] <= 15 and not rental.STATE.exists()
    rental.OUT.mkdir(exist_ok=True)
    q = json.loads((OUT / 'offers.json').read_text())['query']
    offers = rental.api('/bundles/?q=' + urllib.parse.quote(json.dumps(q)))['offers']
    passing = [o for o in offers if o['gpu_name'] == 'RTX PRO 6000 S' and o['inet_down_cost'] <= .005 and o['inet_up_cost'] <= .005 and o['cuda_max_good'] >= 13 and o['dph_total'] <= MAX_RATE]
    assert passing, 'no qualified offer in approved cap; no lease created'
    offer = min(passing, key=lambda row: row['dph_total'])
    (OUT / 'current_offers.json').write_text(json.dumps({'query': q, 'offers': offers, 'selected': offer}, indent=2) + '\n')
    account = rental.api('/users/current/')
    assert account['credit'] >= plan['total_reserve_usd'] + 1
    assert not [r for r in rental.api('/instances/')['instances'] if r['label'] == rental.LABEL]
    (rental.OUT / 'rental_quote.json').write_text(json.dumps({'offer': offer, 'maximum_hours': HOURS,
        'rental_plus_bandwidth_reserve_usd': HOURS * offer['dph_total'] + .6, 'total_including_judge_review_and_margin': HOURS * offer['dph_total'] + 2.6 + plan['independent_review_reported_usd']}, indent=2))
    started = time.time()
    created = rental.api(f"/asks/{offer['id']}/", 'PUT', {'client_id': 'me', 'image': rental.IMAGE, 'disk': 300,
        'label': rental.LABEL, 'runtype': 'ssh_direct', 'cancel_unavail': True})
    assert created['success'], created
    state = {'instance_id': created['new_contract'], 'created_epoch': started, 'hard_destroy_epoch': started + HOURS * 3600,
             'runner_deadline_epoch': started + HOURS * 3600 - 1800, 'hourly_rate': offer['dph_total'], 'image': rental.IMAGE}
    try:
        rental.STATE.write_text(json.dumps(state, indent=2)); rental.STATE.chmod(0o600)
        (rental.OUT / 'lease.json').write_text(json.dumps(state, indent=2))
        rental.claim_instance_owner(state['instance_id'])
    except BaseException:
        result = rental.api(f"/instances/{state['instance_id']}/", 'DELETE', {})
        assert result['success'] and all(r['id'] != state['instance_id'] for r in rental.api('/instances/')['instances'])
        raise
    ssh = host = None
    stop = threading.Event()
    pool = None

    def remote(command, timeout=600, **kwargs):
        left = state['hard_destroy_epoch'] - time.time() - 120
        assert left > 0
        return subprocess.run(ssh + [host, command], check=True, timeout=min(timeout, left), **kwargs)

    def heartbeat():
        while not stop.wait(60):
            try:
                remote('touch /workspace/heartbeat', timeout=15, stdout=subprocess.DEVNULL)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
                print('HEARTBEAT TRANSPORT ' + repr(error), flush=True)

    try:
        subprocess.run([sys.executable, str(ROOT / 'scripts/eval/48_vast_deadline.py'), 'arm', '--state', str(rental.STATE),
                        '--out', str(rental.OUT), '--label', rental.LABEL], check=True)
        ready_by = started + 1800
        while time.time() < ready_by:
            inst = next(row for row in rental.api('/instances/')['instances'] if row['id'] == state['instance_id'])
            if inst['actual_status'] == 'running':
                ports = inst.get('ports') or {}
                if ports.get('22/tcp'):
                    state.update(ssh_host=inst['public_ipaddr'], ssh_port=ports['22/tcp'][0]['HostPort'])
                elif inst.get('ssh_host') and inst.get('ssh_port'):
                    state.update(ssh_host=inst['ssh_host'], ssh_port=inst['ssh_port'])
                if 'ssh_host' in state:
                    ssh, host = rental.saved_connection(state)
                    if subprocess.run(ssh + [host, 'true'], timeout=15).returncode == 0:
                        break
            time.sleep(30)
        else:
            raise TimeoutError('SSH startup exceeded30minutes')
        rental.STATE.write_text(json.dumps(state, indent=2))
        (rental.OUT / 'lease.json').write_text(json.dumps(state, indent=2))
        remote("set -euo pipefail; nvidia-smi; python -c 'import torch; print(torch.__version__,torch.version.cuda); assert torch.cuda.get_device_properties(0).total_memory>90*1024**3'; dd if=/dev/zero of=/workspace/diskcheck bs=1G count=10 oflag=direct; rm /workspace/diskcheck", timeout=180)
        remote('command -v tmux && command -v rsync || (apt-get update -qq && apt-get install -y -qq tmux rsync)', timeout=180)
        code = ['scripts/train/02_merge.py', 'scripts/train/box_watchdog.sh', 'scripts/train/13_run10_evals.sh',
                'scripts/eval/19_gen_replies.py', 'scripts/eval/54_run13_thinking_box.py']
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            for name in code:
                archive.add(ROOT / name, arcname=name)
            for name in ['items.jsonl', 'panel.jsonl', 'gsm8k_long60.jsonl', 'change.md', 'manifest.json']:
                archive.add(ROOT / 'slop/eval/run8' / name, arcname='runs/run10/' + ('run8_manifest.json' if name == 'manifest.json' else name))
            archive.add(OUT / 'plan.json', arcname='runs/run10/plan.json')
        (rental.OUT / 'executed_source_sha256.json').write_text(json.dumps({p: sha(ROOT / p) for p in code}, indent=2))
        remote('mkdir -p /workspace/cg/runs/run10; tar -xzf - -C /workspace/cg', input=stream.getvalue(), timeout=60)
        remote("touch /workspace/heartbeat; tmux new-session -d -s run10_watchdog 'cd /workspace/cg && MAX_SILENT_H=1 bash scripts/train/box_watchdog.sh > runs/run10/watchdog.log 2>&1'")
        remote("for i in $(seq 1 50); do if grep -q 'auth check GET: 200' /workspace/cg/runs/run10/watchdog.log; then cat /workspace/cg/runs/run10/watchdog.log; exit 0; fi; sleep .2; done; exit 1", timeout=20)
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        beat = pool.submit(heartbeat)
        def setup():
            with (rental.OUT / 'setup.log').open('w') as log:
                remote('cd /workspace/cg && bash scripts/train/13_run10_evals.sh prep', timeout=5400, stdout=log, stderr=subprocess.STDOUT)
            print('SETUP COMPLETE pinned Instruct+vLLM0.31', flush=True)
        setup_future = pool.submit(setup)
        for name, source in plan['adapters'].items():
            if setup_future.done():
                setup_future.result()
            target = '/workspace/cg/outputs/up_' + name
            remote('mkdir -p ' + target, timeout=30)
            with (rental.OUT / f'upload_{name}.log').open('w') as log:
                subprocess.run(['rsync', '-az', '--partial', '-e', shlex.join(ssh),
                    source['path'] + '/adapter_config.json', source['path'] + '/adapter_model.safetensors', host + ':' + target + '/'],
                    check=True, stdout=log, stderr=subprocess.STDOUT, timeout=max(1, state['runner_deadline_epoch'] - time.time() - 1800))
            expected = {target + '/' + filename: v['sha256'] for filename, v in source['files'].items()}
            verify = 'import hashlib; files=' + repr(expected) + "; assert all(hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()==s for p,s in files.items())"
            remote('python -c ' + shlex.quote(verify), timeout=300)
            print('REMOTE ADAPTER VERIFIED ' + name, flush=True)
        setup_future.result()
        command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN13_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/54_run13_thinking_box.py'
        script = f'set +e; {command} > runs/run10/job.log 2>&1; status=$?; echo $status > runs/run10/job.exit; exit $status'
        remote('cd /workspace/cg && tmux new-session -d -s run10_train ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
        rental.monitor(remote, lambda: max(1, state['runner_deadline_epoch'] - time.time()), stop, beat)
    finally:
        try:
            if ssh is not None:
                rental.retrieve_or_stop(ssh, host, state)
            else:
                rental.destroy()
            live = rental.api('/instances/')['instances']
            assert all(row['id'] != state['instance_id'] for row in live)
            after = rental.api('/users/current/')
            (OUT / 'provider_closure_verified.json').write_text(json.dumps({'instance_id': state['instance_id'], 'absent_confirmed': True,
                'elapsed_hours': (time.time() - started) / 3600, 'estimated_gpu_usd': (time.time() - started) / 3600 * state['hourly_rate'],
                'credit_before': account['credit'], 'credit_after': after['credit'],
                'credit_difference_not_reconciled_invoice': account['credit'] - after['credit']}, indent=2))
        finally:
            stop.set()
            if pool:
                pool.shutdown(wait=True)
    print('RUN13 RETRIEVED; exact instance destroyed', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run'])
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    else:
        with rental.controller_owner():
            run()
