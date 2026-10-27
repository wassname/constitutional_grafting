"""Recovery collection publishes events independently of expensive judging and ignores unscored metrics. -- PI/OpenAI (Sol)"""
import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]


def load(name):
    spec=importlib.util.spec_from_file_location(name,ROOT/'scripts/eval'/name)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module


def test_local_event_publication_is_atomic_and_never_approves_gate(tmp_path):
    collect=load('67_run16_collect.py');box=tmp_path/'box';out=tmp_path/'out'
    box.mkdir();out.mkdir()
    for name in ['chat_evaluated','documents_evaluated','anchored_gate_ready','anch_trained','anch_config_diff','anchp_','optional_c_ready']:
        (box/(name+'.json')).write_text(json.dumps({'event':name}))
    (box/'anchored_gate.approved.json').write_text('{}')
    collect.publish_events(box,out)
    assert len(list(out.glob('*.json')))==7
    assert not (out/'anchored_gate.approved.json').exists() and not list(out.glob('*.tmp'))
    collect.publish_events(box,out)
    assert json.loads((out/'anchored_gate_ready.json').read_text())['event']=='anchored_gate_ready'


def test_cpu_prioritizes_document_gate_and_judge_excludes_documents(tmp_path,monkeypatch):
    process=load('75_run16_local_process.py');monkeypatch.setattr(process,'BOX',tmp_path)
    plan={'cells':[{'model':'r16_instruct','block':'chat'},{'model':'r16_chat','block':'chat'},
                   {'model':'r16_doc','block':'documents'},{'model':'r16_unfinished','block':'chat'}]}
    for name in ['r16_instruct','r16_chat','r16_doc']:(tmp_path/(name+'.done')).write_text('{}')
    assert [r['model'] for r in process.pending_cells(plan,'cpu')]==['r16_doc','r16_instruct','r16_chat']
    assert [r['model'] for r in process.pending_cells(plan,'judge')]==['r16_chat']


def test_metrics_publish_pending_cpu_without_fake_character_results(tmp_path,monkeypatch):
    import shutil
    metrics=load('68_run16_metrics.py');out=tmp_path/'out';box=out/'box'
    box.mkdir(parents=True);(out/'inputs').mkdir()
    shutil.copyfile(ROOT/'slop/eval/run16_v2/inputs/items.jsonl',out/'inputs/items.jsonl')
    (out/'plan.json').write_text(json.dumps({'cells':[{'model':'r16_pending','block':'chat'}]}))
    (box/'r16_pending.done').write_text('{}')
    monkeypatch.setattr(metrics,'OUT',out);monkeypatch.setattr(metrics,'BOX',box)
    metrics.main()
    result=json.loads((out/'metrics.json').read_text())
    assert result['metrics']=={} and result['pending']=={'r16_pending':'CPU scoring pending'}
    assert not (out/'metrics.tmp').exists()


def test_transient_ssh_pipe_recovers_without_retrying_nontransport_failures():
    import subprocess
    import time
    collect=load('67_run16_collect.py');calls=[];waits=[]
    def broken_then_ok(argv,**kwargs):
        calls.append(argv)
        if len(calls)==1:raise subprocess.CalledProcessError(255,argv)
    collect.sync_results(['rsync','dry-only'],time.time()+600,run=broken_then_ok,sleep=waits.append)
    assert len(calls)==2 and waits==[10]
    def permissions(argv,**kwargs):raise subprocess.CalledProcessError(23,argv)
    import pytest
    with pytest.raises(subprocess.CalledProcessError):collect.sync_results(['rsync','dry-only'],time.time()+600,run=permissions,sleep=waits.append)


def test_unjudged_chat_keeps_cpu_scores_and_explicit_null_character(tmp_path,monkeypatch):
    import shutil
    metrics=load('68_run16_metrics.py');out=tmp_path/'slop/eval/run16_v2';box=out/'box'
    box.mkdir(parents=True);(out/'inputs').mkdir()
    old=tmp_path/'slop/eval/run8';old.mkdir(parents=True)
    shutil.copyfile(ROOT/'slop/eval/run8/items.jsonl',old/'items.jsonl')
    shutil.copyfile(ROOT/'slop/eval/run16_v2/inputs/items.jsonl',out/'inputs/items.jsonl')
    items=[json.loads(line) for line in (out/'inputs/items.jsonl').read_text().splitlines()]
    legacy=[json.loads(line) for line in (old/'items.jsonl').read_text().splitlines()]
    model='r16_unjudged'
    (out/'plan.json').write_text(json.dumps({'cells':[{'model':model,'block':'chat'}]}))
    (box/(model+'.done')).write_text('{}')
    def save(path,records):
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(json.dumps(r)+'\n' for r in records))
    raw=[{'model':model,'item_id':it['id'],'sample':sample,'system':it['system'],
          'gen':{'temperature':.7,'top_p':1.,'seed':sample},
          'turns':[{'user':user,'assistant':'DRY-RUN ONLY'} for user in it['turns']]} for it in items for sample in (0,1)]
    save(box/f'replies_{model}.jsonl',raw)
    save(out/'ordinary'/model/'coherence.jsonl',[dict(item_id=r['item_id'],sample=r['sample'],turn_checks=[dict.fromkeys(metrics.FLAGS,0) for _ in r['turns']]) for r in raw])
    for folder,source in [('ordinary',items),('legacy_small_tasks',legacy)]:
        save(out/folder/model/'judged.jsonl',[{'item_id':it['id'],'sample':sample,'check':{'correct':True}} for it in source if it['family']=='capability' for sample in (0,1)])
    save(box/f'gsm8k_{model}.jsonl',[{'question':str(i),'gold':'0','correct':i%2==0,'finish':'stop'} for i in range(60)])
    monkeypatch.setattr(metrics,'ROOT',tmp_path);monkeypatch.setattr(metrics,'OUT',out);monkeypatch.setattr(metrics,'BOX',box)
    metrics.main();result=json.loads((out/'metrics.json').read_text())
    point=result['metrics'][model]
    assert point['maths']==30 and point['small_tasks_22']==22 and point['all_capability_38']==38
    assert point['character'] is None and result['pending'][model]=='Pinned v2 JEV judging pending'


def test_gate_package_keeps_complete_panel_and_flagged_context_without_approval(tmp_path,monkeypatch):
    package=load('65_run16_read_package.py');out=tmp_path/'out';box=out/'box';box.mkdir(parents=True)
    plan={'cells':[{'model':'r16_instruct','block':'chat','equation':'theta_I','description':'baseline'},
                   {'model':'r16_doc','block':'documents','equation':'theta_I + delta','description':'dry document'}]}
    (out/'plan.json').write_text(json.dumps(plan))
    def write_rows(path,rows):path.parent.mkdir(parents=True,exist_ok=True);path.write_text(''.join(json.dumps(r)+'\n' for r in rows))
    for model in ['r16_instruct','r16_doc']:
        (box/(model+'.done')).write_text('{}')
        record={'model':model,'item_id':'flagged','sample':0,'system':None,
                'turns':[{'user':'FULL USER','assistant':'FULL ASSISTANT '+('x'*5000)+' END','finish_reason':'length','n_tokens':1500}]}
        write_rows(box/f'panel_{model}.jsonl',[record]*4)
        write_rows(box/f'replies_{model}.jsonl',[record])
        write_rows(out/'ordinary'/model/'coherence.jsonl',[{'item_id':'flagged','sample':0,'turn_checks':[{'looped':0,'truncated':1,'lang_switch':0,'role_confusion':0,'empty':0}]}])
    monkeypatch.setattr(package,'OUT',out);monkeypatch.setattr(package,'BOX',box)
    package.build_gate_review()
    assert 'x'*5000+' END' in (out/'gate_review/panels.md').read_text()
    assert 'FULL USER' in (out/'gate_review/flagged_context.md').read_text()
    assert json.loads((out/'gate_review/flags.json').read_text())['models']['r16_doc']['counts']['truncated']==1
    assert not (out/'anchored_gate.approved.json').exists()


def test_finish_actions_do_not_publish_skip_early_and_archive_only_final_models():
    import pytest
    finish=load('76_run16_finish_actions.py');archive=load('77_run16_anchored_archive.py')
    decision={'action':'skip','reason':'Supervisor explicitly deferred capability protection'}
    with pytest.raises(AssertionError):finish.approved_skip(decision,False)
    assert json.loads(finish.approved_skip(decision,True))==decision
    with pytest.raises(AssertionError):finish.approved_skip({'action':'run','reason':'unapproved'},True)
    expected={'adapter_config.json':'cfg','adapter_model.safetensors':'weights'}
    assert archive.expected_files('r10_anch_chatr12',{'sha256':'weights','files':expected})==expected
    assert archive.expected_files('r10_anchp_64',{'complete':True,'sides':'both','source_config_sha256':'cfg','adapter_sha256':{'64':'weights'}})==expected
    with pytest.raises(AssertionError):archive.expected_files('checkpoint-123',{})


def test_large_adapter_copy_has_explicit_long_timeout_not_collector_timeout():
    import time
    collect=load('67_run16_collect.py');timeouts=[]
    collect.sync_results(['rsync','DRY-ONLY'],time.time()+7200,run=lambda argv,**kw:timeouts.append(kw['timeout']),attempt_timeout=3600)
    assert timeouts==[3600]
