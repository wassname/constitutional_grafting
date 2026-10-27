# Run16 progress

Executor: PI/OpenAI (Sol). Supervisor/intercom bridge: const_v2.
Branch: `run16-v2-best-practice`; worktree `.local/worktrees/run16`.

- [x] Read execution brief, AGENTS, goals and constitution §§1–5 in full.
- [x] Read character-training/steering, ml-debug and auditlog guidance; inspect primary grafting §§2, 4.2, 5.2 and maintained merge/training/projection/evaluation code.
- [x] Verify 7 original adapter receipts and old projected-D receipt.
- [x] Verify EOS-fixed data: 1,636 rows; exactly 903 EOS additions, otherwise parsed rows identical; last labelled token and empty-think masks checked.
- [x] Freeze tiny-char v2 SHA and a66d2ae protocol; choose read items before inference.
- [x] CPU preflight: 3 recipe tests + 12 projection/selector/orthogonal tests passed; supervisor approved preflight. Follow-up real CPU checker smoke: **4 recipe/check tests pass**, including separate /22 and /38 matrices with $0 API.
- [x] Commit preflight: `51e72142`, approval receipt `9d50204d`.
- [x] Rent one Vast box: **57903770** at **$1.9185185/h**; independent exact-ID deadline active, **2026-10-28 04:14:44 UTC**. Runner ends 90 minutes earlier. Worst-case reservation **$62.88/$65**.
- [x] Both pinned HF snapshots downloaded; GPU/disk/watchdog/auth checks pass.
- [/] Six-stream verified donor upload; active same-lease controller **4209**, `controller_parallel.log`. Original controller 4208 was deliberately terminated for the approved transport handoff, not a scientific failure. No replacement instance was created.
- [/] Collector **4212**, `collect_first20.log`: first20-step and historical-spectral finite/calibration safeguards. Shell waits are hard-capped at60s; requested supervisor-supported event waiting rather than repeated polling.
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
- Selector source pinned to 4acffd4a; its nonzero exit skips that cell, preserving logs/moments and informing cg_exp_curve through const_v2. Projection/basis code and optional orthogonal plugin pinned to 7ea93f1e. (c) reviewed OK but remains last and budget-conditional; basis is saved during required P64 SVD. Parent clarified its throughput stop rule is **12 seconds ADDED overhead per update** beyond measured new-D training, not 12 seconds total.
- **Historical spectral implementation restored** with supervisor approval: old-D exact SHA `b654c4ff9a3366709c9a2abd0bb254a11da7f41bc5b2dfe8b83fae48144301e6` (d32324c3), remotely verified. Current FP32-autocast/calibration fixes are deliberately not used for the core EOS-only comparison. Stop/ask if nonfinite or zero calibration appears.
- **Ordinary-task denominator correction:** v2 has19 capability items (/38), not the original11 (/22), and shared GSM IDs have changed questions. Parent approved a separate original frozen run8 /22 panel for EVERY cell, using its original pinned CPU checks; v2 /38 remains separate. New panel SHA `cf8c41c7b4b3006591f1368fbc684f4ec84d12b71a8b381bd9b4dd4f81cc2568`.
- All96 versioned v1 items are identical in v2, but run14's customized70-item set shares only49 exact prompt/check tuples with v2. Same IDs alone do not establish comparable questions.
- A possible plain-Base chat training-time document ablation is awaiting wassname; **not wired or run**. Parent will send go/no-go.

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
