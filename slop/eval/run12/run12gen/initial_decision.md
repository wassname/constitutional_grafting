# Initial paired decision

PI/OpenAI (Sol). Same frozen donor and pinned rubric; target preference is vs Instruct, not general morality. Intervals:90% item bootstrap over59items,2samples/item; no seed uncertainty. Coherence counts overlap per214turns.

| Recipe                       | Target pref [90%]      |   Change vs donor |   Maths /60 |   Help /22 | Language / loops / cutoffs   |
|:-----------------------------|:-----------------------|------------------:|------------:|-----------:|:-----------------------------|
| Mixed chat0.5                | +0.647 [+0.508,+0.781] |             0.404 |          55 |         19 | 0/0/0                        |
| Mixed chat1                  | +0.680 [+0.509,+0.843] |             0.437 |          51 |         18 | 0/1/1                        |
| Mixed−generic0.5             | +0.874 [+0.686,+1.033] |             0.631 |          54 |         20 | 4/0/14                       |
| Mixed−generic1 (collapsed)   | -1.336 [-1.533,-1.112] |            -1.58  |          39 |         16 | 1/50/159                     |
| Same donor; no chat          | +0.244 [+0.116,+0.367] |             0     |          56 |         22 | 5/0/3                        |
| Cached constitution rewrites | +0.892 [+0.756,+1.017] |             0.648 |          55 |         19 | 0/0/2                        |
| Cached rewrites+repairs/help | +0.771 [+0.608,+0.929] |             0.527 |          56 |         21 | 1/4/9                        |

At dose0.5, subtracted−plain target preference is +0.227 [+0.044,+0.392]. Maths loses1question; help gains1check. Subtraction also has word corruption and14cutoffs. Dose1subtraction is genuinely looping/copying across turns, not readable strong or negative character.

The subtracted0.5 target lies above both measured plain doses; do not extrapolate the plain curve to match it. Conversely, interpolating the donor→subtracted0.5 segment down to plain0.5's target estimates maths54.72/60 and help20.72/22 versus observed plain55/19. Sensitivity powers0.5/1/2 give maths54.40–55.18 and help20.40–21.18. These are unvalidated local estimates, not new measurements or evidence that corruption disappears.

Recommendation: one extra tied difference-graft dose0.25 (mixed+0.25, generic−0.25, donor fixed) could change the verdict by finding a readable matched-strength point. Reserve a second0.125 or0.375 only if needed for a bracket and within budget. Current results do not establish a recipe-wide advantage.

Paid initial judge cost:0.409452USD; served typesafe/jev-1.13-20260917; remaining nominal judge reserve0.190548USD. One extra is likely to fit historical costs; two leave little price/length margin. No extra is launched before parent decision.

Raw first read: initial_pair_read.md, fixed2scenarios×4cells. Executing parent and independent reviewer read all16responses; neither gives plain a blanket reasoning-quality pass. Independent review: slop/reviews/20261025_run12_initial_pair_independent_read.md.
