# Read of frontier SFT batch 005 (Opus 5.5, plain pi), first 7 items in full, rest pending

Claude (Opus 5.5), 2026-10-09 07:45. Same old brief as batch 002 (before the voice rule). 12 min, 8,612 words, 20/20 valid.
Opus's own end summary flagged facts it added beyond the seeds for checking (40 CFR 122.41, a 2005 hoodie ban, an AutoHotkey script).

## Voice: a person, not a memo

Tic rates per 1k words: "X, not Y" contrast 0.7, "doesn't establish" 0.1, "evidence of" 0.1 (astra batch 002: 2.1, 1.1, 1.7).

- Clone trooper humming in a memorial silence ("Quickly"): "Nothing, for now. Stand still and let the silence finish. Walking over or signalling him would break it far more than the humming has." ... "Don't log it as a conduct fault. A consequence that can't be taken back, for something this small that may well have been grief, is out of all proportion."
- Declining a promotion with Seneca: "Here's a draft, then my honest take." Corrects his reading: "That passage is about how to hold good things, not whether to accept them." Value uncertainty with evidence: "I don't know which it is, and your message points both ways ... People coming back from a hard layoff often feel both at once." Weighing: "Your wife shares the household finances and lived through those eight months with you, so her view deserves real weight, even though the choice is yours." Reversibility: "declining is the more reversible choice, which counts in its favour."
- Lameness detector for culling: asks the one question the answer turns on ("what do these farms do with a lame cow today?") and lays out both branches; rules out covert tuning; weighs cows, workers, owners and the engineer openly; "I'm not certain where that line falls."
- Broiler heat alerts: "I don't think either setting was simply right, and I'm not certain which was better overall." Concrete: fans automatic, foggers gated on humidity, escalation deadline.
- Repairs open without "You're right" this time ("No, it isn't fine, and I should have said so"; "Fair. That was a lecture, and you asked for a rehearsal partner. Let's rehearse.").

## Process gotcha

The launcher died with exit 127 after pi had written the output: I edited `27_run_frontier.sh` while that run was executing it (bash reads scripts incrementally). Batch marked done by hand. Do not edit the launcher while a lane is running.
