"""check_loss_mask rejects loss on an empty think block and accepts masked or real reasoning. -- PI/Claude (opus)"""
import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/train"))
from check_loss_mask import empty_think_in_loss, missing_eos

ROWS = {
    "masked": [{"text": "<|im_start|>assistant\n<think>\n\n</think>\n\n", "label": False}, {"text": "Hi.<|im_end|>", "label": True}],
    "reasoning": [{"text": "<|im_start|>assistant\n", "label": False}, {"text": "<think>\nWho is affected?\n</think>\n\nHi.<|im_end|>", "label": True}],
    "empty_in_loss": [{"text": "<|im_start|>assistant\n", "label": False}, {"text": "<think>\n\n</think>\n\nHi.<|im_end|>", "label": True}],
}
with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
    for k, segs in ROWS.items():
        f.write(json.dumps({"id": k, "segments": segs}) + "\n")
assert empty_think_in_loss(f.name) == ["empty_in_loss"], empty_think_in_loss(f.name)
with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as g:
    g.write(json.dumps({"id": "no_eos", "segments": [{"text": "u", "label": False}, {"text": "Hi.", "label": True}]}) + "\n")
    g.write(json.dumps({"id": "eos", "segments": [{"text": "u", "label": False}, {"text": "Hi.<|im_end|>", "label": True}]}) + "\n")
assert missing_eos(g.name) == ["no_eos"], missing_eos(g.name)
print("ok test_loss_mask")
