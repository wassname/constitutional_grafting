"""Process synced run16 cells without blocking the event collector or the remote driver. -- PI/OpenAI (Sol)"""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'
BOX=OUT/'lease/box_runs'


def pending_cells(plan,mode):
    cells=[r for r in plan['cells'] if (BOX/(r['model']+'.done')).exists()]
    if mode=='cpu':return sorted(cells,key=lambda r:(r['block']!='documents',r['model']!='r16_instruct',r['model']))
    return [r for r in cells if r['block']!='documents' and r['model']!='r16_instruct']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode',choices=['cpu','judge'])
    args=parser.parse_args()
    state=json.loads((ROOT/'.local/run16_v2_rental.json').read_text())
    def call(argv):subprocess.run(list(map(str,argv)),check=True,timeout=max(1,state['runner_deadline_epoch']-time.time()))
    while time.time()<state['runner_deadline_epoch']:
        executed=BOX/'executed_plan.json'
        plan=json.loads((executed if executed.exists() else OUT/'plan.json').read_text())
        for recipe in pending_cells(plan,args.mode):
            model=recipe['model']
            if args.mode=='cpu':
                if not (OUT/'read_packages'/model/'manifest.json').exists():
                    call([sys.executable,ROOT/'scripts/eval/65_run16_read_package.py',model])
            else:
                target=OUT/'judging'/model
                if (target/'judged.jsonl').exists():continue
                costs=[json.loads(p.read_text()).get('new_cached_request_cost_usd',0) for p in (OUT/'judging').glob('*/cost.json')]
                assert sum(costs)<5.5,'Run-wide judge reserve almost exhausted; ask supervisor'
                call([sys.executable,ROOT/'scripts/eval/64_run16_judge.py',target,BOX/'replies_r16_instruct.jsonl',BOX/f'replies_{model}.jsonl'])
                print('JUDGED '+model,flush=True)
        if args.mode=='cpu':call([sys.executable,ROOT/'scripts/eval/68_run16_metrics.py'])
        if (BOX/'complete.json').exists():return
        time.sleep(60)
    raise TimeoutError('Local processing reached unchanged runner deadline')


if __name__=='__main__':main()
