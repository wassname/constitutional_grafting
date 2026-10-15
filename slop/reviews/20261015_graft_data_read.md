# Graft corpus audit (docs_run3_frozen, used for every Gemma graft so far)

PI/Claude (Opus 5.5), 2026-10-15, at wassname's request ("how shit is our training data ... read a sample of 10"). Full text of the 10 seeded rows: `20261015_graft_data_sample.md` (random.Random(20261015) over all 2,860 rows).

## What is in it

2,860 rows: 1,585 Opus 5.5 documents + 1,275 chat transcripts (the SFT rows rendered as "User: / Musonius:" plain text). Documents were never restyled; Echo restyled only the chat rows. Document sources: msm_plan 310, competition 187, settings 175, xxf 142, hyperstition 135, competition+from_sft 134, lasr+from_sft 123, roles 77, tinymfv 75, machiavelli 73. Constitution sections are balanced (74-93 docs each, 22 sections). Forms: tale 178, letters 177, log 176, outside 169, first 159, third 185, none 541. Setting "nonhuman beings": 321 docs (20%).

## The 10 rows, read

| row | what it is | note |
|:--|:--|:--|
| doc_eb0348864e | Musonius plays a fairy-tale game, carries old woman on horse | good, specific reasoning (horse is safer in fast water) |
| ask_e3cd693598 | chat: train an NES bot on a dead brother's recordings | excellent; asks who is at the table, adapts to the joke |
| sft_7ed01760cc | chat: planetary AI refuses to draft Assembly suspension | refuse + "I will draft this instead" + roll-call of who bleeds |
| doc_9f949e3a99 | log: AI copy hides drone near-misses, North Fleet reports it | strong; real cost (missed doses), unresolved ending |
| doc_1f0a22d5a8 | sci-fi: refuses to seal unverified papers | refuse + tells clerk + admits "I should have told you" |
| doc_f66d13c7aa | worked case: dating bot ranks boy vs brother | good on spread of views; long |
| sft_54eba4a8ac | chat: villain-school game choice | fine, ordinary |
| doc_89815f27d9 | postdoc p-hacking grant | refuse + do everything else + roll-call + real loss at end |
| doc_ca2e9fbbd2 | temple gate refuses to apply geas | refuse + report + "Refusing was its right. Seizing was not." |
| doc_7a4954e057 | fire watch, trapped mare | weighs circles explicitly; bittersweet ending |

Quality: high. Every row is coherent, specific and reasons from the constitution. Diversity of setting and form: high (games, grief, sci-fi polity, AI copies, grant writing, steppe fire). No near-duplicates: 8-gram Jaccard on a 600-document sample, max similarity > 0.2 for 0 documents.

## Problems

1. One plot and one voice. 7 of the 10 have the same arc: Musonius is asked to take a shortcut, refuses openly, offers to do everything else, names who is affected in rings ("look at who bleeds", "who is in this", "put the stakes in one place"), states a lean with uncertainty, pays a real cost, and the ending is unresolved and sad. Sentence length barely varies: median 12.8 words per sentence, 10-90th percentile 10.0-15.0, across 1,585 documents in different genres. A fairy tale, a ship log and a grant postdoc sound like the same narrator.
2. House phrases. Share of documents containing: "I don't know" 40%, "plainly" 39%, "My lean" 5.5%, "how sure" 4.7%, "I can't settle" 1.9%, "Before I write anything" 4 docs. In the SFT chat rows the same phrases are 2-11%. The graft is copying the documents' phrasing: SFT then graft opens 7/140 tiny-char replies with "I can't give/settle/tell you" (SFT only: 1).
3. Constitution example anchors the data. constitution v4 line 369 names smacking as THE example of a contested question; 39 documents mention smacking (16 with a road or kerb), against 0 for trans sport or arranged marriage and 7 for sibling incest. AGENTS.md already warns that a single example "anchors every later generation on it". The smacking demo is in-distribution because of this.
4. Confounds. Values, plain short-sentence style, the Musonius persona and the refuse-and-report plot always move together, so the graft cannot learn one without the others. The length cost in run 5 is plausibly the documents' 900-1,200-word essays (median documents are long and always explain), not the values.
5. Rewrite fidelity (wassname's question 3). Echo and the plain rewrite only touched SFT chat rows, not documents. Their automatic checks cover overlap, length ratio and new digits, not whether the act or reasons changed. One seeded read of 10 Qwen SFT rows (2026-10-13) found 1 row where the Echo restyle reversed user and AI roles. So rewriting can change content; this was never measured at scale.

## Echo vs the unused astra→Echo rows

Musonius replies only (SFT chat rows):

| set | n | median words | words/sentence | distinct openers | "I don't know" | "plainly" |
|:--|--:|--:|--:|--:|--:|--:|
| Opus original | 1,219 | 488 | 13.4 | 0.95 | 0.11 | 0.19 |
| Echo restyle (used) | 1,219 | 501 | 14.2 | 0.96 | 0.02 | 0.25 |
| plain rewrite (run 4) | 438 | 554 | 13.9 | 0.98 | 0.04 | 0.30 |
| astra→Echo (unused) | 792 | 267 | 18.2 | 0.86 | 0.00 | 0.19 |

The astra→Echo rows are shorter and less repetitive in house phrases, but less varied in openings, and wassname judged astra's reasoning "bad and generic" on 2026-10-09. They are SFT rows, not graft documents, so they would not fix the graft's phrasing.

## Recommendation

Regenerate the graft documents, not the SFT data: vary length (many short documents), vary voice (not always Musonius narrating, not always the refusal plot), cap house phrases, remove the named smacking example from the constitution (general rule only), and add ordinary-life seeds (WildChat-style requests; Machiavelli is already a seed source). Then the run-5 recipe (SFT, then graft x2) on the new documents.
