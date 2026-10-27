// Paper engineering guides: vendor/fetch, then one guide per paper, then synthesis. -- PI/Claude (opus-5-5), 2026-10-27
const brief = "Read slop/research/paper_guides/BRIEF.md first and follow it exactly.";

const vendor = await runs.run("vendor", {
  agent: "worker",
  model: "openai-codex/gpt-6.1-sol",
  task: `You are in /workspace/2026/constitutional_grafting. Two jobs; you are the only agent allowed to run git here right now.

A) Geodesic Research writing (geodesicresearch.ai, LessWrong authors Kyle O'Brien, Cameron Tice, Puria Radmard, Edward James Young). Already in docs/papers: 2026_tice_alignment-pretraining.md, 2025_obrien_deep-ignorance.md, 2026_obrien_inoculation-midtraining.md, 2026_young_pre-rl-checkpoints.md, and maybe 2026_korbak_midtraining-generalization.md (check its authors/affiliation). Candidates to add: "Research Note: Filtering Subversion-Relevant Information From Pretraining Data Is Feasible" (Oct 2026), "Reducing the Resource Gap Between Lab and External Safety Researchers" (Sep 2026), "Why study proto-training gaming as an adversarial alignment failure mode?" (Jul 2026), plus any other Geodesic post/paper about midtraining, alignment pretraining, persona/character, or post-hoc checkpoint interventions. Relevance test: does it bear on teaching values via documents on a base model, midtraining→post-training persistence, or cheap compute for external researchers? Add relevant ones as rows to docs/papers/manifest.tsv (tab-separated: filename, url, title, authors, year; filename like 2026_<firstauthor>_<slug>.md; prefer arxiv.org/html/... URLs, else the LessWrong post URL), then run 'bash scripts/data/01_fetch_papers.sh' (timeout 600). Check each fetched file has real body text (not a nav page). For skipped items, list title + one-line reason.

B) Code for the major papers into docs/vendor as git submodules. Existing: see .gitmodules (msm, constitutional_midtraining, praxis_grafting, open_character_training, lasr_teaching_claude_why, false_facts_sdf, believe_it_or_not_sdf, virtue_constitution). Find official code (grep the paper markdown for github links; then search GitHub/HF/web) for: Tice alignment pretraining, O'Brien inoculation midtraining, Korbak midtraining generalization, Tan stress-testing alignment midtraining, Minder synthetic persona pretraining, McDougall SDF positive traits, Lowet constitutional adapters, Anthropic Teaching Claude Why (official, if any), Deep Ignorance. Add only real code repos (not dataset-only, not empty): 'git submodule add --depth 1 <url> docs/vendor/<short_name>'. If .git/config is read-only and submodule add fails, record the exact error and instead clone with --depth 1 into docs/vendor/<name> and add it to .gitmodules manually only if that works; never vendor huge repos (>200MB): note them instead. Record HF dataset/model collections too, as links only.

Write slop/research/paper_guides/VENDOR.md: a table (paper | code repo | vendored path + commit | HF artifacts | notes) and the Geodesic add/skip list. Commit with message 'papers/vendor: Geodesic posts + paper code submodules' and trailer 'Co-Authored-By: PI/gpt-6.1-sol <288921227+claudypoo@users.noreply.github.com>'. Stage only the files you created/changed (git add explicit paths). Report what you did, with paths.`,
});

const core = ["2026_nutter_grafting-beliefs", "2026_li_model-spec-midtraining", "2026_cho_constitutional-midtraining",
  "2026_anthropic_teaching-claude-why", "2025_maiya_open-character-training"];
const secondary = ["2026_tan_stress-testing-alignment-midtraining", "2026_korbak_midtraining-generalization",
  "2026_tice_alignment-pretraining", "2026_minder_synthetic-persona-pretraining", "2026_mcdougall_sdf-positive-traits",
  "2026_lowet_constitutional-adapters", "2026_obrien_inoculation-midtraining", "2026_young_pre-rl-checkpoints"];

const extra = {
  "2026_nutter_grafting-beliefs": " This is THE method paper. Read it in full including appendices, and read docs/vendor/praxis_grafting code in full (how Δ is computed, merged, scaled, which modules; controls subtracted; MoE experts; how they choose graft coefficient). Also evaluate wassname's new side idea in a section 'Side idea: orthogonalise Instruct−Base': ablate or orthogonalise the direction τ = θ_Instruct − θ_Base out of the graft Δ (per weight matrix, e.g. project Δ off the top-k singular subspace of τ) to better preserve maths and instruction following. Say whether the paper or code does anything like this, the math, the obvious failure modes (e.g. removing exactly the components that carry character, or that τ is not low-rank), and a cheap test using our existing adapters.",
  "2026_li_model-spec-midtraining": " Read docs/vendor/msm code too. Pin down exactly which checkpoint MSM starts from in §4 (Qwen2.5-32B-Instruct and Qwen3-32B are post-trained: do they midtrain on the Instruct model? check code/configs), document mix, replay, and how AFT data is built.",
  "2026_cho_constitutional-midtraining": " Read docs/vendor/constitutional_midtraining code. Key: what 'content presence drives alignment gains' means operationally, their document generator, token counts, and how much post-training erased.",
  "2026_anthropic_teaching-claude-why": " Also read docs/papers/2026_anthropic_teaching-claude-why-summary.md and the replication code docs/vendor/lasr_teaching_claude_why. Note every pipeline step and whether we do it.",
  "2025_maiya_open-character-training": " Read docs/vendor/open_character_training code: constitution format, introspection/self-reflection data, DPO setup, distillation.",
};

const tasks = core.map((p) => ({ key: p, agent: "worker", model: "openai-codex/gpt-6.1-sol",
  task: `${brief} Write the guide for docs/papers/${p}.md to slop/research/paper_guides/${p}.md. Check docs/vendor and slop/research/paper_guides/VENDOR.md for its code.${extra[p] ?? ""}` }))
  .concat(secondary.map((p) => ({ key: p, agent: "worker", model: "openai-codex/gpt-6-astra",
  task: `${brief} Write the guide for docs/papers/${p}.md to slop/research/paper_guides/${p}.md. Check docs/vendor and slop/research/paper_guides/VENDOR.md for its code. This is a secondary paper: keep the guide to about 2 pages, focus on gotchas and anything that changes our recipe.` })));

const guides = await runs.all(tasks);

const synth = await runs.run("synthesis", {
  agent: "worker",
  model: "openai-codex/gpt-6.1-sol",
  task: `In /workspace/2026/constitutional_grafting, read every guide in slop/research/paper_guides/*.md (and VENDOR.md, BRIEF.md), then AGENTS.md, README.md, docs/plans/20261021_character_graft_recipe.md and our training configs/scripts. Write slop/research/paper_guides/README.md:
1. Index table: paper | one-line engineering takeaway | guide path | code path.
2. 'Gotchas we missed or are exposed to': ranked by (probability it affects our results) × (impact). Each item: evidence (quote + guide path), our affected file:line, a cheap check. Verify each claim against the paper text yourself before including it; drop claims you cannot verify and list them under 'unverified'.
3. 'Recipe decisions that disagree with the literature': where our locked choices (AGENTS.md) differ from all core papers, and whether that is deliberate (cite where) or unexamined.
4. 'Side idea: orthogonalise Instruct−Base from the graft': consolidate from the Nutter guide; give math, pseudocode, failure modes, cheapest test.
5. 'Missing links': which papers are not cited in README.md / AGENTS.md but should be, with the exact line to add (do not edit those files).
Plain English, quotes for evidence, estimative probability words. Do not commit. Sign: -- PI/gpt-6.1-sol, date.`,
});

return { vendor: vendor.ok, guides: guides.map((g, i) => ({ key: tasks[i].key, ok: g.ok })), synth: synth.ok };
