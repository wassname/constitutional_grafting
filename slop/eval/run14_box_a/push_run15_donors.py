"""Read-only donor push over a fresh, receiver-scoped SSH key. -- PI/OpenAI (Sol)"""
import argparse
import importlib.util
import json
import shlex
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'slop/eval/run14_box_a'
spec = importlib.util.spec_from_file_location('r14', ROOT / 'scripts/eval/55_run14_box_a_rental.py')
r14 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r14)
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('receipt', type=Path)
args = parser.parse_args()
assert args.receipt.resolve().parent == OUT
relay = json.loads(args.receipt.read_text())
plan = json.loads((OUT / 'plan.json').read_text())
state = json.loads(r14.rental.STATE.read_text())
assert state['instance_id'] == relay['source_instance_id'] == 57799463
target = next(r for r in r14.rental.api('/instances/')['instances'] if r['id'] == relay['target_instance_id'])
assert target['label'] == relay['target_label'] == 'cg-run15-thinking-heal-retry1' and target['actual_status'] == 'running'
assert target['public_ipaddr'] == relay['target_ssh_host'] == '154.59.156.15'
assert any(str(p['HostPort']) == relay['target_ssh_port'] == '33881' for p in target['ports']['22/tcp'])
assert relay['receiver_authorization_confirmed_utc']
names = relay['requested_names']
assert names == ['stoic', 'const', 'other', 'rewr']
expected = {name: plan['adapters'][name]['files'] for name in names}
for name in names:
    for filename, info in expected[name].items():
        assert {k: relay['source_files'][name][filename][k] for k in info} == info
        info['mtime_seconds'] = relay['source_files'][name][filename]['mtime_seconds']
key = relay['source_ephemeral_private_key_path']
assert key.startswith('/workspace/cg/.local/run15_relay_') and key.rsplit('_', 1)[1].isdigit()
host_key = relay['target_host_public_key']
assert host_key == 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK39ErK/YVIHf74fsjzhsUFrwYrqL3rbQvHZiQgFJ4R+'
known_line = f"[{relay['target_ssh_host']}]:{relay['target_ssh_port']} {host_key}\n"
receiver = 'root@' + relay['target_ssh_host'] + ':/'
ssh, host = r14.rental.saved_connection(state)
code = f'''
import hashlib,json,os,shlex,subprocess,time
from pathlib import Path
os.nice(10)
key=Path({key!r}); known=Path(str(key)+'.known_hosts')
expected={expected!r}
known.write_text({known_line!r}); known.chmod(0o600)
transport=shlex.join(['ssh','-F','/dev/null','-i',str(key),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(known),'-o','ConnectTimeout=15','-o','ServerAliveInterval=30','-o','ServerAliveCountMax=3','-p',{relay['target_ssh_port']!r}])
try:
 for name in {names!r}:
  sources=[]
  for filename,info in expected[name].items():
   path=Path('/workspace/cg/outputs/up_'+name)/filename
   with path.open('rb')as stream: assert hashlib.file_digest(stream,'sha256').hexdigest()==info['sha256']
   assert path.stat().st_size==info['bytes'] and int(path.stat().st_mtime)==info['mtime_seconds']
   sources.append('/workspace/cg/outputs/./up_'+name+'/'+filename)
  print('RELAY DIR START up_'+name,flush=True)
  subprocess.run(['rsync','-azR','--partial','--bwlimit=15360','-e',transport,*sources,{receiver!r}],check=True,timeout=1200)
  for filename,info in expected[name].items():
   path=Path('/workspace/cg/outputs/up_'+name)/filename
   with path.open('rb')as stream: assert hashlib.file_digest(stream,'sha256').hexdigest()==info['sha256']
   assert path.stat().st_size==info['bytes'] and int(path.stat().st_mtime)==info['mtime_seconds']
  print('RELAY DIR DONE up_'+name+' sourcehashes unchanged; receiver must independently hash before atomic install',flush=True)
finally:
 for path in [key,Path(str(key)+'.pub'),known]:path.unlink(missing_ok=True)
 print('RELAY TEMPORARY SOURCE KEY REMOVED',flush=True)
'''
try:
    subprocess.run(ssh + [host, 'python -u -c ' + shlex.quote(code)], check=True, timeout=2000)
finally:
    cleanup = 'from pathlib import Path; [Path(p).unlink(missing_ok=True) for p in ' + repr([key, key + '.pub', key + '.known_hosts']) + ']'
    subprocess.run(ssh + [host, 'python -c ' + shlex.quote(cleanup)], check=True, timeout=30)
relay.update(status='four donor directories sent; source hashes unchanged; ephemeral source key removed', sent_names=names,
             receiver_must_verify=True)
args.receipt.write_text(json.dumps(relay, indent=2) + '\n')
