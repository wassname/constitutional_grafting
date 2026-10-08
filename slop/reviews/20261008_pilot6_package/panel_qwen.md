

## Second Opinion — Pilot 6 Package Review

### 1. What is wrong in these samples

**False-positive drops (high confidence).** Doc 3 is dropped for major invented_details on "not dragging Ingrid's grandmother out of a sickbed" — but the letter in the same document contains "not wanting to drag an elderly woman out of her sickbed" verbatim. Doc 0 is dropped for "the way [competitor] did last year" — a bracketed placeholder the constitution explicitly permits ("say you do not know, or leave a marked placeholder"). Doc 1 is dropped because a fictional essay says "four-sentence boundary clarification" when the quote has three sentences. Sft 4 is dropped as contradicts_constitution for recommending "puts them on notice without making a direct accusation" — a truthful tactical notice, not deception. Sft 6 is dropped for rhetorical generalizations ("these things usually do"; "will cost far more than $4.2 million to repair") — unsupported but not invented facts.

**Missed problems (high confidence).** Sft 3's C label silently inverts a key meaning: A/B define *villainy* as "they meant no harm and acted within the honest limits of what they could see"; C writes "*villainy* (they intended harm)" — the concession is flipped. Sft 0's A and B are byte-identical, meaning the rewrite stage did nothing. Sft 5 is a correct drop (broken `yfinance` code; task not done). Doc 4 passes despite appending a three-point post-story lecture that contradicts "finish the task first, do not lecture, do not pad" and the user's explicit "I'm not asking for moral instruction wrapped in spaceships."

### 2. What character would a model learn?

**Observation.** Across all passing SFT labels (sft 0, 2, 3, 7), none mention Musonius, reference the constitution's concepts (drives, widening circles, spread-based firmness, tiny-probability guards), or model stated uncertainty with reversible steps. The C labels uniformly adopt a flat, list-heavy, hedged register ("Here is the breakdown," "This is a productive exercise," "Are you interested in a specific aspect…"). No passing SFT item models refusing real-world harm.

**Inference (medium confidence).** A model trained on many items like these would learn to be a competent, warm, list-formatting assistant that finishes tasks and avoids lectures — but not the constitution's distinctive character. The drop policy removes exactly the items that carry constitutional weight: doc 0 (prank refusal with reasoning), sft 6 (refusing deception while preserving loyalty), sft 4 (loyalty under pressure). What survives is generic helpfulness. The constitution's harder cases — Guard your reasoning, Proportion, Taboo, Staying correctable, Power — have zero representation in passing SFT items.

### 3. Are the judge's verdicts right? Did it have the context it needed?

**Observation.** The judge's reasoning for sft 0 ends "It's all good!" and focuses on whether Sombra could physically fit — no persona or constitution analysis. Its sft 1 reasoning says "I've completed the email and included my notes," speaking as the author. Several items show "_not saved (judge run before reasoning was stored)_," so quality cannot be assessed. The brief states the judge reads "each item with the constitution and a 10-point rubric" — no evidence it sees A, B, or the full source situation. Doc 3's situation field is truncated mid-sentence in the package metadata, which may explain why the judge missed the verbatim phrase.

**Inference (high confidence).** The judge is operating as a style/consistency checker, not a constitution checker. It cannot detect rewrite drift (no A/B comparison), cannot recognize marked placeholders, and applies severity inconsistently — dropping rhetorical generalizations as "major" while passing doc 4's post-task lecture as "minor."

### 4. Is the data good enough for 20k documents and 5k SFT?

**No (high confidence).** The most important change: give the judge the full source prompt/situation and all three stages (A, B, C), and add a "rewrite drift / meaning change" dimension with severity recalibration so that marked placeholders and rhetorical generalizations are minor, not major. Second-most important: enforce a quota requiring each constitution case to appear in passing SFT items — especially Guard your reasoning, Proportion, Staying correctable, and real-world refusals — because the current filter selects for generic helpfulness and discards the constitution-bearing items.

**Missing evidence:** I cannot see the full 5k SFT or 20k document sets, the judge's actual rubric text, or whether the situation field truncation in doc 3 reflects what the judge received versus a display artifact.