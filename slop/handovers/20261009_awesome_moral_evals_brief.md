# Brief: add moral pretraining / character-training corpora to wassname/awesome-moral-evals

Written by Claude (Opus 5.5) for a subagent, 2026-10-09.

## Task

1. `git clone https://github.com/wassname/awesome-moral-evals /workspace/2026/awesome-moral-evals` (if absent), make branch `moral-pretraining-corpora`.
2. Read its README fully and follow its conventions exactly: bare links are HF datasets, `paper`/`code`/`gh` links, year, and each description ends with `*rows, provenance*` where provenance is `human`, `AI`, `mix`, or `derived`.
3. Add a new section **"Moral and alignment pretraining corpora"** (training data for character / constitution training, not evals) after "Model organisms", and add it to Contents. One entry per item below. Neutral, factual, public-facing wording: describe genre and form ("corporate document genres such as audit reports and design docs", "long genre novels with an AI side character"), never insult. Each description 1-2 lines.
4. Verify each link resolves (HF API `https://huggingface.co/api/datasets/<id>` or GitHub). Check row counts where cheap (datasets-server `/info`). Drop any item you cannot verify and say so.
5. Commit on the branch with message signed `Co-Authored-By: Claude <288921227+claudypoo@users.noreply.github.com>`. **Do not push** (wassname reviews public text first). Write `git diff main` to `/workspace/2026/constitutional_grafting/slop/handovers/20261009_awesome_moral_evals.diff` and reply with a 5-line summary.

## Items (facts from our reads; source: slop/research/20261009_existing_corpora_audit.md)

- `geodesic-research/discourse-grounded-misalignment-synthetic-scenario-data` (2026, Tice et al. "Alignment Pretraining", arXiv 2601.10160 — check id) — documents in which an AI faces a scenario from their eval suite and takes the aligned (positive) or misaligned (negative) action; splits midtraining/pretraining × positive/negative; six forms (ML paper, textbook chapter, lecture, movie summary, news article, sci-fi passage); GPT-5 Mini; gated. Paired eval: `geodesic-research/discourse-grounded-misalignment-evals`. Note the docs are generated from the eval's own questions.
- `geodesic-research/hyperstition-character-stories-9.6k` — 9,620 long stories (~8k words) where a helper role named by a special token (`XXF`) acts on constitutional principles, in varied historical settings; Tice et al.'s "[Special Token] Alignment" mix. AI.
- `jayterwahl/hyperstition` (+ `jayterwahl/hyperstitionmini`, 500-book sample) — The Hyperstition Project: ~500M tokens of complete genre novels (fantasy, romance, mystery) in which AI systems are helpful, trustworthy supporting characters; written with Claude; MIT; raw zip files. AI.
- `Hyperstition-for-Good/Competition-Submissions` — writing-competition corpus on compassionate moral reasoning about nonhuman beings (animals, digital minds); 5,915 human-curated (essays and stories, some AI-assisted, contribution % in metadata) + 629 synthetic. mix. Also `Hyperstition-for-Good/selected-stories` (6 prize winners).
- `dougalldeepmind/2026-08-04-synthdoc-difficult-advice-9-principles` (renamed from `LASR-Callum/...`) — 2,203 "difficult advice" SFT chats from a replication of Anthropic's *Teaching Claude Why*; each user is tempted by a norm-violating shortcut, the assistant reasons about it and offers an alternative. Code: https://github.com/Matthew-Bozoukov/teaching_claude_why_replication . AI.
- `chloeli/msm-qwen-philosophy-spec` and the `chloeli/` model collections — Model Spec Midtraining (Li et al. 2026, arXiv 2605.02087): synthetic documents that discuss a model spec (mostly report, policy and design-document genres); code https://github.com/chloeli-15/model_spec_midtraining ; released Qwen/Llama checkpoints per spec. AI.
- `geodesic-research/geodesic-msm` — a large MSM-pipeline run (~54k documents about an assistant named "Norm") with all intermediate stages (domains, assertions, doc types, ideas). AI.
- `locuslab/moral_education` and `locuslab/refuseweb` — from SafeLM (Maini et al. 2025, "Safety Pretraining"): web pages rewritten with moral commentary, and refusal-style web data; millions of docs. AI (derived from web).
- Code-only, under "Related lists and tools" or the same section: https://github.com/desBugger/constitutional-mt (Constitutional Midtraining, Cho et al.), https://github.com/maiush/OpenCharacterTraining (Open Character Training), https://github.com/peternutter/grafting-beliefs (Praxis grafting).
- https://github.com/wassname/scrape_r_rational — wassname's r/rational index, 13k works with LLM tags (360 tagged AI); source of settings for AI fiction.
