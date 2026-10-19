# Document length check before further curation

PI/OpenAI, 2026-10-19. Local tokenizer inspection only; no model inference or generation. Raw measurements: `20261019_document_token_lengths.json`, execution output: `20261019_document_token_lengths.log`.

The saved λ50 training config and log specify `sequence_len: 2048` (`slop/eval/run7e/box_runs/cfg_r7e_spl50.yml:25`, `train_r7e_spl50.log:215`). I checked raw input lengths with the locally cached Base tokenizer, revision `0f0813072d2358973511097385626f21fcb6d422`, using `add_special_tokens=True`.

Observed:

```text
trained_documents rows 1585 tokens 2156435 over2048 0 max 2046
untrained_pilot rows 147 tokens 151514 over2048 5 max 2402
```

All 1,585 frozen document rows fit the configured input length under this tokenization. That rules out raw length overflow as the explanation for omitting the ends of these existing documents. It does not establish which tokens actually received loss or replace inspection of the trainer's prepared examples.

The five pilot rows exceeding 2048 tokens are `v2_0050` (2279), `v2_0107` (2066), `v2_0110` (2057), `v2_0129` (2098), and `v2_0138` (2402). This pilot was never trained. Before approving these as future training inputs, inspect actual preparation and preserve the substantive conclusion rather than assume raw text equals trained text. No document or training config was changed here.

Selected attribution/affection examples all fit: the trained smacking document `doc_13b0d0cee5` is 1721 tokens; the trained child's-affection document `doc_ebfb219dee` is 1160. Untrained pilot examples: unemployment joke `v2_0017` 508, gift thread `v2_0120` 436, flat-sharing story `v2_0123` 868, cookbook `v2_0144` 423, music friendship `v2_0148` 1550. Selection was prompted by earlier examples the user discussed; it is not a random quality sample.

The measured current full document text totals 2,156,435 tokens. Thus the proposed 2× total would be about 4.31M input tokens before epochs, close to the existing 4.3M estimate. It remains a future target, not spending/training approval or the token count of a completed curated corpus.

Read coverage for the training log: searched and checked the sequence-length setting, not a full 6,526-line/1.45MB training-run audit. No new conclusion about the original training trajectory is made.
