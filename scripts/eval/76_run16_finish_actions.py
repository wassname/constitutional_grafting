"""Apply the supervisor's deferred c=skip and verify final result files without rolling controller4224. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'


def approved_skip(decision,ready):
    assert ready,'Do not publish c decision before optional_c_ready'
    assert decision['action']=='skip' and decision['reason'],'Only the supervisor-approved skip is supported'
    return json.dumps(decision,ensure_ascii=False,indent=2)+'\n'


def main():
    spec=importlib.util.spec_from_file_location('rental16',ROOT/'scripts/eval/60_run16_rental.py')
    control=importlib.util.module_from_spec(spec);spec.loader.exec_module(control)
    collect_spec=importlib.util.spec_from_file_location('collect16',ROOT/'scripts/eval/67_run16_collect.py')
    collect=importlib.util.module_from_spec(collect_spec);collect_spec.loader.exec_module(collect)
    state=json.loads(control.rental.STATE.read_text());assert state['instance_id']==57919543
    ssh,host=control.rental.saved_connection(state)
    deadline=state['hard_destroy_epoch']-120
    def run(argv,**kwargs):
        assert time.time()<deadline
        return subprocess.run(list(map(str,argv)),check=True,timeout=min(300,deadline-time.time()),**kwargs)
    ready=OUT/'optional_c_ready.json'
    while not ready.exists():
        assert time.time()<state['runner_deadline_epoch'],'Skip event never arrived before unchanged runner deadline'
        time.sleep(5)
    assert (OUT/'anchored_chat_evaluated.json').exists(),'Required anchored cells must precede optional c'
    target=ROOT/'.local/artifacts/run16/final_results';target.mkdir(parents=True,exist_ok=True)
    def sync():
        collect.sync_results(['rsync','-az','--delete-delay','--exclude=merged_model','--exclude=dose_model','--exclude=selector_D1',
             '--exclude=heal_parent','--exclude=healed_model','-e',shlex.join(ssh),host+':/workspace/cg/runs/run10/',str(target)+'/'],deadline)
    # Pre-copy while the driver is safely waiting, so only tiny final receipts/log tails remain after skip.
    sync()
    decision=json.loads((OUT/'optional_c.skip_decision.json').read_text())
    approval=OUT/'optional_c.approved.json';approval.write_text(approved_skip(decision,ready.exists()))
    run(['rsync','-az','-e',shlex.join(ssh),approval,host+':/workspace/cg/runs/run10/'+approval.name])
    result=run(ssh+[host,'sha256sum /workspace/cg/runs/run10/'+approval.name],capture_output=True,text=True)
    digest=hashlib.sha256(approval.read_bytes()).hexdigest();assert result.stdout.split()[0]==digest
    (OUT/'optional_c_upload_verified.json').write_text(json.dumps({'instance_id':state['instance_id'],'all_match':True,
        'sha256':digest,'decision':decision,'epoch':time.time()},indent=2)+'\n')
    print('APPROVED c=SKIP UPLOADED AND SHA VERIFIED',flush=True)
    while True:
        result=run(ssh+[host,'cat /workspace/cg/runs/run10/job.exit 2>/dev/null || true'],capture_output=True,text=True)
        if result.stdout.strip():
            assert result.stdout.strip()=='0','Driver failed after skip; live controller owns repair hold'
            break
        time.sleep(2)
    sync()
    run([sys.executable,ROOT/'scripts/eval/74_run16_result_hashes.py','--local-root',target,
         '--receipt',OUT/'final_result_hashes_verified.json'])
    print('ALL FINAL RESULT FILES SHA VERIFIED; controller still owns adapter retrieval/destruction',flush=True)
    closure=OUT/'provider_closure_verified.json'
    while True:
        if closure.exists():
            try:closed=json.loads(closure.read_text())
            except ValueError:closed={}
            if closed.get('instance_id')==state['instance_id'] and closed.get('absent_confirmed'):break
        assert time.time()<state['hard_destroy_epoch'],'Closure receipt not observed before hard deadline'
        time.sleep(5)
    adapters=json.loads((OUT/'lease/retrieval_verified.json').read_text());assert adapters['job_exit']=='0' and adapters['all_available_final_adapter_hashes_match']
    results=json.loads((OUT/'final_result_hashes_verified.json').read_text());assert results['all_match']
    (OUT/'final_delivery_verified.json').write_text(json.dumps({'author':'PI/OpenAI (Sol)','instance_id':state['instance_id'],
        'all_final_adapters_sha_match':True,'all_result_files_sha_match':True,'result_files':len(results['files']),
        'final_adapters':sorted(adapters['manifest']),'provider_absent_confirmed':True,
        'scope':'Final adapters and all result files. Checkpoints and ortho basis not required by supervisor.',
        'epoch':time.time()},indent=2)+'\n')
    print('FINAL ADAPTERS + RESULTS VERIFIED; EXACT INSTANCE DESTRUCTION CONFIRMED',flush=True)


if __name__=='__main__':main()
