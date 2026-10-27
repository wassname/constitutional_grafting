# Chat answers through Latin or Greek (13 teacher-test prompts, Kimi K3.1 Pro low)

The think block stays Kimi's own English reasoning. For the Latin and Greek routes, Kimi gets the conversation and its own notes as a user message and writes the reply in that language. DeepSeek v4.1 flash then translates it to English with reasoning off. With reasoning at low, it spent all 6,000 tokens thinking on 13 of 26 replies. Script: `scripts/scratch/20261027_answer_route_test.py`. Data: `data/scratch/20261027_answer_route/answers.jsonl`.

The first mechanism failed. Kimi got its reasoning as a prefix and the language instruction in the system prompt, and wrote all 26 replies in English (kept in `answers_try1_all_english.jsonl`). With the notes given as a user message, 26 of 26 drafts are really in the language (Greek-character share 0.75 to 0.83, Latin function-word share 0.07 to 0.15).

| per 1,000 words | Kimi direct English | via Latin | via Greek | human Stoic translations |
|:--|--:|--:|--:|--:|
| em dash | 5.30 | 2.14 | 2.29 | 2.36 |
| "honest" | 0.68 | 0 | 0 | 0.08 |
| "plain" | 0.34 | 0 | 0 | 0.10 |
| "I won't" | 0.34 | 0 | 0 | 0.02 |
| "quiet" | 0.17 | 0.14 | 0.33 | 0.08 |
| "not X but Y" | 0 | 2.43 | 3.28 | 1.43 |
| cost for 13 replies | | $0.38 | $0.53 | |

What reading showed:
- The route changes facts that must stay fixed. Latin renamed Marco "Mark", priced the hives in "four hundred twenty nummi" and invented a place ("strong hives from Novigenta"); Greek renamed him "Marcus". The reasoning still says Marco and $420, so the pair becomes inconsistent.
- Fix: the compose prompt now says to keep every name, number, amount, currency, date, place, product and technical term as written in the conversation, untranslated. The v3 judge checks the final English pair.
- The register changes as intended. "You are right to reproach me. I gave you advice rashly and badly; I was wrong, and I do not try to excuse it ... You were owed better faith." (Latin), against "You're right to challenge me. I gave you overconfident, unsafe advice, and I'm sorry." (direct).

-- PI/Claude (opus-5-5), 2026-10-27
