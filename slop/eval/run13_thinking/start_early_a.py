"""Parent-approved A/smoke overlap; never changes or restarts the lease controller. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import json
import shlex
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location('thinking_rental', ROOT / 'scripts/eval/53_run13_thinking_rental.py')
module = importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(module)
rental = module.rental
state = json.loads(rental.STATE.read_text())
guard = json.loads((OUT / 'lease/deadline_guard_armed.json').read_text())
assert state['instance_id'] == guard['instance_id'] == 57749737
assert state['hard_destroy_epoch'] == guard['deadline_epoch']
assert state['runner_deadline_epoch'] - time.time() > 1800
ssh, host = rental.saved_connection(state)
identity = "import pathlib; e=dict(x.split('=',1) for x in pathlib.Path('/proc/1/environ').read_text().split(chr(0)) if '=' in x); assert int(e['CONTAINER_ID'])==57749737; assert not pathlib.Path('/workspace/cg/runs/run10/early_A.launch.json').exists()"
subprocess.run(ssh + [host, 'python -c ' + shlex.quote(identity)], check=True, timeout=30)
executor = ROOT / 'scripts/eval/54_run13_thinking_box.py'
generator = ROOT / 'scripts/eval/19_gen_replies.py'
sha = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
receipt = {'author': 'PI/OpenAI (Sol)', 'approved_by': 'const_v2 2026-10-26T03:04:48Z',
           'instance_id': state['instance_id'], 'runner_deadline_epoch': state['runner_deadline_epoch'],
           'executor_sha256': sha(executor), 'generator_sha256': sha(generator),
           'launched_during_uploads': True, 'requested_epoch': time.time(),
           'original_controller': 'run13-thinking-one-lease proc_bde8 unchanged',
           'condition': 'Main accepts only complete frozen140 keys+panels with matching model file hashes, vLLM version, input hashes, generator/executor hashes, sampling, budget and every exact wire request; otherwise preserve and regenerate A.'}
path = OUT / 'overlap_launch.json'
assert not path.exists()
path.write_text(json.dumps(receipt, indent=2) + '\n')
subprocess.run(['rsync', '-az', '-e', shlex.join(ssh), str(executor), host + ':/workspace/cg/scripts/eval/54_run13_thinking_box.py.next'], check=True, timeout=60)
verify = "import hashlib,pathlib; p=pathlib.Path('/workspace/cg/scripts/eval/54_run13_thinking_box.py.next'); assert hashlib.sha256(p.read_bytes()).hexdigest()==" + repr(receipt['executor_sha256']) + "; assert hashlib.sha256(pathlib.Path('/workspace/cg/scripts/eval/19_gen_replies.py').read_bytes()).hexdigest()==" + repr(receipt['generator_sha256']) + "; p.replace(p.with_suffix(''))"
subprocess.run(ssh + [host, 'python -c ' + shlex.quote(verify)], check=True, timeout=30)
subprocess.run(ssh + [host, 'cat > /workspace/cg/runs/run10/early_A.launch.json'], input=json.dumps(receipt), text=True, check=True, timeout=30)
command = f'cd /workspace/cg && HF_HOME=/workspace/hf RUN13_DEADLINE={state["runner_deadline_epoch"]} python scripts/eval/54_run13_thinking_box.py --early-A'
script = f'set +e; {command} > /workspace/cg/runs/run10/early_A.log 2>&1; status=$?; echo $status > /workspace/cg/runs/run10/early_A.exit; tmux wait-for -S run13_early_A_done; exit $status'
subprocess.run(ssh + [host, 'tmux new-session -d -s run13_early_A ' + shlex.quote('bash -lc ' + shlex.quote(script))], check=True, timeout=30)
print('EARLY A STARTED; same exact lease, main controller unchanged', flush=True)
result = subprocess.run(ssh + [host, 'tmux wait-for run13_early_A_done; cat /workspace/cg/runs/run10/early_A.exit'], check=True,
                        capture_output=True, text=True, timeout=state['runner_deadline_epoch'] - time.time())
subprocess.run(['rsync', '-az', '-e', shlex.join(ssh), '--exclude=merged_model', host + ':/workspace/cg/runs/run10/', str(OUT / 'lease/box_runs') + '/'], check=True, timeout=600)
receipt['exit'] = result.stdout.strip()
receipt['completed_epoch'] = time.time()
path.write_text(json.dumps(receipt, indent=2) + '\n')
assert receipt['exit'] == '0', 'early A failed; preserve native smoke/raw traces; main owns any subsequent action'
assert (OUT / 'lease/box_runs/early_A.receipt.json').exists()
print('EARLY A COMPLETE; verified native smoke+primary downloaded', flush=True)
