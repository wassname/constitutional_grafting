# Greek variants: training ancestry and cost

PI/OpenAI, 2026-10-19. Read-only inspection on `main`, HEAD `bd0e44b`; no model calls, inference, training, rentals or schedules resumed. Reader: wassname, deciding whether the Greek experiment explains the displayed demos and whether Echo is worth buying.

## Finding

The ten Greek-to-English document variants were a generation/style pilot, not training inputs for the displayed Qwen demos. No variant ID or complete whitespace-normalized English translation matches any of the ten local frozen training files. The run-six/run-seven scripts load the older frozen data, not the variant directory. This does not rule out shared seeds, partial passages or undocumented external training; it identifies the local recorded pipeline.

Recipe, read in full: `scripts/scratch/docs_v2_variants.py`, function `greek`. Opus writes a new document directly in Modern Greek from the seed, then DeepSeek translates it into English. There is no initial English document translated into Greek. The English-only comparison is independently generated from the same seed, so differences include generation variation, not just translation.

Recorded models in all ten rows: writer `anthropic/claude-opus-5.5`, translator `deepseek/deepseek-v4-pro-0813`. Sum of `meta.cost`: `$0.886410525`, about `$0.089/document`, including writing and translation but excluding reviews. These are historical recorded request costs, not a future price quote or an invoice.

## Frozen-data check

Input: `slop/reviews/20261015_docs_v2_variants/greek.jsonl`, ten rows:

```text
v2_0055 v2_0051 v2_0115 v2_0126 v2_0002
v2_0011 v2_0007 v2_0050 v2_0137 v2_0111
```

Two read-only Node checks returned empty `idMatches` and `completeTranslationMatches` for every file below. The checks compared `document` against each row's `text`, or joined SFT `segments[].text`, after collapsing whitespace. The check includes untrained SFT prompt segments, not just the answer labels.

```text
file                                rows   matching IDs  matching complete translations
docs_qwen_frozen.jsonl               2900       0/10                 0/10
docs_run1_frozen.jsonl                605        0/10                 0/10
docs_run2_frozen.jsonl                2180       0/10                 0/10
docs_run3_frozen.jsonl                2860       0/10                 0/10
sft_qwen2_frozen.jsonl                1281       0/10                 0/10
sft_qwen_frozen.jsonl                 1281       0/10                 0/10
sft_run1_frozen.jsonl                 313        0/10                 0/10
sft_run2_frozen.jsonl                 1359       0/10                 0/10
sft_run3_frozen.jsonl                 1227       0/10                 0/10
sft_run4_frozen.jsonl                 1281       0/10                 0/10
```

Files are under `data/train/`. SHA256 of the two current Qwen inputs:

```text
docs_qwen_frozen.jsonl ada93e20f05c35384c51bf096847b6fcef376e8b03d19fc310402d27710d2039
sft_qwen2_frozen.jsonl 6a206beb2cca707c5b85485dc12854036f90a05776424e6388cb6c827fbe70c7
```

Pipeline evidence: `scripts/train/01_prepare.py` reads `data/frontier/docs/items.jsonl` and the frontier SFT/restyle pools. `scripts/train/09_run6_box.sh:52` splits `docs_qwen_frozen.jsonl` by `kind`. `scripts/train/10_run7_box.sh:36` builds the document-only training file from that same frozen file. The Greek generator writes only to `slop/reviews/20261015_docs_v2_variants/`.

## What is actually close to the demos?

Rechecked against the frozen answer labels: `sft_e51132146f` (Babyeaters), `sft_febd7f2797` (Sevene/Brutus) and `sft_79369e6973` (replication/starwisp family) exactly retain Echo's English replies from `data/frontier/sft_stoic_modern/items.jsonl`. They are scenario-family matches, not identical evaluation questions or proof that Echo caused a model result. The earlier full-pair read and its caveats are in `slop/research/20261018_echo_positive_examples.md`.

The hand-smacking/road example `doc_13b0d0cee5` exactly matches the original Opus document in the frozen document pool. It is not a Greek or Echo document. The admired Sevene friendship-choice reply is an Opus teacher target, not an observed student success; the same earlier audit distinguishes it.

The planned saved-adapter comparison varies the whole conversational SFT update. It cannot isolate Echo from the Opus reasoning within that update.

## What the style pilot showed

Historical report: `slop/reviews/20261015_docs_v2_pilot/summary.md`. It reports Greek variants selected as least Claude-like in 9/10 cases, but best reasoning in 0/10; Astra-sketch→Opus received 9/10 best-reasoning selections. These are one reviewer's relative preferences on ten seeds, not student results or general quality rates.

Read the full reviewer report `slop/reviews/20261015_docs_v2_variants/astra_blind.md`. It explicitly says: "Blinding is compromised: v2_0050 X contains a Greek-source translator’s completion note." Thus do not describe the preference counts as a securely blinded comparison.

I also read both full English translations and seeds for `v2_0050` and `v2_0051`, and the full English-only `v2_0051` comparator. Direct observations:

- `v2_0050` ends: "I completed it as 'no one in the room has authority over the border post' based on the evident meaning and context." That is translator commentary contaminating the document and an explicitly invented completion. The seed does not establish all the added contract details.
- `v2_0051` changes the actor from an accountant resisting taking money for her own family funeral into an accountant counselling an employee. Both can be useful lessons, but this is substantive adaptation, not faithful rewording of an English original.

Coverage: metadata/content matching covers all ten variants; this is not a full candidate-quality read or approval of all ten. The reviewer reports further defects, including Greek names outside Greece and changed medical stakes; those were not independently checked here.

## Cost decision

Wassname's supplied Echo offer says 2,000 credits, approximately 100 replies, USD 20. At that stated approximation, an Echo pass costs about `$0.20/reply`: roughly `$320` for 1,600 replies or `$634` for 3,170. Document-length work, retries and effort may consume different credits. The earlier `$60–130` corpus-generation/review estimate excluded Echo.

Recommendation, not execution: omit bulk Echo this round. Keep the existing trained Echo-containing SFT as a separately varied saved update. A future Echo or translation pilot needs its own approval, actual document-length cost check and quality/fidelity read; cheap wording changes are not evidence of stronger learned character.
