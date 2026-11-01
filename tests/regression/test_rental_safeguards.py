"""Independent rental deadline and watchdog failure paths. -- PI/OpenAI (Sol)"""
import importlib.util
import json
import os
import runpy
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


guard = load('deadline_guard', 'scripts/eval/48_vast_deadline.py')


class RentalSafeguardsTest(unittest.TestCase):
    def test_exact_deadline_never_deletes_wrong_label_or_false_success(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / 'receipt.json'
            with patch.object(guard, 'api', return_value={'instances': [{'id': 123, 'label': 'wrong'}]}) as api:
                with self.assertRaises(AssertionError): guard.destroy_exact(123, 'expected', out)
                api.assert_called_once_with('/instances/')
            with patch.object(guard, 'api', side_effect=[{'instances': [{'id': 123, 'label': 'expected'}]}, {'success': False}]):
                with self.assertRaises(AssertionError): guard.destroy_exact(123, 'expected', out)
            self.assertFalse(out.exists())
            with patch.object(guard, 'api', side_effect=[{'instances': [{'id': 123, 'label': 'expected'}]}, {'success': True}, {'instances': []}]) as api:
                guard.destroy_exact(123, 'expected', out)
                self.assertEqual(api.call_args_list[1].args, ('/instances/123/', 'DELETE'))
            self.assertTrue(json.loads(out.read_text())['absent_confirmed'])

    def test_persistent_timer_receipt_binds_id_deadline_and_frozen_helper(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d); state = out / 'state.json'; deadline = time.time()+3600
            state.write_text(json.dumps({'instance_id': 123, 'hard_destroy_epoch': deadline}))
            at = guard.datetime.fromtimestamp(deadline, guard.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
            props = 'ActiveState=active\nUnitFileState=enabled\nTimersCalendar='+at+'\n'
            with patch.object(guard.subprocess, 'run') as run, patch.object(guard.subprocess, 'check_output', return_value=props):
                guard.arm(state, out, 'cg-fixture')
            frozen = out / 'deadline_guard/guard.py'
            compile(frozen.read_text(), str(frozen), 'exec')
            self.assertEqual(runpy.run_path(str(frozen))['ROOT'], guard.ROOT)
            receipt = json.loads((out / 'deadline_guard_armed.json').read_text())
            self.assertEqual(receipt['instance_id'], 123); self.assertEqual(receipt['deadline_epoch'], deadline)
            service = (out / 'deadline_guard/cg-vast-123-deadline.service').read_text()
            self.assertIn('--instance-id 123 --label cg-fixture', service)
            self.assertIn('Persistent=true', (out / 'deadline_guard/cg-vast-123-deadline.timer').read_text())
            self.assertTrue(any('enable' in c.args[0] for c in run.call_args_list))

    def test_watchdog_retries_rejected_stop_and_confirms_state(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d); counter = out / 'calls'
            curl = out / 'curl'; curl.write_text(f'''#!{sys.executable}
import json,sys
from pathlib import Path
p=Path({str(counter)!r}); n=int(p.read_text()) if p.exists() else 0
if 'PUT' in sys.argv:
 n+=1; p.write_text(str(n)); print(json.dumps({{'success':n>1}}))
else: print(json.dumps({{'instances':{{'id':123,'actual_status':'stopped' if n>1 else 'running'}}}}))
'''); curl.chmod(0o755)
            sleep = out / 'sleep'; sleep.write_text('#!/bin/sh\nexit 0\n'); sleep.chmod(0o755)
            source = (ROOT / 'scripts/train/box_watchdog.sh').read_text()
            source = source.replace('ID=$(env_of_pid1 CONTAINER_ID); KEY=$(env_of_pid1 CONTAINER_API_KEY)', 'ID=123; KEY=fixture')
            source = source.replace('HB=/workspace/heartbeat;', f'HB={out}/heartbeat;')
            result = subprocess.run(['bash', '-c', source], env=dict(os.environ, PATH=str(out)+':'+os.environ['PATH'], MAX_SILENT_H='-1'), capture_output=True, text=True, timeout=10)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(counter.read_text(), '2')
            self.assertIn('stop unconfirmed', result.stderr)
            self.assertIn('stopped state confirmed', result.stdout)


if __name__ == '__main__': unittest.main()


def test_start_driver_creates_run_dir_before_redirecting_job_log():
    """Chat-only runs upload no adapters, so start_driver itself must create run/ (Li dev run, 2026-11-01). -- PI/Claude"""
    sys.path.insert(0, str(ROOT / "scripts/box"))
    rent = load('rent', 'scripts/box/rent.py')
    lease = rent.Lease.__new__(rent.Lease)
    lease.name, lease.cfg_path, lease.state = "x", ROOT / "configs/runs/character_template.yaml", {"runner_deadline_epoch": 1}
    sent = []
    lease.remote = lambda cmd, **kw: sent.append(cmd)
    lease.start_driver()
    assert sent[0].startswith(f"mkdir -p {rent.REMOTE}/outputs/x/run && ")


def test_every_smoked_file_is_shipped_to_the_box():
    """box.py hashes SMOKED at start, so each must be inside rent.CODE_DIRS (Li dev run attempt 2, 2026-11-01). -- PI/Claude"""
    sys.path.insert(0, str(ROOT / "scripts/box"))
    rent, box = load('rent', 'scripts/box/rent.py'), load('box', 'scripts/box/box.py')
    assert [f for f in box.SMOKED if not any(f.startswith(d + "/") for d in rent.CODE_DIRS)] == []
