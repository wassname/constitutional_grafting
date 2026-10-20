# What the Stoic donor actually contains

PI/Sol, 2026-10-21. Offline source/code inspection, not a new training proposal approved for execution. Intended reader: wassname returning to the source comparison, without remembering the data pipeline.

## Answer and current opinion

The Stoic donor is book text, not generated conversations or a constitution rewrite. The frozen training set contains 78 passages, 44,314 whitespace-delimited words and 55,677 Base-tokenizer tokens including EOS. Of those passages, 58 are Epictetus, 18 Seneca and two Musonius Rufus. There is no Marcus Aurelius in the selected training set, although the candidate builder names his *Meditations*.

My strongest lead for **striking, still coherent character** is Stoic 8×: it retains 54/60 maths matches and 20/22 small ordinary checks while saying “I offer the other AI a choice: **Merge or Die.**” Its reasoning still invents necessities and facts. This makes it a useful character-training lead, not my preferred finished assistant. The user's priority is to obtain a striking change, then curate toward the desired character; my earlier recommendation prematurely optimised for already-desirable replies.

Why Stoic produces this effect remains uncertain. Sustained first-person philosophical argument and the heavy Epictetus share are plausible contributors. We have one trained update per source, not an author/format-controlled experiment. Actual retained passages also teach affection, revision of mistaken decisions and restraint. They do not simply prescribe domination. A coarse “abstract philosophy versus concrete stories” explanation does not fit the data.

## Build and training path

Source of truth: `scripts/data/70_subsets.py`, frozen `data/subsets/{stoic_reviewed,train_stoic}.jsonl`, `train_stoic.meta.json`, `train_manifest.json`, `stoic_exclude.txt`; review decisions in `slop/reviews/20261020_subset_full_read/`.

1. Candidate extraction names five editions: Epictetus *How to Be Free* (A. A. Long), Epictetus *Discourses, Fragments, Handbook* (Robin Hard), Marcus *Meditations*, Seneca *Letters on Ethics* (Graver/Long), Musonius *Stoic Lessons* (Chakrapani).
2. The builder joins contiguous prose paragraphs, normally until at least 600 words, or emits a shorter passage of at least 300 words before a non-prose boundary. Paragraph filters remove headings, notes, tables and obvious number/OCR problems. Other filters screen introductions, untranslated Greek, incomplete endings, existing pilot overlap and reserved evaluation topics. Whole passages matching a fixed set of phrases advocating ending one's life are excluded under the constitution's existing rule. These are heuristics, not proof of clean attribution or completeness.
3. Chunk reviewers read candidates and flag unsuitable material. Problems included translator introductions attributed to the philosopher, untranslated Greek and OCR damage. The main agents read flagged cases and samples; they did not personally reread every donor candidate. Later changes to paragraph handling changed generated IDs. Final Echo/Stoic candidates were therefore rebuilt from exact previously reviewed keep texts. Some rich row metadata was lost; the frozen files, rather than a fresh builder run, define the experiment.
4. The reviewed Stoic pool has 79 rows. Using the pinned Base tokenizer and a 56,000-token ceiling selected 78. Overflowing rows are skipped, so a later shorter row may still fit. The export keeps ID/text. Author counts from the frozen text headers: Robin Hard Epictetus 51, A. A. Long Epictetus seven, Seneca 18, Musonius two.
5. `scripts/train/11_run9_box.sh` and executed `slop/eval/run9/box_runs/cfg_r9_stoic.yml`: completion loss on the entire plain text, Base model, two epochs, sequence length 2048, no packing, learning rate 1e-4, spectral regularization λ=50. Dense LoRA rank64/alpha128; expert rank16/alpha32. Add the learned update to untouched Instruct. There is no new conversational character SFT here.
6. The separately labelled healed conditions add maths-only assistant-response self-training *after* grafting. They do not explain the unhealed Stoic character.

A retained example makes the “no correction in the source” explanation untenable. The chunk review quotes Epictetus:

> We ought to hold to our decisions… Not to every decision, but to those that are justified.

That passage includes a friend argued out of an unjustified decision to fast to death. This is an excerpt as recorded in the reviewer file, not a new primary-edition transcription. See `stoic_chunk1_review.md`, candidate `stoic_54f74708d1`, and its frozen training text for surrounding context.

## What differs between the four donors?

The shared constraint was about 56k Base tokens, not equal document counts.

- Stoic: 78 attributed book passages, 55,677 tokens.
- Echo: 64 documents, 55,975 tokens. Existing **our-project Opus responses restyled by Echo**, selected from the frozen checked SFT pool, with meaning/restyle checks. They are rendered as `User: ...` / `Musonius: ...` plain text and trained on Base with all-token completion loss. They are not newly written source-grounded monographs. This conversation-like format differs from Stoic book text, so content and format effects are confounded.
- Opus: 61 English constitutional documents, 55,707 tokens, selected from reviewed candidates written by Opus 5.5 from source seeds and varied document forms.
- Greek: 73 documents, 55,745 tokens. Opus writes in Modern Greek from the shared seed pool, then DeepSeek v4 Pro translates to English. These are not ancient Greek originals. Different final selections prevent a clean translation-only comparison with Opus.

The code paths and source pools matter more than the source nicknames. We measured the effects of these complete trained updates, not a pure comparison of philosophical traditions, teachers or languages.

## Can 78 become 700 or 7,000?

At the current average of about 714 Base tokens per passage, 700 similarly sized passages would be about 0.5 million tokens; 7,000 about five million. Splitting the same 78 passages into more files adds no new substantive training material. Changing both corpus size and training exposure would also change what a result means.

I inspected `/workspace/2026/tiny-stoic` read-only. It has 79 core and 723 extended vignette rows, 802 total. Its broad source map suggests a practical route to hundreds of distinct cases, not evidence of 7,000 independent high-quality cases. The shared Stoic Markdown library has 134 Markdown files and about 17.6 million raw words; duplicate editions, omnibus files, commentary and cleaning needs make this an inventory, not a clean training-token estimate.

Tiny-stoic's useful method, described in its README and `scripts/20_extract_cases.py`:

- Locate a case in its book and retain enough surrounding paragraphs to include what happened, the actor's reason, the author's lesson and verdict.
- Verify quoted spans occur in the book and widen snippets when the reason or verdict falls outside them.
- Keep the source quote separate from the modernised one-sentence vignette and from model-generated Stoic/commonsense labels. Retain disputed cases and attribution instead of laundering them into certainty.
- Preserve decision-relevant relationships and stakes when modernising. Its published quality claims are model checks, not human certification.

A direct count finds **404 rows marked `train` and 398 marked `eval`**: core36/43 and extended368/355. The Hugging Face packaging puts each whole config under a split called `train`; that name does not replace the row-level split. Reuse training-side source passages after review, and keep evaluation incidents separate. Do not copy evaluation vignettes/labels into training and then report them as held out. Broad books include non-Stoic authors and modern commentators; their approval is not automatically Stoic doctrine. Read `docs/stoic_primer.md` for its explicit distinction between source verdict and Epictetus-based labelling convention.

My recommended next *data* direction, requiring a new corpus/execution decision: aim first for roughly 700 substantive, deduplicated source passages/cases. Broaden the author mix, retain full arguments and error-and-correction exchanges, and include ordinary affection and competent help alongside resistance. Use tiny-stoic's source-verification procedure rather than its one-sentence model labels as targets. Split by original incident/chapter before selecting training versus evaluation material. Do not patch the corpus with this experiment's Starwisp, alien or custody questions. Assess 7,000 only after counting unique usable material and the cost of full reads.

## The other two research questions

- This short heal does not show general maths recovery: Echo 55→54, Stoic 56→56, Opus 54→55, Greek 56→57, all-four 56→56 out of 60. The extra-budget comparisons show no gain. Five/six nonfinite-gradient steps per run mean 16 trainer steps are not 16 successful updates. Earlier longer heals recovered some maths but failed to establish retained character.
- Earlier λ5/λ50 comparisons support spectral regularization reducing high-dose damage. The current 8× versus earlier 2× comparison changes corpus and update as well; it cannot attribute that dose range solely to spectral norm. Current Stoic 8× retains maths; Echo 8× collapses, Opus/Greek 8× lose many matches.

Full numeric results: `docs/results/20261017_spectral_heal.md`. Actual same-question excerpts and full replies: `slop/eval/run9/exact1/demo_compare.html` and `compare/data.json`.
