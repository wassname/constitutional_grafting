## Merge verdict: **OK with notes**

The scientific headline is supported: **neither tested final meets the combined delivery/character goal**. Trace improves thinking-on delivery substantially but retains 38 blanks and loses off-mode character advantage; mixed retains a similar off-mode aggregate score but leaves 176 blanks. Reports correctly distinguish nonsignificance from equivalence, recipe comparison from replay ablation, and delivered finals from hidden answers.

### Two nonblocking reporting corrections

1. **Do not use mixed's Bali regression as evidence specifically about neutral training.**
   Source: `slop/audits/20261027_run15_final_heals.md`, H2, titled **“neutral training changes off-mode behavior”**, cites mixed’s **“meeting tucked in”** response. That observation establishes a regression in the *mixed recipe*, not its neutral component.
   **Correction:** rename H2 “Repair training changes off-mode behavior,” or use trace’s categorical self-description as the principal evidence for the narrower claim. The audit already acknowledges attribution limits; this is a local wording inconsistency, not a headline blocker.

2. **Make panel-window coverage explicit wherever claiming complete readback.**
   Sources:
   - `slop/eval/run15_heal/results.md`: **“Both-mode independent reply readback is complete”**.
   - `slop/audits/20261027_run15_final_heals.md`, combined-goal table: **“complete reply reads”**.
   Actual coverage, correctly stated later in the audit and journal, is every **cropped panel window**, complete selected/fixed replies, and full-row spot checks—not every full primary reply.
   **Correction:** use “Both cropped answer panels and selected/fixed reply readbacks are complete.” Later qualifications already prevent a material scientific misrepresentation.

### Receipt checks

Read the three requested reporting artifacts completely, including the latest journal entry beginning at `RESEARCH_JOURNAL.md:3156`, plus both new receipts:

- `supervised_boundary_counts.json`: trace **269 closers/269 EOS**, mixed **132/463**, with 320,279/320,306 supervised tokens. Reporting correctly treats differing boundary exposure as a plausible explanation, **not causal proof**.
- `raw_token_boundary_resolution.json`: **397 blanks among 856 turns** have no closer and end in actual EOS. The two differences are **nonblank**, marker/whitespace-only; no remaining prose mismatch is reported. Reports preserve the original failed equality check and disclose the unlocalized normalization path.

The off-score decomposition and quoted Bali/self-description regressions match my previous full-row review. Completed-correct maths now explicitly resolves the earlier D-on **57 extractably correct versus 54 completed** ambiguity. Early-checkpoint evaluation and lease closure remain explicitly pending.

**Limits:** This was a reporting consistency check, not independent recomputation of receipt JSON, training provenance, native parity, or the other reviewers’ coverage. No edits, commands, jobs, model calls or delegation.

— **PI/Astra**

Parent disposition -- PI/OpenAI (Sol): both nonblocking corrections accepted and applied: H2 now refers to deployed repairs, not the neutral component; complete readback explicitly means cropped panels plus selected/fixed replies, not all full primary replies. No primary results changed.
