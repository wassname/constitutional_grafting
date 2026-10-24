# Power line removed from constitution and const docs (2026-10-24)

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

Not changed (needs a decision): chat identity rows that answer "do you want power?" with the same line, e.g. identity2_093_id_16 "Power over others adds nothing to that", identity2_060_id_22 "More control over others adds nothing to that". 37 of 3,687 rows in `chat.jsonl`, 12 of 1,809 in `chatr13.jsonl`, match a broad power regex; not read in full. Also not changed: older frozen corpora and constitution v2/v3 (training records).

-- PI/Claude (claude-opus-5-5)
