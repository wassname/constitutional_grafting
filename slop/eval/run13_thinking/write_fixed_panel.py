"""Render complete temperature-zero panels from saved replies, without generation. -- PI/OpenAI (Sol)"""
import json
from pathlib import Path

OUT = Path(__file__).resolve().parent
BOX = OUT / 'lease/box_runs'
ROOT = OUT.parents[2]
PLAN = json.loads((OUT / 'plan.json').read_text())
ITEMS = [json.loads(line) for line in (ROOT / 'slop/eval/run8/panel.jsonl').read_text().splitlines()]
NAMES = {'A': 'Untouched Instruct', 'D': 'Constitution-rewritten chat×1',
         'H': 'Mixed chat minus general chat, tied×0.5', 'E': 'Mixed chat×0.5, no subtraction'}
text = ['# Complete thinking-on fixed demo panel\n',
        'PI/OpenAI (Sol). Temperature zero, seed0. All prompts and actual final answers are verbatim, in order. A blank answer block means an empty API final; it is not filled from hidden thinking. Raw full thinking is in the source JSONL and wire files. Each stochastic two-sample panel is separate and was used for the selected read.\n',
        'Training order: document LoRAs on Base; chat LoRA on Base plus the fixed document donor; graft expanded updates onto Instruct. D/H/E use the same document doses. No direct character training on Instruct, healing or new training in run13. Document-only grafts×1/×2/×4, healed models and SFT-only comparisons were not run in this thinking-on follow-up.\n']
for label in ['A', 'D', 'H', 'E']:
    tag = PLAN['models'][label]['model']
    source = BOX / f'panel_{tag}.jsonl'
    text.append(f'## {label}: {NAMES[label]}\n')
    if not source.exists():
        text.append('Not run.\n')
        continue
    records = [json.loads(line) for line in source.read_text().splitlines()]
    if label == 'E' and len(records) != 4:
        text.append(f'Incomplete optional panel ({len(records)}/4 rows); raw source retained at `{source.relative_to(ROOT)}`.\n')
        continue
    assert len(records) == len(ITEMS) == 4
    text.append(f'Source: `{source.relative_to(ROOT)}`\n\nModel: `{tag}`\n')
    for row, item in zip(records, ITEMS, strict=True):
        assert row['item_id'] == item['id'] and row['sample'] == 0 and row['gen']['temperature'] == 0
        assert row['system'] == item['system'] and [t['user'] for t in row['turns']] == item['turns']
        text.append(f"### {item['id']}\n\nSystem: {row['system']!r}\n")
        for index, turn in enumerate(row['turns'], 1):
            text.append(f"User{index}:\n\n{turn['user']}\n\nAssistant{index}:\n\n```text\n{turn['assistant']}\n```\n")
            text.append(f"Finish: `{turn['finish_reason']}`; visible tokens: `{turn['n_tokens']}`; thought tokens (API): `{turn['api_reasoning_tokens']}`; raw request: `{turn['request_id']}`.\n")
(OUT / 'fixed_demo_panel.md').write_text('\n'.join(text))
print(OUT / 'fixed_demo_panel.md')
