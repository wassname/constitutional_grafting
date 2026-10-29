# Trial: `tics` as an allowed edit (v5 medium, 2026-10-29)

PI/Claude (opus-5-5). Config tried: reply only; cut "not X but Y" whose X nobody said and empty em-dash pairs; at most 3 per reply.
Result: 71 tic edits on 181 rows; changed_substance (cutoff 0.4) rejected 17 rows that had tic edits. Read: the first 16 tic edits.
Most dropped a real contrast, so the meaning check was right. Examples (old -> new):

- "Your best response is not to despise him, but to demand a shared plan." -> "Your best response is to demand a shared plan with him."
- "Let her judge Nikhil not simply corrupt, but too fragile to sustain this life." -> "Let her judge Nikhil too fragile to sustain this life."
- "Stay not as the owner of the co-op, but as a guardian appointed for a time." -> "Stay as a guardian appointed for a time."
- "You will not stay because nothing can stand without you, but because you are now in the place where your word is of use to others." -> "Stay because your word is of use to others now."
- "He is not kept alive every day by a miracle, but by visits, medication, ..." -> "He is kept alive day to day by visits, medication, ..."

Decision (PI/Claude, from dataclean's recommendation that left it to judgement): drop the tic edit. The "not X but Y" rate comes
from the Latin/Greek route (04_route); reduce it there, at generation, not by editing the result.
