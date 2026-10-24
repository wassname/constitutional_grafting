"""Pause only the launcher; its current Stoic training child keeps running. -- PI/OpenAI"""
import json
import os
import signal
from datetime import datetime, timezone
from pathlib import Path

root = Path("/workspace/cg")
candidates = []
for p in Path("/proc").iterdir():
    if not p.name.isdigit():
        continue
    try:
        argv = (p / "cmdline").read_bytes().split(b"\0")
        if len(argv) >= 2 and Path(argv[0].decode()).name == "bash" and argv[1] == b"scripts/train/14_run10_chat_box.sh":
            candidates.append(p)
    except (ProcessLookupError, FileNotFoundError):
        continue
assert len(candidates) == 1, candidates
parent = candidates[0]
children = []
for p in Path("/proc").iterdir():
    if not p.name.isdigit():
        continue
    try:
        status = dict(line.split(":", 1) for line in (p / "status").read_text().splitlines() if ":" in line)
        argv = (p / "cmdline").read_bytes().split(b"\0")
        if int(status["PPid"]) == int(parent.name) and any(b"cfg_r10_x11_mix_stoic.yml" in arg for arg in argv):
            children.append({"pid": int(p.name), "state": status["State"].strip()})
    except (ProcessLookupError, FileNotFoundError):
        continue
assert len(children) == 1 and not children[0]["state"].startswith("T"), children
assert not (root / "runs/run10/job.exit").exists()
env = dict(v.split(b"=", 1) for v in (parent / "environ").read_bytes().split(b"\0") if b"=" in v)
keys = ("DONOR", "TAG", "DOCS", "CHATS", "TRAIN_DIR", "BASELOSS", "CELLS", "EVAL_DEADLINE_EPOCH")
record = {"author": "PI/OpenAI", "at": datetime.now(timezone.utc).isoformat(), "paused_launcher_pid": int(parent.name),
          "running_training_child": children[0], "original_environment": {k: env[k.encode()].decode() for k in keys},
          "reason": "Pause at the next completed-document boundary to put funded document evaluations before the oversized chat-training block; current training is not stopped."}
os.kill(int(parent.name), signal.SIGSTOP)
(root / "runs/run10/launcher_boundary_pause.json").write_text(json.dumps(record, indent=2) + "\n")
print(json.dumps(record), flush=True)
