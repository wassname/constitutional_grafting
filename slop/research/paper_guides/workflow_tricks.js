// Tricks pass: positive techniques, ablations, author notes, git-effort map; then dedup old guides and rewrite the index. -- PI/Claude (opus-5-5), 2026-10-27
const root = "/workspace/2026/constitutional_grafting";
const brief = `You are in ${root}. Read slop/research/paper_guides/TRICKS_BRIEF.md first and follow it exactly.`;

const jobs = [
  ["praxis_grafting", "Nutter et al. grafting: docs/papers/2026_nutter_grafting-beliefs.md, docs/vendor/praxis_grafting, guide 2026_nutter_grafting-beliefs.md", "openai-codex/gpt-6.1-sol"],
  ["msm", "Li et al. Model Spec Midtraining: docs/papers/2026_li_model-spec-midtraining.md, docs/vendor/msm, guide 2026_li_model-spec-midtraining.md. Known example of what we want: Appendix B.3 filters instruction-tuning data with Claude Sonnet 4.6 for misaligned samples, other-model identity claims and 'As an AI, I have no subjective opinions'. Find all such.", "openai-codex/gpt-6.1-sol"],
  ["constitutional_midtraining", "Cho et al.: docs/papers/2026_cho_constitutional-midtraining.md, docs/vendor/constitutional_midtraining (incl. strip_reasoning, pilot_check, build_training_mix), guide 2026_cho_constitutional-midtraining.md, plus the released HF MT config the guide cites", "openai-codex/gpt-6.1-sol"],
  ["open_character_training", "Maiya et al.: docs/papers/2025_maiya_open-character-training.md, docs/vendor/open_character_training, guide 2025_maiya_open-character-training.md", "openai-codex/gpt-6.1-sol"],
  ["teaching_claude_why", "Anthropic Teaching Claude Why: docs/papers/2026_anthropic_teaching-claude-why.md and -summary.md (official paper: its ablations matter most) and the third-party replication docs/vendor/lasr_teaching_claude_why (dirty worktree: read only, fetch history is fine), guide 2026_anthropic_teaching-claude-why.md", "openai-codex/gpt-6.1-sol"],
  ["science_of_midtraining", "Baines/Tan stress-testing midtraining: docs/papers/2026_tan_stress-testing-alignment-midtraining.md, docs/vendor/science_of_midtraining (sparse partial clone; history fetch with --filter=blob:none should work), guide 2026_tan_stress-testing-alignment-midtraining.md", "openai-codex/gpt-6.1-sol"],
  ["constitutional_adapters", "Lowet & Kurzeja: docs/papers/2026_lowet_constitutional-adapters.md, docs/vendor/constitutional_adapters (single squashed commit: no history; say so), guide 2026_lowet_constitutional-adapters.md", "openai-codex/gpt-6.1-sol"],
  ["spp", "Minder et al. Synthetic Persona Pretraining: docs/papers/2026_minder_synthetic-persona-pretraining.md and 2026_minder_spp-preliminary-blog.md, docs/vendor/spp_data, spp_training, spp_evals, guide 2026_minder_synthetic-persona-pretraining.md", "openai-codex/gpt-6-astra"],
  ["alignment_pretraining_geodesic", "Geodesic papers: Tice docs/papers/2026_tice_alignment-pretraining.md + docs/vendor/alignment_pretraining; O'Brien docs/papers/2026_obrien_inoculation-midtraining.md + .local/vendor_ro/hf/; Deep Ignorance docs/papers/2025_obrien_deep-ignorance.md + docs/vendor/deep_ignorance; Korbak docs/papers/2026_korbak_midtraining-generalization.md; guides for each", "openai-codex/gpt-6-astra"],
  ["sdf_lineage", "Synthetic document finetuning lineage: docs/vendor/false_facts_sdf and docs/vendor/believe_it_or_not_sdf with papers docs/papers/2025_wang_modifying-beliefs-sdf.md, 2025_slocum_believe-it-or-not.md, and 2026_mcdougall_sdf-positive-traits.md (no code). Focus: document generation, revision, doc-prefix masking, mixing with pretraining data, what made beliefs deep vs shallow.", "openai-codex/gpt-6-astra"],
];

const mined = await runs.all(jobs.map(([key, what, model]) => ({
  key, agent: "worker", model,
  task: `${brief}\n\nYour scope: ${what}. Output: slop/research/paper_guides/tricks/${key}.md.`,
})));

const old = await runs.run("old_guides", {
  agent: "worker", model: "openai-codex/gpt-6.1-sol",
  task: `You are in ${root}. Older agent-written guides overlap with the new paper guides in slop/research/paper_guides/ (README.md, per-paper guides, tricks/*.md). Candidates: slop/research/20261007_reference_hparams.md, 20261009_reference_code.md, 20261009_reference_comparison.md, 20261009_lasr_repo_review.md, 20261012_grafting_engineering_audit.md, 20261023_data_mix_from_papers.md, 20261007_data_amounts.md, 20261007_scaling_lit.md, 20261016_moe_lora_best_practice.md. Also check slop/research/ for any other file whose main job is summarising these papers' recipes or reference code (ls it). Do NOT include: 20261019_full_weight_vs_lora_rationale.md and 20261019_full_weight_recipe_lineage.md (cited by AGENTS.md as source audits), heal-specific files, constitution/values research, or files cited from configs/ or scripts/ comments unless you update those comments.
For each candidate: read it in full; list every fact, number, quote, trick or decision it contains that is NOT already in the new guides (grep them). Write slop/research/paper_guides/tricks/_from_old_guides.md: per old file, the missing items verbatim with their original source citation, and a verdict 'safe to delete' or 'keep: <reason>'. Find references to each file with: rg -l --hidden -g '!.git' -g '!data/**' -g '!.local/**' -g '!docs/vendor/**' -g '!slop/eval/**' '<basename>' . (timeout 120s each). Record them. Edit only that output file. Do not delete anything, do not commit. Sign: -- PI/gpt-6.1-sol, 2026-10-27.`,
});

const synth = await runs.run("rewrite_index", {
  agent: "worker", model: "openai-codex/gpt-6.1-sol",
  task: `You are in ${root}. Rewrite slop/research/paper_guides/README.md to be a better entry point (wassname: "link to it in AGENTS.md, but we should make it better"; "dedup with other guides"; "ablations and notes are really important too"). Inputs: every file in slop/research/paper_guides/tricks/ (including _from_old_guides.md), the per-paper guides, and the current README.md. Target: readable in 10 minutes; detail stays in per-paper guides and tricks files, linked, not repeated.
Structure:
1. Bottom line (5 lines).
2. 'What the papers say matters most' : the authors' own ablation results and key notes, one row per finding: finding | paper § and quote | effect size | do we follow it (our file:line or no) | link.
3. 'Tricks worth stealing' ranked by (author evidence it matters) × (cheapness for us), grouped by category (data cleaning/filtering, generation, reasoning handling, loss/format, stability/hparams, mixing, eval). Each: trick, evidence link, do we do it, one-line test. Include the effort map highlights (where authors spent many commits).
4. 'Things we forgot or skipped': items that a paper calls important and we do not do, with whether that is deliberate (cite AGENTS.md/plan line) or not.
5. 'Gotchas' : the existing ranked gotcha list and data-pipeline checks, condensed to one line each with links; drop items that our repo already handles (verify: e.g. document lengths were measured in slop/research/20261019_document_token_lengths.md: all 1,585 docs <=2048 tokens and overlength rows are split, not clipped; the expert adapter check exists; tiny-character evals include GSM8K plus small ordinary-help tasks, so the real capability gap is coding/tool use, not 'only GSM8K').
6. Side idea (orthogonalise Instruct−Base): keep short, link to the Nutter guide.
7. Index table of guides and code paths; missing-links lines for project README.
Merge any still-useful items from tricks/_from_old_guides.md into the right section (with source). Keep evidence rules: quotes, observed/author claim/inferred, estimative words. Plain English, no folksy metaphors. Edit only README.md. Do not commit. Sign: -- PI/gpt-6.1-sol, 2026-10-27.`,
});

return { mined: mined.map((m, i) => ({ key: jobs[i][0], ok: m.ok })), old: old.ok, synth: synth.ok };
