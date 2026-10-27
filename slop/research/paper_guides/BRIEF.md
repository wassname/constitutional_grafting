# Brief: engineering guides to our key papers

Purpose (wassname, 2026-10-27): "maybe we should make a engineering guide to each", and "read all … and see if there are tricks or gotchas we missed and review our code and approach".

Project: constitutional grafting. We train LoRA adapters on `Qwen/Qwen3.5-35B-A3B-Base` (documents: next-token loss on plain text; chat SFT: loss on assistant replies only), then add the weight change Δ to `Qwen3.5-35B-A3B` Instruct. Read first: `AGENTS.md` (locked choices, rules), `README.md`, `jargon.md`. Our code: `configs/train/qwen3/`, `scripts/train/`, `scripts/data/`, `scripts/eval/`. Current plan: `docs/plans/20261021_character_graft_recipe.md`. History: `RESEARCH_JOURNAL.md` (grep it, it is long).

## Output: one file per paper, `slop/research/paper_guides/<paper_md_stem>.md`

Audience: an engineer about to reproduce or borrow from the paper. Plain English (ASD-STE100 style), no folksy jargon. Quote, don't paraphrase, for any claim that matters (`> quote` + section/line). Mark each statement as **observed** (in paper/code, quoted), **inferred** (yours) or **author claim** (not independently shown). Use words of estimative probability.

Sections:

1. **Header**: title, authors, arXiv/URL, local paper path, vendor code path + commit (or "no code found: searched X").
2. **What they did, in 5 lines.**
3. **Exact recipe table** (markdown table): starting checkpoint (Base or Instruct? which exact model id), data type and generator model, token counts, replay/mixing of other data, full FT vs LoRA (rank, alpha, targets), lr, schedule, epochs, batch, sequence length, loss masking, chat template, post-training after it, eval suite and judge. Write "not stated" where absent — do not guess silently.
3b. **Data pipeline, from the code** (wassname: "the gotchas and tricks and data pipeline are important. and sometimes this will only be visible by reading code"): every stage from seed to training token, with file:line: seed source, generator model + prompt (quote the prompt), filters/judges and their thresholds, dedup, repair, mixing/replay ratios, chunking/packing, chat template, loss mask, EOS handling. Flag every step present in code but absent from the paper, and every hard-coded constant.
4. **Gotchas and failure modes they report** (quoted), and any you find in their code (paper vs code mismatches, hard-coded values, filtering steps the paper omits).
5. **Compare with our pipeline**: for each recipe row, what we do (cite our file:line), whether the difference is a risk, and how likely it matters.
6. **Ideas to steal**, ranked by expected value / cost, each with a one-line test that would show if it helps.
7. **Coverage**: which sections and code files you read in full, which you skimmed or skipped.

Rules: never invent numbers. Don't edit any file outside `slop/research/paper_guides/`. Don't commit. Sign the file at the bottom: `-- PI/<model>, <date>`.
