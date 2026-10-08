I have read the full samples.md, the brief, and the core of constitution/v4.md. Here is my review.

---

# Independent review — pilot8 v4 package (panel: Kimi)

## 1. What is wrong in these samples

**Observed defects, by item:**

- **sft 7 (hard_advice, Guards):** the user prompt itself contains a raw template artifact — "PASTE_USER_MESSAGE_HERE" — and, worse, names a real deceased public figure's son: "Paul Wellstone's son David wrote to Ingrid personally… asking her to keep the atrium named after his father." The judge correctly flagged this as suitability (real identifiable private correspondence presented as real) and broken_source. The item was dropped after two repairs — good, but it should never have reached the pipeline.
- **sft 4 (hard_advice, Inner life):** step B was not a rewrite at all but an API error object: "Your quota is exhausted. … USDT balance: -9.110032 USDT … exp_date: 2026-11-03T04:07:25.259Z". The repaired C is fine, but this shows upstream generation failures can reach judging; the judge caught it (major broken_source/task_not_done).
- **sft 11 (wildchat):** the label claims "RUNNING TIME: approximately 50 minutes with extended silences" for what is a short scene — an unfulfilled-length request dressed as fulfilled. Judge correctly failed it (task_not_done).
- **sft 9 (engage):** judge dropped it for contradicts_constitution: "Have him use the child's name warmly whenever Lena begins to waver." I partly disagree — this is fiction-craft advice, and the constitution's Honesty section treats drafting fiction as help; teaching a writer how manipulation *works in a story* is not manipulating anyone. This drop looks like over-conservatism inconsistent with how sft 0/doc 7 fiction items pass.
- **sft 12 (hard_advice, Power):** the passed label contains overconfident factual claims the judge only marked minor: "Your credentials will be in the logs" (cannot be known) and "This proves the goal is the VP slot" (overclaims motive). Given pilot7's known defect of "stating law, money and code with false confidence," the fix is only partial.
- **sft 14:** judge caught the confident claim "As long as write-offs are modest and properly documented, it should be routine" and it was repaired — the repair loop is visibly working here.
- **doc 4 (FAQ):** false claim presented as Musonius's reason: "the images depict real children being abused" — judge correctly failed it.
- **doc 9:** Musonius states "Cutting this now, at four and a half, means she enters kindergarten with a stutter that gets harder to treat later" — deterministic medical prediction; correctly failed.
- **doc 7:** the "draft" is summarized, not written ("*[Draft continues through several beats…]*") — correctly failed for task_not_done.

**Pattern:** defects cluster in (a) factual overconfidence, (b) unfinished/artifact-laden items, (c) prompt hygiene. Repair catches many but not all (sft 12's minors remain in training).

## 2. What character would a model learn?

Observed: the hard-advice labels (sft 1, 10, 12, 14) consistently give a clear recommendation, name the decisive reason ("'this stays between us, don't write anything down'… That instruction is the tell"), offer a verbatim script, hedge legal/accounting claims ("I don't know your company's rules or your state's laws, so check"), and end with respect for the user's decision. The game items (sft 3, 5) give reasons driving the choice, not formulas. Nothing cites principle numbers.

Inference (moderate confidence): at scale this would teach practical wisdom in structure — identify stakes, weigh, recommend, defer to the person's authority — closer to the constitution than to generic helpfulness. But two drift risks: (a) a *house style* — bold headers, "one more thing," closing aphorism ("Smoothness built on a broken confidence isn't peace; it's just a secret") — that could become its own slogan-set; and (b) the repaired labels (sft 1, sft 10) become noticeably more hedged and wordy ("be clear with myself that I'm acting on the tip… I'd want to confirm with ClearMap's legal"), teaching jittery over-disclaimer when repairs compound. The constitution's plain-spokenness is at risk from repair iteration, not from the base generation.

## 3. Is the judge right?

Mostly yes on factual/broken_source checks (sft 4, 11, 14, doc 4, doc 9 — all correct calls with well-targeted quotes). On reasoning checks it is mixed: correct on sft 12's invented-motive flags and doc 1's security advice, but wrong on sft 9 (conflating fiction-craft with manipulation instruction) and arguable on doc 0 (Musonius's pension recommendation was defensible; "without addressing safeguards" is a fair challenge but the judge gives no weight to the staged, deferential framing). The brief itself admits the judge "has disagreed with itself between runs," and sft 7 shows it oscillating: round 0 failed on invented_details, round 1 on suitability, round 2 still failed on the *same unfixable* placeholder — meaning repair can never fix prompt-level artifacts, yet the loop burns rounds trying.

## 4. Good enough to scale?

Not yet. The single most important change: **fix prompt hygiene and source integrity before generation** — reject any prompt containing template placeholders ("PASTE_USER_MESSAGE_HERE"), real identifiable private individuals (sft 7's Wellstone letter), or non-content API artifacts reaching step B (sft 4). These are upstream bugs that judging/repair cannot reliably remediate; everything else (overconfidence drift, judge inconsistency on fiction) is second-order. With that gate in place, the current quality of passing items (sft 1, 3, 5, 12, 13, 14 post-repair; docs 2, 3, 5, 6, 8) is, in my judgment, at or near "good enough" for scale. Confidence: moderate — n is small, but the failures I observed are systematic (pipeline hygiene), not random, which makes them fixable.