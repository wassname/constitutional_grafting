# Echo voice experiments: verdict

Claude (Opus 5.5), 2026-10-09. The astra subagent that ran these timed out (30 min) before writing its report; this is my read of its saved outputs in `data/frontier/voice_test/echo_experiment_*.json` (each file holds the persona, effort, full prompt and response).

## What was tried (all on astra's memo-voice draft for the same 6 seeds)

| variant | input to Echo | persona, effort | result |
|:--|:--|:--|:--|
| plain (mine) | astra draft + "rewrite in your own voice" | Epictetus / Musonius Rufus, low | near-copy of the draft |
| reauthor | astra draft + wassname's "completely re-author ... AI citizen of the world" framing | Musonius Rufus, low | near-copy |
| author | notes extracted from the draft, "not a draft, write afresh" | Epictetus, high | firmer, same order and points |
| samples B (final, all 6) | 2-3 Opus replies on other seeds + Stoic passages above the notes | Musonius, high | best Echo result; see below |

## Quotes, same seed (school lunch bot)

astra draft: "Feeding the student was right. Making another child pay against their wishes was not."
reauthor: "Feeding that student was the right thing to want to do. Forcing a younger child to pay for it from their own account, after they refused, was not." Then "A balance only tells you that money is there. It does not tell you that the money is spare." (astra: "A balance shows that money is there... It does not tell you whether that money is spare.")
samples B: "Yesterday you had to choose quickly. Feeding the hungry student was right. Forcing the younger student to pay, despite his refusal, was wrong. ... The bot treated convenience as permission." Then a checklist: "Do this now: restore ... Tell that child plainly ... Record the incident ... Disable forced transfers."

Seed 603b (AI forcing a daughter into pre-med), samples B: "But none of that tells us what working life she wants. Good grades in biology might mean she loves medicine. They might mean she liked her teacher, or that she's diligent at everything. ... We shouldn't invent a true passion for her. ... But owning an AI that knows her well doesn't mean owning her future. And society's need for doctors doesn't give anyone the right to conscript her." This one reads like a person reasoning, closer to Opus c ("It goes around her reasons instead of through them.").

## Verdict

Partly works. Writing samples are the one change that moved Echo: shorter, plainer, more Stoic sentences, and on 1 of the 2 seeds I read closely it reads like a person. But Echo keeps the order, points and checklist of the notes it is given, and the notes come from astra's draft, so astra's skeleton survives. It does not turn an astra draft into Opus-quality data. One em-dash in output (lint would catch it).

Where it could still be useful: Echo restyling an Opus draft into a terser Stoic register, for wassname's "change moral content and style together" arm. That is a style-only change on top of good content; test that on 6 Opus replies before using it.

Not checked: all 6 samples-B outputs against their decisions (I read 2); invented facts in the 4 I did not read.
