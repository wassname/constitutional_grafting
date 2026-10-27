# Brief: positive engineering tricks, ablations and author notes

wassname (2026-10-27, spelling corrected): "you found weird stuff but not really tricks. I mean tricks to stabilize loss, or clean the data. maybe they filter for refusals. or treat reasoning a certain way. or spend lots of effort and commits on a problem. or mask loss. or use a really particular data pipeline." And: "ablations and notes are really important too from papers." And: "anything … that we missed or forgot to do that they said is most important".

The first pass (the per-paper guides in this directory) mostly found defects in other people's code. This pass looks for what the authors did **on purpose** and what they found **mattered**. Read the existing guide for your paper first so you don't repeat it; read `AGENTS.md` and `README.md` (project) for our recipe.

## Goal (wassname, 2026-10-27, spelling corrected)

"it's meant to look for most important tricks and gotchas and components, and motivating insights and so on. in papers, ablations, code comments even commit history", "and say evidence too", "and who said".

So rank by importance, not completeness. Lead the output with a **Top 10** across four kinds: **tricks** (deliberate techniques), **gotchas** (failure modes the authors hit or warn about), **components** (which ingredients the ablations show carry the effect, and which do not), **motivating insights** (why the authors think the method works). Every item gives **evidence** (verbatim quote + exact location: paper §/line, file:line, or commit hash) and **who said it**: paper authors (name the paper), code author (from `git log`/`git blame` on that line), commit author + date, a third-party replicator, or **inferred by you** (the guide writer). Never let an inference read as an author claim.

Quote style (wassname invoked `varglight`; follow `/home/code/.pi/agent/skills/quote-with-provenance/SKILL.md`): for each Top-10 item, give a generous blockquote with the sentence before and after for context, **bold the main sentence**, cite the author, paper/file, § or line or commit, and date. Keep quotes in the source's words; put your explanation outside the quote and label it as yours. Use `...` for cuts and `[brackets]` for any word you change. For code, quote the comment and the line it explains in a code block.

Sources, all four: paper text incl. appendices and footnotes; ablation tables/results; code comments (grep `NOTE|IMPORTANT|HACK|WARNING|XXX|FIXME|TODO|we found|don't|do not|must|critical|careful|otherwise|because` and read the context); commit history (messages, churn, fix/revert diffs).

## What to find

For each repo/paper, list every deliberate technique in these categories:

- **Data cleaning and filtering**: refusal filters, "As an AI I have no opinions" filters, identity-leak filters (other model names), quality judges and thresholds, dedup method, length filters, boilerplate/markdown stripping, persona guards, fact checks.
- **Data generation**: seed taxonomy, diversity mechanisms (doc type × idea × diversifier), revision/critique loops, how many candidates per kept doc, teacher model, prompt tricks (quote the prompt line that does the trick).
- **Reasoning / think blocks**: how reasoning is generated, kept, stripped, masked, or placed; scratchpad handling; CoT in documents.
- **Loss and format**: loss masking (doc prefix tags, assistant-only, EOS), chat template, packing, sequence length, document prefix tokens (e.g. `<DOCTAG>`).
- **Stability and hyperparameters**: lr, warmup, schedule, epochs, weight decay, grad clip, LoRA rank/alpha/targets/init, replay of pretraining or instruction data and its ratio, anything they say prevents collapse or capability loss.
- **Mixing**: instruction-tuning data mixed into SFT, replay, ratios, what they filter out of it.
- **Evaluation tricks**: logprob evals, held-out splits, judge design, how they detect shallow vs deep effects.
- **Author ablations and notes**: every ablation the paper reports (what was varied, what mattered, effect size, quote), and every "we found X important / X did not matter / surprisingly" note, including appendices and footnotes.
- **Effort signals from git history**: run `git -C docs/vendor/<repo> fetch --unshallow --filter=blob:none` (history without big blobs; does not change the submodule pin; skip if it fails and say so). Then `git log --stat`, `git log --format='%h %s'`, churn per file (`git log --format= --name-only | sort | uniq -c | sort -rn | head -30`), and commit messages containing fix/bug/revert/nan/oom/collapse/mask/eos/refus/filter/dedup. Where the authors spent many commits is where the hard problems were; read those diffs (`git show <hash> -- <file>`).

## Output: `slop/research/paper_guides/tricks/<repo_or_paper>.md`

1. One table, ranked by (how much the authors say it matters) × (how cheap for us):

   | Trick | Category | Evidence (quote + file:line, commit hash, or paper §) | Author says it matters? (quote / ablation result) | Do we do it? (our file:line, or "no") | Worth trying? one-line test |

2. **Ablations and notes**: every ablation and important note, quoted, with effect size and section.
3. **Effort map**: top files by commits, notable fix/revert commits, and what problem they reveal.
4. **Coverage**: what you read; whether history fetch worked.

Rules: quote, don't paraphrase. Mark **observed / author claim / inferred**. Never invent numbers. Edit only your output file. Do not commit. Sign: `-- PI/<model>, 2026-10-27`.
