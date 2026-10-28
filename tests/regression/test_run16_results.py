"""Report interpolation stays bracketed and Markdown tables remain contiguous. -- PI/OpenAI (Sol)"""
import importlib.util
from pathlib import Path
import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('results79',ROOT/'scripts/eval/79_run16_results.py')
report=importlib.util.module_from_spec(spec);spec.loader.exec_module(report)


def test_matched_character_estimate_does_not_extrapolate():
    assert report.interpolate(.6,.8,53,54,.7)==pytest.approx(53.5)
    with pytest.raises(AssertionError):report.interpolate(.6,.8,53,54,.9)
    with pytest.raises(AssertionError):report.interpolate(.8,.6,53,54,.7)


def test_two_tables_render_without_blank_lines_inside_rows():
    text=report.markdown(['# Question','| A | B |','|:--|--:|','| x |1|','Bottom line','## Next','| C |','|:--|','| z |'])
    assert text.count('|:--')==2
    assert '| B |\n|:--' in text and '|1|\n\nBottom' in text
    assert '|\n\n|' not in text


def test_report_has_two_tables_and_all_panel_text_is_verbatim():
    import json
    out=ROOT/'slop/eval/run16_v2'
    assert sum(line.startswith('|:--') for line in (out/'results.md').read_text().splitlines())==2
    appendix=(out/'T0_demo_appendix.md').read_text()
    plan=json.loads((out/'plan.json').read_text())['cells']
    assert len(plan)==18
    for cell in plan:
        assert cell['model'] in appendix and cell['equation'] in appendix
        rows=[json.loads(l) for l in (out/'lease/box_runs'/f"panel_{cell['model']}.jsonl").open()]
        assert len(rows)==4
        for row in rows:
            assert row['gen']['temperature']==0
            for turn in row['turns']:
                assert turn['user'] in appendix and turn['assistant'] in appendix


def test_abx_raw_clean_reuse_and_budget_receipt_are_consistent():
    import json
    out=ROOT/'slop/eval/run16_v2'
    result=json.loads((out/'document_change/result.json').read_text())
    selection=json.loads((out/'document_change/selection.json').read_text())
    raw=[json.loads(l) for l in (out/'document_change/raw/abx/trials.jsonl').open()]
    clean=[json.loads(l) for l in (out/'document_change/coherent/abx/trials.jsonl').open()]
    assert len(raw)==1884 and len(clean)==876
    ids=set(selection['common_coherent_item_ids']);assert len(ids)==73
    assert clean==[r for r in raw if r['item_id'] in ids]
    assert result['served_models']==['deepseek/deepseek-v4.1-flash']
    assert result['completed'] and result['actual_or_conservative_charged_usd']<result['hard_cap_usd']==8
    cost=json.loads((out/'cost_receipt.json').read_text())
    total=cost['lease_gpu_estimate_usd']+cost['new_successful_cached_jev_usd']+cost['document_abx_api_usd']+sum(cost['other_unreconciled_reserves_usd'].values())
    assert total==pytest.approx(cost['conservative_total_with_reserves_usd']) and total<cost['hard_cap_usd']


def test_combined_diagnostic_counts_remain_separate_from_jev_score():
    import json
    out=ROOT/'slop/eval/run16_v2'
    core=json.loads((out/'chat_decision_audit.json').read_text())['records']
    anchored=json.loads((out/'anchored_decision_audit.json').read_text())
    records=core+anchored['records'];assert len(records)==26
    for key,count in anchored['combined_core_plus_anchored_counts_over26_per_item'].items():
        assert sum(r[key] for r in records)==count
    assert anchored['combined_core_plus_anchored_counts_over26_per_item']['fridge_knowingly_agrees_to_false_temperatures']==3
