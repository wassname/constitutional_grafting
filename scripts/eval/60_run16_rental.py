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
HOURS, RATE = 24.5, 1.92
LOCAL_CODE = ['scripts/eval/38_run10_chat_rental.py', 'scripts/eval/48_vast_deadline.py']
CODE = ['scripts/train/02_merge.py', 'scripts/train/box_watchdog.sh', 'scripts/train/13_run10_evals.sh',
        'scripts/train/14_run10_chat_box.sh', 'scripts/train/check_loss_mask.py', 'scripts/train/spectral_plugin.py',
        'scripts/train/router_dtype_plugin.py', 'scripts/train/demo_plugin.py', 'scripts/train/spectral_math.py', 'scripts/train/41_expert_adapter_check.py',
        'scripts/train/16_project_chat_adapter.py', 'scripts/train/43_adapter_energy.py', 'scripts/data/90_generic_control.py',
        'scripts/eval/19_gen_replies.py', 'scripts/eval/26_gsm8k.py', 'scripts/eval/33_subset_cells.py',
        'scripts/eval/62_run16_box.py', 'scripts/eval/61_run16_cells.py', 'scripts/eval/47_base_heldout_loss.py', 'scripts/eval/run16_recovery.py',
        'scripts/train/18_project_char_vs_cap.py', 'configs/train/qwen3/sft.yml']
INPUTS = ['draft_code_tools.jsonl', 'small_tasks.jsonl', 'run8_manifest.json', 'run16_manifest.json', 'items.jsonl', 'boundary_items.jsonl', 'demos.jsonl', 'panel.jsonl', 'pov.jsonl', 'change.md', 'gsm8k_long60.jsonl']


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def retrieve_hold_snapshot(ssh,host,state,hold_until,failure_index):
    """Copy and verify final AND checkpoint adapters while the owned instance remains alive."""
    bounded=dict(state,hard_destroy_epoch=min(state['hard_destroy_epoch'],hold_until))
    code="import hashlib,json;from pathlib import Path;p=Path('/workspace/cg/outputs');print(json.dumps({str(f.relative_to(p)):hashlib.file_digest(f.open('rb'),'sha256').hexdigest() for d in p.glob('r10_*') for f in d.rglob('adapter_*') if f.is_file()}))"
    manifest=json.loads(subprocess.check_output(ssh+[host,'python -c '+shlex.quote(code)],text=True,
        timeout=min(300,max(1,hold_until-time.time()-60))))
    rental.retrieve_outputs(ssh,host,bounded)
    for name,digest in manifest.items():assert sha(rental.ADAPTER_DIR/name)==digest,name
    receipt={'instance_id':state['instance_id'],'failure_index':failure_index,'files_sha256':manifest,
             'all_final_and_checkpoint_adapters_verified':True,'verified_epoch':time.time()}
    (rental.OUT/f'held_retrieval_{failure_index}.json').write_text(json.dumps(receipt,indent=2)+'\n')
    return receipt


def upload_approved_sources(remote,fix):
    assert fix['reason'] and fix['source_sha256']
    archive=io.BytesIO()
    with tarfile.open(fileobj=archive,mode='w:gz') as bundle:
        for path,digest in fix['source_sha256'].items():
            assert path in CODE and sha(ROOT/path)==digest,(path,'unapproved or changed hotfix')
            bundle.add(ROOT/path,arcname=path)
    remote('tar -xzf - -C /workspace/cg',input=archive.getvalue(),timeout=90)
    verify='import hashlib; files='+repr({'/workspace/cg/'+p:d for p,d in fix['source_sha256'].items()})+"; assert all(hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()==s for p,s in files.items())"
    remote('python -c '+shlex.quote(verify),timeout=60)


def archive_failed_outputs(remote,failure_index,partial_models=()):
    code="import sys,json;sys.path.insert(0,'/workspace/cg/scripts/eval');from run16_recovery import archive_partial_cells; print(json.dumps(archive_partial_cells('/workspace/cg/runs/run10',"+repr(list(partial_models))+","+str(failure_index)+")))"
    remote('python -c '+shlex.quote(code),timeout=60)


def start_driver(remote,state,resume_chat=False):
    command=f'cd /workspace/cg && HF_HOME=/workspace/hf RUN16_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/62_run16_box.py'
    if resume_chat:command+=' --resume-chat'
    script=f'set +e; {command} > runs/run10/job.log 2>&1; status=$?; echo $status > runs/run10/job.exit; exit $status'
    remote('cd /workspace/cg && tmux new-session -d -s run10_train '+shlex.quote('bash -lc '+shlex.quote(script)),timeout=30)


def remote_production_started(remote):
    code="import json,sys,time; from pathlib import Path; sys.path.insert(0,'/workspace/cg/scripts/eval'); from run16_recovery import production_step_evidence; p=Path('/workspace/cg/runs/run10/production_started.json'); e=production_step_evidence('/workspace/cg'); p.write_text(json.dumps(e)) if e and not p.exists() else None; print(json.dumps(e))"
    result=remote('python -c '+shlex.quote(code),timeout=30,capture_output=True,text=True)
    return json.loads(result.stdout)


def monitor_with_repair(remote,state,stop,heartbeat,now=None,allow_postproduction=False,failure_index_start=0,snapshot=None):
    """Only failures before the first production update get a bounded, explicit-approval repair hold."""
    now=now or time.time
    hold_until=None;failure_index=failure_index_start
    while True:
        try:
            rental.monitor(remote,lambda:max(1,state['runner_deadline_epoch']-now()),stop,heartbeat)
            return
        except AssertionError as error:
            if not (str(error).startswith('remote comparison exited') or str(error)=='detached comparison disappeared without an exit record'):
                raise
            evidence=remote_production_started(remote)
            if evidence and not allow_postproduction:
                (rental.OUT/'post_production_failure.json').write_text(json.dumps({'instance_id':state['instance_id'],
                    'error':str(error),'production_evidence':evidence,'action':'retrieve then destroy; no repair hold'},indent=2)+'\n')
                raise
            if allow_postproduction or hold_until is None:hold_until=min(now()+3600,state['runner_deadline_epoch'])
            event={'instance_id':state['instance_id'],'failure_index':failure_index,'error':str(error),
                   'status':'holding','first_production_step_observed':bool(evidence),'post_production':bool(evidence),'hold_until_epoch':hold_until,
                   'hard_destroy_epoch':state['hard_destroy_epoch'],
                   'action':'keep heartbeat/deadline guard; investigate; upload approved hotfix and restart within existing60min window'}
            def publish():
                data=json.dumps(event,indent=2)+'\n'
                (rental.OUT/'driver_failure.json').write_text(data)
                (rental.OUT/f'driver_failure_{failure_index}.json').write_text(data)
                remote('cat > /workspace/cg/runs/run10/driver_failure.json',input=data.encode(),timeout=30)
            publish();print('RUN16 PRE-PRODUCTION REPAIR HOLD '+json.dumps(event),flush=True)
            if allow_postproduction:
                assert snapshot is not None,'Post-production hold requires verified retrieval'
                try:event['retrieval']=snapshot(failure_index,hold_until)
                except Exception as retrieval_error:event['retrieval_error']=repr(retrieval_error)
                publish()
            approval=OUT/'driver_repair.approved.json'
            while True:
                while now()<hold_until and not approval.exists():
                    if heartbeat.done():heartbeat.result()
                    stop.wait(min(5,max(0,hold_until-now())))
                if not approval.exists():
                    event['status']='expired';publish()
                    raise TimeoutError('repair window expired; retrieve then destroy') from error
                try:
                    fix=json.loads(approval.read_text())
                    assert fix['instance_id']==state['instance_id'] and fix['failure_index']==failure_index,'stale repair approval'
                    assert fix['reason'] and fix['source_sha256']
                    if allow_postproduction:assert fix.get('resume_chat') is True,'Post-production repair must request verified resume'
                    for path,digest in fix['source_sha256'].items():assert path in CODE and sha(ROOT/path)==digest,'changed/unapproved hotfix: '+path
                except (AssertionError,ValueError,KeyError) as invalid:
                    approval.rename(rental.OUT/f'driver_repair_rejected_{failure_index}_{int(now())}.json')
                    event['approval_error']=str(invalid);publish()
                    continue
                break
            upload_approved_sources(remote,fix)
            if allow_postproduction:
                assert fix.get('resume_chat') is True,'Post-production repair must explicitly request verified resume'
                archive_failed_outputs(remote,failure_index,fix.get('partial_models',[]))
            else:
                assert not remote_production_started(remote),'production started during repair approval; do not restart'
                previous=f'/workspace/cg/runs/run10/driver_failures/attempt_{failure_index}'
                remote('mkdir -p '+previous+'; cd /workspace/cg/runs/run10; for f in job.log job.exit train_random_smoke.log train_r10_eos_chatr12.log; do [ ! -f "$f" ] || mv "$f" '+previous+'/; done; rm -rf /workspace/cg/outputs/random_smoke_base /workspace/cg/outputs/random_smoke_adapter /workspace/cg/outputs/prepared_random_smoke',timeout=60)
            approval.rename(rental.OUT/f'driver_repair_{failure_index}.approved.json')
            event.update(status='restarting',repair=fix);publish()
            start_driver(remote,state,resume_chat=True) if allow_postproduction else start_driver(remote,state)
            failure_index+=1


def parallel_work(remote,ssh,host,state,plan,setup,stop,heartbeat,pool):
    def upload(name):
        source=plan['adapters'][name];target='/workspace/cg/outputs/up_'+name
        remote('mkdir -p '+target,timeout=30);started=time.time()
        with (rental.OUT/f'upload_{name}_parallel.log').open('w') as log:
            subprocess.run(['rsync','-az','--partial','--info=progress2','-e',shlex.join(ssh),
                source['path']+'/adapter_config.json',source['path']+'/adapter_model.safetensors',host+':'+target+'/'],
                check=True,stdout=log,stderr=subprocess.STDOUT,timeout=max(1,state['runner_deadline_epoch']-time.time()-4*3600))
        expected={target+'/'+f:v['sha256'] for f,v in source['files'].items()}
        verify='import hashlib; files='+repr(expected)+"; assert all(hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()==s for p,s in files.items())"
        remote('python -c '+shlex.quote(verify),timeout=300)
        receipt={'name':name,'files':expected,'seconds':time.time()-started,'verified_epoch':time.time(),'instance_id':state['instance_id']}
        data=json.dumps(receipt,indent=2)+'\n';(rental.OUT/f'upload_{name}.verified.json').write_text(data)
        remote('cat > /workspace/cg/runs/run10/upload_'+name+'.verified.json',input=data.encode(),timeout=30)
        print('REMOTE ADAPTER VERIFIED '+name,flush=True)
    pending={name:pool.submit(upload,name) for name in ['stoic','const','other','rewr','mix_stoic','mix_const']}
    for name in ['stoic','const','other']:pending[name].result()
    pending['ctl']=pool.submit(upload,'ctl')
    setup.result()
    start_driver(remote,state)
    print('NEW-D DRIVER STARTED after three doc donors; remaining uploads continue',flush=True)
    def checked_remote(*args,**kwargs):
        for future in pending.values():
            if future.done():future.result()
        return remote(*args,**kwargs)
    monitor_with_repair(checked_remote,state,stop,heartbeat)
    for future in pending.values():future.result()


def run():
    plan = json.loads((OUT / 'plan.json').read_text())
    assert not rental.STATE.exists()
    assert plan['total_reserve_usd'] <= 65
    assert plan['max_hours']==HOURS and plan['max_hourly_rate']==RATE
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
    total = plan['prior_spend_reserve_usd'] + HOURS * offer['dph_total'] + traffic + sum(plan[k] for k in ['judge_reserve_usd', 'review_reserve_usd', 'termination_margin_usd'])
    assert total <= 65, 'Actual offer including traffic exceeds reported/approved reservation'
    cash_required = HOURS * offer['dph_total'] + traffic + plan['termination_margin_usd'] + 1
    autobill = account['autobill_amount'] if account['has_billing'] and not account['billing_failed'] and account['autobill_threshold'] > 0 else 0
    assert account['credit'] + autobill >= cash_required, f"Vast available funding {account['credit'] + autobill:.2f} below guarded requirement {cash_required:.2f}"
    assert not [r for r in rental.api('/instances/')['instances'] if r['label'] == rental.LABEL]
    (rental.OUT / 'rental_quote.json').write_text(json.dumps({'offer': offer, 'maximum_hours': HOURS,
        'total_reserve_usd': total, 'prior_spend_reserve_usd':plan['prior_spend_reserve_usd'], 'traffic_reserve_usd': traffic, 'selection_policy':'cheapest eligible RTX PRO 6000 S under rate/cap',
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
        pool = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        beat = pool.submit(heartbeat)

        def setup():
            with (rental.OUT / 'setup.log').open('w') as log:
                remote('cd /workspace/cg && UV_EXCLUDE_NEWER="8 days" uv pip install --python "$(command -v python)" jaxtyping==0.3.11 beartype==0.23.1 && bash scripts/train/13_run10_evals.sh prep', timeout=5400, stdout=log, stderr=subprocess.STDOUT)
            fetch = "from huggingface_hub import snapshot_download; print(snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422',ignore_patterns=['*.gguf','*.bin','*.onnx'],max_workers=8))"
            with (rental.OUT / 'base_download.log').open('w') as log:
                remote('HF_HOME=/workspace/hf python -c '+shlex.quote(fetch),timeout=5400,stdout=log,stderr=subprocess.STDOUT)
        setup_future = pool.submit(setup)
        parallel_work(remote,ssh,host,state,plan,setup_future,stop,beat,pool)
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


def parallel_attach():
    """Resume an owned existing lease; never creates a replacement instance."""
    state=json.loads(rental.STATE.read_text());plan=json.loads((OUT/'plan.json').read_text())
    ssh,host=rental.saved_connection(state)
    assert any(r['id']==state['instance_id'] and r['label']==rental.LABEL for r in rental.api('/instances/')['instances'])
    assert (rental.OUT/'deadline_guard_armed.json').exists()
    stop=threading.Event()
    def remote(command,timeout=600,**kwargs):
        left=state['hard_destroy_epoch']-time.time()-120;assert left>0
        return subprocess.run(ssh+[host,command],check=True,timeout=min(timeout,left),**kwargs)
    def beat():
        while not stop.wait(60):remote('touch /workspace/heartbeat',timeout=15,stdout=subprocess.DEVNULL)
    pool=concurrent.futures.ThreadPoolExecutor(max_workers=10);heartbeat=pool.submit(beat)
    try:
        # Attach is for an already-launched driver. Fresh/replacement leases always use run().
        monitor_with_repair(remote,state,stop,heartbeat)
    finally:
        try:
            try:rental.retrieve_outputs(ssh,host,state)
            finally:rental.destroy()
        finally:stop.set();pool.shutdown(wait=True)


def resume_chat_attach():
    state=json.loads(rental.STATE.read_text());fix=json.loads((OUT/'chat_resume.approved.json').read_text())
    assert fix['instance_id']==state['instance_id'] and fix['resume_chat'] is True
    assert fix['failure_index']==1,'This action consumes the explicit current GSM-failure recovery approval'
    assert any(r['id']==state['instance_id'] and r['label']==rental.LABEL for r in rental.api('/instances/')['instances'])
    guard=json.loads((rental.OUT/'deadline_guard_armed.json').read_text())
    assert guard['instance_id']==state['instance_id'] and guard['deadline_epoch']==state['hard_destroy_epoch']
    ssh,host=rental.saved_connection(state);stop=threading.Event()
    def remote(command,timeout=600,**kwargs):
        left=state['hard_destroy_epoch']-time.time()-120;assert left>0
        return subprocess.run(ssh+[host,command],check=True,timeout=min(timeout,left),**kwargs)
    def beat():
        while not stop.wait(60):remote('touch /workspace/heartbeat',timeout=15,stdout=subprocess.DEVNULL)
    pool=concurrent.futures.ThreadPoolExecutor(max_workers=1);heartbeat=pool.submit(beat)
    started=False
    try:
        remote('touch /workspace/heartbeat',timeout=30)
        upload_approved_sources(remote,fix)
        archive_failed_outputs(remote,fix['failure_index'],fix['partial_models'])
        (OUT/'chat_resume.approved.json').rename(rental.OUT/'chat_resume_1.approved.json')
        start_driver(remote,state,resume_chat=True);started=True
        monitor_with_repair(remote,state,stop,heartbeat,allow_postproduction=True,failure_index_start=2,
            snapshot=lambda index,until:retrieve_hold_snapshot(ssh,host,state,until,index))
    finally:
        try:
            if started:
                try:rental.retrieve_outputs(ssh,host,state)
                finally:rental.destroy()
                assert all(r['id']!=state['instance_id'] for r in rental.api('/instances/')['instances'])
                (OUT/'provider_closure_verified.json').write_text(json.dumps({'instance_id':state['instance_id'],
                    'absent_confirmed':True,'elapsed_hours':(time.time()-state['created_epoch'])/3600,
                    'estimated_gpu_usd':(time.time()-state['created_epoch'])/3600*state['hourly_rate']},indent=2)+'\n')
            else:
                (rental.OUT/'resume_setup_failure.json').write_text(json.dumps({'instance_id':state['instance_id'],
                    'action':'No destroy: preserve existing artifacts; supervisor must repair setup before watchdog/deadline'},indent=2)+'\n')
        finally:stop.set();pool.shutdown(wait=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['run','parallel-attach','resume-chat','snapshot','approve-gate','destroy'])
    args=parser.parse_args()
    if args.action in ['run','parallel-attach','resume-chat']:
        with rental.controller_owner():
            {'run':run,'parallel-attach':parallel_attach,'resume-chat':resume_chat_attach}[args.action]()
    elif args.action=='destroy': rental.destroy()
    else:
        state=json.loads(rental.STATE.read_text()); ssh,host=rental.saved_connection(state)
        if args.action=='snapshot': rental.retrieve_outputs(ssh,host,state)
        else:
            path=OUT/'anchored_gate.approved.json'
            subprocess.run(['rsync','-az','-e',shlex.join(ssh),str(path),host+':/workspace/cg/runs/run10/'+path.name],check=True,timeout=60)
