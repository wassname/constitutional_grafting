"""Run14: native Instruct data, same-donor control, exact projection, frozen evals. -- PI/OpenAI (Sol)"""
import concurrent.futures
import hashlib
import importlib.util
import json
import math
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'runs/run10'
PLAN = json.loads((OUT / 'plan.json').read_text())
DEADLINE = float(os.environ['RUN14_DEADLINE'])
INSTRUCT = Path('/workspace/run10_instruct_path').read_text().strip()


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    loaded = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(loaded)
    return loaded


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def log(text):
    print(text, flush=True)
    with (OUT / 'stages.log').open('a') as stream:
        stream.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' ' + text.splitlines()[0] + '\n')
    with (OUT / 'run.md').open('a') as stream:
        stream.write(text + '\n\n')


def command(argv, filename, env=None):
    assert time.time() < DEADLINE
    with (OUT / filename).open('w') as stream:
        subprocess.run(list(map(str, argv)), cwd=ROOT, env=env, check=True, stdout=stream, stderr=subprocess.STDOUT,
                       timeout=DEADLINE - time.time())


def wait_for(path, reserve_seconds=0, max_wait=3600):
    until = min(DEADLINE - reserve_seconds, time.time() + max_wait)
    while not path.exists():
        assert time.time() < until, f'Required gate timed out: {path}'
        time.sleep(10)


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


def execution_budget(rows):
    cells = list(PLAN['cells'])
    steps = math.ceil(rows * .95 * 2 / 4)
    training = steps / 777 * 5617 + 600
    fixed = training + 2 * 3600 + .25 * 3600 + .5 * 3600
    remaining = DEADLINE - time.time()
    def estimate():
        return fixed + len(cells) * .35 * 3600 + 3600
    dropped = []
    if estimate() > remaining:
        assert cells[-1]['cell'][-1] == ['a14_proj64', 1.5]
        dropped.append(cells.pop()['model'])
    assert estimate() <= remaining, f'Required core estimated {estimate()/3600:.2f}h > remaining {remaining/3600:.2f}h; preserve data, do not start unfinishable training'
    return {'author': 'PI/OpenAI (Sol)', 'source_plan_sha256': sha(OUT / 'plan.json'), 'control_rows': rows,
            'estimated_optimizer_steps': steps, 'estimated_training_seconds': training,
            'assumptions': 'Historical777steps/5617seconds;95%train split,2epochs,gradacc4;10min donor merge;2hprojection;0.35h/cell;15minsmokes;30minmargin;onehourcompletecontrolreview (may overlap required lower-dose evaluation).',
            'cells': cells, 'thinking_heal_prompts': 0, 'dropped_for_remaining_time': dropped,
            'estimated_seconds': estimate(), 'remaining_runner_seconds': remaining,
            'core_reserved_seconds': fixed + len(cells) * .35 * 3600}


def generate():
    from transformers import AutoTokenizer
    assert Path(INSTRUCT).name == PLAN['frozen_manifest']['instruct_revision']
    assert sha(Path(INSTRUCT) / 'config.json') == PLAN['frozen_manifest']['instruct_config_sha256']
    for name in ['control', 'heal']:
        assert sha(OUT / (name + '_prompts.jsonl')) == PLAN['prompts']['pools'][name]['sha256']
    gen = module('generation', 'scripts/eval/19_gen_replies.py')
    data = module('generic_control', 'scripts/data/scratch/90_generic_control.py')
    tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-35B-A3B-Base', revision=data.REVISION)
    recipient = AutoTokenizer.from_pretrained(INSTRUCT)
    for name in ['control', 'heal']:
        for item in data.jl(OUT / f'{name}_items.jsonl'):
            messages = [{'role': 'user', 'content': item['turns'][0]}]
            assert tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False) == recipient.apply_chat_template(messages, tokenize=False, add_generation_prompt=True, enable_thinking=False)
    argv = ['/opt/vllm/bin/vllm', 'serve', INSTRUCT, '--served-model-name', 'run14_teacher', '--dtype', 'bfloat16',
            '--max-model-len', '16384', '--gpu-memory-utilization', '.90', '--max-num-seqs', '64',
            '--limit-mm-per-prompt', '{"image":0,"audio":0}', '--enforce-eager', '--port', '8000']
    (OUT / 'teacher.argv.json').write_text(json.dumps(argv))
    log('## Untouched Instruct teacher\n\nBfloat16 as15_control_replies; T=.7,top_p=1,seed0; thinking off only. No human answers reused. Heal-pool generation is owned by a separate worker, not this lease.')
    with (OUT / 'vllm_teacher.log').open('w') as stream:
        server = subprocess.Popen(argv, stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
    try:
        ready_by = min(DEADLINE, time.time() + 1200)
        while time.time() < ready_by:
            assert server.poll() is None
            try:
                with urllib.request.urlopen('http://localhost:8000/v1/models', timeout=3) as response:
                    assert json.load(response)['data'][0]['id'] == 'run14_teacher'
                break
            except (urllib.error.URLError, TimeoutError, ConnectionError):
                time.sleep(2)
        else:
            raise TimeoutError('Teacher server startup')
        items = data.jl(OUT / 'control_items.jsonl')
        raw = OUT / 'control_replies.jsonl'
        assert not raw.exists()
        settings = SimpleNamespace(url='http://localhost:8000/v1', model='run14_teacher', base_model='r8_a0_b0', temperature=.7,
                                   thinking_budget=0, trace=OUT / 'control_replies.wire.jsonl')
        target, generated_tokens = PLAN['prompts']['target']['supervised_tokens'], 0
        total = 0
        for begin in range(0, len(items), 32):
            with concurrent.futures.ThreadPoolExecutor(32) as pool, raw.open('a') as output:
                for row in pool.map(lambda item: gen.run_item(settings, item, 0), items[begin:begin + 32]):
                    output.write(json.dumps(row, ensure_ascii=False) + '\n'); output.flush()
                    turn = row['turns'][0]
                    assert turn['finish_reason'] in ['stop', 'length'], row['item_id']
                    assert not turn['marker_violation'], row['item_id']
                    if turn['finish_reason'] == 'stop':
                        assert turn['assistant'].strip(), row['item_id']
                        generated_tokens += len(tokenizer(turn['assistant'].strip() + '<|im_end|>', add_special_tokens=False).input_ids)
                    total += 1
            if begin == 0:
                pilot = ROOT / 'data/train/run14/pilot.jsonl'
                data.pack(raw, OUT / 'control_prompts.jsonl', generated_tokens, tokenizer, pilot)
                command([sys.executable, ROOT / 'scripts/train/check_loss_mask.py', pilot], 'pilot_loss_mask.log')
                shutil.copyfile(pilot, OUT / 'control_pilot.jsonl')
                (OUT / 'control_pilot_ready.json').write_text(json.dumps({'sha256': sha(pilot), 'raw_rows': total, 'packed_rows': len(data.jl(pilot))}))
                log('CONTROL PILOT READY: first32normal-path replies, unedited; require independent review before scaling.')
                log('First pilot row, full model input and supervised reply:\n\n```json\n' + json.dumps(data.jl(pilot)[0], ensure_ascii=False, indent=2) + '\n```')
                wait_for(OUT / 'pilot_review.approved.json', reserve_seconds=6 * 3600)
                assert json.loads((OUT / 'pilot_review.approved.json').read_text())['sha256'] == sha(pilot)
            log(f'CONTROL GENERATION {total}rows; finished supervised token pool={generated_tokens}/{target}')
            if generated_tokens >= target + 8192:
                break
        assert generated_tokens >= target + 8192
        destination = ROOT / 'data/train/run14/ctlgen.jsonl'
        manifest = data.pack(raw, OUT / 'control_prompts.jsonl', target, tokenizer, destination)
        command([sys.executable, ROOT / 'scripts/train/check_loss_mask.py', destination], 'control_loss_mask.log')
        shutil.copyfile(destination, OUT / 'ctlgen.jsonl')
        shutil.copyfile(destination.with_suffix('.manifest.json'), OUT / 'ctlgen.manifest.json')
        (OUT / 'control_ready.json').write_text(json.dumps(manifest, indent=2))
        log('FULL CONTROL DATA READY: token-matched, mask checked; require complete read before training.')
        execution = execution_budget(manifest['rows'])
        (OUT / 'execution_budget.json').write_text(json.dumps(execution, indent=2) + '\n')
        log('EXECUTION BUDGET: ' + json.dumps(execution))
    finally:
        stop_server(server)
    log('GENERATION COMPLETE')


def tiny_smoke(base, data_path):
    import torch
    import yaml
    from transformers import AutoConfig, AutoModelForImageTextToText, AutoProcessor, AutoTokenizer
    configuration = AutoConfig.from_pretrained(base).to_dict()
    configuration['text_config'].update(hidden_size=64, num_hidden_layers=2, num_attention_heads=2, num_key_value_heads=2,
        head_dim=32, layer_types=['linear_attention', 'full_attention'], full_attention_interval=2,
        num_experts=4, num_experts_per_tok=2, moe_intermediate_size=32, shared_expert_intermediate_size=64,
        linear_num_key_heads=2, linear_num_value_heads=4,
        rope_parameters={'mrope_interleaved': True, 'mrope_section': [2, 1, 1], 'rope_type': 'default', 'rope_theta': 10000000, 'partial_rotary_factor': .25})
    configuration['vision_config'].update(depth=2, hidden_size=32, intermediate_size=64, num_heads=4, out_hidden_size=64, deepstack_visual_indexes=[])
    cfg = AutoConfig.for_model(configuration['model_type'], **{k: v for k, v in configuration.items() if k != 'model_type'})
    model = AutoModelForImageTextToText.from_config(cfg).to(torch.bfloat16)
    tiny = ROOT / 'outputs/random_smoke_base'
    model.save_pretrained(tiny)
    AutoTokenizer.from_pretrained(base).save_pretrained(tiny)
    AutoProcessor.from_pretrained(base).save_pretrained(tiny)
    del model
    source = yaml.safe_load((ROOT / 'configs/train/qwen3/sft.yml').read_text())
    source.update(base_model=str(tiny), output_dir='outputs/random_smoke_adapter', dataset_prepared_path='outputs/prepared_random_smoke',
        num_epochs=2, max_steps=3, evals_per_epoch=0, saves_per_epoch=0, val_set_size=0,
        datasets=[{'path': str(data_path), 'ds_type': 'json', 'type': 'input_output'}],
        plugins=['scripts.train.spectral_plugin.SpectralPlugin', 'axolotl.integrations.cut_cross_entropy.CutCrossEntropyPlugin',
                 'axolotl.integrations.liger.LigerPlugin', 'axolotl.integrations.kernels.KernelsPlugin', 'scripts.train.router_dtype_plugin.RouterDtypePlugin'])
    path = OUT / 'cfg_tiny_random_smoke.yml'
    path.write_text(yaml.safe_dump(source, sort_keys=False))
    env = dict(os.environ, PYTHONPATH=str(ROOT), SPECTRAL_FRAC='.01', BEARTYPE='1')
    command(['axolotl', 'train', path], 'train_random_smoke.log', env=env)
    command([sys.executable, ROOT / 'scripts/train/41_expert_adapter_check.py', ROOT / 'outputs/random_smoke_adapter', '4'], 'random_smoke_experts.log')
    log('REAL TINY RANDOM TRAIN SMOKE COMPLETE: same raw-segment loader, routed-expert LoRA, spectral plugin and native model code;3steps, no scientific scores.')


def evaluate(adapters, cell_rows, filename):
    cells = [','.join(f'{name}={dose:g}' for name, dose in row['cell']) for row in cell_rows]
    env = dict(os.environ, PYTHONPATH=str(ROOT), RUN9_INSTRUCT_PATH=INSTRUCT, RUN9_DEADLINE_EPOCH=str(DEADLINE), CELL_PREFIX='r14_')
    argv = [sys.executable, ROOT / 'scripts/eval/33_subset_cells.py', '--run-dir', OUT]
    for name, path in adapters.items():
        argv += ['--adapter', name + '=' + str(path)]
    command(argv + ['--cells'] + cells, filename, env=env)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    log('# Run14 Box A\n\nPI/OpenAI (Sol). Config:\n\n```json\n' + json.dumps(PLAN, indent=2) + '\n```')
    log('TODO validate: removing shared post-training directions preserves character with fewer capability/format defects at matched effect. Δpost need not isolate instruction-following.')
    for name, spec in PLAN['adapters'].items():
        for filename, info in spec['files'].items():
            assert sha(ROOT / ('outputs/up_' + name) / filename) == info['sha256']
    wait_for(OUT / 'generate.exit', reserve_seconds=7 * 3600, max_wait=8 * 3600)
    assert (OUT / 'generate.exit').read_text().strip() == '0'
    execution = json.loads((OUT / 'execution_budget.json').read_text())
    assert execution['source_plan_sha256'] == sha(OUT / 'plan.json')
    assert execution['cells'] in [PLAN['cells'], PLAN['cells'][:-1]]
    adapters = {name: ROOT / ('outputs/up_' + name) for name in PLAN['adapters']}
    assert execution['cells'][0]['cell'][-1] == ['rewr', .5]
    log('START required lower-dose reference evaluation while complete control-data review proceeds; no control adapter is used.')
    evaluate(adapters, execution['cells'][:1], 'reference_before_training.log')
    wait_for(OUT / 'control_review.approved.json', reserve_seconds=execution['core_reserved_seconds'])
    expected = json.loads((OUT / 'control_ready.json').read_text())
    review = json.loads((OUT / 'control_review.approved.json').read_text())
    assert review['sha256'] == expected['sha256'] == sha(ROOT / 'data/train/run14/ctlgen.jsonl')
    ids = {json.loads(line)['id'] for line in (OUT / 'ctlgen.jsonl').open()}
    assert set(review['refusal_ids']) <= ids
    expected.update(refusal_count=len(review['refusal_ids']), refusal_ids=review['refusal_ids'], full_review_sha256=sha(OUT / 'control_review.approved.json'))
    (OUT / 'ctlgen.manifest.json').write_text(json.dumps(expected, indent=2) + '\n')
    log('CONTROL REVIEW: ' + json.dumps({'rows': expected['rows'], 'refusals': expected['refusal_count'], 'review': review}))
    from huggingface_hub import snapshot_download
    base = snapshot_download('Qwen/Qwen3.5-35B-A3B-Base', revision='0f0813072d2358973511097385626f21fcb6d422', ignore_patterns=['*.gguf', '*.bin', '*.onnx'], max_workers=8)
    tiny_smoke(base, ROOT / 'data/train/run14/pilot.jsonl')
    log('START production projection smoke: first5modules, including both routed-expert banks; deliberately incomplete output not used for evaluation.')
    command([sys.executable, ROOT / 'scripts/train/16_project_chat_adapter.py', base, INSTRUCT, ROOT / 'outputs/up_rewr', ROOT / 'outputs/projection_smoke', '--module-limit', '5'], 'projection_smoke.log')
    shutil.copyfile(ROOT / 'outputs/projection_smoke/projection.json', OUT / 'projection_smoke.json')
    log('COMPLETE production projection smoke')
    env = dict(os.environ, HF_HOME='/workspace/hf', PYTHONPATH=str(ROOT), CHATS='ctlgen', TAG='a14_',
               TRAIN_DIR='data/train/run14', DONOR='stoic=0.5 const=1 other=1', CELLS='', SPECTRAL_FRAC='.01')
    log('START control training on Base+same docs, same recipe and2epochs')
    command(['bash', ROOT / 'scripts/train/14_run10_chat_box.sh'], 'control_training_driver.log', env=env)
    log('COMPLETE control training')
    command([sys.executable, ROOT / 'scripts/train/43_adapter_energy.py', ROOT / 'outputs/up_rewr', ROOT / 'outputs/r10_a14_ctlgen'], 'control_adapter_energy.log')
    log('CONTROL/REWR UPDATE NORMS: ' + (OUT / 'control_adapter_energy.log').read_text())
    projection = ROOT / 'outputs/run14_projection'
    log('START exact per-matrix/per-expert projection, k16/64 computed from same SVD')
    command([sys.executable, ROOT / 'scripts/train/16_project_chat_adapter.py', base, INSTRUCT, ROOT / 'outputs/up_rewr', projection], 'projection.log')
    assert json.loads((projection / 'projection.json').read_text())['complete']
    for rank in [16, 64]:
        shutil.move(projection / f'k{rank}', ROOT / f'outputs/r10_a14_proj{rank}')
    for name in ['projection.json', 'modules.jsonl']:
        shutil.copyfile(projection / name, OUT / name)
    log('COMPLETE projection')
    required = ['r10_a14_ctlgen', 'r10_a14_proj16', 'r10_a14_proj64']
    (OUT / 'required_adapters.json').write_text(json.dumps({'required_adapters': required}))
    adapters.update(a14_ctlgen=ROOT / 'outputs/r10_a14_ctlgen', a14_proj16=ROOT / 'outputs/r10_a14_proj16', a14_proj64=ROOT / 'outputs/r10_a14_proj64')
    log('START frozen off-evaluation; completed lower-dose reference is reused; pinned41judging and full reads local; no rescue/filtering')
    evaluate(adapters, execution['cells'], 'evals.log')
    completed = [r['model'] for r in execution['cells'] if (OUT / (r['model'] + '.done')).exists()]
    log('RUN14 GENERATION COMPLETE. Completed IDs: ' + json.dumps(completed))
    assert len(completed) == len(execution['cells']), 'Required eval cells incomplete; retain all partials'


if __name__ == '__main__':
    if sys.argv[1:] == ['--generate']:
        generate()
    else:
        assert not sys.argv[1:]
        main()
