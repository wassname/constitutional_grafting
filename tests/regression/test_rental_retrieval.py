"""Failed or corrupt artifact retrieval must not destroy the source disk. -- PI/Sol"""
import hashlib
import importlib.util
import json
import shlex
import subprocess
import tempfile
import time
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('rental', ROOT / 'scripts/eval/34_run9_rental.py')
rental = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rental)


class RentalRetrievalTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.out = Path(self.tmp.name) / 'run'
        self.adapters = Path(self.tmp.name) / 'weights'
        (self.out / 'box_runs').mkdir(parents=True)
        (self.out / 'box_runs/job.exit').write_text('0')
        self.tag = 'r9e_fixture_healed'
        (self.out / 'box_runs/exact_manifest.json').write_text(json.dumps({'required_cells': [self.tag]}))
        self.payloads = {'adapter_config.json': b'{}', 'adapter_model.safetensors': b'complete fixture bytes'}
        self.manifest = {self.tag: {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                                    for name, data in self.payloads.items()}}
        directory = self.adapters / self.tag
        directory.mkdir(parents=True)
        for name, data in self.payloads.items():
            (directory / name).write_bytes(data)
        self.state = {'instance_id': 123, 'hard_destroy_epoch': time.time() + 7200}
        for name, value in [('OUT', self.out), ('ADAPTER_DIR', self.adapters), ('STAGE', 'exact')]:
            replacement = patch.object(rental, name, value)
            replacement.start()
            self.addCleanup(replacement.stop)
        self.api = self.enterContext(patch.object(rental, 'api', return_value={'success': True}))
        self.destroy = self.enterContext(patch.object(rental, 'destroy'))

    def execute(self, command, **kwargs):
        if command[0] == 'rsync':
            self.assertIs(kwargs['check'], True)
        elif 'python -c' in command[-1]:
            remote_code = command[-1].split('python -c ', 1)[1]
            compile(shlex.split(remote_code)[0], '<remote-manifest>', 'exec')
            return subprocess.CompletedProcess(command, 0, stdout=json.dumps(self.manifest))
        return subprocess.CompletedProcess(command, 0)

    def test_matching_binary_and_configuration_allow_destruction(self):
        with patch.object(rental.subprocess, 'run', side_effect=self.execute):
            rental.retrieve_or_stop(['ssh'], 'host', self.state)
        self.destroy.assert_called_once_with()
        self.api.assert_not_called()
        self.assertTrue(json.loads((self.out / 'retrieval_verified.json').read_text())['all_final_adapter_hashes_match'])

    def test_transfer_error_stops_and_preserves_disk(self):
        def fail_transfer(command, **kwargs):
            if command[0] == 'rsync' and '--partial' in command:
                raise subprocess.CalledProcessError(12, command)
            return self.execute(command, **kwargs)
        with patch.object(rental.subprocess, 'run', side_effect=fail_transfer):
            with self.assertRaises(subprocess.CalledProcessError):
                rental.retrieve_or_stop(['ssh'], 'host', self.state)
        self.destroy.assert_not_called()
        self.api.assert_called_once_with('/instances/123/', 'PUT', {'state': 'stopped'})
        self.assertTrue((self.out / 'retrieval_failure.json').is_file())

    def test_corrupt_binary_or_configuration_stops_despite_zero_transfer_exit(self):
        for name in self.payloads:
            with self.subTest(name=name):
                self.api.reset_mock()
                (self.adapters / self.tag / name).write_bytes(b'X' * len(self.payloads[name]))
                with patch.object(rental.subprocess, 'run', side_effect=self.execute):
                    with self.assertRaisesRegex(AssertionError, 'incomplete or corrupt artifact'):
                        rental.retrieve_or_stop(['ssh'], 'host', self.state)
                self.destroy.assert_not_called()
                self.api.assert_called_once_with('/instances/123/', 'PUT', {'state': 'stopped'})
                (self.adapters / self.tag / name).write_bytes(self.payloads[name])

    def test_diagnostic_timeout_also_preserves_disk(self):
        with patch.object(rental.subprocess, 'run', side_effect=subprocess.TimeoutExpired('ssh', 30)):
            with self.assertRaises(subprocess.TimeoutExpired):
                rental.retrieve_or_stop(['ssh'], 'host', self.state)
        self.destroy.assert_not_called()
        self.api.assert_called_once_with('/instances/123/', 'PUT', {'state': 'stopped'})


if __name__ == '__main__':
    unittest.main()
