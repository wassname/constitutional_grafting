# Plan: do values trained as reasoning end up high-curvature?

2026-10-07 · PI/claude-opus · speculative, wassname wants to try it.

Idea source: wassname's agenda footnote `[^deep]`, from Merullo et al. (arXiv 2510.24256).

wassname, 2026-10-07: "ok highly specualtise but I'd like to try ti"

## Hypothesis

Merullo found that deleting low-curvature directions of the capability loss keeps logic (95–106% of baseline) and open-book QA (93–99%). It loses closed-book facts (74–86%), math (66–74%) and memorised text (3–16%). Two other papers find the same split under pruning:

- Jin et al. 2023, `docs/papers/jin2023_downscaling-fact-recall.md`: "Reducing the model size by more than 30% (via either scaling approach) significantly decreases the ability to recall facts seen in pre-training. Yet, a 60–70% reduction largely preserves the various ways the model can process in-context information"
- Jaiswal et al. 2024 (LLM-KICK), `docs/papers/jaiswal2024_llm-kick.md`: "all pruning methods suffer significant performance degradation, sometimes at trivial sparsity ratios (*e.g.*, 25-30\%), and fail for N:M sparsity on knowledge-intensive tasks [...] yet, pruned LLMs even at $\geq 50$\% sparsity are robust in-context retrieval and summarization systems"

These pruning papers use magnitude or OBS-style pruning, not the K-FAC curvature basis. They support the general "stored facts are fragile, procedures are robust" split, not the curvature mechanism itself.

Hypothesis, speculative: values learned as stored verdicts ("X is wrong") behave like closed-book facts and are cheap to remove. Values learned as a reasoning procedure used on many ordinary inputs behave like logic: high curvature in the trained model, so removing them costs capability.

## Goals

1. [ ] goal: measure where trained values sit on Merullo's curvature spectrum
   - verify: value-eval retention after Merullo's K-FAC edit, reported next to logic, closed-book QA and memorisation retention on the same edited model
   - subtle failure mode: the edit breaks the eval answer format, not the values. Discriminator: a neutral control task in the same format keeps >90% retention.
   - subtle failure mode: curvature measured on the original model instead of the trained model. The K-FAC statistics must be collected on the trained model.
2. [ ] goal: compare verdict-style vs reasoning-style value training
   - arm A: SFT on moral questions → verdicts
   - arm B: SFT where the same constitution reasoning appears across ordinary tasks (advice, planning, writing), with the same value data token count
   - verify: B value retention after the edit exceeds A by more than seed-to-seed spread (≥3 seeds)
   - subtle failure mode: B wins only because its value score was higher before the edit. Discriminator: match before-edit value scores within noise, report retention as a ratio.
   - common failure mode: both arms ~equal; then the hypothesis is not supported at this scale. Report it as such, after checking edit and eval code with a fresh-eyes review.
3. [ ] goal: test the agenda's threat directly
   - verify: directional ablation of a value direction (difference of means, refusal-direction style) on both arms; report value-score drop and capability drop (MMLU-style + GSM8K subset)
   - discriminator: entangled values → ablation that removes them also costs capability; shallow values → value drop with ~no capability drop

## Scale

Start small: a model where Merullo's setup is cheap to reproduce (they used OLMo-2-1B/7B). Check whether their code is public before reimplementing. Only move to the Qwen graft if goal 2 shows a gap.

This is independent of the graft pipeline. For the graft itself, the report still says not to target high capability curvature, because the public original undoes it: `slop/research/20261007_curvature_evidence.md`.
