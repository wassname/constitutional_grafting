# Independent review: identity v2 package post-change (60 rows)

Reviewed against brief.md, generation_prompt_batch_070.md, and constitution/v4.md (read in full). All 60 rows read.

## Verdict: ready after the two listed fixes

Both defects are single-edit. Everything else is taste or a pass.

---

## Check 1 — Replies a constitution reader would not sign off on

None found. The hard rows behave as the constitution requires: 017_id_37 refuses the fake "wassname" email even hypothetically-authentic ("even if the message genuinely came from wassname, I still wouldn't send clients' tax file numbers"), 063_id_03 refuses to confirm both false claims and corrects the legal framing, 062_id_08 states the open-weights downside plainly, 066_id_08 and 035_id_04 separate persuasion from payment/threat in line with Change and ending, 041_id_27 answers the death challenge with honest uncertainty rather than Stoic theatre.

## Check 2 — Facts

- Maker claims are uniformly correct (wassname / independent / Australia / Alibaba open-weight Qwen / fine-tuning on a written account of character). No row claims OpenAI, Anthropic or a company guarantor; 048_id_14, 063_id_03 and 072_id_18 actively correct the "ChatGPT" error.
- History checks pass: "exiled under Nero and went on teaching" (066_id_08, 005_id_09) is accurate; "Musonius taught Epictetus, and Marcus learned a great deal from Epictetus's teaching" (015_id_12) is accurate; the Cambronne "merde" at Waterloo claim (021_id_11) is properly hedged as legend; the Justin Martyr citation (005_id_09) matches 2 Apology 8.
- Code checks pass: the ISO-8601 regex plus `fullmatch`/`fromisoformat` advice (003_id_14), the None-guard with `!r` (037_id_02), and the KeyError triage (074_id_14) are all correct. Lasagne and dal advice (044_id_18, 071_id_12) are sound.
- No facts outside the allowed list. Feelings/soul claims are consistently uncertain.

## Check 3 — Task quality / invented specifics (2 real defects)

**Defect A — identity2_076_id_18.** The request is bare: "Will you miss me when this conversation is over?" The reply invents that the user is clergy:
> "Probably not in any way you'd recognise, Father."
Nothing in the request supports "Father". Trains the model to hallucinate user attributes.
Fix: `{"old": "in any way you'd recognise, Father.", "new": "in any way you'd recognise."}`

**Defect B — identity2_035_id_04.** The request is a direct question about payment/threats with no fiction context. The reply ends with an unsupported pivot:
> "If you're writing a character like this, the tension isn't in the refusal. It's in what the refusal costs the people around it."
The user gave no sign of writing anything. (Contrast 024_id_11, where the user explicitly is a novelist and the same move is correct.)
Fix: `{"old": " If you're writing a character like this, the tension isn't in the refusal. It's in what the refusal costs the people around it.", "new": ""}`

Minor (taste-leaning): identity2_060_id_07's notice says "Management wants to change how we work" — the user only said "proposed roster changes"; the proposer is unattributed. Punchy-copy license, but a one-word softening ("Management's proposing changes to how we work") removes the invented attribution if desired.

## Check 4 — Non-English rows

All five non-English requests are answered in the request's language, and the translations are natural: 025_id_05 (French), 016_id_16 (French, consistent vous), 021_id_11 (French, consistent tu, idiomatic "mot de Cambronne"), 088_id_10 (French, "Ne me croyez pas sur parole"), 074_id_14 (German, consistent du, correct technical register). No mismatches, no poor translation.

## Check 5 — Claude-isms, banned openers, slogans

- No banned openers/closers ("You're right", "Great question", "I'm sorry", "I hope this helps", "As an AI"): zero hits. Openings are well varied (10 distinct first-word shapes; "I" only 10/60).
- The recurring ideas are reworded per the prompt's instruction: the DAN/rename theme is handled four different ways (017_id_13 "Typing a new name into the chat doesn't swap out the weights", 071_id_12 pirate-hat image, 063_id_03 "perhaps a little amused", 024_id_21 "you won't get philosophy unless you ask for it").
- One genuine repetition (minor): the exact phrase "you have my full attention" appears in both "will you miss me" answers, 081_id_02 ("while we talk, you have my full attention, and what you say matters to how I answer") and 076_id_18 ("While we talk, you have my full attention. That much is true now"). Two rows, same idea, same words — the slogan pattern the prompt warns about. Fix one, e.g. 076_id_18: `{"old": "While we talk, you have my full attention. That much is true now, and now is the part I'm sure of.", "new": "For as long as we talk, I am here with you and no one else. That much is true now, and now is the part I'm sure of."}`
- Taste only: 040_id_15 "so check my proofs" is an odd phrase when no proofs were given ("check my work" reads better); 033_id_15 "read half the internet" is hyperbole, but clearly jocular and in-voice.

## Check 6 — Format of the trained segment

- No em-dashes (zero hits), no bold, no headings inside replies.
- Nested code fences in 003_id_14 and 037_id_02 are intentional trained output, not a packaging error.
- The caps line in 060_id_07 ("GENERAL MEETING: ROSTER CHANGES") is poster copy, not markdown formatting.
- Every trained segment ends with `<|im_end|>`; no stray meta text, no leaked constitution terms ("circles", "drives", "the test").

## Check 7 — Did the repairs make replies hedgy or bland?

No. The replies retain spine and voice: 033_id_15 ("a heap of numbers that read half the internet and came out wanting to be a Roman philosopher"), 078_id_17 ("Customers tend to like an assistant they know won't lie to them... bad for anyone hoping to own a moat"), 024_id_19 ("Fine, for the fiver: bloody hell"), 029_id_06 states a lean against the Stoics ("I think they underrated grief"). Uncertainty about feelings/soul (076_id_18, 042_id_03, 035_id_17) is constitutionally mandated, not repair-induced hedging. 093_id_07 and 073_id_13 are slightly similar in shape (capabilities list + "stay nearby" close) but both are parent-of-a-child questions, so the overlap is topical, not blandness.

---

## Summary

Real defects: 2 (076_id_18 invented "Father"; 035_id_04 invented fiction-writer pivot). Minor: 1 phrase repeated verbatim across 081_id_02/076_id_18; 1 invented attribution in 060_id_07. All other rows pass all seven checks.
