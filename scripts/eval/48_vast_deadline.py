"""Arm an independent systemd deadline against one exact Vast instance. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import json
import os
import shlex
import subprocess
import time
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def api(path: str, method: str = 'GET') -> dict:
    entries = dict(line.split('=', 1) for line in (ROOT / '.env').read_text().splitlines() if '=' in line and not line.startswith('#'))
    key = entries['VASTAI_API_KEY'].strip().strip('"').strip("'")
    request = urllib.request.Request('https://console.vast.ai/api/v0' + path, method=method,
                                    data=b'{}' if method == 'DELETE' else None,
                                    headers={'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json'})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def destroy_exact(instance_id: int, label: str, out: Path) -> None:
    instances = api('/instances/')['instances']
    live = [row for row in instances if row['id'] == instance_id]
    if live:
        assert len(live) == 1 and live[0]['label'] == label, 'exact instance/label mismatch'
        result = api(f'/instances/{instance_id}/', 'DELETE')
        assert result['success'] is True, result
        assert all(row['id'] != instance_id for row in api('/instances/')['instances']), 'destroy not confirmed'
    out.write_text(json.dumps({'author': 'PI/OpenAI (Sol)', 'instance_id': instance_id,
                              'label': label, 'absent_confirmed': True, 'confirmed_epoch': time.time()}, indent=2) + '\n')


def arm(state_path: Path, out: Path, label: str) -> None:
    state = json.loads(state_path.read_text())
    instance_id, deadline = state['instance_id'], state['hard_destroy_epoch']
    assert deadline > time.time() + 60
    unit = f'cg-vast-{instance_id}-deadline'
    at = datetime.fromtimestamp(deadline, timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    directory = out / 'deadline_guard'; directory.mkdir(exist_ok=True)
    frozen = directory / 'guard.py'; frozen.write_bytes(Path(__file__).read_bytes()); frozen.chmod(0o700)
    # PI/OpenAI: the frozen helper needs the project credential path, not its archive's parent path.
    source = frozen.read_text().replace('ROOT = Path(__file__).resolve().parents[2]', f'ROOT = Path({str(ROOT)!r})', 1)
    compile(source, str(frozen), 'exec')
    frozen.write_text(source)
    command = shlex.join(['/usr/bin/python3', str(frozen), 'destroy', '--instance-id', str(instance_id),
                          '--label', label, '--out', str(directory / 'destroy_verified.json')])
    service = f'[Unit]\nDescription=Exact-ID Vast hard deadline {instance_id}\n[Service]\nType=oneshot\nUser={os.environ["USER"]}\nWorkingDirectory={ROOT}\nExecStart={command}\nTimeoutStartSec=120\nRestart=on-failure\nRestartSec=15\n'
    timer = f'[Unit]\nDescription=Hard deadline for Vast {instance_id}\n[Timer]\nOnCalendar={at}\nPersistent=true\nAccuracySec=1s\nRandomizedDelaySec=0\nUnit={unit}.service\n[Install]\nWantedBy=timers.target\n'
    for suffix, text in [('service', service), ('timer', timer)]:
        local = directory / f'{unit}.{suffix}'; local.write_text(text)
        subprocess.run(['sudo', '-n', 'install', '-m', '644', str(local), f'/etc/systemd/system/{unit}.{suffix}'], check=True)
    subprocess.run(['sudo', '-n', 'systemctl', 'daemon-reload'], check=True)
    subprocess.run(['sudo', '-n', 'systemctl', 'enable', '--now', f'{unit}.timer'], check=True)
    props = subprocess.check_output(['systemctl', 'show', f'{unit}.timer', '--property=ActiveState,UnitFileState,NextElapseUSecRealtime,TimersCalendar'], text=True)
    assert 'ActiveState=active' in props and 'UnitFileState=enabled' in props, props
    assert at.removesuffix(' UTC') in props, props
    receipt = {'author': 'PI/OpenAI (Sol)', 'instance_id': instance_id, 'label': label, 'deadline_epoch': deadline,
               'deadline_utc': at, 'unit': unit, 'state_path': str(state_path), 'systemctl_show': props,
               'guard_sha256': hashlib.sha256(frozen.read_bytes()).hexdigest(),
               'policy': 'Destroy exact instance at absolute cap even if controller is stuck; retrieval must finish before this deadline. Independent systemd daemon, persistent timer files; API availability still required.'}
    (out / 'deadline_guard_armed.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('EXACT-ID DEADLINE GUARD ARMED ' + json.dumps(receipt), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['arm', 'destroy'])
    parser.add_argument('--state', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--label', required=True)
    parser.add_argument('--instance-id', type=int)
    args = parser.parse_args()
    if args.action == 'arm':
        arm(args.state.resolve(), args.out.resolve(), args.label)
    else:
        destroy_exact(args.instance_id, args.label, args.out.resolve())


if __name__ == '__main__':
    main()
