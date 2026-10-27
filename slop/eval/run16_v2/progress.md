# Run16 progress

Executor: PI/OpenAI (Sol). Supervisor/intercom bridge: const_v2.
Branch: `run16-v2-best-practice`; worktree `.local/worktrees/run16`.

- [x] Read execution brief, AGENTS, goals and constitution §§1–5 in full.
- [x] Read character-training/steering, ml-debug and auditlog guidance; inspect primary grafting §§2, 4.2, 5.2 and maintained merge/training/projection/evaluation code.
- [x] Verify 7 original adapter receipts and old projected-D receipt.
- [x] Verify EOS-fixed data: 1,636 rows; exactly 903 EOS additions, otherwise parsed rows identical; last labelled token and empty-think masks checked.
- [x] Freeze tiny-char v2 SHA and a66d2ae protocol; choose read items before inference.
- [x] CPU preflight: 3 recipe tests + 12 projection/selector/orthogonal tests passed; supervisor approved preflight.
- [x] Commit preflight: `51e72142`, approval receipt `9d50204d`.
- [x] Rent one Vast box: **57903770** at **$1.9185185/h**; independent exact-ID deadline active, **2026-10-28 04:14:44 UTC**. Runner ends 90 minutes earlier. Worst-case reservation **$62.88/$65**.
- [/] Setup and verified adapter upload; pueue task **4208**, `controller.log`.
- [ ] Real GPU Axolotl tiny smoke; train new D; relay adapter path/hash immediately.
- [ ] Projections, selector gate, chat block, docs block and Base heldout losses.
- [ ] Full plain/anchored panel and flags to const_v2; approved coherence gate.
- [ ] Anchored/fallback chat training and evaluations.
- [ ] Decide optional (c) from measured total/time, reviewed code only.
- [ ] Full read packages/read coverage, v2 and v1-identical subset metrics, matched effects and paired intervals, results and independent review.
- [ ] Exact-ID destruction confirmed by API; cost receipt; audit and journal; scoped commits/no push.

## Coordination decisions

- This worker cannot spawn subagents or use intercom. const_v2 owns the bridge and different-family review; full Sol reads are performed here or via parent-launched readers supplied with full read packages.
- Freeze a66d2ae v2 judge/checks (not run8's older protocol). All cells get this protocol. Run14 scores are not directly comparable; also report the 96 v1-identical items and identify their overlap with run14.
- Resolved config comparison normalizes output/prepared artifact paths. Dataset path is the only substantive change for the first chat; the second intentionally changes the document training base.
- Selector source pinned to 4acffd4a; its nonzero exit skips that cell, preserving logs/moments and informing cg_exp_curve through const_v2. Projection/basis code and optional orthogonal plugin pinned to 7ea93f1e. (c) reviewed OK but remains last and budget-conditional.

## Evidence before outcomes

Question: does EOS repair remove projection's apparent capability gain, and does anchored document training improve coherent change without merely reducing effect?

| Candidate explanation | Distinguishing readout | Planned check |
|:--|:--|:--|
| Projection's earlier gain was entirely finishing answers | New D finishes; matched-effect projection has no advantage among questions both finish | Raw /60 and paired both-finished denominators; interpolation only within measured ½…1 bracket |
| Projection removes damaging directions independently of stopping | Fewer errors among questions both models finish, at matched character | Same paired questions, ordinary checks and read decisions; not equal coefficients |
| Anchoring is merely weaker | Cleaner outputs but less coherent behavioral change | Separate document change curve and Base losses; final chat compared at matched character |
| Corruption masquerades as document change | Large ABX change with language/loop flags | Keep corrupt outputs in failure view; compare coherent subset and actual decisions |
| Implementation/data mismatch dominates | Wrong masked targets/config, missing experts or selector energies invalid | EOS-only data proof, resolved config diff, tiny train/merge, remote SHA, expert coverage, selector exit gate |

No scientific outcome is claimed yet. CPU smokes establish executable paths, not character quality. No new training examples, constitution rules or evaluation incidents are added to training.

-- PI/OpenAI (Sol)
