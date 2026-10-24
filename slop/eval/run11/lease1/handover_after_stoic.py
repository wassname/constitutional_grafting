"""Replace only the finished Stoic job's launchers, retaining the lease. -- PI/OpenAI"""
import argparse
import importlib.util
import json
import os
import select
import shlex
import signal
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("rental", ROOT / "scripts/eval/38_run10_chat_rental.py")
rental = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rental)
REMOTE = r'''
import json, os, select, shlex, signal, subprocess, sys
from pathlib import Path
os.chdir('/workspace/cg')
r=Path('runs/run10'); p=json.loads((r/'launcher_boundary_pause.json').read_text())
pid=p['paused_launcher_pid']; child=p['running_training_child']['pid']
status=dict(line.split(':',1) for line in Path(f'/proc/{pid}/status').read_text().splitlines() if ':' in line)
assert status['State'].strip().startswith('T'), status['State']
assert Path(f'/proc/{pid}/cmdline').read_bytes().split(b'\0')[1]==b'scripts/train/14_run10_chat_box.sh'
fields=Path(f'/proc/{child}/stat').read_text().rsplit(') ',1)[1].split()
assert int(fields[1])==pid, 'Training child no longer belongs to the paused launcher'
assert fields[0]=='Z', f'Stoic training child still active: {fields[0]}'
assert int(fields[49])==0, f'Stoic child exit code: {fields[49]}'
assert not (r/'job.exit').exists(), 'Unexpected old job.exit; inspect before handover'
outer=int(status['PPid']); argv=Path(f'/proc/{outer}/cmdline').read_bytes()
assert b'14_run10_chat_box.sh' in argv and b'job.exit' in argv, argv
report={'paused_launcher_pid':pid,'training_child_pid':child,'training_exit_code':0,'old_exit_writer_pid':outer}
if sys.argv[1]=='preflight':
    print(json.dumps(report)); sys.exit(0)
assert sys.argv[1]=='replace'
for name in ['job.log','job.exit']:
    assert not (r/('before_document_priority.'+name)).exists()
parent_fd=os.pidfd_open(pid); outer_fd=os.pidfd_open(outer)
os.kill(pid,signal.SIGKILL)
assert select.select([parent_fd],[],[],10)[0], 'Old launcher has not exited'
assert select.select([outer_fd],[],[],10)[0], 'Old exit writer has not exited'
os.close(parent_fd); os.close(outer_fd)
result=subprocess.run(['tmux','kill-session','-t','=run10_train'],capture_output=True,text=True)
report['old_tmux_retire_returncode']=result.returncode
assert subprocess.run(['tmux','has-session','-t','=run10_train'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode!=0
for name in ['job.log','job.exit']:
    path=r/name
    if path.exists(): path.rename(r/('before_document_priority.'+name))
wrapper='set +e; cd /workspace/cg; python runs/run10/remaining_stages.py > runs/run10/job.log 2>&1; status=$?; echo "$status" > runs/run10/job.exit; exit "$status"'
subprocess.run(['tmux','new-session','-d','-s','run10_train','bash -lc '+shlex.quote(wrapper)],check=True)
subprocess.run(['tmux','has-session','-t','=run10_train'],check=True)
assert not (r/'job.exit').exists(), 'Replacement exited immediately; inspect job.log before attaching'
(r/'ordered_handover.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
'''


def main(preflight_only):
    state = json.loads(rental.STATE.read_text())
    ssh, host = rental.saved_connection(state)
    def remote(mode):
        try:
            return subprocess.run(ssh + [host, "python - " + mode], input=REMOTE, text=True, check=True, capture_output=True, timeout=45)
        except subprocess.CalledProcessError as error:
            print(error.stderr, file=sys.stderr)
            raise
    preflight = remote("preflight")
    print(preflight.stdout, flush=True)
    if preflight_only:
        return
    assert rental.EXPECTED_ADAPTERS_FILE == "run11_execution_plan.json"
    controllers, snapshots = [], []
    for p in Path("/proc").iterdir():
        if not p.name.isdigit():
            continue
        try:
            argv = [os.fsdecode(arg) for arg in (p / "cmdline").read_bytes().split(b"\0") if arg]
            if not argv or not Path(argv[0]).name.startswith("python") or not any(Path(arg).name == "38_run10_chat_rental.py" for arg in argv):
                continue
            env = dict(entry.split(b"=", 1) for entry in (p / "environ").read_bytes().split(b"\0") if b"=" in entry)
            if (env.get(b"RUN_ROOT"), env.get(b"RUN10_LEASE")) != (b"slop/eval/run11", b"lease1"):
                continue
            if argv[-1] == "attach": controllers.append(int(p.name))
            if argv[-1] == "snapshot": snapshots.append(int(p.name))
        except (FileNotFoundError, ProcessLookupError):
            continue
    assert len(controllers) == 1 and not snapshots, (controllers, snapshots)
    assert subprocess.run(["tmux", "has-session", "-t", "=run11_controller_ordered"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0
    source = Path(__file__).with_name("remaining_stages.py").read_bytes()
    upload = "import sys; from pathlib import Path; b=sys.stdin.buffer.read(); compile(b,'remaining_stages.py','exec'); p=Path('/workspace/cg/runs/run10/remaining_stages.py'); t=p.with_suffix('.py.tmp'); t.write_bytes(b); t.replace(p); Path('/workspace/heartbeat').touch()"
    subprocess.run(ssh + [host, "python -c " + shlex.quote(upload)], input=source, check=True, timeout=30)
    fd = os.pidfd_open(controllers[0])
    # Skip the old controller's teardown while ownership transfers. -- PI/OpenAI
    os.kill(controllers[0], signal.SIGKILL)
    assert select.select([fd], [], [], 10)[0], "Old local controller has not exited"
    os.close(fd)
    replacement = remote("replace")
    print(replacement.stdout, flush=True)
    local_exit = rental.OUT / "box_runs/job.exit"
    if local_exit.exists():
        local_exit.rename(local_exit.with_name("before_document_priority.job.exit"))
    command = f"cd {shlex.quote(str(ROOT))} && . .local/run11_lease1_env.sh && uv run --no-project scripts/eval/38_run10_chat_rental.py attach >> slop/eval/run11/lease1/controller.log 2>&1; echo CONTROLLER EXIT $? >> slop/eval/run11/lease1/controller.log"
    subprocess.run(["tmux", "new-session", "-d", "-s", "run11_controller_ordered", command], check=True)
    (rental.OUT / "ordered_handover_local.json").write_text(json.dumps({"old_controller_pid": controllers[0], "remote": json.loads(replacement.stdout), "controller_tmux": "run11_controller_ordered"}, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preflight-only", action="store_true")
    main(parser.parse_args().preflight_only)
