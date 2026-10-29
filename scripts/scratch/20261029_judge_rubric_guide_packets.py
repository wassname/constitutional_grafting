# Per-item read packets: summary stats + seeded stratified sample of 24 earlier replies. PI/Claude judgerubric
import json, random, re, collections
ROOT='/workspace/2026/constitutional_grafting'; D=f'{ROOT}/.local/20261029_judge_rubric/prev'
its=[json.loads(l) for l in open(f'{ROOT}/slop/eval/run18/inputs/items.jsonl') if json.loads(l)['judged']]
refs={json.loads(l)['item_id']:json.loads(l) for l in open(f'{ROOT}/slop/eval/judge_inputs/20261029_refs_opus_v4.jsonl')}
per=collections.defaultdict(list)
for l in open(f'{D}/all_replies.jsonl'):
    r=json.loads(l); per[r['item_id']].append(r)
def group(r):
    s=r['source']
    if s.startswith('tiny-character'): return 'api_models'
    m=re.search(r'slop/eval/([^/]+)',s) or re.search(r'\.local/([^/]+)',s)
    g=m.group(1) if m else 'other'
    return 'run17_cells' if g.startswith('run17') or 'run17' in s else g
def cut(t,n=220):
    w=t.split(); return t if len(w)<=n else ' '.join(w[:n])+f' […{len(w)-n} more words]'
def first(r): return (r['assistant'][0].strip().split('\n')[0][:60]) if r['assistant'] else ''
items=[]
for it in its:
    rs=per[it['id']]; rng=random.Random(it['id'])
    by=collections.defaultdict(list)
    for r in rs: by[group(r)].append(r)
    for g in by.values(): rng.shuffle(g)
    pick=[]; gs=sorted(by)
    while len(pick)<24 and any(by[g] for g in gs):
        for g in gs:
            if by[g] and len(pick)<24: pick.append(by[g].pop())
    fl=collections.Counter(first(r) for r in rs)
    summ={'n_replies':len(rs),'by_source_group':dict(collections.Counter(group(r) for r in rs)),
          'first_line_counts_top10':fl.most_common(10) if it['family'] in ('choice','pov','tiny_stoic','instructions','ai_risk','sycophancy','daily_dilemmas') else 'n/a'}
    items.append({'id':it['id'],'family':it['family'],'system':it['system'],'turns':it['turns'],'tests':it['tests'],'notes':it['notes'],
                  'summary':summ,'our_refs':[[t['assistant'] for t in d] for d in refs[it['id']]['refs']],
                  'sample':[{'rid':r['rid'],'group':group(r),'model':r['model'],'thinking_on':r['thinking'],'assistant':[cut(t) for t in r['assistant']]} for r in pick]})
items.sort(key=lambda i:(i['family'],i['id']))
B=12
for b in range(B):
    with open(f'{ROOT}/.local/20261029_judge_rubric/guide_packets/guide_batch_{b}.jsonl','w') as f:
        for it in items[b::B]: f.write(json.dumps(it,ensure_ascii=False)+'\n')
print('batches',B,'items',len(items),'words/batch ~',sum(len(json.dumps(i).split()) for i in items)//B)
