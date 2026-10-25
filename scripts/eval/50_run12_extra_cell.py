"""Run the approved quarter-dose cell on the existing held worker. PI/OpenAI (Sol)."""
import importlib.util
import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "slop/eval/run12/run12gen"
CELL = "stoic=0.5,const=1,other=1,x12_chatmix=0.25,x12_chatgen=-0.25"
TAG = "r10_stoic0.5_const1_other1_x12_chatmix0.25_x12_chatgen-0.25"
SESSION = "run12_extra025"
CHANNEL = "run12_extra025_done"


def main():
    assert os.environ["RUN10_LEASE"] == "run12gen"
    spec = importlib.util.spec_from_file_location("rental", ROOT / "scripts/eval/38_run10_chat_rental.py")
    rental = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rental)
    state = json.loads(rental.STATE.read_text())
    guard = json.loads((OUT / "deadline_guard_armed.json").read_text())
    assert state["instance_id"] == guard["instance_id"] == 57641120
    assert state["hard_destroy_epoch"] == guard["deadline_epoch"]
    report = (OUT / "box_runs/run.md").read_text()
    resolved = json.loads(re.search(r"```json\n(.*?)\n```", report, re.S)[1])
    deadline = resolved["deadline_epoch"]
    assert abs(deadline - (state["hard_destroy_epoch"] - 4400)) < 1
    assert deadline - time.time() > 1200
    argv = resolved["argv"][:resolved["argv"].index("--cells") + 1] + [CELL]
    assert argv[0] == "scripts/eval/33_subset_cells.py"
    script = (
        "set +e\ncd /workspace/cg\n"
        'export PYTHONPATH="$PWD${PYTHONPATH:+:$PYTHONPATH}" HF_HOME=/workspace/hf CELL_PREFIX=r10_\n'
        f"export RUN9_INSTRUCT_PATH={shlex.quote(resolved['model_path'])} RUN9_DEADLINE_EPOCH={deadline}\n"
        + shlex.join(["python", *argv]) + " > runs/run10/extra025.log 2>&1\n"
        "status=$?\nprintf '%s\\n' \"$status\" > runs/run10/extra025.exit\n"
        f"tmux wait-for -S {CHANNEL}\nexit \"$status\"\n"
    )
    remote_code = (
        "import json,pathlib,shlex,subprocess; "
        "e=dict(x.split('=',1) for x in pathlib.Path('/proc/1/environ').read_text().split(chr(0)) if '=' in x); "
        "assert int(e['CONTAINER_ID'])==57641120; p=pathlib.Path('/workspace/cg/runs/run10'); "
        "assert not (p/'eval_release.done').exists(); assert not (p/'extra025.exit').exists(); "
        f"assert not list(p.glob('*{TAG}*')), 'preserve existing quarter-dose artifacts'; "
        "subprocess.run(['tmux','has-session','-t','run10_train'],check=True); "
        f"script={script!r}; (p/'extra025.command.sh').write_text(script); "
        f"subprocess.run(['tmux','new-session','-d','-s',{SESSION!r},'bash -lc '+shlex.quote(script)],check=True)"
    )
    ssh, host = rental.saved_connection(state)
    request = {"author": "PI/OpenAI (Sol)", "instance_id": state["instance_id"],
               "authorized_by": "const_v2 approval 2026-10-25T20:43:02Z; one extra only",
               "cell": CELL, "argv": argv, "deadline_epoch": deadline, "script": script,
               "requested_epoch": time.time()}
    path = OUT / "extra025_launch.json"
    assert not path.exists(), "inspect the existing launch; never duplicate the extra job"
    path.write_text(json.dumps(request, indent=2) + "\n")
    subprocess.run(ssh + [host, "python -c " + shlex.quote(remote_code)], check=True, timeout=45)
    request["launched_epoch"] = time.time()
    path.write_text(json.dumps(request, indent=2) + "\n")
    print("EXTRA QUARTER-DOSE CELL STARTED ON EXISTING WORKER", flush=True)
    result = subprocess.run(ssh + [host, f"tmux wait-for {CHANNEL}; cat /workspace/cg/runs/run10/extra025.exit"],
                            check=True, capture_output=True, text=True, timeout=deadline - time.time())
    assert result.stdout.strip() == "0", result.stdout
    request["completed_epoch"] = time.time()
    request["exit"] = 0
    path.write_text(json.dumps(request, indent=2) + "\n")
    print("EXTRA QUARTER-DOSE CELL COMPLETE; SNAPSHOT REQUIRED", flush=True)


if __name__ == "__main__":
    main()
