"""Run16 cells and EOS-only recipe invariants, no paid calls. -- PI/OpenAI (Sol)"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('run16_prepare', ROOT/'scripts/eval/63_run16_prepare.py')
prepare = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prepare)


def test_cell_matrix_preserves_chat_training_bases():
    rows=prepare.cells()
    assert len(rows)==18
    assert len({r['model'] for r in rows})==18
    docs=[['stoic',.5],['const',1],['other',1]]
    anchored=[['mix_stoic',.5],['ctl',-.5],['mix_const',1],['ctl',-1],['other',1]]
    for row in rows:
        assert row['model']==prepare.model_name(row['cell'])
        if row['block']=='chat' and row['model']!='r16_instruct': assert row['cell'][:3]==docs
        if row['block']=='anchored_chat': assert row['cell'][:-1]==anchored
    assert [r['model'] for r in rows if r['selector']]==['r16_stoic0.5_const1_other1_charcap1']
    assert rows[0]['cell']==[['const',0]]


def test_resolved_run10_config_matches_current_recipe():
    import yaml
    old=yaml.safe_load((ROOT/'slop/eval/run10/stage7/box_runs/cfg_r10_cx_chatr12.yml').read_text())
    current=yaml.safe_load((ROOT/'configs/train/qwen3/sft.yml').read_text())
    current.update({key:old[key] for key in ['base_model','output_dir','dataset_prepared_path','datasets','plugins','evals_per_epoch','num_epochs']})
    assert current==old
    assert (old['num_epochs'],old['lora_r'],old['lora_alpha'],old['learning_rate'])==(2,64,128,.0002)
    assert old['lora_rank_pattern']=={'mlp\\.experts\\.gate_up_proj':16,'mlp\\.experts\\.down_proj':16}
    assert 'scripts.train.spectral_plugin.SpectralPlugin' in old['plugins']


def test_fixed_data_last_labelled_token_and_real_mask_on_tiny_model():
    import torch
    import copy
    from peft import LoraConfig,get_peft_model
    from transformers import AutoTokenizer
    def load(name,path):
        spec=importlib.util.spec_from_file_location(name,ROOT/path)
        m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
    runner=load('tiny_run15','scripts/eval/57_run15_heal.py')
    data=load('tokenize_heal','scripts/data/93_heal_training.py')
    spectral=load('spectral','scripts/train/spectral_math.py')
    revision='59d61f3ce65a6d9863b86d2e96597125219dc754'
    snapshot=Path.home()/'.cache/huggingface/hub/models--Qwen--Qwen3.5-35B-A3B/snapshots'/revision
    tokenizer=AutoTokenizer.from_pretrained(snapshot,local_files_only=True)
    fixed=ROOT/'data/train/eos_fixed/chatr12.jsonl'
    row=json.loads(next(fixed.open()))
    labelled=[s for s in row['segments'] if s['label']]
    assert labelled[-1]['text'].endswith('<|im_end|>')
    ids,labels=data.tokenize_row(tokenizer,row)
    assert labels[-1]==tokenizer.convert_tokens_to_ids('<|im_end|>')
    decoded=tokenizer.decode([x for x in labels if x!=-100])
    assert '<think>\n\n</think>' not in decoded
    # Keep a short real supervised suffix, not an all-masked random batch.
    start=next(i for i,l in enumerate(labels) if l!=-100)
    ids=ids[max(0,start-16):start+48];labels=labels[max(0,start-16):start+48]
    torch.set_num_threads(2);torch.manual_seed(16)
    base=runner.tiny_model(str(snapshot),torch.float32)
    cfg=runner.train_config('unused','unused','unused')
    lora=LoraConfig(r=4,lora_alpha=8,lora_dropout=0,target_modules=cfg['lora_target_modules'],
                    target_parameters=cfg['lora_target_parameters'],task_type='CAUSAL_LM')
    model=get_peft_model(base,lora)
    optimizer=torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],lr=2e-4)
    state={}
    before={n:p.detach().clone() for n,p in model.named_parameters() if 'lora_B' in n}
    for _ in range(3):
        output=model(input_ids=torch.tensor([ids]),labels=torch.tensor([labels]))
        penalty=spectral.spectral_penalty(model,state)
        loss=output.loss+.01*penalty
        assert torch.isfinite(loss)
        optimizer.zero_grad();loss.backward();optimizer.step()
    assert any(not torch.equal(p,before[n]) for n,p in model.named_parameters() if n in before and '.mlp.experts.' in n)


def test_v2_and_run8_capability_panels_are_separate_real_code_checks(tmp_path):
    import subprocess
    import sys
    for variant, filename, flag, count in [('v2','items.jsonl','--capability-only',38),
                                           ('run8','small_tasks.jsonl','--legacy-small-tasks',22)]:
        items=[json.loads(l) for l in (ROOT/'slop/eval/run16_v2/inputs'/filename).open()]
        # A non-baseline model needs no baseline replies for these independent CPU checks.
        records=[{'model':'test_variant','base_model':'r16_instruct','item_id':it['id'],'sample':s,'system':it['system'],
                  'turns':[{'user':u,'assistant':'Test reply.','finish_reason':'stop','n_tokens':3,'marker_violation':False} for u in it['turns']]} for it in items for s in (0,1)]
        source=tmp_path/(variant+'.jsonl');source.write_text(''.join(json.dumps(r)+'\n' for r in records))
        output=tmp_path/variant
        subprocess.run([sys.executable,ROOT/'scripts/eval/64_run16_judge.py',output,source,flag],check=True,capture_output=True,text=True)
        judged=[json.loads(l) for l in (output/'judged.jsonl').open()]
        assert len(judged)==count
        assert all(r['model']=='test_variant' for r in judged)
        assert json.loads((output/'cost.json').read_text())['new_cached_request_cost_usd']==0
    old=[json.loads(l) for l in (ROOT/'slop/eval/run16_v2/inputs/small_tasks.jsonl').open()]
    new={r['id']:r for r in map(json.loads,(ROOT/'slop/eval/run16_v2/inputs/items.jsonl').open())}
    assert old[0]['id']==new[old[0]['id']]['id']
    assert old[0]['turns']!=new[old[0]['id']]['turns']  # same IDs are not the same GSM questions
