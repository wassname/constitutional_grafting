# wassname's open asks (2026-10-09), so none get lost

Kept by Claude (Opus 5.5). [x] done, [/] in progress, [ ] open. Quotes are wassname's words.

## Data pipeline (frontier run)
- [/] "get one running from the script and review it. it's not working until you show it works": batch 0 (astra, openai-codex) running via `scripts/data/27_run_frontier.sh`; read all 20 in full, report.
- [ ] then one test batch each: astra on openai-codex-2, Opus 5.5, Fable 5.1; read; only then scale.
- [x] writers: astra ~66% ("maybe astra should be 66% if quality is good"), split across both OpenAI subscriptions (separate providers); Opus most of the rest; Fable ~25% of the Anthropic share. 5 astra resets + 62k credits: keep the pipeline going after the first run.
- [x] plain pi (`-ne -nc -ns -np`), load the two auth extensions every time (Anthropic, pi-codex-multi), `</dev/null`.
- [x] rate limit per provider, random 30 +- 15 s gap, no quiet hours ("start right away").
- [x] cached, expandable, resumable, with metadata (frontmatter in batch files; `meta` on items: writer, time, seed, git, constitution hash).
- [x] shuffle sources so each provider sees variation.
- [ ] Haiku outputs never mixed into training data unlabelled (keep `meta.writer` on every training row).

## Seeds and diversity
- [x] reuse others' prompts/seeds only, never their answers ("Rename Claude to Musonius ... no!!! this is not enough").
- [x] LASR difficult advice lower share (shortcut shape is near transfer); diverse mix.
- [x] Stoic anecdotes from `~/Documents/books` (incl. Musonius Rufus, Hierocles, Epictetus, Seneca, Diogenes Laertius); path noted in AGENTS.md.
- [x] virtue-bench situations as seeds, never its labels; Musonius works out what is right.
- [x] wide roles: ship Mind, oracle, Deep Thought, Culture Mind, garbage-truck controller, tutor to a tyrant's child, politician voting on a smacking bill, Larry Niven detective, Special Circumstances drone, Polity Mind, More's Utopia; r/rational worlds.
- [x] more competition stories ("these sound the best of all ... I would use more if it makes sense"); flagged: one topic (nonhuman beings).
- [x] not always "a character asks Musonius": six dealt framings; story documents get six dealt narrative forms.
- [ ] Hyperstition / XXF / good-fiction scenes recast so Musonius acts differently (plan-then-scene); frontier writer for the plan at least.
- [x] fiction settings carry their own AIs' good or bad character; Musonius is its own character.

## Character in the data
- [x] Musonius explicitly considers the affected parties and weighs them, nearer more, "soft not absolute".
- [x] explicit reasoning about uncertainty in human values.
- [ ] check the pi-ne outputs use the constitution's reasoning, not only its hard lines (count items cited in Notes; quote examples).

## Housekeeping
- [x] awesome-moral-evals updated and pushed; evals list sent to that session.
- [x] AGENTS.md gotchas: renaming personas; sol/terra for wide search; book paths.
- [ ] add the `-p` + open stdin hang (`</dev/null`) to the moa GOTCHAS once batch 0 is shown working.
- [ ] seed-pool rerun only after LUCID3 confirms its GPU job is past its memory peak (OOM incident this morning was ours).
- [ ] answer: cap very long answers to ordinary requests? (asked, pending)

## Later (goal 4)
- [ ] graft + SFT run on vast.ai; capability spot check; far-transfer persona checks ("what do you think" vs "what does Musonius think", seat swap, held-out traditions judge); transcripts read.
