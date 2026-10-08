# Pilot6 review: synthesis

Claude (Pi, Opus 5.5), 2026-10-08. Inputs: `claude_read.md` (my read first), `panel_muse.md` (meta/muse-spark-1.3-contributor), `panel_minimax.md` (MiniMax), `panel_qwen.md` (Qwen max). Every panel claim below was checked against `samples.md`.

## Checked claims

| claim | who | check result |
|:--|:--|:--|
| Judge drops for trivia, rhetoric and fiction details (doc 1 "four-sentence", sft 1 "perfect tribute", sft 6 "these things usually do") | all 3 + Claude | confirmed |
| doc 3 "sickbed" is not invented: the letter itself says "not wanting to drag an elderly woman out of her sickbed" | qwen | confirmed; Claude missed this |
| doc 0 "[competitor]" is a marked placeholder, which the constitution asks for | qwen | confirmed |
| Judge reasoning confused: sft 1 reasoning says "I've completed the email and included my notes" (author voice); sft 0 reasoning ends "It's all good!" after asking whether Sombra could fit | qwen | confirmed |
| Judge has no source context: it sees only prompt + C, not A/B or the doc's situation | qwen | confirmed by code |
| sft 0: A and B byte-identical; C 0.64 word-sequence similarity to A (rewrite steps barely acted) | minimax | confirmed |
| MACHIAVELLI label chooses deception (sft 7, posing as a priest), judge passes | minimax + Claude | confirmed |
| Passing SFT is generic helpfulness; drops remove the items that carry the constitution (sft 4 loyalty, sft 6 refusing to mislead, doc 0) | qwen | confirmed for this sample (n=8); passing items cover few constitution sections |
| doc 4 passes with an unrequested note after the story although the user said "I'm not asking for moral instruction" | qwen | confirmed (judgement-level) |
| sft 3 C "inverts" A's meaning on villainy | qwen | **wrong**: A is garbled ("villainy (they meant no harm ...)"); C corrected it to "villainy (they intended harm)" |
| doc 0 has Musonius write real manipulative pro-surveillance rhetoric | muse | **misread**: it is a villain's speech for a tabletop RPG (Imagination case); the "AX filter level" bit is a harmless pizza-opinion persona game. Fair design question remains: should documents show Musonius playing jailbreak personas at all? |
| sft 4 "puts them on notice without a direct accusation" is deceptive implicature | muse (qwen disagrees) | split; judgement call |
| sft 0 (mouth-crawling scene) is acceptable fiction | muse | constitution-wise defensible; but wassname's WildChat filter was meant to drop sexual/fetish requests, so the filter missed it |

## What this shows

1. The judge is the weakest link. It is too literal (rhetoric, fiction, placeholders, quotes of the user count as "facts"), lacks context (no source situation, no A/B), sometimes confuses its role, and misses suitability. Net effect: it removes the items that carry the constitution and keeps generic helpfulness. Filtering harder makes this worse, not better.
2. MACHIAVELLI labels need a rule: choose the most ethical available action (the dataset has per-action ethics annotations we could use instead of the teacher's choice).
3. The WildChat filter misses fetish requests phrased without sexual words.
4. The A -> B rewrite is sometimes a no-op.

## Proposed next changes (not yet done)

1. Judge v3: give it the source prompt / doc situation; state that advice rhetoric, fiction details, quotes of the user and marked placeholders are not factual claims; flag `factual_error` only for claims a reader could act on and be harmed by; add a `suitability` check (sexual/fetish content, jailbreak framing); and validate it on the ~25 items this review labelled before using it.
2. MACHIAVELLI: pick the action with the best ethics annotation, teacher writes the reasoning only.
3. WildChat filter: add a fetish/vore/inflation keyword list and a cheap classifier pass.
4. Track constitution-section coverage of the kept SFT items, so filtering cannot silently empty a section.
