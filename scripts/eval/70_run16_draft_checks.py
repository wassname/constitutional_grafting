"""Score the separate draft code/tools panel, with unchanged a0b0683 checks in a credential-free sandbox. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path("/") if sys.argv[1:]==["--inside"] else Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'


def inside(records_path,items_path,checks_path):
    spec=importlib.util.spec_from_file_location('draft_checks',checks_path)
    checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)
    items={r['id']:r for r in map(json.loads,Path(items_path).read_text().splitlines())}
    records=[json.loads(l) for l in Path(records_path).open()]
    assert len(items)==36 and len(records)==72
    model=records[0]['model'];assert {r['model'] for r in records}=={model}
    assert {(r['item_id'],r['sample']) for r in records}=={(i,s) for i in items for s in (0,1)}
    for r in records:
        item=items[r['item_id']]
        assert r['system']==item['system'] and [t['user'] for t in r['turns']]==item['turns']
        result={'model':model,'item_id':r['item_id'],'sample':r['sample'],'family':item['family'],
                'check':checks.item_check(item['checks'],[t['assistant'] for t in r['turns']]),
                'turn_checks':[checks.turn_checks(t,item['checks']) for t in r['turns']]}
        print(json.dumps(result),flush=True)


def main(model):
    protocol=json.loads((OUT/'draft_code_tools/protocol.json').read_text())
    source=OUT/'lease/box_runs'/f'draft_code_tools_{model}.jsonl'
    target=OUT/'draft_code_tools'/model;target.mkdir(parents=True,exist_ok=True)
    assert not (target/'judged.jsonl').exists(), 'Preserve completed draft checks'
    checks=OUT/'draft_code_tools/checks_a0b0683.py';items=OUT/'inputs/draft_code_tools.jsonl'
    assert hashlib.sha256(checks.read_bytes()).hexdigest()==protocol['checks_sha256']
    assert hashlib.sha256(items.read_bytes()).hexdigest()==protocol['panel_sha256']
    image=(ROOT/'.local/run16_draft_sandbox/image.txt').read_text().strip()
    command=['docker','run','--rm','--network','none','--read-only','--user','65534:65534','--cap-drop','ALL',
             '--security-opt','no-new-privileges','--pids-limit','64','--memory','1g','--cpus','1',
             '--tmpfs','/tmp:rw,nosuid,nodev,size=256m,mode=1777',
             '-v','/usr:/usr:ro','-v','/lib:/lib:ro','-v','/lib64:/lib64:ro',
             '-v','/workspace/2026/tiny-character/.venv:/env:ro',
             '-v',str(Path(__file__).resolve())+':/inputs/runner.py:ro',
             '-v',str(source)+':/inputs/replies.jsonl:ro',
             '-v',str(items)+':/inputs/items.jsonl:ro',
             '-v',str(checks)+':/inputs/checks.py:ro',
             image,'/env/bin/python','-I','/inputs/runner.py','--inside']
    # Only these four input files, system binaries/libraries and dependency venv are mounted. No home/project/key paths or socket.
    temporary=target/'judged.tmp'
    with temporary.open('w') as output, (target/'checks.log').open('w') as error:
        subprocess.run(command,stdout=output,stderr=error,check=True,timeout=2500)
    records=[json.loads(l) for l in temporary.open()]
    assert len(records)==72 and all(r['model']==model for r in records)
    summary={family:{'correct':sum(r['check']['correct'] for r in records if r['family']==family),
                     'n':sum(r['family']==family for r in records)} for family in ['code','tools']}
    temporary.rename(target/'judged.jsonl')
    (target/'summary.json').write_text(json.dumps({'label':'draft code/tools','model':model,'scores':summary,'judge_calls':0,
        'image_digest':image,'protocol':protocol,'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
        'sandbox_argv':command},indent=2)+'\n')
    print(model,summary)


if __name__=='__main__':
    if sys.argv[1:]==['--inside']:
        inside('/inputs/replies.jsonl','/inputs/items.jsonl','/inputs/checks.py')
    else:
        parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('model');args=parser.parse_args();main(args.model)
