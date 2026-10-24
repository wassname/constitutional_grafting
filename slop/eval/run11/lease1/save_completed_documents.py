"""Save completed document adapters while the existing lease continues. -- PI/OpenAI"""
import importlib.util
import json
import shlex
import subprocess
from pathlib import Path

root = Path.cwd()
out = root / "slop/eval/run11/lease1"
state = json.loads((root / ".local/run10_lease1_rental.json").read_text())
names = ["r10_x11_replay_ctl", "r10_x11_mix_const"]
ssh = ["ssh", "-i", str(Path.home() / ".ssh/id_vast"), "-o", "BatchMode=yes", "-o", "ConnectTimeout=10",
       "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=3", "-o", "StrictHostKeyChecking=accept-new",
       "-o", f"UserKnownHostsFile={root / '.local/run10_known_hosts'}", "-p", str(state["ssh_port"])]
host = "root@" + state["ssh_host"]
code = f"""import hashlib,json
from pathlib import Path
root=Path('/workspace/cg')
stages=(root/'runs/run10/stages.log').read_text()
names={names!r}
for name in names:
    assert 'done train doc '+name.removeprefix('r10_x11_') in stages, name
print(json.dumps({{name:{{f.name:{{'bytes':f.stat().st_size,'sha256':hashlib.file_digest(f.open('rb'),'sha256').hexdigest()}} for f in [(root/'outputs'/name/'adapter_config.json'),(root/'outputs'/name/'adapter_model.safetensors')]}} for name in names}}))
"""
result = subprocess.run(ssh + [host, "python -c " + shlex.quote(code)], check=True, capture_output=True, text=True, timeout=180)
manifest = json.loads(result.stdout)
(out / "partial_remote_adapter_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
spec = importlib.util.spec_from_file_location("rental", root / "scripts/eval/38_run10_chat_rental.py")
rental = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rental)
for name in names:
    destination = rental.ADAPTER_DIR / name
    destination.mkdir(parents=True, exist_ok=True)
    print("COPY " + name, flush=True)
    subprocess.run(["rsync", "-az", "--partial", "--include=adapter_config.json", "--include=adapter_model.safetensors",
                    "--exclude=*", "-e", shlex.join(ssh), host + ":/workspace/cg/outputs/" + name + "/", str(destination) + "/"],
                   check=True, timeout=1800)
rental.verify_downloaded_adapters(manifest, rental.ADAPTER_DIR)
receipt = {"author": "PI/OpenAI", "instance_id": state["instance_id"], "scope": "Only the two completed document adapters; lease still running, not final retrieval.",
           "all_listed_hashes_match": True, "manifest": manifest}
(out / "partial_adapter_retrieval_verified.json").write_text(json.dumps(receipt, indent=2) + "\n")
print("VERIFIED completed document adapters: " + ", ".join(names), flush=True)
