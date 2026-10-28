"""Preserve run16 selector moments before exact-ID teardown; no model calls. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'


def main():
    spec=importlib.util.spec_from_file_location('rental16',ROOT/'scripts/eval/60_run16_rental.py')
    rental=importlib.util.module_from_spec(spec);spec.loader.exec_module(rental)
    state=json.loads(rental.rental.STATE.read_text());ssh,host=rental.rental.saved_connection(state)
    while time.time()<state['runner_deadline_epoch']:
        ready=subprocess.run(ssh+[host,'test -f /workspace/cg/runs/run10/selector_gate.json'],timeout=30)
        if ready.returncode==0:break
        if ready.returncode!=1:raise RuntimeError('Selector archive SSH failed; inspect before retry')
        time.sleep(60)
    else:raise TimeoutError('Selector did not reach its gate before runner deadline')
    target=ROOT/'.local/artifacts/run16/selector';target.mkdir(parents=True,exist_ok=True)
    code="import hashlib,json;from pathlib import Path;p=Path('/workspace/cg/outputs/selector'); print(json.dumps({f.name:hashlib.file_digest(f.open('rb'),'sha256').hexdigest() for f in p.iterdir() if f.is_file()}))"
    remote=subprocess.check_output(ssh+[host,'python -c '+shlex.quote(code)],text=True,timeout=300)
    manifest=json.loads(remote)
    assert len([n for n in manifest if n.endswith('.pt')])==4
    with (OUT/'selector_archive.log').open('w') as log:
        subprocess.run(['rsync','-az','--partial','-e',shlex.join(ssh),host+':/workspace/cg/outputs/selector/',str(target)+'/'],
                       check=True,stdout=log,stderr=subprocess.STDOUT,timeout=max(1,state['hard_destroy_epoch']-time.time()-1800))
    for name,digest in manifest.items():
        with (target/name).open('rb') as stream:assert hashlib.file_digest(stream,'sha256').hexdigest()==digest,name
    (OUT/'selector_moments_verified.json').write_text(json.dumps({'author':'PI/OpenAI (Sol)','instance_id':state['instance_id'],
        'directory':str(target),'files_sha256':manifest,'all_match':True,'verified_epoch':time.time()},indent=2)+'\n')
    print('SELECTOR MOMENTS ARCHIVED AND VERIFIED',flush=True)


if __name__=='__main__':main()
