"""Early artifact backups verify receipt-bound weights and safely seed final retrieval. -- PI/OpenAI (Sol)"""
import errno
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[2]
spec=importlib.util.spec_from_file_location('archive16',ROOT/'scripts/eval/73_run16_artifact_archive.py')
archive=importlib.util.module_from_spec(spec);spec.loader.exec_module(archive)


@pytest.mark.parametrize('cross_filesystem',[False,True])
def test_verified_archive_and_final_retrieval_seed(tmp_path,monkeypatch,cross_filesystem):
    target=tmp_path/'archive';canonical=tmp_path/'canonical';manifest={}
    receipts=target/'projections';receipts.mkdir(parents=True)
    weights={}
    for name in archive.ADAPTERS:
        for filename in ['adapter_config.json','adapter_model.safetensors']:
            relative='outputs/'+name+'/'+filename;path=archive.destination(target,relative)
            path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes((name+filename).encode())
            manifest[relative]=hashlib.sha256(path.read_bytes()).hexdigest()
        weights[name]=manifest['outputs/'+name+'/adapter_model.safetensors']
    (receipts/'eos_trained.json').write_text(json.dumps({'sha256':weights['r10_eos_chatr12']}))
    (receipts/'selector_gate.json').write_text(json.dumps({'report':{'adapter_sha256':weights['r10_charcap']}}))
    for label,ranks in [('p16_',[64,128]),('p16out_',[64]),('oldp_',[64])]:
        (receipts/(label+'.json')).write_text(json.dumps({'adapter_sha256':{str(rank):weights['r10_'+label+str(rank)] for rank in ranks}}))
    archive.verify_receipt_weights(target,manifest)
    if cross_filesystem:
        def no_hardlink(*args):raise OSError(errno.EXDEV,'different filesystem')
        monkeypatch.setattr(archive.os,'link',no_hardlink)
    assert len(archive.seed_final_retrieval(target,canonical))==12
    for name in archive.ADAPTERS:
        assert archive.digest(canonical/name/'adapter_model.safetensors')==weights[name]
    manifest['outputs/r10_charcap/adapter_model.safetensors']='CORRUPTED'
    with pytest.raises(AssertionError):archive.verify_receipt_weights(target,manifest)


def test_final_anchored_seed_does_not_require_or_copy_core_or_checkpoint_files(tmp_path):
    target=tmp_path/'archive';canonical=tmp_path/'canonical';name='r10_anch_chatr12'
    folder=target/'adapters'/name;folder.mkdir(parents=True)
    for filename in ['adapter_config.json','adapter_model.safetensors']:(folder/filename).write_bytes(b'DRY-FINAL-ONLY')
    seeded=archive.seed_final_retrieval(target,canonical,names=[name])
    assert len(seeded)==2 and {p.name for p in canonical.iterdir()}=={'.retrieval.lock',name}
