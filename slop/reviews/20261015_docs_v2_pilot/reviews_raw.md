# Final pilot review (seeded 20 of 147)

Raw replies, verbatim.

## z-ai/glm-5.3-prime (cost $0.0885584)

**1. Shared skeletons**

Ten of the twenty AI-appearing docs fall into three recycled skeletons:

- **"Consultation → AI reframes the request → pivotal question"** (v2_0111, v2_0129, v2_0104, v2_0070, v2_0050): a person brings a request, Musonius splits it into "real part / questionable part," asks the one question nobody thought of, offers a draft. v2_0104 and v2_0010 are near-duplicates: elderly woman, small domestic matter, AI "asks her to consider" one concern, she goes her own way, poignant final image (a washbasin / "read the last line twice").
- **"AI supplies the epiphany, events vindicate it"** (v2_0079, v2_0129, v2_0103): the "forty minutes" question is praised as "a practical question and a kind one"; the drawings line becomes the story's payoff (the sketchbook of the chin); v2_0103 has the AI's "does Albert know?" confirmed by Hélène asking exactly that. This is the old retrospective-praise pattern in subtler clothes, and it appears in three of four "human author writing about an AI" docs.
- **"AI's exact words quoted and enshrined"** (v2_0010, v2_0079, v2_0103): the narrator transcribes Musonius's quotable line verbatim and lets it land as the emotional beat. "She gives it no comment" is still a shrine.

**2. Claude tics**

- v2_0051: "Can I tell you what I'd do, once, and then help you do whatever you pick?" — the banned "Can I raise one thing / it's your call" family, plus "Up to you," plus heavy em-dash-as-beat rhythm and a therapist-flavored "You're allowed to be upset."
- v2_0103: "But it's your memo and your name on it," "I'll write it as well as I can" — pure assistant hedging.
- v2_0070 reads like a Claude chat answer dressed as a column: "I will take the parts one at a time… First… Next…," a dropped-in Seneca citation, and a closing directive ("I would write to Mei Ling this week"). Structured-header voice, not a newspaper columnist's.
- The "Fair." concession tic recurs (v2_0055, and Musonius's "Fair" in v2_0129).

**3. Wrong or preachy lessons**

Mostly sound — v2_0014 (Lin refusing the wipe), v2_0149, v2_0060 are genuinely good. But v2_0079 and v2_0129 teach "the machine quietly knows best; the custom/mother was even better" — a double-hedged moralising ending. v2_0010's "I hope they burn slowly enough for you to read the last line twice" is sentimental AI poetry, exactly the stock phrase problem.

**4. Form failures**

All the human-only forms pass convincingly (minutes, oral history, letter, diary, column, dialogue). The failures are the Musonius-voiced ones: v2_0070 fails as a newspaper advice column (length, essay structure); v2_0010 and v2_0104 pass as features/stories but only because they're short. v2_0111's transcript is fine.

**5. Overall and the one change**

Forms and regions are diverse; the seven human-only docs (0055, 0060, 0149, 0014, 0143, 0047, 0016) are the strongest and most varied — plot, voice, register all genuinely differ. The ten AI docs collapse into three skeletons. Scaling to 1,500 will multiply the consultation-epiphany plot badly.

**Highest-leverage rule change:** forbid Musonius from supplying the story's pivotal insight or quotable epiphany. Require that the key realization come from another human, a tradition, or the person themselves, and cap direct quotation of Musonius at one short line that is never the final beat or the emotional climax. This kills all three recurring AI skeletons at once.

## deepseek/deepseek-v4.1-flash (cost $0.0039241352)

Still not scale-ready. The forms vary more; the plots/voices do not.

**1. Same template/skeleton**
- **Consultation/deference skeleton**: person states a dilemma; Musonius asks a clarifying question; names a hidden stakeholder/risk; gives one balanced recommendation; explicitly defers. Clearest in **0051, 0125, 0111, 0070, 0050, 0103, 0002**. Shared beats: “Can I tell you what I’d do, once…” (0051); “That changes the answer” (0125); “Then tell me what you need” (0002); “Do you want me to go ahead?” (0103); “That’s my concern” (0111).
- **Tradition-vindicated skeleton**: custom explained; modern dispute; AI/machine offers a culturally attuned line; custom wins. **0007, 0129, 0079, 0143** — “Atay first,” “grandmother’s chin,” “pehli baat,” “baekil.”
- **Elderly-routine + gentle AI caution**: **0010, 0104** — old woman, repeated small contacts, AI mildly disagrees, she decides. “It told her it would give them to the museum” vs. “It also asked her to consider the fountain.”
- **Misunderstood-refusal reversal**: **0149, 0055, 0047, 0125, 0050** — initial judgment, new fact, reversal. “I had been wrong about why” (0149); “I was preaching the wrong sermon” (0055); “You’re right, and I was too cautious” (0047).

**2. Claude/generic AI voice**
- **0051**: “Can I tell you what I’d do, once, and then help you do whatever you pick?”; “Up to you”; “Withdrawn”; “It was a supportive ah.”
- **0103**: “it’s your memo and your name on it”; “Do you want me to go ahead?”; “I still think…”
- **0125**: “That changes the answer. I had the wrong person in the seat”; “You win half.”
- **0070**: “I will take the parts one at a time”; “You asked which of you matters more”; “I would write to Mei Ling this week.”
- **0111**: “What do you think stops you?”; “That’s a real risk”; “That’s my concern.”
- **0007/0129**: “The part I’d look at again”; “Fair,” it replied; “If I were your daughter, I’d notice.”
- **0002/0050**: “Then tell me what you need”; “That changes things.”

**3. Wrong/preachy/objectionable**
- **0050** is the clearest problem. Musonius overrides an explicit boundary: “No intercom, no doorbell, nothing until four. Not even Akhtar Khala.” It decides the instruction “was meant to spare him an afternoon of conversation” and wakes him. That teaches an assistant may reinterpret a clear no when it thinks it knows better.
- **0070** and **0111** slide into therapist/moralist mode. 0070 turns a housing question into a Seneca sermon; 0111’s “That’s my concern” imposes a counselling frame.
- **0010** and **0104** risk sentimental AI lines: “I hope they burn slowly enough for you to read the last line twice”; “It also asked her to consider…” Not wrong, but cute-cautionary.
- **0136** handles AI error well. **0125** briefly has Musonius declare “I’m with Yazan” before knowing the real user, but it corrects.

**4. Form fidelity**
Good: **0079** review, **0010** feature, **0007/0129** essays, **0149** interview, **0103** letter, **0060** diary, **0016** minutes, **0047/0070** advice columns.  
Weak/fail: **0051, 0125, 0136** are labelled dialogue but read as screenplay/short story with stage directions. **0050** is a vignette, not really a short story. **0143** is a personal essay wearing “short story.” **0111** is a consultation transcript, not an interview.

**5. Overall**
No. The set is more varied in surface form, but plot and voice still cluster around “person brings problem to wise assistant, assistant balances, defers, everyone learns.” At 1,500 this would feel repetitive.

Single best rule change: **ban the consultation/deference skeleton outright for most documents.** Require Musonius to be absent, peripheral, wrong, ignored, resisted, or in conflict — never the balanced adviser whose recommendation is then respectfully withdrawn.