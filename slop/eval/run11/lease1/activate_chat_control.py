"""Route the unstarted chat control to its verified replacement. -- PI/OpenAI"""
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

root = Path.cwd()
manifest_path = root / "data/train/run11_matched_chat_control/manifest.json"
manifest = json.loads(manifest_path.read_text())
original = root / "data/train/run11/chatgen.jsonl"
replacement = manifest_path.parent / "chatgen.jsonl"
backup = root / "data/train/run11_original/chatgen.jsonl"
receipt = root / "runs/run10/executed_data_override.json"

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

assert not (root / "runs/run10/train_r10_x11_chatgen.log").exists(), "chatgen already started"
assert not (root / "outputs/prepared_r10_chatgen").exists(), "chatgen already prepared"
assert not (root / "outputs/r10_x11_chatgen").exists(), "chatgen adapter directory already exists"
assert not original.is_symlink() and sha(original) == manifest["original_control_sha256"]
assert sha(replacement) == manifest["sha256"]
assert not backup.exists() and not receipt.exists(), "activation already recorded"
backup.parent.mkdir(parents=True, exist_ok=True)
shutil.copy2(original, backup)
assert sha(backup) == manifest["original_control_sha256"]
link = original.with_suffix(".matched-link")
os.symlink(os.path.relpath(replacement, original.parent), link)
link.replace(original)
assert original.resolve() == replacement.resolve() and sha(original) == manifest["sha256"]
record = {**manifest, "activated_at": datetime.now(timezone.utc).isoformat(),
          "training_path": str(original.relative_to(root)), "resolved_path": str(replacement.relative_to(root)),
          "preserved_original_path": str(backup.relative_to(root)),
          "reason": "Repair the approved chatmix/control supervised-token match before chat training; keep two epochs and hard lease cap."}
receipt.write_text(json.dumps(record, indent=2) + "\n")
print("ACTIVATED matched chat control: " + json.dumps(record), flush=True)
