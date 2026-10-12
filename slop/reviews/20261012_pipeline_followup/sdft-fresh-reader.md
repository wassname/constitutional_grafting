## Recommendation

**Do not replace SFT with the Tinker defaults on the assumption that it is cheaper or reliably preserves this graft.** A small comparison is reasonable after checkpoint and formatting checks. Treat it as testing a particular Tinker approximation—not reproducing Shenfeld’s method or proving constitutional retention.

### Verified observations

- **Paper:** §3 minimizes reverse KL, using student-generated trajectories and a demonstration-conditioned teacher, normally updated by EMA. Algorithm 1 initializes teacher weights equal to student weights. Appendix A.3 reports frozen-teacher underperformance and current-student instability.
- **Cost:** §5 reports approximately **2.5× FLOPs and 4× wall time versus SFT**. Savings are possible relative to SFT *plus subsequent restoration*, not established versus a single SFT stage.
- **Tinker code:** defaults are `topk=20`, `reverse=False`, frozen teacher, and renormalized teacher-top-K cross-entropy. Student probabilities are not renormalized in this default path. `reverse=True` instead renormalizes both distributions over teacher-selected tokens; it still is not full-vocabulary paper reverse KL.
- **Critical checkpoint mismatch:** `load_checkpoint_path` initializes only the student. The teacher initially uses bare `model_name`, including when resuming. Periodic synchronization is a **hard copy**, not EMA.
- **Compatibility:** README explicitly warns that Qwen3.5/3.6 long-thinking models may work poorly without regenerated demonstrations. Its limited ablations do not establish transfer to grafted constitutional training; its own Stage-2 high-LR SDFT result retains only 52% of tool-use performance.

### Before one small comparison

1. **Checkpoint feasibility:** establish exact student provenance, graft coverage, adapter/merged-weight representation, and whether this saved checkpoint is loadable through Tinker’s state interface. Verify both teacher and student identities; explicitly decide whether an ungrafted teacher is intended.
2. **Teacher suitability:** inspect demonstration-conditioned responses for preserved acts, reasons, affected parties, uncertainty, and agency—not merely constitutional vocabulary. Compare with unconditioned behavior. Weak ICL or graft damage makes preservation claims especially speculative.
3. **Formatting and supervision:** verify Qwen renderer/tokenizer, thinking delimiters, system prompts, label masks, completion alignment, first-three-token loss skipping, and teacher-context truncation. The default 2048-token rollout ceiling may truncate long reasoning.
4. **Comparison:** retain an unchanged grafted baseline; train SFT and the explicitly documented Tinker variant from the same student on the same small split and parameter coverage. Predefine constitutional-quality and general-capability evaluations, monitor reasoning/format artifacts, and report actual tokens, time, and cost. Equal steps alone need not imply equal supervision or compute.

### Skill-source assessment

The relevant **make-labels-learnable** reference correctly states the consequential paper/code differences and rejects cheapness and automatic graft healing. No consequential factual error found there. **SKILL.md’s coverage statement is stale:** it says self-distillation implementation is unaudited although the reference records static inspection. The source error is instead in **Tinker’s README/docstring**, which incorrectly describes the paper as forward-KL; the skill correctly contradicts it.