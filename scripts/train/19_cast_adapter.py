"""Copy a LoRA adapter with its weights cast to bf16, to halve upload size. Merges run in fp16, so the rounding is below the merge's own.
usage: python scripts/train/19_cast_adapter.py SRC_DIR DST_DIR   -- PI/Claude (opus-5-5)"""
import json
import shutil
import sys
from pathlib import Path

import torch
from safetensors.torch import load_file, save_file

src, dst = map(Path, sys.argv[1:3])
dst.mkdir(parents=True, exist_ok=False)
w = load_file(str(src / 'adapter_model.safetensors'))
cast = {k: v.to(torch.bfloat16) for k, v in w.items()}
rel = max(((v.float() - cast[k].float()).norm() / v.float().norm()).item() for k, v in w.items())
save_file(cast, str(dst / 'adapter_model.safetensors'))
shutil.copyfile(src / 'adapter_config.json', dst / 'adapter_config.json')
(dst / 'cast.json').write_text(json.dumps({'source': str(src), 'dtype': 'bfloat16', 'max_relative_fro_error': rel}) + '\n')
print(json.dumps({'source': str(src), 'tensors': len(w), 'max_relative_fro_error': rel}))
