"""LoRA projection away from exact Base→Instruct singular subspaces: both sides, or output/input side only. -- PI/OpenAI (Sol); sides by PI/Claude"""
import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

import torch
from beartype import beartype
from safetensors import safe_open
from jaxtyping import Float, jaxtyped
from safetensors.torch import load_file, save_file
from torch import Tensor


@jaxtyped(typechecker=beartype)
def project_factors(A: Float[Tensor, '*batch r i'], B: Float[Tensor, '*batch o r'],
                    U: Float[Tensor, '*batch o k'], V: Float[Tensor, '*batch i k'], sides: str = 'both'
                    ) -> tuple[Float[Tensor, '*batch r i'], Float[Tensor, '*batch o r']]:
    """both: (I-UUᵀ)ΔW(I-VVᵀ); output: (I-UUᵀ)ΔW, Safe LoRA's side; input: ΔW(I-VVᵀ)."""
    assert sides in ('both', 'output', 'input'), sides
    return (A if sides == 'output' else A - (A @ V) @ V.mT), (B if sides == 'input' else B - U @ (U.mT @ B))


@jaxtyped(typechecker=beartype)
def frobenius_squared(A: Float[Tensor, '*batch r i'], B: Float[Tensor, '*batch o r']) -> Float[Tensor, '*batch']:
    a, b = A.double(), B.double()
    return ((a @ a.mT) * (b.mT @ b)).sum(dim=(-2, -1))


def unpack_factors(A, B, experts):
    return A.reshape(experts, -1, A.shape[-1]), B.reshape(B.shape[0], -1, experts).permute(2, 0, 1)


def pack_factors(A, B):
    return A.flatten(0, 1).contiguous(), B.permute(1, 2, 0).flatten(1).contiguous()


def parameter_name(stem):
    name = stem.removeprefix('base_model.model.')
    assert name != stem
    if name.endswith('.mlp.experts.base_layer'):
        return name.removesuffix('.base_layer') + '.gate_up_proj'
    if name.endswith('.mlp.experts'):
        return name + '.down_proj'
    assert '.mlp.experts' not in name, stem
    return name + '.weight'


def tensor(path, index, name):
    with safe_open(str(path / index[name]), framework='pt', device='cpu') as stream:
        return stream.get_tensor(name)


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('base', type=Path)
    parser.add_argument('instruct', type=Path)
    parser.add_argument('adapter', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--ranks', type=int, nargs='+', default=[16, 64])
    parser.add_argument('--device', default='cuda')
    parser.add_argument('--save-basis', type=Path, help='Save per-stem batched U/V in fp16 safetensors for OrthoPlugin')
    parser.add_argument('--basis-rank', type=int, default=64, help='Rank of the saved basis (64 for production)')
    parser.add_argument('--batch-experts', type=int, default=8)
    parser.add_argument('--sides', choices=['both', 'output', 'input'], default='both')
    parser.add_argument('--module-limit', type=int, help='Production path smoke only; output is deliberately marked incomplete')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    config = json.loads((args.adapter / 'adapter_config.json').read_text())
    assert not config['use_rslora'] and not config['fan_in_fan_out']
    assert config['target_parameters'] == ['mlp.experts.gate_up_proj', 'mlp.experts.down_proj']
    assert config['lora_alpha'] / config['r'] == 2
    assert all(config['alpha_pattern'][key] / rank == 2 for key, rank in config['rank_pattern'].items())
    b_index = json.loads((args.base / 'model.safetensors.index.json').read_text())['weight_map']
    i_index = json.loads((args.instruct / 'model.safetensors.index.json').read_text())['weight_map']
    model_config = json.loads((args.base / 'config.json').read_text())['text_config']
    n_experts = model_config['num_experts']
    assert n_experts > 0
    weights = load_file(str(args.adapter / 'adapter_model.safetensors'))
    stems = sorted(key.removesuffix('.lora_A.weight') for key in weights if key.endswith('.lora_A.weight'))
    assert stems and len(weights) == 2 * len(stems)
    svd_rank = max(args.ranks + ([args.basis_rank] if args.save_basis else []))
    assert min(args.ranks) > 0 and (not args.save_basis or args.basis_rank > 0)
    if args.save_basis:
        assert args.module_limit is None, 'Cannot save an incomplete training basis'
        assert not args.save_basis.exists(), args.save_basis
    bases, basis_error = {}, {'max_abs': 0., 'max_relative_fro': 0.}
    outputs = {rank: {} for rank in args.ranks}
    rows = []
    started = time.time()
    print(json.dumps({'argv': vars(args), 'adapter_sha256': sha(args.adapter / 'adapter_model.safetensors'),
                      'method': f'sides={args.sides}: (I-U_kU_kT) B A (I-V_kV_kT) restricted to those sides; exact full SVD, truncated to k; checkpoint subtraction in fp32; factors saved fp32'}, default=str), flush=True)
    print('SHOULD: projection leaves original LoRA rank/scale unchanged; removed energy + retained energy = original energy. -- PI/OpenAI', flush=True)
    for stem in stems[:args.module_limit]:
        name = parameter_name(stem)
        A0, B0 = weights[stem + '.lora_A.weight'], weights[stem + '.lora_B.weight']
        assert A0.dtype == B0.dtype == torch.float32
        experts = n_experts if '.mlp.experts.' in name else 1
        A, B = unpack_factors(A0.to(args.device), B0.to(args.device), experts)
        delta_post = tensor(args.instruct, i_index, name).float() - tensor(args.base, b_index, name).float()
        if experts == 1:
            delta_post = delta_post.unsqueeze(0)
        assert delta_post.shape == (experts, B.shape[1], A.shape[2]), (name, delta_post.shape, A.shape, B.shape)
        assert min(delta_post.shape[-2:]) >= svd_rank
        original_sq = 4 * frobenius_squared(A, B)
        projected = {rank: (torch.empty_like(A), torch.empty_like(B)) for rank in args.ranks}
        spectra = []
        if args.save_basis:
            bases[stem + '.U'] = torch.empty(experts, B.shape[1], args.basis_rank, dtype=torch.float16)
            bases[stem + '.V'] = torch.empty(experts, A.shape[2], args.basis_rank, dtype=torch.float16)
        for begin in range(0, experts, args.batch_experts):
            end = min(experts, begin + args.batch_experts)
            post = delta_post[begin:end].to(args.device)
            options = {'driver': 'gesvd'} if post.is_cuda else {}
            U, S, Vh = torch.linalg.svd(post, full_matrices=False, **options)
            assert torch.isfinite(S).all() and (S[:, svd_rank - 1] > 0).all(), name
            spectra.append(S[:, [0, min(15, S.shape[-1] - 1), min(63, S.shape[-1] - 1)]].cpu())
            if args.save_basis:
                for side, exact in [('U', U[..., :args.basis_rank]), ('V', Vh[..., :args.basis_rank, :].mT)]:
                    saved = exact.half()
                    error = exact - saved.float()
                    basis_error['max_abs'] = max(basis_error['max_abs'], error.abs().max().item())
                    basis_error['max_relative_fro'] = max(basis_error['max_relative_fro'], (error.norm() / exact.norm()).item())
                    bases[stem + '.' + side][begin:end] = saved.cpu()
            for rank in args.ranks:
                pa, pb = project_factors(A[begin:end], B[begin:end], U[..., :rank], Vh[..., :rank, :].mT, args.sides)
                projected[rank][0][begin:end] = pa
                projected[rank][1][begin:end] = pb
            del post, U, S, Vh
        spectra = torch.cat(spectra)
        for rank, (pa, pb) in projected.items():
            retained_sq = 4 * frobenius_squared(pa, pb)
            removed_sq = original_sq - retained_sq
            assert torch.isfinite(retained_sq).all() and (removed_sq >= 0).all(), name
            packed_a, packed_b = pack_factors(pa, pb)
            outputs[rank][stem + '.lora_A.weight'] = packed_a.cpu()
            outputs[rank][stem + '.lora_B.weight'] = packed_b.cpu()
            record = {'parameter': name, 'module_class': 'experts' if experts > 1 else 'shared' if '.shared_expert.' in name else 'attention',
                      'k': rank, 'experts': experts, 'original_squared_fro': original_sq.sum().item(),
                      'retained_squared_fro': retained_sq.sum().item(), 'removed_squared_fro': removed_sq.sum().item(),
                      'removed_energy_fraction': (removed_sq.sum() / original_sq.sum()).item(),
                      'removed_component_norm_fraction': (removed_sq.sum() / original_sq.sum()).sqrt().item(),
                      'per_expert_removed_energy_fraction': (removed_sq / original_sq).cpu().tolist(),
                      'post_sigma1_16_64_mean': spectra.mean(0).tolist()}
            rows.append(record)
            with (args.output / 'modules.jsonl').open('a') as stream:
                stream.write(json.dumps(record) + '\n')
        print(f'PROJECTED {len(rows) // len(args.ranks)}/{len(stems)} {name} elapsed={time.time() - started:.1f}s', flush=True)
        del A, B, delta_post, projected
    summary = []
    for rank in args.ranks:
        for group in ['attention', 'shared', 'experts']:
            selected = [r for r in rows if r['k'] == rank and r['module_class'] == group]
            original = sum(r['original_squared_fro'] for r in selected)
            removed = sum(r['removed_squared_fro'] for r in selected)
            if selected:
                summary.append({'k': rank, 'module_class': group, 'modules': len(selected), 'matrices': sum(r['experts'] for r in selected),
                                'original_squared_fro': original, 'removed_squared_fro': removed,
                                'removed_energy_fraction': removed / original, 'removed_component_norm_fraction': (removed / original) ** .5})
        destination = args.output / f'k{rank}'
        destination.mkdir()
        shutil.copyfile(args.adapter / 'adapter_config.json', destination / 'adapter_config.json')
        save_file(outputs[rank], str(destination / 'adapter_model.safetensors'))
    if args.save_basis:
        args.save_basis.parent.mkdir(parents=True, exist_ok=True)
        save_file(bases, str(args.save_basis), metadata={
            'format': 'ortho-v1', 'rank': str(args.basis_rank),
            'base_revision': args.base.name, 'instruct_revision': args.instruct.name,
            'fp16_error': json.dumps(basis_error)})
    report = {'basis_path': str(args.save_basis) if args.save_basis else None,
              'basis_fp16_error': basis_error if args.save_basis else None,
              'author': 'PI/OpenAI (Sol)', 'complete': args.module_limit is None, 'sides': args.sides,
              'base_revision': args.base.name, 'instruct_revision': args.instruct.name,
              'source_adapter_sha256': sha(args.adapter / 'adapter_model.safetensors'),
              'source_config_sha256': sha(args.adapter / 'adapter_config.json'), 'source_code_sha256': sha(__file__),
              'elapsed_seconds': time.time() - started, 'peak_cuda_bytes': torch.cuda.max_memory_allocated() if args.device == 'cuda' else None,
              'definition': 'removed component Frobenius/original Frobenius = sqrt(1-retained squared Frobenius/original squared Frobenius)',
              'summary': summary, 'adapter_sha256': {str(rank): sha(args.output / f'k{rank}/adapter_model.safetensors') for rank in args.ranks}}
    (args.output / 'projection.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__':
    main()
