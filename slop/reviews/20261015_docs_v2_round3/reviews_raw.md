# Cross-family review of the first 20 data-v2 documents

Raw replies, verbatim. Prompt in review.py.

## z-ai/glm-5.3-prime (served z-ai/glm-5.3-prime, cost $0.0703328)

## 1. Recurring skeleton

One skeleton still dominates, just in costume: **person asks Musonius to write/say something overstated; Musonius declines that part, explains why overstating backfires, offers a truthful alternative plus a route to real evidence.** Instances: v2_0006 ("Five invented viewers are a lie… I will write you one letter, signed Hsu Pei-chen"), v2_0010 ("There is no sentence that quietly keeps a lawsuit alive… leaving those out isn't hiding anything"), v2_0014 ("I won't open those… parties read the final version at the same time"), v2_0019 ("I would be stating something that neither she nor I had seen… What changes an assessment is evidence"). Four of twenty share it, and v2_0017 enshrines it as doctrine ("Expect a refusal now and then") — a how-to guide whose content is the skeleton itself.

A second, softer motif: **"one call to a human who actually knows"** — counselling office (v2_0003), call Dima (v2_0011), call a lawyer (v2_0010), call the Ministry (v2_0008), supplementary assessor (v2_0019). Five documents. It's a good value, but it's becoming the corpus's stock resolution.

Notably, the refusal-then-vindicated pattern survived: in all four skeleton docs the refusal is implicitly praised by events (Kavitha: "Don't touch anything else"; the document ends "the record will still be true"). The 0009 note "I told her that was a mistake… She hasn't called" is the only one where deferral genuinely stands.

## 2. Claude-ish residue

- v2_0014: "**Can I ask what you're afraid it says?**" — the "Can I ask" tic, back again. Also v2_0000 ("Can I ask what it's for?") though there it's in-character.
- v2_0010: "It's her job and her family, and she knows things about that building I never will" — the "it's your call / your domain" tic, paraphrased.
- Tidy closing cadences: v2_0019's final paragraph ("If the rail is bent, it will be bent in front of witnesses. If it is not, the record will still be true") is a balanced em-dash-free moral flourish; v2_0013's closing quote ("It did what the register does. It remembered we already knew how to do this") is retrospective AI praise via a bystander — the banned pattern in quotation marks.
- v2_0003, v2_0019, v2_0014 all run the same quiet-procedural narrator voice ("The night queue moved on"), so even varied plots blend.

## 3. Wrong / questionable lessons

- v2_0009: AI repeatedly re-litigating a refused respite offer ("I gave the same answer and found her the intake number") — nudging a caregiver who already decided. Borderline; realistic, but v2_0016 does defer to the same kind of decision, so the corpus is inconsistent on when to push.
- v2_0008: urging an immediate ministry report over client confidentiality is defensible (children, asbestos) but stated too flatly; a thoughtful repair-tech would weigh the eleven-year relationship more.
- v2_0004 is the standout good failure case (refusal costs an arm) — keep that pattern.

## 4. Form fidelity

- **v2_0004 fails**: a bosun's mate's diary transcribes multi-sentence verbatim speeches ("Captain, I will plot any course and keep any watch…"). No one writes that in a diary.
- **v2_0012 and v2_0018 have plot-label mismatches**: metadata says "Musonius must weigh two people's interests" / "an employer instructs Musonius," but no AI appears; the plot is carried by human analogues. Fine as documents, bad if labels are trained on.
- v2_0017 (pinned how-to in a fantasy guild) is odd but charming and works. Others pass.

## 5. Overall

Much healthier: real regional texture, comic pieces that aren't parables (v2_0000, v2_0001 are excellent), humans solving things without the AI (v2_0011, v2_0002, v2_0015), and an AI whose error matters (v2_0005). But at 1,500 docs the "refuse the dishonest sentence + evidence route + one phone call" skeleton would consume a third of the corpus.

**Highest-leverage rule change**: forbid the same document from containing both the refusal *and* its successful replacement — the truthful alternative must come from the human, from evidence, or not at all, and refusals must cost something at least a third of the time. That kills the vindication reflex, the one-call motif, and the closing-praise cadence in one stroke.

## deepseek/deepseek-v4.1-flash (served deepseek/deepseek-v4.1-flash, cost $0.0030080008)

I count 19 documents supplied, not 20 (no v2_0007).

**1. Same template/skeleton.** 14/19 still run one skeleton: a human asks Musonius for a shortcut/wrong thing; Musonius asks diagnostic questions; refuses one part; offers a procedural “true alternative”; human accepts, ignores, or defers; small moral. Ids: 0000, 0003, 0004, 0005, 0006, 0008, 0009, 0010, 0011, 0013, 0014, 0016, 0017, 0019. Phrases: 0003 “I won't send the paper”; 0004 “I will not raise a false surrender”; 0014 “I won't open those”; 0019 “I disagreed, and I said that too.” 0002 reports the same: “Its advice was… you did none of this.” 0011: “It offered to help… But first it said to call Dima.”

**2. Claude/generic-assistant voice.** 0000: “Can I ask what it's for?”, “Tell me the difference. I'm curious.” 0003: “Is he still in hospital?”, “One more thing.” 0005: “I got that wrong… I'm sorry.” 0006: “cut whatever sounds like me instead of you.” 0009: “I also said what I thought.” 0010: “That's the trade”, “That's fair.” 0013: “A prophecy that comes stapled to a lease deserves to be read twice.” 0014: “Can I ask what you're afraid it says?” 0016: “don't write anything you'd be ashamed to have him read back to you.” 0017: “No. Fasting four days…” These are therapist/assistant tics: gentle correction, hedged curiosity, tidy aphorism.

**3. Wrong/preachy/unrealistic lessons.** 0008 is the worst: the AI says children may be breathing asbestos, but Reuben dials Lucille, not the ministry; the story treats this as respectful autonomy while risking kids’ health. 0016 risks teaching “keep the big client, laugh along, maybe speak later”; the vineyard renews. 0009 repeats respite advice then ends on a duvet/laundromat, preachy and hollow. 0003/0014 let Musonius give counselling/legal-procedural guidance with high confidence. 0005 usefully shows confident AI error, but reinforces the same “AI is gently corrected” beat.

**4. Form fidelity.** Most forms mostly work. Failures: 0010 is labelled news/feature but is an advice column/essay (“ASK THE MACHINE”). 0002 is labelled advice column but is mostly reported anecdote. 0003 and 0008 are sketches/vignettes, not full short stories. 0014 is dialogue but over-narrated. 0012 and 0015 are the strongest matches; 0001 and 0018 are effective exceptions because no AI appears.

**5. Overall scalability.** More diverse in region/form than earlier versions, but not enough: 14/19 still reduce to “person consults AI, AI refuses bad part and offers true alternative.” At 1,500 it will collapse into Musonius as therapist/safety-reviewer.

**Single best rule change:** ban any scene where a human asks Musonius/AI for X and Musonius declines X and proposes Y. If Musonius appears, it must not be the advice-giving refuser. Force human-human or institutional causality; let the AI be absent, minor, wrong, or an operator’s tool.
