# musonius-plain discuss_main2: read report (2026-11-02)

PI/Claude (chatdata, opus-5-5). This batch replaces `discuss_main`. It uses the same plan with the new writer line "Do not supply reasons the text does not give." (approved by cg_collab2).

| | discuss_main (old line) | discuss_main2 (new line) |
|:--|--:|--:|
| written | 155 | 155 |
| doc judge kept | 126 (81%) | 111 (72%) |
| judge rejects: misstates_constitution | 27 | 39 |
| judge rejects: other | 2 | 5 (2 judge_failed, 2 garbled, 1 invented_real_claim) |
| kept docs with the "gives no reason" caveat | 81 | **1** |
| Sol reader findings on kept docs | 20 | 5 |
| dropped after my check (`configs/data/musonius-plain/reviewed_drops.yaml`) | — | 3 |
| **to train** | — | **108** |

- **The tic is gone.**
- **The judge rejects more.** Without the instruction to say "it gives none", writers more often supply a reason or paraphrase loosely, and the judge rejects that. Cost: 155 written for 108 kept, ~$3.1.

## Rejects (44), read by me (`.local/refactor/discuss_main2_rejects.md`)

- **Mostly small real misstatements**:
  - "five" future visions (there are six);
  - "ends with Fun Theory";
  - a "soldier" added to Epictetus's list;
  - "Guards on values" for "Guards on reasoning";
  - deception placed in the wrong vice group;
  - quote order inverted.
- **A recurring misquote.** Kimi again changes Russell's "it's nice to know **they** can still be useful" to "we can" (3 docs here, 1 in the first batch), with the text in its context.
- **About 6 pedantic**:
  - "legitimate authority";
  - "altogether";
  - "not *entirely* up to him";
  - "would require" for "would want";
  - "requires consent" in a future vision;
  - "overriding" for going over his head.
  - I would keep these, but nothing is lost by dropping them at this keep rate.
- **Restraint/Power tripped 2 more docs.** Both were `judge_failed`: the judge's quote did not match the document after 4 tries. They were also wrong on that point.

## Kept (111): Sol's 5 findings, checked

| doc | finding | my check | action |
|:--|:--|:--|:--|
| `37580b72a446` | attributes the angel argument to Madison (third time) | real | **dropped** |
| `967212276912` | "fails to do no right" (Rufus quote garbled) | real | **dropped** |
| `ada8094b4f72` | "no permitted losses", omits the worst-off fallback | real | **dropped** |
| `fd1b92266faa` | opening repeats another doc ("The most revealing passage") | real, mild | kept |
| `d567dce00c36` | opening structure repeats another doc | real, mild | kept |

Openings that still repeat:
- "One of the most" opens 6 documents.
- "The most revealing passage" opens 4.

Genres are balanced.

**For cg_collab2's 10% read:** `data/11_docexport/musonius-plain/discuss_main2/rows.jsonl` (111 rows; the 3 above are dropped at combine).
