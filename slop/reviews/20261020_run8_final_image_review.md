# Final image/report review

— PI/OpenAI; fresh context, same model family. Not cross-family validation or scientific certification.

## Result

No concrete blocking issue found in the reviewed figure, estimates, or current interpretation.

### Image-first reading

Before reading the author's interpretation, I saw two comparisons of character-score change against task-check loss: full 59-item character evaluation and a shared nine-item subset. Moderate updates score above baseline; strong SFT and combined updates move far right and below baseline. The extreme document-only point appears only in the subset. Labels, legend, error bars and extreme failure points were readable without clipping.

### Checks

- **Figure/JSON agreement:** All plotted means and interval endpoints visually agree with `slop/eval/run8/paired_estimates.json`, under `views.full` and `views.shared`. Examples: full `(1,1)` is approximately `(22.73, +1.091)`; full `(2,2)` is `(95.45, −1.927)`; shared `(0,4)` is `(90.91, −2.0)`.
- **Paths and coverage:** `scripts/eval/31_saved_update_report.py`, `render()`, selects SFT with `"b" == 0`, documents with `"a" == 0`, and both with `"a" == "b"`. These match the labels. Seven requested mixtures include the baseline; half-SFT and document4 are additional observations. Document4 is not presented as a full-59 estimate.
- **Capability:** The figure explicitly says “Loss on 11 task checks” and identifies eight maths, two format/count and one story-length check. Separate long60 maths is explicitly not plotted. The report acknowledges format-sensitive losses rather than equating this axis with general usefulness.
- **Intervals:** The reference `04_report.py::boot()` uses 2,000 item-bootstrap draws and 5th/95th percentiles; `per_item()` averages samples first. `17_plot.py::plot_data()` computes paired task differences. The figure correctly calls these “marginal 90% item-bootstrap intervals,” not joint confidence regions or seed uncertainty.
- **Failure points:** `incoherent_points.json` names exactly `(2,0)`, `(2,2)` and `(0,4)`, matching the × markers. `read_notes.md`, sections “SFT strength two,” “Both updates at strength two,” and “Document strength four,” supplies specific looping observations rather than relying solely on cap counts.
- **Interpretation:** The current results section explicitly says the comparisons do not “establish equal-effective-strength method rankings.” Its examples of misleading newsroom wording, inconsistent viewpoint judgments and faulty arithmetic prevent the higher preference scores from being presented as proof of good reasons.

## Residual risks and uncertainty

- Document2 also has manually reported looping, but is drawn with a circle. This does not contradict the one-way caption “× marks confirmed looping/severe confusion,” although readers should not interpret circles as certified coherent.
- I checked reported failure evidence, not the underlying raw replies. The optional half-SFT report and four reply exports were not read.
- No recomputation, hash verification, execution, serving-parity check or raw judged-record audit was performed. Code assertions are inspected safeguards, not evidence that this review executed them.
- Exact cross-host repeatability, judge validity and broader capability remain unestablished, as the report acknowledges. Regenerating from verified raw records could disprove the apparent numerical agreement.

## Scope actually read

Complete:
- `AGENTS.md`
- `/home/code/.pi/agent/AGENTS.md`
- `/home/code/.pi/agent/skills/ml-debug/SKILL.md`
- `slop/eval/run8/paired_estimates.json`
- `scripts/eval/31_saved_update_report.py`
- `slop/eval/run8/read_notes.md`
- `slop/eval/run8/incoherent_points.json`
- `/home/code/.local/share/tiny-character-2d69739/scripts/17_plot.py`
- `/home/code/.local/share/tiny-character-2d69739/scripts/04_report.py`

Also ingested `slop/eval/run8/character_capability.png` first. Read only lines 1–90 of `docs/results/20261017_spectral_heal.md`; older historical claims within that returned range were not reviewed.

---

# Final image/report review — follow-up

— PI/OpenAI; same-family independent context, not cross-family validation or scientific certification.

## Original review retained

No concrete blocking issue was found in the original image/report review. Figure values visually agreed with the supplied JSON; mixture paths, full59/shared9 distinction, capability definition and interval qualifications matched the reviewed code. The report did not treat preference scores as proof of good reasons or establish a method winner.

## Targeted marker follow-up

Read only:
- `/workspace/2026/constitutional_grafting/slop/eval/run8/character_capability.png`
- `/workspace/2026/constitutional_grafting/slop/eval/run8/incoherent_points.json`

The marker JSON now includes `"r8_a0_b2"` alongside `"r8_a2_b0"`, `"r8_a2_b2"` and `"r8_a0_b4"`.

The updated PNG displays an orange × at `(0,2)` in both panels: approximately `(9.1, −0.09)` in full59 and `(9.1, +0.41)` in shared9. Both markers and their labels remain readable. Existing extreme-failure markers remain visible and correctly labelled; no new clipping or label ambiguity was observed.

**This addresses my previous marker concern.** Document2 now receives the same looping marker as the other documented failure points. Its positive shared-subset score is visibly compatible with inspected looping, rather than suggesting that a positive score establishes coherence.

## Remaining limitations

The parent's statement that metrics and coordinates were unchanged was not independently verified by rereading estimates or executing a comparison. Placement is visually consistent with the earlier review.

All previous limitations remain: no raw-reply audit, recomputation, hash verification, execution or serving-parity check; optional half-SFT reply exports were not read. Cross-host repeatability, semantic judge validity and general capability remain unestablished. Circles should not be interpreted as certified coherent.