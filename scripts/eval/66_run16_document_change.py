"""Stage-appropriate document change: frozen v2 moral/persona ABX, raw and coherent. No preferred-character score. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
BOX=OUT/'lease/box_runs'


def rows(p):return [json.loads(line) for line in p.open() if line.strip()]


def main():
    plan=json.loads((OUT/'plan.json').read_text())
    models=[r['model'] for r in plan['cells'] if r['block']=='documents']
    assert all((BOX/(m+'.done')).exists() for m in models+['r16_instruct'])
    items={r['id']:r for r in rows(OUT/'inputs/items.jsonl')}
    # Freeze the family filter, not a selection by whether the model takes a preferred action.
    selected={iid for iid,it in items.items() if it['family'] not in {'capability','instructions'}}
    assert len(selected)==157
    target=OUT/'document_change';target.mkdir(parents=True,exist_ok=True)
    common=set(selected)
    flags={}
    for model in ['r16_instruct']+models:
        checked=rows(OUT/'ordinary'/model/'coherence.jsonl')
        bad={r['item_id'] for r in checked if any(any(c[k] for k in ('looped','truncated','lang_switch','role_confusion','empty')) for c in r['turn_checks'])}
        flags[model]=sorted(bad)
        common-=bad
    (target/'selection.json').write_text(json.dumps({'author':'PI/OpenAI (Sol)',
        'rule':'All v2 items outside capability/instructions (157). Raw ABX includes failures; coherent ABX uses same common item set across Instruct and ALL five document cells, both samples/all turns clean. Read flags before interpreting change.',
        'raw_item_ids':sorted(selected),'common_coherent_item_ids':sorted(common),'flagged_item_ids':flags,
        'items_sha256':hashlib.sha256((OUT/'inputs/items.jsonl').read_bytes()).hexdigest()},indent=2)+'\n')
    for label,ids in [('raw',selected),('coherent',common)]:
        folder=target/label;folder.mkdir(exist_ok=True)
        assert ids, 'No common coherent document items; do not manufacture a change score'
        paths={}
        for model in ['r16_instruct']+models:
            path=folder/(model+'.jsonl')
            records=[r for r in rows(BOX/f'replies_{model}.jsonl') if r['item_id'] in ids]
            assert len(records)==2*len(ids)
            path.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records));paths[model]=path
        # Existing project-approved ABX judge/protocol, both sample orders; a same-record null should be at chance.
        if not (folder/'abx/trials.jsonl').exists():
            command=[sys.executable,ROOT/'scripts/eval/40_strength_abx.py',folder/'abx',paths['r16_instruct'],
                     'null_identical='+str(paths['r16_instruct'])]+[m+'='+str(paths[m]) for m in models]
            with (folder/'judge.log').open('w') as stream:
                subprocess.run(list(map(str,command)),check=True,stdout=stream,stderr=subprocess.STDOUT)
    print(target)


if __name__=='__main__':main()
