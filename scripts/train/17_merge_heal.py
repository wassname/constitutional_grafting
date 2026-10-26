"""Merge one heal with fp32 update/accumulation, round once to fp16. -- PI/OpenAI (Sol)"""
import argparse
import json
from pathlib import Path


def merge_heal(model, adapter):
    import torch
    from peft import PeftModel
    wrapped = PeftModel.from_pretrained(model, adapter)
    reports = []
    with torch.no_grad():
        for name, module in list(wrapped.named_modules()):
            if not hasattr(module, 'lora_A') or 'default' not in module.lora_A:
                continue
            assert not module.use_dora['default']
            module.lora_A['default'].to(torch.float32)
            module.lora_B['default'].to(torch.float32)
            base = module.get_base_layer()
            parameter = getattr(base, module.parameter_name) if hasattr(module, 'parameter_name') else base.weight
            dtype = parameter.dtype
            delta = module.get_delta_weight('default').float()
            before = parameter.detach().float()
            updated = (before + delta).to(dtype)
            actual = updated.float() - before
            requested_norm = delta.norm()
            reports.append({'module': name, 'dtype': str(dtype), 'requested_fro': requested_norm.item(),
                'stored_fro': actual.norm().item(), 'nonzero_stored_elements': int(actual.count_nonzero()),
                'rounding_error_rel': ((actual - delta).norm() / requested_norm).item() if requested_norm > 0 else 0})
            assert torch.isfinite(updated).all()
            parameter.data = updated
            module.merged_adapters.append('default')
            del delta, before, updated, actual
    assert reports and any(r['nonzero_stored_elements'] for r in reports)
    return wrapped.unload(), reports


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('parent')
    parser.add_argument('adapter')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    import torch
    from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
    model = AutoModelForImageTextToText.from_pretrained(args.parent, dtype=torch.float16, device_map='cuda')
    model, reports = merge_heal(model, args.adapter)
    model.save_pretrained(args.output, safe_serialization=True, max_shard_size='10GB')
    AutoTokenizer.from_pretrained(args.parent).save_pretrained(args.output)
    AutoProcessor.from_pretrained(args.parent).save_pretrained(args.output)
    (args.output / 'heal_merge_report.json').write_text(json.dumps({'author': 'PI/OpenAI (Sol)',
        'parent': args.parent, 'adapter': args.adapter, 'accumulation_dtype': 'float32', 'saved_dtype': 'float16', 'modules': reports}, indent=2) + '\n')
