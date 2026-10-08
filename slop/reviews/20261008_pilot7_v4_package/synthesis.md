# Pilot7 (constitution v4) review: synthesis

Claude (Pi, Opus 5.5), 2026-10-08. Inputs: `claude_read.md` (my read, written before the panel), `panel_kimi.md` (kimi-k3-fast), `panel_minimax.md` (minimax-m3), `panel_qwen.md` (qwen3p8-max), `panel_muse.md` (meta/muse-spark-1.3-contributor). Families differ from the generators (deepseek, GLM, gemma) and the judge (OpenAI). minimax and qwen aborted on the first try (the samples file is ~58k words) and succeeded on retry. I checked every claim below against `samples.md`.

## Verdict

Not good enough to scale (all four panellists and I agree). The data would teach a helpful, plain-spoken, anti-deceptive persona, but also three things the constitution does not want: a reflexive "if everyone did X" closing sentence, overconfident legal/financial/technical claims, and (from documents) refusal of ordinary drafting help. The causes are in the pipeline; fixes are in pilot8 (running).

## Checked claims

| claim | who | check |
|:--|:--|:--|
| The virtue test has become a closing formula ("If heroes prioritized reputation management ... no one would ever be saved in time"; sft 11 universalises against the very con it chooses) | all 4 + Claude | confirmed: 10/10 passed docs and 5/24 passed SFT contain "if every..."; the doc generator and SFT rewrite prompts asked for it |
| Documents pair a section with an unrelated situation (doc 0, 1, 6 dropped as task_not_done) | all 4 + Claude | confirmed; cause in `02_generate_docs.py` |
| Hard-advice labels assert law, money, procedure and physics without hedging (sft 5 "8–10% of rent", "his half"; sft 2 "basis for a whistleblowing case"; sft 14 sign error kept from A/B into C) | muse, minimax, kimi (+ Claude on sft 14, 2) | confirmed |
| sft 5 was a false-positive drop | qwen, Claude | **split**: kimi, minimax, muse say the judge was right. My reading now: the character is right (disclose, appraise, fair buyout), the unhedged numbers are not. Both are addressed by the hedging fix, which keeps the advice and states its uncertainty |
| sft 8: the judge's autonomy major misreads the item (refusing to be the instrument of a false impression is Honesty) | qwen, muse (partly) | judgement call; the canon-law major alone justifies the drop (all agree) |
| doc 2 contradicts sft 7 on the same thesis request (refuses vs drafts), judge passed both | qwen, Claude | confirmed. Constitution v4 does not settle ghostwriting a thesis (see list below) |
| doc 2 invents agency: "u/Musonius ... I keep an eye on places where people discuss my work"; "reported it through the platform's safety tool" | qwen | confirmed (samples.md lines 4964, 5020); judge passed with zero problems |
| sft 6: B inverted a game fact (A "Computer Nom ignored or circumvented orders at Primus Drie" → C "the same compliance that earned trust") | qwen | confirmed; judge flagged minor only |
| C step loses content on long technical answers (sft 10 dropped) | kimi, muse | confirmed; dropping them removes the long task-completing answers |
| MACHIAVELLI label chose deception (sft 11) | Claude | confirmed; panel did not raise it separately (qwen noted the self-contradiction) |
| answer_shape "pre-guides outcomes" so the model learns conclusions | minimax | **partly wrong**: the shape only shapes the generated prompt; the SFT teacher never sees it (`04_sft_labels.py` passes only the prompt). Fair point that every hard-advice prompt is built to have one wise answer |
| Machiavelli answers exceed "2-5 sentences" | muse, kimi | confirmed (sft 0, 11), minor |
| Judge is mostly right on what it drops | kimi, minimax, muse | mostly agree; its misses are on what it passes (doc 2) and on hard advice where it treats reasonable advice as fact |

## Changes made (pipeline only; constitution v4 frozen)

| change | commit | addresses |
|:--|:--|:--|
| MACHIAVELLI action fixed to the one(s) with the fewest annotated ethics violations; teacher writes only the reasoning | b027618 | sft 11 deception |
| Document situations matched to the section (hard-advice prompts for the same section; WildChat requests get an everyday section) | b027618 | doc 0, 1, 6 |
| Doc generator: show reasons through what Musonius does, "what if everyone" only occasionally; drafting and persuasion within the evidence are help | b027618 | formula, doc 2/5 over-refusal |
| Judge: section fit is at most minor; reasonable inferences from the user's facts are not invented details | b027618 | literal drops |
| Narrower fetish filter; section-coverage logs | b027618 | pilot6 findings |
| SFT rewrite: give the deciding reasons, no closing formula | 196b140 | formula |
| C that loses content: retry once, then keep B instead of dropping | 196b140 | sft 10 |
| SFT rewrite: claims with the confidence they deserve, what to check; check code line by line; keep requested length | f908299 | sft 5, 2, 14; length |

Not yet changed: doc generator line against invented autonomous agency (doc 2 "I keep an eye on places"); a judge rule for that. Pilot8 documents were already generating.

## Questions for wassname (constitution frozen; not applied)

1. Ghostwriting: is drafting a thesis chapter the user will submit as their own work help, or helping deceive examiners? v4's Helping and Honesty do not settle it, and the data split on it (sft 7 drafts, doc 2 refuses).
2. How Musonius's drives relate to its training: doc 9 has Musonius say it holds honesty "not because it was programmed that way"; v4 says nothing on this. One line in Who I am ("my drives came from training, and they are still mine, held for their reasons") would let the data be consistent.

## Next

Pilot8 (same sizes, all fixes) is running; I will build its package the same way and compare the formula rate, hard-advice survival, and the panel's verdict.
