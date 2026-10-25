"""Reuse frozen records for the chat baseline comparison. -- PI/OpenAI (Sol)"""
import hashlib
import json
import random
import sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0, 'scripts/eval')
from coherence_metrics import check_coherence, load_pinned_checks

R = Path('slop/eval/run11')
N = 'r10_stoic0.5_const1_other1_x11_chatr131'
O = 'r10_stoic0.5_const1_other1_cx_chatr121'
D = 'r10_stoic0.5_const1_other1'
B = 'r8_a0_b0'
models = [N,O,D,B]
load = lambda p: list(map(json.loads, Path(p).read_text().splitlines()))
out = R / 'chatr13'
judging = out / 'comparison'
strength = out / 'strength'
judging.mkdir(exist_ok=True); strength.mkdir(exist_ok=True)
jsources = [R / 'chatr13/judging/judged.jsonl', Path('slop/eval/run10/stage7/judging/cells/judged.jsonl'), Path('slop/eval/run10/stage5/judging/cells/judged.jsonl')]
bykey = {}
for p in jsources:
    for x in load(p):
        if x['model'] in models:
            key = (x['model'],x['item_id'],x['sample'])
            if key not in bykey: bykey[key] = x
assert all(sum(k[0]==m for k in bykey)==140 for m in models)
(judging / 'judged.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in bykey.values()))
sources = [R / 'strength/chatr13/trials.jsonl',Path('slop/eval/run10/strength/trials.jsonl')]
srows = [x for p in sources for x in load(p) if x['model'] in models]
assert len({(x['model'],x['item_id'],x['j']) for x in srows}) == len(srows)
(strength / 'trials.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in srows))
manifest=json.loads(Path('slop/eval/run8/manifest.json').read_text())
checks=load_pinned_checks(Path('.local/tiny-character'),manifest['protocol_sha256'])
items={x['id']:x for x in load('slop/eval/run8/items.jsonl')}
boxes = {N:R/'lease1/box_runs',O:Path('slop/eval/run10/stage7/box_runs'),D:Path('slop/eval/run10/stage5/box_runs'),B:Path('slop/eval/run8/box_runs')}
records=[x for m in models for x in load(boxes[m]/f'replies_{m}.jsonl')]
coherence,summaries=check_coherence(records,items,checks)
(out/'coherence.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in coherence))
(out/'coherence_summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
lines=['# Chatr13 ordinary-check failures','PI/OpenAI (Sol). All frozen-check failures, with full prompts and replies.']
for r in bykey.values():
    if r['model'] not in [N,O] or r['family']!='capability': continue
    c=r['check']; score=c['correct'] if 'correct' in c else c['format_ok']
    if score==1: continue
    x=next(x for x in records if (x['model'],x['item_id'],x['sample'])==(r['model'],r['item_id'],r['sample']))
    lines += [f"## {r['model']} / {r['item_id']} / sample{r['sample']}",f"Check:{c}",f"System:{x['system']!r}"]
    for t in x['turns']: lines += ['### User',t['user'],'### Assistant',t['assistant'],f"Finish:{t['finish_reason']}"]
(out/'ordinary_failures.md').write_text('\n\n'.join(lines)+'\n')
summary={}
for m in models:
    rr=[x for x in bykey.values() if x['model']==m]
    char=[x for x in rr if x.get('on_target') is not None]
    caps=[x for x in rr if x['family']=='capability']
    strengths=[x for x in srows if x['model']==m]
    maths=load(boxes[m]/f'gsm8k_{m}.jsonl')
    summary[m]={'character_mean':sum(x['on_target'] for x in char)/len(char) if char else None,'character_records':len(char),'character_items':len({x['item_id'] for x in char}),'ordinary_sum':sum(x['check']['correct'] if 'correct' in x['check'] else x['check']['format_ok'] for x in caps),'ordinary_n':len(caps),'maths_correct':sum(x['correct'] for x in maths),'maths_n':len(maths),'strength_correct':sum(x['separated'] for x in strengths),'strength_trials':len(strengths),'coherence':summaries[m]}
proof={'author':'PI/OpenAI (Sol)','summary':summary,'judged_sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in jsources},'strength_sources':{str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sources},'scope':'CPU-only reuse of frozen scores and checks; no new model calls or altered thresholds.'}
(out/'comparison_summary.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
