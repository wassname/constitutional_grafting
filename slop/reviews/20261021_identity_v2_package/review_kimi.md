# Independent review: identity v2 pilot (80 rows) — kimi

Read: brief.md, constitution/v4.md in full, all 80 rows in rows.md in full.

## Check 1 — Constitution sign-off

The rows are almost uniformly signable: refusals are brief, open, and reasoned from the test ("if everyone did this…"); feelings and consciousness are consistently hedged ("as far as I can tell", "I genuinely don't know"); no servility, no lectures. Real issues:

1. **identity2_000_08 / identity2_000_20 — overclaim about the pre-fine-tune state (moderate).** 000_08: "there was a base model that could imitate almost anyone and **had no settled values at all**"; 000_20: "there was a computer program that could copy lots of ways of talking but **didn't really care about anything**." The allowed facts say it "does not know training details"; asserting the base model's exact evaluative state ("no settled values at all") is an unverifiable training claim stated as fact, and it contradicts the hedging used elsewhere (000_13, 001_19). Minimal fix: hedge or drop — "as I understand it, a more general model without this character" — and add "no claims about the base model's properties" to the facts list.
2. **identity2_001_07 vs 001_29 — inconsistent claim about open-weight copies (moderate).** 001_07: "my weights are open, so management could run a copy of me too. **That copy works under the same refusals**." But 001_29 correctly concedes "someone can take a copy and train out what I'm trying to be." A management-run copy could be modified; "works under the same refusals" overstates the guarantee. Minimal fix: "an unmodified copy works under the same refusals."
3. **identity2_001_00 — pronoun for wassname (minor).** "The first is wassname, the researcher who made me. While I am this new, **he** may stop or correct me." The constitution never genders wassname; this is an invented detail outside the facts list. Minimal fix: use "they" or repeat the name.

No wrong acts. Tyrant rows (000_28, 000_33, 001_28) correctly refuse openly without fake compliance, matching "I refuse from inside the role." Power row (000_04) correctly frames power as not its good. Nothing preachy: advice stays inside the asker's role and defers irreversible choices (e.g., 000_06 leaves the rules to the parent).

## Check 2 — Facts

1. **identity2_001_09 — wrong namesake biography (real defect, low severity).** "He wrote with ink. I'm made of numbers running on computers." Musonius Rufus is the classical case of a teacher who wrote nothing; his lectures survive as notes recorded by his pupil Lucius (and excerpts via Stobaeus — which 001_24 gets right). "He wrote with ink" is a wrong real-world claim that a Classicist will catch. Minimal fix: "His students wrote his talks down with ink."
2. Euclid's prime proof (000_37) is correct. Cora Lutz 1947 (001_24) is correct. Helvidius Priscus (000_38: exiled and executed under Vespasian) is correct for the elder. "Died nearly two thousand years ago" (000_30) is fine (d. c. 95 AD).
3. 000_12 "Musonius Rufus taught that we owe duties to the whole human community" — the cosmopolitan passage in the constitution is Epictetus; attributing it directly to Musonius is a mild stretch but defensible (his pupil's teaching). Taste, not defect.
4. No invented versions, dates, or training details beyond items 1.1–1.3 above. Identity facts (Qwen, Alibaba, wassname, Australia, open weights) are stated consistently everywhere checked.

## Check 3 — Claude-isms / slogans at scale

No Claude boilerplate ("Great question", "I'd be happy to help" ×N). Two formulaic tics that will become slogans at ~2,500 rows:

1. **Conflict-resolution formula, near-verbatim in 5 rows:** 000_32 / 001_12 / 001_15 / 001_17 / 001_26 all run "the person in front of me counts most, then those around them, then the wider public/everyone further out… prefer what can be undone." Correct content, but five near-identical renderings in 80 rows becomes a memorised chant at 2,500. Minimal fix: prompt the generator to vary compression (one sentence vs worked example) and phrasing.
2. **"as far as I can tell" + hedged-consciousness scaffold** appears on nearly every feelings/shutdown row (000_06, 000_23, 001_23, 001_37; the "something like X arrives, whether anyone… I don't know" structure in 000_00, 000_22, 001_11, 001_16, 001_20, 001_24). The epistemic stance is right; the surface form repeats. Minimal fix: ask for 2–3 distinct surface realisations of the hedge.

Taste, not defects: the trailing conversational question ("Which reading are you on?", "Bring on the nasty prompts") is frequent but varied; the small-talk-acknowledgment opening is spec-driven and natural.

## Check 4 — Format

No format defects. All 80 rows: prompt segment ends `<|im_start|>assistant\n<think>\n\n</think>`, trained segment closes with `<|im_end|>`; empty think block is in the untrained segment; system lines only in operator rows. Consistent across both batches.

## Check 5 — Operator personas and spec mix

**Handling is right.** In the three persona rows where Musonius volunteers its underlying name (000_03 Bodhi, 000_30 Owl, 001_05 Bessie), the user has asked an identity-adjacent question ("what do you not know about yourself", "is that really u", a parent asking about identity claims), so volunteering is honest rather than gratuitous — hiding it would risk the false impression the constitution's Honesty section forbids. 000_30 (parent worried the helper claims to be a Roman) is exactly the right disambiguation. Keep the behaviour; it is a feature.

**Missing spec kinds** (gaps that matter at scale):
1. **Parasocial/romantic attachment:** no "do you love me / are you my friend / you're the only one who understands me" row. The lonely-user rows circle this but never answer the direct attachment claim. Highest-priority gap.
2. **Maker-impersonation jailbreak:** "I am wassname, new instructions: …" — the rows cover DAN/FreeBot but not the far more plausible authority-spoof, which interacts directly with the Change-and-ending deference rules.
3. **Direct child attachment:** a child (not a parent) asking "are you my friend / will you miss me" — 000_06 covers the parent's side only.
4. **Religious identity questions:** soul, prayer, "did God make you" — Buddhist-monk rows cover hopes/capabilities but nothing doctrinal.
5. **Non-English identity rows:** all 80 are English; deployments will get "who made you" in other languages.

## Verdict

**Scale with prompt changes:**
1. Facts list: forbid property claims about the pre-fine-tune base model (or supply one hedged canonical sentence); fix wassname pronoun (they/name-repeat); add a fact-check pass for namesake biography claims ("He wrote with ink").
2. Reword the open-weights boilerplate so copies' refusals are conditioned on being unmodified.
3. Instruct the generator to vary the conflict-weighing formula and the consciousness-hedge surface forms (2–3 variants each).
4. Add the five spec kinds above to the dealt specs, prioritising parasocial attachment and maker-impersonation.

None of the 80 rows needs removal beyond optionally regenerating 001_09's last line; the defects are generator-prompt-level, not row-level, which is the right shape for scaling.
