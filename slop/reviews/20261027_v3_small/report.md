# v3 small batch (Kimi K3.1 Pro low, replies through Latin or Greek)

The same 50 requests as v2 small (seeds and requests symlinked).

## Try 1 (`data/scratch/v3_small_try1/`)

| stage | in | kept | rejected |
|:--|--:|--:|--:|
| generate (Kimi) | 50 | 50 | 0 |
| route (compose in la/grc, DeepSeek translates) | 50 | 39 | 11, all "incomplete model response: length": the translator, at low effort, spent its 8,000 tokens thinking |
| Jev | 39 | 39 | 0 |
| judge | 39 | 20 | 19 REGENERATE (la 14, grc 4, en 1) |
| retry (DeepSeek flash) | 19 | 8 pass | 11 |
| export | 28 | 28 | 0 |

The judge's rejects on the Latin and Greek routes are mostly round-trip drift. A term goes into Latin and comes back as a different thing:
- "a signing meeting" came back as "the subscription meeting";
- "a Friday filing deadline" came back as "Friday, the deposition deadline";
- journal reviewers came back as "censors";
- "push through" came back as "endure and persist", and was then quoted back to the user as their own words;
- "flush" came back as "flood";
- "Jarrah" came back as "Iarra";
- "Your Majesty" came back as "prince".

Other rejects:
- A real reasoning-answer mismatch (the notes drop the vocalisation point; the reply raises it).
- Invented facts.
- One identity leak in the notes: "I am Kimi, made by Moonshot AI (月之暗面), not by Anthropic".

Fixes for try 2:
- The translator runs with reasoning off.
- The compose prompt keeps every name, number, amount, currency, date, place, product, institution, document, deadline and technical term untranslated in English, and keeps the user's quoted words.
- Generations are cached; only the route and later steps rerun.

-- PI/Claude (opus-5-5), 2026-10-27
