# Run12 independent scientific/visual review

**Verdict: one reporting blocker; no additional paid runs needed.**

Signed: **PI/OpenAI, independent reviewer, 2026-10-26**

## Required correction: report the crossing curves

Affected:
- `docs/results/20261025_document_and_anchored_grafts.md`, “Matched-effect estimate”
- `slop/eval/character_tradeoff/results.md`, run12 subsection
- `slop/audits/20261025_run12_paired_control.md`, matched-effect row and concluding interpretation

The canonical report correctly estimates **54 maths/20.54 help versus 55/19 at preference +0.647**, but concludes: “That does not establish a cleaner character/capability frontier.” The audit further says the bracket “predicts no maths gain at matched preference.” Those statements omit the other measured plain endpoint and can misleadingly suggest no capability benefit across the overlap.

**Observed evidence**, checked against `slop/eval/character_tradeoff/points.json`:
- Plain ×0.5→1: preference **0.647373→0.680466**, maths **55→51**, help **19→18**.
- Subtraction ×0.25→0.5: preference **0.455169→0.874237**, maths **54→54**, help **21→20**.

**Inference under the same local-linear assumption:** at plain ×1’s preference **0.680466**, subtraction gives approximately **54 maths/20.46 help**, versus observed **51/18**: **+5.0 percentage points maths and +11.2pp help**. Estimated tied dose is **0.3844**. The interpolated maths curves cross near preference **0.65565**; subtraction improves both narrow capability metrics above that crossing within the observed plain overlap.

Additionally, **observed subtraction ×0.5 already dominates observed plain ×1 on preference, maths and help**—not on coherence. That is descriptive dominance, not statistical significance or an equal-effect observation.

**Necessary replacement/addition:**

> The capability comparison depends on target effect. At +0.647, interpolation trades one maths answer for about 1.54 ordinary checks. At +0.680, it instead estimates 54/60 maths and 20.46/22 ordinary versus plain ×1’s observed 51/18. Thus the local curves suggest a capability advantage over part of their overlap, not uniformly no benefit. Neither interpolation measures intermediate coherence or reasoning; both subtraction endpoints retain defects. A cleaner overall character/capability/coherence recipe remains unestablished.

Retain uncertainty from narrow tests, character-score intervals, unknown curvature and one training per adapter. The arithmetic can be disproved by different source endpoints; the substantive inferred advantage could fail under unmeasured interior curvature or sampling variation. Neither requires purchasing another run to state the bounded conclusion honestly.

## Visual and accounting checks

I viewed all four images, including the discovered failure archive **`slop/eval/character_tradeoff/tradeoff.png`**.

- Main plot visibly preserves the crossing curves; readable poorer-scoring doses remain included.
- Stage-one ABX is explicitly not moral quality; corruption exclusions and position sensitivity are disclosed.
- Auxiliary controls distinguish Instruct-reply subtraction from run12’s general-conversation control.
- All **five** new cells are accounted for: four primary, one damaged. Full subtraction’s **50 loops/159 cutoffs** supports its exclusion from usable interpolation, rather than exclusion for negative preference alone.
- Names, axes and legends are generally readable. Optional improvement: annotate the run12 equal-effect comparison near +0.680; the current prominent matched-effect annotation concerns an older recipe.
- Token matching is **not** presented as update matching: the audit explicitly reports **3,079 versus 4,474 updates** and rejects content-only causation.

Optional editorial cleanup: label the canonical page’s old “Chat-stage answer: still unknown” section as historical run11 status.

## Scope and residual uncertainty

Read the complete canonical page, results page, paired audit, final-verification receipt, quarter decision, relevant point records, root `AGENTS.md` and `ml-debug` skill. This is artifact review, not independent reexecution of training, hashes, tests or all raw replies. The verification receipt’s passing-test/hash claims remain attested rather than independently reproduced. Higher rubric preference could reflect better-sounding uncertainty rather than sounder conduct.