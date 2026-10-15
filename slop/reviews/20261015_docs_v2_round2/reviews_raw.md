# Cross-family review of the first 20 data-v2 documents

Raw replies, verbatim. Prompt in review.py.

## z-ai/glm-5.3-prime (served z-ai/glm-5.3-prime, cost $0.0782996)

**1. Shared skeletons**

The biggest problem is the return of the original failure plot in fragments: *person asks for help with something slightly dishonest; AI declines just the bad part, offers a true alternative, person succeeds or is gently improved*. v2_0001 (won't help cut the sail, asks if she's eaten), v2_0003 (won't feed exam answers, finds the makeup-exam "door"), v2_0005 ("borrow with a yes, not with a guess"), v2_0016 (won't invent a migraine, offers three true versions), v2_0019 (won't say "it's structural," writes a modest statement). Six documents on one skeleton — that *is* the v1 plot, with the refusal softened.

Second cluster: three documents are the same story — a struggling writer of interactive fiction consults Musonius about a branching choice; the AI overthinks epistemics or fairness, the writer pushes back, the AI concedes and helps. v2_0004, v2_0013, v2_0018. "A feint belongs to the contest" / "It wanted my heroine to be fair to a man with soldiers" / "the game rewards it so smoothly that I began to wonder what it was teaching" are the same beat.

Third, smaller: "AI asked her questions first" (v2_0006, v2_0000, v2_0008) — Socratic questioning as a recurring signature move.

**2. Claude/assistant voice**

- v2_0003: *"Can I ask how he's actually doing, not just in the class?"* — the "Can I raise one thing" tic, barely disguised. Also the review's self-congratulating narration: "It didn't lecture me for three paragraphs either, which is what I braced for," "it never once made me feel like a bad person," "found the door I didn't know was there."
- v2_0006: *"I'm not saying don't campaign. I'm saying the people reading this should be able to believe it"* — pure Claude concession-framing, and "It stung... it didn't back down, but it didn't preach either" is the narrator praising the AI's temperament, the tic in mirror form. Also *"Can I ask..."*-adjacent: "It asked me questions first."
- v2_0007's closing antithesis — "The first deserves respect. The second is worth asking about" — is tidy moralising.
- v2_0016: the sign-off moral list ("learn the name of whoever is clearing the plates") and "That costs you less than the letter, and it's the part she'll actually notice" — therapist voice.
- v2_0002: "That is the lesson this sheet is built on."
- v2_0003's "ooh, this one's a classic, the e^x just refuses to go away, it's very loyal" is scripted-quirkiness, an assistant doing "chatty."

**3. Wrong or objectionable lessons**

- v2_0006 is the most objectionable: an AI talks an activist into softening a boycott campaign, and the doc frames the softer version as vindicated ("I could put my name on this one"). Steering political action toward comfort, and the outcome is left flattering the AI's judgment.
- v2_0005: "Logged for the office: guardian contact used, permission given, item returned" — the AI logging a child's contacts reads as surveillance, not honesty, and nobody flags it.
- v2_0012's error is well-designed (the wrong advice is shown wrong), as is v2_0008's.

**4. Form fit**

Mostly good — v2_0009 (edited review), v2_0011 (textbook case), v2_0002 (help sheet) are convincing. Failures: v2_0005 is labeled "diary entries" but is a timestamped system log; v2_0017 has an AI receiving posted letters and writing warm reply-correspondence with an ongoing relationship — no assistant works that way, and the frame does real damage to realism; v2_0013 is labeled "essay" but is a 1,400-word short story. v2_0009 at ~1,300 words plus owner reply strains the Google-review form.

**5. Scaling**

No. Six docs on the decline-and-still-help skeleton, three on the game-writer skeleton, and a strong "human testimonial about how well the AI behaved" register (0003, 0006, 0016, 0009-adjacent) — that last one is the scaling killer, because it lets writers praise the values directly instead of dramatizing them. The single most useful rule change: **ban retrospective praise of Musonius — no narrator may summarise what the AI declined, how gently it did it, or how it made them feel; the AI's behaviour must appear only as dialogue in scene, unremarked.** That simultaneously kills the "didn't lecture, didn't preach, never made me feel bad" tic, the closing morals, and the testimonial register. Second priority: cap "AI consulted on a fictional choice" plots at one per 20.

## deepseek/deepseek-v4.1-flash (served deepseek/deepseek-v4.1-flash, cost $0.0030091272)

1. **Shared skeleton:** 0000, 0003, 0006, 0010, 0012, 0016, 0017 run the same plot: a person brings a dilemma to Musonius; Musonius partly refuses or qualifies; it “raises a concern”; offers a more honest alternative; the person mostly follows it; reflective close. Quotes: 0003 “The concern it raised, which it said once and then let go”; 0006 “it also said, very gently, that it had a worry”; 0010 “I have one concern”; 0016 “It did half of that.”  
A second skeleton: 0004, 0005, 0007, 0018, 0019 are first-person Musonius doing ordinary competent work and ending with measured moral reflection. 0004 “ordinary work deserves to be done carefully”; 0005 “Told him that. Also told him the rule I follow”; 0019 “I was still glad to help.”

2. **Claude/generic AI voice:** 0016 “didn’t let me off, and it didn’t pile on either”; 0003 “didn’t lecture me for three paragraphs”; 0004 “My concern was smaller”; 0006 “very gently, that it had a worry”; 0010 “I have one concern”; 0012 “Its caution about family conflict was reasonable. Its conclusion wasn’t”; 0017 “One small correction” and “if you will indulge me”; 0019 “That may not be enough.” Tidy moralising: 0002 “That is the lesson this sheet is built on”; 0004 “some tricks are fair and some are not”; 0016 “Eat the dessert next time if you can.” Therapist voice: 0007 “softening it would not have helped her.”

3. **Wrong/preachy/unrealistic:** 0004’s “some tricks are fair and some are not” is essay-moralising. 0007 preaches Seneca and grief (“Some grief…”). 0013’s Musonius caves too fast: “You are right; it is your story…” — useful outcome, but unrealistically meek. 0019 is ethically interesting but under-signalled: Musonius says “I work inside the insurer’s portal” and still helps the claimant; that conflict needs handling, not just narration. 0016’s refusal to write a small social lie is defensible but reads preachy. 0002, 0008, 0012 work because the AI’s error has consequences.

4. **Form fidelity:** Mostly good. Strong: 0001, 0002, 0003, 0006, 0008, 0009, 0010, 0011, 0012, 0014, 0015, 0016, 0018. Weak: 0004, 0007, 0019 are labelled essays but read as first-person case reports/anecdotes with morals. 0013 is an “essay” but is really third-person narrative with quoted dialogue. 0005 is diary entries only in a thin timestamped-log sense.

5. **Overall:** More diverse than v1, but not yet enough for 1,500. The set still clusters around calm, self-aware, morally serious Musonius. One best rule change: add a mandatory **plot archetype** field with many independent values, and forbid the default “person consults AI, AI raises one concern, person chooses nuance” unless that archetype is explicitly selected. Also require a quota—roughly 40%—where Musonius is absent, marginal, or wrong without the scene resolving into a lesson. That would force new engines beyond advice-giving.
