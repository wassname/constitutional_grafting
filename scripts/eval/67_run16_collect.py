"""Incrementally collect run16 evidence, CPU flags, selected full reads and approved v2 judgments. -- PI/OpenAI (Sol)"""
import argparse
import importlib.util
import json
from pathlib import Path
import shlex
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'slop/eval/run16_v2'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--until-event',required=True,help='Stop after copying this box receipt, e.g. eos_trained or anchored_gate_ready')
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location('run16_rental',ROOT/'scripts/eval/60_run16_rental.py')
    controller=importlib.util.module_from_spec(spec);spec.loader.exec_module(controller)
    state=json.loads(controller.rental.STATE.read_text());ssh,host=controller.rental.saved_connection(state)
    box=OUT/'lease/box_runs';box.mkdir(exist_ok=True)
    plan=json.loads((OUT/'plan.json').read_text())
    def calls(argv): subprocess.run(list(map(str,argv)),check=True,timeout=max(1,state['runner_deadline_epoch']-time.time()))
    while time.time()<state['runner_deadline_epoch']:
        calls(['rsync','-az','--exclude=merged_model','--exclude=dose_model','--exclude=selector_D1',
               '-e',shlex.join(ssh),host+':/workspace/cg/runs/run10/',str(box)+'/'])
        if args.until_event!='eos_trained':
            for done in sorted(box.glob('r16_*.done')):
                model=done.stem
                if not (OUT/'read_packages'/model/'manifest.json').exists():
                    calls([sys.executable,ROOT/'scripts/eval/65_run16_read_package.py',model])
                if model=='r16_instruct':continue
                recipe=next((r for r in plan['cells'] if r['model']==model),None)
                if recipe is None and (box/'executed_plan.json').exists():
                    recipe=next(r for r in json.loads((box/'executed_plan.json').read_text())['cells'] if r['model']==model)
                if recipe['block']=='documents':continue
                judged=OUT/'judging'/model
                if (judged/'judged.jsonl').exists():continue
                # Six dollars is a run-wide reservation, not permission to spend six per cell.
                costs=[json.loads(p.read_text()).get('new_cached_request_cost_usd',0) for p in (OUT/'judging').glob('*/cost.json')]
                assert sum(costs)<5.5, 'Judge reserve almost exhausted; ask supervisor before another cell'
                calls([sys.executable,ROOT/'scripts/eval/64_run16_judge.py',judged,
                       box/'replies_r16_instruct.jsonl',box/f'replies_{model}.jsonl'])
        receipt=box/(args.until_event+'.json')
        if receipt.exists():
            print('COLLECTED EVENT '+str(receipt),flush=True)
            return
        if (box/'job.exit').exists():
            raise RuntimeError('Box job exited before requested event: '+(box/'job.exit').read_text())
        time.sleep(60)
    raise TimeoutError('Run16 collection reached runner deadline')


if __name__=='__main__':main()
