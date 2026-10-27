"""Judge test-retest: re-judge the same v2 small pairs with a fresh Haiku sample (attempt 2) to separate judge noise from teacher-sample noise.
-- PI/Claude (opus-5-5), 2026-10-27"""
import sys
sys.path.insert(0, "scripts/data/v2")
import build
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.pipe import Run, read_jsonl

cfg = build.load_config("v2")
run = Run(version="v2_judgeretest", batch="small", config=cfg)
rows = read_jsonl(run.data / "06_jev/v2/small/rows.jsonl")
Judge(first_attempt=2)(rows, run)
