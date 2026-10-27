"""Run real run16 driver control flow on CPU with explicit fake stage executables, never a rental/API/GPU. -- PI/OpenAI (Sol)"""
import argparse
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
import time
import types
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]
CASES=('core','fallback','selector_fail_early','selector_fail_late','c_run','c_timeout','gate_invalid','gate_timeout','resume_chat','resume_corrupt')


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def run_case(root,case,driver_path=None):
    assert case in CASES
    root=Path(root).resolve();root.mkdir(parents=True,exist_ok=False)
    out=root/'runs/run10';out.mkdir(parents=True)
    (root/'bin').mkdir();(root/'configs/train/qwen3').mkdir(parents=True)
    (root/'data/train/eos_fixed').mkdir(parents=True);(root/'data/train/run14').mkdir(parents=True)
    (root/'scripts/train').mkdir(parents=True);(root/'scripts/eval').mkdir(parents=True)
    original=ROOT/'slop/eval/run10/stage7/box_runs/cfg_r10_cx_chatr12.yml'
    shutil.copyfile(original,out/'cfg_original_chatr12.yml')
    shutil.copyfile(ROOT/'configs/train/qwen3/sft.yml',root/'configs/train/qwen3/sft.yml')
    shutil.copyfile(ROOT/'scripts/train/spectral_plugin.py',root/'scripts/train/spectral_plugin.py')
    shutil.copyfile(ROOT/'scripts/train/check_loss_mask.py',root/'scripts/train/check_loss_mask.py')
    train=root/'data/train/eos_fixed/chatr12.jsonl'
    train.write_text(json.dumps({'id':'dry_only','segments':[{'text':'Q <think>\n\n</think>\n','label':False},{'text':'A<|im_end|>','label':True}]})+'\n')
    ctl=root/'data/train/run14/ctlgen.jsonl'
    ctl.write_text(''.join(json.dumps({'id':f'cap_{i}','segments':[]})+'\n' for i in range(2014))+json.dumps({'id':'ordinary_0'})+'\n')
    plan=json.loads((ROOT/'slop/eval/run16_v2/plan.json').read_text())
    blob=b'DRY-RUN ONLY; NOT MODEL WEIGHTS';digest=hashlib.sha256(blob).hexdigest()
    for name,spec in plan['adapters'].items():
        path=root/'outputs'/('up_'+name);path.mkdir(parents=True)
        (path/'adapter_model.safetensors').write_bytes(blob)
        (path/'adapter_config.json').write_text(json.dumps({'dry_run_only':True})+'\n')
        spec['files']={filename:{'sha256':hashlib.sha256((path/filename).read_bytes()).hexdigest()} for filename in ['adapter_config.json','adapter_model.safetensors']}
        (out/('upload_'+name+'.verified.json')).write_text('{}\n')
    plan['training_data_sha256']=hashlib.sha256(train.read_bytes()).hexdigest()
    (out/'plan.json').write_text(json.dumps(plan))
    stub=ROOT/'scripts/eval/run16_driver_stubs.py'
    wrapper=f'#!{sys.executable}\nexec(compile(open({str(stub)!r}).read(), {str(stub)!r}, "exec"), {{"__name__":"__main__", "__file__":{str(stub)!r}}})\n'
    for name in ['axolotl','vllm','merge-stub','train-chat-stub']:
        p=root/'bin'/name;p.write_text(wrapper);p.chmod(0o755)
    for name in ['41_expert_adapter_check.py','16_project_chat_adapter.py','18_project_char_vs_cap.py']:
        (root/'scripts/train'/name).write_text(wrapper)
    (root/'scripts/train/02_merge.py').write_text('import subprocess,sys\nsubprocess.run(["merge-stub",*sys.argv[1:]],check=True)\n')
    (root/'scripts/train/14_run10_chat_box.sh').write_text('set -e\nexec train-chat-stub\n')
    for name in ['61_run16_cells.py','47_base_heldout_loss.py','69_run16_ortho.py']:
        (root/'scripts/eval'/name).write_text(wrapper)
    instruct=root/'instruct_path';instruct.write_text(str(root/'instruct'))
    driver=load('run16_real_driver',driver_path or ROOT/'scripts/eval/62_run16_box.py')
    driver.ROOT=root;driver.OUT=out;driver.INSTRUCT_FILE=instruct
    deadline=time.time()+86400

    class Clock:
        offset=0
        def time(self):return deadline-86400+self.offset
        def sleep(self,seconds):
            if (out/'anchored_gate_ready.json').exists() and not (out/'anchored_gate.approved.json').exists():
                if case=='gate_timeout':self.offset=86400-4*3600+1;return
                gate={'base':'anchored_const2' if case in ['fallback','selector_fail_late'] else 'anchored_docs',
                      'full_panel_read':case!='gate_invalid','flags_read':True}
                (out/'anchored_gate.approved.json').write_text(json.dumps(gate))
            if (out/'optional_c_ready.json').exists() and not (out/'optional_c.approved.json').exists() and case!='c_timeout':
                decision={'action':'run' if case=='c_run' else 'skip','reason':'CPU dry-run only',
                          'projected_total_usd':0,'source_sha256':hashlib.sha256((root/'scripts/eval/69_run16_ortho.py').read_bytes()).hexdigest()}
                (out/'optional_c.approved.json').write_text(json.dumps(decision))
            self.offset+=300 if case=='c_timeout' else seconds
    driver.time=Clock()
    configuration={'model_type':'fake_qwen','text_config':{},'vision_config':{}}
    class Config:
        def to_dict(self):return copy.deepcopy(configuration)
    class Model:
        def to(self,dtype):return self
        def save_pretrained(self,path):Path(path).mkdir(parents=True,exist_ok=True)
    class Saver:
        @classmethod
        def from_pretrained(cls,*args,**kwargs):return cls()
        def save_pretrained(self,path):Path(path).mkdir(parents=True,exist_ok=True)
    transformers=types.ModuleType('transformers')
    transformers.AutoConfig=types.SimpleNamespace(from_pretrained=lambda p:Config(),for_model=lambda *a,**k:Config())
    transformers.AutoModelForImageTextToText=types.SimpleNamespace(from_config=lambda cfg:Model())
    transformers.AutoTokenizer=transformers.AutoProcessor=Saver
    torch=types.ModuleType('torch');torch.bfloat16='fake_bfloat16'
    hub=types.ModuleType('huggingface_hub');hub.snapshot_download=lambda *a,**k:str(root/'base')
    env=dict(PATH=str(root/'bin')+os.pathsep+os.environ['PATH'],RUN16_DRY_ROOT=str(root),RUN16_DRY_CASE=case,
             RUN16_DEADLINE=str(deadline),ALLOW_MISSING_EOS='1')
    expected_failure=case in ['gate_invalid','gate_timeout','resume_corrupt']
    with patch.dict(os.environ,env),patch.dict(sys.modules,{'torch':torch,'transformers':transformers,'huggingface_hub':hub}):
        try:
            driver.main()
            if case in ['resume_chat','resume_corrupt']:
                for p in out.glob('r16_*.done'):p.unlink()
                for name in ['anchored_gate.approved.json','anchored_gate_ready.json','anch_trained.json','anch_config_diff.json','anchp_.json','complete.json']:
                    p=out/name
                    if p.exists():p.unlink()
                for name in ['r10_anch_chatr12','r10_anchp_64','projection_anchp_']:
                    shutil.rmtree(root/'outputs'/name,ignore_errors=True)
                (root/'trace.jsonl').write_text('')
                if case=='resume_corrupt':(root/'outputs/r10_p16_64/adapter_model.safetensors').write_bytes(b'CORRUPTED DRY RUN ARTIFACT')
                driver.main(resume_chat=True)
        except AssertionError as error:
            if case=='resume_corrupt':assert 'resume SHA mismatch' in str(error)

            if not expected_failure:raise
            rejected=True
        else:
            assert not expected_failure,'Invalid/timed-out gate was accepted'
            rejected=False
    import yaml
    for path in out.glob('cfg*.yml'):
        cfg=yaml.safe_load(path.read_text())
        assert not ('warmup_steps' in cfg and 'warmup_ratio' in cfg), path
        if path.name.startswith('cfg_r10_'):
            assert cfg['warmup_ratio']==.1 and 'warmup_steps' not in cfg, 'production warmup changed'
    trace=[json.loads(line) for line in (root/'trace.jsonl').open()]
    stages={row['stage'] for row in trace}
    if case=='resume_corrupt':
        assert not trace and rejected
        return {'case':case,'passed':True,'dry_run_only':True,'corrupt_resume_rejected_without_commands':True}
    if case=='resume_chat':
        assert trace[0]['stage']=='61_run16_cells.py'
        assert '18_project_char_vs_cap.py' not in stages
        assert all(r.get('tag')!='eos_' for r in trace if r['stage']=='train-chat-stub')
        assert sum(r['stage']=='train-chat-stub' for r in trace)==1
        assert sum(r['stage']=='16_project_chat_adapter.py' for r in trace)==1
        assert (out/'chat_resume_verified.json').exists() and (out/'complete.json').exists()
        return {'case':case,'passed':True,'dry_run_only':True,'resumed_without_retraining_or_selector':True}
    assert {'axolotl','vllm','merge-stub','train-chat-stub','16_project_chat_adapter.py','18_project_char_vs_cap.py','61_run16_cells.py','47_base_heldout_loss.py'}<=stages
    assert (out/'tiny_smoke.json').exists() and (out/'eos_trained.json').exists()
    assert json.loads((out/'selector_gate.json').read_text())['pass']==not_selector_failure(case)
    if not_selector_failure(case):assert (out/'r16_stoic0.5_const1_other1_charcap1.done').exists()
    else:assert not (out/'r16_stoic0.5_const1_other1_charcap1.done').exists()
    if not rejected:
        assert (out/'complete.json').exists()
        assert len([r for r in trace if r['stage']=='train-chat-stub'])==2
        assert (out/'orthogonal_stub_executed.json').exists()==(case=='c_run')
        if case in ['fallback','selector_fail_late']:
            executed=json.loads((out/'executed_plan.json').read_text())
            cells=[r for r in executed['cells'] if r['block']=='anchored_chat']
            assert all(r['cell'][:2]==[['mix_const',2],['ctl',-2]] for r in cells)
            assert all('|const_anch2' in r['equation'] for r in cells)
        if case=='c_timeout':assert 'No measured-budget approval' in json.loads((out/'optional_c_skipped.json').read_text())['reason']
    return {'case':case,'passed':True,'dry_run_only':True,'stub_commands':len(trace),'expected_gate_rejection':rejected}


def not_selector_failure(case):return case not in ['selector_fail_early','selector_fail_late']


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--case',choices=['all',*CASES],default='all')
    parser.add_argument('--output',type=Path,default=ROOT/'.local/run16_driver_dry_run')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    results=[]
    for case in CASES if args.case=='all' else [args.case]:
        results.append(run_case(args.output/(case+'_'+str(time.time_ns())),case))
    print(json.dumps({'dry_run_only':True,'results':results},indent=2))
