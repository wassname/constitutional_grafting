"""Budget and unchanged ABX sample/order construction, with no API calls. -- PI/OpenAI (Sol)"""
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('bounded_abx',ROOT/'scripts/eval/78_run16_document_abx_bounded.py')
abx=importlib.util.module_from_spec(spec);spec.loader.exec_module(abx)


def test_budget_reserves_inflight_work_and_does_not_repay_reservations():
    budget=abx.Budget(7)
    budget.reserve(.6)
    with pytest.raises(AssertionError):budget.reserve(.5)
    budget.finish(.6,.2)
    assert budget.spent==7.2 and budget.reserved==0
    budget.reserve(.7)
    budget.finish(.7,.4)
    assert budget.spent<abx.CAP


def test_null_and_changed_trials_keep_other_sample_and_seeded_order():
    ref={('item',0):'base0',('item',1):'base1'};changed={('item',0):'new0',('item',1):'new1'}
    trials=abx.trials_for(ref,{'null_identical':ref,'changed':changed},lambda r:r)
    assert len(trials)==4
    for t in trials:
        assert t['x']==ref[('item',t['j'])]
        assert t[t['instruct_is'].lower()]==ref[('item',1-t['j'])]
        assert t['identical']==(t['model']=='null_identical')
    assert trials==abx.trials_for(ref,{'null_identical':ref,'changed':changed},lambda r:r)
