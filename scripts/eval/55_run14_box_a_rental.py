"""One exact-ID-guarded run14 lease; $35 combined cap, no public push. -- PI/OpenAI (Sol)"""
import argparse
import concurrent.futures
import hashlib
import importlib.util
import io
import json
import shlex
import subprocess
import sys
import tarfile
import threading
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'slop/eval/run14_box_a'
SPEC = importlib.util.spec_from_file_location('rental', ROOT / 'scripts/eval/38_run10_chat_rental.py')
rental = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rental)
rental.OUT = OUT / 'lease'
rental.STATE = ROOT / '.local/run14_box_a_rental.json'
rental.LABEL = 'cg-run14-box-a'
rental.SUBSETS = rental.DOCS = []
rental.EXPECTED_ADAPTERS_FILE = 'required_adapters.json'
rental.ADAPTER_DIR = ROOT / '.local/adapters/cg_run14_adapters'
HOURS, RATE = 14, 1.92
LOCAL_CODE = ['scripts/eval/38_run10_chat_rental.py', 'scripts/eval/48_vast_deadline.py']
CODE = ['scripts/train/02_merge.py', 'scripts/train/box_watchdog.sh', 'scripts/train/13_run10_evals.sh',
        'scripts/train/14_run10_chat_box.sh', 'scripts/train/check_loss_mask.py', 'scripts/train/spectral_plugin.py',
        'scripts/train/router_dtype_plugin.py', 'scripts/train/demo_plugin.py', 'scripts/train/41_expert_adapter_check.py',
        'scripts/train/16_project_chat_adapter.py', 'scripts/train/43_adapter_energy.py', 'scripts/data/90_generic_control.py',
        'scripts/eval/19_gen_replies.py', 'scripts/eval/26_gsm8k.py', 'scripts/eval/33_subset_cells.py',
        'scripts/eval/56_run14_box_a.py', 'configs/train/qwen3/sft.yml']
INPUTS = ['items.jsonl', 'boundary_items.jsonl', 'demos.jsonl', 'panel.jsonl', 'pov.jsonl', 'change.md', 'gsm8k_long60.jsonl']


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def prepare():
    frozen = json.loads((ROOT / 'slop/eval/run8/manifest.json').read_text())
    for name in INPUTS:
        assert sha(ROOT / 'slop/eval/run8' / name) == frozen['input_sha256'][name]
    previous = json.loads((ROOT / 'slop/eval/run13_thinking/plan.json').read_text())
    adapters = {name: previous['adapters'][name] for name in ['stoic', 'other', 'rewr', 'const']}
    for name, source in adapters.items():
        for filename, info in source['files'].items():
            assert sha(Path(source['path']) / filename) == info['sha256'], (name, filename)
    prompts = json.loads((OUT / 'prompt_manifest.json').read_text())
    assert prompts['target']['sha256'] == '91e95a6eceff6841190e2485006493b1967e0dc9cc4f954da5e8c7a488a79042'
    assert prompts['target']['supervised_tokens'] == 788606
    docs = [['stoic', .5], ['const', 1], ['other', 1]]
    prefix = 'r14_stoic0.5_const1_other1'
    cells = [{'model': prefix + '_rewr1_ctlgen-' + str(dose), 'cell': docs + [['rewr', 1], ['a14_ctlgen', -dose]],
              'equation': f'θ_I + Δ_docs + Δsft_rewr|docs − {dose}·Δsft_ctlgen|docs'} for dose in [.25, .5, 1]]
    cells += [{'model': prefix + '_ctlgen1', 'cell': docs + [['a14_ctlgen', 1]],
               'equation': 'θ_I + Δ_docs + Δsft_ctlgen|docs'},
              {'model': prefix + '_rewr0.5', 'cell': docs + [['rewr', .5]],
               'equation': 'θ_I + Δ_docs + ½·Δsft_rewr|docs'}]
    cells += [{'model': prefix + f'_proj{k}_{dose}', 'cell': docs + [[f'a14_proj{k}', dose]],
               'equation': f'θ_I + Δ_docs + {dose}·P_{k}(Δsft_rewr|docs)'} for k, dose in [(16, 1), (64, 1), (64, 1.5)]]
    cells = [cells[i] for i in [4, 3, 5, 1, 6, 0, 2, 7]]
    for row in cells:
        row['model'] = 'r14_' + '_'.join(f'{name}{dose:g}' for name, dose in row['cell'])
    plan = {'author': 'PI/OpenAI (Sol)', 'approval': 'wassname via const_v2,2026-10-26; slop/plans/20261026_box_a_control1_projection.md; lowerDdose explicitly added',
            'adapters': adapters, 'frozen_manifest': frozen, 'prompts': prompts, 'cells': cells,
            'baseline': 'r8_a0_b0', 'max_hours': HOURS, 'max_hourly_rate': RATE, 'disk_gb': 500,
            'traffic_reserve_usd': .8, 'judge_reserve_usd': 2, 'review_reserve_usd': 2,
            'termination_margin_usd': 1, 'total_reserve_usd': HOURS * RATE + 4.8 + 1,
            'thinking_heal_prompts': 0,
            'heal_pool_owner': 'Separate OpenRouter worker via const_v2; parent seq13,2026-10-26; no GPU generation or training from heal pool in BoxA',
            'training': 'Same cfg_r10_cx_chatr12 with new data/output paths,2epochs, spectral_frac=.01; same Base+docs',
            'recovery': 'On retrieval failure stop exactinstance; no replacement; independent hard destruction deadline remains.',
            'priority_if_over_cap': ['drop k64 dose1.5; notify parent BEFORE rental'],
            'runtime_guard': 'After control generation estimate steps/time from actual rowcount; may omit only final optional k64dose1.5; fail before training if required core cannot fit. Fullcontrolreview overlaps required lowerD evaluation.'}
    assert plan['total_reserve_usd'] <= 35
    (OUT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    print(json.dumps(plan, indent=2))


def quote():
    assert not rental.STATE.exists(), 'Existing run14 state: no replacement lease'
    plan = json.loads((OUT / 'plan.json').read_text())
    query = json.loads((OUT / 'offers_datacenter.json').read_text())['query']
    offers = rental.api('/bundles/?q=' + urllib.parse.quote(json.dumps(query)))['offers']
    rows = []
    for offer in offers:
        if offer['hosting_type'] != 1 or offer['gpu_name'] not in ['RTX PRO 6000 S', 'RTX PRO 6000 Max-Q'] or offer['cuda_max_good'] < 13:
            continue
        traffic = max(plan['traffic_reserve_usd'], 200 * offer['inet_down_cost'] + 15 * offer['inet_up_cost'])
        total = plan['max_hours'] * offer['dph_total'] + traffic + sum(plan[k] for k in ['judge_reserve_usd', 'review_reserve_usd', 'termination_margin_usd'])
        rows.append({'offer_id': offer['id'], 'machine_id': offer['machine_id'], 'gpu': offer['gpu_name'],
                     'hourly_including_500GB': offer['dph_total'], 'traffic_reserve_200GB_in_15GB_out': traffic, 'whole_job_usd': total})
    rows.sort(key=lambda r: r['whole_job_usd'])
    report = {'checked_epoch': time.time(), 'candidates': rows, 'eligible_under_35': [r for r in rows if r['whole_job_usd'] <= 35]}
    (OUT / 'stock_latest.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return 0 if report['eligible_under_35'] else 3


def run():
    plan = json.loads((OUT / 'plan.json').read_text())
    assert not rental.STATE.exists()
    assert plan['total_reserve_usd'] <= 35
    approval = json.loads((OUT / 'preflight_approved.json').read_text())
    assert approval['controller_sha256'] == sha(__file__)
    assert approval['local_source_sha256'] == {name: sha(ROOT / name) for name in LOCAL_CODE}
    assert approval['source_sha256'] == {name: sha(ROOT / name) for name in CODE}, 'Code changed since preflight review'
    assert approval['prompt_manifest_sha256'] == sha(OUT / 'prompt_manifest.json')
    assert approval['plan_sha256'] == sha(OUT / 'plan.json')
    assert plan['prompts']['no_robots_review']['all_selected_prompts_fully_read']
    funding = json.loads((OUT / 'funding_confirmation.json').read_text())
    selection = json.loads((OUT / 'offer_selection.json').read_text())
    assert selection['plan_sha256'] == sha(OUT / 'plan.json') and selection['reported_to_parent_utc']
    for name in INPUTS:
        assert sha(ROOT / 'slop/eval/run8' / name) == plan['frozen_manifest']['input_sha256'][name]
    for group in ['control', 'heal']:
        source = list(map(json.loads, (OUT / (group + '_prompts.jsonl')).open()))
        assert sha(OUT / (group + '_prompts.jsonl')) == plan['prompts']['pools'][group]['sha256']
        expected = [{'id': r['id'], 'system': None, 'turns': [r['prompt']], 'max_new_tokens': 2048} for r in source]
        assert list(map(json.loads, (OUT / (group + '_items.jsonl')).open())) == expected
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w:gz') as archive:
        for name in CODE:
            archive.add(ROOT / name, arcname=name)
        for name in INPUTS + ['manifest.json']:
            archive.add(ROOT / 'slop/eval/run8' / name, arcname='runs/run10/' + ('run8_manifest.json' if name == 'manifest.json' else name))
        for name in ['plan.json', 'target_tokens.json', 'control_prompts.jsonl', 'heal_prompts.jsonl', 'control_items.jsonl', 'heal_items.jsonl']:
            archive.add(OUT / name, arcname='runs/run10/' + name)
    rental.OUT.mkdir(exist_ok=True)
    query = json.loads((OUT / 'offers_datacenter.json').read_text())['query']
    offers = rental.api('/bundles/?q=' + urllib.parse.quote(json.dumps(query)))['offers']
    passing = [o for o in offers if o['id'] == selection['offer_id'] and o['hosting_type'] == 1 and o['gpu_name'] == 'RTX PRO 6000 S' and o['cuda_max_good'] >= 13.0
               and o['inet_down_cost'] <= .005 and o['inet_up_cost'] <= .005 and o['dph_total'] <= RATE]
    assert passing, 'No current datacentre offer fits; no lease created'
    assert len(passing) == 1, 'Reported exact offer unavailable or ambiguous; report a fresh quote before creation'
    offer = passing[0]
    account = rental.api('/users/current/')
    traffic = max(plan['traffic_reserve_usd'], 200 * offer['inet_down_cost'] + 15 * offer['inet_up_cost'])
    total = HOURS * offer['dph_total'] + traffic + sum(plan[k] for k in ['judge_reserve_usd', 'review_reserve_usd', 'termination_margin_usd'])
    assert total <= min(35, selection['maximum_total_usd']), 'Actual offer including traffic exceeds reported/approved reservation'
    cash_required = HOURS * offer['dph_total'] + traffic + plan['termination_margin_usd'] + 1
    autobill = account['autobill_amount'] if funding['auto_billing_confirmed'] and account['has_billing'] and not account['billing_failed'] and account['autobill_threshold'] > 0 else 0
    assert account['credit'] + autobill >= cash_required, f"Vast available funding {account['credit'] + autobill:.2f} below guarded requirement {cash_required:.2f}"
    assert not [r for r in rental.api('/instances/')['instances'] if r['label'] == rental.LABEL]
    (rental.OUT / 'rental_quote.json').write_text(json.dumps({'offer': offer, 'maximum_hours': HOURS,
        'total_reserve_usd': total, 'traffic_reserve_usd': traffic, 'reported_selection': selection,
        'vast_cash_required': cash_required, 'auto_billing_confirmation': funding,
        'live_account_funding': {k: account[k] for k in ['credit', 'has_billing', 'billing_failed', 'autobill_amount', 'autobill_threshold']}}, indent=2))
    started = time.time()
    created = rental.api(f"/asks/{offer['id']}/", 'PUT', {'client_id': 'me', 'image': rental.IMAGE, 'disk': 500,
        'label': rental.LABEL, 'runtype': 'ssh_direct', 'cancel_unavail': True})
    assert created['success'], created
    state = {'instance_id': created['new_contract'], 'created_epoch': started, 'hard_destroy_epoch': started + HOURS * 3600,
             'runner_deadline_epoch': started + (HOURS - 1.5) * 3600, 'hourly_rate': offer['dph_total'], 'image': rental.IMAGE}
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
        seen = set()
        while not stop.wait(60):
            try:
                code = "from pathlib import Path; import json; p=Path('/workspace/cg/runs/run10'); print(json.dumps([n for n in ['control_pilot_ready.json','control_ready.json','generate.exit'] if (p/n).exists()]+[f.name for f in p.glob('r14_*.done')]))"
                result = remote('touch /workspace/heartbeat; python -c ' + shlex.quote(code), timeout=15, capture_output=True, text=True)
                for stage in json.loads(result.stdout):
                    if stage not in seen:
                        print('RUN14 MILESTONE ' + stage, flush=True)
                        seen.add(stage)
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
        (rental.OUT / 'executed_source_sha256.json').write_text(json.dumps({p: sha(ROOT / p) for p in CODE}, indent=2))
        remote('mkdir -p /workspace/cg/runs/run10; tar -xzf - -C /workspace/cg', input=stream.getvalue(), timeout=90)
        remote("touch /workspace/heartbeat; tmux new-session -d -s run10_watchdog 'cd /workspace/cg && MAX_SILENT_H=1 bash scripts/train/box_watchdog.sh > runs/run10/watchdog.log 2>&1'")
        remote("for i in $(seq 1 50); do if grep -q 'auth check GET: 200' /workspace/cg/runs/run10/watchdog.log; then cat /workspace/cg/runs/run10/watchdog.log; exit 0; fi; sleep .2; done; exit 1", timeout=20)
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
        beat = pool.submit(heartbeat)

        def setup():
            with (rental.OUT / 'setup.log').open('w') as log:
                remote('cd /workspace/cg && UV_EXCLUDE_NEWER="8 days" uv pip install --python "$(command -v python)" jaxtyping==0.3.11 beartype==0.23.1 && bash scripts/train/13_run10_evals.sh prep', timeout=5400, stdout=log, stderr=subprocess.STDOUT)
            command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN14_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/56_run14_box_a.py --generate'
            script = f'set +e; {command} > runs/run10/generate.log 2>&1; status=$?; echo $status > runs/run10/generate.exit; exit $status'
            remote('cd /workspace/cg && tmux new-session -d -s run14_generate ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
            print('GENERATION STARTED during adapter uploads', flush=True)
            fetch = "from huggingface_hub import snapshot_download; print(snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422',ignore_patterns=['*.gguf','*.bin','*.onnx'],max_workers=8))"
            with (rental.OUT / 'base_download.log').open('w') as log:
                remote('HF_HOME=/workspace/hf python -c ' + shlex.quote(fetch), timeout=5400, stdout=log, stderr=subprocess.STDOUT)
        setup_future = pool.submit(setup)
        for name, source in plan['adapters'].items():
            if setup_future.done():
                setup_future.result()
            target = '/workspace/cg/outputs/up_' + name
            remote('mkdir -p ' + target, timeout=30)
            with (rental.OUT / f'upload_{name}.log').open('w') as log:
                subprocess.run(['rsync', '-az', '--partial', '-e', shlex.join(ssh),
                    source['path'] + '/adapter_config.json', source['path'] + '/adapter_model.safetensors', host + ':' + target + '/'],
                    check=True, stdout=log, stderr=subprocess.STDOUT, timeout=max(1, state['runner_deadline_epoch'] - time.time() - 3600))
            expected = {target + '/' + filename: info['sha256'] for filename, info in source['files'].items()}
            verify = 'import hashlib; files=' + repr(expected) + '; assert all(hashlib.file_digest(open(p,"rb"),"sha256").hexdigest()==s for p,s in files.items())'
            remote('python -c ' + shlex.quote(verify), timeout=300)
            print('REMOTE ADAPTER VERIFIED ' + name, flush=True)
        setup_future.result()
        command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN14_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/56_run14_box_a.py'
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
    print('RUN14 RETRIEVED; exact instance destroyed', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['prepare', 'quote', 'run', 'snapshot', 'approve-pilot', 'approve-control'])
    args = parser.parse_args()
    if args.action == 'prepare':
        prepare()
    elif args.action == 'quote':
        sys.exit(quote())
    elif args.action == 'run':
        with rental.controller_owner():
            run()
    elif args.action == 'snapshot':
        state = json.loads(rental.STATE.read_text())
        ssh, host = rental.saved_connection(state)
        rental.retrieve_outputs(ssh, host, state)
    else:
        state = json.loads(rental.STATE.read_text())
        ssh, host = rental.saved_connection(state)
        filename = 'pilot_review.approved.json' if args.action == 'approve-pilot' else 'control_review.approved.json'
        path = OUT / filename
        receipt = json.loads(path.read_text())
        data = rental.OUT / 'box_runs' / ('control_pilot.jsonl' if args.action == 'approve-pilot' else 'ctlgen.jsonl')
        assert receipt['sha256'] == sha(data)
        assert receipt['fully_read_rows'] == sum(1 for _ in data.open()) and receipt['independent_review_path']
        subprocess.run(['rsync', '-az', '-e', shlex.join(ssh), str(path), host + ':/workspace/cg/runs/run10/' + filename], check=True, timeout=60)
