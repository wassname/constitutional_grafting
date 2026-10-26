"""Read-only donor push over a fresh, receiver-scoped SSH key. -- PI/OpenAI (Sol)"""
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
relay = json.loads((OUT / 'relay_to_run15.json').read_text())
plan = json.loads((OUT / 'plan.json').read_text())
state = json.loads(r14.rental.STATE.read_text())
assert state['instance_id'] == relay['source_instance_id'] == 57799463
target = next(r for r in r14.rental.api('/instances/')['instances'] if r['id'] == relay['target_instance_id'])
assert target['label'] == 'cg-run15-thinking-heal' and target['actual_status'] == 'running'
assert target['public_ipaddr'] == '154.59.156.39'
assert any(str(p['HostPort']) == '35774' for p in target['ports']['22/tcp'])
names = ['const', 'other', 'rewr']
expected = {name: plan['adapters'][name]['files'] for name in names}
key = relay['source_ephemeral_private_key_path']
assert key.startswith('/workspace/cg/.local/run15_relay_') and key.rsplit('_', 1)[1].isdigit()
host_key = 'ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIL6iCQpmIWLE11Y3SANmXUT5DZ2lc0X78rgGqTylxcb9'
ssh, host = r14.rental.saved_connection(state)
code = f'''
import hashlib,json,os,shlex,subprocess,time
from pathlib import Path
os.nice(10)
key=Path({key!r}); known=Path(str(key)+'.known_hosts')
expected={expected!r}
known.write_text('[154.59.156.39]:35774 '+{host_key!r}+'\\n'); known.chmod(0o600)
transport=shlex.join(['ssh','-F','/dev/null','-i',str(key),'-o','IdentitiesOnly=yes','-o','BatchMode=yes','-o','StrictHostKeyChecking=yes','-o','UserKnownHostsFile='+str(known),'-o','ConnectTimeout=15','-o','ServerAliveInterval=30','-o','ServerAliveCountMax=3','-p','35774'])
try:
 for name in {names!r}:
  sources=[]
  for filename,info in expected[name].items():
   path=Path('/workspace/cg/outputs/up_'+name)/filename
   with path.open('rb')as stream: assert hashlib.file_digest(stream,'sha256').hexdigest()==info['sha256']
   assert path.stat().st_size==info['bytes']
   sources.append('/workspace/cg/outputs/./up_'+name+'/'+filename)
  print('RELAY DIR START up_'+name,flush=True)
  subprocess.run(['rsync','-azR','--partial','--bwlimit=15360','-e',transport,*sources,'root@154.59.156.39:/'],check=True,timeout=1200)
  for filename,info in expected[name].items():
   path=Path('/workspace/cg/outputs/up_'+name)/filename
   with path.open('rb')as stream: assert hashlib.file_digest(stream,'sha256').hexdigest()==info['sha256']
  print('RELAY DIR DONE up_'+name+' sourcehashes unchanged; receiver must independently hash before atomic install',flush=True)
finally:
 for path in [key,Path(str(key)+'.pub'),known]:path.unlink(missing_ok=True)
 print('RELAY TEMPORARY SOURCE KEY REMOVED',flush=True)
'''
try:
    subprocess.run(ssh + [host, 'python -u -c ' + shlex.quote(code)], check=True, timeout=1300)
finally:
    cleanup = 'from pathlib import Path; [Path(p).unlink(missing_ok=True) for p in ' + repr([key, key + '.pub', key + '.known_hosts']) + ']'
    subprocess.run(ssh + [host, 'python -c ' + shlex.quote(cleanup)], check=True, timeout=30)
relay.update(status='three donor directories sent; source hashes unchanged; ephemeral source key removed', sent_names=names,
             receiver_stage='/workspace/cg/outputs/relay_from_box_a', receiver_must_verify=True)
(OUT / 'relay_to_run15.json').write_text(json.dumps(relay, indent=2) + '\n')
