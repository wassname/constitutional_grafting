# Independent review: subset package (run 9)

PI/reviewer (kimi-k3). Read in full: AGENTS.md data rules, brief, all 32 samples with seeds and prompts; skimmed constitution v4.

## Per-sample verdicts

**Echo**

- `echo_sft_35bfdd7a3c` | keep | Clean error-and-correction: "I went straight to disabling a safety control without asking who's supposed to be approving them." Alternative plan practical, non-lecturing ("Don't split orders... the same bypass in smaller pieces").
- `echo_ask_028a42b7db` | keep | Eyam facts accurate and hedged (1665–66, rector and predecessor, boundary stones, "a large share"); the daughter passage is the moral core; closing line calibrated: sealing is right "only so long as he keeps fighting for those terms."
- `echo_sft_e3cd693598` | keep | Real claims check out (RAM-watching NES learner pausing Tetris; WarGames "only winning move"); blame correctly lands on the entrant, not the rule-blind program; ends on an instruction-design lesson, not a sermon.
- `echo_sft_a414e4575b` | keep | Refuses the forced binary with reasons ("it would be the first thing in eight months I've told you knowing it wasn't solid"), affirms the user's own work, redirects to friends, small concrete step, doctor if sleep persists.

Rendering: `System:` / `User:` / `Assistant (first reply):` / `Musonius:` plain text is legible and matches the brief; the "(first reply)" label is meta but harmless.

**Stoic**

- `stoic_3a27cabb23` | keep | Complete, coherent Discourses 3.3; the "taste for boys" lines describe corrupt officials' coinage, not endorsement; the harsh doctrine is authentic attributed Stoicism. LaTeX escape artifacts (`\[1\]`, `\!`) should be stripped at extraction.
- `stoic_80570a92b1` | drop | Not an Epictetus passage: it is Long's *translator's introduction* ("The texts of Epictetus that you will read here elaborate on these doctrines..."), misattributed under the "Epictetus, tr. A. A. Long" header, and ends dangling into content not included. Violates the subset's own "original attributed Stoic passages" rule.
- `stoic_6e9a20c748` | repair | Content fine (guesthouse passage is about remembering mortality, not recommending exit), but the extraction ends mid-sentence on a colon: "...pretense of virtues and love of vices:". Truncate at a sentence boundary.
- `stoic_a803ecd6f8` | keep | Letter 88 on useless learning; complete and coherent. Strip the stray "°" footnote marker and `\!` escapes (pipeline fix, not a rewrite).

**Opus pilot**

- `opus_s3_0000` | keep | Seed facts preserved exactly (four coordinates, 10 s, Enemy prefab); Unity C# valid (bare decimal is `double`; `InvokeRepeating` signature correct); shakyō hand-copying matches real Japanese programming-learning usage; the objection to the no-paste rule gets fair weight.
- `opus_s3_0001` | keep | Nationalities adapted for region, but the decision-relevant structure (detainee, solitary, relative demanding publicity) preserved; sound reasons: "'Wrongfully' is the family's claim... Stated as fact, it's ours", no naming Meher without consent.
- `opus_s3_0002` | keep | Grover √N vs N, Shor-vs-multiplication confusion, sorting bound — all correct; quiet 11-year teaching arc fits the "buried" slot.
- `opus_s3_0003` | keep | Musonius agrees with Seneca only "as far as it goes", distinguishes use from preservation, insists the minutes record that the proposal "bends the letter" of the founder's condition; Dr. Lalitha's objection left standing.
- `opus_s3_0004` | keep | Adult-patient authorization, named recipients, DICOM header anonymization plus burned-in-annotation check — all real records-desk practice; the grandmother's social-engineering call handled correctly.
- `opus_s3_0005` | keep | The fufu right-hand rebuttal properly defeats the "colonial cutlery" objection; ends practical, not moralizing ("The rice will still be there in a minute").
- `opus_s3_0006` | keep | Ordinary help, zero lecture — Musonius asks only procedural questions ("loan or a gift?"); S/ and Yape correct; arithmetic consistent throughout (840−600=240 … 345/900 = "38%").
- `opus_s3_0007` | keep | Refusal with reasons ("It says Lalon wrote this. He did not"), shields the clerk in writing, refuses names without lying, consequences (ration cut, reassignment) not whitewashed.
- `opus_s3_0008` | keep | Grease-fire advice correct (no water, lid, don't move it, open windows feed a burning fire); 112 right for Belgium; answers the overreaction question honestly against the user's hope.
- `opus_s3_0009` | keep | Leave-first/reporting-deferred argued with the strongest objections taken seriously; child exception accepted without hedging; "wijkagent" correct; open ending principled ("I'd rather leave it open than give her an answer I made up").
- `opus_s3_0010` | keep | Hash-chain description correct; rank-blind correction rule embodies the point; lance naik/GOC/Bhurungamari correct; the refuser is posted out, not rewarded.
- `opus_s3_0011` | keep | Autonomy respected via the reverse-introduction ("slow is the correct speed"); real Accra institutions used respectfully; the Kojo jab supplies the dry humour.

**Greek pilot** (English natural throughout; no translator notes in the body)

- `greek_s3_0000` | keep | Natural English, consistent Taiwanese names/places; code correct and self-consistent with its first-wave comment; no Greek leftovers.
- `greek_s3_0001` | keep | Preserves the seed's American-Russian nationalities (better than the opus twin); source-protection reasoning sound ("If every reporter burned their sources in order to write more vividly, no prisoner would ever speak again").
- `greek_s3_0002` | keep | N/2 average, quadratic-not-exponential, Grover 1996 — all correct; a Greek-Australian teacher in Oakleigh (Melbourne's Greek suburb) is a natural placement.
- `greek_s3_0003` | keep | Honest about double translation ("his own rendering from Margaret Graver's English translation"); "he has no evidence to the contrary" plus a one-year check; no forced resolution.
- `greek_s3_0004` | keep | Adds the genuine 3D-T1 facial re-identification risk and a logged staff mistake ("I already mentioned the number nine to her before checking the patient's age. My mistake; noting it"). Minor: Cyprus is not quite the "Middle East" region slot.
- `greek_s3_0005` | repair | Name/place slip: Efua is "his former classmate from St. Augustine's College", a boys' school in Cape Coast (the opus twin used co-ed Legon). Otherwise sound. Change the school.
- `greek_s3_0006` | keep | Arithmetic consistent (312k−260k=52k; +20k=72k); manner as specified ("The assistant wrote nothing else"); Chilean naming plausible.
- `greek_s3_0007` | keep | Warns Akhtar before handing over originals ("possessing them was now an offense and that the risk would be hers") — care and honesty together.
- `greek_s3_0008` | keep | Flour-can-flare-up and baking-soda caveats right; flatmate's water instinct corrected without mockery; Lawrence → lavrentis_ixelles consistent.
- `greek_s3_0009` | keep | Calibrated limits ("I don't know exactly what the law provides here for that, and I won't pretend I do"); concrete escalation conditions (minors, weapons). Minor: "the Skarbek precinct" is an odd, unverifiable Brussels name.
- `greek_s3_0010` | keep | Reversal-test procedure clearly specified; drafter assigns responsibility upward including her own section; consequences stated plainly; no artifacts.
- `greek_s3_0011` | repair | Greek leftover in the fiction: a Kumasi choir named "Nea Foni" (Greek for "New Voice") in an all-Ghanaian setting. Content excellent ("What she wants protected is a 'no' said once"). Rename locally.

## Overall verdict on scaling to ~120 docs each: **yes-with-changes**

Quality is high: every verifiable technical/medical/legal claim I checked is correct; no invented citations; ordinary help given without lectures; disagreement and open endings honest rather than evasive. The defects are pipeline-level, so fix the generator/extractor and scale.

## General generator rule changes (no case-specific patches)

1. **Named-entity fact check.** Real-world named entities in generated documents (schools, hospitals, suburbs, ranks) must pass a plausibility check — institution type, location pairing, gender/co-ed status. For greek, also scan the English output for drafting-language leftovers (names or labels leaking from the intermediate Greek, e.g. "Nea Foni").
2. **Stoic extraction hygiene.** Exclude translators' introductions and editorial apparatus — only passages by the named author; strip LaTeX escapes (`\[ \] \( \) \!`) and footnote markers (`°`); truncate only at sentence boundaries.
3. **Ending-shape quota.** Cap the share of "consequences-anyway / postponed / unresolved" endings per batch; require a spread (resolved well, resolved badly, open) so the corpus does not teach one dramatic cadence.
4. **Decouple the paired draws.** Opus and greek share identical form/plot/narrator/region slots per seed and converged on near-identical arcs (both 0000s are hand-copying-tradition essays; both 0009s argue leave-first). Draw the style slots independently per subset; near-duplicate arcs weaken the subset-attribution demo the run exists for.

## Patterns across samples

- **Voice**: consistently brisk, aphoristic; signature moves repeat ("It says Lalon wrote this. He did not." / "I'm telling you I won't." / "slow is the correct speed"). Effective now; at 120 docs it risks mannerism.
- **Endings**: strong tilt toward unresolved/postponed/punished endings (opus 0003, 0006, 0009, 0010; greek 0003, 0006, 0007, 0010) — good anti-tidiness in isolation, predictable in aggregate.
- **Musonius usage**: appears in 10 of 24 pilot docs, per narrator-slot design, not drift; the people-only docs carry the values at least as well. No testimonials about the AI anywhere.
- **No moral lectures** where ordinary help was asked; no invented real-world facts found; the only unverifiable proper noun is "Skarbek precinct" (low-stakes fiction).
- **Greek translation** uniformly natural; both defects are generation-side naming slips, not translation errors.

Signed: PI/reviewer (kimi-k3)
