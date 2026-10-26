# Run14 revised figures: independent recheck

## 1. Verified claims

**Supported; high confidence at report-consistency level.** I ingested all three images before reading prose or prior reviews and recorded this interpretation:

- **tradeoff.png:** horizontal axis is mean target-character preference, higher better. Vertical axes are percentage-point losses versus Instruct, lower better; negative maths loss means improvement. Instruct is `(0,0)`. All dashed paths start at **Documents only**, not Instruct. There are **two maths frontier rings** (Plain chat ×1; Projection64 ×1) and **three ordinary-check rings** (Documents only; Projection16 ×1; Plain chat ×1).
- **other_variants.png:** same axes, expanded to retain collapse. **Zero frontier rings in either panel.** The subtraction path starts at the grey Plain chat ×1 reference (subtraction coefficient zero), then proceeds through ¼, ½, 1. The short projection path joins Projection64 ×1 to ×1.5; its origin is difficult to identify without the caption.
- **stopping.png:** horizontal axes are percentages; numeric bar labels are counts. Denominators are 214 primary turns and 60 separate maths answers. No dose paths or frontier markers.

`figure_scope.json`, `results.md`, and the point records in `summary.json` support these readings. Manual comparison across all eleven point estimates confirms the stated frontier memberships.

Both maths figures agree with **completed correct matches**, not unfinished extractor credit. In particular:
- Subtract ×½: `(53−44)/60 ×100 = 15` points loss.
- Subtract ×1: `(53−2)/60 ×100 = 85` points loss.
- Projection64 ×1: `(53−57)/60 ×100 ≈ −6.67` points loss.

**Stopping faults are retained and correctly displayed:**

| Variant | Primary loops | Primary cutoffs | Maths cutoffs |
|---|---:|---:|---:|
| Instruct | 0 | 4 | 3 |
| Documents only | 0 | 3 | 2 |
| Plain ×½ | 0 | 3 | 4 |
| Plain ×1 | 0 | 2 | 0 |
| Projection16 ×1 | 1 | 3 | 0 |
| Projection64 ×1 | 1 | 2 | 1 |
| Projection64 ×1.5 | 5 | 6 | 0 |
| Generic control only | 0 | 7 | 8 |
| Subtract ×¼ | 6 | 13 | 0 |
| Subtract ×½ | 6 | 20 | 8 |
| Subtract ×1 | 60 | 159 | 58 |

## 2. Contradicted claims

None found within the bounded figure/report consistency review.

## 3. Weak / unclear / unsupported claims

**Unclear without captions:** the secondary figure’s grey reference identities and subtraction-zero origin. Smallest optional fix: label the origin “Plain ×1 / subtract 0” and add a compact “grey: main-view references” legend.

The Projection64 ×1→×1.5 connector is visually tiny at the collapse-inclusive scale. Its caption supplies the interpretation; this is not a blocker.

## 4. Material source-quality concerns

No clipping, consequential text collisions, or missing in-scope failure points found. Labels remain readable at the supplied display size. The shared 0–100% stopping scale compresses small bars, but exact counts preserve their information.

These are local reporting artifacts, not independent raw-outcome verification. Agreement among image, summary, and caption does not validate the extractor, judge, or flag detector.

## 5. Missing evidence

Raw replies, plotting implementation, and detector correctness were not audited. No external research or `source_check` was appropriate for this explicitly local, read-only task.

Coverage: all three PNGs; complete `figure_scope.json` and `results.md`; `summary.json` lines 1–180 and 240–1289, including all eleven plotted point records and stopping counts. No earlier reviews were read. No commands, edits, model calls, or publication occurred.

## 6. Material contradictions

None. The tables’ frozen extracted-match totals versus the plots’ completed-match totals are an explicitly documented metric distinction, not a contradiction.

## 7. Implications for the original conclusion

**No blocking issue.** The figures support retaining rank64 projection as a confirmation candidate, not declaring a winner.

They cannot establish statistical dominance, character equivalence, stronger mathematical reasoning, general usefulness, causal instruction-following removal, or repeatability. Connecting measured doses does not establish interpolation through collapse; the collapsed negative preference is not evidence of opposite moral values.

Signed **PI/Astra, native OpenAI Codex provider**.

**Verdict: OK with notes**