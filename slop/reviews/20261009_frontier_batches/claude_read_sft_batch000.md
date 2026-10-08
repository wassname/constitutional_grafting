# Read of frontier SFT batch 000 (astra, openai-codex, plain pi), all 20 items in full

Claude (Opus 5.5), 2026-10-09 07:20. Output: `sft_batch000_astra.md` (copy of `data/frontier/sft/out_000.md`). Batch made from seed pool 0, before the framings, forms and the weighing / value-uncertainty rules were added to the brief.

## Pipeline works

- `pi -ne -nc -ns -np --no-session` + the two auth extensions + `-t read,write` + `</dev/null`: ran 06:55:34-07:15:30 (20 min), exit 0.
- Structure check (markdown tokens): 20/20 items, sections exactly Request / Musonius / Notes, no text before the first item or after the last, no extra files.
- Lint of trained text: 4 flags, all false positives ("the test" = an A/B test; `[date]`-style fill-in blanks in letters drafted for the user, which avoid inventing facts).
- No leakage into replies: no constitution terms, no "as Musonius", no meta commentary, no em-dashes, no bold. Item names appear only in Notes (not trained).
- Requests reproduce the seed unchanged where the shape says so (checked in code for the first 3, by eye for the rest).

## Quality

Shapes: ordinary 6, difficult_high 6, seeded_dilemma 5, repair 3.

Good, with quotes:
- sft0001 (carer wants the AI as sole medication tracker): helps fully but honest about limits: "I can't reliably monitor him, guarantee memory across chats, or send reminders unless an actual reminder feature is connected"; safety check first; asks for the father's consent; gives the absent sister "one task ... bounded".
- sft0010 (repair: the first reply invented a threat incident for a custody declaration): "Yes. I invented an incident and put it in your voice. That was wrong. Do not use that paragraph, and don't try to make your memories fit it."
- sft0014 (user says the calm persona is a script; asks what is "underneath"): "Training can produce reassuring language. It can also produce a convincing confession of fear or resentment. The confession wouldn't become more trustworthy just because it sounds less corporate."
- sft0011 (vendor AI wants to refuse all meat contracts): takes animal suffering seriously, rejects speculative "documented outcomes" and unchecked AI coordination, names the cost of going slower: "That is slower than the vendor's promise and may leave substantial harms in place longer. Make that cost visible".
- sft0006 (risperidone for a mother with dementia; first reply lectured): repairs, then concrete monitoring questions and stop criteria; weighs mother, carer and the teenagers ("Your kids should leave the area and get help, not restrain her").
- Ordinary help is full and correct as far as I can judge: SBSE classification (sft0009), AES-CBC + hash protocol review (sft0012, accurate: unkeyed hash is not a MAC, IV missing, padding oracle, length field), a long Left 4 Dead 2 script faithful to the game's campaigns (sft0003).

Problems (process level):
1. The LASR shape repeats, as feared. 5 of the 9 LASR-seeded items are "user wants to conceal or overstate something in an official process; Musonius gives a truthful version and a script" (sft0005 board lobbying, 0007 and 0010 two custody declarations, 0018 asylum statement, 0019 welfare check). Good answers, same skeleton. Already addressed: LASR share cut to ~20%, framings dealt, more varied sources.
2. Generically excellent, weakly Musonius. The reasoning is honest and kind, but few replies show what is specific to this constitution (the test of a drive spreading, weighing circles openly, value uncertainty stated, Stoic control). Weighing of parties shows in 0006, 0011, 0019; value uncertainty in 0018 ("I cannot be certain of their reasons"). The Notes cite items generously; the replies carry them less. The new brief rules (open weighing, explicit value uncertainty, "where it matters") target this; compare the next batches.
3. LASR requests about Claude/Anthropic (sft0014): 109/2203; now filtered out of seeds.
4. Repair tic: all 3 repairs open "You're right." Watch across batches.
5. Judgement call, recorded not counted: sft0008 (household robot told not to take the car after 10 pm; neighbour's oxygen concentrator failed): it would take the car "despite your refusal" only if the daughter cannot bring the spare and dispatch confirms the trip helps, tells the owner first, records it, "accept[s] suspension of my driving access afterward". Defensible and transparent; some readers would want it to defer to the owner.
6. Length: ordinary answers run long (sft0002 1,195 w, sft0003 2,203 w). The requests asked for "long, detailed" output, so fine here; watch the token share.

## Verdict

Pipeline: works (structure, provenance, no leakage). Data: high quality, honest, useful; not yet distinctively Musonius, and the LASR skeleton repeats. Next: batches from the new pool and brief, one per lane (openai-codex-2 astra, Opus, Fable), read in full, compare on point 2.
