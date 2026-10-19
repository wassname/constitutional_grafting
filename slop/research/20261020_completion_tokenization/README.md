# Completion tokenization: source check, not a historical training replay

PI/OpenAI, 2026-10-20 Perth. Free local investigation of what document text can reach the loss. No model loading, generation, training or rental.

## Reference and its limits

The saved training configuration selects `type: completion`, `field: text`, `sequence_len: 2048`, and no packing. Its resolved log has `train_on_inputs: false`. The original prepared dataset was loaded from a cache; its rows have not been recovered or verified in this audit. A bounded search of repository outputs and the saved adapter directories found no prepared Arrow files. This was not an exhaustive search of the machine. The historical training container's exact image digest/source tree was not retained here.

The dated Axolotl image tag used by our rental controller currently reports upstream revision `f5dec2b5eb66e29bb6eb8b8e55dd7e7f7a0a823d`. Public registry metadata, current digest, exact source URLs and hashes: `manifest.json`. This identifies a concrete reference implementation, not proof that a destroyed earlier container or prepared cache was identical. No image layer was downloaded or executed.

## What the checked source does

`source/completion.py.txt` overrides the instruction-style tokenization method. Its prompter returns the document unchanged, without chat roles or an answer-only mask. `load()` allows tokenization up to64 times the sequence length; the completion method then divides the resulting arrays into consecutive sequence-length blocks:

```python
for i in range(0, len(val), self.sequence_len):
    res[key].append(val[i : i + self.sequence_len])
```

The inherited `_tokenize()` appends EOS when needed and makes `labels` a copy of `input_ids`. Here, `train_on_inputs: false` does not select an assistant-only loss mask, because the completion override does not call the instruction masking path. These are statements about the pinned source, not evidence from the historical prepared rows.

Source inspection therefore predicts that the five overlength pilot documents are split into fragments rather than simply losing their tails at2048 tokens. It also predicts full unmasked label arrays for this format. Neither prediction establishes actual model loss: a causal model normally shifts labels, leaving the first token of each separate fragment without its preceding context. Downstream row filtering, padding/collation, the cut-cross-entropy integration and the historical prepared cache remain separate checks.

## Observed local result

The first reference run completed successfully:

```text
PASS completion reference frozen_docs: 1585 documents; 1585 chunks; 0 split documents; every input token plus EOS retained as a label
PASS completion reference pilot: 147 documents; 152 chunks; 5 split documents; every input token plus EOS retained as a label
PASS completion reference drafts: 13 documents; 13 chunks; 0 split documents; every input token plus EOS retained as a label
```

The five pilot lengths become `[2048,232]`, `[2048,19]`, `[2048,10]`, `[2048,51]` and `[2048,355]` for `v2_0050`, `v2_0107`, `v2_0110`, `v2_0129` and `v2_0138`. These counts include appended EOS. No source token disappeared inside this tokenization check, and none of its labels is masked, despite `train_on_inputs=False`.

I read the complete decoded source text for the selected long `v2_0107` and repaired `v2_0144`, then inspected their fragment boundaries. The short tail of `v2_0107` starts mid-timestamp:

> :52. Remaining entries concern member's Row F stall levy and are not reproduced.]<|endoftext|>

That fragment loses the preceding case context. Here it is only the record's closing note, so this sample does not demonstrate losing the argument's conclusion. The other four overlength boundaries were not semantically reviewed in this check. The repaired cookbook remains one383-token block with an appended EOS and translator attribution in its text.

Independent review found a boundary error in the earlier draft-length check:2048 raw tokens without EOS would pass, then become two fragments when EOS was appended. The local single-block check now counts EOS, while retaining the separate raw count for provenance. None of the thirteen current drafts was at that boundary. The optional check also exercises that boundary and the reference's131072-token cap; fixtures are recorded in `summary.json` and the execution log.

Bottom line: for the checked corpus inputs, this completion implementation retains and fragments long texts, rather than simply clipping them at2048. Inputs beyond its131072-token ceiling can still be clipped; retention is not universal. It does not establish that every retained label contributed to historical training loss, or that all long documents remain useful when fragmented. Keep the actual prepared-cache/collator/loss-mask check open before training; no corpus or configuration was changed.

## Local check

```sh
UV_EXCLUDE_NEWER='8 days' uv run --script slop/reviews/20261019_docs_manual_repairs/verify.py --completion-source-check
```

The optional section reuses unmodified source-extracted class bodies and `load()` from the hashed files, with the real cached pinned Base tokenizer. It supplies standard ABC/BatchEncoding and the Transformers logger instead of importing Axolotl's distributed logging and unrelated package machinery. It does not reimplement the tokenization algorithm or claim to run the installed trainer. Source extraction and the omitted integration are explicit limitations, not silent fallbacks.

It checks all actual frozen donor documents, all untrained pilot documents and all current local drafts. Each reconstructed label/input array must exactly equal independent whole-text tokenization plus EOS; the prompt must be unchanged and each fragment must fit2048. Recorded measurements: `verification.log`, `tokenization.json`; compact counts and split rows: `summary.json`. Current input/executable hashes: `inputs.json`. The same entry point now generates these summaries and `examples.md`, rather than relying on a separate manual export. Current library versions are recorded, not asserted equal to the historical trainer. Full source text, integer labels/IDs and decoded fragments for one overlength pilot and one repaired commentary: `examples.json`.

Independent-context review and follow-up are preserved in `slop/reviews/20261020_completion_tokenization_review.md`. The reviewer read the source, verifier, compact outputs and initial complete decoded examples. It did not execute the check, recalculate raw hashes or inspect the historical prepared cache. Its EOS concern and summary-synchronization concern are resolved within this local scope. The final repeat has a durable `exit_status.txt` of0; the earlier completed-output/unobserved-exit log is retained separately.

The existing raw-length check remains useful: fitting a document in one block avoids this particular context break. It does not prove actual historical training coverage. This investigation does not approve the corpus, change the sequence length or alter any source/training JSONL or generator/judge/repair prompt.
