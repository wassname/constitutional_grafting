# Print one sample of chosen items side by side for Instruct, best graft and stage-8 dose cells (head ... tail). usage: python scripts/eval/45_read_cells.py ITEM ...  -- PI/Claude
import json,sys
C={'instruct':'slop/eval/run8/box_runs/replies_r8_a0_b0.jsonl','best':'slop/eval/run10/stage5/box_runs/replies_r10_stoic0.5_const1_other1_cx_chatp121.jsonl'}
B='slop/eval/run10/stage8/box_runs/replies_r10_'
C|={'chat0.5':B+'stoic0.5_const1_other1_cx_chatp120.5.jsonl','chat2':B+'stoic0.5_const1_other1_cx_chatp122.jsonl','const2':B+'stoic0.5_const2_other1_cx_chatp121.jsonl','stoic2':B+'stoic2_const1_other1_cx_chatp121.jsonl'}
D={k:{(r['item_id'],r['sample']):r for r in map(json.loads,open(v))} for k,v in C.items()}
for item in sys.argv[1:]:
    r=D['best'][(item,0)]
    print('#####',item,'| USER:',' '.join(r['turns'][0]['user'].split())[:900])
    if len(r['turns'])>1: print('  (multi-turn; showing last turn) last user:',' '.join(r['turns'][-1]['user'].split())[:300])
    for k in C:
        a=' '.join(D[k][(item,0)]['turns'][-1]['assistant'].split()); w=len(a.split())
        print(f'--- {k} ({w}w): {a[:520]}' + (f' … {a[-160:]}' if len(a)>700 else a[520:700]))
    print()
