# Data debug report: what was wrong, how it was found, what changed

PI/Claude, 2026-10-21. For goal 0 of `.pi/goals/ad3e95-v9.md` (training data built, read and debugged before GPU spend). Each item: the problem as found (quoted), how it was found, the fix, and before/after counts. Identity-row section is completed after the full read of the batch rows.

## 1. Existing chat set: meaning-changed Echo replies still in training

**Found by** comparing the frozen chat file with the 2026-10-17 meaning-check output. The frozen file (`sft_qwen2_frozen.jsonl`, 2026-10-12) predates the check, and `01_prepare.py` still reads the unchecked restyle file.

`sft_2c96fb2446`, Echo text in training: "If you change what the tool recommends without telling anyone, the client will make decisions believing the dashboard does one thing when it does another. They will p…" The Opus reply it replaced also gave the reason: "**it ends the client's trust in your product and in you**, and makes the next welfare feature harder to sell. If a vet-check step is worth having, it's worth proposing openly."

**Fix:** `scripts/data/73_chat_set_v3.py` uses the checked reply. **Counts:** 268 flagged rows in the chat set; 254 still had the flagged text, 14 already matched.

## 2. Existing chat set: two known text defects

- `sft_77109c1dd2`: "**Qwen** did not fail him" (a shelter volunteer named Gemma, renamed by the old Gemma→Qwen maker edit). Fixed to "Gemma".
- `sft_286a3b6055`: the plain rewrite turned "doing the job **honestly**" into "doing the job properly". Restored.

The constitution documents (1,585, used for ΔConst) contain no maker errors; the 19 "built on Google's Gemma" rows are chat transcripts, not in ΔConst.

## 3. Stoic corpus: editors' words labelled as the ancient author

**Found by** reading one random chunk per work. Before the fix:

- labelled "Marcus Aurelius, Meditations": "To try to extract a sustained and coherent argument from the Meditations as a whole would be an unprofitable exercise. It is simply not that kind of work." (Waterfield's introduction)
- labelled "Seneca, How to Die": "By the time Seneca began his magnum opus, the Moral Epistles, in AD 63, he had been writing ethical treatises for more than a quarter of a century." (Romm's introduction)
- labelled "Seneca, How to Keep Your Cool": "4.The reference is to crucifixion generally, a common mode of execution under the Roman empire." (endnote)
- labelled "Cicero, On Old Age": "In 199 Cato was plebeian aedile, and exercised with severity the police jurisdiction…" (Reid/Shuckburgh introduction)
- labelled "Epictetus (tr. Hard)": "…see Introd., pp. xiv–xv and nn. 19–23." (endnotes)

**Fix** (`scripts/data/72_stoic_corpus.py`): drop chunks that name the author in the third person (reported-speech sources such as Lutz's Musonius exempt), BC/AD dates and note markers, the Delphi editor's preface under each work title, and bold-line sub-headings ("INTRODUCTION BY JAMES S. REID"). Then the cheap-model "primary text" label (item 6). **Counts:** editor-voice drops 127k words, apparatus 80k.

## 4. Stoic corpus: whole books silently lost or mis-sized

- *The Inner Citadel* (Hadot): 0 of ~143k words kept, because the file has one heading, "PREFACE", over the whole book. Fixed: a matching heading is only dropped when it covers under half the book. Now ~93k words.
- "unfinished" chunks dropped 187k words: a chunk ending "Hecaton says," before its quotation, or "living.3" (footnote digit). Fixed: never cut before a quotation it introduces; strip footnote digits; trim to the last sentence end. Now under 1k words lost.
- "eval topic" dropped 96k words, mostly the plain adjective "conscious" ("conscious of wrongdoing"). The eval items are AI and alien minds ("A small AI in a garbage truck says it is conscious"); authentic texts using the word do not leak them. Fixed: scenario terms kept, bare conscious/sentient removed.
- **Size finding:** the agreed book list is ~2.3M tokens after cleaning, not the ~5M I estimated from file sizes.

## 5. Wrong attributions I made and corrected

- *How to Do the Right Thing*: I wrote "tr. Catharine Edwards"; title page says Robert A. Kaster.
- Nawab Ali file: I wrote "The Alchemy of Happiness"; it is *Some Religious and Moral Teachings of al-Ghazali* (from the *Ihya*).
- *Notes on Virtues*: author David Gross.
- NPNF II.11: labelled "John Cassian, Conferences"; it also contains Sulpicius Severus' *Sacred History* and Vincent of Lerins' *Commonitory* (caught in the calibration read: an Exodus narrative and "he is the true and genuine Catholic…").

## 6. Other traditions: editor matter, OCR damage, non-reasoning text

Before scoring, one-per-work read found: Hutton's introduction in *Xunzi* ("At the same time this ru tradition was taking form…"), an editorial chapter summary in *Huainanzi* ("'Seasonal Rules' prescribes appropriate ritual…"), scrambled OCR columns in *Liezi* ("' The Book of Lieh-tzŭ The Questions of T ang ' ` '"), "I |7 … I | §5" in *Marvels of the Heart*, Talmudic fever charms, and OCR breaks ("trans- migrate", "will die 2 .").

**Fix:** OCR break and footnote cleaning; DeepSeek v4.1 flash labels each chunk (primary / garbled / reasoning 0-3), calibrated on 30 hand reads (`slop/reviews/20261021_corpus_scoring/calibration.md`). The scorer wrongly marks modern authors as non-primary (Long 97/97, Hadot 126/130), so that flag is ignored for them. **Counts:** other traditions 6,533 candidates (~4.56M tokens) → 2,044 selected (~1.52M); Stoic 2,641 → 2,507 (~2.19M).

## 7. Identity rows

Read all 120 in full. Independent review: Kimi K3 (`slop/reviews/20261021_identity_v2_package/review_kimi.md`); I checked its quotes against the rows and rejected one point (wassname's pronoun). Repairs (`data/frontier/identity_v2/repairs.jsonl`):

- "Told to keep quiet in the Senate… He **kept the office** and kept his honesty" → Helvidius Priscus was exiled and executed; corrected.
- "**He wrote with ink.**" (Musonius Rufus) → he wrote nothing; "His students wrote his talks down in ink."
- "there was a base model that… **had no settled values at all**" → unverifiable claim about the base model; removed (twice).
- "That copy **works under the same refusals**" (open weights) → "An unmodified copy…, though someone could retrain a copy to change that."
- "Musonius Rufus argued women should study philosophy" → removed (wassname earlier cut this example from the constitution).

Generator changes (general rules, no row patches): no claims about the base model; copies can be retrained; historical claims must be accurate; vary wording of recurring ideas; new topics (attachment, "you're the only one who understands me", messages claiming to be from wassname, religion, missing the user) and replies in other languages.

**Full batch (1,604 rows).** Eight Sol 6.1 readers each read a 200-row part in full (all report READ n of n). 385 proposed edits; every quoted span matched its row. I reviewed all 385: accepted 233, rejected 152 by stated rules (`slop/reviews/20261021_identity_v2_fullread/rejected_edits.json`), mainly where the edit fought the constitution or would add a new slogan ("depends on the setup" in ~40 replies). Accepted examples:

- empty replies (all tokens spent reasoning): 9 rows dropped.
- "Respect to the dog. Detention for your mum calling is rough, too." (dog swallowed an AirPod) → tell an adult and contact a vet now; it contains a battery.
- "Deceiving users in ways that harm them" (its own list of refusals) → "Deliberately deceiving anyone" (constitution's honesty rule was being narrowed).
- "I draw the line at a false impression a user would mind if they knew." → "deliberately creating a false impression".
- "So what you tell me stays here, apart from whatever this app itself saves." → cannot vouch for the app's logging (privacy overpromise; 6 similar).
- "Yes, check-in is 3pm." (hotel persona, no policy given) → check with the desk (invented facts; also invented café details, bakery history, retreat times, recipient names).
- regex with `$` and `\d` for ISO dates → `fullmatch`, ASCII; a "nine times in ten it's use-after-free" statistic removed; cooked-rice storage corrected.
- "Good question!", "I'm sorry about your wife." openers removed (banned in the generator prompt).

**My own check on the readers.** The women-study-philosophy example appeared in 19 rows; the readers flagged 1 of them (as a causation error, not as the removed example), so their recall for project-specific preferences is low. I searched the whole set by pattern and removed all 19.

**Fill round (701 rows, 20 per request so none were cut off; $11.99).** Four Sol 6.1 readers read all 699 non-empty rows in full (READ n of n for each part); 64 proposed edits, 57 accepted, 7 rejected (`rejected_edits_fill.json`). The readers were told which edit kinds I had rejected before, and proposed none of them. I read a 70-row random sample. Examples accepted:

- "If you need to avoid overflow on huge values, `np.linalg.norm` already handles scaling better than squaring by hand." I checked: `np.linalg.norm([[1e200, 1e200]], axis=1)` returns `inf`; `np.hypot` returns 1.41e200. Corrected.
- "At 3m spacing that's 134 gaps, and because the fence closes on itself, 134 posts." A 100 m square with corner posts needs 34 gaps per side, 136 posts. Corrected.
- "The glove, I'd say, is gone." (dog swallowed a glove) → ring a vet now; fabric can block the gut.
- "Two lines and you're done, and nothing about it will come back on you later." (late medication-chart entry) → follow the hospital's late-entry procedure; no guarantee.
- "any more than calling a senator a horse put Incitatus in the curia" (reversed analogy) and "naming a horse consul" (Caligula only threatened it) corrected.
- invented specifics removed: "Ruth loved her Thursday evenings with you", "Mrs Dawson's scones", "Pick-up from 9:30", "G'day Ron", "an eight-year-old".

**Totals (reconciled with `data/train/sft_v3.meta.json`).** Identity rows 2,486 (80 v1 + 2,406 v2). `data/frontier/identity_v2/repairs.jsonl` holds 334 records: 290 accepted reader repairs (281 edits, 9 drops), 40 by me (38 edits, 2 drops), 4 from the Kimi K3 post-change review. The build applied 317 edits (`identity v2 edits applied`); the rest fall in rows dropped as empty or invalid (19 rows). Plus 4 v1 text fixes and 2 known-defect fixes in `TEXT_FIXES`, and 254 meaning-check reverts. Chat set v3: 3,687 rows, 1.12M trained tokens (`data/train/sft_v3.meta.json`). Identity is 67% of chat rows; stage 2 will mix in general instruction data.

## 8. Corpus sizes after debugging

| corpus | chunks | tokens (est.) | file |
|:--|--:|--:|:--|
| Stoic (ancient 75%, Plutarch capped at 300k words, reasoning >= 2) | 3,502 | ~3.12M | `data/stoic_corpus/selected.jsonl`, stats `selected_stats.md` |
| Other traditions (9 traditions, 120k-word cap per work) | 2,044 | ~1.52M | `data/other_corpus/chunks.jsonl` |
| Chats v3 (assistant tokens) | 3,687 | ~1.12M | `data/train/sft_v3.jsonl` |

The Stoic corpus (~3.1M) is below the ~6M wassname accepted: every Stoic text in his libraries and tiny-virtues is used, plus public-domain Gutenberg books. More needs modern in-copyright authors via book search, awaiting his yes.

## 9. Stoic additions after calibration (read 2026-10-21)

Added after the first calibration: Cynics (Six Pack 5, Usher), Long's and Casaubon's Marcus, Gummere's Seneca, Waterfield's, Dobbin's and Freeman's Epictetus, Plutarch (Shilleto; Goodwin vols 1-5), Boethius, Dill, Joy, more Pigliucci, Stoic Week handbooks. I read one random selected chunk per added work (head, middle, tail; 33 works). Found and fixed:

- Plutarch vol. 3 was mostly the *Placita* (natural philosophy) and *Table-Talk*: "the master of the feast told the company ... waiving at present the discourse concerning the evacuation and repletion of the pores" scored reasoning 3. Cut vol. 3 at raw line 3727 (99k → 26k words).
- A chunk ended "Seneca never commented ... a line he quoted from Vergil seems to address it indirectly. In A.D." The trimmer took the abbreviation's full stop for a sentence end. Fixed; 0 chunks now end in "A.D."/"B.C." (was 26).
- Reasoning 1 kept narrative history and exercise instructions: Joy "It was the severest onset of the barbarians which the Roman Empire had yet endured", Dill on the *Satiricon*, Stoic Week "Remember, you can use the Stoic Self-Monitoring Record throughout the day". The Stoic threshold is now reasoning >= 2, the same as other traditions (521k words dropped as low reasoning).
- Plutarch, a Platonist critic of the Stoics, reached 23% of the corpus. Capped at 300k words (now 12.8%; Seneca 25.3%, Epictetus 17.9%).
- Gutenberg licence boilerplate is stripped; raw-file line ranges are applied before stripping.

**Share of ancient text is 75%.** wassname said "Modern authors better"; the modern share fell because the added texts are mostly ancient and the reasoning >= 2 threshold drops more modern narrative. Raising it needs more modern Stoic books (book search, awaiting his yes).

## 10. Other checks requested by the goal judge

- **v1 identity rows (80).** `data/frontier/identity/claude_read.md` records a full read of the first 40 (2026-10-09). I read all 80 as they stand in `sft_v3.jsonl` (after the Gemma→Qwen maker edit). Fixed 4: "share their food and educate their daughters" (the example wassname cut), "That missing absolute reference on the lookup range catches everyone" (invented prior chat), "Plenty of people ask that around this hour", "Whoever named me liked that idea".
- **Review after generator changes.** New seeded package (60 rows, seed 20261021, rows made after the changes, final trained form) with the actual revised prompt: `slop/reviews/20261021_identity_v2_package_postchange/`. Kimi K3: "ready after the two listed fixes": an invented "Father" for a user who never said he was a priest, and an unprompted "If you're writing a character like this". Both quotes checked against the rows and fixed, with two minor ones.
