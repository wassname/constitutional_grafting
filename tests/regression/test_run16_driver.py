"""Execute run16's real driver with fake external stages; catch orchestration failures before rental. -- PI/OpenAI (Sol)"""
import importlib.util
import subprocess
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('run16_dry',ROOT/'scripts/eval/72_run16_driver_dry_run.py')
dry=importlib.util.module_from_spec(spec);spec.loader.exec_module(dry)


@pytest.mark.parametrize('case',dry.CASES)
def test_real_driver_every_operational_branch(tmp_path,case):
    result=dry.run_case(tmp_path/case,case)
    assert result['passed'] and result['dry_run_only']


def test_dry_run_reproduces_original_env_callback_bug(tmp_path):
    source=(ROOT/'scripts/eval/62_run16_box.py').read_text()
    assert "'train_random_smoke.log', extra=env" in source
    broken=tmp_path/'original_bug.py'
    broken.write_text(source.replace("'train_random_smoke.log', extra=env","'train_random_smoke.log', env=env",1))
    with pytest.raises(TypeError,match="unexpected keyword argument 'env'"):
        dry.run_case(tmp_path/'broken','core',broken)


def test_stub_rejects_original_conflicting_smoke_warmups(tmp_path):
    source=(ROOT/'scripts/eval/62_run16_box.py').read_text()
    assert "    source.pop('warmup_ratio', None)\n" in source
    broken=tmp_path/'conflicting_warmups.py'
    broken.write_text(source.replace("    source.pop('warmup_ratio', None)\n",'',1))
    with pytest.raises(subprocess.CalledProcessError):
        dry.run_case(tmp_path/'conflict','core',broken)
    log=(tmp_path/'conflict/runs/run10/train_random_smoke.log').read_text()
    assert 'warmup_steps and warmup_ratio are mutually exclusive' in log
