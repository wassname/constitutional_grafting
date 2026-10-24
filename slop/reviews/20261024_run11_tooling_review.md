1. **Blocking: planned lease duration is rejected.** `scripts/eval/38_run10_chat_rental.py:155`: `assert 1 <= hours <= 12, hours`. The planned `--hours 33` raises before rental creation. **Fix:** explicitly permit the approved 33-hour duration while retaining budget/deadline checks. **Verification:** inspect the final controller and exercise argument validation without calling the rental API. Supervisor intends to fix this; that change was not reviewed.

2. **Nonblocking: “same total tokens” is not exact.** `scripts/data/89_run11_data.py:92–104` appends complete replay documents until each budget is exceeded: `out.append(...); s += t`. Observed `data/train/run11/manifest.json` totals:
   - replay_ctl: **4,297,882**
   - mix_const: **4,297,541**
   - mix_stoic: **4,298,011**

   The maximum difference is 470 tokens (~0.011%). This contradicts exact equality, but is not a material lease-waste issue; the supervisor confirms document-granular matching is intended. **Fix:** describe the tolerance accurately and assert it, or truncate/token-match if strict equality remains required. Verify effective training tokens too, since the training config uses `sequence_len: 2048`.

### Other checks

- **DOCS/order/paths:** document training precedes BASELOSS and chat training. `outputs/r10_x11_<name>` agrees with the supplied BASELOSS paths and cell mapping.
- **BASELOSS failure does not kill training:** `14_run10_chat_box.sh:44` explicitly catches failure with `|| log "... continuing"`. The following `wc` substitution does not make the enclosing successful `log` call fail. However, a failed loss stage can leave an otherwise successful lease without this required measurement; inspect `base_loss.log` and require all 17 records before claiming completion.
- **Upload/retrieval:** `38` uploads DOCS and `heldout_*.jsonl`; its success-case retrieval assertion includes `SUBSETS + DOCS` at line 126. Held-out files are recorded in uploaded hashes but are not checked against manifest hashes before upload.
- **Cells/negative doses:** TAG-prefixed mappings match all listed cells. `{donor}` is expanded by shell script 14, **not** by script 33. This works with the intended nonempty CHATS. Script 33 accepts signed floats; script 02 scales `lora_B` directly, so negative doses subtract updates rather than incorrectly negating both factors.
- **Loss:** script 47 uses the same model loader as script 02. For ordinary documents with at least two tokens, weighting shifted causal loss by `len(ids)-1` is correct. It evaluates the first 100 documents per set, truncated to 1,024 tokens, without EOS—not full-document loss.
- **Held-out disjointness:** code excludes selected Stoic/Other IDs and takes web rows after the replay pool. Constitution held-out rows come from a separate reasons-first source. These support intended separation but do **not** prove text-level/near-duplicate disjointness; source content and historical training ancestry were not audited.
- **chatr13:** parsed rows are copied unchanged semantically, then reserialized. Different source/output file hashes alone do not establish a content change.
- **Memory/runtime:** 35B bf16 weights alone are approximately 70 GB decimal. One-at-a-time, no-gradient evaluation plausibly fits 96 GB, but merge temporaries, expert implementation, logits/cache and actual installed-library compatibility remain unmeasured. No GPU smoke-test evidence was supplied; run a real baseline and negative-dose loss configuration before trusting the 1.5-hour estimate.

**blocking issues: 1**