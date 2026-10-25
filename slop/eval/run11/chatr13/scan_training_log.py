"""Scan every training record and preserve all non-progress messages for reading. -- PI/OpenAI (Sol)"""
import ast
import hashlib
import json
import math
import re
from decimal import Decimal
from pathlib import Path

r = Path('slop/eval/run11/lease1')
p = r / 'box_runs/train_r10_x11_chatr13.log'
raw = p.read_bytes()
text = re.sub(r'\x1b\[[0-?]*[ -/]*[@-~]', '', raw.decode()).replace('\r', '\n')
clean = text.splitlines()
(r / 'box_runs/train_r10_x11_chatr13.clean.log').write_text('\n'.join(clean) + '\n')
metrics, messages = [], []
for i, line in enumerate(clean, 1):
    s = re.sub(r'^\s*\d+%\|.*?\|\s*\d+/\d+\s*\[[^\]]*\]\s*', '', line).strip()
    if not s:
        continue
    record = None
    if s.startswith('{') and s.endswith('}'):
        value = ast.literal_eval(s)
        if isinstance(value, dict) and {'loss', 'eval_loss', 'train_loss'} & value.keys():
            record = value
    if record is not None:
        numeric = {k: float(v) for k, v in record.items()}
        assert all(math.isfinite(v) for v in numeric.values()), (i, record)
        metrics.append({'clean_line': i, 'raw': record, 'numeric': numeric})
    elif not re.fullmatch(r'\d+/\d+ \[[^\]]*\]', s):
        messages.append(f'{i}: {line}')
(r / 'chatr13_metrics.jsonl').write_text(''.join(json.dumps(x) + '\n' for x in metrics))
(r / 'chatr13_setup_and_messages.log').write_text('\n'.join(messages) + '\n')
train = [x for x in metrics if 'loss' in x['numeric']]
evaluation = [x for x in metrics if 'eval_loss' in x['numeric']]
assert len(train) == 854 and len(evaluation) == 3
half_ulp = lambda s: 0.0 if float(s) == 0 else float(Decimal('0.5') * Decimal(10) ** Decimal(str(s)).as_tuple().exponent)
sum_residuals, product_residuals = [], []
for row in train + evaluation:
    phase = 'eval' if 'eval_loss' in row['numeric'] else 'train'
    v, raw_row = row['numeric'], row['raw']
    ce, penalty, total, sigma, lam = [v[f'{phase}_{name}'] for name in ('text_loss', 'spectral_penalty', 'total_loss', 'spectral_sigma_max_mean', 'spectral_lam')]
    residual = abs(total-ce-penalty)
    tolerance = sum(half_ulp(raw_row[f'{phase}_{name}']) for name in ('text_loss', 'spectral_penalty', 'total_loss'))
    assert residual <= tolerance + 1e-7, (row['clean_line'], residual, tolerance)
    sum_residuals.append(residual)
    residual = abs(penalty-lam*sigma)
    dl, ds = [half_ulp(raw_row[f'{phase}_{name}']) for name in ('spectral_lam','spectral_sigma_max_mean')]
    tolerance = half_ulp(raw_row[f'{phase}_spectral_penalty']) + abs(lam)*ds + abs(sigma)*dl + ds*dl
    assert residual <= tolerance + 1e-7, (row['clean_line'], residual, tolerance)
    product_residuals.append(residual)
indices = sorted({0,1,2,len(train)-1,*range(0,len(train),30),*range(80,91)})
lines=['# Chatr13 training trajectory','PI/OpenAI (Sol). All metrics scanned; displayed losses are rounded by Trainer. All nonmetric messages preserved separately.','| Update | Epoch | Text loss | Spectral penalty | Total | Mean sigma | Lambda | LR | Grad norm |','|:--|--:|--:|--:|--:|--:|--:|--:|--:|']
for i in indices:
    v=train[i]['numeric'];lines.append(f"| {i+1} | {v['epoch']:.4f} | {v['train_text_loss']:.4f} | {v['train_spectral_penalty']:.6f} | {v['train_total_loss']:.4f} | {v['train_spectral_sigma_max_mean']:.5f} | {v['train_spectral_lam']:.5f} | {v['learning_rate']:.3g} | {v['grad_norm']:.3f} |")
lines += ['## Every evaluation record',*[json.dumps(x) for x in evaluation]]
(r/'chatr13_metric_trajectory.md').write_text('\n\n'.join(lines)+'\n')
report={'author':'PI/OpenAI (Sol)','raw_sha256':hashlib.sha256(raw).hexdigest(),'raw_bytes':len(raw),'raw_newlines':raw.count(b'\n'),'clean_lines':len(clean),'metric_rows':len(metrics),'optimizer_rows':len(train),'evaluation_rows':len(evaluation),'nonmetric_lines':len(messages),'all_metric_values_finite':True,'all_component_sums_match_with_display_rounding':True,'max_component_sum_residual':max(sum_residuals),'all_penalty_lambda_sigma_products_match_with_display_rounding':True,'max_product_residual':max(product_residuals),'eval_records':evaluation,'first_optimizer':train[0],'last_optimizer':train[-1],'final_record':metrics[-1],'max_grad_norm':max(x['numeric']['grad_norm'] for x in train),'max_active_GiB':max(x['numeric']['memory/max_active (GiB)'] for x in train),'lambda_calibration_lines':[s for s in messages if 'spectral_lam fixed' in s],'scope':'Complete log scan; nonmetric/trajectory reads remain required. Components example-weighted by plugin, not pure token-weighted validation NLL.'}
(r/'chatr13_log_scan.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2),flush=True)
