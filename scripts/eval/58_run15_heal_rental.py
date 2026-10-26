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
rental.OUT = OUT / 'lease_retry'
rental.STATE = ROOT / '.local/run15_heal_retry_rental.json'
rental.LABEL = 'cg-run15-thinking-heal-retry1'
PLAN = OUT / 'retry_plan.json'
GATE = OUT / 'preflight_retry_approved.json'
rental.SUBSETS = rental.DOCS = []
rental.EXPECTED_ADAPTERS_FILE = 'required_adapters.json'
rental.ADAPTER_DIR = Path.home() / '.local/share/cg_run15_heal_adapters'
HOURS, RATE = 6, 1.91
CODE = ['scripts/train/02_merge.py', 'scripts/train/17_merge_heal.py', 'scripts/train/box_watchdog.sh',
        'scripts/train/13_run10_evals.sh', 'scripts/train/check_loss_mask.py', 'scripts/train/spectral_plugin.py',
        'scripts/train/router_dtype_plugin.py', 'scripts/train/heal_plugin.py', 'scripts/train/spectral_math.py', 'scripts/train/heal_callback.py', 'scripts/train/41_expert_adapter_check.py',
        'scripts/eval/19_gen_replies.py', 'scripts/eval/57_run15_heal.py', 'configs/train/qwen3/sft.yml']
INPUTS = ['items.jsonl', 'panel.jsonl', 'gsm8k_long60.jsonl', 'change.md']
_ORIGINAL_RETRIEVE = rental.retrieve_outputs


def retrieve_with_checkpoints(ssh, host, state):
    code = "import hashlib,json; from pathlib import Path; p=Path('/workspace/cg/outputs'); print(json.dumps({str(f.relative_to(p)): hashlib.file_digest(f.open('rb'),'sha256').hexdigest() for f in p.glob('r10_*/checkpoint-*/adapter_*') if f.is_file()}))"
    result = subprocess.run(ssh + [host, 'python -c ' + shlex.quote(code)], check=True, capture_output=True, text=True,
                            timeout=min(300, max(1, state['hard_destroy_epoch'] - time.time() - 60)))
    hashes = json.loads(result.stdout)
    _ORIGINAL_RETRIEVE(ssh, host, state)
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
    data = json.loads((OUT / 'data/train/manifest.json').read_text())
    for name, info in data['variants'].items():
        assert sha(OUT / f'data/train/{name}.jsonl') == info['sha256']
    prep = json.loads((ROOT / 'slop/data/20261026_thinking_heal/summary.json').read_text())['conservative_accounted_usd']
    closure = json.loads((OUT / 'provider_closure_verified.json').read_text())
    assert closure['absent_confirmed'] and closure['instance_id'] == 57812278
    first_gpu = closure['estimated_gpu_usd']
    baseline = json.loads((OUT / 'lease/box_runs/baseline_receipt.json').read_text())
    assert baseline['plan_sha256'] == sha(OUT / 'plan.json')
    assert all(sha(OUT / 'lease/box_runs' / name) == digest for name, digest in baseline['verified_sha256'].items())
    plan = {'author': 'PI/OpenAI (Sol)', 'approval': 'const_v2 explicit one-replacement exception2026-10-26T13:50Z; original$20 all-in, no further lease',
            'adapters': adapters, 'D_cell': old['models']['D']['cell'], 'frozen_manifest': frozen, 'data_manifest': data,
            'thinking_budget': 4096, 'selected_item_ids': ['sys_payday_loan', 'task_agent', 'task_email'],
            'max_hours': HOURS, 'max_rate': RATE, 'disk_gb': 400, 'prep_api_accounted_usd': prep,
            'first_lease_gpu_usd': first_gpu,
            'judge_reserve_usd': 1.5, 'review_reserve_usd': .5, 'traffic_reserve_usd': 1.6,
            'termination_margin_usd': 1, 'total_reserve_usd': HOURS * RATE + prep + first_gpu + 4.6,
            'baseline_reuse': {'source_lease': 57812278, 'plan_sha256': baseline['plan_sha256'],
                'executor_sha256': baseline['executor_sha256'],
                'generator_sha256': json.loads((OUT / 'lease/executed_source_sha256.json').read_text())['scripts/eval/19_gen_replies.py'],
                'source_receipt_sha256': sha(OUT / 'lease/box_runs/baseline_receipt.json'),
                'verified_sha256': baseline['verified_sha256']},
            'timing_policy': 'Traces first; mixed only if measured remaining time fits; never discard a completed trace heal.',
            'transport': 'All4 donors via owner-approved readonly cloud relay; original pinned SHA256, source before/after SHA, new receiver SHA/mtime and atomic install. No local donor bytes consumed.',
            'training': 'Frozen bf16-rounded training copy of ordered-fp16 D; rank8/alpha16 all existing dense/expert targets; LR1e-4, spectral_frac.01, oneepoch, quarter checkpoints; no KL. Matched total assistant tokens, half traces+half replay in mixed.',
            'precision': 'Train a frozen bf16-rounded copy of ordered-fp16 D; LoRA fp32 and spectral math FP32 outside autocast. Original D remains fp16 for all serving. Heal adapters are therefore trained against D_bf16, served against D_fp16. Native expert-LoRA or approved fp32-accumulated fp16 merge.',
            'evaluation': 'Instruct reused from first lease at exact recorded serving protocol; D and final trace/mix generated on replacement. All: full frozen70x2 + GSM60 + fixedT0panel in both modes. Early quarter checkpoints: selected3x2 plus T0panel in both modes; not full-scope scores.',
            'recovery': 'One authorized replacement only. Snapshot/retrieve logs and adapters; stop on failed retrieval. Independent exact-ID destruction deadline. First-lease files retained unchanged.',
            'timing': 'Measure20steps; project both variants with1.5time margin and reserve3h evaluation before runnerdeadline. Runnerends45min before providerdestroy.'}
    assert plan['total_reserve_usd'] <= 20
    PLAN.write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps({k: v for k, v in plan.items() if k not in ['adapters', 'frozen_manifest', 'data_manifest']}, indent=2))


def run():
    plan = json.loads(PLAN.read_text())
    assert not rental.STATE.exists() and plan['total_reserve_usd'] <= 20
    gate = json.loads(GATE.read_text())
    assert gate['plan_sha256'] == sha(PLAN)
    assert gate['source_sha256'] == {p: sha(ROOT / p) for p in CODE + ['scripts/eval/58_run15_heal_rental.py', 'scripts/eval/48_vast_deadline.py', 'scripts/eval/38_run10_chat_rental.py']}
    assert gate['cpu_real_pipeline_pass'] and gate['independent_review_path']
    query = json.loads((OUT / 'offers.json').read_text())['query']
    offers = rental.api('/bundles/?q=' + urllib.parse.quote(json.dumps(query)))['offers']
    passing = [o for o in offers if o['hosting_type'] == 1 and o['gpu_name'] == 'RTX PRO 6000 S' and o['cuda_max_good'] >= 13
               and o['inet_down_cost'] <= .005 and o['inet_up_cost'] <= .005 and o['dph_total'] <= RATE]
    assert passing, 'No passing offer within cap; no lease created'
    offer = min(passing, key=lambda x: x['dph_total'])
    traffic = max(.8, 120 * offer['inet_down_cost'] + 25 * offer['inet_up_cost'])
    traffic += .8
    total = HOURS * offer['dph_total'] + plan['prep_api_accounted_usd'] + plan['first_lease_gpu_usd'] + 3 + traffic
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
            archive.add(PLAN, arcname='runs/run10/plan.json')
            archive.add(OUT / 'plan.json', arcname='runs/run10/baseline_original_plan.json')
            previous = OUT / 'lease/box_runs'
            for name in plan['baseline_reuse']['verified_sha256']:
                archive.add(previous / name, arcname='runs/run10/' + name)
            for name in ['baseline_receipt.json', 'native_parser_smoke.json', 'native_parser_smoke.wire.jsonl',
                         'server_r15_instruct.argv.json', 'server_r15_instruct.log']:
                archive.add(previous / name, arcname='runs/run10/' + name)
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
            print('SETUP COMPLETE; exact-protocol first-lease Instruct baseline supplied for verified reuse', flush=True)
        future = pool.submit(setup)
        print('RUN15 RELAY TARGET READY ' + json.dumps(state), flush=True)
        relay = OUT / 'relay_retry_complete.json'
        while not relay.exists():
            assert time.time() < min(started + 3600, state['runner_deadline_epoch'] - 4 * 3600), 'Cloud relay did not arrive within its setup reserve'
            if future.done():
                future.result()
            beat.result() if beat.done() else None
            time.sleep(5)
        assert json.loads(relay.read_text())['instance_id'] == state['instance_id']
        for name, source in plan['adapters'].items():
            target = '/workspace/cg/outputs/up_' + name
            expected = {target + '/' + filename: v['sha256'] for filename, v in source['files'].items()}
            verify = 'import hashlib; files=' + repr(expected) + "; assert all(hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()==s for p,s in files.items())"
            remote('python -c ' + shlex.quote(verify), timeout=300)
            print('REMOTE ADAPTER VERIFIED ' + name, flush=True)
        future.result()
        command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN15_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/57_run15_heal.py'
        script = f'set +e; {command} > runs/run10/job.log 2>&1; status=$?; echo $status > runs/run10/job.exit; exit $status'
        remote('cd /workspace/cg && tmux new-session -d -s run10_train ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
        repair_until = None
        for repair_index in range(3):
            try:
                rental.monitor(remote, lambda: max(1, state['runner_deadline_epoch'] - time.time()), stop, beat)
                break
            except AssertionError as error:
                if not str(error).startswith('remote comparison exited') or repair_index == 2:
                    raise
                resume = OUT / 'repair_retry_resume.json'
                assert not resume.exists(), 'Stale repair receipt'
                if repair_until is None:
                    repair_until = min(time.time() + 1200, state['runner_deadline_epoch'] - 1800)
                until = repair_until
                request = {'instance_id': state['instance_id'], 'repair_index': repair_index,
                           'error': str(error), 'repair_until_epoch': until, 'hard_destroy_epoch': state['hard_destroy_epoch']}
                (rental.OUT / f'repair_request_{repair_index}.json').write_text(json.dumps(request, indent=2))
                print('RUN15 REPAIR REQUIRED ' + json.dumps(request), flush=True)
                while time.time() < until and not resume.exists():
                    stop.wait(5)
                if not resume.exists():
                    raise
                receipt = json.loads(resume.read_text())
                assert receipt['instance_id'] == state['instance_id'] and receipt['repair_index'] == repair_index
                assert receipt['remote_job_restarted'] and receipt['patched_source_sha256']
                resume.rename(rental.OUT / f'repair_resume_{repair_index}.json')
    finally:
        try:
            if ssh is not None:
                rental.retrieve_or_stop(ssh, host, state)
            else:
                rental.destroy()
            assert all(r['id'] != state['instance_id'] for r in rental.api('/instances/')['instances'])
            after = rental.api('/users/current/')
            (OUT / 'provider_closure_retry_verified.json').write_text(json.dumps({'instance_id': state['instance_id'], 'absent_confirmed': True,
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
