"""Launch-critical owner, retrieval, deadline and watchdog failure paths. -- PI/OpenAI (Sol)"""
import importlib.util
import json
import os
import runpy
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / file)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


rental = load('guarded_rental', 'scripts/eval/38_run10_chat_rental.py')
guard = load('deadline_guard', 'scripts/eval/48_vast_deadline.py')


class RentalSafeguardsTest(unittest.TestCase):
    def test_owner_lock_covers_instance_not_only_copying(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / '.local').mkdir(); state = root / '.local/state.json'
            state.write_text(json.dumps({'instance_id': 123}))
            with patch.object(rental, 'ROOT', root), patch.object(rental, 'STATE', state), rental.controller_owner():
                for p in [state.with_suffix('.owner.lock'), root / '.local/vast_instance_123.owner.lock']:
                    with p.open('a') as f:
                        with self.assertRaises(BlockingIOError):
                            rental.fcntl.flock(f, rental.fcntl.LOCK_EX | rental.fcntl.LOCK_NB)

    def test_attach_keeps_heartbeat_until_retrieval_finishes(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d); state = out / 'state.json'; state.write_text(json.dumps({'instance_id': 123, 'created_epoch': time.time()-3600, 'runner_deadline_epoch': time.time()-1, 'hard_destroy_epoch': time.time()+3600}))
            event = threading.Event()
            def copy(*args):
                self.assertFalse(event.is_set(), 'heartbeat ended before retrieval')
            with patch.object(rental, 'STATE', state), patch.object(rental, 'OUT', out), patch.object(rental, 'saved_connection', return_value=(['ssh'], 'fixture')), patch.object(rental.threading, 'Event', return_value=event), patch.object(rental.concurrent.futures, 'ThreadPoolExecutor'), patch.object(rental, 'api', return_value={'credit': 1, 'instances': [{'id': 123}]}), patch.object(rental, 'monitor'), patch.object(rental.subprocess, 'run'), patch.object(rental, 'retrieve_or_stop', side_effect=copy):
                rental.attach()
            self.assertTrue(event.is_set())

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

    def test_fresh_bundle_on_approved_host_is_accepted_before_budget_gate(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); out = root / 'out'; out.mkdir()
            offer = {'id': 999, 'machine_id': 56389, 'gpu_name': 'RTX PRO 6000 S', 'inet_down_cost': .002, 'inet_up_cost': .004, 'cuda_max_good': 13, 'dph_total': 1.84}
            with patch.object(rental, 'STATE', root / 'state.json'), patch.object(rental, 'OUT', out), patch.object(rental, 'RUN_ROOT', root), patch.object(rental, 'BUDGET_USD', 0), patch.dict(os.environ, {'APPROVED_MACHINE_ID': '56389', 'OFFER_ID': 'stale', 'MAX_RATE_USD': '1.844445'}), patch.object(rental, 'api', side_effect=[{'credit': 100}, {'offers': [offer]}]) as api:
                with self.assertRaisesRegex(AssertionError, 'cumulative run-10 lease reserves'):
                    rental.run(1)
                self.assertEqual(len(api.call_args_list), 2)
                self.assertTrue(all(c.args[0].startswith(('/users/', '/bundles/')) for c in api.call_args_list))

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
