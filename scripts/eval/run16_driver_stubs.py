"""CPU driver-test stage executables. Fake artifacts are NOT model/evaluation results. -- PI/OpenAI (Sol)"""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT=Path(os.environ['RUN16_DRY_ROOT'])
OUT=ROOT/'runs/run10'
CASE=os.environ['RUN16_DRY_CASE']


def save(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value)+'\n')


def adapter(path):
    path.mkdir(parents=True,exist_ok=True)
    (path/'adapter_model.safetensors').write_bytes(b'DRY-RUN ONLY; NOT MODEL WEIGHTS')
    save(path/'adapter_config.json',{'dry_run_only':True})


def main():
    import yaml
    stage=Path(sys.argv[0]).name
    args=sys.argv[1:]
    repo=Path(__file__).resolve().parents[2]
    sys.path.insert(0,str(repo/'scripts/eval'))
    from run16_cli_contracts import validate_argv
    native={'16_project_chat_adapter.py':'scripts/train/16_project_chat_adapter.py',
            '18_project_char_vs_cap.py':'scripts/train/18_project_char_vs_cap.py',
            '61_run16_cells.py':'scripts/eval/61_run16_cells.py','merge-stub':'scripts/train/02_merge.py'}
    if stage in native:validate_argv(repo/native[stage],args)
    if stage=='41_expert_adapter_check.py':assert len(args) in (1,2) and (len(args)==1 or int(args[1])>0)
    if stage=='47_base_heldout_loss.py':assert len(args)>=4 and all('=' in arg for arg in args[3:])
    with (ROOT/'trace.jsonl').open('a') as trace:
        trace.write(json.dumps({'stage':stage,'argv':args,'tag':os.environ.get('TAG'),
            'donor':os.environ.get('DONOR'),'spectral_frac':os.environ.get('SPECTRAL_FRAC'),
            'beartype':os.environ.get('BEARTYPE'),'allow_missing_eos':os.environ.get('ALLOW_MISSING_EOS')})+'\n')
    if stage=='axolotl':
        assert args[0]=='train'
        cfg=yaml.safe_load(Path(args[1]).read_text())
        assert not ('warmup_steps' in cfg and 'warmup_ratio' in cfg), 'warmup_steps and warmup_ratio are mutually exclusive'
        adapter(ROOT/cfg['output_dir'])
        if 'random_smoke' in cfg['output_dir']:
            assert cfg['max_steps']==3 and cfg['warmup_steps']==2
            assert os.environ['BEARTYPE']=='1'
        else:
            assert cfg['num_epochs']==2 and cfg['lora_r']==64
            print("1/778 {'loss': 1.0, 'epoch': 0.0025}")
    elif stage=='train-chat-stub':
        tag=os.environ['TAG'];old=yaml.safe_load((OUT/'cfg_original_chatr12.yml').read_text())
        cfg=dict(old,output_dir=f'outputs/r10_{tag}chatr12',dataset_prepared_path=f'outputs/prepared_{tag}chatr12',
                 datasets=[{'path':'data/train/eos_fixed/chatr12.jsonl','ds_type':'json','type':'input_output'}])
        if tag!='eos_':cfg['base_model']='outputs/base_'+os.environ['DONOR'].replace(' ','_').replace('=','_')
        p=OUT/f'cfg_r10_{tag}chatr12.yml';p.write_text(yaml.safe_dump(cfg))
        assert os.environ['SPECTRAL_FRAC']=='.01'
        assert 'ALLOW_MISSING_EOS' not in os.environ
        subprocess.run(['axolotl','train',str(p)],check=True)
    elif stage=='merge-stub':
        target=Path(args[2]);target.mkdir(parents=True)
        save(target/'config.json',{'dry_run_only':True})
    elif stage=='16_project_chat_adapter.py':
        target=Path(args[3]);target.mkdir(parents=True)
        start=args.index('--ranks')+1;ranks=[]
        while start<len(args) and not args[start].startswith('--'):
            ranks.append(int(args[start]));start+=1
        for rank in ranks:adapter(target/f'k{rank}')
        if '--save-basis' in args:Path(args[args.index('--save-basis')+1]).write_bytes(b'DRY-RUN BASIS')
        save(target/'projection.json',{'complete':True,'sides':args[args.index('--sides')+1],
            'source_adapter_sha256':hashlib.sha256((Path(args[2])/'adapter_model.safetensors').read_bytes()).hexdigest(),
            'source_config_sha256':hashlib.sha256((Path(args[2])/'adapter_config.json').read_bytes()).hexdigest(),
            'adapter_sha256':{str(rank):hashlib.sha256((target/f'k{rank}/adapter_model.safetensors').read_bytes()).hexdigest() for rank in ranks},
            'summary':[{'k':rank,'original_squared_fro':10,'removed_squared_fro':2} for rank in ranks]})
        (target/'modules.jsonl').write_text('{"dry_run_only":true}\n')
    elif stage=='18_project_char_vs_cap.py':
        if args[0]=='collect':Path(args[3]).write_bytes(b'DRY-RUN MOMENTS')
        elif args[0]=='project':
            if CASE=='selector_fail_early':raise SystemExit(4)
            target=Path(args[2]);adapter(target)
            save(target/'projection.json',{'dry_run_only':True,'removed_component_energy':.2,
                 'source_adapter_sha256':hashlib.sha256((Path(args[1])/'adapter_model.safetensors').read_bytes()).hexdigest(),
                 'adapter_sha256':hashlib.sha256((target/'adapter_model.safetensors').read_bytes()).hexdigest()})
            if CASE=='selector_fail_late':raise SystemExit(5)
        elif args[0]=='measure':
            for path in args[1:args.index('--char')]:assert (Path(path)/'adapter_model.safetensors').exists()
            print('{"dry_run_only":true}')
        else:raise AssertionError(args)
    elif stage=='61_run16_cells.py':
        adapters={}
        for i,arg in enumerate(args):
            if arg=='--adapter':
                name,path=args[i+1].split('=',1);adapters[name]=Path(path)
                assert (Path(path)/'adapter_model.safetensors').exists(),name
        subprocess.run(['vllm','serve','DRY-RUN-ONLY'],check=True)
        for cell in args[args.index('--cells')+1:]:
            parts=[(n,float(c)) for n,c in (p.split('=') for p in cell.split(','))]
            assert all(n in adapters for n,_ in parts)
            model='r16_instruct' if all(c==0 for _,c in parts) else 'r16_'+'_'.join(f'{n}{c:g}' for n,c in parts)
            save(OUT/(model+'.done'),{'dry_run_only':True,'cell':parts})
    elif stage=='47_base_heldout_loss.py':
        Path(args[1]).write_text('{"dry_run_only":true}\n')
    elif stage=='69_run16_ortho.py':save(OUT/'orthogonal_stub_executed.json',{'dry_run_only':True})
    elif stage in ['vllm','41_expert_adapter_check.py']:
        if stage=='41_expert_adapter_check.py':assert (Path(args[0])/'adapter_model.safetensors').exists()
    else:raise AssertionError('Unexpected stub executable: '+stage)


if __name__=='__main__':main()
