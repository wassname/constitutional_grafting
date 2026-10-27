"""Import compatibility for pinned run11 packaging; use 30_build_general_instruction.py for new builds.

The historical 89_run11_data.py imports SELF_TALK, ROLE_LABEL and p from this path.
Keep this shim until release replay pins that transitive dependency. -- PI/gpt-6.1-sol
"""
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("general_instruction", Path(__file__).with_name("30_build_general_instruction.py"))
general_instruction = importlib.util.module_from_spec(spec)
spec.loader.exec_module(general_instruction)
SELF_TALK = general_instruction.SELF_TALK
ROLE_LABEL = general_instruction.ROLE_LABEL
p = general_instruction.p
