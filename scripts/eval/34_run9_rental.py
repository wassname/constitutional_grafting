"""Run 9: train subset grafts and evaluate coalitions on one finite rental lease (adapted from 30_run8_rental.py). -- PI/Claude (Opus 5.5)

uv run --no-project scripts/eval/34_run9_rental.py run --hours 8
uv run --no-project scripts/eval/34_run9_rental.py destroy
No project API key is copied to the GPU box. Model calls and training APIs are absent.
"""
import argparse
import concurrent.futures
import hashlib
import io
import json
import os
import shlex
import subprocess
import tarfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUTS = ROOT / "slop/eval/run8"
LEASE = os.environ.get('RUN9_LEASE', 'initial')
assert LEASE.replace('_', '').isalnum(), LEASE
OUT = ROOT / 'slop/eval/run9' / ('' if LEASE == 'initial' else LEASE)
STATE = ROOT / '.local' / f'run9_{LEASE}_rental.json'
BUDGET_USD = 50
ADAPTER_DIR = Path.home() / '.local/share/cg_run9_adapters'
SUBSETS = ['echo', 'stoic', 'opus', 'greek', 'joint']
IMAGE = "axolotlai/axolotl:main-20261009-py3.12-cu130-2.14.1"
LABEL = "cg-run9-subsets-50usd" + ('' if LEASE == 'initial' else '-' + LEASE)
FIELDS = ["id", "actual_status", "intended_status", "dph_total", "total_dph", "start_date", "disk_space", "disk_usage", "inet_up", "inet_down", "gpu_name", "gpu_ram", "cost_per_hour"]


def api(path, method="GET", body=None):
    entries = dict(line.split("=", 1) for line in (ROOT / ".env").read_text().splitlines() if "=" in line and not line.startswith("#"))
    key = entries["VASTAI_API_KEY"].strip().strip('"').strip("'")
    req = urllib.request.Request("https://console.vast.ai/api/v0" + path,
        data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as f:
                return json.load(f)
        except urllib.error.HTTPError as error:
            if method != 'GET' or error.code not in {429, 500, 502, 503, 504} or attempt == 5:
                raise
            delay = min(120, max(float(error.headers.get('Retry-After', 60)), 30 * 2**attempt))
            print(f'Provider GET {path.split("?")[0]} returned {error.code}; retry in {delay:g}s ({attempt + 1}/6).', flush=True)
            time.sleep(delay)


def destroy():
    live = api("/instances/")["instances"]
    matches = [r for r in live if r['label'] == LABEL]
    assert len(matches) <= 1, "multiple rentals with this lease's exact label: inspect before teardown"
    if not matches:
        print('No rental exists for this lease.', flush=True)
        return
    instance_id = matches[0]['id']
    if any(r["id"] == instance_id for r in live):
        result = api(f"/instances/{instance_id}/", "DELETE", {})
        (OUT / "destroy_response.json").write_text(json.dumps(result, indent=2))
        assert result["success"], result
    assert all(r["id"] != instance_id for r in api("/instances/")["instances"])
    print(f"RENTAL DESTROYED {instance_id}", flush=True)


def run(hours=8):
    assert 1 <= hours <= 12, hours
    OUT.mkdir(parents=True, exist_ok=True); STATE.parent.mkdir(parents=True, exist_ok=True)
    assert not STATE.exists(), "existing rental state: inspect it before creating another lease"
    assert (INPUTS / "manifest.json").exists(), "run-8 frozen inputs missing"
    account = api("/users/current/")
    q = {"gpu_ram": {"gte": 90000}, "num_gpus": {"eq": 1}, "rentable": {"eq": True}, "verified": {"eq": True},
         "reliability2": {"gte": 0.98}, "disk_space": {"gte": 300}, "disk_bw": {"gte": 500},
         "cpu_ram": {"gte": 110000}, "inet_down": {"gte": 500}, "duration": {"gte": 259200},
         "datacenter": {"eq": True}, "allocated_storage": 300, "order": [["dph_total", "asc"]], "limit": 50}
    offers = api("/bundles/?q=" + urllib.parse.quote(json.dumps(q)))["offers"]
    offers = [r for r in offers if r['gpu_name'] == 'RTX PRO 6000 S' and r["inet_down_cost"] <= 0.005 and r["inet_up_cost"] <= 0.005 and r["cuda_max_good"] >= 13.0]
    assert offers, "no suitable low-bandwidth-cost datacentre offer"
    offer = min(offers, key=lambda r: r["dph_total"])
    rate = offer["dph_total"]
    assert hours * rate + 2 <= min(BUDGET_USD, account["credit"] - 1), "lease plus bandwidth reserve exceeds the $50 Vast allowance or credit"
    (OUT / "rental_quote.json").write_text(json.dumps({"offer": offer, "image": IMAGE, "account_credit_before": account["credit"],
        "maximum_hours": hours, "rental_plus_bandwidth_reserve_usd": hours * rate + 2, "vast_cap_usd": BUDGET_USD}, indent=2))
    print(f"Quote: {offer['gpu_name']}, datacentre {offer['geolocation']}, ${rate:.3f}/h including 300 GB; {hours:g}-hour reserve ${hours * rate + .6:.2f}", flush=True)
    body = {"client_id": "me", "image": IMAGE, "disk": 300, "label": LABEL, "runtype": "ssh_direct", "cancel_unavail": True}
    created_at = time.time()
    try:
        created = api(f"/asks/{offer['id']}/", "PUT", body)
        assert created["success"], created
        state = {"instance_id": created["new_contract"], "created_epoch": created_at, "hard_destroy_epoch": created_at + hours * 3600,
                 "runner_deadline_epoch": created_at + (hours - .5) * 3600, "hourly_rate": rate, "image": IMAGE}
        STATE.write_text(json.dumps(state, indent=2)); os.chmod(STATE, 0o600)
        (OUT / "lease.json").write_text(json.dumps(state, indent=2))
    except BaseException:
        destroy()
        raise
    print(f"RENTAL CREATED {state['instance_id']}; hard destruction deadline {state['hard_destroy_epoch']}", flush=True)
    ssh = None
    stop = threading.Event()
    heartbeat = None

    def remaining():
        return max(1, state["runner_deadline_epoch"] - time.time())

    def remote(command, timeout=None, **kwargs):
        return subprocess.run(ssh + [host, command], check=True, timeout=min(timeout or remaining(), remaining()), **kwargs)

    def keep_alive():
        while not stop.wait(60):
            try:
                remote("touch /workspace/heartbeat", timeout=15, stdout=subprocess.DEVNULL)
            except subprocess.TimeoutExpired as error:
                print(f'Heartbeat transport timeout: {error}', flush=True)
            except subprocess.CalledProcessError as error:
                if error.returncode != 255:
                    raise
                print('Heartbeat SSH disconnected; next minute will retry.', flush=True)

    try:
        ready_by = time.time() + 1800
        previous = None
        while time.time() < ready_by:
            instance = next(r for r in api("/instances/")["instances"] if r["id"] == state["instance_id"])
            status = instance["actual_status"]
            if status != previous:
                print(f"Rental status: {status}", flush=True); previous = status
            if status == "running":
                ports = instance.get("ports") or {}
                if ports.get("22/tcp"):
                    address, port = instance["public_ipaddr"], ports["22/tcp"][0]["HostPort"]
                elif instance.get("ssh_host") and instance.get("ssh_port"):
                    address, port = instance["ssh_host"], instance["ssh_port"]
                else:
                    time.sleep(60); continue
                host = f"root@{address}"
                ssh = ["ssh", "-i", str(Path.home() / ".ssh/id_vast"), "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=30", "-o", "ServerAliveCountMax=3",
                       "-o", "StrictHostKeyChecking=accept-new", "-o", f"UserKnownHostsFile={ROOT / '.local/run9_known_hosts'}", "-p", str(port)]
                if subprocess.run(ssh + [host, "true"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15).returncode == 0:
                    break
            time.sleep(60)
        else:
            raise TimeoutError("rental image/SSH did not become ready in 30 minutes")
        state.update({"ssh_host": address, "ssh_port": port}); STATE.write_text(json.dumps(state, indent=2))
        remote("set -e; nvidia-smi; python -c 'import torch; print(torch.__version__, torch.version.cuda); assert torch.cuda.get_device_properties(0).total_memory > 90*1024**3'; dd if=/dev/zero of=/workspace/cg_disk_check bs=1G count=10 oflag=direct status=progress; rm /workspace/cg_disk_check", timeout=180)
        remote("command -v rsync && command -v tmux || (apt-get update -qq && apt-get install -y -qq rsync tmux)", timeout=180)
        code = ["scripts/train/02_merge.py", "scripts/train/box_watchdog.sh", "scripts/eval/19_gen_replies.py",
                "scripts/eval/26_gsm8k.py", "scripts/eval/33_subset_cells.py", "tests/regression/test_moe_expert_merge.py",
                "scripts/train/11_run9_box.sh", "configs/train/qwen3/graft.yml", "configs/train/demo_prompts.json",
                "scripts/train/demo_plugin.py", "scripts/train/spectral_plugin.py", "scripts/train/router_dtype_plugin.py",
                "scripts/train/41_expert_adapter_check.py", "scripts/train/43_adapter_energy.py", "scripts/train/44_energy_doses.py",
                ]
        code += [str(q.relative_to(ROOT)) for q in [ROOT / "scripts/__init__.py", ROOT / "scripts/train/__init__.py"] if q.exists()]
        source_hashes = {}
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w:gz") as tar:
            for name in code:
                tar.add(ROOT / name, arcname=name)
                source_hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for path in INPUTS.iterdir():
                if path.name in {"items.jsonl", "boundary_items.jsonl", "demos.jsonl", "panel.jsonl", "pov.jsonl", "change.md", "gsm8k_long60.jsonl", "gsm8k_long60.jsonl.meta.json"}:
                    tar.add(path, arcname="runs/run9/" + path.name)
            tar.add(INPUTS / "manifest.json", arcname="runs/run9/run8_manifest.json")
        (OUT / "executed_source_sha256.json").write_text(json.dumps(source_hashes, indent=2))
        remote("mkdir -p /workspace/cg; tar -xzf - -C /workspace/cg", input=stream.getvalue(), timeout=60)
        remote("touch /workspace/heartbeat; tmux new-session -d -s run9_watchdog 'cd /workspace/cg && MAX_SILENT_H=1 bash scripts/train/box_watchdog.sh > runs/run9/watchdog.log 2>&1'", timeout=30)
        remote("""python - <<'PY'
import subprocess, time
from pathlib import Path
p = Path('/workspace/cg/runs/run9/watchdog.log')
for _ in range(50):
    if p.exists() and 'auth check GET:' in p.read_text():
        text = p.read_text()
        print(text)
        assert 'auth check GET: 200' in text, text
        subprocess.run(['tmux', 'has-session', '-t', 'run9_watchdog'], check=True)
        break
    time.sleep(0.2)
else:
    raise TimeoutError('watchdog authentication was not confirmed')
PY""", timeout=20)
        heartbeat = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        heartbeat_future = heartbeat.submit(keep_alive)


        def setup():
            script = """set -euo pipefail
export HF_HOME=/workspace/hf UV_EXCLUDE_NEWER='8 days'
command -v uv
uv venv /opt/vllm --python 3.12
uv pip install --python /opt/vllm/bin/python vllm==0.31.0
python - <<'PY'
from huggingface_hub import snapshot_download
from pathlib import Path
import json
manifest = json.loads(Path('/workspace/cg/runs/run9/run8_manifest.json').read_text())
p = snapshot_download('Qwen/Qwen3.5-35B-A3B', revision=manifest['instruct_revision'], ignore_patterns=['*.gguf', '*.bin', '*.onnx'], max_workers=16)
Path('/workspace/run9_instruct_path').write_text(p)
print('Pinned Instruct snapshot:', p)
b = snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422', ignore_patterns=['*.gguf', '*.bin', '*.onnx'], max_workers=16)
print('Pinned Base snapshot:', b)
PY
python -c 'import axolotl, yaml; print("axolotl", axolotl.__version__)'
python -c 'import torch,peft,transformers; print(torch.__version__,peft.__version__,transformers.__version__)'
/opt/vllm/bin/python -c 'import vllm; print(vllm.__version__)'
cd /workspace/cg
python tests/regression/test_moe_expert_merge.py
"""
            with (OUT / "setup.log").open("w") as f:
                remote("bash -s", input=script, text=True, stdout=f, stderr=subprocess.STDOUT)
            print("SETUP COMPLETE: pinned Instruct and Base, inference environment and remote CPU regression", flush=True)

        try:
            setup()
        except Exception:
            stop.set()
            destroy()
            raise
        if heartbeat_future.done():
            heartbeat_future.result()
        # The box can set up while reviewed training data is finalised locally; upload it once data/subsets/train_manifest.json exists.
        manifest_path = ROOT / "data/subsets/train_manifest.json"
        while not manifest_path.exists():
            assert remaining() > 4 * 3600, "training data not ready with enough lease left for training and evaluation"
            print("Waiting for data/subsets/train_manifest.json", flush=True)
            stop.wait(120)
        train_manifest = json.loads(manifest_path.read_text())
        assert set(train_manifest["subsets"]) == set(SUBSETS), train_manifest["subsets"].keys()
        data = ["data/subsets/train_manifest.json"] + [f"data/subsets/train_{s}.jsonl" for s in SUBSETS]
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w:gz") as tar:
            for name in data:
                tar.add(ROOT / name, arcname=name)
        (OUT / "uploaded_data_sha256.json").write_text(json.dumps({n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in data}, indent=2))
        remote("tar -xzf - -C /workspace/cg", input=stream.getvalue(), timeout=120)
        print("DATA UPLOADED: " + json.dumps({k: (v["docs"], v["tokens_incl_eos"]) for k, v in train_manifest["subsets"].items()}), flush=True)
        command = (f"cd /workspace/cg && HF_HOME=/workspace/hf RUN9_INSTRUCT_PATH=$(cat /workspace/run9_instruct_path) "
                   f"INCUMBENT_ENERGY={os.environ['INCUMBENT_ENERGY']} RUN9_DEADLINE_EPOCH={state['runner_deadline_epoch']} bash scripts/train/11_run9_box.sh")
        script = f'set +e; {command} > runs/run9/job.log 2>&1; status=$?; echo $status > runs/run9/job.exit; tmux wait-for -S run9_done; exit $status'
        remote('cd /workspace/cg && tmux new-session -d -s run9_eval ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
        previous = set()
        last_stages = None
        failures = 0
        while remaining() > 1:
            try:
                result = remote("cd /workspace/cg && python -c " + shlex.quote("import json, subprocess; from pathlib import Path; p=Path('runs/run9'); print(json.dumps({'exit': (p/'job.exit').read_text().strip() if (p/'job.exit').exists() else None, 'running': subprocess.run(['tmux','has-session','-t','run9_eval'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0, 'completed': {f.stem: json.loads(f.read_text()) for f in p.glob('r9_*.done')}, 'stages': (p/'stages.log').read_text().splitlines()[-2:] if (p/'stages.log').exists() else []}))"), timeout=30, capture_output=True, text=True)
            except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as error:
                if isinstance(error, subprocess.CalledProcessError) and error.returncode != 255:
                    raise
                failures += 1
                print(f'SSH transport interrupted ({failures}/10); detached comparison remains owned.', flush=True)
                assert failures < 10, 'SSH unavailable for repeated status checks'
            else:
                failures = 0
                status = json.loads(result.stdout)
                for tag in sorted(set(status['completed']) - previous):
                    print('CELL COMPLETE ' + tag + ': ' + json.dumps(status['completed'][tag]), flush=True)
                if status['stages'] != last_stages:
                    print('STAGE ' + ' | '.join(status['stages']), flush=True)
                    last_stages = status['stages']
                previous = set(status['completed'])
                if status['exit'] is not None:
                    assert status['exit'] == '0', f"remote comparison exited {status['exit']}; inspect job.log"
                    break
                assert status['running'], 'detached comparison disappeared without an exit record'
            if heartbeat_future.done():
                heartbeat_future.result()
            stop.wait(45)
        else:
            raise TimeoutError('comparison reached runner deadline')
    finally:
        stop.set()
        if heartbeat:
            heartbeat.shutdown(wait=True)
        try:
            live = [r for r in api("/instances/")["instances"] if r["id"] == state["instance_id"]]
            if live and ssh is not None:
                with (OUT / 'shutdown_diagnostics.log').open('w') as diagnostics:
                    subprocess.run(ssh + [host, 'nvidia-smi; free -h; df -h /workspace; dmesg -T 2>&1 | tail -80'], stdout=diagnostics, stderr=subprocess.STDOUT, timeout=30)
                subprocess.run(["rsync", "-az", "--exclude=merged_model", "-e", shlex.join(ssh), host + ":/workspace/cg/runs/run9/", str(OUT / "box_runs") + "/"],
                               check=True, timeout=600)
                ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
                with (OUT / 'adapter_download.log').open('w') as f:  # final adapters first, then per-epoch checkpoints for later attribution
                    for pattern in ["adapter_*", "checkpoint-*/adapter_*", "checkpoint-*/trainer_state.json"]:
                        subprocess.run(["rsync", "-az", "--partial", "-e", shlex.join(ssh), "--include=*/", f"--include=r9_*/{pattern}", "--exclude=*",
                                        host + ":/workspace/cg/outputs/", str(ADAPTER_DIR) + "/"], stdout=f, stderr=subprocess.STDOUT, timeout=3600)
            for latest in live:
                (OUT / "last_instance_metrics.json").write_text(json.dumps({k: latest[k] for k in FIELDS if k in latest}, indent=2))
        finally:
            destroy()
            after = api("/users/current/")
            (OUT / "account_credit_after.json").write_text(json.dumps({"credit": after["credit"], "before": account["credit"],
                "elapsed_hours": (time.time() - created_at) / 3600, "credit_difference_not_reconciled_invoice": account["credit"] - after["credit"]}, indent=2))
    print("RETRIEVAL COMPLETE; rental destroyed. No aggregate character result until reply and judge review.", flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["run", "destroy"])
    parser.add_argument('--hours', type=float, default=5)
    args = parser.parse_args()
    run(args.hours) if args.action == 'run' else destroy()
