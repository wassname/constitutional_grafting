"""Draft code/tools checks stay separate, code-scored and credential-isolated. -- PI/OpenAI (Sol)"""
import importlib.util
import json
from pathlib import Path
import subprocess

import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('run16_draft',ROOT/'scripts/eval/70_run16_draft_checks.py')
draft=importlib.util.module_from_spec(spec);spec.loader.exec_module(draft)


def test_real_draft_check_runner_with_trusted_positive_and_negative_fixtures(tmp_path,capsys):
    checks=ROOT/'slop/eval/run16_v2/draft_code_tools/checks_a0b0683.py'
    items=[];replies=[]
    for i in range(36):
        code=i<20
        item={'id':f'smoke_{i}','family':'code' if code else 'tools','system':None,'turns':['Synthetic pipeline smoke'],
              'checks':{'kind':'unittest','test':'def check(f):\n    assert f(1)==2\n','entry_point':'f'} if code else {'kind':'tool_call','answers':[{'add':{'a':[1],'b':[2]}}]}}
        items.append(item)
        answer='```python\ndef f(x):\n    return x+1\n```' if code else '[{"name":"add","arguments":{"a":1,"b":2}}]'
        for sample in [0,1]: replies.append({'model':'smoke_only','item_id':item['id'],'sample':sample,'system':None,
            'turns':[{'user':item['turns'][0],'assistant':answer if sample==0 else 'Not a solution.','finish_reason':'stop','n_tokens':20}]})
    p=tmp_path/'items.jsonl';p.write_text(''.join(json.dumps(r)+'\n' for r in items))
    r=tmp_path/'replies.jsonl';r.write_text(''.join(json.dumps(x)+'\n' for x in replies))
    draft.inside(r,p,checks)
    results=[json.loads(l) for l in capsys.readouterr().out.splitlines()]
    assert len(results)==72
    assert all(x['check']['correct']==float(x['sample']==0) for x in results)


def test_docker_boundary_has_no_credentials_socket_network_or_root_writes():
    image=ROOT/'.local/run16_draft_sandbox/image.txt'
    if not image.exists():pytest.skip('Local prepared Docker sandbox not available')
    code='''import os,socket
from pathlib import Path
assert os.getuid()==65534
assert not Path('/home/code/.ssh').exists()
assert not Path('/workspace/2026/constitutional_grafting/.env').exists()
assert not Path('/var/run/docker.sock').exists()
try:socket.create_connection(('1.1.1.1',80),timeout=.1)
except OSError:pass
else:raise AssertionError('Network unexpectedly available')
try:Path('/usr/run16_forbidden').write_text('no')
except OSError:pass
else:raise AssertionError('Root filesystem unexpectedly writable')
Path('/tmp/allowed').write_text('yes')
print('isolated')
'''
    args=['docker','run','--rm','--network','none','--read-only','--user','65534:65534','--cap-drop','ALL',
          '--security-opt','no-new-privileges','--pids-limit','64','--memory','1g','--cpus','1',
          '--tmpfs','/tmp:rw,nosuid,nodev,size=256m,mode=1777','-v','/usr:/usr:ro','-v','/lib:/lib:ro','-v','/lib64:/lib64:ro',
          image.read_text().strip(),'/usr/bin/python3.12','-I','-c',code]
    result=subprocess.run(args,check=True,capture_output=True,text=True,timeout=30)
    assert result.stdout.strip()=='isolated'
