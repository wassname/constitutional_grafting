"""Identify the first completed production update without changing the frozen training plugin. -- PI/OpenAI (Sol)"""
import json
from pathlib import Path
import re


def production_step_evidence(root):
    """Return evidence once production (not random smoke/data preparation) has taken a step."""
    root=Path(root);run=root/'runs/run10';adapter=root/'outputs/r10_eos_chatr12'
    for path in [run/'production_started.json',run/'eos_trained.json',adapter/'adapter_model.safetensors']:
        if path.exists():return {'source':str(path),'reason':'durable production marker or final adapter'}
    for path in adapter.glob('checkpoint-*/trainer_state.json'):
        try:step=json.loads(path.read_text())['global_step']
        except (ValueError,KeyError):return {'source':str(path),'reason':'production checkpoint exists; fail closed on incomplete state'}
        if step>=1:return {'source':str(path),'global_step':step}
    path=run/'train_r10_eos_chatr12.log'
    if not path.exists():return None
    text=path.read_text(errors='replace')
    # Locked 1,636-row, two-epoch recipe: recorded run10 progress has 777/778 optimizer updates.
    # Tokenization bars are /1636; random smoke has its own log, never counted here.
    for step,total in re.findall(r'(\d+)/(777|778)\s*\[',text):
        if int(step)>=1:return {'source':str(path),'global_step':int(step),'total_updates':int(total)}
    for line in text.replace('\r','\n').splitlines():
        if "'ce_loss'" not in line and "'loss'" not in line:continue
        epoch=re.search(r"'epoch'\s*:\s*['\"]?([0-9.eE+\-]+)",line)
        if epoch and float(epoch[1])>0:return {'source':str(path),'epoch':float(epoch[1])}
    return None


def archive_partial_cells(run_dir,models,failure_index):
    """Preserve incomplete cell outputs and failed job logs, never overwrite a completed cell."""
    import shutil
    run=Path(run_dir);destination=run/'driver_failures'/f'attempt_{failure_index}'
    destination.mkdir(parents=True,exist_ok=True)
    names={'job.log','job.exit'}
    for model in models:
        assert re.fullmatch(r'r16_[A-Za-z0-9_.\-]+',model),model
        assert not (run/(model+'.done')).exists(),'Completed cells are not partial: '+model
        for prefix in ['replies_','demos_','panel_','pov_','small_tasks_','draft_code_tools_','gsm8k_','merge_','vllm_']:
            for suffix in ['.jsonl','.jsonl.wire.jsonl','.jsonl.meta.json','.log','.json','.argv.json']:
                names.add(prefix+model+suffix);names.add('gen_'+prefix+model+suffix)
    moved=[]
    for name in sorted(names):
        source=run/name
        if source.is_file():
            assert not (destination/name).exists(),'Refuse to overwrite failure evidence: '+name
            shutil.move(str(source),str(destination/name));moved.append(name)
    return moved
