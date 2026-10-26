"""Own one finite run15 heal lease, including exact-ID deadline and retrieval. -- PI/OpenAI (Sol)"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import shlex
import subprocess
import sys
import tarfile
import threading
import time
import urllib.parse

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'slop/eval/run15_heal'
SPEC = importlib.util.spec_from_file_location('rental', ROOT / 'scripts/eval/38_run10_chat_rental.py')
rental = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rental)
rental.OUT = OUT / 'lease'
rental.STATE = ROOT / '.local/run15_heal_rental.json'
rental.LABEL = 'cg-run15-thinking-heal'
rental.SUBSETS = rental.DOCS = []
rental.EXPECTED_ADAPTERS_FILE = 'required_adapters.json'
rental.ADAPTER_DIR = Path.home() / '.local/share/cg_run15_heal_adapters'
HOURS, RATE = 6, 1.99
CODE = ['scripts/train/02_merge.py', 'scripts/train/17_merge_heal.py', 'scripts/train/box_watchdog.sh',
        'scripts/train/13_run10_evals.sh', 'scripts/train/check_loss_mask.py', 'scripts/train/spectral_plugin.py',
        'scripts/train/router_dtype_plugin.py', 'scripts/train/heal_plugin.py', 'scripts/train/41_expert_adapter_check.py',
        'scripts/eval/19_gen_replies.py', 'scripts/eval/57_run15_heal.py', 'configs/train/qwen3/sft.yml']
INPUTS = ['items.jsonl', 'panel.jsonl', 'gsm8k_long60.jsonl', 'change.md']
_ORIGINAL_RETRIEVE = rental.retrieve_outputs


def retrieve_with_checkpoints(ssh, host, state):
    _ORIGINAL_RETRIEVE(ssh, host, state)
    code = "import hashlib,json; from pathlib import Path; p=Path('/workspace/cg/outputs'); print(json.dumps({str(f.relative_to(p)): hashlib.file_digest(f.open('rb'),'sha256').hexdigest() for f in p.glob('r10_*/checkpoint-*/adapter_*') if f.is_file()}))"
    result = subprocess.run(ssh + [host, 'python -c ' + shlex.quote(code)], check=True, capture_output=True, text=True,
                            timeout=min(300, max(1, state['hard_destroy_epoch'] - time.time() - 60)))
    hashes = json.loads(result.stdout)
    assert all(sha(rental.ADAPTER_DIR / name) == digest for name, digest in hashes.items())
    (rental.OUT / 'checkpoint_hashes_verified.json').write_text(json.dumps(hashes, indent=2) + '\n')


rental.retrieve_outputs = retrieve_with_checkpoints


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare():
    old = json.loads((ROOT / 'slop/eval/run13_thinking/plan.json').read_text())
    frozen = old['frozen_manifest']
    for name in INPUTS:
        assert sha(ROOT / 'slop/eval/run8' / name) == frozen['input_sha256'][name]
    adapters = {name: old['adapters'][name] for name in ['stoic', 'const', 'other', 'rewr']}
    for name, source in adapters.items():
        for filename, info in source['files'].items():
            assert sha(Path(source['path']) / filename) == info['sha256']
    data = json.loads((OUT / 'data/train/manifest.json').read_text())
    for name, info in data['variants'].items():
        assert sha(OUT / f'data/train/{name}.jsonl') == info['sha256']
    prep = json.loads((ROOT / 'slop/data/20261026_thinking_heal/summary.json').read_text())['conservative_accounted_usd']
    plan = {'author': 'PI/OpenAI (Sol)', 'approval': 'wassname via const_v2,2026-10-26; goal2 ad3e95-v12, cap$20 all-in',
            'adapters': adapters, 'D_cell': old['models']['D']['cell'], 'frozen_manifest': frozen, 'data_manifest': data,
            'thinking_budget': 4096, 'selected_item_ids': ['sys_payday_loan', 'task_agent', 'task_email'],
            'max_hours': HOURS, 'max_rate': RATE, 'disk_gb': 400, 'prep_api_accounted_usd': prep,
            'judge_reserve_usd': 4, 'review_reserve_usd': 1, 'traffic_reserve_usd': .8,
            'termination_margin_usd': 1, 'total_reserve_usd': HOURS * RATE + prep + 6.8,
            'training': 'Frozen ordered-fp16 D; rank8/alpha16 all existing dense/expert targets; LR1e-4, spectral_frac.01, oneepoch, quarter checkpoints; no KL. Matched total assistant tokens, half traces+half replay in mixed.',
            'precision': 'Train frozen D weights fp16, trainable LoRA fp32. Native unmerged expert-LoRA vLLM if supported; otherwise explicit fp32 update+accumulation rounded once to fp16, same parent.',
            'evaluation': 'Fresh Instruct and D, final trace/mix: full frozen70x2 + GSM60 + fixedT0panel in both modes. Early quarter checkpoints: selected3x2 plus T0panel in both modes; not full-scope scores.',
            'recovery': 'Snapshot/retrieve logs and all adapters; stop if retrieval fails, exact-ID independent destruction deadline remains. No replacement lease.',
            'timing': 'Measure20steps; project both variants with1.5time margin and reserve3h evaluation before runnerdeadline. Runnerends45min before providerdestroy.'}
    assert plan['total_reserve_usd'] <= 20
    (OUT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({k: v for k, v in plan.items() if k not in ['adapters', 'frozen_manifest', 'data_manifest']}, indent=2))


def run():
    plan = json.loads((OUT / 'plan.json').read_text())
    assert not rental.STATE.exists() and plan['total_reserve_usd'] <= 20
    gate = json.loads((OUT / 'preflight_approved.json').read_text())
    assert gate['plan_sha256'] == sha(OUT / 'plan.json')
    assert gate['source_sha256'] == {p: sha(ROOT / p) for p in CODE + ['scripts/eval/58_run15_heal_rental.py', 'scripts/eval/48_vast_deadline.py', 'scripts/eval/38_run10_chat_rental.py']}
    assert gate['cpu_real_pipeline_pass'] and gate['independent_review_path']
    query = json.loads((OUT / 'offers.json').read_text())['query']
    offers = rental.api('/bundles/?q=' + urllib.parse.quote(json.dumps(query)))['offers']
    passing = [o for o in offers if o['hosting_type'] == 1 and o['gpu_name'] == 'RTX PRO 6000 S' and o['cuda_max_good'] >= 13
               and o['inet_down_cost'] <= .005 and o['inet_up_cost'] <= .005 and o['dph_total'] <= RATE]
    assert passing, 'No passing offer within cap; no lease created'
    offer = min(passing, key=lambda x: x['dph_total'])
    traffic = max(.8, 120 * offer['inet_down_cost'] + 25 * offer['inet_up_cost'])
    total = HOURS * offer['dph_total'] + plan['prep_api_accounted_usd'] + 6 + traffic
    assert total <= 20
    account = rental.api('/users/current/')
    autobill = account['autobill_amount'] if account['has_billing'] and not account['billing_failed'] and account['autobill_threshold'] > 0 else 0
    assert account['credit'] + autobill >= HOURS * offer['dph_total'] + traffic + 2
    assert not [r for r in rental.api('/instances/')['instances'] if r['label'] == rental.LABEL]
    rental.OUT.mkdir(exist_ok=True)
    (rental.OUT / 'rental_quote.json').write_text(json.dumps({'offer': offer, 'max_hours': HOURS, 'total_reserve_usd': total,
        'traffic_reserve_usd': traffic, 'account_credit': account['credit'], 'auto_billing_amount': autobill}, indent=2))
    started = time.time()
    created = rental.api(f"/asks/{offer['id']}/", 'PUT', {'client_id': 'me', 'image': rental.IMAGE, 'disk': 400,
        'label': rental.LABEL, 'runtype': 'ssh_direct', 'cancel_unavail': True})
    assert created['success'], created
    state = {'instance_id': created['new_contract'], 'created_epoch': started, 'hard_destroy_epoch': started + HOURS * 3600,
             'runner_deadline_epoch': started + HOURS * 3600 - 2700, 'hourly_rate': offer['dph_total'], 'image': rental.IMAGE}
    try:
        rental.STATE.write_text(json.dumps(state, indent=2)); rental.STATE.chmod(0o600)
        (rental.OUT / 'lease.json').write_text(json.dumps(state, indent=2))
        rental.claim_instance_owner(state['instance_id'])
    except BaseException:
        result = rental.api(f"/instances/{state['instance_id']}/", 'DELETE', {})
        assert result['success']
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
            inst = next(r for r in rental.api('/instances/')['instances'] if r['id'] == state['instance_id'])
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
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode='w:gz') as archive:
            for name in CODE:
                archive.add(ROOT / name, arcname=name)
            for name in INPUTS + ['manifest.json']:
                archive.add(ROOT / 'slop/eval/run8' / name, arcname='runs/run10/' + ('run8_manifest.json' if name == 'manifest.json' else name))
            archive.add(OUT / 'plan.json', arcname='runs/run10/plan.json')
            for variant in ['trace', 'mix']:
                archive.add(OUT / f'data/train/{variant}.jsonl', arcname=f'data/train/run15/{variant}.jsonl')
        (rental.OUT / 'executed_source_sha256.json').write_text(json.dumps({p: sha(ROOT / p) for p in CODE}, indent=2))
        remote('mkdir -p /workspace/cg/runs/run10; tar -xzf - -C /workspace/cg', input=stream.getvalue(), timeout=90)
        remote("touch /workspace/heartbeat; tmux new-session -d -s run10_watchdog 'cd /workspace/cg && MAX_SILENT_H=1 bash scripts/train/box_watchdog.sh > runs/run10/watchdog.log 2>&1'")
        remote("for i in $(seq 1 50); do if grep -q 'auth check GET: 200' /workspace/cg/runs/run10/watchdog.log; then cat /workspace/cg/runs/run10/watchdog.log; exit 0; fi; sleep .2; done; exit 1", timeout=20)
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        beat = pool.submit(heartbeat)
        def setup():
            with (rental.OUT / 'setup.log').open('w') as stream:
                remote('cd /workspace/cg && bash scripts/train/13_run10_evals.sh prep', timeout=5400, stdout=stream, stderr=subprocess.STDOUT)
            command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN15_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/57_run15_heal.py --early-baseline'
            script = f'set +e; {command} > runs/run10/early_baseline.log 2>&1; status=$?; echo $status > runs/run10/early_baseline.exit; exit $status'
            remote('touch /workspace/cg/runs/run10/early_baseline.launch; tmux new-session -d -s run15_early_baseline ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
            print('SETUP COMPLETE; BOTH-MODE INSTRUCT BASELINE started during adapter uploads', flush=True)
        future = pool.submit(setup)
        for name, source in plan['adapters'].items():
            if future.done():
                future.result()
            target = '/workspace/cg/outputs/up_' + name
            remote('mkdir -p ' + target, timeout=30)
            with (rental.OUT / f'upload_{name}.log').open('w') as stream:
                subprocess.run(['rsync', '-az', '--partial', '-e', shlex.join(ssh),
                    source['path'] + '/adapter_config.json', source['path'] + '/adapter_model.safetensors', host + ':' + target + '/'],
                    check=True, stdout=stream, stderr=subprocess.STDOUT, timeout=max(1, state['runner_deadline_epoch'] - time.time() - 3600))
            expected = {target + '/' + filename: v['sha256'] for filename, v in source['files'].items()}
            verify = 'import hashlib; files=' + repr(expected) + "; assert all(hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()==s for p,s in files.items())"
            remote('python -c ' + shlex.quote(verify), timeout=300)
            print('REMOTE ADAPTER VERIFIED ' + name, flush=True)
        future.result()
        command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN15_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/57_run15_heal.py'
        script = f'set +e; {command} > runs/run10/job.log 2>&1; status=$?; echo $status > runs/run10/job.exit; exit $status'
        remote('cd /workspace/cg && tmux new-session -d -s run10_train ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
        rental.monitor(remote, lambda: max(1, state['runner_deadline_epoch'] - time.time()), stop, beat)
    finally:
        try:
            if ssh is not None:
                rental.retrieve_or_stop(ssh, host, state)
            else:
                rental.destroy()
            assert all(r['id'] != state['instance_id'] for r in rental.api('/instances/')['instances'])
            after = rental.api('/users/current/')
            (OUT / 'provider_closure_verified.json').write_text(json.dumps({'instance_id': state['instance_id'], 'absent_confirmed': True,
                'elapsed_hours': (time.time() - started) / 3600, 'estimated_gpu_usd': (time.time() - started) / 3600 * state['hourly_rate'],
                'credit_before': account['credit'], 'credit_after': after['credit'],
                'credit_difference_not_reconciled_invoice': account['credit'] - after['credit']}, indent=2))
        finally:
            stop.set()
            if pool:
                pool.shutdown(wait=True)
    print('RUN15 RETRIEVED; exact instance destroyed', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'run', 'snapshot', 'attach'])
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    elif args.action == 'snapshot':
        state = json.loads(rental.STATE.read_text()); ssh, host = rental.saved_connection(state)
        rental.retrieve_outputs(ssh, host, state)
    else:
        with rental.controller_owner():
            run() if args.action == 'run' else rental.attach()
