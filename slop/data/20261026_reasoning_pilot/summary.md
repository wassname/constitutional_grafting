# Reasoning pilot — blocked at primer

The approved pilot could not proceed past step 1. **No teacher generations, independent spot check, training or GPU work were run.** No conclusions about reasoning quality or teacher/arm choice are warranted.

## Evidence and spend

- Read the complete approved plan at commit `a8a1712b`, AGENTS.md, both named research briefs and constitution/v4.md.
- OpenRouter's current `/api/v1/models` listing included all three required models. Their listing metadata and prices are in `model_preflight.json`.
- Froze 20 training rows with `random.Random(0)`, in the plan's exact shape quotas (4/3/3/3/2/2/2/1), before any model outputs. `selection.json` records source hash, source indices, original rows and decoded conversations; the final existing answer was excluded from the teacher prompt. The fixed random 10 review IDs are in `review_selection.json`.
- Asked `anthropic/claude-opus-5.5` for the primer, including the constitution and AGENTS data rules. Served provider: **Claude Platform on AWS**. Request: `prompts/primer.json`; full response, visible API reasoning and refusal: `raw.jsonl`.
- The response was truncated after about 100 words: `finish_reason: content_filter`, `native_finish_reason: refusal`. The refusal states: “This request was blocked as it seems to violate Anthropic's Terms of Service restrictions on reverse engineering or duplicating model outputs.”
- `primer.md` preserves the incomplete text and is **not an approved or usable primer**. The API reasoning was read in full; it sketched the supplied conversion, telescope-club and parcel-correction examples, but did not supply a complete primer.
- Actual reported spend: **$0.099392**, from 21,428 prompt tokens and 684 completion tokens (525 reasoning tokens). Budget cap: $15. No retries or alternate provider/model requests were made. `budget.json` records the settled call.

## Status and recommendation

Coverage: **0/80** candidate generations exist or were read. Failure counts, reviewer agreement, best/worst examples, preferred teacher/arm and empirical scaling cost are **not available**. No samples were accepted for training. The requested three best and three worst examples cannot be supplied without fabricating results.

Stop here rather than bypass the provider refusal or silently substitute a primer writer. A new approved direction is required before changing the primer source/recipe. const_v2 received this report through `contact_supervisor` (target `01a11a85`) and explicitly instructed: commit the blocked report and script, then stop; the supervisor will seek wassname's changed recipe for a fresh run. Do not scale to 50 or ~1,800 rows on this evidence. This is an API/provider block, not evidence that forward constitutional reasoning is impossible.

The script `scripts/data/90_reasoning_pilot.py` contains resumable selection, budget-limited API requests, teacher arms and independent-review stages. Its local self-test passed prompt decoding, final-answer exclusion and multi-turn preservation. Later paid stages remain unexecuted and require a complete, reviewed primer first.

No constitution or existing training files were edited. All task artifacts are restricted to this directory and the single requested script. No full private book passages were added; the saved primer prompt contains the existing constitution's attributed short excerpts.

-- PI/Sol (worker)
