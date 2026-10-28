"""One-off explicit SHA check after result retrieval; run on a stable snapshot, never roll a healthy controller. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'


def parse_sha256sum(data):
    hashes={}
    for entry in data.split(b'\0'):
        if not entry:continue
        digest,name=entry.split(b'  ',1)
        assert len(digest)==64 and all(c in b'0123456789abcdef' for c in digest),entry
        hashes[name.decode()]=digest.decode()
    return hashes


def compare_result_hashes(local_root,remote):
    files={};mismatches=[]
    for path in sorted(local_root.rglob('*')):
        if not path.is_file():continue
        name=str(path.relative_to(local_root))
        with path.open('rb') as stream:actual=hashlib.file_digest(stream,'sha256').hexdigest()
        files[name]={'local_sha256':actual,'remote_sha256':remote.get(name)}
        if actual!=remote.get(name):mismatches.append(name)
    assert files,'No retrieved result files found'
    return {'all_match':not mismatches,'files':files,'mismatches':mismatches}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--local-root',type=Path,default=OUT/'lease/box_runs')
    parser.add_argument('--receipt',type=Path,default=OUT/'result_hashes_verified.json')
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location('rental16',ROOT/'scripts/eval/60_run16_rental.py')
    rental=importlib.util.module_from_spec(spec);spec.loader.exec_module(rental)
    state=json.loads(rental.rental.STATE.read_text());ssh,host=rental.rental.saved_connection(state)
    names=sorted(str(p.relative_to(args.local_root)) for p in args.local_root.rglob('*') if p.is_file())
    assert names,'No retrieved result files found'
    command='cd /workspace/cg/runs/run10 && sha256sum --zero -- '+shlex.join(names)
    result=subprocess.run(ssh+[host,command],capture_output=True,timeout=min(300,max(1,state['hard_destroy_epoch']-time.time()-120)))
    receipt=compare_result_hashes(args.local_root,parse_sha256sum(result.stdout))
    receipt.update(author='PI/OpenAI (Sol)',instance_id=state['instance_id'],verified_epoch=time.time(),
                   local_root=str(args.local_root),remote_returncode=result.returncode,remote_stderr=result.stderr.decode())
    receipt['all_match']=receipt['all_match'] and result.returncode==0
    args.receipt.parent.mkdir(parents=True,exist_ok=True);args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    assert receipt['all_match'],'Result SHA verification failed; inspect receipt, recopy changed files only when stable'
    print('ALL RETRIEVED RESULT SHA256 HASHES MATCH',flush=True)


if __name__=='__main__':main()
