"""Real cell-driver command construction must pass each downstream script's native argparse. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
from types import SimpleNamespace

import pytest

ROOT=Path(__file__).resolve().parents[2]


def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


contracts=load('cli_contracts',ROOT/'scripts/eval/run16_cli_contracts.py')


def execute_real_cells(tmp_path,monkeypatch,source=None):
    driver=load('real_cells',source or ROOT/'scripts/eval/61_run16_cells.py')
    driver.ROOT=ROOT
    out=tmp_path/'out';out.mkdir()
    manifest=json.loads((ROOT/'slop/eval/run16_v2/inputs/run16_manifest.json').read_text())
    for name in driver.INPUTS:
        data=(ROOT/'slop/eval/run16_v2/inputs'/name).read_bytes()
        (out/name).write_bytes(data)
    model=tmp_path/manifest['instruct_revision'];model.mkdir();(model/'config.json').write_text('{}')
    manifest['instruct_config_sha256']=hashlib.sha256(b'{}').hexdigest()
    (out/'run16_manifest.json').write_text(json.dumps(manifest))
    adapter=tmp_path/'adapter';adapter.mkdir();(adapter/'adapter_model.safetensors').write_bytes(b'DRY-ONLY')
    monkeypatch.setenv('RUN9_DEADLINE_EPOCH',str(driver.time.time()+3600));monkeypatch.setenv('RUN9_INSTRUCT_PATH',str(model))
    monkeypatch.setattr(sys,'argv',['61_run16_cells.py','--run-dir',str(out),'--adapter','const='+str(adapter),'--cells','const=0'])
    commands=[]
    def run(argv,**kwargs):
        argv=list(map(str,argv));commands.append(argv)
        script=Path(argv[1]);args=contracts.validate_argv(script,argv[2:])
        if script.name=='02_merge.py':
            merged=Path(args.out);merged.mkdir()
            (merged/'merge_report.json').write_text(json.dumps({'groups':{},'dtype':'float16','adapters':[{}]}))
        elif script.name=='19_gen_replies.py':
            items=[json.loads(l) for l in Path(args.items).open()]
            records=[{'dry_run_only':True,'model':args.model,'item_id':it['id'],'sample':s,
                      'turns':[{'user':u,'assistant':'DRY-RUN ONLY','finish_reason':'stop','n_tokens':3,'marker_violation':False} for u in it['turns']]} for it in items for s in range(args.samples)]
            Path(args.out).write_text(''.join(json.dumps(r)+'\n' for r in records))
        elif script.name=='26_gsm8k.py':
            assert args.n==60 and Path(args.items).name=='gsm8k_long60.jsonl'
            Path(args.out).write_text(''.join(json.dumps({'dry_run_only':True,'correct':False})+'\n' for _ in range(60)))
        else:raise AssertionError(script)
        return SimpleNamespace(returncode=0)
    class Server:
        pid=99999999
        def poll(self):return None
        def wait(self,timeout=None):return 0
    monkeypatch.setattr(driver.subprocess,'run',run);monkeypatch.setattr(driver.subprocess,'Popen',lambda *a,**k:Server())
    monkeypatch.setattr(driver.os,'killpg',lambda *a:None)
    monkeypatch.setattr(driver.urllib.request,'urlopen',lambda *a,**k:io.StringIO('{"data":[{"id":"r16_instruct"}]}'))
    driver.main()
    return out,commands


def test_every_real_cell_subprocess_argv_matches_native_argparse(tmp_path,monkeypatch):
    out,commands=execute_real_cells(tmp_path,monkeypatch)
    assert len(commands)==8
    assert (out/'r16_instruct.done').exists()
    gsm=next(a for a in commands if Path(a[1]).name=='26_gsm8k.py')
    assert gsm[-2:]==['--items',str(out/'gsm8k_long60.jsonl')]
    generation=[contracts.validate_argv(a[1],a[2:]) for a in commands if Path(a[1]).name=='19_gen_replies.py']
    assert {Path(a.items).name for a in generation}=={'items.jsonl','demos.jsonl','panel.jsonl','pov.jsonl','small_tasks.jsonl','draft_code_tools.jsonl'}


def test_native_parser_rejects_original_extra_gsm_arguments(tmp_path,monkeypatch):
    source=(ROOT/'scripts/eval/61_run16_cells.py').read_text()
    fixed='out / "gsm8k_long60.jsonl"], f"gsm8k_{tag}.log")'
    assert fixed in source
    broken=tmp_path/'broken_cells.py'
    broken.write_text(source.replace(fixed,'out / "gsm8k_long60.jsonl", "small_tasks.jsonl", "draft_code_tools.jsonl"], f"gsm8k_{tag}.log")'))
    with pytest.raises(SystemExit) as error:execute_real_cells(tmp_path,monkeypatch,broken)
    assert error.value.code==2
    assert not (tmp_path/'out/r16_instruct.done').exists()


def test_resume_entrypoint_flags_use_native_parsers():
    assert contracts.validate_argv(ROOT/'scripts/eval/62_run16_box.py',['--resume-chat']).resume_chat
    assert contracts.validate_argv(ROOT/'scripts/eval/60_run16_rental.py',['resume-chat']).action=='resume-chat'
