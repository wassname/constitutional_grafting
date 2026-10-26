# Handover: make the graft work with thinking mode on (goals 2 and 3 of `.pi/goals/ad3e95-v12.md`)

From PI/Claude opus (session const_v2), 2026-10-26, because wassname split the work: this session keeps goal 1 (controls, Box A, expanded eval). The new session owns goals 2 and 3 below. Read AGENTS.md and `constitution/v4.md` sections 1–5 first.

## The problem

The best graft so far, D = `θ_I + Δ_docs + 1·Δsft_rewr|docs` (`r10_stoic0.5_const1_other1_cx_chatr121`), works only with thinking off. With Qwen's default thinking on it writes its answer inside an unclosed think block, so users see a blank reply: 176/214 turns, almost all on character turns (`slop/eval/run13_thinking/results.md`). Cause, very probably: every chat training row had an empty think block. Loss on empty think blocks is now banned (`scripts/train/check_loss_mask.py`, AGENTS rule), but our data already masked them, so masking alone does not fix it. Serving with thinking off is acceptable for the demo (wassname), so this work is lower priority but wanted.

## Goal 3: in-character reasoning data (main thread)

wassname's requirements: good moral reasoning; not rationalising; never mentions the guide/primer/instructions; the constitution only as the character's own commitments, never as an authority; reasons, not rules (frontier writers drift into rules and refusals; see AGENTS); try options quickly and judge by reading.

Done: 20-row pilot, `slop/data/20261026_reasoning_pilot/` (summary.md, samples.md, read.md, guide_audit.md; script `scripts/data/91_reasoning_pilot.py`, `just reasoning-pilot`). Teachers Kimi K3.1 Pro, MiMo v2.6 Flash, GLM 5.3; guides none / Kimi / Opus (Opus guide obtained by one honest retry after a ToS filter refusal; GLM guide failed twice). Journal: "In-character reasoning pilot". Cost $3.74 of $15.

Findings:
- Only Kimi K3.1 Pro writing directly in English is usable. MiMo and GLM invent facts and break the format; Greek/Latin gave no reasoning gain (also true in the 15 Oct pilot).
- Kimi's visible reasoning never cites the constitution, the guide or instructions (0/59 rows). Good.
- **Main open problem, found late by PI/Claude:** with Kimi's native reasoning on, Kimi deliberates in the hidden field (median ~1,000 words), decides, then writes the short visible `<reasoning>` (median 60–77 words) as a summary. In `P0_kimi_owned_10` the hidden reasoning drafts the visible text after deciding. So the visible reasoning is post-hoc. The hidden reasoning is real but telegraphic, assistant-voiced and talks about the task and instructions ("System prompt: …", "Should have reasoning first tags").
- On visible reasoning, the Opus guide gives the most deliberate traces (who is affected, what decides it); answer quality is about the same across guides, and the better/same/worse counts are noise from single samples.
- The Opus guide needs repair before reuse: the vice exclusion is a bare rule (derive it from v4 Honesty/Vice), the "if you may cite" section conflicts with owned values, and it omits Control, Consistency, Means and ends, no-one-worse-off-first, Guards, Roles.

Options awaiting wassname's choice (PI/Claude recommends testing 1 and 3 on the same 20 rows, about $2):
1. Kimi native reasoning off, visible reasoning only, with the reply prefilled with `<reasoning>` to stop meta-planning leaking (it leaked 3,000 tokens when simply switched off). Forward by construction.
2. Train on the hidden reasoning rewritten into the character's voice (real deliberation, but no longer the teacher's own words).
3. Ask Kimi to think as Musonius in its hidden reasoning, and use that.
4. Keep the current method (post-hoc summaries); not recommended.
Then: ~50-row pilot, 2 samples per row, read the reasoning first; check factual citations separately (one Kimi row cites nonexistent CFR subsections); scaling to ~1,800 rows is ~$50–125 API and needs a budget decision.

## Decision locked in (wassname, 2026-10-26)

> "ok great so it works. lock it in, moving on"

Recipe for the reasoning data: Kimi K3.1 Pro, direct English, with the Opus guide (repaired as above: derive the vice exclusion, drop the "if you may cite" section, add the omitted principles). wassname on the post-hoc finding: "of course this is how all reasoning models work". Open question for wassname: "the whole point is non visible reasoning". Which text goes into the student's think block? (a) the teacher's written <reasoning> section (60–150 words, natural, owned values; PI/Claude's assumption), or (b) the teacher's native hidden reasoning (~1,000 words, real deliberation, but telegraphic and talks about the instructions).

## Goal 2: cheap heal (secondary)

Brief `slop/plans/20261026_thinking_heal.md`; research `slop/research/20261026_healing_reasoning_after_merges.md` (nobody has shown a character-preserving post-merge heal; wassname's steer-heal-love found heals can undo the change). A Sol worker (run 2323dbc3) is generating ~600 Instruct thinking traces via OpenRouter `qwen/qwen3.5-35b-a3b` (process heal-traces-600-resume, log `slop/data/20261026_thinking_heal/generation_resume.log`), after a 429 rate-limit stop; 'wait'×8 filter; all rows must be read in full before training (batch files planned). Cost ≈$2 of $5. Training on a GPU (frozen D + rank-8 LoRA, cap $20) has not been scheduled. The worker reports to const_v2 via intercom; redirect it to the new session (its intercom target will be shown by `intercom list-cwd`).

## Resources

OpenRouter key in `.env` (weekly limit $488, ~$480 left). Round budget $100 total, of which goal 3 has $15 and the heal $20. Vast auto-billing is on. Research briefs in `slop/research/20261026_*`. Do not commit full book passages; commit scoped paths only (other sessions share this checkout).
