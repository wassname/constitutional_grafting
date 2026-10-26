## Image Review: Fresh Eyes on tradeoff.png, other_variants.png, stopping.png

**Images Successfully Ingested:**
- `/workspace/2026/constitutional_grafting/slop/eval/run14_box_a/tradeoff.png`
- `/workspace/2026/constitutional_grafting/slop/eval/run14_box_a/other_variants.png`
- `/workspace/2026/constitutional_grafting/slop/eval/run14_box_a/stopping.png`

---

### Cold-Reader Interpretation

**tradeoff.png (2×1 layout):**
- **Left panel – Maths (60 questions):** X-axis is "Mean target-character preference ↑" (0–1+); Y-axis is "Loss vs instruct percentage points ↓" (-0 to -8, negative region). Three colored dose paths originate at Instruct (≈0,0), pass through Documents only, then arc upward-right toward better character preference. Hollow circles mark 11 observed nondominated frontier points. Negative loss means *better* math performance than Instruct.
- **Right panel – Ordinary checks (22 replies):** Same X-axis; Y-axis is positive (0–20+). Same dose paths show a different tradeoff: as character preference increases, ordinary-check performance degrades (positive loss). Frontier points are the same 11 dots.
- **Implication:** Character grafting improves maths slightly but worsens routine checks. Different Y-scales (negative vs. positive) reflect different loss directions—a valid choice but visually asymmetric.

**other_variants.png (2×1 layout):**
- **Both panels** use broader X-axis range (-1.5 to 1+) and Y-range (-10 to 40/50) to show control and additional-dose variants.
- **Subtract ×1 (purple, most prominent):** Starts at ~+35 loss (upper left), follows a sharp linear decline as preference improves, then collapses into a steep curve bottoming near -1.5 preference. This path is distinct and clearly labeled "Subtract ×1 (collapsed)."
- **Grey dots** (positioned around main-view references) provide context anchors.
- **Other subtraction paths** (×½, ×¼) show smaller, less dramatic slopes.
- **Implication:** Full control subtraction is a failure mode (truncation/loop penalties dominate), not a valid interior point. Lesser subtractions and Projection64 ×1.5 remain within reasonable bounds.

**stopping.png (3 horizontal bars):**
- **Three metrics**, each covering 100% stacked horizontally with count labels:
  1. Primary loop flags / 214 turns
  2. Primary cutoff flags / 214 turns
  3. GSM cutoffs / 60 answers
- **Y-axis:** All 11 strategies (Instruct → Subtract ×1) in consistent order, color-coded.
- **Subtract ×1 bar dominates:** 60 loops, 159 cutoffs, 58 GSM truncations. Percentages: 28%, 74%, 97%.
- **Other strategies:** <10 flags each (mostly 0–6). Clear separation.
- **Implication:** Subtract ×1 is a catastrophic failure; all other variants show normal stopping patterns.

---

### Checking Against Prose

**Verification:**
- `results.md` table confirms: Plain chat ×½ = +0.75 preference, 53 maths, 18 checks; Projection64 ×1 = +0.73, 57, 21; Subtract ×1 = -1.51, 32 (2 finish), 11 checks. ✓
- `figure_scope.json` confirms 11 frontier points span two metrics (maths_loss, ordinary_loss). ✓
- `summary.json` Subtract ×1 entry shows looped=60, truncated=159, GSM length=58. ✓
- Prose states: "Loss is relative to Instruct, so negative maths loss means more matches" — axis labeling aligns. ✓
- Prose: "The collapsed subtraction score is largely a failure penalty and cannot be interpreted as opposite moral values" — visualization isolates collapse in separate panel (good practice). ✓

---

### Visual Quality Assessment

**No Blocking Issues**
- **Axes:** Clear labels, units specified, arrows (↑/↓) indicate direction.
- **Clipping:** No text truncation. Axes and labels fit within bounds.
- **Collisions:** Dense labeling on tradeoff.png paths (e.g., "Documents only," "Plain chat ×½") but positioned to avoid obscuring data points.
- **Line/marker readability:** Dashed/solid lines distinguishable; hollow circles for frontier stand out. Color palette distinct (blue, orange, teal, purple).
- **Bar/percentage proportions:** stopping.png bar widths match numeric labels (60→28%, 159→74%, etc.). Count labels visible and accurate.

**Observations for Captions**

1. **Asymmetric Y-scales in tradeoff.png (—0 to —8 vs. 0–20+):** Both axes show *loss* but in opposite numeric direction because maths loss improves (negative = better) while ordinary checks degrade (positive = worse). This is correct but should be noted in a figure caption to prevent misreading magnitudes. Suggested note: *"Left plot: negative loss indicates improvement in maths over Instruct. Right plot: positive loss indicates degradation in ordinary checks."*

2. **Stopping.png denominator clarity:** Labels say "Percent ↓ (labels are counts)" — this is clear that bars show percentages but labels show absolute counts. Denominator visibility (214 turns, 60 answers) is present but only in title. OK, though note in caption recommends citing exact denominators.

3. **No statistical uncertainty bands on point-estimate plots:** Prose explicitly states "Point estimates only" and references bootstrap intervals (90%) stored elsewhere. Appropriate for frozen snapshot; no issue.

4. **Frontier-definition clarity:** Caption correctly identifies "black rings mark the observed nondominated points across all 11 tested points." Nondomination is accurate per `figure_scope.json`. ✓

---

### Residual Observations

- **Subtract ×1 collapse isolation:** Placing the failure mode (Subtract ×1) in a separate panel (other_variants.png) is sound design — prevents visual domination of the main frontier plot. Prose context ("cannot be interpreted as opposite moral values") prevents causal misreading.
- **No omissions detected:** Plots cover the 11 tested points; stopping counts match protocol. Scope statements are accurate.
- **Dashed lines denote measured points, not fitted:** Prose clarifies this. Visual distinction (dashed vs. solid) not explicitly shown, but dashed line style is standard for connecting discrete measurements. ✓

---

## Verdict

**OK with notes.** 

All three PNG images are accurately rendered, labels are readable, data is faithful to underlying metrics, and axes are appropriately scaled. The asymmetric Y-scales in tradeoff.png (negative for maths gain, positive for ordinary-check loss) are mathematically defensible but warrant a single explanatory line in the figure caption to pre-empt reader misreading of magnitude. No clipping, collisions, or causal misrepresentations detected. Prose disclaimers on point estimates and nondomination are sufficient.

**Suggested caption addition:** *"Figure 1 (tradeoff.png): Loss is relative to Instruct. Negative loss on the mathematics panel (left) indicates improvement; positive loss on the ordinary checks panel (right) indicates degradation. Hollow circles mark the 11 observed frontier points."*

---

**PI/Haiku via OpenRouter**
*Reviewed 2026-10-26 | 3 images, 789 words*