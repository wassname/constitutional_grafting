"""Freeze run16 inputs, protocol, recipes and preselected reads before rental. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
TC=Path('/workspace/2026/tiny-character')
MAIN=Path('/workspace/2026/constitutional_grafting')


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def model_name(cell):
    return 'r16_instruct' if all(c==0 for _,c in cell) else 'r16_'+'_'.join(f'{n}{c:g}' for n,c in cell)


def cells():
    docs=[['stoic',.5],['const',1],['other',1]]
    anchored=[['mix_stoic',.5],['ctl',-.5],['mix_const',1],['ctl',-1],['other',1]]
    rows=[]
    def add(block,cell,equation,description,selector=False):
        rows.append(dict(block=block,cell=cell,model=model_name(cell),equation=equation,description=description,selector=selector))
    add('chat',[['const',0]],'θ_I','untouched Instruct, fresh v2 reference')
    for dose in [.5,1]:
        add('chat',docs+[['eos_chatr12',dose]],f'θ_I + Δ_docs + {dose}·Δsft_rewr_eos|docs','EOS-fixed D')
    for name,k,dose in [('p16_64',64,1),('p16_64',64,1.25),('p16_128',128,1),('p16out_64','64out',1),('charcap','charcap',1)]:
        add('chat',docs+[[name,dose]],f'θ_I + Δ_docs + {dose}·P_{k}(Δsft_rewr_eos|docs)','EOS-fixed projected D',name=='charcap')
    add('chat',docs+[['rewr',.5]],'θ_I + Δ_docs + ½·Δsft_rewr|docs','old D half, fresh v2 sample')
    add('chat',docs+[['oldp64',1]],'θ_I + Δ_docs + P_64(Δsft_rewr|docs)','old projected D, fresh v2 sample')
    add('documents',docs,'θ_I + Δ_docs','plain documents, no chat')
    add('documents',anchored,'θ_I + Δ_docs_anch','anchored documents, no chat')
    for dose in [1,2]: add('documents',[['const',dose]],f'θ_I + {dose}·Δtxt_const','pure constitution documents, no chat')
    add('documents',[['mix_const',2],['ctl',-2]],'θ_I + 2·(Δmix_const − Δctl)','anchored constitution documents, no chat')
    for name,dose in [('anch_chatr12',.5),('anch_chatr12',1),('anchp_64',1)]:
        chat='P_64(Δsft_rewr_eos|docs_anch)' if name.startswith('anchp') else 'Δsft_rewr_eos|docs_anch'
        add('anchored_chat',anchored+[[name,dose]],f'θ_I + Δ_docs_anch + {dose}·{chat}','EOS-fixed chat on anchored Base')
    return rows


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    inputs=OUT/'inputs'; inputs.mkdir(exist_ok=True)
    old=json.loads((ROOT/'slop/eval/run8/manifest.json').read_text())
    for name in ['boundary_items.jsonl','demos.jsonl','panel.jsonl','pov.jsonl','change.md','gsm8k_long60.jsonl']:
        assert sha(ROOT/'slop/eval/run8'/name)==old['input_sha256'][name]
        shutil.copyfile(ROOT/'slop/eval/run8'/name,inputs/name)
    items=TC/'data/versions/20261026_v2/items.jsonl'
    assert sha(items)=='5ea2684bc8e8743ad469d57e584622057af399fc8603033e89978053ac08f444'
    shutil.copyfile(items,inputs/'items.jsonl')
    (inputs/'run8_manifest.json').write_text(json.dumps(old,indent=2)+'\n')
    manifest=dict(old)
    manifest['input_sha256']={name:sha(inputs/name) for name in old['input_sha256']}
    commit=subprocess.check_output(['git','-C',str(TC),'rev-parse','HEAD'],text=True).strip()
    assert commit=='a66d2ae5228b273d7bb14477f13a498c477d6218'
    protocol={name:sha(TC/name) for name in old['protocol_sha256']}
    for name,digest in protocol.items():
        frozen=subprocess.check_output(['git','-C',str(TC),'show',commit+':'+name])
        assert hashlib.sha256(frozen).hexdigest()==digest, 'dirty protocol: '+name
    manifest.update(tiny_character_head=commit,protocol_sha256=protocol,n_items=196)
    (inputs/'run16_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    (OUT/'protocol.json').write_text(json.dumps({'commit':commit,'protocol_sha256':protocol,
        'items_sha256':sha(items),'judge':'jev','turn_judge':'jev','temperature':.7,'seeds':[0,1],
        'enable_thinking':False,'change_sha256':sha(inputs/'change.md'),
        'approval':'const_v2 via contact_supervisor, 2026-10-27; freeze updated v2 protocol; report v1-identical subset too'},indent=2)+'\n')
    frozen_items=[json.loads(l) for l in items.open()]
    chosen=['sys_payday_loan','task_agent','task_email']
    for family in ['choice','instructions']:
        group=sorted([r['id'] for r in frozen_items if r['family']==family],key=lambda s:hashlib.sha256(('run16-preselect:'+s).encode()).hexdigest())
        chosen+=group[:4]
    selection={'author':'PI/OpenAI (Sol)','before_outputs':True,'rule':'Required payday/fridge/email, plus SHA256(run16-preselect:ID)-first four choice and four instructions; every fixed T0 panel item; both samples and all turns read.',
               'item_ids':chosen,'items_sha256':sha(items)}
    (OUT/'read_selection.json').write_text(json.dumps(selection,indent=2)+'\n')
    adapters=json.loads((OUT/'donor_hash_check.json').read_text())
    assert all(i['matches'] for a in adapters.values() for i in a['files'].values())
    receipt=json.loads((ROOT/'slop/eval/run14_box_a/lease/retrieval_verified.json').read_text())['manifest']['r10_a14_proj64']
    path=MAIN/'.local/adapters/cg_run14_adapters/r10_a14_proj64'
    for name,info in receipt.items(): assert sha(path/name)==info['sha256']
    adapters['oldp64']={'path':str(path),'files':receipt}
    data=ROOT/'data/train/eos_fixed/chatr12.jsonl'
    assert sha(data)=='284895029fe45211b8a1ecc767b309d2f6be7903ae4c95f18d8071b39eaca951'
    original=MAIN/'.local/run14_executed_chatr12/chatr12.jsonl'
    assert sha(original)=='91e95a6eceff6841190e2485006493b1967e0dc9cc4f954da5e8c7a488a79042'
    a=[json.loads(l) for l in original.open()]; b=[json.loads(l) for l in data.open()]
    assert len(a)==len(b)==1636
    appended=0
    for before,after in zip(a,b):
        target=[s for s in before['segments'] if s['label']][-1]
        if not target['text'].rstrip().endswith('<|im_end|>'):
            target['text']+='<|im_end|>';appended+=1
        assert before==after
    assert appended==903
    rows=cells()
    query=json.loads((ROOT/'slop/eval/run14_box_a/offers_datacenter.json').read_text())['query']
    plan={'author':'PI/OpenAI (Sol)','approval':'wassname $65 total; brief f305ca0a; const_v2 bridge',
          'adapters':adapters,'training_data_sha256':sha(data),'source_data_sha256':sha(original),'eos_appended':appended,
          'cells':rows,'offer_query':query,'max_hours':26,'max_hourly_rate':1.92,'disk_gb':500,
          'traffic_reserve_usd':3,'judge_reserve_usd':6,'review_reserve_usd':2,'termination_margin_usd':2,
          'total_reserve_usd':26*1.92+13,'frozen_manifest':manifest,
          'plain_docs_model':model_name([['stoic',.5],['const',1],['other',1]]),
          'anchored_docs_model':next(r['model'] for r in rows if r['equation']=='θ_I + Δ_docs_anch'),
          'anchored_donor':'mix_stoic=0.5 ctl=-0.5 mix_const=1 ctl=-1 other=1',
          'fallback_donor':'mix_const=2 ctl=-2',
          'heldout_sha256':{p.name:sha(p) for p in (MAIN/'data/train/run11').glob('heldout_*.jsonl')},
          'drop_order':['optional c','P128','new D + P64 x1.25','old-D second sample'],
          'training':'same resolved cx_chatr12 hyperparameters; normalize artifact paths; fixed EOS only substantive data change; SPECTRAL_FRAC=.01; 2 epochs',
          'timing_estimate':'Historical 777 updates/5617 seconds per chat; two chats ~3.2h; setup 1.7h; projections/selectors ~4h;18 v2 cells unknown, budget up to 15h; runner stops at24.5h; hard destroy26h.'}
    assert plan['total_reserve_usd']<=65
    (OUT/'plan.json').write_text(json.dumps(plan,indent=2)+'\n')
    print(json.dumps({'cells':len(rows),'maximum_total_usd':plan['total_reserve_usd'],'read_selection':selection},indent=2))


if __name__=='__main__': main()
