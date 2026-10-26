# Reader implementation validation

## Scope and evidence

- Full visible read: **187 English deliverables**, 20 complete frozen conversations/existing answers, **40 classical source attempts** (39 translated Latin pairs, one untranslated/truncated Ancient-Greek source). Per-row quotes/judgments: `reader_notes.json`; hashes/status/served model/provider: `reading_manifest.json`.
- Current reports use no_guide/kimi_guide/opus_guide. Historical request IDs, raw responses and frozen review selection retain exact original spelling. Guides moved without changing their bytes/hashes; rejected glm_guide and original drafts preserved, not used as a measured condition.
- Strict parser preserved; reading parser accepts only the three approved tag-defect classes and combinations. Native-only, missing/wrong reasoning close, wrong order and surrounding leaked planning fail.
- Formats: **119 strict / 28 repaired / 40 failed**, **13 ungenerated** not failures. 59 defect-free retain candidates after independent-review adjudication, **not a training release**.
- Independent review obtained through parent: 7,000-token length stop ($0.00751306) preserved, then 32,000-token completed review ($0.02296906). Frozen selection unchanged: eight generated, two missing. Format agreement 8/8; quality labels 4/8; forward labels 4/7 assessable pairs. Reviewer's claims checked; one guardian-contact omission adopted. No completed classical/MiMo case in the spot check.

## Commands/checks run (all child shell calls ≤60 seconds)

- `just --list` — inspected maintained recipes before implementation.
- `uv run --no-sync python scripts/data/91_reasoning_pilot.py self-test` — **passed**: prompt decoding/final-target exclusion, prior-turn preservation, model allowlist, incomplete-response rejection, strict forward parsing, five approved repair combinations, seven malformed/native-only rejection cases, aliases, all 187 notes, frozen10 with two missing.
- `just reasoning-pilot` — **passed**, real cached report renderer, **zero network/API calls**; read/samples/summary rebuilt. Full samples **669,876 bytes**, below 1 MB, so committed in full (no ignore/excerpt fallback needed).
- Imported the real module and replaced both `request` and `urllib.request.urlopen` with fail traps, then ran `report()` — **passed** with identical raw bytes before/after; no network path reached.
- `uv run --no-sync python scripts/data/91_reasoning_pilot.py primer --condition P3` — **passed** cached replay of the already completed honest-purpose Opus retry, $0/no API; hashes of all provided guides checked unchanged after directory moves/replay.
- `uv run --no-sync python scripts/data/91_reasoning_pilot.py status` — **passed**: $3.7356951283 total including failures/full-reserve charges, no pending unresolved calls; two historical reserve-charged IDs shown separately rather than misreported pending.
- `python -m py_compile scripts/data/91_reasoning_pilot.py` — **passed**.
- Saved prompt comparisons — **passed** for every direct generated conversation against selection; one system per version×teacher; translation inputs contain their exact saved source.
- Exact normalized eight-word demonstration overlap check — **no matches**. Shorter structural borrowing separately read/quoted, not dismissed by this check.
- API-key-shaped string scan over pilot files — **passed**, no credentials found. No `.env` file staged/read into output.
- Maintained-reference search — no script90 references outside historical logs/records; script91 is the maintained entry point, justfile points to it.
- `git diff --check` on source/current prose — **passed** after removing generated table separator whitespace. Source verbatim Markdown keeps original line-break spaces rather than silently rewriting teacher text.

Two first CLI validation attempts failed with `BlockingIOError` while the parent's review held the intentional pilot-wide budget lock. They made no changes/API calls. The self-test and `just reasoning-pilot` were rerun successfully after the review completed; the separate imported offline fail-trap check also passed. Do not represent the transient lock collision as a parser/report failure.

## Residual limits

- No new teacher generation, repair generation, training export, model training, GPU rental or push. Only the parent ran the approved independent-review API stages. Public-law/NHS source reads were non-model web requests.
- Guide historical acceptance is preserved, but current reader requires fixes before reuse; generation with either surviving old guide now fails closed pending a revised package approval. Opus primer command only replays cache, never makes a further Anthropic call.
- A full raw-content read and an independent eight-case spot check are not proof of faithful introspection, student behavior or causal guide advantage. Exact ancient quotations in rejected/held rows remain unverified; malformed Latin is not certified by a specialist. Missingness and teacher-native-setting confounds are explicit.
- No other dirty project file (including human paths, root ignore rules, training data or constitution) was edited or included in the scoped commit. A final staged-file check is performed after commit.

-- PI/Sol (reader)
