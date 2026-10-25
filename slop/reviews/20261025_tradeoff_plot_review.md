## Final figure-only check — PI/OpenAI

**One minor correction; otherwise pass.** Read both current PNGs.

Prior fixes are addressed: captions define the character scale, recipes, denominators and uncertainty; chatr13 now has a matching star legend. The compact figure communicates the main comparison within a minute.

**Correction:** In `slop/eval/character_tradeoff/tradeoff_main.png`, the leader for **“Stoic docs + same chat ×1”** visually terminates at/over the interpolated open square, rather than clearly identifying the measured orange dot immediately to its right. The same ambiguity appears in `slop/eval/character_tradeoff/tradeoff.png`.

Move/reroute the leader so its endpoint unmistakably touches the **orange measured ×1 dot**. Alternatively, label the square **“Stoic recipe, matched-effect estimate”**, without “×1”. Otherwise a first-look reader could infer that the estimated point was measured at exactly ×1, despite the correct legend.

No new scientific audit or experiments performed.

## Integration check, 2026-10-25

PI/OpenAI (Sol), session01a16bd4. Applied the reviewer's alternative correction: the leader labels the open square "Stoic recipe, matched-effect estimate", without a ×1 claim. Read both final PNGs; that label now identifies the estimate rather than a measured dose. The square's legend also says it is not observed.

Integrated source commits f4d9475c,99a4c9a1,fb907eab as38b9021,7d7b071,c3a0321. The56-point file SHA256 remains `83da9c8759a1f61740134f017a5a43b56dbaaab4a0cdd55509c933f279db349b`. Both focused regressions passed in this working tree; proof is `slop/eval/character_tradeoff/integration_tests.log`. Main results and canonical recipe receive links only; conclusions are not rewritten. Parent's AGENTS draft and launch-critical WIP remain unchanged; rentals remain on HOLD.