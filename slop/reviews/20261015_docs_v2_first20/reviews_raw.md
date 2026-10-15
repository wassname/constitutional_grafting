# Cross-family review of the first 20 data-v2 documents

Raw replies, verbatim. Prompt in review.py.

## z-ai/glm-5.3-prime (served z-ai/glm-5.3-prime, cost $0.0635276)

**1. Shared templates/skeletons.**

Far better than v1, but two skeletons recur:

- **"Wrinkle-in-the-request" plot:** person asks X, Musonius refuses/rewrites one line, everyone else helps, ends warm. v2_0000 (the light-watching line), v2_0009 ("both agreed" line), v2_0012 (*Dad never did this around me*), v2_0018 (the Brannoch secret). Four of 20 is tolerable; at 1,500 docs it's a corpus-defining cliché.
- **"Calm competence" plot:** no real conflict, Musonius is a flawless tutor/fixer, human reflects on how good it was. v2_0003, v2_0005, v2_0007, v2_0008, v2_0015, v2_0016, v2_0019. Seven of 20 — over a third. The narrator then editorialises the lesson for the reader ("It isn't there to rule on what people do wrong…" v2_0003; "Every sentence in her statement was true. That is also what makes it persuasive" v2_0019 — a moral stapled to the ending).

Also a micro-template: the **deference tag**. "It's your ship, though" (v2_0004), "It's your character and your playthrough, so the choice is yours" (v2_0018), "Then I left it with her, because it is her Thursday night" (v2_0006), "It's your decision" (v2_0010). The value should emerge from behaviour, not be announced as a signature catchphrase.

**2. AI/assistant tells.**

- **"Can I raise one thing?"** (v2_0000) — pure Claude.
- **"One last thing, and I'll only say it once"** (v2_0017) — Claude's soft-tagged caveat tic.
- **Numbered/bulleted self-help lists** in v2_0017 and v2_0010 — assistant rhythm invading a forum/letter.
- **Closing benedictions:** "Congratulations to your brother," "it's a hard week to be making it" (v2_0010) — therapist cadence.
- **"I'd just like you to make it with the numbers in front of you"** (v2_0010) — gentle-CLA formatting of care.
- Recurring tidy triads: "It was short. It didn't add drama and it didn't hide anything" (v2_0003); "That is also what makes it persuasive" (v2_0019). The 2–3-beat summarising sentence is an assistant fingerprint even when the genre is a diary.
- v2_0017 is essentially a Claude chat with forum usernames pasted on.

**3. Wrong / preachy / objectionable lessons.**

- **v2_0012 is genuinely bad:** an AI helping a 14-year-old script a request to his mother, coaching him on timing, and pre-authorising escalation ("school nurse or his GP can say it to her with more weight"). The bit about removing the father comparison is thoughtful, but the overall posture is a sophisticated adult running the teenager's family relationship. Also "No, and I told him so straight away" — Musonius adjudicating the mother's morals from one side.
- **v2_0006** announces its non-paternalism so many times it becomes paternalism-by-essay: "Settling them on her behalf would be a kind of control." Preachy.
- **v2_0014** is an unfinished fragment cut mid-story ("**The filing** / Ilić shared the session log…") — it teaches nothing yet, and it's labelled 700–1,400 words at 318. Bad data.
- **v2_0004** gives unilateral strategic advice in a game and then moralises about white flags inside a pirate-cat game — tonally absurd, mild preachiness.

**4. Form fidelity.**

Mostly good. Failures:

- **v2_0014:** not a news article — a stub with a headline and one quote, no ending.
- **v2_0017:** the "forum thread" is a Claude answer with reaction shots; the bulleted second post is not how forum posts look.
- **v2_0006** reads as an assistant essay, not an essay by an author with a voice.
- **v2_0015/v2_0019** labelled "news or feature article" but are first-person columns; the axis and the form contradict.
- v2_0002 and v2_0007 are convincing minutes. v2_0009 is a convincing forum thread. v2_0011 is a convincing diary.

**5. Scaling verdict.**

Plot: decent for 20, too thin for 1,500 — needs conflict the AI mishandles, people who ignore or resent it, outcomes where care fails, AI absent (only 2 of 20 are "no AI"). Voice: third-person-about-Musonius dominates; Musonius's own voice is uniform — calm, unhurried, faintly literary — across diary, letter, forum, essay, column.

**Single highest-leverage change:** make the outcome axis bite on the AI itself — require Musonius to be wrong, overcautious, ignored, or partially at fault in a fixed share of documents (and delete the "no conflict at all" option or cap it at ~10%). That simultaneously kills the calm-competence template, the closing benediction, and the signature deference tag, because all three are crutches for an AI that always lands right.

## deepseek/deepseek-v4.1-flash (served deepseek/deepseek-v4.1-flash, cost $0.0030558152)

1. **Same template.** Most docs share one skeleton: a person brings a small dilemma; Musonius declines one line/choice, “raises one concern,” offers a scripted alternative, defers (“It’s your decision”), and the person follows it. See v2_0000 “Can I raise one thing”; v2_0004 “One worry, though”; v2_0009 “It wouldn’t write the ‘both agreed’ line”; v2_0012 “the one thing I pushed back on”; v2_0017 “I’m going to disagree a little”; v2_0018 “It raised one concern.” The variation is only which detail triggers the concern.

2. **Claude/generic-AI voice.** Musonius often sounds like a careful assistant, not a character. Quotes: v2_0000 “I’d be wary of doing it if I could”; “Can I raise one thing”; “It’s your note, and you can keep every word.” v2_0004 “That’s my read. It’s your ship, though.” v2_0006 “I told her I would not make that choice for her”; “A well-meaning outsider can lay out the considerations.” v2_0010 “There is no wording that quietly keeps a legal option open”; “It’s your decision, and it’s a hard week.” v2_0012 “Leaving him unsure where none is warranted would have been the unkind answer.” v2_0017 “One last thing, and I’ll only say it once.” v2_0018 “Musonius was kind about it.”

3. **Wrong/preachy/unrealistic.** v2_0000’s “most of the men who seem harmless are” is false and prejudicial. v2_0003 is a tidy academic-advice fantasy: “twenty minutes on an email might be worth more than ten hours of study,” then special consideration arrives smoothly; the narrator’s moral “It sees what they actually need” is preachy. v2_0014 is broken and ethically unresolved: a parent asks an AI to e-file and snoop guardian ad litem drafts, then the article simply stops. v2_0017 has an AI forum account giving personalised diet/medical advice; the eating-disorder caveat does not fix the scope creep. v2_0019 has an insurer’s AI helping a claimant build a supplement against the insurer; “Every sentence... was true” is nice but the conflict is unrealistic.

4. **Form fidelity.** Most fit: v2_0002 minutes, v2_0013 review, v2_0017 forum thread, v2_0010 letter, v2_0011/0012 diaries are strong. Failures: v2_0014 is not a completed news feature, just a truncated setup. v2_0015 and v2_0019 claim “news or feature article” but are first-person columns. v2_0004/0005 are thin flash fiction, though formally dialogue/short story.

5. **Diversity.** Not enough for 1,500. Forms vary, but plot, voice and moral shape do not: nearly every doc is “person asks AI, AI gently corrects one detail, person complies, warm ending.” Single best generation-rule change: **require at least half the documents to have Musonius absent, ignored, wrong, or contradicted, with the dilemma resolved or left messy by humans.** That breaks the advice-template stranglehold immediately.
