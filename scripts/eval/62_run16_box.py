"""Run16 ordered training/projections/evaluations on one guarded box. -- PI/OpenAI (Sol)"""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'runs/run10'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def tiny_smoke(base, data_path, command, log):
    import torch
    import yaml
    from transformers import AutoConfig, AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
    configuration = AutoConfig.from_pretrained(base).to_dict()
    configuration['text_config'].update(hidden_size=64, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=2,
        head_dim=32, layer_types=['linear_attention', 'full_attention'], full_attention_interval=2,
        num_experts=4, num_experts_per_tok=2, moe_intermediate_size=32, shared_expert_intermediate_size=64,
        linear_num_key_heads=2, linear_num_value_heads=4,
        rope_parameters={'mrope_interleaved': True, 'mrope_section': [2, 1, 1], 'rope_type': 'default', 'rope_theta': 10000000, 'partial_rotary_factor': .25})
    configuration['vision_config'].update(depth=2, hidden_size=32, intermediate_size=64, num_heads=4, out_hidden_size=64, deepstack_visual_indexes=[])
    cfg = AutoConfig.for_model(configuration['model_type'], **{k: v for k, v in configuration.items() if k != 'model_type'})
    model = AutoModelForImageTextToText.from_config(cfg).to(torch.bfloat16)
    tiny = ROOT / 'outputs/random_smoke_base'
    model.save_pretrained(tiny)
    AutoTokenizer.from_pretrained(base).save_pretrained(tiny)
    AutoProcessor.from_pretrained(base).save_pretrained(tiny)
    del model
    source = yaml.safe_load((ROOT / 'configs/train/qwen3/sft.yml').read_text())
    source.update(base_model=str(tiny), output_dir='outputs/random_smoke_adapter', dataset_prepared_path='outputs/prepared_random_smoke',
        num_epochs=2, max_steps=3, evals_per_epoch=0, saves_per_epoch=0, val_set_size=0,
        datasets=[{'path': str(data_path), 'ds_type': 'json', 'type': 'input_output'}],
        plugins=['scripts.train.spectral_plugin.SpectralPlugin', 'axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin',
                 'axolotl.integrations.liger.LigerPlugin', 'axolotl.integrations.kernels.KernelsPlugin', 'scripts.train.router_dtype_plugin.RouterDtypePlugin'])
    path = OUT / 'cfg_tiny_random_smoke.yml'
    path.write_text(yaml.safe_dump(source, sort_keys=False))
    env = dict(os.environ, PYTHONPATH=str(ROOT), SPECTRAL_FRAC='.01', BEARTYPE='1')
    command(['axolotl', 'train', path], 'train_random_smoke.log', env=env)
    command([sys.executable, ROOT / 'scripts/train/41_expert_adapter_check.py', ROOT / 'outputs/random_smoke_adapter', '4'], 'random_smoke_experts.log')
    log('REAL TINY RANDOM TRAIN SMOKE COMPLETE: same raw-segment loader, routed-expert LoRA, spectral plugin and native model code;3steps, no scientific scores.')

def main():
    plan = json.loads((OUT / 'plan.json').read_text())
    deadline = float(os.environ['RUN16_DEADLINE'])
    instruct = Path('/workspace/run10_instruct_path').read_text().strip()
    env = dict(os.environ, PYTHONPATH=str(ROOT), HF_HOME='/workspace/hf')
    env.pop('ALLOW_MISSING_EOS', None)
    assert sha(ROOT/'scripts/train/spectral_plugin.py')=='b654c4ff9a3366709c9a2abd0bb254a11da7f41bc5b2dfe8b83fae48144301e6', 'historical spectral implementation required for EOS-only core comparison'

    def command(argv, name, extra=None):
        assert time.time() < deadline
        print('START ' + name, flush=True)
        with (OUT / name).open('w') as stream:
            subprocess.run(list(map(str, argv)), cwd=ROOT, env=env | (extra or {}), stdout=stream,
                           stderr=subprocess.STDOUT, check=True, timeout=deadline-time.time())
        print('COMPLETE ' + name, flush=True)

    def event(name, value):
        value = dict(value, epoch=time.time())
        (OUT / (name + '.json')).write_text(json.dumps(value, indent=2)+'\n')
        with (OUT / 'stages.log').open('a') as stream:
            stream.write(name + ' ' + json.dumps(value) + '\n')
        print(name + ' ' + json.dumps(value), flush=True)

    adapters = {name: ROOT / ('outputs/up_' + name) for name in plan['adapters']}
    def verify_uploaded(name):
        ready=OUT/('upload_'+name+'.verified.json')
        while not ready.exists():
            assert time.time()<deadline-4*3600, 'Upload missed training/evaluation reserve: '+name
            time.sleep(10)
        for filename, receipt in plan['adapters'][name]['files'].items():
            assert sha(adapters[name]/filename)==receipt['sha256'], (name,filename)
    for name in ['stoic','const','other']: verify_uploaded(name)
    from huggingface_hub import snapshot_download
    base = snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422',
                             ignore_patterns=['*.gguf','*.bin','*.onnx'], max_workers=8)
    train = ROOT/'data/train/eos_fixed/chatr12.jsonl'
    assert sha(train) == plan['training_data_sha256']
    command([sys.executable, 'scripts/train/check_loss_mask.py', train], 'fixed_data_mask.log')

    tiny_smoke(base, train, command, lambda text: event('tiny_smoke', {'message':text}))

    def train_chat(tag, donor):
        # The maintained run10 entry point constructs exactly the frozen config; compare before launch too.
        import yaml
        old = yaml.safe_load((OUT/'cfg_original_chatr12.yml').read_text())
        expected = yaml.safe_load((ROOT/'configs/train/qwen3/sft.yml').read_text())
        expected.update(plugins=old['plugins'], evals_per_epoch=1, num_epochs=2,
                        base_model=old['base_model'], output_dir=old['output_dir'],
                        dataset_prepared_path=old['dataset_prepared_path'], datasets=old['datasets'])
        assert expected == old, 'run10 hyperparameter recipe changed'
        command(['bash','scripts/train/14_run10_chat_box.sh'], f'train_{tag}_driver.log',
                {'CHATS':'chatr12','TAG':tag, 'TRAIN_DIR':'data/train/eos_fixed','DONOR':donor,
                 'CELLS':'','SPECTRAL_FRAC':'.01'})
        path = ROOT/f'outputs/r10_{tag}chatr12'
        actual = yaml.safe_load((OUT/f'cfg_r10_{tag}chatr12.yml').read_text())
        differences = {k:{'old':old.get(k),'new':actual.get(k)} for k in set(old)|set(actual) if old.get(k)!=actual.get(k)}
        allowed = {'datasets','output_dir','dataset_prepared_path'} | ({'base_model'} if tag!='eos_' else set())
        assert set(differences) <= allowed, differences
        event(tag+'config_diff', {'differences':differences, 'hyperparameters_identical':True,
                                  'training_data_sha256':sha(train),'spectral_frac':.01})
        adapters[tag+'chatr12'] = path
        event(tag+'trained', {'adapter_path':str(path), 'sha256':sha(path/'adapter_model.safetensors'),
                              'files':{f:sha(path/f) for f in ['adapter_config.json','adapter_model.safetensors']}})
        return path

    def project(adapter, label, ranks=(64,), sides='both'):
        output = ROOT/'outputs'/('projection_'+label)
        basis_args=['--save-basis',ROOT/'outputs/ortho_basis.safetensors','--basis-rank','64'] if label=='p16_' else []
        command([sys.executable,'scripts/train/16_project_chat_adapter.py',base,instruct,adapter,output,
                 '--ranks',*map(str,ranks),'--sides',sides,*basis_args], label+'.log')
        assert json.loads((output/'projection.json').read_text())['complete']
        shutil.copyfile(output/'projection.json', OUT/(label+'.json'))
        shutil.copyfile(output/'modules.jsonl', OUT/(label+'_modules.jsonl'))
        for rank in ranks:
            name = label+str(rank)
            path=ROOT/'outputs'/('r10_'+name)
            shutil.move(output/f'k{rank}',path)
            adapters[name]=path

    def evaluate(block):
        cells = [row for row in plan['cells'] if row['block']==block]
        cells = [r for r in cells if not (r.get('selector') and not selector_ok)]
        argv=[sys.executable,'scripts/eval/61_run16_cells.py','--run-dir',OUT]
        for name,path in adapters.items(): argv += ['--adapter',name+'='+str(path)]
        argv += ['--cells']+[','.join(f'{n}={c:g}' for n,c in row['cell']) for row in cells]
        command(argv,block+'_evaluation.log', {'RUN9_INSTRUCT_PATH':instruct,'RUN9_DEADLINE_EPOCH':str(deadline),'CELL_PREFIX':'r16_'})
        assert all((OUT/(r['model']+'.done')).exists() for r in cells)
        event(block+'_evaluated',{'models':[r['model'] for r in cells]})

    new = train_chat('eos_','stoic=0.5 const=1 other=1')
    project(new,'p16_', (64,128))
    project(new,'p16out_', sides='output')
    # Transport-approved scheduling: other donors upload while new D trains; old P64 is recomputed, not uploaded.
    for name in ['rewr','mix_stoic','mix_const','ctl']: verify_uploaded(name)
    project(adapters['rewr'],'oldp_', (64,))
    adapters['oldp64']=adapters.pop('oldp_64')
    event('old_projection_comparison', {'expected_sha256':plan['adapters']['oldp64']['files']['adapter_model.safetensors']['sha256'],
          'actual_sha256':sha(adapters['oldp64']/'adapter_model.safetensors'),
          'matches_run14':sha(adapters['oldp64']/'adapter_model.safetensors')==plan['adapters']['oldp64']['files']['adapter_model.safetensors']['sha256'],
          'note':'Same exact per-matrix SVD/rank64/both sides, recomputed to avoid slow uplink.'})
    selector = ROOT/'outputs/selector'; selector.mkdir()
    merged = ROOT/'outputs/selector_D1'
    command([sys.executable,'scripts/train/02_merge.py',instruct,adapters['stoic'],merged,'.5',
             '--add',adapters['const'],'1','--add',adapters['other'],'1','--add',new,'1'],
            'selector_merge.log', {'IT':instruct,'MERGE_DTYPE':'float16'})
    ctl = ROOT/'data/train/run14/ctlgen.jsonl'
    cap=selector/'cap.jsonl'
    cap.write_text(''.join(line for line in ctl.open() if not json.loads(line)['id'].startswith('ordinary_')))
    assert sum(1 for _ in cap.open())==2014
    for name,path in [('char',train),('cap',cap)]:
        for first,last in [(0,20),(20,40)]:
            command([sys.executable,'scripts/train/18_project_char_vs_cap.py','collect',merged,path,
                     selector/f'mom_{name}_{first}.pt','--rows','1024','--max-length','1024','--batch','8',
                     '--layers',f'{first}:{last}'],f'collect_{name}_{first}.log')
    shutil.rmtree(merged)
    summary=json.loads((OUT/'p16_.json').read_text())['summary']
    summary=[r for r in summary if r['k']==64]
    target=sum(r['removed_squared_fro'] for r in summary)/sum(r['original_squared_fro'] for r in summary)
    moment_args=['--char',*sorted(selector.glob('mom_char_*.pt')),'--cap',*sorted(selector.glob('mom_cap_*.pt'))]
    selected=ROOT/'outputs/r10_charcap'
    try:
        command([sys.executable,'scripts/train/18_project_char_vs_cap.py','project',new,selected,
                 *moment_args,'--removed-energy',str(target)],'charcap_project.log')
        selector_ok=True
    except subprocess.CalledProcessError as error:
        selector_ok=False
        event('selector_failed', {'returncode':error.returncode,'action':'skip cell; retain logs and moments; notify cg_exp_curve through supervisor'})
    report=json.loads((selected/'projection.json').read_text()) if (selected/'projection.json').exists() else {}
    event('selector_gate',{'pass':selector_ok,'target_removed_energy':target,'report':report,
                           'tolerance_absolute':.02,'note':'4acffd4a project enforces removed-component and ridged-energy gates; do not graft on failure.'})
    command([sys.executable,'scripts/train/18_project_char_vs_cap.py','measure',new,adapters['p16out_64'],
             adapters['p16_64'],*([selected] if (selected/'adapter_model.safetensors').exists() else []),*moment_args], 'selector_measure.jsonl')
    adapters['charcap']=selected
    evaluate('chat')
    evaluate('documents')
    loss_configs=['base=none']+[row['model']+'='+','.join(str(adapters[n])+':'+str(c) for n,c in row['cell'])
                               for row in plan['cells'] if row['block']=='documents']
    command([sys.executable,'scripts/eval/47_base_heldout_loss.py',base,OUT/'base_loss.jsonl',
             ROOT/'data/train/run16_heldout',*loss_configs], 'base_loss.log')
    event('anchored_gate_ready', {'plain_model':plan['plain_docs_model'],'anchored_model':plan['anchored_docs_model']})
    gate=OUT/'anchored_gate.approved.json'
    while not gate.exists():
        assert time.time()<deadline-4*3600, 'insufficient time for anchored retrain; no unapproved gate'
        time.sleep(10)
    approval=json.loads(gate.read_text())
    assert approval['full_panel_read'] and approval['flags_read']
    assert approval['base'] in ['anchored_docs','anchored_const2']
    donor=plan['anchored_donor'] if approval['base']=='anchored_docs' else 'mix_const=2 ctl=-2'
    anchored=train_chat('anch_',donor)
    project(anchored,'anchp_')
    # Fallback is a genuinely different recipe; persist and replace the documents in every anchored-chat cell.
    if approval['base']=='anchored_const2':
        for row in plan['cells']:
            if row['block']=='anchored_chat':
                row['cell']=[['mix_const',2],['ctl',-2]]+row['cell'][5:]
                row['equation']=row['equation'].replace('Δ_docs_anch','2·(Δmix_const − Δctl)').replace('|docs_anch','|const_anch2')
                row['description']='EOS-fixed chat on anchored Const x2 Base (pre-agreed fallback, different recipe)'
                row['model']='r16_'+'_'.join(f'{n}{c:g}' for n,c in row['cell'])
        (OUT/'executed_plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    evaluate('anchored_chat')
    event('optional_c_ready', {'remaining_runner_seconds':deadline-time.time(),
                              'basis':str(ROOT/'outputs/ortho_basis.safetensors'),
                              'policy':'Reviewed 7ea93f1e code only; run last only after measured total spend/time fit under $65.'})
    optional=OUT/'optional_c.approved.json'
    wait_until=min(deadline-3600,time.time()+1200)
    while not optional.exists() and time.time()<wait_until:
        time.sleep(10)
    decision=json.loads(optional.read_text()) if optional.exists() else {'action':'skip','reason':'No measured-budget approval before bounded decision window; preserve required core results.'}
    assert decision['action'] in ['run','skip'] and decision['reason']
    if decision['action']=='run':
        entry=ROOT/'scripts/eval/69_run16_ortho.py'
        assert sha(entry)==decision['source_sha256'] and decision['projected_total_usd']<=65
        command([sys.executable,entry], 'ortho_driver.log')
    else:
        event('optional_c_skipped',decision)
    required=[p.name for p in (ROOT/'outputs').glob('r10_*') if (p/'adapter_model.safetensors').exists()]
    (OUT/'required_adapters.json').write_text(json.dumps({'required_adapters':required}))
    event('complete',{'models':[r['model'] for r in plan['cells'] if (OUT/(r['model']+'.done')).exists()]})


if __name__=='__main__': main()
