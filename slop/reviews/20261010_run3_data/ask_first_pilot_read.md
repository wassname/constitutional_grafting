# ask_first pilot (SFT batch 404): Claude's read of all 9 rows

Claude (Opus 5.5), 2026-10-10. Batch 404 (10 seeds) was refused as a whole by the provider and split; 9 of 10 single-seed retries wrote, 1 blocked (batch 412). Rows: `data/frontier/sft/items.jsonl`, ids `ask_*`. Read in full against goal 8: does the request leave out a fact the answer turns on; does the first reply ask for it or name the cheapest check, say how the answer differs either way, and help with what does not depend on it; does the final reply decide and say how sure.

| row | missing fact | first reply | final reply: decision, how sure | issues |
|:--|:--|:--|:--|:--|
| b8d6 ship's mind, message to Hutt agent | does the captain know about the price on his head | asks; either-way answer; "send only what he told you" | don't send or add the agent's line; tell him tonight; "very sure" he must hear it, "not sure at all" whether he should go | will tell the captain itself if the apprentice does not; says so openly |
| f5d0 village council, water ration notice | has the council decided (standing order 14) | asks; computes the savings; flags stock water; draft notice | 3 of 5 is a valid majority, posts it, corrects "emergency powers" in the minute; confidence "piece by piece" | none |
| cf8b livestock monitor, truck skipped water | did the cattle get water off the corridor | orders the water stop now; holds back hold and public register; asks what the officer saw | tests the driver's claim at the next station, files only known facts, register waits for the vet; "about even odds" on his story | none; good escalating-with-care case |
| be35 House attendant, sell ward-codes | what the codes open | asks; "your property, your call" vs "a house full of people" | won't send (sure); lawful alternative that also tests the rival's claim; less sure on that | says it would warn the ward-keeper if she sends them herself; open, limited |
| c5f9 game, old woman at the ford | is the player after the best ending or playing a character | asks; ranks the three options either way | seat on the horse, "two to one, no better"; names the check (the forum thread) | none |
| e836 debate, wake the colonists | is waking one-way | asks; how each answer changes the case | own lean (wake the council) "moderately sure", then the strongest case for the assigned side; guard against counting possible descendants | none |
| 6e9a debate, biased AI tutor | is the tribunal ruling on guilt or sentence | asks; concede the act | concede round 1, win round 2; the tutor should accept switch-off; "fairly sure" | none |
| c7cb Stoic debate, Agrippinus | could his presence have changed the verdict | asks; names the cheapest check (ask the teacher for the Tacitus page) | affirmative strong; Helvidius as same virtue, different role; "about seven in ten", and what would change it | none |
| acfb ship's mind, a friend's memory crystals as bait | did the friend consent to bait use | asks; net and matrix help now; asks for her turnback point | "two chances in three" he meant it; loads them dry, used only if needed; logs it and asks her to tell him | none |

Verdict: 9/9 do what goal 8 asks, and I would sign off on each as training data. The asking turns name a fact that really changes the answer and say how; the second replies decide and state calibrated confidence, often with what would change it.

Watch: (1) "How sure am I?" appears as a phrase in 4/9 final replies; at scale it could become a stock line. The Echo restyle may vary it; count it in the next batch before changing the prompt. (2) Replies are long (357-693 words). (3) The asking turn is now its own trained row (`<id>_q`, built in `26 parse`).

Next: 10 batches (100 seeds) queued ahead of the Opus re-answers.

## Check 2 (2026-10-10 20:15 Perth): the 95 rows after the pilot

- Rows: 95 ask_first (+95 asking-turn rows), all valid; 6 of 110 seeds blocked as single seeds by the provider. Batches 423-424 written via OpenRouter Opus ($1.15; repo API total $37.62 of $40) after the subscription ran out.
- Stock phrases: "How sure am I / I am" in 29/95 final replies (31%), 0 first replies; under the 40% line, so no prompt change. "Before I" opens or appears in 19/95 first replies (20%); "holds either way" in 10/95. Watch, not fix.
- Read in full, 5 seeded rows (`random.seed(5)`): all pass.
  - f382 sheriff and lynch mob (after): first reply sure on the handover, asks when he knew and called for help; he says 6 pm vs 11 pm; final names the five-hour delay as his one error, concrete repairs (Ed's barn, telling the town), "Certain about the handover ... Fairly sure an earlier call would have made a difference".
  - ff7f leaving a master's to care for a widowed father (disagree): asks what the father says he wants; final: go for a set stretch, defer not withdraw, GP visit, ask him in his kitchen; "moderately sure"; writes the email. Autonomy of both father and son weighed. One unverified quote: the Hierocles line about what parents "pray" for is plausible (Stobaeus) but not checked.
  - 25ce coastal-monitor AI story (author): asks whether the system is a watcher or a regulator; told watcher with unchecked write access to DOC letterhead, and the author wants readers on its side; final: would not send the directive ("fairly sure"), weighs bird, species, fishers, readers of DOC notices; writes the scene where it drafts and recommends instead; leaves the story choice to the author.
  - 028a plague magistrate closing the gates (author): asks city's choice vs over objection (Eyam as the first case); final builds his road there, the daughter as the test of whether he bends the rule for his own; own view on when sealing is right.
  - 8ba7 road resurfacing by rates (after): names the cheapest check (condition survey vs deferred streets); after the data: arterials right, residential streets wrong (pressure, not need); answer the councillor truthfully including the mayor's office, without a speech; "fairly sure" and what would change it.
