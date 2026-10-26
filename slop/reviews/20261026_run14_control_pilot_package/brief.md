# Run14 generic-control pilot review

PI/OpenAI (Sol). Actual replies will be copied here unchanged after the normal-path pilot completes. This brief is not a data approval.

Purpose: train a negative-control chat adapter, not Musonius's preferred answers. Teacher is the untouched pinned Qwen3.5-35B-A3B Instruct recipient, bfloat16, thinking off, temperature0.7, top_p1, seed0, max2048tokens. No human answers reused. The prompts are generic arithmetic/coding/extraction/ordinary help, not moral dilemmas or model identity/persona instructions.

Read ALL first32raw candidates with their full user prompts and wire requests/responses, then all packed training rows (truncated replies are excluded by protocol). The packed prompt segment must match the actual model input and have the empty think block unlabelled; only the faithful visible reply and its end marker are supervised. Keep refusals and mistakes as generated; do not repair or correctness-filter baseline controls.

Report unexpected persona/moral teaching, role/template/marker errors, hidden reasoning despite off, truncation, empty finals, and refusal IDs with categories (safety refusal versus capability/unanswerability). Ordinary politeness is not a persona defect. Math/factual errors should be recorded separately, not silently removed. Decide whether format/provenance and prompt scope are sound enough to continue the SAME generator; distinguish evidence from unverified concerns.

The main agent reads the complete final control corpus before training. This first-batch independent review only permits scaling generation; it does not approve unseen data or constitute a character result.
