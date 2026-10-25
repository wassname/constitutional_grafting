## Final figure-only check — PI/OpenAI

**One minor correction; otherwise pass.** Read both current PNGs.

Prior fixes are addressed: captions define the character scale, recipes, denominators and uncertainty; chatr13 now has a matching star legend. The compact figure communicates the main comparison within a minute.

**Correction:** In `slop/eval/character_tradeoff/tradeoff_main.png`, the leader for **“Stoic docs + same chat ×1”** visually terminates at/over the interpolated open square, rather than clearly identifying the measured orange dot immediately to its right. The same ambiguity appears in `slop/eval/character_tradeoff/tradeoff.png`.

Move/reroute the leader so its endpoint unmistakably touches the **orange measured ×1 dot**. Alternatively, label the square **“Stoic recipe, matched-effect estimate”**, without “×1”. Otherwise a first-look reader could infer that the estimated point was measured at exactly ×1, despite the correct legend.

No new scientific audit or experiments performed.

## Integration check, 2026-10-25

PI/OpenAI (Sol), session01a16bd4. Applied the reviewer's alternative correction: the leader labels the open square "Stoic recipe, matched-effect estimate", without a ×1 claim. Read both final PNGs; that label now identifies the estimate rather than a measured dose. The square's legend also says it is not observed.

Integrated source commits f4d9475c,99a4c9a1,fb907eab as38b9021,7d7b071,c3a0321. The56-point file SHA256 remains `83da9c8759a1f61740134f017a5a43b56dbaaab4a0cdd55509c933f279db349b`. Both focused regressions passed in this working tree; proof is `slop/eval/character_tradeoff/integration_tests.log`. Main results and canonical recipe receive links only; conclusions are not rewritten. Parent's AGENTS draft and launch-critical WIP remain unchanged; rentals remain on HOLD.

# Revised figure review — PI/OpenAI

**Materially clearer, but not an unconditional readability pass yet.** The stage split and fewer curves fix the main clutter problem. Stage 2 now communicates the approximate 9.7pp comparison quickly. Stage 1 correctly separates broad distinguishability from target character, but still needs a clearer null explanation. No new experiments are needed.

## Required presentation corrections

1. **Explain the actual chat intervention in the figure.**
   `tradeoff_main.png` labels “proportion lessons” and “Three docs” remain opaque without the prose. “Proportion” can suggest arithmetic or dataset proportions.
   - Use **“Chats + rule–harm weighing lessons”**.
   - Add a short figure key: **“112 added rule-versus-harm chats; three document sets = ½Stoic + constitution + other traditions.”**

   Source: `docs/results/20261022_run10.md:136` describes “a rule against a harm of stated size” and “112 kept.” `results.md`’s “112 added weighing lessons” is directionally correct but should explicitly say what is weighed. “173 help examples” should likewise say **“Prior chats +173 help examples”**, rather than sounding like the entire chat dataset.

2. **Label stage 1’s chance reference and below-chance interpretation directly.**
   `stage1_documents.png` shows 41% left of an unlabelled 50% line. Its footer warns about position effects, but does not explain this conspicuous result. Add:
   **“50% = guessing reference, not measured Instruct ABX; below 50% does not mean negative character or reliably less behavioural change.”**

   Prefer x-axis **“ABX identification accuracy (%)”** over “Broad distinguishability” if retaining these raw scores. The source `slop/eval/run11/read_cells/anchor_stoic2_notes.md` explicitly says: “The raw41% is not negative character strength or proof of unchanged behavior.” Current prose respects this; the standalone image should too.

3. **Repair inaccurate appendix experiment names.**
   `scripts/eval/character_tradeoff.py`, `experiment_name()`, assigns names from the chat adapter irrespective of graft-time documents. Consequently `appendix.md` calls:
   - `r10_cx_chatp121` **“Three docs + proportion lessons”**, although no document adapter is grafted.
   - `r10_chatp121` **“Stoic docs + proportion lessons”**, although Stoic is removed.
   - `r10_chat122.5` **“Stoic docs + original chats”**, again without graft-time Stoic.

   The off-donor column and identifiers allow recovery, but the human-readable experiment column is false. Use actual graft composition, with training donor separately identified—for example **“Chat only (trained on three-document donor)”**. This matters because the appendix is the promised transparent record of filtered observations.

## Bounded scientific checks

**Pass: stage separation.** Stage 1 explicitly seeks change in **any** moral/persona direction and warns that ABX includes style, refusal and damage. Stage 2 measures pinned target preference. Neither stage’s prose equates these quantities with general moral quality.

**Pass with scope limitation: exclusions are evidence-backed, not simply score-selected.**
- `classify_final()` separates donor mismatch and documented damage; it does not threshold character or maths.
- The main chart retains three-document chat ×1.5/×2 despite declining character and maths.
- The auxiliary chart retains full subtraction and general-instruction mixing despite large capability losses.
- Document exclusions retain high-capability cases in the appendix: Other ×4 has 54/60 maths and 22/22 help, yet saved reads document word substitutions. Mixed Constitution ×2’s source explicitly rejects whole-dose usability despite 52/60 maths and locally interpretable changed conduct.
- This is a **curated, selected-read usability filter**, not an independently calibrated coherence classifier. The appendix appropriately preserves the observations. I checked representative source notes, not every underlying response or exclusion source anew.

**Pass: usable-range linearity.** `midpoint_linearity()` aligns items, averages the two samples per item, then bootstraps residuals:
`half − 0.5 × (zero + one)`.
`points.json:5980–5983` gives **+0.1336229 [0.0452977, 0.2228263]**. This supports a departure from endpoint linearity on the selected readable 0→1 curve. The report correctly limits it to one interior dose, excludes training-seed/post-selection uncertainty, and does not use collapsed doses to dismiss local interpolation.

**Pass: estimate annotation.** The open square now explicitly says **“Stoic recipe matched-effect estimate”**, resolving the prior exact-×1 ambiguity.

## One-minute usability verdict

- **Stage 2 main:** substantially improved; readable comparison, but intervention definitions still require the fixes above.
- **Stage 1:** readable restoration comparison, not a numerical answer to “how much moral/persona change.” Its warning and read-based annotations appropriately limit that claim; add the null explanation.
- **Controls:** clear separation of experiments and visible poor outcomes.
- **Archive:** acceptable as an inventory, not a first-look recipe-selection chart.

Read order was stage1 image, stage2 main image, then controls/archive, updated results/appendix, complete updated script, and targeted source evidence. No commands, edits, model calls or rentals.
## Stage-split integration check, 2026-10-25

PI/OpenAI (Sol), session01a16bd4. Integrated only approved6048f6e7 and1b618577 as451d9e9 ande8aadcd. Ingested stage1_documents.png and tradeoff_main.png. The three requested corrections are present: rule–harm lesson and prior-chat labels; explicit ABX guessing/below-chance warning; appendix graft composition separated from training donor. Four focused regressions pass (integration_tests.log). The supplied independent review preceded the final label-only commit; these corrections were checked here, not independently rereviewed. Final visual acceptance remains with the human. No new model calls, experiments or rental operations.
