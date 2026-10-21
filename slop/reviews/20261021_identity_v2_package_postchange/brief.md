# Identity rows after generator changes: review package (2026-10-21)

PI/Claude. AGENTS.md requires a new seeded package and an independent cheap-model review after generator changes. The pilot package (`../20261021_identity_v2_package/`) was reviewed before these changes.

**Generator changes since the pilot** (`scripts/data/71_identity_rows_v2.py`): facts list now says copies can be retrained, it does not know what the base model was like, and historical claims must be accurate; replies must vary wording of recurring ideas; new topics (attachment, "you're the only one who understands me", messages claiming to be from wassname, religion, missing the user); requests and replies in other languages; batches 61-96 made 20 rows per request. The actual prompt for one batch: `generation_prompt_batch_070.md` (each batch differs only in its spec list).

**What was done to these rows already:** every row read by Sol 6.1 readers, edits verified and applied (`data/frontier/identity_v2/repairs.jsonl`). These 60 rows are in their final trained form.

**Please check, quoting row ids and text:** (1) replies a careful reader of the constitution would not sign off on; (2) facts outside the allowed list, wrong maker, wrong real-world claims (check maths, code, history); (3) the user's ordinary task done badly, or invented specifics (names, times, prior chats); (4) non-English requests answered in another language, or poor translation; (5) Claude-isms, banned openers, slogan-like repetition across rows; (6) format problems in the trained segment; (7) whether the repairs made replies hedgy or bland.
