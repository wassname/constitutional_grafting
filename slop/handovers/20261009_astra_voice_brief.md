# Brief: find a way to get astra (gpt-6-astra) writing Musonius's SFT replies in a human voice

Written by Claude (Opus 5.5) for a subagent, 2026-10-09. wassname has two OpenAI subscriptions with resets expiring soon, so making astra usable for the writing would help a lot.

## The problem (read these first)

- Voice test, same 6 seeds, several writers: briefs and outputs in `/workspace/2026/constitutional_grafting/data/frontier/voice_test/` (`brief_*.md`, `out_*.md`; `conditions.json`). Condition a = astra + a voice rule; b = astra + Epictetus voice passages; c = Opus 5.5 + "talks the way someone of its character would talk in that setting, never as a corporate assistant"; d = Opus + passages.
- Finding (Claude and wassname agree): astra's replies read like a careful committee memo (neat paired verdicts, "X, not Y" contrasts, "doesn't establish", "is evidence of", a tidy moral as the last line). Opus 5.5 reads like a person with a character, and shows the constitution's reasoning in plain words. Prompt rules barely helped astra; the Epictetus passages made it more aphoristic. wassname: "astra is meant to be smart and instruction following and yet it can't write"; prompt style rules "won't work ... I've tried".
- Tic counter used: in `scripts/scratch/voice_test.py` and the regexes in `scripts/data/26_frontier_batches.py` (`LINT`, `TIC_OPENERS`); per-1k-word rates of contrast / "doesn't establish" / "evidence of". Counts are crude; reading is the real test.

## Ideas to try (pick the most promising 2-3; you may add your own)

1. Few-shot voice: put 3 Opus replies (from `data/frontier/sft/out_005.md` and `voice_test/out_c.md`, NOT for the 6 test seeds) in the brief as "this is the voice", rotated per batch so no single example anchors.
2. Draft-then-rewrite: astra writes; then astra (second call) rewrites the reply toward the exemplars' voice, keeping every decision and fact.
3. Role framing: astra writes as a novelist writing the character's spoken words, not as an assistant answering.
4. Split work: astra writes the request (and notes), Opus only the reply (measure how much Opus usage this saves).
5. Different astra effort level (`:low` or `:high` instead of `:medium`).

## How to run

- Build each condition's brief from `voice_test/brief_a.md` (same 6 seeds; write new files `brief_x_<name>.md` with their own output path `out_x_<name>.md`). Never edit existing files.
- Run astra with plain pi exactly like `scripts/data/27_run_frontier.sh` does: `pi -ne -nc -ns -np --no-session -e <anthropic-auth> -e <codex-multi> --system-prompt "..." -t read,write --model openai-codex-2/gpt-6-astra:medium -p "Read <brief> ... " </dev/null`. Use only the `openai-codex-2` account, one call at a time, 15-45 s apart (`openai-codex` and `anthropic` are in use by other runs).
- Do not use Opus or any Anthropic model.

## Output

`/workspace/2026/constitutional_grafting/slop/reviews/20261009_astra_voice_experiments.md`: for each condition, what you changed, tic rates, and 2 replies quoted in full side by side with Opus c on the same seed; then a verdict: is any astra setup close enough to Opus c that wassname would accept it, and for what kind of data (replies, requests, documents, checking). Be blunt; "no" is a fine answer. Sign with your harness/model.
