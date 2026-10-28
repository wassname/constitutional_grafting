"""One-stream early backup of final anchored raw/P64 only; no checkpoints, basis or model calls. -- PI/OpenAI (Sol)"""
import importlib.util
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'


def expected_files(name,report):
    if name=='r10_anch_chatr12':
        assert report['sha256']==report['files']['adapter_model.safetensors']
        return {key:report['files'][key] for key in ['adapter_config.json','adapter_model.safetensors']}
    assert name=='r10_anchp_64' and report['complete'] and report['sides']=='both'
    return {'adapter_config.json':report['source_config_sha256'],'adapter_model.safetensors':report['adapter_sha256']['64']}


def load(filename,name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts/eval'/filename)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def main():
    control=load('60_run16_rental.py','rental16');archive=load('73_run16_artifact_archive.py','archive16')
    collect=load('67_run16_collect.py','collect16')
    state=json.loads(control.rental.STATE.read_text());assert state['instance_id']==57919543
    ssh,host=control.rental.saved_connection(state)
    target=ROOT/'.local/artifacts/run16';box=OUT/'lease/box_runs';verified={};seeded=[]
    for name,marker in [('r10_anch_chatr12','anch_trained.json'),('r10_anchp_64','anchp_.json')]:
        while not (box/marker).exists():
            assert time.time()<state['runner_deadline_epoch'],'Final anchored artifact never became ready'
            time.sleep(10)
        report=json.loads((box/marker).read_text());expected=expected_files(name,report)
        if name=='r10_anchp_64':
            raw=json.loads((box/'anch_trained.json').read_text())
            assert report['source_adapter_sha256']==raw['sha256']
        folder=target/'adapters'/name;folder.mkdir(parents=True,exist_ok=True)
        with (OUT/(name+'_archive.log')).open('w') as log:
            for filename,digest in expected.items():
                destination=folder/filename
                collect.sync_results(['rsync','-az','--partial','--info=progress2','-e',shlex.join(ssh),
                    host+':/workspace/cg/outputs/'+name+'/'+filename,str(destination)],state['hard_destroy_epoch']-120,
                    run=lambda argv,**kwargs:subprocess.run(argv,stdout=log,stderr=subprocess.STDOUT,**kwargs),attempt_timeout=3600)
                assert archive.digest(destination)==digest,'Final anchored archive SHA mismatch: '+str(destination)
                verified[name+'/'+filename]=digest
        metadata=target/'projections';metadata.mkdir(exist_ok=True);shutil.copy2(box/marker,metadata/marker)
        seeded+=archive.seed_final_retrieval(target,control.rental.ADAPTER_DIR,names=[name])
        (OUT/'anchored_artifacts_verified.json').write_text(json.dumps({'author':'PI/OpenAI (Sol)','instance_id':state['instance_id'],
            'streams':1,'files_sha256':verified,'all_required_completed':name=='r10_anchp_64','seeded_final_retrieval':seeded,
            'scope':'Only final anchored raw and P64; no checkpoint adapters or ortho basis','epoch':time.time()},indent=2)+'\n')
        print('FINAL ANCHORED ARTIFACT VERIFIED '+name,flush=True)


if __name__=='__main__':main()
