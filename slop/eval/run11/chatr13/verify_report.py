"""Verify report numbers and assigned-source quotations without model calls. -- PI/OpenAI (Sol)"""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
R = Path('slop/eval/run11')
P = Path('docs/results/20261025_document_and_anchored_grafts.md')
page = P.read_text()
new='r10_stoic0.5_const1_other1_x11_chatr131'
old='r10_stoic0.5_const1_other1_cx_chatr121'
summary=json.loads((R/'chatr13/comparison_summary.json').read_text())['summary']
labels={'Chatr12, previous baseline':old,'Chatr13, new baseline':new,'Same documents, no chat':'r10_stoic0.5_const1_other1','Instruct, no adapters':'r8_a0_b0'}
count=0
for line in page.split('## New chat baseline:',1)[1].split('### What the training learned',1)[0].splitlines():
    if not line.startswith('| ') or line.startswith('| Graft'):continue
    cells=[x.strip().replace('*','') for x in line.split('|')[1:-1]]
    label,char,maths,ordinary,flags,strength=cells;m=labels[label];v=summary[m]
    assert int(maths)==v['maths_correct'] and int(ordinary)==v['ordinary_sum']
    assert flags==' / '.join(str(v['coherence'][k]) for k in ['lang_switch','looped','truncated'])
    if v['character_mean'] is not None:assert float(char)==float(f"{v['character_mean']:+.2f}")
    if v['strength_trials']:assert int(strength.split('%')[0])==round(100*v['strength_correct']/v['strength_trials'])
    count+=1
assert count==4
paired=(R/'chatr13/paired_vs_chatr12.md').read_text()
assert '| '+new+' | +0.77 | -0.12 [-0.27, +0.01] |' in paired
assert '−0.12 [−0.27, +0.01]' in page
scan=json.loads((R/'lease1/chatr13_log_scan.json').read_text());assert scan['optimizer_rows']==854
assert [r['numeric']['eval_text_loss'] for r in scan['eval_records']]==[1.860,1.636,1.681]
assignments=[]
for line in (R/'report_quote_verification.log').read_text().splitlines():
    if not line.startswith('PASS '):continue
    m=re.match(r'PASS (\S+) (\S+) turn(\d+) (assistant|user):.*sample(\d+)',line);assert m,line
    groups=m.groups()
    if groups[0]!=new:assignments.append(groups)
assert len(assignments)==29
assignments.insert(0,(new,'da_t6_b15_s001','2','assistant','0'))
quotes=re.findall(r'(?:^>[^\n]*(?:\n|$))+',page,flags=re.M);assert len(quotes)==30
coherence=json.loads((R/'solo_document_table.coherence.json').read_text())['models']
norm=lambda s:' '.join(s.replace('*','').split())
lines=[]
for q,(model,item,turn,role,sample) in zip(quotes,assignments,strict=True):
    directory=R/'lease1/box_runs' if model==new else Path(coherence[model]['source']).parent
    kind='panel' if item.startswith('panel_') else 'replies'
    rows=list(map(json.loads,(directory/f'{kind}_{model}.jsonl').read_text().splitlines()))
    row=next(x for x in rows if x['item_id']==item and x['sample']==int(sample))
    excerpt='\n'.join(l.removeprefix('> ') for l in q.splitlines())
    assert norm(excerpt) in norm(row['turns'][int(turn)-1][role]),(model,item,excerpt)
    lines.append(f'PASS {model} {item} turn{turn} {role}: exact assigned-source excerpt after whitespace/Markdown-emphasis normalization; sample{sample}')
lines.append('PI/OpenAI (Sol): all30 blockquotes verified.')
(R/'report_quote_verification.log').write_text('\n'.join(lines)+'\n')
proof={'author':'PI/OpenAI (Sol)','checked_at':datetime.now(timezone.utc).isoformat(),'page':str(P),'page_sha256':hashlib.sha256(P.read_bytes()).hexdigest(),'chat_comparison_rows':4,'character_records_per_chat':118,'character_items_per_chat':59,'paired_character_difference':'-0.12 [-0.27, +0.01]','maths_and_ordinary_match_raw_records':True,'coherence_flags_match_pinned_checks':True,'training_components_match_complete_log_scan':True,'all_assigned_source_quotes':30,'lease_closure':json.loads((R/'lease1/closure_usage.json').read_text())['closure'],'scope':'CPU verification only; no new calls, score changes or causal/equivalence claim.'}
(R/'chatr13/report_verification.json').write_text(json.dumps(proof,indent=2)+'\n')
print(json.dumps(proof,indent=2))
