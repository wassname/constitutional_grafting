"""Re-judge the same v2 small pairs into data/07_judge/<out>/small. Usage: judge_retest.py <out_version> <first_attempt>
Used for judge test-retest (v2_judgeretest, attempt 2) and the loosened rubric (v2_rubric2, attempt 0). -- PI/Claude (opus-5-5), 2026-10-27"""
import sys
sys.path.insert(0, "scripts/data/v2")
import build
from constitutional_grafting.data.v2.judge import Judge
from constitutional_grafting.data.v2.pipe import Run, read_jsonl

out, attempt = sys.argv[1], int(sys.argv[2])
run = Run(version=out, batch="small", config=build.load_config("v2"))
Judge(first_attempt=attempt)(read_jsonl(run.data / "06_jev/v2/small/rows.jsonl"), run)
