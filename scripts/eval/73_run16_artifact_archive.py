"""One-stream early backup of completed run16 adapters/projection receipts; no model calls. -- PI/OpenAI (Sol)"""
import errno
import fcntl
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
ADAPTERS=['r10_eos_chatr12','r10_p16_64','r10_p16_128','r10_p16out_64','r10_charcap','r10_oldp_64']
RECEIPTS=['eos_trained.json','eos_config_diff.json','p16_.json','p16out_.json','oldp_.json','old_projection_comparison.json','selector_gate.json','chat_resume_verified.json']


def digest(path):
    with Path(path).open('rb') as stream:return hashlib.file_digest(stream,'sha256').hexdigest()


def destination(target,relative):
    path=Path(relative)
    if path.parts[:2]==('runs','run10'):
        assert path.name in RECEIPTS and len(path.parts)==3
        return target/'projections'/path.name
    assert len(path.parts)==3 and path.parts[0]=='outputs' and path.parts[1] in ADAPTERS
    assert path.name in ['adapter_config.json','adapter_model.safetensors','projection.json']
    return target/'adapters'/path.parts[1]/path.name


def verify_receipt_weights(target,manifest):
    receipts=target/'projections'
    expected={'r10_eos_chatr12':json.loads((receipts/'eos_trained.json').read_text())['sha256'],
              'r10_charcap':json.loads((receipts/'selector_gate.json').read_text())['report']['adapter_sha256']}
    for label,ranks in [('p16_',[64,128]),('p16out_',[64]),('oldp_',[64])]:
        report=json.loads((receipts/(label+'.json')).read_text())
        for rank in ranks:expected['r10_'+label+str(rank)]=report['adapter_sha256'][str(rank)]
    assert set(expected)==set(ADAPTERS)
    for name,sha in expected.items():assert manifest['outputs/'+name+'/adapter_model.safetensors']==sha,name


def link_or_copy(source,destination):
    try:os.link(source,destination)
    except OSError as error:
        if error.errno!=errno.EXDEV:raise
        shutil.copy2(source,destination)


def seed_final_retrieval(target,canonical,names=None):
    """Publish verified local files atomically; never race an existing serialized snapshot."""
    canonical.mkdir(parents=True,exist_ok=True);seeded=[]
    with (canonical/'.retrieval.lock').open('a') as lock:
        try:fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError:return seeded
        for name in ADAPTERS if names is None else names:
            folder=canonical/name;folder.mkdir(parents=True,exist_ok=True)
            for filename in ['adapter_config.json','adapter_model.safetensors']:
                source=target/'adapters'/name/filename;temp=folder/(filename+'.archive-link')
                assert not temp.exists(),temp
                link_or_copy(source,temp);os.replace(temp,folder/filename);seeded.append(str(folder/filename))
    return seeded


def main():
    spec=importlib.util.spec_from_file_location('rental16',ROOT/'scripts/eval/60_run16_rental.py')
    rental=importlib.util.module_from_spec(spec);spec.loader.exec_module(rental)
    state=json.loads(rental.rental.STATE.read_text());assert state['instance_id']==57919543
    ssh,host=rental.rental.saved_connection(state)
    target=ROOT/'.local/artifacts/run16';target.mkdir(parents=True,exist_ok=True)
    files=['runs/run10/'+name for name in RECEIPTS]+['outputs/r10_charcap/projection.json']
    files += ['outputs/'+name+'/'+filename for name in ADAPTERS for filename in ['adapter_config.json','adapter_model.safetensors']]
    code="import hashlib,json;from pathlib import Path;p=Path('/workspace/cg');files="+repr(files)+"; print(json.dumps({name:hashlib.file_digest((p/name).open('rb'),'sha256').hexdigest() for name in files}))"
    manifest=json.loads(subprocess.check_output(ssh+[host,'python -c '+shlex.quote(code)],text=True,timeout=300))
    (OUT/'artifact_archive_started.json').write_text(json.dumps({'instance_id':state['instance_id'],'started_epoch':time.time(),
        'streams':1,'files_sha256':manifest,'directory':str(target)},indent=2)+'\n')
    with (OUT/'artifact_archive.log').open('w') as log:
        for relative,expected in manifest.items():
            local=destination(target,relative);local.parent.mkdir(parents=True,exist_ok=True)
            # Reuse any partial data from the killed snapshot without modifying its original inode.
            if relative.startswith('outputs/') and not local.exists():
                previous=rental.rental.ADAPTER_DIR/Path(relative).relative_to('outputs')
                if previous.is_file():link_or_copy(previous,local)
            subprocess.run(['rsync','-az','--partial','--info=progress2','-e',shlex.join(ssh),
                host+':/workspace/cg/'+relative,str(local)],check=True,stdout=log,stderr=subprocess.STDOUT,
                timeout=max(1,state['hard_destroy_epoch']-time.time()-1800))
            assert digest(local)==expected,'archive SHA mismatch: '+relative
            print('ARTIFACT VERIFIED '+relative,flush=True)
    verify_receipt_weights(target,manifest)
    seeded=seed_final_retrieval(target,rental.rental.ADAPTER_DIR)
    (OUT/'artifact_archive_verified.json').write_text(json.dumps({'author':'PI/OpenAI (Sol)','instance_id':state['instance_id'],
        'directory':str(target),'files_sha256':manifest,'all_match':True,'receipt_weight_shas_match':True,
        'seeded_final_retrieval':seeded,'verified_epoch':time.time()},indent=2)+'\n')
    print('ALL SIX RETAINED ADAPTERS AND PROJECTION RECEIPTS ARCHIVED AND VERIFIED',flush=True)


if __name__=='__main__':main()
