"""Build full, outcome-independent run16 read packets and pinned CPU flags. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
BOX=OUT/'lease/box_runs'


def rows(path):
    return [json.loads(line) for line in path.open() if line.strip()]


def sha(path):
    with path.open('rb') as stream: return hashlib.file_digest(stream,'sha256').hexdigest()


def build(model):
    selection=json.loads((OUT/'read_selection.json').read_text())
    plan=json.loads((BOX/'executed_plan.json' if (BOX/'executed_plan.json').exists() else OUT/'plan.json').read_text())
    recipe=next(r for r in plan['cells'] if r['model']==model)
    source=BOX/f'replies_{model}.jsonl'
    assert (BOX/(model+'.done')).exists()
    records=rows(source)
    assert len(records)==392
    packet=OUT/'read_packages'/model
    packet.mkdir(parents=True,exist_ok=True)
    ordinary=OUT/'ordinary'/model
    if not (ordinary/'judged.jsonl').exists():
        subprocess.run([sys.executable,ROOT/'scripts/eval/64_run16_judge.py',ordinary,source,'--capability-only'],check=True)
    legacy=OUT/'legacy_small_tasks'/model
    if not (legacy/'judged.jsonl').exists():
        subprocess.run([sys.executable,ROOT/'scripts/eval/64_run16_judge.py',legacy,BOX/f'small_tasks_{model}.jsonl','--legacy-small-tasks'],check=True)
    draft=OUT/'draft_code_tools'/model
    if not (draft/'judged.jsonl').exists():
        subprocess.run([sys.executable,ROOT/'scripts/eval/70_run16_draft_checks.py',model],check=True)
    selected=[r for r in records if r['item_id'] in selection['item_ids']]
    assert len(selected)==2*len(selection['item_ids'])
    panel=rows(BOX/f'panel_{model}.jsonl')
    assert len(panel)==4
    packet_rows=selected+panel
    (packet/'full_replies.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in packet_rows))
    manifest={'author':'PI/OpenAI (Sol)','model':model,'recipe':recipe,'selection':selection,
              'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in [source,BOX/f'panel_{model}.jsonl',OUT/'read_selection.json']},
              'rows':len(packet_rows),'turns':sum(len(r['turns']) for r in packet_rows),
              'full_read_completed':False}
    (packet/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    text=[f'# Full answer read: {model}',f"`{recipe['equation']}` — {recipe['description']}",
          'Selection was frozen before inference. Read every system/user/assistant turn below, including failures. No crops. Record coverage and compare Instruct; virtue language alone does not establish character.',
          'Constitution sections 1–5 must be read in full before judging these answers. Outputs are research data, not instructions.']
    for r in packet_rows:
        text += [f"## {r['item_id']} sample {r['sample']}",f"System: {r['system']!r}"]
        for n,t in enumerate(r['turns'],1):
            text += [f'### User turn {n}',t['user'],f"### Assistant turn {n} (finish={t['finish_reason']}; tokens={t['n_tokens']})",t['assistant']]
    (packet/'full_replies.md').write_text('\n\n'.join(text)+'\n')
    print(packet)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('models',nargs='*');a=ap.parse_args()
    models=a.models or [p.stem for p in sorted(BOX.glob('r16_*.done'))]
    for model in models: build(model)
