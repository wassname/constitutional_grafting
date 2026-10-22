"""Run 10 stage 2: chat adapter(s) on Base + A_STOIC·ΔStoic, then grafts onto Instruct, on one finite rental lease (from 37_run10_rental.py).
Uploads the stage-1 ΔStoic (sha-verified) to outputs/up_stoic. Box job: scripts/train/14_run10_chat_box.sh. -- PI/Claude (Opus 5.5)

CHATS="chat12 chatgen12" CELLS="stoic=2,chat12=2.5 ..." uv run --no-project scripts/eval/38_run10_chat_rental.py run --hours 10
uv run --no-project scripts/eval/38_run10_chat_rental.py destroy
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
LEASE = os.environ.get('RUN10_LEASE', 'stage2')
STAGE = 'subsets'
assert LEASE.replace('_', '').isalnum(), LEASE
OUT = ROOT / 'slop/eval/run10' / LEASE
STATE = ROOT / '.local' / f'run10_{LEASE}_rental.json'
BUDGET_USD = 80  # run-10 Vast lease reserves, within wassname's $100 GPU budget (raised from 60 on 2026-10-23 for the complex-path retry)
ADAPTER_DIR = Path.home() / '.local/share/cg_run10_adapters'
SUBSETS = os.environ.get('CHATS', 'chat12 chatgen12').split()  # chat adapters trained this lease (retrieved as r10_<name>)
A_STOIC = os.environ.get('A_STOIC', '2')
DONOR = os.environ.get('DONOR', f'stoic={A_STOIC}')  # stage-1 adapters merged into Base for chat training, e.g. 'stoic=2 const=1 other=1'
TAG = os.environ.get('TAG', '')
EXTRA = os.environ.get('EXTRA', '').split()  # already-trained run-10 chat adapters to upload for eval cells only, e.g. 'chat12 chatgen12'  # chat adapter prefix: complex path TAG=cx_ -> r10_cx_chat12
CELLS = os.environ.get('CELLS', f'stoic={A_STOIC},chat12=2.5 stoic={A_STOIC},chatgen12=2.5 stoic={A_STOIC},chat12=1 chat12=2.5 stoic={A_STOIC},chat12=4')
_VERIFIED = json.loads((ROOT / 'slop/eval/run10/stage1/retrieval_verified.json').read_text())['manifest']
DONOR_SRC = {  # name -> (local dir, sha256 per file from the training lease's own record)
    'stoic': (Path.home() / '.local/share/cg_run10_adapters/r10_stoic', {f: v['sha256'] for f, v in _VERIFIED['r10_stoic'].items()}),
    'other': (Path.home() / '.local/share/cg_run10_adapters/r10_other', {f: v['sha256'] for f, v in _VERIFIED['r10_other'].items()}),
    # run 7e ΔConst: weights hash from slop/eval/run7e/box_runs/adapters_sha256_final.txt:2; config identical to ΔStoic's
    'const': (Path.home() / '.local/share/cg_run7e_adapters/r7e_graft_docs_spl50', {
        'adapter_model.safetensors': '5149961a47aab9f39560ae1aac3b1e63504c5d69118e64d95c1051da86e6acaa',
        'adapter_config.json': '72ee136d1f239225aee34e25cda91f1371b9e90ca04a020e492fb500045c0030'})}
IMAGE = "axolotlai/axolotl:main-20261009-py3.12-cu130-2.14.1"
LABEL = "cg-run10-" + LEASE
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
                print(f'Provider {method} {path.split("?")[0]} returned {error.code}: {error.read()[:400]!r}', flush=True)
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


def verify_downloaded_adapters(manifest, adapter_dir):
    """Verify every final binary and configuration before disk destruction. -- PI/Sol"""
    for tag, files in manifest.items():
        for filename, expected in files.items():
            path = adapter_dir / tag / filename
            with path.open('rb') as stream:
                actual = hashlib.file_digest(stream, 'sha256').hexdigest()
            assert path.stat().st_size == expected['bytes'] and actual == expected['sha256'], f'incomplete or corrupt artifact: {path}'


def retrieve_outputs(ssh, host, state):
    """Copy run evidence and final weights, then verify them against remote hashes. -- PI/Sol"""
    deadline = state['hard_destroy_epoch']
    def timeout(seconds):
        remaining = deadline - time.time() - 60
        assert remaining > 0, 'no retrieval time remains before hard destruction'
        return min(seconds, remaining)

    with (OUT / 'shutdown_diagnostics.log').open('w') as diagnostics:
        subprocess.run(ssh + [host, 'nvidia-smi; free -h; df -h /workspace; dmesg -T 2>&1 | tail -80'], stdout=diagnostics, stderr=subprocess.STDOUT, timeout=timeout(30))
    subprocess.run(['rsync', '-az', '--exclude=merged_model', '--exclude=heal_parent', '--exclude=dose_model', '--exclude=healed_model',
                    '-e', shlex.join(ssh), host + ':/workspace/cg/runs/run10/', str(OUT / 'box_runs') + '/'], check=True, timeout=timeout(600))
    prefix = 'r10_*'
    code = ("import hashlib,json; from pathlib import Path; p=Path('/workspace/cg/outputs'); "
            f"print(json.dumps({{d.name:{{f.name:{{'bytes':f.stat().st_size,'sha256':hashlib.file_digest(f.open('rb'),'sha256').hexdigest()}} "
            f"for f in [d/'adapter_config.json',d/'adapter_model.safetensors']}} for d in p.glob({prefix!r}) if (d/'adapter_model.safetensors').is_file()}}))")
    result = subprocess.run(ssh + [host, 'python -c ' + shlex.quote(code)], check=True, capture_output=True, text=True, timeout=timeout(180))
    manifest = json.loads(result.stdout)
    job_exit = OUT / 'box_runs/job.exit'
    if job_exit.exists() and job_exit.read_text().strip() == '0':
        if STAGE == 'exact':
            cells = json.loads((OUT / 'box_runs/exact_manifest.json').read_text())['required_cells']
            expected = {tag for tag in cells if tag.endswith('_healed')}
        else:
            expected = {f'r10_{TAG}{name}' for name in SUBSETS}
        assert set(manifest) == expected, 'missing or unexpected final adapters on remote'
    (OUT / 'remote_adapter_manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    ADAPTER_DIR.mkdir(parents=True, exist_ok=True)
    patterns = ['adapter_*', 'checkpoint-*/trainer_state.json'] if STAGE == 'exact' else ['adapter_*', 'checkpoint-*/adapter_*', 'checkpoint-*/trainer_state.json']
    with (OUT / 'adapter_download.log').open('w') as log:
        for pattern in patterns:
            subprocess.run(['rsync', '-az', '--partial', '-e', shlex.join(ssh), '--include=*/', f'--include={prefix}/{pattern}', '--exclude=*',
                            host + ':/workspace/cg/outputs/', str(ADAPTER_DIR) + '/'], stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=timeout(3600))
    verify_downloaded_adapters(manifest, ADAPTER_DIR)
    (OUT / 'retrieval_verified.json').write_text(json.dumps({'author': 'PI/Sol', 'all_final_adapter_hashes_match': True, 'manifest': manifest}, indent=2) + '\n')


def retrieve_or_stop(ssh, host, state):
    """A failed copy retains the stopped disk until the existing hard deadline. -- PI/Sol"""
    try:
        retrieve_outputs(ssh, host, state)
    except BaseException as error:
        (OUT / 'retrieval_failure.json').write_text(json.dumps({'author': 'PI/Sol', 'error': repr(error), 'state': state,
            'action': 'Stop and retain disk for artifact-only recovery; existing hard destruction deadline remains.'}, indent=2) + '\n')
        result = api(f"/instances/{state['instance_id']}/", 'PUT', {'state': 'stopped'})
        assert result['success'], result
        print('RETRIEVAL FAILED; instance stopped with disk retained until the existing hard destruction deadline.', flush=True)
        raise
    destroy()


def run(hours=8):
    assert 1 <= hours <= 12, hours
    OUT.mkdir(parents=True, exist_ok=True); STATE.parent.mkdir(parents=True, exist_ok=True)
    assert not STATE.exists(), "existing rental state: inspect it before creating another lease"
    account = api("/users/current/")
    q = {"gpu_ram": {"gte": 90000}, "num_gpus": {"eq": 1}, "rentable": {"eq": True}, "verified": {"eq": True},
         "reliability2": {"gte": 0.98}, "disk_space": {"gte": 300}, "disk_bw": {"gte": 500},
         "cpu_ram": {"gte": 110000}, "inet_down": {"gte": 500}, "duration": {"gte": 259200},
         "datacenter": {"eq": True}, "allocated_storage": 300, "order": [["dph_total", "asc"]], "limit": 50}
    offers = api("/bundles/?q=" + urllib.parse.quote(json.dumps(q)))["offers"]
    offers = [r for r in offers if r['gpu_name'] == 'RTX PRO 6000 S' and r["inet_down_cost"] <= 0.005 and r["inet_up_cost"] <= 0.005 and r["cuda_max_good"] >= 13.0]
    assert offers, "no suitable low-bandwidth-cost datacentre offer"
    skip = set(os.environ.get('SKIP_OFFERS', '').split())  # offers that refused a rental (HTTP 400) on an earlier attempt
    offers = [o for o in offers if str(o['id']) not in skip]
    offer = min(offers, key=lambda r: r["dph_total"])
    rate = offer["dph_total"]
    quote_paths = sorted((ROOT / 'slop/eval/run10').glob('*/rental_quote.json'))  # run-10 leases share one Vast allowance
    previous_reserve = 0.0
    for p in quote_paths:
        if not p.exists() or p.parent == OUT:
            continue
        quoted = json.loads(p.read_text())['rental_plus_bandwidth_reserve_usd']
        closed = p.parent / 'account_credit_after.json'
        if (p.parent / 'destroy_response.json').exists() and closed.exists():
            elapsed = json.loads(closed.read_text())['elapsed_hours']
            lease = json.loads((p.parent / 'lease.json').read_text())
            quoted = min(quoted, elapsed * lease['hourly_rate'] + 2)
        previous_reserve += quoted
    assert previous_reserve + hours * rate + 2 <= BUDGET_USD, 'cumulative run-10 lease reserves exceed the Vast allowance'
    # Vast auto-billing (wassname: "vast ... auto top up") charges autobill_amount once credit falls below autobill_threshold
    autobill = account['autobill_amount'] if account.get('has_billing') and not account.get('billing_failed') and account.get('autobill_threshold', 0) > 0 else 0
    print(f"credit {account['credit']:.2f} + auto-bill {autobill} available for a {hours * rate + 2:.2f} reserve", flush=True)
    assert hours * rate + 2 <= account['credit'] + autobill - 1, 'lease plus bandwidth reserve exceeds available credit (incl. auto-bill)'
    (OUT / "rental_quote.json").write_text(json.dumps({"offer": offer, "image": IMAGE, "account_credit_before": account["credit"],
        "maximum_hours": hours, "rental_plus_bandwidth_reserve_usd": hours * rate + 2, "previous_lease_reserve_usd": previous_reserve,
        "stage": STAGE, "vast_cap_usd": BUDGET_USD}, indent=2))
    print(f"Quote: {offer['gpu_name']}, datacentre {offer['geolocation']}, ${rate:.3f}/h including 300 GB; {hours:g}-hour reserve ${hours * rate + 2:.2f}", flush=True)
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
                       "-o", "StrictHostKeyChecking=accept-new", "-o", f"UserKnownHostsFile={ROOT / '.local/run10_known_hosts'}", "-p", str(port)]
                if subprocess.run(ssh + [host, "true"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15).returncode == 0:
                    break
            time.sleep(60)
        else:
            raise TimeoutError("rental image/SSH did not become ready in 30 minutes")
        state.update({"ssh_host": address, "ssh_port": port}); STATE.write_text(json.dumps(state, indent=2))
        remote("set -e; nvidia-smi; python -c 'import torch; print(torch.__version__, torch.version.cuda); assert torch.cuda.get_device_properties(0).total_memory > 90*1024**3'; dd if=/dev/zero of=/workspace/cg_disk_check bs=1G count=10 oflag=direct status=progress; rm /workspace/cg_disk_check", timeout=180)
        remote("command -v rsync && command -v tmux || (apt-get update -qq && apt-get install -y -qq rsync tmux)", timeout=180)
        code = ["scripts/train/box_watchdog.sh", "tests/regression/test_moe_expert_merge.py", "scripts/train/02_merge.py",
                "scripts/train/14_run10_chat_box.sh", "scripts/train/13_run10_evals.sh", "configs/train/qwen3/sft.yml", "configs/train/demo_prompts.json",
                "scripts/eval/19_gen_replies.py", "scripts/eval/26_gsm8k.py", "scripts/eval/33_subset_cells.py",
                "scripts/train/demo_plugin.py", "scripts/train/spectral_plugin.py", "scripts/train/router_dtype_plugin.py",
                "scripts/train/41_expert_adapter_check.py", "scripts/train/43_adapter_energy.py"]
        code += [str(q.relative_to(ROOT)) for q in [ROOT / "scripts/__init__.py", ROOT / "scripts/train/__init__.py"] if q.exists()]
        source_hashes = {}
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w:gz") as tar:
            for name in code:
                tar.add(ROOT / name, arcname=name)
                source_hashes[name] = hashlib.sha256((ROOT / name).read_bytes()).hexdigest()
            for f in ["items.jsonl", "boundary_items.jsonl", "demos.jsonl", "panel.jsonl", "pov.jsonl", "change.md", "gsm8k_long60.jsonl", "gsm8k_long60.jsonl.meta.json"]:
                tar.add(ROOT / "slop/eval/run8" / f, arcname="runs/run10/" + f)
            tar.add(ROOT / "slop/eval/run8/manifest.json", arcname="runs/run10/run8_manifest.json")
        (OUT / "executed_source_sha256.json").write_text(json.dumps(source_hashes, indent=2))
        remote("mkdir -p /workspace/cg/runs/run10; tar -xzf - -C /workspace/cg", input=stream.getvalue(), timeout=60)
        remote("touch /workspace/heartbeat; tmux new-session -d -s run10_watchdog 'cd /workspace/cg && MAX_SILENT_H=1 bash scripts/train/box_watchdog.sh > runs/run10/watchdog.log 2>&1'", timeout=30)
        remote("""python - <<'PY'
import subprocess, time
from pathlib import Path
p = Path('/workspace/cg/runs/run10/watchdog.log')
for _ in range(50):
    if p.exists() and 'auth check GET:' in p.read_text():
        text = p.read_text()
        print(text)
        assert 'auth check GET: 200' in text, text
        subprocess.run(['tmux', 'has-session', '-t', 'run10_watchdog'], check=True)
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
python - <<'PY'
from huggingface_hub import snapshot_download
if True:
    b = snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422', ignore_patterns=['*.gguf', '*.bin', '*.onnx'], max_workers=16)
    print('Pinned Base snapshot:', b)
PY
python -c 'import axolotl, yaml; print("axolotl", axolotl.__version__)'
python -c 'import torch,peft,transformers; print(torch.__version__,peft.__version__,transformers.__version__)'
cd /workspace/cg
python tests/regression/test_moe_expert_merge.py
"""
            with (OUT / "setup.log").open("w") as f:
                remote("bash -s", input=script, text=True, stdout=f, stderr=subprocess.STDOUT)
            print("SETUP COMPLETE: pinned Base and remote CPU regression", flush=True)

        try:
            setup()
        except Exception:
            stop.set()
            destroy()
            raise
        if heartbeat_future.done():
            heartbeat_future.result()
        remote("cd /workspace/cg && tmux new-session -d -s run10_prep 'bash scripts/train/13_run10_evals.sh prep > runs/run10/prep.log 2>&1'", timeout=30)
        _chat_verified = json.loads((ROOT / 'slop/eval/run10/stage2/retrieval_verified.json').read_text())['manifest'] if EXTRA else {}
        for name, (src, sha) in [(n, DONOR_SRC[n]) for n in sorted({d.split('=')[0] for d in DONOR.replace('|', ' ').split()})] + [
                (n, (Path.home() / f'.local/share/cg_run10_adapters/r10_{n}', {f: v['sha256'] for f, v in _chat_verified[f'r10_{n}'].items()})) for n in EXTRA]:
            remote(f'mkdir -p /workspace/cg/outputs/up_{name}', timeout=30)
            for attempt in range(3):  # rsync --partial resumes; one broken pipe ended lease 57231438
                with (OUT / f'upload_{name}.log').open('a') as stream:
                    done = subprocess.run(['rsync', '-az', '--partial', '-e', shlex.join(ssh), str(src / 'adapter_config.json'), str(src / 'adapter_model.safetensors'),
                                           host + f':/workspace/cg/outputs/up_{name}/'], stdout=stream, stderr=subprocess.STDOUT, timeout=remaining()).returncode == 0
                if done:
                    break
                print(f'{name} upload attempt {attempt + 1} failed; retrying', flush=True); time.sleep(30)
            assert done, f'{name} adapter upload failed 3 times'
            for f in ['adapter_model.safetensors', 'adapter_config.json']:
                code = f"import hashlib; p='/workspace/cg/outputs/up_{name}/{f}'; a=hashlib.file_digest(open(p,'rb'),'sha256').hexdigest(); assert a == {sha[f]!r}, a; print(a)"
                remote('python -c ' + shlex.quote(code), timeout=300)
            print(f'{name.upper()} ADAPTER UPLOADED AND VERIFIED', flush=True)
        manifest_path = ROOT / "data/train/run10/manifest.json"
        train_manifest = json.loads(manifest_path.read_text())
        for name in SUBSETS:  # upload exactly the files the manifest hashed
            assert hashlib.sha256((ROOT / f"data/train/run10/{name}.jsonl").read_bytes()).hexdigest() == train_manifest[name]["sha256"], name
        data = ["data/train/run10/manifest.json"] + [f"data/train/run10/{s}.jsonl" for s in SUBSETS]
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w:gz") as tar:
            for name in data:
                tar.add(ROOT / name, arcname=name)
        (OUT / "uploaded_data_sha256.json").write_text(json.dumps({n: hashlib.sha256((ROOT / n).read_bytes()).hexdigest() for n in data}, indent=2))
        remote("tar -xzf - -C /workspace/cg", input=stream.getvalue(), timeout=120)
        print("DATA UPLOADED: " + json.dumps({k: (train_manifest[k]["rows"], train_manifest[k]["words"]) for k in SUBSETS}), flush=True)
        command = (f"cd /workspace/cg && HF_HOME=/workspace/hf DONOR={shlex.quote(DONOR)} TAG={TAG} EXTRA={shlex.quote(' '.join(EXTRA))} CHATS={shlex.quote(' '.join(SUBSETS))} CELLS={shlex.quote(CELLS)} "
                   f"EVAL_DEADLINE_EPOCH={state['hard_destroy_epoch'] - 4400:.0f} bash scripts/train/14_run10_chat_box.sh")
        script = f'set +e; {command} > runs/run10/job.log 2>&1; status=$?; echo $status > runs/run10/job.exit; exit $status'
        remote('cd /workspace/cg && tmux new-session -d -s run10_train ' + shlex.quote('bash -lc ' + shlex.quote(script)), timeout=30)
        previous = set()
        last_stages = None
        last_step_print = 0.0
        failures = 0
        while remaining() > 1:
            try:
                result = remote("cd /workspace/cg && python -c " + shlex.quote("import json, subprocess; from pathlib import Path; p=Path('runs/run10'); print(json.dumps({'exit': (p/'job.exit').read_text().strip() if (p/'job.exit').exists() else None, 'running': subprocess.run(['tmux','has-session','-t','run10_train'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode == 0, 'completed': {}, 'step': ((sorted(p.glob('train_r10_*.log'), key=lambda f: f.stat().st_mtime)[-1].read_text(errors='replace')[-400:].replace(chr(13), chr(10)).splitlines() or [''])[-1] if list(p.glob('train_r10_*.log')) else ''), 'stages': (p/'stages.log').read_text(errors='replace').splitlines()[-2:] if (p/'stages.log').exists() else []}))"), timeout=30, capture_output=True, text=True)
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
                if time.time() - last_step_print > 900:
                    print('PROGRESS ' + status['step'][-200:], flush=True); last_step_print = time.time()
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
        live = [r for r in api('/instances/')['instances'] if r['id'] == state['instance_id']]
        for latest in live:
            (OUT / 'last_instance_metrics.json').write_text(json.dumps({k: latest[k] for k in FIELDS if k in latest}, indent=2))
        assert live, 'rental disappeared before artifact retrieval; local artifacts are not verified'
        if ssh is not None:
            retrieve_or_stop(ssh, host, state)
        else:
            destroy()
        after = api('/users/current/')
        (OUT / 'account_credit_after.json').write_text(json.dumps({'credit': after['credit'], 'before': account['credit'],
            'elapsed_hours': (time.time() - created_at) / 3600, 'credit_difference_not_reconciled_invoice': account['credit'] - after['credit']}, indent=2))
    print("RETRIEVAL COMPLETE; rental destroyed. Chat adapters in " + str(ADAPTER_DIR), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["run", "destroy"])
    parser.add_argument('--hours', type=float, default=5)
    args = parser.parse_args()
    run(args.hours) if args.action == 'run' else destroy()
