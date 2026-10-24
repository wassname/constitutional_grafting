## Verdict: capability-only scoring PASS; one reporting defect remains

### 1. Ordinary-scored models can still disappear from the report

**Evidence:** `scripts/eval/43_paired_ablation.py:47` loads only `gsm8k_r10_*.jsonl`; `:58–59` then applies:

> `if m not in maths: continue`

**Affected inputs:** Any model with valid ordinary checks but no matching maths file—including the supplied **`r8_a0_b0` baseline**, whose filename cannot match that glob. This silently removes its row despite the new union of character/ordinary models.

**Minimal fix:** Retain ordinary-scored rows and display missing maths as “not run”; accept the baseline’s actual maths filename when available. Add a reporting test with `r8_a0_b0` and an ordinary-scored model lacking maths. The existing test supplies `r10_*` maths files for both models, so cannot detect this.

**Cheapest discriminator:** Inspect a report generated from the seven-model parity set: does it include the baseline and retain a model when its maths artifact is absent? Source inspection predicts omission.

### What passed

- `41_tc_judge.py:37–66` validates the ordinary model/item/two-sample matrix, rejects duplicates, checks user/system prompts, invokes the pinned check functions, and exits **before credential loading and judge subprocess execution** (`:69` onward).
- All twelve supplied sample replies and verdicts were read. The Stoic ×4 omelet answer correctly illustrates the distinction: mathematical credit **1.0**, alongside language-switch flag **1.0**. Ordinary score alone must not imply coherence.
- `ordinary_existing/parity.json` records **154 comparisons with no differences**. This supports check-result equivalence on those records; I did not rerun it.
- Numerical credit is preserved in the report. No accidental constitutional scoring found in capability-only mode.

**Limits:** “Ordinary” means eight maths, two JSON-format and one minimum-length case, each sampled twice—not broad usefulness. The seeded review sample covers maths only. Historical diffs were not supplied as artifacts, so complete default-path equivalence cannot be independently attested from the current files alone.