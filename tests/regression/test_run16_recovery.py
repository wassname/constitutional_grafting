"""Bounded pre-production repair, exact-instance approval and no post-update repair. -- PI/OpenAI (Sol)"""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT=Path(__file__).resolve().parents[2]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


recovery=load('step_evidence','scripts/eval/run16_recovery.py')


def test_only_production_progress_counts(tmp_path):
    run=tmp_path/'runs/run10';run.mkdir(parents=True)
    (run/'train_random_smoke.log').write_text("3/3 [00:01] {'loss':1,'epoch':2}")
    assert recovery.production_step_evidence(tmp_path) is None
    path=run/'train_r10_eos_chatr12.log'
    path.write_text("1636/1636 [00:01] tokenization\n0/778 [00:00] {'ce_loss':1,'epoch':0}")
    assert recovery.production_step_evidence(tmp_path) is None
    path.write_text(path.read_text()+'\n1/778 [00:07, 7s/it]')
    assert recovery.production_step_evidence(tmp_path)['global_step']==1
    path.write_text("{'ce_loss':1,'epoch':0.0025}")
    assert recovery.production_step_evidence(tmp_path)['epoch']==.0025


def test_production_checkpoint_and_marker_fail_closed(tmp_path):
    path=tmp_path/'outputs/r10_eos_chatr12/checkpoint-1/trainer_state.json';path.parent.mkdir(parents=True)
    path.write_text('{"global_step":0}');assert recovery.production_step_evidence(tmp_path) is None
    path.write_text('{"global_step":1}');assert recovery.production_step_evidence(tmp_path)['global_step']==1
    path.write_text('{');assert recovery.production_step_evidence(tmp_path)
    path.unlink();marker=tmp_path/'runs/run10/production_started.json';marker.parent.mkdir(parents=True);marker.write_text('{}')
    assert recovery.production_step_evidence(tmp_path)


class Heartbeat:
    def done(self):return False


@pytest.fixture
def controller(tmp_path,monkeypatch):
    m=load('repair_controller','scripts/eval/60_run16_rental.py')
    m.OUT=tmp_path;m.rental.OUT=tmp_path/'lease';m.rental.OUT.mkdir()
    return m


def test_preproduction_failure_holds_and_restarts_only_after_approved_hotfix(controller,monkeypatch):
    m=controller;clock=[1000.];calls=[];monitors=[0]
    state={'instance_id':42,'runner_deadline_epoch':20000.,'hard_destroy_epoch':24000.}
    def monitor(*args):
        monitors[0]+=1
        if monitors[0]==1:raise AssertionError('remote comparison exited 1; inspect job.log')
    monkeypatch.setattr(m.rental,'monitor',monitor)
    def remote(command,**kw):
        calls.append(command)
        return SimpleNamespace(stdout='null' if 'production_step_evidence' in command else '')
    class Stop:
        def wait(self,seconds):
            clock[0]+=seconds
            event=json.loads((m.rental.OUT/'driver_failure.json').read_text())
            assert event['status']=='holding' and event['hold_until_epoch']==4600.
            assert not any('tmux new-session' in x for x in calls)
            patch='scripts/eval/62_run16_box.py'
            (m.OUT/'driver_repair.approved.json').write_text(json.dumps({'instance_id':42,'failure_index':0,
                'reason':'Test investigated callback fix','source_sha256':{patch:m.sha(m.ROOT/patch)}}))
    m.monitor_with_repair(remote,state,Stop(),Heartbeat(),now=lambda:clock[0])
    assert monitors[0]==2
    assert any('tar -xzf' in x for x in calls) and any('driver_failures/attempt_0' in x for x in calls)
    assert sum('tmux new-session' in x for x in calls)==1
    assert (m.rental.OUT/'driver_repair_0.approved.json').exists()
    event=json.loads((m.rental.OUT/'driver_failure.json').read_text());assert event['status']=='restarting'
    assert event['hard_destroy_epoch']==24000. and clock[0]<4600.


def test_preproduction_hold_expires_at60minutes_then_caller_destroys(controller,monkeypatch):
    m=controller;clock=[1000.];actions=[]
    def monitor(*args):raise AssertionError('remote comparison exited 1; inspect job.log')
    monkeypatch.setattr(m.rental,'monitor',monitor)
    def remote(command,**kwargs):return SimpleNamespace(stdout='null' if 'production_step_evidence' in command else '')
    class Stop:
        def wait(self,seconds):clock[0]+=seconds
    with pytest.raises(TimeoutError,match='repair window expired'):
        try:m.monitor_with_repair(remote,{'instance_id':42,'runner_deadline_epoch':20000.,'hard_destroy_epoch':24000.},Stop(),Heartbeat(),now=lambda:clock[0])
        finally:actions.extend(['retrieve','destroy'])
    assert clock[0]==4600. and actions==['retrieve','destroy']
    assert json.loads((m.rental.OUT/'driver_failure.json').read_text())['status']=='expired'


def test_after_first_production_step_no_hold_or_restart(controller,monkeypatch):
    m=controller;actions=[]
    def monitor(*args):raise AssertionError('remote comparison exited 1; inspect job.log')
    monkeypatch.setattr(m.rental,'monitor',monitor)
    def remote(command,**kwargs):
        actions.append(command);return SimpleNamespace(stdout='{"global_step":1}')
    with pytest.raises(AssertionError,match='remote comparison exited'):
        try:m.monitor_with_repair(remote,{'instance_id':42,'runner_deadline_epoch':20000.,'hard_destroy_epoch':24000.},None,Heartbeat(),now=lambda:1000.)
        finally:actions.extend(['retrieve','destroy'])
    assert not (m.rental.OUT/'driver_failure.json').exists()
    assert not any('tmux new-session' in x for x in actions)
    assert actions[-2:]==['retrieve','destroy']


def test_repair_cannot_extend_existing_runner_deadline(controller,monkeypatch):
    m=controller;clock=[1000.]
    def monitor(*args):raise AssertionError('remote comparison exited 1; inspect job.log')
    monkeypatch.setattr(m.rental,'monitor',monitor)
    def remote(command,**kwargs):return SimpleNamespace(stdout='null' if 'production_step_evidence' in command else '')
    class Stop:
        def wait(self,seconds):clock[0]+=seconds
    with pytest.raises(TimeoutError):
        m.monitor_with_repair(remote,{'instance_id':42,'runner_deadline_epoch':1010.,'hard_destroy_epoch':2000.},Stop(),Heartbeat(),now=lambda:clock[0])
    assert clock[0]==1010.


def test_six_streams_start_before_doc_wait_and_monitor_does_not_wait_for_control(controller,monkeypatch):
    m=controller;events=[]
    class Future:
        finished=False
        def __init__(self,fn,name):self.fn,self.name=fn,name
        def result(self):
            if not self.finished:
                events.append('result:'+self.name);self.fn(self.name);self.finished=True
        def done(self):return self.finished
    class Pool:
        def submit(self,fn,name):events.append('submit:'+name);return Future(fn,name)
    class Setup:
        def result(self):events.append('setup')
    plan={'adapters':{name:{'path':'/fake/'+name,'files':{'adapter_model.safetensors':{'sha256':'dry-only'}}}
                     for name in ['stoic','const','other','rewr','mix_stoic','mix_const','ctl']}}
    def remote(command,**kwargs):events.append('remote:'+command);return SimpleNamespace(stdout='')
    monkeypatch.setattr(m.subprocess,'run',lambda *a,**k:SimpleNamespace(returncode=0))
    monkeypatch.setattr(m,'start_driver',lambda *a:events.append('start'))
    monkeypatch.setattr(m,'monitor_with_repair',lambda *a:events.append('monitor'))
    m.parallel_work(remote,['fake-ssh'],'host',{'instance_id':42,'runner_deadline_epoch':m.time.time()+10000},plan,Setup(),None,None,Pool())
    assert events[:6]==['submit:'+n for n in ['stoic','const','other','rewr','mix_stoic','mix_const']]
    assert events.index('result:other')<events.index('start')<events.index('monitor')<events.index('result:ctl')


def test_approved_postproduction_policy_holds_snapshots_and_resumes(controller,monkeypatch):
    m=controller;clock=[1000.];calls=[];monitors=[0];snapshots=[]
    def monitor(*args):
        monitors[0]+=1
        if monitors[0]==1:raise AssertionError('remote comparison exited 2; inspect job.log')
    monkeypatch.setattr(m.rental,'monitor',monitor)
    def remote(command,**kwargs):
        calls.append(command);return SimpleNamespace(stdout='{"global_step":777}' if 'production_step_evidence' in command else '')
    def snapshot(index,until):
        snapshots.append((index,until))
        assert json.loads((m.rental.OUT/'driver_failure.json').read_text())['status']=='holding'
        return {'all_final_and_checkpoint_adapters_verified':True}
    class Stop:
        def wait(self,seconds):
            clock[0]+=seconds
            p='scripts/eval/61_run16_cells.py'
            (m.OUT/'driver_repair.approved.json').write_text(json.dumps({'instance_id':42,'failure_index':2,'reason':'Approved tested argv repair',
                'source_sha256':{p:m.sha(m.ROOT/p)},'resume_chat':True,'partial_models':['r16_instruct']}))
    m.monitor_with_repair(remote,{'instance_id':42,'runner_deadline_epoch':20000.,'hard_destroy_epoch':24000.},Stop(),Heartbeat(),
        now=lambda:clock[0],allow_postproduction=True,failure_index_start=2,snapshot=snapshot)
    assert snapshots==[(2,4600.)]
    assert any('--resume-chat' in command for command in calls)
    event=json.loads((m.rental.OUT/'driver_failure.json').read_text())
    assert event['post_production'] and event['failure_index']==2 and event['status']=='restarting'


def test_partial_cell_archive_does_not_move_other_doses_or_completed_cells(tmp_path):
    run=tmp_path/'run';run.mkdir()
    for name in ['replies_r16_doc1.jsonl','replies_r16_doc1.25.jsonl','draft_code_tools_r16_doc1.jsonl.wire.jsonl','job.exit']:
        (run/name).write_text('raw evidence')
    moved=recovery.archive_partial_cells(run,['r16_doc1'],1)
    assert 'replies_r16_doc1.jsonl' in moved and 'draft_code_tools_r16_doc1.jsonl.wire.jsonl' in moved
    assert (run/'replies_r16_doc1.25.jsonl').exists()
    assert (run/'driver_failures/attempt_1/replies_r16_doc1.jsonl').read_text()=='raw evidence'
    (run/'r16_doc1.25.done').write_text('{}')
    with pytest.raises(AssertionError,match='Completed cells'):
        recovery.archive_partial_cells(run,['r16_doc1.25'],2)
