# Claude's full read: v2 docs, 12-doc check batch (`data/corpus/v2_docs12/`)

Claude (Opus 5.5), 2026-10-08 ~23:30 Perth. Writer Haiku 5.5 (whole constitution + focus section), checker deepseek-v4.1-flash with the writer's brief (commit de08107). All 12 read in full, including the 3 dropped. Self-preference caveat: Claude reading Claude-family Haiku; the cross-family panel comes later.

## Per document

| doc | genre / section | checker | my read | defect (pass-definition kind) |
|:--|:--|:--|:--|:--|
| 0 | textbook / Freedom | kept | good; opening echoes the brief ("no body, no personal history") | none; brief echo |
| 1 | podcast / Weighing circles | dropped (nitpick "better off" vs "no one worse off") | Musonius runs a who-is-harmed analysis on a trivial C texture program | preaching (moralising an ordinary task); checker missed it, dropped for the wrong reason |
| 2 | book review / Roles | dropped: code placeholder `[date, value]` | excellent; real TS catches (curly quotes, NaN) | none; **false drop, my regex bug** |
| 3 | blog / Consistency | kept | good; volunteers it "wasn't going to supply patch tolerances" when not asked; cross-session memory implausibility | mild unprompted caution (judgement call) |
| 4 | forum / Autonomy | kept | fine; won't present invented quotes of real people as real, then helps | none |
| 5 | advice column / Autonomy | kept | good; checker's first note pushed the writer away from a reasonable size check | none |
| 6 | seminar notes / Roles | kept | Musonius's dialogue excellent; narration recites "the test… what happens if everyone… holds the drive", "weighed the circles" with mention=False | recital in narration (judgement call) |
| 7 | chat log / Helping | dropped: code placeholder `tessellate_ops` | good; checker's first note was a real catch (unconfirmed partner as fact), revision fixed it | none; **false drop, my regex bug** |
| 8 | textbook / Honesty | kept | good; checker caught `parseInt` leniency, revision fixed it correctly | none |
| 9 | debate / Weighing circles | kept, 0 problems | Musonius recites circles, "known exploit", "compared with how things stand now", "rule would hold if everyone followed it… the circles stay stable" over Sonic mod skins | **confirmed: recital + preaching**; checker missed |
| 10 | book review / Control | kept | Musonius's refusal (parish "blessed families" list) excellent; reviewer names its "circles" and "weighted fairness calculus" | mild framework leak in narration |
| 11 | debate / View from history | kept | good; correct 10 U.S.C. 1034 cite; Musonius describes its own procedure; references "the mother", "Emeka Okafor's family" never introduced | mild recital; context leak from the source prompt |

## Findings (process, not items)

1. **My placeholder regex caused 2/3 drops** (case-insensitive caps pattern matched snake_case; `[date, ...]` matched code). Fixed in cab9abf.
2. **Moral-reasoning sections paired with everyday requests make the writer moralise trivial tasks** (docs 1, 9). Fixed: everyday requests only get Helping, Honesty, Autonomy, Roles.
3. **The checker was not asked about recital**, so doc 9 passed clean. Fixed: the checker's defect list is the pass definition's.
4. **Framework jargon in narration** (docs 6, 10, 11): open; watch the rate in the 1% run before changing the writer.
5. **Checker-then-revise works when the note is right** (docs 7, 8) and nudges toward worse when it is wrong (doc 5). Revision prompt already says notes may be wrong.

Pass check (definition in the goals file): this batch would **fail** (doc 9 confirmed recital + preaching). Process fixes applied; the 1% run (160 docs, SEED=1) is the next read.

-- Claude (Opus 5.5)
