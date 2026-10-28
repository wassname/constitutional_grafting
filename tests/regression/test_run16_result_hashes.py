"""Post-retrieval receipts cover every copied result and reject mismatches/missing remote files. -- PI/OpenAI (Sol)"""
import hashlib
import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('result_hashes16',ROOT/'scripts/eval/74_run16_result_hashes.py')
checks=importlib.util.module_from_spec(spec);spec.loader.exec_module(checks)


def test_all_retrieved_results_verified_with_zero_delimited_sha256sum(tmp_path):
    remote={}
    for name,text in [('replies.jsonl','{"dry_run_only":true}\n'),('logs/spaced log.txt','dry-only log\n')]:
        path=tmp_path/name;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
        remote[name]=hashlib.sha256(path.read_bytes()).hexdigest()
    output=b''.join(digest.encode()+b'  '+name.encode()+b'\0' for name,digest in remote.items())
    parsed=checks.parse_sha256sum(output)
    receipt=checks.compare_result_hashes(tmp_path,parsed)
    assert receipt['all_match'] and set(receipt['files'])==set(remote)


def test_changed_and_missing_results_are_not_verified(tmp_path):
    (tmp_path/'changed.log').write_text('new')
    (tmp_path/'missing.json').write_text('{}')
    receipt=checks.compare_result_hashes(tmp_path,{'changed.log':hashlib.sha256(b'old').hexdigest()})
    assert not receipt['all_match']
    assert receipt['mismatches']==['changed.log','missing.json']
