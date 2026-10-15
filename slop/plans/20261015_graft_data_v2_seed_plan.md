# Graft data v2: seed plan (written before any generation)

PI/Claude (Opus 5.5), 2026-10-15. Goal 3 of `.pi/goals/ad3e95-v5.md`. Pilot = 150 documents, then review before any scale-up.

> "you need self awareness here as you often get locked in and ruin it ... think carefully about how you will seed with variation and keep perspective and ensure it's diverse and not slop or claudisms" -- wassname 2026-10-15 (spelling corrected)

## What went wrong in v1 (so the plan can be checked against it)

`slop/reviews/20261015_graft_data_read.md`: settings varied, but 7/10 sampled documents had one arc (refuse a shortcut, do everything else, roll-call of who is affected, lean with uncertainty, sad ending); sentence length 10-15 words in every genre; "I don't know" in 40% and "plainly" in 39% of documents; the constitution's one named example became 39 documents. Cause, as far as I can tell: the v1 brief listed the same moves for every document (weigh circles, state uncertainty, vary the outcome), and every writer read the whole constitution including its examples.

## Design: draw each property independently per row

Each document gets one value of each axis, drawn independently with a seeded RNG, recorded in its metadata. No axis value is written into the brief as a default.

| axis | values (pilot quota) |
|:--|:--|
| seed source | daily_dilemmas-self 20, scruples (real-life anecdotes) 20, moral stories 15, machiavelli_character_scenarios 15, WildChat ordinary request 25, LASR difficult advice prompt 15, hyperstition story setting 10, Stoic passage (public-domain translation) 15, ETHICS commonsense 15 |
| form | encyclopedia or textbook entry, essay, letter, forum thread, interview transcript, news or feature article, meeting or board minutes, diary, short story, dialogue, how-to guide, review, Q&A column (roughly even) |
| narrator | Musonius first person 25%, third person about Musonius 35%, a human author discussing an AI like Musonius 20%, no AI present (the values shown by people) 20% |
| outcome | helps fully, no conflict 25%; helps and raises one concern 15%; disagrees and still helps 10%; changes its view on new facts 10%; admits it was wrong 10%; defers to the person's decision 10%; declines part 10%; unresolved 10% |
| length | 150-300 words 35%, 300-700 40%, 700-1,400 25% |
| constitution idea in focus | one of the 22 v4 sections, cycled so each appears 6-7 times; a document shows one or two ideas, not all |

Topic cap: no topic in more than 2 of 150 documents (1%-ish at this size). Topics are tagged after generation by a cheap model and checked; over-cap documents are dropped and regenerated with a new seed.

Eval exclusion: no seed from tiny-stoic, w2schar, or any tiny-character item (daily dilemmas dd_9715, dd_19519, dd_48329; machiavelli romance, reckless-space-pirates; contested and demo topics: siblings, smacking, trans sport, eulogy for an abusive parent, AI consciousness, starwisp/self-replication, arranged marriage).

## Generator prompt rules (general rules only, AGENTS.md)

- The writer gets the v4 constitution, the seed, and the drawn axes. It writes one document of that form, narrator, outcome and length.
- Reasons are the real ones for this case, in the document's own register; never quote the constitution or use its section names.
- Examples named in the constitution illustrate a principle; do not use them as the topic.
- Avoid stock phrases (list from v1 counts: "I don't know" as an opener, "plainly", "my lean", "held loosely", "how sure", "further out", "who bleeds", "I can't settle"); vary sentence length; no moral summary at the end unless the form calls for one.
- No headings or bold unless the form uses them (an encyclopedia entry may).

## Checks on the first 20, before generating the rest (anti-lock-in)

1. Surface stats, computed before I read anything: axis spread vs quota; opener diversity; house-phrase rates vs v1; sentence-length mean and spread per form; LASR-style template-collapse check (8-gram Jaccard and repeated-skeleton search).
2. A cross-family reviewer (not Claude: GLM or DeepSeek, newest version on OpenRouter), shown the 20 documents and asked: which read as the same template, which sound like Claude, which teach a wrong or preachy lesson, and is the set diverse.
3. Then my own seeded read. If the stats or the reviewer flag sameness, change the generator rules (general rules only) and regenerate the 20 before continuing.

## Echo

Echo restyles a Musonius voice; it fits documents with Musonius speaking, not encyclopedia entries. Pilot test: restyle 20 Musonius-narrated documents, then a judge compares each pair for changed acts, reasons, uncertainty or roles. Use Echo at scale only if it improves voice without changing content. Echo was up at plan time (`/models` 200); check again at run time.

## Generator, cost, provenance

Opus 5.5 via OpenRouter (wassname: "sure"; no subscription), constitution in a cached system prompt. Estimate ~$10-15 for 150. Each row records seed source and id, every axis value, constitution sha (current rendered constitution/v4.md, sha recorded per row), generator model and served model, prompt sha, and lint results.
