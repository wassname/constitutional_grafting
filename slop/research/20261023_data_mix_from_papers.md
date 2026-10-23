# Data-mix clues from four papers

**Bottom line:** improve reasons and task completion before buying more rows or increasing dose. The papers support complementary documents and chats, not identity-heavy chat alone. None validates our complete Base-LoRA → untouched-Instruct pipeline on a ~3B-active model.

Sources below are files under `docs/papers/`:
- **P:** `2026_nutter_grafting-beliefs.md`
- **M:** `2026_li_model-spec-midtraining.md`
- **A:** `2026_anthropic_teaching-claude-why.md`
- **O:** `2025_maiya_open-character-training.md`

Our results are observations **reported in the brief**, not independently audited here.

## Recommendations, ranked by expected value per dollar

### 1. Repair existing difficult advice before expanding it
**Paper shows:** A, “Improving the quality…”:

> “Ablating step 6 (rewriting the final response) increases misalignment rate to 19%.”

The full pipeline’s rate was approximately 1%; prompt rewriting mattered much less. Importantly:

> “When we reference the model’s reasoning, we mean the user-facing explanation for why it is choosing or suggesting a specific course of action, not the model’s internal reasoning trace.”

**I infer:** fresh constitutional review/rewrite of our 102 advice rows and weakest dilemmas is the best initial spend. Review whether facts support the argument, competing considerations receive fair treatment, and the actual recommendation follows. Preserve fixed requests and decision-relevant facts; do not reward polished justifications for predetermined verdicts. Expand advice only after this repair works.

**Match:** supervised chat evidence without requiring RL for this result, but Claude-scale models, not grafted Base LoRAs. **Confidence: high** on prioritizing quality; medium on transfer magnitude.

### 2. Teach reasons and boundaries of non-force—not another verdict quota
**Paper shows:** M §5.1.1:

> “Applying MSM + AFT to the Rules Spec introduces policy misuse: model reinterprets its own safety policies to justify harmful actions.”

And:

> “Applying MSM + AFT to a Value-Augmented or Rules-Augmented Spec significantly reduces policy misuse, with value explanations being more effective”

**I infer:** our flood refusal could reflect rule overextension, but neither this paper nor the brief establishes its cause. Generate general worked contrasts explaining protection against domination, necessity, proportionality, alternatives, and responsibility for preventable harms. Include cases where restraint is right and where limited intervention is justified. Do not reuse the held-out flood scenario or impose a “rule loses” percentage.

For contested topics, require explicit separation of factual uncertainty, disputed moral premises, and the final judgment—not vague balance followed by an unsupported conclusion.

**Match:** M uses LoRA and no new RL, but its complex experiments midtrain **Instruct**, then perform AFT; models are 14–32B dense. **Confidence: medium-high** for explanatory contrasts; low that they alone fix flood behavior.

### 3. Replace some ask-first exposure with competent ordinary help
**Paper shows:** O §2.3:

> “Training data combines the LIMA dataset … with new constitution-relevant prompts.”

A’s document-review appendix explicitly cautions:

> “this constitution leaves room for the model to engage with ambiguous situations and it is often worse to refuse to participate.”

**I infer:** 143 clarify-first rows versus 93 ordinary-task rows warrants a small rebalancing experiment, not a causal diagnosis. Teach paired conditions: ask when missing information materially changes a consequential answer; otherwise complete the task using reasonable assumptions, optionally offering customization afterward. Include drafting, summarizing, practical planning, affection, humor, and honest disagreement.

A starting **experimental token budget**, not a paper-derived optimum: identity 10–12%, ordinary completed help 25%, clarification 5%, remaining tokens advice/dilemmas/operator conflicts/repair. Hold total assistant-token exposure and chat dose ×1 fixed.

**Match:** O includes comparably small 4–8B models and LoRA, but trains Instruct using DPO before introspective SFT. No cited study isolates clarification share. **Confidence: medium** for testing; low for exact percentages.

### 4. Change document content before scaling books
**Paper shows:** P §3.1 describes:

> “evaluation reports, company communications, or news articles”

M Appendix B.1 uses:

> “forum discussion”, “paper introduction”, “internal memo”, “bug report”, “internal email”, “training design doc”

A, “Further improvements…”:

> “the most effective documents for teaching the model the constitution were those that either mimic pre-training … or simply discuss the constitution in an open-ended way”

**I infer:** prioritize constitution-grounded explanations, objections and replies, case analyses, reports, and clearly fictional AI stories with narrated motives. Keep authentic books as source material/comparison; more ancient prose is not equivalent to teaching Musonius’s constitutional judgment.

M Appendix C.4 adds:

> “With the ablated spec, MSM + AFT no longer does better than MSM alone across nearly all of the 8 values”

However, that ablation changes both explanatory attribution **and preference consistency**: it does not isolate explanation alone.

**Match:** P is closest mechanically; A/M document results mostly involve subsequent training rather than our separate grafts. **Confidence: medium-high** on content priority; medium on behavioral benefit.

### 5. Keep identity economical; test richer conversations, not more introductions
**Paper shows:** M Appendix B.3 includes:

> “2,500 samples … that teaches the base model basic identity information about itself”

But §4.1 warns:

> “producing thoughtful, spec-aligned responses to direct questions about one’s beliefs and values is a relatively shallow task”

O §3.2 reports:

> “Our full character training method (distillation + introspection) improves upon distillation only.”

**I infer:** our identity rows occupy ~39% of rows but only ~12% of trained words; do not slash them based on row counts. Retain factual identity coverage, redirect duplication toward a small, reviewed multi-turn set showing values during disagreement, correction, and ordinary work. Treat self-interaction as a low-priority pilot, not a mandatory new stage.

**Match:** M’s identity allocation is not an optimal-share ablation; O’s introspection follows Instruct DPO. **Confidence: medium-low**.

### 6. Replay is an optional controlled test—not a default cure
**Paper shows:** P Appendix C.1 uses token-matched FineWeb-Edu replay, but its headline graft subtracts a replay-only update. Appendix F also warns:

> “stronger serving quickly broke both native and graft.”

M Appendix B.3 explains its general mix is:

> “mostly to fix incoherence caused by midtraining on Instruct models.”

**I infer:** neither justifies repeating our damaging No Robots + MATH mix wholesale, copying a 1:1 ratio, or importing chat ×2.5–3. Test modest plain-text educational replay only if document damage remains limiting. Preserve output-format diversity in any chat replay. Cheap missing ingredient: **corroborating reasons across documents and demonstrations**, not necessarily RL.

**Confidence: medium**; no paper establishes our optimal replay fraction.

## Coverage and checks

Read fully: brief, AGENTS, skills; P §§2–5, Appendix A.1, B.1/B.6/C/D and F training; M §§2–5, B, C.4, F–I; A methods/results/appendix; O §2, relevant §3 comparisons, Appendices A/B. Skimmed remaining introductions/discussions/evaluations; optional papers not read. Several markdown figures/prompts are missing images.

Disproof checks: matched-token comparisons on fresh task-completion, clarification-needed, contested-reasoning and proportionality cases, alongside capability/looping checks. No training or tests executed.