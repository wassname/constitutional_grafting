"""vast.ai lease for one run config: rent, set up, upload adapters, run scripts/box/box.py, follow it, retrieve, destroy.

Safety kept from runs 10-16: cost cap checked against the live offer; independent systemd deadline (48_vast_deadline.py) plus
an on-box watchdog that stops the instance when the heartbeat goes silent; uploads and retrievals checked by sha256; on a driver
failure the box is held up to 60 min (heartbeat on) for a fix: `rent.py CONFIG push` copies changed code, then
`touch .local/<name>/resume` restarts the driver, which skips stages whose receipts and adapter hashes match.

usage: python scripts/box/rent.py configs/runs/run17.yaml run | attach | push | snapshot | destroy   -- PI/Claude (opus-5-5), 2026-10-28
"""
import argparse
import concurrent.futures
import fcntl
import hashlib
import io
import json
import shlex
import shutil
import subprocess
import sys
import tarfile
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

from confighash import driver_config_sha
from tinychar import TC, JUDGE_V2

ROOT = Path(__file__).resolve().parents[2]
CODE_DIRS = ["scripts/box", "scripts/train", "scripts/eval", "configs"]  # copied whole; small text files
REMOTE = "/workspace/cg"


def sha(path):
    with Path(path).open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def adapter_receipt(path: Path) -> dict:
    return {f: sha(path / f) for f in ("adapter_config.json", "adapter_model.safetensors")}


def api(path, method="GET", body=None):
    entries = dict(l.split("=", 1) for l in (ROOT / ".env").read_text().splitlines() if "=" in l and not l.startswith("#"))
    key = entries["VASTAI_API_KEY"].strip().strip('"').strip("'")
    req = urllib.request.Request("https://console.vast.ai/api/v0" + path, data=json.dumps(body).encode() if body is not None else None,
                                 method=method, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(req, timeout=30) as f:
                return json.load(f)
        except urllib.error.HTTPError as e:
            if method != "GET" or e.code not in {429, 500, 502, 503, 504} or attempt == 5:
                raise
            time.sleep(min(120, 30 * 2 ** attempt))
        except urllib.error.URLError:  # connection reset before any response (lease 4's stop call): state-setting PUTs are idempotent
            if attempt == 5:
                raise
            time.sleep(min(120, 30 * 2 ** attempt))


class Lease:
    def __init__(self, cfg_path: Path):
        self.cfg_path = cfg_path
        self.cfg = yaml.safe_load(cfg_path.read_text())
        self.name = self.cfg["name"]
        self.label = f"cg-{self.name}"
        self.out = ROOT / "slop/eval" / self.name / "lease"
        self.local = ROOT / ".local" / self.name
        self.state_path = self.local / "rental.json"
        # The usual path, but stored on the /workspace volume: run 19's retrieval failed with the root disk full (1.8 TB, 0 free).
        self.adapter_dir = Path.home() / f".local/share/cg_{self.name}_adapters"
        if not self.adapter_dir.exists():
            (store := ROOT / ".local/adapters" / self.adapter_dir.name).mkdir(parents=True, exist_ok=True)
            self.adapter_dir.symlink_to(store)
        self.out.mkdir(parents=True, exist_ok=True)
        self.local.mkdir(parents=True, exist_ok=True)
        self.state = json.loads(self.state_path.read_text()) if self.state_path.exists() else None
        self.stop = threading.Event()

    # --- connection
    @property
    def ssh(self):
        s = self.state
        return ["ssh", "-i", str(Path.home() / ".ssh/id_vast"), "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", "-o", "ServerAliveInterval=30",
                "-o", "StrictHostKeyChecking=accept-new", "-o", f"UserKnownHostsFile={self.local / 'known_hosts'}", "-p", str(s["ssh_port"]), f"root@{s['ssh_host']}"]

    def remote(self, command, timeout=600, **kw):
        left = self.state["hard_destroy_epoch"] - time.time() - 120
        assert left > 0, "past the hard destroy deadline"
        return subprocess.run(self.ssh + [command], check=True, timeout=min(timeout, left), **kw)

    def rsync(self, *args, timeout=3600, compress=True, tries=6):
        """--partial resumes, so a dropped ssh connection (exit 255; run 19's Texas box dropped single and parallel streams alike) is
        retried after a pause."""
        for attempt in range(tries):
            try:
                return subprocess.run(["rsync", "-az" if compress else "-a", "--partial", "-e", shlex.join(self.ssh[:-1]), *args], check=True,
                                      timeout=min(timeout, max(1, self.state["hard_destroy_epoch"] - time.time() - 120)))
            except subprocess.CalledProcessError as e:
                if e.returncode != 255 or attempt == tries - 1:
                    raise
                print(f"RSYNC RETRY {attempt + 1}/{tries - 1} after ssh drop: {args[-2]}", flush=True)
                time.sleep(20)

    def host(self, path=""):
        return f"{self.ssh[-1]}:{path}"

    def save(self):
        self.state_path.write_text(json.dumps(self.state, indent=2))
        (self.out / "lease.json").write_text(json.dumps(self.state, indent=2))

    # --- code and adapters
    def code_tar(self) -> bytes:
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as t:
            for d in CODE_DIRS:
                t.add(ROOT / d, arcname=d, filter=lambda i: None if "__pycache__" in i.name else i)
            t.add(ROOT / self.cfg["inputs"], arcname=self.cfg["inputs"])
            for path in JUDGE_V2["change"], JUDGE_V2["refs"]:
                t.add(path, arcname=str(path.relative_to(ROOT)))
            for name in ("src", "scripts", "data", "pyproject.toml", "uv.lock", ".local/raw/gsm8k_test.parquet"):
                t.add(TC / name, arcname=str(TC.relative_to(ROOT) / name), filter=lambda i: None if "__pycache__" in i.name else i)
            for spec in (self.cfg.get("train") or {}).get("chats", {}).values():
                t.add(ROOT / spec["data"], arcname=spec["data"])
            if sel := self.cfg.get("selector"):
                for key in ("cap_data", "char_data"):
                    if sel.get(key):
                        t.add(ROOT / sel[key], arcname=sel[key])
        return buf.getvalue()

    def push(self):
        """Every step here is idempotent, so a dropped ssh connection (exit 255; run 22's second box reset ssh during setup) is retried."""
        def remote(*a, **kw):
            for attempt in range(4):
                try:
                    return self.remote(*a, **kw)
                except subprocess.CalledProcessError as e:
                    if e.returncode != 255 or attempt == 3:
                        raise
                    print(f"PUSH RETRY {attempt + 1}/3 after ssh drop", flush=True)
                    time.sleep(20)
        remote(f"mkdir -p {REMOTE} && tar -xzf - -C {REMOTE}", input=self.code_tar(), timeout=120)
        key_line = next(l for l in (ROOT / ".env").read_text().splitlines() if l.startswith("OPENROUTER_API_KEY="))
        remote(f"umask 077; cat > {REMOTE}/.env; chmod 600 {REMOTE}/.env", input=(key_line + "\n").encode(), timeout=30)
        remote(f"cd {REMOTE}/.local/tiny-character-9e33eed && "
                    "(command -v git || (apt-get update -qq && apt-get install -y -qq git)) && "
                    "UV_PROJECT_ENVIRONMENT=.venv uv sync --locked > /workspace/judge_setup.log 2>&1 && "
                    "test -x .venv/bin/python && PYTHONPATH=src .venv/bin/python -c "
                    "'import inspect_ai, llm_judge, tiny_character' >> /workspace/judge_setup.log 2>&1", timeout=1200)
        (self.out / "pushed_code.json").write_text(json.dumps({"epoch": time.time(), "files": {str(p.relative_to(ROOT)): sha(p)
            for d in CODE_DIRS for p in (ROOT / d).rglob("*") if p.is_file() and "__pycache__" not in str(p)}}, indent=1))

    def hub_folders(self) -> set[str]:
        from huggingface_hub import HfApi
        return {f.split("/")[0] for f in HfApi().list_repo_files(self.cfg["adapter_hub"])}

    def upload(self, name):
        src = Path(self.cfg["adapters"][name])
        files = adapter_receipt(src)
        target = f"{REMOTE}/outputs/{self.name}/up_{name}"
        self.remote(f"mkdir -p {target}", timeout=30)
        hub = self.cfg.get("adapter_hub")
        if hub and src.name not in self.hub_folders():  # adapters not published there (e.g. ones made on an earlier lease) go by rsync
            hub = None
        if hub:  # public HF repo with one folder per adapter, named like the local dir: the box downloads fast
            fetch = ("from huggingface_hub import hf_hub_download as d; import shutil; "
                     f"[shutil.copy(d({hub!r}, {src.name!r} + '/' + f, local_dir='/workspace/hub'), {target!r} + '/' + f) "
                     "for f in ('adapter_config.json', 'adapter_model.safetensors')]")
            self.remote("HF_HOME=/workspace/hf python -c " + shlex.quote(fetch), timeout=3600)
        # Uploads run ~1-5 MB/s from this container; lease 3 saw every stream reset together twice in 3.5 h, so retry (rsync --partial
        # resumes) up to 12 times rather than lose a set-up box. A failure here destroys the lease.
        for attempt in range(0 if hub else 12):
            try:
                self.rsync(str(src / "adapter_config.json"), str(src / "adapter_model.safetensors"), self.host(target + "/"), timeout=4 * 3600)
                break
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print(f"UPLOAD RETRY {name} {attempt + 1}/12: {e!r}"[:300], flush=True)
                assert attempt < 11, f"upload failed 12 times: {name}"
                time.sleep(60)
        check = "import hashlib,json;print(json.dumps({f:hashlib.file_digest(open(" + repr(target) + "+'/'+f,'rb'),'sha256').hexdigest() for f in ['adapter_config.json','adapter_model.safetensors']}))"
        got = json.loads(self.remote("python -c " + shlex.quote(check), timeout=300, capture_output=True, text=True).stdout)
        assert got == files, f"upload sha mismatch: {name}"
        receipt = json.dumps({"name": name, "source": str(src), "files": files, "epoch": time.time()}, indent=2)
        self.remote(f"mkdir -p {REMOTE}/outputs/{self.name}/run && cat > {REMOTE}/outputs/{self.name}/run/upload_{name}.verified.json", input=receipt.encode(), timeout=30)
        print("UPLOADED " + name, flush=True)

    # --- driver
    def start_driver(self):
        cmd = (f"cd {REMOTE} && HF_HOME=/workspace/hf VLLM=/opt/vllm/bin/vllm BOX_DEADLINE={self.state['runner_deadline_epoch']} "
               f"python scripts/box/box.py {self.cfg_path.relative_to(ROOT)}")
        script = f"set +e; {cmd} > outputs/{self.name}/run/job.log 2>&1; echo $? > outputs/{self.name}/run/job.exit"
        self.remote(f"rm -f {REMOTE}/outputs/{self.name}/run/job.exit; tmux new-session -d -s box " + shlex.quote("bash -lc " + shlex.quote(script)), timeout=30)

    def status(self) -> dict:
        code = (f"import json,subprocess;from pathlib import Path;p=Path('{REMOTE}/outputs/{self.name}/run');"
                "print(json.dumps({'exit':(p/'job.exit').read_text().strip() if (p/'job.exit').exists() else None,"
                "'running':subprocess.run(['tmux','has-session','-t','box'],capture_output=True).returncode==0,"
                "'stages':(p/'stages.log').read_text().splitlines()[-1][:300] if (p/'stages.log').exists() else '',"
                "'done':sorted(f.name for f in p.glob('*.done'))}))")
        return json.loads(self.remote("python -c " + shlex.quote(code), timeout=30, capture_output=True, text=True).stdout)

    def heartbeat(self):
        while not self.stop.wait(60):
            try:
                self.remote("touch /workspace/heartbeat", timeout=20, stdout=subprocess.DEVNULL)
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e:
                print("HEARTBEAT TRANSPORT " + repr(e), flush=True)

    def follow(self):
        """Follow the driver; on failure hold up to 60 min for `push` + a resume trigger, then restart (resume by receipts)."""
        last, failures, holds = None, 0, 0
        trigger = self.local / "resume"
        while True:
            assert time.time() < self.state["runner_deadline_epoch"], "runner deadline reached"
            try:
                s = self.status()
                failures = 0
            except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
                failures += 1
                assert failures < 10, "SSH unavailable for 10 status checks"
                self.stop.wait(45)
                continue
            if (s["stages"], s["done"]) != last:
                print(f"STAGE {s['stages']} | done {s['done']}", flush=True)
                last = (s["stages"], s["done"])
            if s["exit"] == "0":
                return
            if s["exit"] is not None or not s["running"]:
                holds += 1
                hold_until = min(time.time() + 3600, self.state["runner_deadline_epoch"])
                failure = {"exit": s["exit"], "stages": s["stages"], "hold_until": hold_until, "hold": holds,
                           "action": f"inspect outputs/{self.name}/run/job.log; fix; rent.py CONFIG push; touch {trigger}"}
                (self.out / f"driver_failure_{holds}.json").write_text(json.dumps(failure, indent=2))
                self.rsync(self.host(f"{REMOTE}/outputs/{self.name}/run/"), str(self.out / "box_runs") + "/", timeout=600)
                print("DRIVER FAILURE, HOLDING 60 MIN " + json.dumps(failure), flush=True)
                while time.time() < hold_until and not trigger.exists():
                    self.stop.wait(10)
                if not trigger.exists():
                    raise TimeoutError("repair hold expired")
                trigger.unlink()
                self.start_driver()
            self.stop.wait(45)

    def retrieve(self):
        """Run evidence, then every trained adapter (final and any checkpoints) as bf16 copies made on the box, checked against
        remote hashes. bf16 halves the download (max relative error ~0.002, as the HF copies); several files at once and no rsync
        compression, because one ssh stream to a distant box tops out near 9 MB/s (run 19: Texas to Perth, 240 ms)."""
        self.rsync("--exclude=merged_model", self.host(f"{REMOTE}/outputs/{self.name}/run/"), str(self.out / "box_runs") + "/", timeout=1800)
        cast = (f"import hashlib,json,torch;from pathlib import Path;from safetensors.torch import load_file,save_file;"
                f"p=Path('{REMOTE}/outputs/{self.name}');q=Path('{REMOTE}/outputs/{self.name}_bf16');m={{}}\n"
                "for f in p.rglob('adapter_*'):\n"
                " if not f.is_file() or f.parent.name.startswith('up_'): continue\n"
                " o=q/f.relative_to(p);o.parent.mkdir(parents=True,exist_ok=True)\n"
                " if f.suffix=='.safetensors': save_file({k:(v.to(torch.bfloat16) if v.dtype==torch.float32 else v) for k,v in load_file(f).items()},o)\n"
                " else: o.write_bytes(f.read_bytes())\n"
                " m[str(f.relative_to(p))]=hashlib.file_digest(o.open('rb'),'sha256').hexdigest()\n"
                "for f in p.rglob('trainer_state.json'):\n"
                " o=q/f.relative_to(p);o.parent.mkdir(parents=True,exist_ok=True);o.write_bytes(f.read_bytes())\n"
                "print(json.dumps(m))")
        manifest = json.loads(self.remote(f"cd {REMOTE} && /workspace/axolotl-venv/bin/python -c " + shlex.quote(cast), timeout=1800,
                                          capture_output=True, text=True).stdout.splitlines()[-1])
        if not manifest:  # nothing trained on this lease (e.g. run 19o: uploaded adapters only)
            print("RETRIEVED 0 adapter files (none trained)", flush=True)
            return
        size = int(self.remote(f"du -sb {REMOTE}/outputs/{self.name}_bf16 | cut -f1", timeout=600, capture_output=True, text=True).stdout.split()[-1])
        free = shutil.disk_usage(self.adapter_dir.resolve()).free
        assert free > 1.2 * size, f"local disk: {free / 1e9:.0f} GB free at {self.adapter_dir.resolve()}, retrieval needs ~{size / 1e9:.0f} GB"
        dirs = sorted({Path(rel).parts[0] for rel in manifest})
        with concurrent.futures.ThreadPoolExecutor(8) as ex:  # one rsync per adapter folder
            for job in [ex.submit(self.rsync, "-R", self.host(f"{REMOTE}/outputs/{self.name}_bf16/./{d}"), str(self.adapter_dir) + "/",
                                  compress=False) for d in dirs]:
                job.result()
        for rel, digest in manifest.items():
            assert sha(self.adapter_dir / rel) == digest, f"retrieval sha mismatch: {rel}"
        (self.out / "retrieval_verified.json").write_text(json.dumps({"epoch": time.time(), "dtype": "bf16", "files": manifest}, indent=2))
        print(f"RETRIEVED {len(manifest)} adapter files (bf16) to {self.adapter_dir}", flush=True)

    def destroy(self):
        live = [r for r in api("/instances/")["instances"] if self.state and r["id"] == self.state["instance_id"]]
        if not self.state:
            live = [r for r in api("/instances/")["instances"] if r["label"] == self.label]
        assert len(live) <= 1 and all(r["label"] == self.label for r in live), "label mismatch: inspect before teardown"
        for r in live:
            assert api(f"/instances/{r['id']}/", "DELETE", {})["success"]
            assert all(x["id"] != r["id"] for x in api("/instances/")["instances"])
            subprocess.run(["sudo", "-n", "systemctl", "disable", "--now", f"cg-vast-{r['id']}-deadline.timer"], check=False)
            print(f"DESTROYED {r['id']}", flush=True)

    # --- lease
    def run(self):
        cfg = self.cfg
        assert self.state is None, f"existing lease state {self.state_path}: attach or destroy first"
        for p in cfg["adapters"].values():
            adapter_receipt(Path(p))  # fail before renting if an adapter is missing
        for spec in (cfg.get("train") or {}).get("chats", {}).values():
            subprocess.run([sys.executable, ROOT / "scripts/train/check_loss_mask.py", ROOT / spec["data"]], check=True)
        smoke = json.loads((self.local / "smoke_passed.json").read_text())  # written by `box.py CONFIG --smoke` (AGENTS.md: smoke before renting)
        assert smoke["driver_config_sha256"] == driver_config_sha(self.cfg_path) and all(sha(ROOT / f) == d for f, d in smoke["code_sha256"].items()), \
            "config or driver code changed since the local smoke: rerun it"
        offers = api("/bundles/?q=" + urllib.parse.quote(json.dumps(cfg["offer_query"])))["offers"]
        ok = [o for o in offers if o["gpu_name"] == cfg["gpu_name"] and o["cuda_max_good"] >= 13.0 and o["dph_total"] <= cfg["max_hourly_rate"]
              and o["inet_down_cost"] <= .005 and o["inet_up_cost"] <= .005]
        assert ok, "no offer fits; no lease created"
        offer = min(ok, key=lambda o: o["dph_total"])
        reserve = cfg.get("reserve_usd", {"traffic": 3, "judge": 6})  # per run: run 18 sets its own from its cell count
        total = cfg["max_hours"] * offer["dph_total"] + reserve["traffic"] + reserve["judge"]
        assert total <= cfg["budget_usd"], f"offer reserve ${total:.2f} exceeds budget ${cfg['budget_usd']}"
        acct = api("/users/current/")  # credit plus one auto top-up must cover the whole lease (as run 16's controller checked)
        autobill = acct["autobill_amount"] if acct["has_billing"] and not acct["billing_failed"] and acct["autobill_threshold"] > 0 else 0
        assert acct["credit"] + autobill >= cfg["max_hours"] * offer["dph_total"] + 4, f"vast funding {acct['credit'] + autobill:.2f} below the lease cost"
        (self.out / "rental_quote.json").write_text(json.dumps({"offer": offer, "reserve_usd": total, "credit": acct["credit"], "autobill": autobill}, indent=2))
        started = time.time()
        created = api(f"/asks/{offer['id']}/", "PUT", {"client_id": "me", "image": cfg["image"], "disk": 500, "label": self.label,
                                                      "runtype": "ssh_direct", "cancel_unavail": True})
        assert created["success"], created
        self.state = {"instance_id": created["new_contract"], "created_epoch": started, "hourly_rate": offer["dph_total"],
                      "hard_destroy_epoch": started + cfg["max_hours"] * 3600, "runner_deadline_epoch": started + (cfg["max_hours"] - 1) * 3600}
        self.save()
        pool = concurrent.futures.ThreadPoolExecutor(8)
        try:
            subprocess.run([sys.executable, ROOT / "scripts/eval/48_vast_deadline.py", "arm", "--state", self.state_path, "--out", self.out,
                            "--label", self.label], check=True)
            while time.time() < started + 2700:  # run 17's first lease: 30 min was not enough and nothing was logged
                inst = next(r for r in api("/instances/")["instances"] if r["id"] == self.state["instance_id"])
                ports = inst.get("ports") or {}
                ssh_rc = None
                if inst["actual_status"] == "running":
                    if ports.get("22/tcp"):
                        self.state.update(ssh_host=inst["public_ipaddr"], ssh_port=ports["22/tcp"][0]["HostPort"])
                    elif inst.get("ssh_host") and inst.get("ssh_port"):  # vast's SSH proxy, as run 16's controller fell back to
                        self.state.update(ssh_host=inst["ssh_host"], ssh_port=inst["ssh_port"])
                    if "ssh_host" in self.state:
                        self.save()
                        try:
                            probe = subprocess.run(self.ssh + ["true"], timeout=20, capture_output=True, text=True)
                            ssh_rc = (probe.returncode, probe.stderr.strip()[-160:])
                            if probe.returncode == 0:
                                break
                        except subprocess.TimeoutExpired:
                            ssh_rc = "timeout"
                print(f"WAIT SSH {int(time.time() - started)}s status={inst['actual_status']} intended={inst.get('intended_status')} "
                      f"msg={str(inst.get('status_msg'))[:120]!r} port22={bool(ports.get('22/tcp'))} proxy={inst.get('ssh_host')}:{inst.get('ssh_port')} ssh={ssh_rc}", flush=True)
                time.sleep(30)
            else:
                raise TimeoutError("SSH not ready in 45 min")
            self.remote("nvidia-smi && python -c 'import torch; assert torch.cuda.get_device_properties(0).total_memory > 90*1024**3' "
                        "&& (command -v tmux && command -v rsync || (apt-get update -qq && apt-get install -y -qq tmux rsync))", timeout=300)
            self.push()
            self.remote(f"touch /workspace/heartbeat; tmux new-session -d -s watchdog 'cd {REMOTE} && MAX_SILENT_H=1 bash scripts/train/box_watchdog.sh > /workspace/watchdog.log 2>&1'")
            self.remote("sleep 5; grep -q 'auth check GET: 200' /workspace/watchdog.log", timeout=30)
            beat = pool.submit(self.heartbeat)
            setup = (f"cd {REMOTE} && export UV_EXCLUDE_NEWER='8 days' && uv venv /opt/vllm --python 3.12 && uv pip install --python /opt/vllm/bin/python vllm==0.31.0 "
                     "&& uv pip install --python \"$(command -v python)\" jaxtyping==0.3.11 beartype==0.23.1")
            needed = ("base", "instruct") if (cfg.get("train") or {}).get("chats") else ("instruct",)  # Base only when chats train on it
            fetch = ("from huggingface_hub import snapshot_download as s; [s(r, revision=v, ignore_patterns=['*.gguf','*.bin','*.onnx'], max_workers=8) "
                     f"for r, v in {[(cfg[k]['repo'], cfg[k]['revision']) for k in needed]!r}]")
            jobs = [pool.submit(lambda: self.remote(setup + " > /workspace/setup.log 2>&1", timeout=5400)),
                    pool.submit(lambda: self.remote("HF_HOME=/workspace/hf python -c " + shlex.quote(fetch) + " > /workspace/download.log 2>&1", timeout=5400))]
            jobs += [pool.submit(self.upload, n) for n in cfg["adapters"]]
            for j in jobs:
                j.result()
            self.start_driver()
            self.follow()
            if beat.done():
                beat.result()
        finally:
            try:
                if self.state.get("ssh_host"):
                    try:
                        self.retrieve()
                    except BaseException as e:
                        (self.out / "retrieval_failure.json").write_text(json.dumps({"error": repr(e)}))
                        assert api(f"/instances/{self.state['instance_id']}/", "PUT", {"state": "stopped"})["success"]
                        print("RETRIEVAL FAILED: instance stopped, disk kept until the hard deadline", flush=True)
                        raise
                self.destroy()
                (self.out / "closure.json").write_text(json.dumps({"elapsed_hours": (time.time() - started) / 3600,
                    "estimated_gpu_usd": (time.time() - started) / 3600 * self.state["hourly_rate"]}, indent=2))
            finally:
                self.stop.set()
                pool.shutdown(wait=True)

    def attach(self):
        pool = concurrent.futures.ThreadPoolExecutor(1)
        beat = pool.submit(self.heartbeat)
        try:
            self.follow()
            self.retrieve()
            self.destroy()
        finally:
            self.stop.set()
            pool.shutdown(wait=True)
            if beat.done():
                beat.result()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", type=Path)
    ap.add_argument("action", choices=["run", "attach", "push", "snapshot", "destroy"])
    a = ap.parse_args()
    lease = Lease(a.config.resolve())
    with (lease.local / "controller.lock").open("a") as lock:
        if a.action in ("run", "attach"):
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        {"run": lease.run, "attach": lease.attach, "push": lease.push, "snapshot": lease.retrieve, "destroy": lease.destroy}[a.action]()


if __name__ == "__main__":
    main()
