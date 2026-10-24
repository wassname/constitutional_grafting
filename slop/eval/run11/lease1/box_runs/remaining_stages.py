"""Finish this lease's document tests before budgeted chat jobs. -- PI/OpenAI"""
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

R = Path("runs/run10")
PLAN = R / "run11_execution_plan.json"


def configuration(original):
    document_cells = [cell for cell in original["CELLS"].split() if "x11_chat" not in cell]
    document_cells[-1:-1] = ["x11_mix_const=4", "x11_mix_const=4,x11_replay_ctl=-4"]
    extra_losses = [
        "stoic3=outputs/up_stoic:3", "stoic8=outputs/up_stoic:8",
        "const3=outputs/up_const:3", "other4=outputs/up_other:4",
        "mixs4=outputs/r10_x11_mix_stoic:4", "mixc4=outputs/r10_x11_mix_const:4",
        "anchs4=outputs/r10_x11_mix_stoic:4,outputs/r10_x11_replay_ctl:-4",
        "anchc4=outputs/r10_x11_mix_const:4,outputs/r10_x11_replay_ctl:-4",
    ]
    chats = [
        ("chatr13", 854, "{donor},x11_chatr13=1"),
        ("chatmix", 3079, "{donor},x11_chatmix=1"),
        ("chatgen", 4474, "{donor},x11_chatmix=1,x11_chatgen=-1 {donor},x11_chatmix=0.5,x11_chatgen=-0.5"),
    ]
    return document_cells, original["BASELOSS"].split() + extra_losses, chats


def save(plan):
    temporary = PLAN.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(plan, indent=2) + "\n")
    temporary.replace(PLAN)


def log(message):
    line = f"{datetime.now(timezone.utc).isoformat()} {message}"
    print(line, flush=True)
    with (R / "stages.log").open("a") as stream:
        stream.write(line + "\n")


def phase(original, chats, cells, losses):
    env = os.environ | original | {"CHATS": chats, "CELLS": " ".join(cells), "BASELOSS": " ".join(losses), "CONTROL": ""}
    subprocess.run(["bash", "scripts/train/14_run10_chat_box.sh"], env=env, check=True)


def main():
    assert Path.cwd() == Path("/workspace/cg")
    original = json.loads((R / "launcher_boundary_pause.json").read_text())["original_environment"]
    assert original["TAG"] == "x11_" and original["DONOR"] == "stoic=0.5 const=1 other=1"
    document_cells, losses, chats = configuration(original)
    plan = {"author": "PI/OpenAI", "required_adapters": ["r10_x11_" + name for name in original["DOCS"].split()],
            "document_cells_requested": document_cells, "base_loss_configs_requested": losses,
            "chat_decisions": [], "completed_chat_adapters": [],
            "source_sha256": {name: hashlib.sha256(Path(name).read_bytes()).hexdigest()
                              for name in (str(Path(__file__)), "scripts/train/14_run10_chat_box.sh", "scripts/eval/47_base_heldout_loss.py")}}
    save(plan)
    # Keep adapter weights and trainer history, not optimizer state. -- PI/OpenAI
    for checkpoint in Path("outputs/r10_x11_mix_stoic").glob("checkpoint-*"):
        assert checkpoint.is_dir(), checkpoint
        subprocess.run(["find", str(checkpoint), "-maxdepth", "1", "-type", "f", "!", "-name", "adapter_*",
                        "!", "-name", "trainer_state.json", "-print", "-delete"], check=True)
    with (R / "expert_check_r10_x11_mix_stoic.log").open("w") as stream:
        subprocess.run([sys.executable, "scripts/train/41_expert_adapter_check.py", "outputs/r10_x11_mix_stoic"], stdout=stream, stderr=subprocess.STDOUT, check=True)
    log("done train doc mix_stoic")
    phase(original, "", document_cells, losses)
    log("RUN11 document evaluation command returned 0; coverage is recorded by cell .done files")

    seconds_per_update = 7.2
    for name, updates, cells_string in chats:
        cells = cells_string.split()
        remaining_hours = (float(original["EVAL_DEADLINE_EPOCH"]) - time.time()) / 3600
        required_hours = updates * seconds_per_update * 1.2 / 3600 + 0.3 + 0.37 * len(cells) + 1 / 3
        eligible = name != "chatgen" or "chatmix" in plan["completed_chat_adapters"]
        selected = eligible and remaining_hours >= required_hours
        decision = {"name": name, "selected": selected, "dependency_satisfied": eligible,
                    "estimated_updates": updates, "seconds_per_update": seconds_per_update,
                    "required_hours_with_margin": required_hours, "remaining_eval_hours": remaining_hours,
                    "cells_requested": cells}
        plan["chat_decisions"].append(decision)
        if selected:
            plan["required_adapters"].append("r10_x11_" + name)
        save(plan)
        log("RUN11 chat budget decision " + json.dumps(decision))
        if not selected:
            continue
        if name == "chatgen":
            assert not Path("outputs/prepared_r10_chatgen").exists(), "Inspect unexpected pre-existing chatgen cache before training"
            actual_hash = hashlib.sha256(Path("data/train/run11/chatgen.jsonl").read_bytes()).hexdigest()
            assert actual_hash == "42928ea94a16d7202495fbfe814eba71e1db4bdd5ae5f75c565be97d66c203aa", actual_hash
            Path("outputs/up_x11_chatmix").symlink_to("r10_x11_chatmix", target_is_directory=True)
        phase(original, name, cells, [])
        plan["completed_chat_adapters"].append(name)
        text = (R / f"train_r10_x11_{name}.log").read_text(errors="replace")
        rate = float(re.findall(r"'train_steps_per_second': '([0-9.]+)'", text)[-1])
        seconds_per_update = 1 / rate
        decision["observed_train_steps_per_second"] = rate
        save(plan)
    log("RUN11 remaining stages complete; unselected chats were not trained")


if __name__ == "__main__":
    main()
