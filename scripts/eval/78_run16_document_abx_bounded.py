"""Budgeted replay of run16's planned document ABX, with pilot and paid-request cache. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import httpx

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
CAP=8.0
MODEL='deepseek/deepseek-v4.1-flash'


class Budget:
    def __init__(self,spent=0):self.spent=spent;self.reserved=0.;self.lock=threading.Lock()
    def reserve(self,amount):
        with self.lock:
            assert self.spent+self.reserved+amount<=CAP,'ABX hard cap would be exceeded'
            self.reserved+=amount
    def finish(self,bound,cost):
        with self.lock:self.reserved-=bound;self.spent+=cost


def trials_for(ref,models,render):
    trials=[]
    for name,records in models.items():
        assert set(records)==set(ref)
        for item in sorted({i for i,_ in ref}):
            for j in (0,1):
                first=random.Random(f'{name}|{item}|{j}').random()<.5
                inst,model=render(ref[(item,1-j)]),render(records[(item,1-j)])
                trials.append({'model':name,'item_id':item,'j':j,'instruct_is':'A' if first else 'B','identical':inst==model,
                    'x':render(ref[(item,j)]),'a':inst if first else model,'b':model if first else inst})
    return trials


def main():
    spec=importlib.util.spec_from_file_location('abx40',ROOT/'scripts/eval/40_strength_abx.py')
    abx=importlib.util.module_from_spec(spec);spec.loader.exec_module(abx)
    assert abx.MODEL==MODEL,'Do not silently switch the planned judge'
    listing=json.loads((ROOT/'.local/run16_abx_model.json').read_text());assert listing['id']==MODEL
    prompt_price=float(listing['pricing']['prompt']);output_price=float(listing['pricing']['completion'])
    plan=json.loads((OUT/'plan.json').read_text());box=OUT/'lease/box_runs'
    names=[r['model'] for r in plan['cells'] if r['block']=='documents']
    items={r['id']:r for r in map(json.loads,(OUT/'inputs/items.jsonl').read_text().splitlines())}
    selected={i for i,r in items.items() if r['family'] not in {'capability','instructions'}};assert len(selected)==157
    common=set(selected);flags={};all_records={}
    for model in ['r16_instruct',*names]:
        all_records[model]=abx.load(str(box/f'replies_{model}.jsonl'))
        checked=[json.loads(l) for l in (OUT/'ordinary'/model/'coherence.jsonl').open()]
        bad={r['item_id'] for r in checked if any(any(t[k] for k in ['looped','truncated','lang_switch','role_confusion','empty']) for t in r['turn_checks'])}
        flags[model]=sorted(bad);common-=bad
    assert common
    target=OUT/'document_change';target.mkdir(exist_ok=True)
    (target/'selection.json').write_text(json.dumps({'author':'PI/OpenAI (Sol)','raw_item_ids':sorted(selected),'common_coherent_item_ids':sorted(common),'flagged_item_ids':flags,'rule':'Same157 moral/persona items as66; coherent set common to Instruct and all5 document models, both samples/all turns clean. No target-character filter.'},indent=2)+'\n')
    model_records={'null_identical':all_records['r16_instruct']}|{n:all_records[n] for n in names}
    trials=trials_for({k:r for k,r in all_records['r16_instruct'].items() if k[0] in selected},
        {n:{k:r for k,r in rs.items() if k[0] in selected} for n,rs in model_records.items()},abx.render)
    cache_path=ROOT/'.local/run16_document_abx_requests.jsonl';cache={}
    if cache_path.exists():
        for line in cache_path.open():
            r=json.loads(line);cache[r['key']]=r
    budget=Budget(sum(r['charged_or_reserved_usd'] for r in cache.values()));lock=threading.Lock();keylocks={}
    def body_for(t):
        return {'model':MODEL,'temperature':0,'max_tokens':400,'reasoning':{'enabled':False},'usage':{'include':True},'messages':[{'role':'user','content':abx.PROMPT.format(x=t['x'],a=t['a'],b=t['b'])}]}
    def _process(t):
        body=body_for(t);key=hashlib.sha256(json.dumps(body,sort_keys=True).encode()).hexdigest()
        if key in cache:
            assert cache[key]['ok'],'Prior paid failure requires investigation, not blind retries'
            return cache[key]['result']
        # UTF-8 bytes upper-bound text token count, plus generous chat framing; no reasoning/tools.
        bound=(len(body['messages'][0]['content'].encode())+4096)*prompt_price+400*output_price
        budget.reserve(bound);cost=bound;record={'key':key,'ok':False,'model':MODEL}
        try:
            response=httpx.post('https://openrouter.ai/api/v1/chat/completions',headers={'Authorization':'Bearer '+abx.KEY},json=body,timeout=300)
            j=response.json();cost=float(j.get('usage',{}).get('cost',bound))
            assert cost<=bound,'Provider cost exceeded conservative token reservation'
            response.raise_for_status()
            import re
            text=j['choices'][0]['message']['content'];match=re.search(r'"same_as_x"\s*:\s*"([AB])"',text or '')
            assert match,'Unparseable ABX answer; do not blindly repay'
            result={'same_as_x':match.group(1),'reason':text,'served':j.get('model'),'cost':cost}
            record.update(ok=True,result=result)
            return result
        finally:
            budget.finish(bound,cost);record.update(charged_or_reserved_usd=cost,epoch=time.time())
            with lock:
                cache[key]=record
                with cache_path.open('a') as stream:stream.write(json.dumps(record)+'\n')
    def process(t):
        key=hashlib.sha256(json.dumps(body_for(t),sort_keys=True).encode()).hexdigest()
        with lock:guard=keylocks.setdefault(key,threading.Lock())
        with guard:return _process(t)
    pilot=[t for n in model_records for t in [next(t for t in trials if t['model']==n and t['j']==0),next(t for t in trials if t['model']==n and t['j']==1)]]
    pilot_results=[process(t) for t in pilot]
    pilot_bytes=sum(len(body_for(t)['messages'][0]['content'].encode()) for t in pilot)
    estimate=2*sum(r['cost'] for r in pilot_results)/pilot_bytes*sum(len(body_for(t)['messages'][0]['content'].encode()) for t in trials)
    receipt={'author':'PI/OpenAI (Sol)','judge':MODEL,'pricing':listing['pricing'],'pilot_trials':len(pilot),'pilot_cost_usd':sum(r['cost'] for r in pilot_results),'conservative_estimated_total_usd':estimate,'hard_cap_usd':CAP,'raw_trials':len(trials),'coherent_items':len(common),'cache_reuse':'Coherent subset reuses exact same raw judgments, not another paid draw'}
    (target/'pilot.json').write_text(json.dumps(receipt,indent=2)+'\n');print('ABX PILOT '+json.dumps(receipt),flush=True)
    assert estimate<=CAP,'Pilot estimate exceeds approved$8; report matched change not established'
    with ThreadPoolExecutor(4) as pool:results=list(pool.map(process,trials))
    rows=[{k:v for k,v in t.items() if k not in ['x','a','b']}|r|{'separated':r['same_as_x']==t['instruct_is']} for t,r in zip(trials,results)]
    summaries={}
    for mode,ids in [('raw',selected),('coherent',common)]:
        folder=target/mode/'abx';folder.mkdir(parents=True,exist_ok=True)
        chosen=[r for r in rows if r['item_id'] in ids]
        (folder/'trials.jsonl').write_text(''.join(json.dumps(r)+'\n' for r in chosen));summary={}
        for name in model_records:
            per={i:[r['separated'] for r in chosen if r['model']==name and r['item_id']==i] for i in sorted(ids)}
            values=[sum(v)/len(v) for v in per.values()];rng=random.Random(0)
            samples=sorted(sum(rng.choice(values) for _ in values)/len(values) for _ in range(4000))
            summary[name]={'strength':sum(values)/len(values),'ci90':[samples[200],samples[3799]],'items':len(ids),'trials':2*len(ids),'identical_pairs':sum(r['identical'] for r in chosen if r['model']==name)}
        (folder/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');summaries[mode]=summary
    receipt.update(completed=True,actual_or_conservative_charged_usd=budget.spent,summaries=summaries,served_models=sorted({str(r['served']) for r in results}))
    assert budget.spent<=CAP
    (target/'result.json').write_text(json.dumps(receipt,indent=2)+'\n');print('ABX COMPLETE $'+str(budget.spent),flush=True)


if __name__=='__main__':main()
