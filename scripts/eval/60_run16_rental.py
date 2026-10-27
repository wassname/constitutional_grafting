"""Run16 fork of run14 controller: one exact-ID guarded lease; $65 total cap, no push. -- PI/OpenAI (Sol)"""
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
OUT = ROOT / 'slop/eval/run16_v2'
SPEC = importlib.util.spec_from_file_location('rental', ROOT / 'scripts/eval/38_run10_chat_rental.py')
rental = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rental)
rental.OUT = OUT / 'lease'
rental.STATE = ROOT / '.local/run16_v2_rental.json'
rental.LABEL = 'cg-run16-v2'
rental.SUBSETS = rental.DOCS = []
rental.EXPECTED_ADAPTERS_FILE = 'required_adapters.json'
rental.ADAPTER_DIR = Path.home() / '.local/share/cg_run16_adapters'
HOURS, RATE = 26, 1.92
LOCAL_CODE = ['scripts/eval/38_run10_chat_rental.py', 'scripts/eval/48_vast_deadline.py']
CODE = ['scripts/train/02_merge.py', 'scripts/train/box_watchdog.sh', 'scripts/train/13_run10_evals.sh',
        'scripts/train/14_run10_chat_box.sh', 'scripts/train/check_loss_mask.py', 'scripts/train/spectral_plugin.py',
        'scripts/train/router_dtype_plugin.py', 'scripts/train/demo_plugin.py', 'scripts/train/spectral_math.py', 'scripts/train/41_expert_adapter_check.py',
        'scripts/train/16_project_chat_adapter.py', 'scripts/train/43_adapter_energy.py', 'scripts/data/90_generic_control.py',
        'scripts/eval/19_gen_replies.py', 'scripts/eval/26_gsm8k.py', 'scripts/eval/33_subset_cells.py',
        'scripts/eval/62_run16_box.py', 'scripts/eval/61_run16_cells.py', 'scripts/eval/47_base_heldout_loss.py',
        'scripts/train/18_project_char_vs_cap.py', 'configs/train/qwen3/sft.yml']
INPUTS = ['run8_manifest.json', 'run16_manifest.json', 'items.jsonl', 'boundary_items.jsonl', 'demos.jsonl', 'panel.jsonl', 'pov.jsonl', 'change.md', 'gsm8k_long60.jsonl']


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def run():
    plan = json.loads((OUT / 'plan.json').read_text())
    assert not rental.STATE.exists()
    assert plan['total_reserve_usd'] <= 65
    approval = json.loads((OUT / 'preflight_approved.json').read_text())
    assert approval['controller_sha256'] == sha(__file__)
    assert approval['source_sha256'] == {name: sha(ROOT / name) for name in CODE + LOCAL_CODE}
    assert approval['plan_sha256'] == sha(OUT / 'plan.json')
    assert approval['cpu_pipeline_pass']
    assert sha(ROOT/'data/train/eos_fixed/chatr12.jsonl') == plan['training_data_sha256']
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode='w:gz') as archive:
        for name in CODE:
            archive.add(ROOT / name, arcname=name)
        for name in INPUTS:
            archive.add(OUT/'inputs'/name, arcname='runs/run10/'+name)
        archive.add(OUT/'plan.json',arcname='runs/run10/plan.json')
        for name, digest in plan['heldout_sha256'].items():
            source=Path('/workspace/2026/constitutional_grafting/data/train/run11')/name
            assert sha(source)==digest
            archive.add(source,arcname='data/train/run16_heldout/'+name)
        archive.add(ROOT/'slop/eval/run10/stage7/box_runs/cfg_r10_cx_chatr12.yml',arcname='runs/run10/cfg_original_chatr12.yml')
        archive.add(ROOT/'data/train/eos_fixed/chatr12.jsonl',arcname='data/train/eos_fixed/chatr12.jsonl')
        archive.add(Path('/workspace/2026/constitutional_grafting/slop/eval/run14_box_a/lease/box_runs/ctlgen.jsonl'),arcname='data/train/run14/ctlgen.jsonl')
    rental.OUT.mkdir(exist_ok=True)
    query = plan['offer_query']
    offers = rental.api('/bundles/?q=' + urllib.parse.quote(json.dumps(query)))['offers']
    passing = [o for o in offers if o['hosting_type'] == 1 and o['gpu_name'] == 'RTX PRO 6000 S' and o['cuda_max_good'] >= 13.0
               and o['inet_down_cost'] <= .005 and o['inet_up_cost'] <= .005 and o['dph_total'] <= RATE]
    assert passing, 'No current datacentre offer fits; no lease created'
    offer = min(passing,key=lambda o:o['dph_total'])
    account = rental.api('/users/current/')
    traffic = max(plan['traffic_reserve_usd'], 250 * offer['inet_down_cost'] + 120 * offer['inet_up_cost'])
    total = HOURS * offer['dph_total'] + traffic + sum(plan[k] for k in ['judge_reserve_usd', 'review_reserve_usd', 'termination_margin_usd'])
    assert total <= 65, 'Actual offer including traffic exceeds reported/approved reservation'
    cash_required = HOURS * offer['dph_total'] + traffic + plan['termination_margin_usd'] + 1
    autobill = account['autobill_amount'] if account['has_billing'] and not account['billing_failed'] and account['autobill_threshold'] > 0 else 0
    assert account['credit'] + autobill >= cash_required, f"Vast available funding {account['credit'] + autobill:.2f} below guarded requirement {cash_required:.2f}"
    assert not [r for r in rental.api('/instances/')['instances'] if r['label'] == rental.LABEL]
    (rental.OUT / 'rental_quote.json').write_text(json.dumps({'offer': offer, 'maximum_hours': HOURS,
        'total_reserve_usd': total, 'traffic_reserve_usd': traffic, 'selection_policy':'cheapest eligible RTX PRO 6000 S under rate/cap',
        'vast_cash_required': cash_required, 'auto_billing_policy':'AGENTS auto-top-up confirmed by wassname',
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
                code = "from pathlib import Path; import json; p=Path('/workspace/cg/runs/run10'); print(json.dumps([n for n in ['eos_trained.json','chat_evaluated.json','documents_evaluated.json','selector_gate.json','anchored_gate_ready.json','anch_trained.json','anchored_chat_evaluated.json'] if (p/n).exists()]+[f.name for f in p.glob('r16_*.done')]))"
                result = remote('touch /workspace/heartbeat; python -c ' + shlex.quote(code), timeout=15, capture_output=True, text=True)
                for stage in json.loads(result.stdout):
                    if stage not in seen:
                        print('RUN16 MILESTONE ' + stage, flush=True)
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
            fetch = "from huggingface_hub import snapshot_download; print(snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422',ignore_patterns=['*.gguf','*.bin','*.onnx'],max_workers=8))"
            with (rental.OUT / 'base_download.log').open('w') as log:
                remote('HF_HOME=/workspace/hf python -c '+shlex.quote(fetch),timeout=5400,stdout=log,stderr=subprocess.STDOUT)
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
        command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN16_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/62_run16_box.py'
        script = f'set +e; {command} > runs/run10/job.log 2>&1; status=$?; echo $status > runs/run10/job.exit; exit $status'
        remote('cd /workspace/cg && tmux new-session -d -s run10_train ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
        rental.monitor(remote, lambda: max(1, state['runner_deadline_epoch'] - time.time()), stop, beat)
    finally:
        try:
            if ssh is not None:
                try:
                    rental.retrieve_outputs(ssh, host, state)
                finally:
                    rental.destroy()
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
    print('RUN16 RETRIEVED; exact instance destroyed', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['run','snapshot','approve-gate','destroy'])
    args=parser.parse_args()
    if args.action=='run':
        with rental.controller_owner(): run()
    elif args.action=='destroy': rental.destroy()
    else:
        state=json.loads(rental.STATE.read_text()); ssh,host=rental.saved_connection(state)
        if args.action=='snapshot': rental.retrieve_outputs(ssh,host,state)
        else:
            path=OUT/'anchored_gate.approved.json'
            subprocess.run(['rsync','-az','-e',shlex.join(ssh),str(path),host+':/workspace/cg/runs/run10/'+path.name],check=True,timeout=60)
