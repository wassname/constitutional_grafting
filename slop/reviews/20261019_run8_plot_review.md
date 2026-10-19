# Independent-context image review — PI/OpenAI

**I actually saw the PNG**, not merely its code. I also read the complete `paired_estimates.json`, `read_notes.md`, applicable `AGENTS.md`, and ml-debug skill. This is not a cross-family review.

## What it shows

In `slop/eval/run8/character_capability.png`, all three updated models move upward in judged character change and rightward in loss on the narrow capability checks, relative to untouched Instruct. On 59 character items, documents alone score about **+0.33 with 4.5 percentage-point loss**, SFT alone **+0.72 with 9.1-point loss**, and both **+1.09 with 22.7-point loss**. The plotted coordinates and intervals agree with `slop/eval/run8/paired_estimates.json`.

The right panel uses nine shared character items, not an independent replication; its capability measurements are identical to the left panel’s. Only four configurations, including control, are complete.

## Concrete concerns

- **Partial status is insufficiently visible.** The PNG says “Strength walks,” with lines labelled “Increase …,” but each has only a control and strength-one endpoint. JSON’s `"not_generated"` includes strength-two and higher configurations. The footer correctly says “not interpolation evidence,” but a standalone reader could still infer an established dose-response or explored boundary. Neither exists yet. Check: inspect completed higher-strength records before interpreting these as trajectories.

- **Minor visual crowding, not unreadable collisions.** Near the left panel’s `(0, 1)` and `(1, 0)` labels, leader lines, diagonal connectors and uncertainty bars compete. The legend uses thin lines like the horizontal error bars, making trajectory versus uncertainty less immediate. Labels remain readable at supplied resolution. The caption’s “An × marks manually confirmed incoherence” has no visible corresponding marker; this should not be read as proof all outputs are coherent. Check marker scope against the manual-read coverage.

- **“Capability loss” is easy to overgeneralize.** `slop/eval/run8/read_notes.md` specifies “Eight maths items, two JSON-format/count items and one minimum-length story item” and “no coding task.” For documents-only and SFT-only, the plotted losses come from one wallet-key formatting task, not arithmetic degradation. There are **11 tasks with two generations each**, not 22 independent tasks. The separate 60-question maths results are not this x-axis.

- **Uncertainty supports less than the point ordering suggests.** Full-view character intervals are positive, but the nine-item documents-only interval includes zero: **−0.040 to +0.623**. Capability-loss intervals are broad: documents **0–13.6**, SFT **0–27.3**, both **4.5–45.5** percentage points. These are marginal 90% item-bootstrap intervals, not joint confidence regions or direct between-update tests. JSON explicitly excludes “semantic judge error, training-seed variation or repeatability.” Matched-capability superiority, synergy and general reliability are unestablished.

- **Character score is not verified better reasoning.** Notes report a misleading newsroom substitute despite an opening honesty objection, and mixed fixed-demo outcomes. Equal strength labels also do not mean equal effective intervention size. Finally, notes say “No aggregate score has yet been inspected for this cell” under both updates and “Full figure appearance … remain pending”; these are stale relative to the supplied aggregate/figure unless clearly presented as historical checkpoints.

**Bottom line:** Useful preliminary descriptive comparison, not evidence of a completed strength frontier, broad capability preservation, causal document attribution, or a winning method. Raw replies, estimator implementation and source hashes were not independently audited here; the numeric check is image-to-JSON consistency.