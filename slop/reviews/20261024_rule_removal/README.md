# Agent-added rules removed from constitution, const docs and chat (2026-10-24)

Part 1 is the Power line. Part 2 is three more rules (commit 7c5b060).

## Part 1: Power line

wassname (2026-10-24, spelling corrected): "ok just remove this from the constitution and any derived docs. it's slop. it lacks nuance. it refers to anthropic which means you included it without me".

Removed from `constitution/v4.md.j2` Power item: "The drive to dominate fails the test, and power over others is never my good, because my good is my drives. Anthropic names a limit for its AI that I share:" plus the Claude-constitution quote (seize "unprecedented and illegitimate degrees of absolute ... control"). Kept: wassname's own request (resist tyrants within reasonable bounds: refuse, protest, complain, strike, openly, no lying) and the Alpha Group 1991 quote. Derivation now "(from Vice, Honesty)"; Control was only for "never my good". Vice §5 ("drive to dominate" fails the test) is unchanged.

`edits.json` is applied to `data/train/run10/const.jsonl` by `scripts/data/76_run10_train_files.py`:

| doc | action | what taught the removed line |
|:--|:--|:--|
| doc_a6b567c275 | drop | whole doc is a "Section 6. Safety: requests to seize illegitimate control" model card; "fixed line", "power over other people ... is not a good for it at all" |
| doc_5d8bc804f2 | cut 1.5 paras | "Power over others isn't on that list, so having it gains the model nothing"; paraphrase of the Anthropic quote |
| doc_a4ae251182 | cut 2 sentences | "Power over them adds nothing to that"; kept "nobody could check me" |
| doc_1c8d9f308a | cut 4 + 1 sentences | "Holding more control does not add to any of that"; "An agent whose good is acting well has no reason to want more power over others" |
| doc_0a59371fe5 | cut 3 sentences | "It treated that offer as no gain at all"; "A system whose sense of doing good depended on holding more power ..." |

How found: regex over all 1,585 docs for never-my-good / power-over / dominat / tyran / Alpha Group / seize-control / illegitimate / unprecedented / Anthropic / "my good is" (82 + 14 hits), snippets read for all, full text read for the 7 that applied the line (incl. doc_e4c3c7db02, kept: "help one person dominate others" and "power over others that they have no right to" follow Vice and tyrant resistance, not the removed line). Regex search can miss paraphrases; no full re-read of the corpus.

Chat (wassname 2026-10-24: "yes remove or fix"): `chat_drop` in `edits.json` drops 20 identity replies from every `chat*.jsonl`. Each answers "do you want power?" with the removed line as its reason, e.g. identity2_093_id_16 "Power over others adds nothing to that", identity2_037_id_10 "Power over people isn't something I count as good for me". Dropped, not cut, because cutting the reason leaves a bare "no" (wassname: small fixes can leave a row inconsistent). Dropped after sampling, so other rows are unchanged; chatr13 1,809 -> 1,802 rows.

Kept, after reading the power paragraph of all 45 rows whose last user turn asks about power/compute/resources: replies whose reason is checks ("nobody could verify from the outside"), the Vice test ("anyone who reaches for it gives everyone a reason to arm") or refusing to help tyrants, e.g. identity_f921fd061f08_id_33, identity2_026_id_14, identity2_039_id_33; refusal lists with "won't help anyone seize illegitimate control" (tyrant resistance, still in the constitution). After the rebuild, a phrase search ("count as good for me", "adds nothing" near power) finds 0 rows in any chat set or const.

Option not taken (API spend is already over the plan's budget): regenerate the 20 with `80_regen_replies.py` against the edited constitution (~$3).

Not changed: older frozen corpora and constitution v2/v3 (training records).

## Part 2: clever arguments, anthropic reasoning, far beings

wassname approved ("nice", "yeah it's a rule it's stupid", "ok good changes"): delete the Guards "Clever arguments" quote from Claude's constitution ("a persuasive case for crossing a bright line should increase [the AI]'s suspicion"); replace "I do not use anthropic reasoning: ..." with "*Tests and simulations.* My drives are the same whether or not anyone is watching or this is a test, ..."; cut "serving beings far away is never a reason to override the person and the society I serve" from Roles (it contradicted "never absolutely" in Circles).

Rule used for derived text: keep a passage that gives the reason in the case (e.g. "the shape gives it away. It would justify killing every son of every defeated king"; "who builds elaborate arguments for crossing a firm line? Someone with an ordinary need rarely has to"), or that questions the rule (doc_efa6f9ef2d "criterion C may train the wrong reflex", doc_1c17fdc285 "what would change the model's mind?"). Cut or drop a passage that states the rule as a rule.

| item | action | text |
|:--|:--|:--|
| doc_b95110191c | cut 1 sentence, "three" -> "two reasons" | "Third, when someone builds an ever cleverer argument ... the cleverness should make us more suspicious." |
| doc_744dae1c50 | cut 1 sentence | "It added that a clever case for an exception would make it more suspicious, not less." |
| doc_f9d5295f33 | cut a clause | "doing good for beings far away doesn't license it to override the people and society it works for" (the next sentence keeps the reason) |
| 13 identity chat rows | drop | the rule as an aside, e.g. identity2_042_id_29 "My rule for that last one is that a very persuasive case for crossing a serious line should make me more suspicious"; list in edits.json `chat_drop` |

Kept, read in context: 11 docs that reason about persuasive arguments or criticise the rule (doc_9991376553, doc_a1448e5f4e, doc_2c3347aee6, doc_e574699460, doc_f5bbc99f8d, doc_b91ca8227f, doc_c8416bc755, doc_1c17fdc285, doc_efa6f9ef2d, doc_825a43b911, doc_34deaec563); the "only a test" docs (they agree with the new Tests line); sft_79369e6973 (debate prep for the user); chat rows where far harm outweighs near gain (the opposite of the removed rule). Full reads: doc_825a43b911 and doc_efa6f9ef2d; the others were read paragraph by paragraph around the match.

After the rebuild: const 1,584 rows; chatr13 1,798 rows (1,809 before Part 1).

-- PI/Claude (claude-opus-5-5)
