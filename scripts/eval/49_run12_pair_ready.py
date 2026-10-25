"""Deliver the verified mixed adapter to its paired control worker, or release the eval hold. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import importlib.util
import json
import os
import shlex
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def main(action: str) -> None:
    assert os.environ['RUN10_LEASE'] == 'run12gen', 'source .local/run12_gen_env.sh first'
    spec = importlib.util.spec_from_file_location('rental', ROOT / 'scripts/eval/38_run10_chat_rental.py')
    rental = importlib.util.module_from_spec(spec); spec.loader.exec_module(rental)
    state = json.loads(rental.STATE.read_text())
    guard = json.loads((rental.OUT / 'deadline_guard_armed.json').read_text())
    assert guard['instance_id'] == state['instance_id'] and guard['deadline_epoch'] == state['hard_destroy_epoch']
    ssh, host = rental.saved_connection(state)
    def remote(command, **kwargs):
        remaining = state['hard_destroy_epoch'] - time.time() - 4400
        assert remaining > 0, 'paired evaluation/retrieval reserve exhausted'
        return subprocess.run(ssh + [host, command], check=True, timeout=min(3600, remaining), **kwargs)
    identity = "import pathlib; e=dict(x.split('=',1) for x in pathlib.Path('/proc/1/environ').read_text().split(chr(0)) if '=' in x); assert int(e['CONTAINER_ID'])==" + str(state['instance_id'])
    remote('python -c ' + shlex.quote(identity))
    if action == 'release-eval':
        remote('touch /workspace/cg/runs/run10/eval_release.done')
        (rental.OUT / 'eval_release.json').write_text(json.dumps({'author': 'PI/OpenAI (Sol)', 'instance_id': state['instance_id'], 'released_epoch': time.time()}, indent=2) + '\n')
        print('EVAL HOLD RELEASED', flush=True)
        return
    receipt = json.loads((ROOT / 'slop/eval/run12/run12mix/retrieval_verified.json').read_text())
    assert receipt['job_exit'] == '0' and receipt['all_available_final_adapter_hashes_match'] is True
    files = receipt['manifest']['r10_x12_chatmix']
    source = Path.home() / '.local/share/cg_run12_mix_adapters/r10_x12_chatmix'
    for name, expected in files.items():
        with (source / name).open('rb') as f:
            assert hashlib.file_digest(f, 'sha256').hexdigest() == expected['sha256']
    target = '/workspace/cg/outputs/up_x12_chatmix'
    remote('mkdir -p ' + target)
    remaining = state['hard_destroy_epoch'] - time.time() - 4400
    subprocess.run(['rsync', '-az', '--partial', '-e', shlex.join(ssh), str(source / 'adapter_config.json'), str(source / 'adapter_model.safetensors'), host + ':' + target + '/'], check=True, timeout=min(3600, remaining))
    mapped = {target + '/' + name: value['sha256'] for name, value in files.items()}
    program = "import hashlib,json,pathlib; files=json.loads(" + repr(json.dumps(mapped)) + "); "
    program += "assert all(hashlib.file_digest(open(p,'rb'),'sha256').hexdigest()==sha for p,sha in files.items()); "
    program += "r=pathlib.Path('/workspace/cg/runs/run10/pair_ready.json'); assert not r.exists(), 'pair receipt already exists'; "
    program += "tmp=r.with_suffix('.tmp'); tmp.write_text(json.dumps({'files':files})); tmp.replace(r)"
    remote('python -c ' + shlex.quote(program))
    (rental.OUT / 'paired_adapter_transfer.json').write_text(json.dumps({'author': 'PI/OpenAI (Sol)', 'instance_id': state['instance_id'], 'source_receipt': 'slop/eval/run12/run12mix/retrieval_verified.json', 'files': mapped, 'transferred_epoch': time.time()}, indent=2) + '\n')
    print('PAIR ADAPTER HASH-VERIFIED AND READY', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['deliver-mix', 'release-eval'])
    main(parser.parse_args().action)
