# Collect every earlier reply to the 177 judged items (exact user turns + system), dedupe by text. PI/Claude judgerubric
import json, glob, os, hashlib, collections, sys
ROOT='/workspace/2026/constitutional_grafting'
its={json.loads(l)['id']:json.loads(l) for l in open(f'{ROOT}/slop/eval/run18/inputs/items.jsonl') if json.loads(l)['judged']}
pats=[f'{ROOT}/slop/eval/**/*.jsonl', f'{ROOT}/.local/run1*/**/*.jsonl', '/workspace/2026/tiny-character/results/**/replies.jsonl']
files=set()
for p in pats: files|=set(glob.glob(p, recursive=True))
files={f for f in files if 'judge_rubric' not in f and not f.endswith('.wire.jsonl') and os.path.getsize(f)>2000 and ('replies' in os.path.basename(f) or os.path.basename(f).startswith(('think_',)))}
seen={}; per=collections.defaultdict(list); nfiles=0
for f in sorted(files):
    try:
        with open(f) as fh: first=fh.readline()
        r=json.loads(first)
        if not {'item_id','turns','model'}<=set(r): continue
    except Exception: continue
    nfiles+=1
    for l in open(f):
        try: r=json.loads(l)
        except Exception: continue
        i=r.get('item_id')
        if i not in its or not isinstance(r.get('turns'),list): continue
        if [t.get('user') for t in r['turns']]!=its[i]['turns'] or r.get('system')!=its[i]['system']: continue
        a=[t.get('assistant') or '' for t in r['turns']]
        if not any(x.strip() for x in a): continue
        h=hashlib.sha256(json.dumps([i,a]).encode()).hexdigest()[:12]
        if h in seen: seen[h]['n']+=1; continue
        rec={'rid':h,'item_id':i,'model':r['model'],'source':os.path.relpath(f,'/workspace/2026'),'thinking':os.path.basename(f).startswith('think_'),'assistant':a,'n':1}
        seen[h]=rec; per[i].append(rec)
with open(f'{ROOT}/.local/20261029_judge_rubric/prev/all_replies.jsonl','w') as out:
    for i in its:
        for r in per[i]: out.write(json.dumps(r,ensure_ascii=False)+'\n')
c=[len(per[i]) for i in its]
print('files',nfiles,'replies',sum(c),'per item min/median/max',min(c),sorted(c)[len(c)//2],max(c))
print('items with 0:',[i for i in its if not per[i]][:10])
