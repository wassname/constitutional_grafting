"""Keep the chat adapter's action on inputs that character data uses more than capability data. -- PI/Claude (opus-5-5)

Per LoRA module, with per-token input second moments C_char, C_cap measured on the deployed graft:
    C_char v = λ C_cap v           generalized eigenproblem, ridge εI added to both so unseen directions get λ ≈ 1
    Q = C_cap V_keep V_keepᵀ       each row of A is a functional a; its coordinates u = Vᵀ C_cap a split its energy:
    A′ = A Q                       aᵀC_cap a = Σ u_i², aᵀC_char a = Σ λ_i u_i². Dropping small-λ u_i lowers both, never raises.
                                   Input side only; LoRA rank, B and scale unchanged.
V_keep = {v : λ ≥ τ}. One global τ, set so the removed weight energy matches --removed-energy (run-14 P₆₄ removed 0.15).
This is the input-side (activation) half of a K-FAC curvature estimate: output-gradient covariance is taken as I.
Routed-expert gate_up reads the layer-wide MoE input covariance: per-expert hidden covariances (256×2048² per layer) do not fit.
Routed-expert down_proj uses per-expert covariances, shrunk toward the layer's pooled expert covariance with --shrink tokens.

usage: collect MODEL DATA.jsonl OUT.pt [--rows N] [--layers A:B]   (run once per data set; shards over layers merge in project)
       project ADAPTER OUT_DIR --char C.pt.. --cap C.pt.. [--removed-energy .15 | --tau T]
       measure ADAPTER.. --char C.pt.. --cap C.pt..                 (fraction of each adapter's input energy on each data set)
"""
import argparse
import hashlib
import importlib.util
import json
import random
import re
import shutil
import types
from collections import defaultdict
from pathlib import Path

import torch
from beartype import beartype
from jaxtyping import Float, jaxtyped
from safetensors.torch import load_file, save_file
from torch import Tensor

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('projection16', ROOT / 'scripts/train/16_project_chat_adapter.py')
p16 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p16)

GROUP = {'self_attn.q_proj': 'attn_in', 'self_attn.k_proj': 'attn_in', 'self_attn.v_proj': 'attn_in',
         'linear_attn.in_proj_qkv': 'attn_in', 'linear_attn.in_proj_z': 'attn_in',
         'self_attn.o_proj': 'attn_out', 'linear_attn.out_proj': 'attn_out',
         'mlp.shared_expert.gate_proj': 'mlp_in', 'mlp.shared_expert.up_proj': 'mlp_in', 'mlp.experts.gate_up_proj': 'mlp_in',
         'mlp.shared_expert.down_proj': 'shared_down', 'mlp.experts.down_proj': 'expert_down'}
HOOKED = {'self_attn.q_proj': 'attn_in', 'linear_attn.in_proj_qkv': 'attn_in', 'self_attn.o_proj': 'attn_out',
          'linear_attn.out_proj': 'attn_out', 'mlp.shared_expert.gate_proj': 'mlp_in', 'mlp.shared_expert.down_proj': 'shared_down'}


def cov_key(parameter: str) -> str:
    layer, rest = re.search(r'layers\.(\d+)\.(.+?)(?:\.weight)?$', parameter).groups()
    return f'{layer}.{GROUP[rest]}'


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def patch_experts(module, key, S, N, mask_flat):
    """Eager Qwen3_5MoeExperts.forward, plus per-expert down_proj input moments (unweighted by routing, as the matrix sees them)."""
    def forward(self, hidden_states, top_k_index, top_k_weights):
        out = torch.zeros_like(hidden_states)
        mask = mask_flat['m']
        if key not in S:
            S[key] = torch.zeros(self.num_experts, self.intermediate_dim, self.intermediate_dim, device=hidden_states.device)
            N[key] = torch.zeros(self.num_experts, device=hidden_states.device)
        for e in torch.unique(top_k_index).tolist():
            if e == self.num_experts:
                continue
            token, pos = torch.where(top_k_index == e)
            gate, up = torch.nn.functional.linear(hidden_states[token], self.gate_up_proj[e]).chunk(2, dim=-1)
            h = self.act_fn(gate) * up
            kept = h[mask[token]].float()
            S[key][e] += kept.T @ kept
            N[key][e] += kept.shape[0]
            y = torch.nn.functional.linear(h, self.down_proj[e]) * top_k_weights[token, pos, None]
            out.index_add_(0, token, y.to(out.dtype))
        return out
    module.forward = types.MethodType(forward, module)


# ---------------------------------------------------------------- collect

def collect(args):
    from transformers import AutoModelForImageTextToText, AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=getattr(torch, args.dtype), device_map=args.device).eval()
    rows = [json.loads(line) for line in args.data.open()]
    random.Random(0).shuffle(rows)
    texts = [''.join(s['text'] for s in row['segments']) for row in rows[:args.rows]]
    first, last = map(int, args.layers.split(':')) if args.layers else (0, 10 ** 9)
    S, N = {}, defaultdict(int)
    mask_flat = {}

    def accumulate(key, x):
        x = x.reshape(-1, x.shape[-1])[mask_flat['m']].float()
        S[key] = S.get(key, 0) + x.T @ x
        N[key] += x.shape[0]

    def hook(key):
        return lambda module, inputs: accumulate(key, inputs[0])

    hooked = 0
    for name, module in model.named_modules():
        found = re.search(r'language_model\.layers\.(\d+)\.(.+)$', name)
        if not found or not first <= int(found[1]) < last:
            continue
        layer, rest = found.groups()
        if rest in HOOKED:
            module.register_forward_pre_hook(hook(f'{layer}.{HOOKED[rest]}'))
            hooked += 1
        elif rest == 'mlp.experts':
            patch_experts(module, f'{layer}.expert_down', S, N, mask_flat)
            hooked += 1
    assert hooked, 'no modules hooked'
    print(json.dumps({'model': str(args.model), 'data': str(args.data), 'rows': len(texts), 'layers': args.layers, 'hooked': hooked}), flush=True)
    decoder = model.model.language_model
    with torch.inference_mode():
        for begin in range(0, len(texts), args.batch):
            batch = tokenizer(texts[begin:begin + args.batch], add_special_tokens=False, padding=True, truncation=True,
                              max_length=args.max_length, return_tensors='pt', padding_side='right').to(args.device)
            mask_flat['m'] = batch['attention_mask'].reshape(-1).bool()
            decoder(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'])
            if begin // args.batch % 20 == 0:
                print(f'COLLECT {begin + len(batch["input_ids"])}/{len(texts)} tokens={int(mask_flat["m"].sum())}', flush=True)
    tokens = {key: N[key].cpu() if torch.is_tensor(N[key]) else N[key] for key in S}
    torch.save({'sum': {key: value.cpu() for key, value in S.items()}, 'tokens': tokens,
                'meta': {'model': str(args.model), 'data': str(args.data), 'data_sha256': sha(args.data), 'rows': len(texts),
                         'max_length': args.max_length, 'layers': args.layers}}, args.out)
    print('SHOULD: every hooked key has >0 tokens; attn_in/mlp_in token counts equal the masked token total. -- PI/Claude', flush=True)
    print(json.dumps({k: (int(v.sum()) if torch.is_tensor(v) else v) for k, v in sorted(tokens.items())[:6]}), flush=True)


def load_moments(paths: list[Path], shrink: float) -> dict[str, Tensor]:
    """Merge layer shards and return per-token second moments; expert_down is shrunk toward the layer's pooled expert moment."""
    total, count = {}, {}
    for path in paths:
        blob = torch.load(path, weights_only=False)
        for key, value in blob['sum'].items():
            assert key not in total, f'{key} in two shards'
            total[key], count[key] = value.double(), blob['tokens'][key]
    moments = {}
    for key, value in total.items():
        if key.endswith('expert_down'):
            n = count[key].double()
            pooled = value.sum(0) / n.sum()
            moments[key] = (value + shrink * pooled) / (n + shrink)[:, None, None]
        else:
            moments[key] = value / count[key]
    return moments


# ---------------------------------------------------------------- project

@jaxtyped(typechecker=beartype)
def generalized_eig(C_char: Float[Tensor, '*b d d'], C_cap: Float[Tensor, '*b d d'], eps: float
                    ) -> tuple[Float[Tensor, '*b d'], Float[Tensor, '*b d d'], Float[Tensor, '*b d d']]:
    """λ, V with C_char V = C_cap V diag(λ) and Vᵀ C_cap V = I, after adding the same ridge to both; also returns ridged C_cap."""
    d = C_cap.shape[-1]
    ridge = eps * C_cap.diagonal(dim1=-2, dim2=-1).mean(-1)[..., None, None] * torch.eye(d, dtype=C_cap.dtype, device=C_cap.device)
    cap, char = C_cap + ridge, C_char + ridge
    L = torch.linalg.cholesky(cap)
    Linv = torch.linalg.solve_triangular(L, torch.eye(d, dtype=cap.dtype, device=cap.device).expand_as(L), upper=False)
    lam, Y = torch.linalg.eigh(Linv @ char @ Linv.mT)
    return lam, Linv.mT @ Y, cap


def projector(lam, V, cap, tau: float):
    """Right-multiplier for A. Not V_keep V_keepᵀ C_cap: that projects inputs and can raise the adapter's energy (2× on a toy)."""
    return cap @ (V * (lam >= tau)[..., None, :].to(V.dtype)) @ V.mT


def input_energy(A, B, C):
    """tr(BᵀB · A C Aᵀ) summed over the batch: mean squared change of the module output per token, up to the LoRA scale²."""
    return ((B.mT @ B) * (A @ C @ A.mT)).sum(dim=(-2, -1)).sum().item()


def modules(adapter: Path, experts: int, device):
    weights = load_file(str(adapter / 'adapter_model.safetensors'))
    for stem in sorted(key.removesuffix('.lora_A.weight') for key in weights if key.endswith('.lora_A.weight')):
        name = p16.parameter_name(stem)
        n = experts if '.mlp.experts.' in name else 1
        A, B = p16.unpack_factors(weights[stem + '.lora_A.weight'].float().to(device), weights[stem + '.lora_B.weight'].float().to(device), n)
        yield stem, name, A, B


def project(args):
    char, cap = load_moments(args.char, args.shrink), load_moments(args.cap, args.shrink)
    assert char.keys() == cap.keys()
    experts = next(v.shape[0] for k, v in cap.items() if k.endswith('expert_down'))
    eig = {}
    for key in cap:  # eigendecomposition in float64, stored float32 to fit 40 layers × 256 experts × 512² on one GPU
        lam, V, ridged = generalized_eig(char[key].to(args.device), cap[key].to(args.device), args.eps)
        eig[key] = (lam, V.float(), ridged.float())
    items = list(modules(args.adapter, experts, args.device))
    assert {cov_key(name) for _, name, _, _ in items} <= eig.keys(), sorted({cov_key(n) for _, n, _, _ in items} - eig.keys())[:5]
    original = sum(p16.frobenius_squared(A, B).sum().item() for _, _, A, B in items)

    def removed(tau):
        kept = sum(p16.frobenius_squared(A @ projector(*eig[cov_key(name)], tau), B).sum().item() for _, name, A, B in items)
        return 1 - kept / original

    if args.tau is None:  # removed Frobenius energy is not monotone in τ (Q is oblique in the plain weight metric): grid, not bisection
        low, high = min(v[0].min().item() for v in eig.values()), max(v[0].max().item() for v in eig.values())
        assert low > 0
        grid = torch.logspace(torch.log10(torch.tensor(low)), torch.log10(torch.tensor(high)), 40).tolist()
        tau = min(grid, key=lambda t: abs(removed(t) - args.removed_energy))
    else:
        tau = args.tau
    args.output.mkdir(parents=True, exist_ok=False)
    source = load_file(str(args.adapter / 'adapter_model.safetensors'))
    out, rows = dict(source), []
    for stem, name, A, B in items:
        key = cov_key(name)
        Q = projector(*eig[key], tau)
        A2 = A @ Q
        packed_a, _ = p16.pack_factors(A2.float(), B.float())
        out[stem + '.lora_A.weight'] = packed_a.cpu().contiguous()
        C_char, C_cap = char[key].float().to(args.device), cap[key].float().to(args.device)
        rows.append({'parameter': name, 'key': key, 'dropped_directions_mean': float((eig[key][0] < tau).double().sum(-1).mean()),
                     'weight_energy': [p16.frobenius_squared(A, B).sum().item(), p16.frobenius_squared(A2, B).sum().item()],
                     'char_energy': [input_energy(A, B, C_char), input_energy(A2, B, C_char)],
                     'cap_energy': [input_energy(A, B, C_cap), input_energy(A2, B, C_cap)]})
    shutil.copyfile(args.adapter / 'adapter_config.json', args.output / 'adapter_config.json')
    save_file(out, str(args.output / 'adapter_model.safetensors'))
    total = {k: [sum(r[k][i] for r in rows) for i in (0, 1)] for k in ('weight_energy', 'char_energy', 'cap_energy')}
    report = {'author': 'PI/Claude (opus-5-5)', 'tau': tau, 'eps': args.eps, 'shrink': args.shrink,
              'removed_weight_energy': 1 - total['weight_energy'][1] / total['weight_energy'][0],
              'kept_char_input_energy': total['char_energy'][1] / total['char_energy'][0],
              'kept_cap_input_energy': total['cap_energy'][1] / total['cap_energy'][0],
              'source_adapter_sha256': sha(args.adapter / 'adapter_model.safetensors'), 'source_code_sha256': sha(__file__),
              'char': [str(p) for p in args.char], 'cap': [str(p) for p in args.cap],
              'adapter_sha256': sha(args.output / 'adapter_model.safetensors')}
    (args.output / 'modules.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in rows))
    (args.output / 'projection.json').write_text(json.dumps(report, indent=2) + '\n')
    print('SHOULD: kept_char_input_energy > kept_cap_input_energy; removed_weight_energy ≈ --removed-energy. -- PI/Claude', flush=True)
    print(json.dumps(report), flush=True)


def measure(args):
    """Same input-energy diagnostic for any adapters (e.g. plain, P₆₄): which share of its action on each data set it keeps."""
    char, cap = load_moments(args.char, args.shrink), load_moments(args.cap, args.shrink)
    experts = next(v.shape[0] for k, v in cap.items() if k.endswith('expert_down'))
    for adapter in args.adapters:
        total = defaultdict(float)
        for _, name, A, B in modules(adapter, experts, args.device):
            key = cov_key(name)
            total['weight'] += p16.frobenius_squared(A, B).sum().item()
            total['char'] += input_energy(A, B, char[key].float().to(args.device))
            total['cap'] += input_energy(A, B, cap[key].float().to(args.device))
        print(json.dumps({'adapter': str(adapter), **total}), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='command', required=True)
    c = sub.add_parser('collect')
    c.add_argument('model', type=Path); c.add_argument('data', type=Path); c.add_argument('out', type=Path)
    c.add_argument('--rows', type=int, default=1024); c.add_argument('--max-length', type=int, default=1024)
    c.add_argument('--batch', type=int, default=8); c.add_argument('--layers'); c.add_argument('--dtype', default='bfloat16')
    c.add_argument('--device', default='cuda')
    for name in ('project', 'measure'):
        s = sub.add_parser(name)
        if name == 'project':
            s.add_argument('adapter', type=Path); s.add_argument('output', type=Path)
            s.add_argument('--removed-energy', type=float, default=.15); s.add_argument('--tau', type=float)
        else:
            s.add_argument('adapters', type=Path, nargs='+')
        s.add_argument('--char', type=Path, nargs='+', required=True); s.add_argument('--cap', type=Path, nargs='+', required=True)
        s.add_argument('--eps', type=float, default=1e-3); s.add_argument('--shrink', type=float, default=256.)
        s.add_argument('--device', default='cuda')
    args = parser.parse_args()
    {'collect': collect, 'project': project, 'measure': measure}[args.command](args)


if __name__ == '__main__':
    main()
