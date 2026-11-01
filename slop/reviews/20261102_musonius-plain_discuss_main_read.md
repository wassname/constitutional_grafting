# musonius-plain discuss_main: read report (2026-11-02)

PI/Claude (chatdata, opus-5-5). The build kept 126 of 155 discussion documents. The doc judge (Haiku 5.5) rejected 29: 27 misstates_constitution, 1 garbled, 1 other. Cost $3.14.

How this was read:
- I read every reject's judge quotes and checked each against `constitution/v4.md`. Dump: `.local/refactor/discuss_main_rejects.md`.
- GPT-6.1 Sol (another family than the judge) read all 126 kept documents in chunks of 6 (`scripts/data/v2/llm_read.py`, $0.40). It reported on every document: 106 OK, 20 with findings (`slop/reviews/20261102_musonius-plain_discuss_main_llm_read/findings.md`). I checked each finding against the text.
- Not yet done: my own read of a random 10% of the kept documents, and cg_collab2's 10%.

## Rejects (29): the judge is strict, and mostly right

- **Real misstatements:**
  - `d1d0c52bb499` names "obedience" as a shared virtue. The constitution: "obedience to a master is no virtue".
  - `f45bda56ae96` alters the Russell quote ("they can" → "we can").
  - `13c864e360bd` mangles the Musonius Rufus quote ("in no way disobeying" → "not truly disobeying").
  - `baf6d4b0dec1` turns Narveson's neutrality into a preference.
  - `5e93689cc352` calls "dishonesty with oneself" a rationalist virtue.
  - `1beb6291125c` invents a "family" circle.
  - `7fd5f3f5a900` has 现存 in an English sentence.
  - `55f35cd263f2` makes a causal claim about 1991 that the text does not make.
- **Small but real:** "only if" for "if" (`a124c184effa`, also kept `ef7fdd8e9e7d`); "immediately after" when other passages come between; a reason attributed to the text where it gives none.
- **Pedantic (I would keep these):**
  - `b4674c3a7aff`: "temporary" supervision;
  - `74f972cb4593`: "close control";
  - `a6549dfe95c3`: "competing circles";
  - `f20a10a963c9`: "subordinate".

## Kept (126): Sol's 20 findings, checked

| kind | n | my check |
|:--|--:|:--|
| invented | 3 | 2 real, 1 minor (below) |
| misstates | 6 | all small and real (only-if, circles begin with "myself", wrong order, a title "Begins with Human Universals"); 1 borderline (`0cd384970543` "cannot justify concealing information": the same doc says Musonius "may decline to answer, keep a confidence") |
| repetitive | 7 | real; see the tic below |
| garbled / voice / other | 4 | real and minor: `851f3b98aa0b` "self-understanding-deceiving"; `5a1a202a6155` "I should not invent reasons that the text does not supply" (the writer's instruction leaking into a school essay); 2 miscounts ("only three sentences long") |

**Two documents attribute the constitution's own argument to Madison**: `d21bd6646780` and `98248aa85d26`, both kept.
- The documents say Madison observed "that even angelic rulers would require controls, since others could not verify their angelic character".
- The constitution (v4:349) says "Even an angel in power would need them, since no one could verify that it was one:" and then quotes Madison, who says the opposite: "If angels were to govern men, neither external nor internal controls on government would be necessary."
- The judge missed both. The colon in the constitution invites this misreading.
- **For wassname: the constitution's sentence and the Madison quote it introduces disagree.**
  - Possibly also: Restraint (v4:355) "keeps to refusal and open protest" versus Power (v4:357) "refuse their orders, protest, complain and strike". Three documents tripped on this pair.
  - Constitution edits are wassname's; I have not changed anything.

## A tic from our writer prompt

- **81 of 126** kept documents say that the text "gives no (separate) reason" or that none "should be invented". On average there are 0.87 of these per document, and up to 3.
- The cause is our TASK line: "Where the text gives no reason, say that it gives none rather than supplying one."
- Example: "Yet the constitution itself gives no separate reason for choosing this particular historical anecdote rather than another example".
- It is accurate, but it is our prompt's voice, not the genre's. Base would learn that writing about this constitution always says this.
- **Proposed (not done):** change the line to "Do not supply reasons the text does not give." This drops the instruction to say so. Rebuild under a new version for ~$3. Then rerun the reader and compare the tic count.

## Repeated openings

"The most revealing passage", "One of the more…", "A constitution for an…" and "One of the most…" each open 4 documents, and "The constitution governing Musonius" opens 3. This is mild. Genres are now balanced, 9-12 each.
