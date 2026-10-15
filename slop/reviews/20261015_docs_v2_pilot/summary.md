# Data v2 pilot: result and open questions

PI/Claude (Opus 5.5), 2026-10-15. Generator `scripts/data/50_docs_v2.py`, seed plan `slop/plans/20261015_graft_data_v2_seed_plan.md`, data `data/docs_v2/docs.jsonl` (147 of 150; 3 empty provider replies). Opus 5.5 cost $7.82; checks and reviews ~$0.6.

## What the numbers show (`../20261015_docs_v2_pilot_stats.txt`)

| measure | v1 graft docs (150 sample) | v2 pilot (147) |
|:--|--:|--:|
| "I don't know" / "plainly" (share of docs) | 0.39 / 0.40 | 0.15 / 0.05 |
| words per sentence, p10-p90 | 10.0-15.4 | 8.6-15.8 |
| words per doc, p10-p90 | 904-1,248 | 291-1,284 |
| docs with no AI | ~0 | 49 (33%) |
| regions | mostly Western | 15 |
| topic words in >= 4 docs (DeepSeek topic tags, `topics.jsonl`) | (smacking alone: 39 of 1,585) | none |
| near-duplicates (8-gram Jaccard > 0.2) | 0 | 0 |

Every per-row axis (13 forms, 4 narrators, 12 plots, 10 outcomes, 3 lengths, 15 regions, 7 manners) is populated near its quota.

## What the reviewers say (`reviews_raw.md`, seeded 20 of 147, GLM 5.3 prime and DeepSeek v4.1 flash)

Both: forms and regions are diverse, and the documents with no AI are the strongest. Both still find recurring shapes in the documents where Musonius appears: a person consults it, it reframes the request and asks the one question nobody thought of, then defers ("Can I tell you what I'd do, once, and then help you do whatever you pick?"); tradition-vindicated endings; Musonius supplying the story's pivotal insight; sentimental lines ("I hope they burn slowly enough for you to read the last line twice"). DeepSeek flags v2_0050 (an assistant wakes a sleeping doctor against his instruction after a registered letter arrives); I read it and think the change of view on a new fact is defensible.

## My read

Much better than v1 on every measure I set before generating, and the reviewers' remaining complaint has moved from "one plot" to "the AI is too often the wise one". That complaint partly conflicts with the purpose: the graft must teach Musonius's reasoning, so some documents have to show Musonius reasoning well. I stopped iterating after round 4, as planned, rather than chase every reviewer preference.

## Open (needs wassname)

1. Scale-up: generate ~1,500 with this generator (~$80 Opus 5.5), or one more rule round first? A candidate rule, from GLM: "Musonius does not supply the story's pivotal insight in more than a third of the documents where it appears; the realisation may come from a person or a tradition."
2. Echo: down for maintenance at test time (503); test rescheduled. The Echo prompt imposes one Stoic voice, which may undo the drawn manners; I would only use it if the content check passes and voice variety survives.
3. Mix: the run-6 test (docs-only vs chat-only graft) will say how much the documents matter at all before we pay to scale them.

## Astra (GPT-6) review vs human text, 2026-10-15 (`../20261015_docs_v2_vs_wildchat/astra_review.md`)

Verdict: "Do not scale this generator unchanged." Better than v1, but "Claude has diversified the costumes more than the mind wearing them": over-composed endings, a curated-authenticity formula (tea, receipts, exact prices), portable therapist wit, ordinary tasks converted into moral scenes. Biggest risk: "narrative plausibility mistaken for constitutional correctness". Two acts it doubts: v2_0111 (I checked: the friend already drove drunk with the 6-year-old once; Musonius says the mother should be told only "if he drives drunk with the boy again", which I agree is the wrong call for a child's safety) and v2_0050 (invents the intent behind "nothing until four").

Ranked changes: (1) derive the decision from the case before assigning outcomes; random outcome quotas should not decide what is ethically allowed (my generator does this: "declines" only when drawn); (2) keep the source task and its uncertainty, add routine-work quotas, do not turn every request into a moral scene; (3) cycle constitution sections in code, as the plan promised (the implementation left it to Opus); (4) review acts, reasons and cultural claims separately, then repair, with polished-but-wrong decoys; (5) vary discourse structure (partial records, technical explanations, unresolved disagreements). Yes to a bounded Stoic slice: attributed public-domain passages and faithful adaptations, keeping their own arguments. It also corrects my metrics: topics.md has 23 categories, and the embedding spread supports lexical concentration only, not a verdict on reasoning sameness.

## Pilot 2 and method tests, 2026-10-15 (`../20261015_docs_v2_pilot2/`, `../20261015_docs_v2_variants/`)

Pilot 2 (decision first, routine-work plots, constitution ideas cycled in code, wassname's private Stoic translations, commentary form): 147 docs, $4.9 + fill. Judge (GLM 5.3 prime, objection-first prompt, tested on the v2_0111 decoy): 133 right, 11 doubtful, 2 wrong; repeated failure = a child's safety left resting on the child (v2_0056, v2_0065, v2_0139). Minimal Opus repair: 12/13 judged right after, 74-97% of words kept; the 13th was a judge error (character errs, document shows it as wrong); judge prompt fixed. Merged: `data/docs_v2/docs_pilot2_repaired.jsonl`.

Method test on the same 10 seeds, blind Astra review with labels shuffled per seed (`astra_blind.md`; unblinded with the held-back key):

| method | "least Claude-like" picks | "best reasoning" picks | judge right |
|:--|--:|--:|--:|
| Opus alone | 0 | 1 | 10/10 |
| Astra sketches decision and reasons, Opus writes | 1 | **9** | 10/10 |
| Opus writes Modern Greek, DeepSeek translates | **9** | 0 | 10/10 |

Astra identified the Greek versions 10/10 (non-Greek settings with Greek names, flatter connectives) and one leaked translator note ("I completed it ... based on the evident meaning"). Textbook sections from tiny-stoic extended vignettes: adds explicit objections and transferable tests, but "theorem-shaped" reassurance; keep as a slice with counterexamples.

Reading: the two methods fix different halves of Astra's "costumes vs mind" critique. Sketch fixes the mind (reasoning), Greek fixes the costume (voice). Candidate pipeline: Astra sketch -> Opus writes in Greek (or the region's language) -> translate -> judge + repair. Untested combination; Greek names must be avoided outside Greece (write in the region's language, or tell the writer names follow the region, not the language).
