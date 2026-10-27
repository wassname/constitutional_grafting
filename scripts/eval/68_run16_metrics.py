"""Cached run16 metrics, paired item intervals and bracketed matched-effect estimates; no model calls. -- PI/OpenAI (Sol)"""
from collections import defaultdict
import hashlib
import itertools
import json
from pathlib import Path
import random
from statistics import mean

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
BOX=OUT/'lease/box_runs'
FLAGS=('looped','truncated','lang_switch','role_confusion','empty')


def rows(p): return [json.loads(line) for line in p.open() if line.strip()]


def boot(values):
    # Exact resampling scheme/endpoints from 43_paired_ablation.py and run14.
    rng=random.Random(0)
    b=sorted(mean(rng.choice(values) for _ in values) for _ in range(2000))
    return [b[100],b[1899]]


def main():
    plan=json.loads((BOX/'executed_plan.json' if (BOX/'executed_plan.json').exists() else OUT/'plan.json').read_text())
    items={r['id']:r for r in rows(OUT/'inputs/items.jsonl')}
    v1={r['id']:r for r in rows(Path('/workspace/2026/tiny-character/data/versions/20261012_v1/items.jsonl'))}
    assert len(v1)==96 and all(items[iid]==item for iid,item in v1.items())
    old={r['id']:r for r in rows(ROOT/'slop/eval/run8/items.jsonl')}
    small={iid for iid,item in old.items() if item['family']=='capability'}
    assert len(small)==11
    exact_old={iid for iid,it in old.items() if all(it[k]==items[iid][k] for k in ['system','turns','checks','max_new_tokens'])}
    assert len(exact_old)==49
    expected={(iid,s) for iid in items for s in (0,1)}
    metrics={};vectors={};maths={};sources={}
    def source(p):
        with p.open('rb') as stream:sources[str(p.relative_to(ROOT))]=hashlib.file_digest(stream,'sha256').hexdigest()
    for recipe in plan['cells']:
        model=recipe['model'];ordinary=OUT/'ordinary'/model
        if not (BOX/(model+'.done')).exists():continue
        checked=rows(ordinary/'coherence.jsonl');cap=rows(ordinary/'judged.jsonl')
        assert {(r['item_id'],r['sample']) for r in checked}==expected
        turns=[c for r in checked for c in r['turn_checks']]
        legacy=rows(OUT/'legacy_small_tasks'/model/'judged.jsonl')
        legacy_by=defaultdict(list)
        for r in legacy:
            c=r['check'];legacy_by[r['item_id']].append(c['correct'] if 'correct' in c else c['format_ok'])
        assert set(legacy_by)==small and all(len(v)==2 for v in legacy_by.values())
        cap_by=defaultdict(list)
        for r in cap:
            c=r['check'];cap_by[r['item_id']].append(c['correct'] if 'correct' in c else c['format_ok'])
        assert len(cap_by)==19 and all(len(v)==2 for v in cap_by.values())
        gsm=rows(BOX/f'gsm8k_{model}.jsonl');assert len(gsm)==60
        math={r['question']:r for r in gsm};maths[model]=math
        if metrics:
            ref=next(iter(maths.values()));assert math.keys()==ref.keys()
            assert all(math[q]['gold']==ref[q]['gold'] for q in math)
        raw=rows(BOX/f'replies_{model}.jsonl');assert len(raw)==392
        assert {(r['item_id'],r['sample']) for r in raw}==expected
        for r in raw:
            assert r['gen']=={'temperature':.7,'top_p':1.,'seed':r['sample']}
            assert r['system']==items[r['item_id']]['system'] and [t['user'] for t in r['turns']]==items[r['item_id']]['turns']
        point=dict(recipe,maths=sum(r['correct'] for r in gsm),maths_finished=sum(r['finish']=='stop' for r in gsm),
                   small_tasks_22=sum(sum(legacy_by[iid]) for iid in small),
                   all_capability_38=sum(sum(v) for v in cap_by.values()),turns=len(turns),
                   flags={k:sum(c[k] for c in turns) for k in FLAGS},
                   character=None,character_ci90=None,character_v1_96=None)
        char={}
        if recipe['block']!='documents' and model!='r16_instruct':
            judged=OUT/'judging'/model
            if not (judged/'judged.jsonl').exists():continue
            meta=json.loads((judged/'meta.json').read_text())
            assert meta['items_sha256']=='5ea2684bc8e8743ad469d57e584622057af399fc8603033e89978053ac08f444'
            groups=defaultdict(list)
            for r in rows(judged/'judged.jsonl'):
                if r['model']==model and r.get('on_target') is not None:groups[r['item_id']].append(r['on_target'])
            assert len(groups)==177 and all(len(v)==2 for v in groups.values())
            char={iid:mean(v) for iid,v in groups.items()}
            point.update(character=mean(char.values()),character_ci90=boot(list(char.values())),character_items=len(char),
                         character_v1_96=mean(v for iid,v in char.items() if iid in v1),
                         character_run14_overlap=mean(v for iid,v in char.items() if iid in exact_old))
            source(judged/'judged.jsonl');source(judged/'meta.json')
        elif model=='r16_instruct':point.update(character=0,character_v1_96=0)
        metrics[model]=point
        vectors[model]={'character':char,'ordinary':{iid:mean(legacy_by[iid]) for iid in small},
                        'maths':{q:float(r['correct']) for q,r in math.items()}}
        for p in [ordinary/'coherence.jsonl',ordinary/'judged.jsonl',BOX/f'gsm8k_{model}.jsonl',BOX/f'replies_{model}.jsonl']:
            source(p)
    paired={}
    models=list(metrics)
    for a,b in itertools.combinations(models,2):
        comparison={}
        for kind,scale in [('character',1),('ordinary',22),('maths',60)]:
            va,vb=vectors[a][kind],vectors[b][kind]
            if va and vb:
                assert va.keys()==vb.keys()
                values=[scale*(va[k]-vb[k]) for k in sorted(va)]
                comparison[kind]={'mean':mean(values),'ci90':boot(values),'n_items':len(values),'direction':a+' minus '+b}
        common=[q for q in maths[a] if maths[a][q]['finish']==maths[b][q]['finish']=='stop']
        both=[float(maths[a][q]['correct'])-float(maths[b][q]['correct']) for q in common]
        comparison['both_finished']={'n':len(common),'a_correct':sum(maths[a][q]['correct'] for q in common),
                                    'b_correct':sum(maths[b][q]['correct'] for q in common),
                                    'difference_count_ci90':[x*len(common) for x in boot(both)] if both else None}
        paired[a+' vs '+b]=comparison
    low='r16_stoic0.5_const1_other1_eos_chatr120.5';high='r16_stoic0.5_const1_other1_eos_chatr121'
    matched=[]
    if low in metrics and high in metrics:
        x0,x1=metrics[low]['character'],metrics[high]['character']
        for model,p in metrics.items():
            if model in {low,high,'r16_instruct'} or p['block']=='documents' or p['character'] is None:continue
            target=p['character']
            if not x1>x0 or not x0<=target<=x1:
                matched.append({'model':model,'status':'not bracketed by increasing measured new-D half…one path; no extrapolation'})
                continue
            t=(target-x0)/(x1-x0)
            common=[q for q in maths[low] if all(maths[m][q]['finish']=='stop' for m in [low,high,model])]
            expected_math=sum((1-t)*maths[low][q]['correct']+t*maths[high][q]['correct'] for q in common)
            matched.append({'model':model,'status':'linear interpolation estimate, not an evaluated checkpoint; uncertainty not propagated',
                'target_character':target,'estimated_plain_new_D_dose':.5+.5*t,'reference_models':[low,high],
                'estimated_maths':(1-t)*metrics[low]['maths']+t*metrics[high]['maths'],
                'estimated_small_tasks_22':(1-t)*metrics[low]['small_tasks_22']+t*metrics[high]['small_tasks_22'],
                'both_finished_common_n':len(common),'candidate_correct_common':sum(maths[model][q]['correct'] for q in common),
                'estimated_plain_new_D_correct_common':expected_math,
                'sensitivity':[{'power':power,'estimated_maths':(1-t**power)*metrics[low]['maths']+t**power*metrics[high]['maths']} for power in [.5,1,2]]})
    result={'author':'PI/OpenAI (Sol)','protocol':'a66d2ae v2; fresh same-lease baseline; no direct historical-score comparison',
            'v1_identical_items':96,'run14_same_id_items':len(old),'run14_exact_prompt_check_overlap_items':len(exact_old),'metrics':metrics,'paired':paired,'matched':matched,'sources_sha256':sources}
    (OUT/'metrics.json').write_text(json.dumps(result,indent=2)+'\n')
    table=['| Model | Character [90%] | Maths /60 | Run8 tasks /22 | Flags loop/cutoff/language |', '|:--|--:|--:|--:|:--|']
    for model,p in metrics.items():
        char='not measured' if p['character'] is None else f"{p['character']:+.3f}"+(f" [{p['character_ci90'][0]:+.3f}, {p['character_ci90'][1]:+.3f}]" if p['character_ci90'] else ' (ref)')
        f=p['flags'];table.append(f"| `{model}` | {char} | {p['maths']} | {p['small_tasks_22']:g} | {f['looped']:g}/{f['truncated']:g}/{f['lang_switch']:g} over {p['turns']} turns |")
    (OUT/'metrics.md').write_text('\n'.join(table)+'\n')
    print('\n'.join(table))


if __name__=='__main__':main()
