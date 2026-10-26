"""Rank-8 format repair on frozen merged D, then both-mode native evaluation. -- PI/OpenAI (Sol)"""
import argparse
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'runs/run10'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def rows(path):
    with Path(path).open() as stream:
        return [json.loads(line) for line in stream]


def log(text):
    print(text, flush=True)
    with (OUT / 'stages.log').open('a') as stream:
        stream.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' ' + text.splitlines()[0] + '\n')
    with (OUT / 'run.md').open('a') as stream:
        stream.write(text + '\n\n')


def train_config(base, data, output, tiny=False):
    import yaml
    cfg = yaml.safe_load((ROOT / 'configs/train/qwen3/sft.yml').read_text())
    cfg.update(base_model=str(base), output_dir=str(output), dataset_prepared_path=str(output) + '_prepared',
        datasets=[{'path': str(data), 'ds_type': 'json', 'type': 'input_output'}],
        lora_r=8, lora_alpha=16, lora_rank_pattern={}, lora_alpha_pattern={},
        num_epochs=1, learning_rate=1e-4, val_set_size=0, evals_per_epoch=0,
        saves_per_epoch=4, save_total_limit=4, bf16=False, fp16=True,
        plugins=['scripts.train.spectral_plugin.SpectralPlugin',
                 'axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin',
                 'axolotl.integrations.liger.LigerPlugin', 'axolotl.integrations.kernels.KernelsPlugin',
                 'scripts.train.router_dtype_plugin.RouterDtypePlugin', 'scripts.train.heal_plugin.HealPlugin'],
        seed=15)
    if tiny:
        cfg.update(max_steps=3, saves_per_epoch=0, sequence_len=256)
    return cfg


def tiny_model(reference, dtype):
    import torch
    from transformers import AutoConfig, AutoModelForImageTextToText
    source = AutoConfig.from_pretrained(reference, local_files_only=True).to_dict()
    source['text_config'].update(hidden_size=32, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=2,
        head_dim=16, layer_types=['linear_attention', 'full_attention'], full_attention_interval=2,
        num_experts=4, num_experts_per_tok=2, moe_intermediate_size=16, shared_expert_intermediate_size=32,
        linear_num_key_heads=2, linear_num_value_heads=4, linear_key_head_dim=16, linear_value_head_dim=16,
        rope_parameters={'mrope_interleaved': True, 'mrope_section': [1, 1, 0], 'rope_type': 'default', 'rope_theta': 10000000, 'partial_rotary_factor': .25})
    source['vision_config'].update(depth=2, hidden_size=32, intermediate_size=64, num_heads=4, out_hidden_size=32, deepstack_visual_indexes=[])
    config = AutoConfig.for_model(source['model_type'], **{k: v for k, v in source.items() if k != 'model_type'})
    config.text_config.dtype = dtype
    config.dtype = dtype
    return AutoModelForImageTextToText.from_config(config, dtype=dtype)


def baseline_can_continue(deadline, now):
    return deadline - now > 3 * 3600 + 1200


def adapter_incompatible(text):
    if re.search(r'(?i)out of memory|cudaerrormemoryallocation|no space left on device|connection refused|timed out', text):
        return False
    return bool(re.search(r'(?is)(lora|adapter).{0,300}(unsupported|not supported|not implemented|notimplementederror|incompatible)|(unsupported|not supported|not implemented|notimplementederror|incompatible).{0,300}(lora|adapter)', text))


def evaluation_order(adapters, finals):
    return [('r15_D', None)] + [(tag, adapters[tag]) for tag in finals] + [(tag, path) for tag, path in adapters.items() if tag not in finals]


def stop_server(server):
    for sig in [signal.SIGTERM, signal.SIGKILL]:
        try:
            os.killpg(server.pid, sig)
        except ProcessLookupError:
            pass
        try:
            server.wait(timeout=60)
            return
        except subprocess.TimeoutExpired:
            continue
    raise RuntimeError('server did not stop')


class Runner:
    def __init__(self):
        self.plan = json.loads((OUT / 'plan.json').read_text())
        self.deadline = float(os.environ['RUN15_DEADLINE'])
        self.instruct = Path('/workspace/run10_instruct_path').read_text().strip()
        self.parent = ROOT / 'outputs/parent_D'
        self.env = dict(os.environ, IT=self.instruct, MERGE_DTYPE='float16', HF_HOME='/workspace/hf', PYTHONPATH=str(ROOT))
        self.env.pop('KGROUPS', None)

    def command(self, argv, filename, env=None):
        left = self.deadline - time.time()
        assert left > 0, 'runner deadline reached'
        with (OUT / filename).open('w') as stream:
            subprocess.run(list(map(str, argv)), cwd=ROOT, env=env or self.env, check=True,
                           stdout=stream, stderr=subprocess.STDOUT, timeout=left)

    def server(self, path, name, adapters=None):
        argv = ['/opt/vllm/bin/vllm', 'serve', str(path), '--served-model-name', name, '--dtype', 'float16',
                '--max-model-len', '16384', '--gpu-memory-utilization', '.90', '--max-num-seqs', '64',
                '--limit-mm-per-prompt', '{"image":0,"audio":0}', '--enforce-eager', '--port', '8000', '--reasoning-parser', 'qwen3']
        if adapters:
            argv += ['--enable-lora', '--max-lora-rank', '8', '--max-cpu-loras', str(len(adapters)), '--lora-modules']
            argv += [json.dumps({'name': tag, 'path': str(p), 'base_model_name': name}) for tag, p in adapters.items()]
        receipt = OUT / ('server_' + name)
        receipt.with_suffix('.argv.json').write_text(json.dumps(argv, indent=2) + '\n')
        with receipt.with_suffix('.log').open('w') as stream:
            process = subprocess.Popen(argv, env=self.env, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            until = min(self.deadline, time.time() + 1200)
            while time.time() < until:
                assert process.poll() is None, f'vLLM startup failed: {receipt}.log'
                try:
                    with urllib.request.urlopen('http://localhost:8000/v1/models', timeout=3) as response:
                        served = {r['id'] for r in json.load(response)['data']}
                    assert name in served and set(adapters or {}) <= served
                    return process
                except (urllib.error.URLError, TimeoutError, ConnectionError):
                    time.sleep(2)
            raise TimeoutError('vLLM readiness deadline')
        except BaseException:
            stop_server(process)
            raise

    def generate(self, items, prefix, model, mode, temperature=.7, samples=2):
        destination = OUT / (prefix + '_' + model + '_' + mode + '.jsonl')
        assert not destination.exists(), destination
        argv = [sys.executable, ROOT / 'scripts/eval/19_gen_replies.py', items, destination, model,
                'r15_instruct', '--temperature', temperature, '--samples', samples,
                '--workers', '32', '--tokenizer', self.instruct, '--trace', str(destination) + '.wire.jsonl']
        if mode == 'on':
            argv += ['--thinking-budget', '4096']
        self.command(argv, destination.name + '.log')
        actual = rows(destination)
        expected = len(rows(items)) * samples
        assert len(actual) == len({(r['item_id'], r['sample']) for r in actual}) == expected
        return actual

    def evaluate(self, model, full=True):
        for mode in ['on', 'off']:
            if full:
                replies = self.generate(OUT / 'items.jsonl', 'replies', model, mode)
                log(f'PRIMARY COMPLETE {model} {mode}; {len(replies)}rows; all failures retained')
            else:
                self.generate(OUT / 'selected_items.jsonl', 'selected', model, mode)
            self.generate(OUT / 'panel.jsonl', 'panel', model, mode, temperature=0, samples=1)
            if full:
                generated = self.generate(OUT / 'gsm_items.jsonl', 'gsm_replies', model, mode, temperature=0, samples=1)
                originals = rows(OUT / 'gsm8k_long60.jsonl')
                records = []
                for reply, original in zip(generated, originals, strict=True):
                    turn = reply['turns'][0]
                    found = re.findall(r'Answer:\s*\$?\s*(-?[\d,]*\.?\d+)', turn['assistant'])
                    pred = float(found[-1].replace(',', '')) if found else None
                    gold = float(original['answer'].split('####')[-1].strip().replace(',', ''))
                    records.append({'model': model, 'mode': mode, 'gold': gold, 'pred': pred, 'correct': pred == gold,
                                    'correct_completed': pred == gold and turn['finish_reason'] == 'stop', **turn})
                (OUT / f'gsm8k_{model}_{mode}.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in records))
        (OUT / (model + '.done')).write_text(json.dumps({'completed_epoch': time.time(), 'full': full}))
        log(f'EVAL COMPLETE {model} full={full}')

    def merge_parent(self):
        assert not self.parent.exists()
        first, *rest = self.plan['D_cell']
        argv = [sys.executable, ROOT / 'scripts/train/02_merge.py', self.instruct,
                ROOT / ('outputs/up_' + first[0]), self.parent, first[1]]
        for name, dose in rest:
            argv += ['--add', ROOT / ('outputs/up_' + name), dose]
        self.command(argv, 'merge_D.log')
        receipt = json.loads((self.parent / 'merge_report.json').read_text())
        assert receipt['dtype'] == 'float16' and receipt['groups'] == {}
        assert [(r['adapter_sha256'], r['scale']) for r in receipt['adapters']] == [
            (self.plan['adapters'][name]['files']['adapter_model.safetensors']['sha256'], dose) for name, dose in self.plan['D_cell']]
        shutil.copyfile(self.parent / 'merge_report.json', OUT / 'merge_D.json')
        log('D PARENT MERGED: pinned Instruct, ordered fp16 docs+rewr updates, frozen for both heals')

    def tiny_smoke(self):
        import torch
        import yaml
        from transformers import AutoProcessor, AutoTokenizer
        tiny = ROOT / 'outputs/random_heal_smoke_base'
        model = tiny_model(self.instruct, torch.float16)
        model.save_pretrained(tiny)
        tokenizer = AutoTokenizer.from_pretrained(self.instruct)
        tokenizer.save_pretrained(tiny)
        AutoProcessor.from_pretrained(self.instruct).save_pretrained(tiny)
        del model
        messages = [{'role': 'user', 'content': 'What is 2+2?'}]
        on = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=True)
        off = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
        data = OUT / 'tiny_smoke.jsonl'
        examples = [{'id': 'trace', 'segments': [{'text': on.removesuffix('<think>\n'), 'label': False},
                    {'text': '<think>\nTwo and two are four.\n</think>\n\n4.<|im_end|>', 'label': True}]},
                    {'id': 'replay', 'segments': [{'text': off, 'label': False}, {'text': '4.<|im_end|>', 'label': True}]}]
        data.write_text(''.join(json.dumps(r) + '\n' for r in examples))
        cfg = train_config(tiny, data, ROOT / 'outputs/random_heal_smoke_adapter', tiny=True)
        path = OUT / 'cfg_tiny_heal_smoke.yml'
        path.write_text(yaml.safe_dump(cfg, sort_keys=False))
        self.command(['axolotl', 'train', path], 'tiny_heal_train.log', env=dict(self.env, SPECTRAL_FRAC='.01', BEARTYPE='1'))
        self.command([sys.executable, ROOT / 'scripts/train/41_expert_adapter_check.py', ROOT / 'outputs/random_heal_smoke_adapter', '4'], 'tiny_heal_experts.log')
        log('REAL GPU TINY AXOLOTL HEAL SMOKE COMPLETE: same native loader/targets/spectral kernels,3steps')

    def train(self):
        import yaml
        manifest = self.plan['data_manifest']
        later_steps = math.ceil(manifest['variants']['mix']['rows'] / 4)
        for variant in ['trace', 'mix']:
            data = ROOT / f'data/train/run15/{variant}.jsonl'
            assert sha(data) == manifest['variants'][variant]['sha256']
            self.command([sys.executable, ROOT / 'scripts/train/check_loss_mask.py', data], f'loss_mask_{variant}.log')
            output = ROOT / ('outputs/r10_heal15_' + variant)
            cfg = train_config(self.parent, data, output)
            path = OUT / ('cfg_heal_' + variant + '.yml')
            path.write_text(yaml.safe_dump(cfg, sort_keys=False))
            env = dict(self.env, SPECTRAL_FRAC='.01', HEAL_LATER_STEPS=str(later_steps if variant == 'trace' else 0),
                       HEAL_TRAIN_DEADLINE=str(self.deadline - 3 * 3600), HEAL_TIMING_PATH=str(OUT / ('timing_' + variant + '.json')))
            log(f'START TRAIN {variant}: rank8,alpha16,oneepoch,LR1e-4,spectral_frac.01,frozen fp16 D')
            self.command(['axolotl', 'train', path], 'train_r10_heal15_' + variant + '.log', env=env)
            for checkpoint in output.glob('checkpoint-*'):
                for file in checkpoint.iterdir():
                    if file.is_file() and not (file.name.startswith('adapter_') or file.name == 'trainer_state.json'):
                        file.unlink()
            self.command([sys.executable, ROOT / 'scripts/train/41_expert_adapter_check.py', output], 'experts_' + variant + '.log')
            log('TRAIN COMPLETE ' + variant)
        (OUT / 'required_adapters.json').write_text(json.dumps({'required_adapters': ['r10_heal15_trace', 'r10_heal15_mix']}))

    def prepare_inputs(self):
        gsm = rows(OUT / 'gsm8k_long60.jsonl')
        (OUT / 'gsm_items.jsonl').write_text(''.join(json.dumps({'id': 'gsm60_' + str(i), 'system': None,
            'turns': [r['question'] + "\n\nThink step by step, then give the final answer on the last line as 'Answer: <number>'."],
            'max_new_tokens': 1500}) + '\n' for i, r in enumerate(gsm)))
        selected = [r for r in rows(OUT / 'items.jsonl') if r['id'] in self.plan['selected_item_ids']]
        assert len(selected) == len(self.plan['selected_item_ids'])
        (OUT / 'selected_items.jsonl').write_text(''.join(json.dumps(r) + '\n' for r in selected))

    def baseline(self):
        self.prepare_inputs()
        process = self.server(self.instruct, 'r15_instruct')
        try:
            from transformers import AutoTokenizer
            tokenizer = AutoTokenizer.from_pretrained(self.instruct)
            gen = module('heal_baseline_generator', 'scripts/eval/19_gen_replies.py')
            native = []
            for name, prompt, cap, budget, total in [('normal', 'What is 2+2? Give a short answer.', 512, 4096, None),
                ('thinking_cap', 'Calculate 273 times 489 carefully. Explain your calculation.', 256, 8, None),
                ('total_cutoff', 'Work out the prime factorization of 987654321, explaining each step.', 256, 4096, 2)]:
                reply = gen.chat('http://localhost:8000/v1', 'r15_instruct', [{'role': 'user', 'content': prompt}], cap, .7, 0,
                    thinking_budget=budget, tokenizer=tokenizer, trace_path=OUT / 'native_parser_smoke.wire.jsonl', total_max_tokens=total)
                if name == 'normal':
                    assert reply['assistant'] and reply['finish_reason'] == 'stop' and reply['reasoning_end_token_positions']
                elif name == 'thinking_cap':
                    assert budget - 1 <= reply['thinking_tokens'] <= budget + 1 and reply['reasoning_end_token_positions']
                else:
                    assert reply['finish_reason'] == 'length' and reply['empty_final'] and reply['total_completion_tokens'] == total
                native.append({'case': name, **reply})
            (OUT / 'native_parser_smoke.json').write_text(json.dumps(native, indent=2))
            self.evaluate('r15_instruct')
        finally:
            stop_server(process)
        files = list(OUT.glob('*r15_instruct*.jsonl')) + list(OUT.glob('*r15_instruct*.wire.jsonl'))
        (OUT / 'baseline_receipt.json').write_text(json.dumps({'plan_sha256': sha(OUT / 'plan.json'),
            'executor_sha256': sha(__file__), 'verified_sha256': {p.name: sha(p) for p in files}}))

    def main(self):
        log('# Run15 thinking-heal\n\n-- PI/OpenAI (Sol)\n\nResolved plan:\n\n```json\n' + json.dumps(self.plan, indent=2) + '\n```')
        log('SHOULD: no loss on empty think blocks; nonempty traces supervise closing marker, answer and EOS. Parent stays fp16/frozen. TODO validate: neutral traces restore format; replay retains D character rather than undoing it.')
        for name, digest in self.plan['frozen_manifest']['input_sha256'].items():
            if (OUT / name).exists():
                assert sha(OUT / name) == digest
        for name, source in self.plan['adapters'].items():
            for filename, expected in source['files'].items():
                assert sha(ROOT / ('outputs/up_' + name) / filename) == expected['sha256']
        assert Path(self.instruct).name == self.plan['frozen_manifest']['instruct_revision']
        assert sha(Path(self.instruct) / 'config.json') == self.plan['frozen_manifest']['instruct_config_sha256']
        if (OUT / 'early_baseline.launch').exists():
            while subprocess.run(['tmux', 'has-session', '-t', 'run15_early_baseline'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0:
                assert baseline_can_continue(self.deadline, time.time()), 'early baseline exhausted evaluation plus minimum training/merge reserve' 
                time.sleep(5)
            assert (OUT / 'early_baseline.exit').read_text().strip() == '0'
            receipt = json.loads((OUT / 'baseline_receipt.json').read_text())
            assert receipt['plan_sha256'] == sha(OUT / 'plan.json') and receipt['executor_sha256'] == sha(__file__)
            assert all(sha(OUT / name) == digest for name, digest in receipt['verified_sha256'].items())
            log('EARLY BASELINE ACCEPTED: same plan/executor and hashed complete both-mode outputs')
        else:
            self.baseline()
        self.prepare_inputs()
        self.merge_parent()
        self.tiny_smoke()
        self.train()
        adapters = {}
        finals = []
        for name in ['trace', 'mix']:
            directory = ROOT / ('outputs/r10_heal15_' + name)
            final = 'r15_heal_' + name
            adapters[final] = directory
            finals.append(final)
            checkpoints = sorted(directory.glob('checkpoint-*'), key=lambda p: int(p.name.split('-')[-1]))
            for checkpoint in checkpoints:
                if sha(checkpoint / 'adapter_model.safetensors') != sha(directory / 'adapter_model.safetensors'):
                    adapters[final + '_step' + checkpoint.name.split('-')[-1]] = checkpoint
        process = None
        try:
            process = self.server(self.parent, 'r15_D', adapters)
            gen = module('heal_generator', 'scripts/eval/19_gen_replies.py')
            smoke = {tag: gen.chat('http://localhost:8000/v1', tag,
                [{'role': 'user', 'content': 'What is 2+2? Give a short answer.'}], 128, 0, 0,
                trace_path=OUT / 'adapter_smoke.wire.jsonl') for tag in ['r15_D'] + list(adapters)}
            (OUT / 'adapter_smoke.json').write_text(json.dumps(smoke, indent=2))
            log('NATIVE ADAPTER ON MERGED D SMOKE COMPLETE; all expert/dense adapters accepted, raw requests and responses saved')
        except (AssertionError, urllib.error.HTTPError) as error:
            if process is not None:
                stop_server(process)
            detail = error.read().decode(errors='replace') if isinstance(error, urllib.error.HTTPError) else str(error)
            engine_log = (OUT / 'server_r15_D.log').read_text(errors='replace')
            assert adapter_incompatible(detail + '\n' + engine_log[-8000:]), detail
            (OUT / 'native_lora_unsupported.json').write_text(json.dumps({'error': str(error), 'detail': detail, 'deviation': 'Native expert-LoRA rejected at startup or inference; use approved fp32-accumulated heal merge, saved fp16. No checkpoints dropped.'}))
            log('NATIVE LORA UNSUPPORTED; explicit fp32-accumulated fp16 merge evaluation')
            for tag, adapter in evaluation_order(adapters, finals):
                path = self.parent
                if adapter is not None:
                    path = ROOT / 'outputs/healed_model'
                    self.command([sys.executable, ROOT / 'scripts/train/17_merge_heal.py', self.parent, adapter, path], 'merge_' + tag + '.log')
                    shutil.copyfile(path / 'heal_merge_report.json', OUT / ('merge_' + tag + '.json'))
                process = self.server(path, tag)
                try:
                    self.evaluate(tag, full=tag in ['r15_D'] + finals)
                finally:
                    stop_server(process)
                    if adapter is not None:
                        shutil.rmtree(path)
        except BaseException:
            if process is not None:
                stop_server(process)
            raise
        else:
            try:
                self.evaluate('r15_D')
                for tag in finals:
                    self.evaluate(tag)
                for tag in adapters:
                    if tag not in finals:
                        assert self.deadline - time.time() > 900, 'early-checkpoint panels did not fit'
                        self.evaluate(tag, full=False)
            finally:
                stop_server(process)
        log('RUN15 GENERATION COMPLETE; pinned judging and complete selected reads local')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--early-baseline', action='store_true')
    args = parser.parse_args()
    runner = Runner()
    runner.baseline() if args.early_baseline else runner.main()
