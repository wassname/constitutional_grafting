## Five-cell image review — PI/OpenAI

Independent context, but same model family; not cross-family validation or a final-matrix gate.

### Initial review

**What the image shows:** Five measured cells, including untouched Instruct at the origin. Higher means greater judged character improvement; farther right means more task-check loss. Both updates have the largest character gain and task loss. Documents 2× moves below zero on all 59 character items, but remains positive on the nine-item subset. Neither documents-2× character interval excludes zero.

**Agreement:** The plotted centers and interval endpoints visually agree with `/workspace/2026/constitutional_grafting/slop/eval/run8/paired_estimates.json`: full-character means are +1.091, +0.719, +0.335 and −0.088; corresponding task losses are 22.73, 9.09, 4.55 and 9.09 percentage points. Shared-subset means also agree. No concrete numerical mismatch found.

**Labels and uncertainty:** `/workspace/2026/constitutional_grafting/slop/eval/run8/character_capability.png` clearly defines coefficient order, task composition, baseline and “marginal 90% item-bootstrap intervals.” It explicitly says “Dashed lines are not interpolation evidence” and “5/7 requested mixtures measured.” Labels are readable at supplied resolution; the dense footer may need enlargement when embedded. No observed unreadable or clipped element.

**Primary versus pre-rule:** The image says “Character includes fixed broken-reply penalties”; it does not plot raw preferences. `/workspace/2026/constitutional_grafting/docs/results/20261017_spectral_heal.md:27` explicitly separates “Raw Jev preference is+1.13” from “primary score is−0.09 after44/118 character samples are overridden.” This is clear, not a misleading presentation of raw preference as better character.

**Remaining presentation risk:** Standalone image readers are not told that the nine-item panel is *not independent replication*, or that intervals exclude judge error and training/serving variation. The accompanying document and JSON supply those caveats. This is an omission risk, not an observed false claim; embedding the image with that text substantially addresses it.

**Initial coverage:** Ingested PNG first; fully read paired estimates, both specified AGENTS.md files and ml-debug/SKILL.md; read results lines 1–65 only. Three initial reads of `documents2_rule_audit.json` returned no content, so its override counts and pre-rule calculation were then unverified. No shell, API, edits or broader discovery. Final matrix and higher strengths remain unfinished.

### Follow-up: restored rule audit

Directly read the complete restored `/workspace/2026/constitutional_grafting/slop/eval/run8/documents2_rule_audit.json`. The earlier empty reads remain a real limitation of the initial review; the parent attributes them to an interrupted rewrite.

The restored artifact reports `"character_rows": 118`, `"automatic_broken_rows": 44`, primary mean −0.08826271186440678 and diagnostic pre-rule mean +1.1252542372881356. These agree with the previously read primary estimate and the document’s rounded −0.09/+1.13 figures. The denominator is consistent with 59 items × two samples.

These are **saved reported counts and means**, not independently recalculated results from raw replies or scores. The turn-level language list is not an override ledger and cannot alone establish the 44 overridden sample rows.

The scope appropriately warns: “Foreign spans are not proof every reply is incoherent.” The zero exact-phrase search counts explicitly rely on a prior search, “not rerun here”; I have not verified them. No concrete internal contradiction found. Recalculating from raw/score files and checking override membership would test the remaining uncertainty. PNG and primary estimates were not rereviewed.

— PI/OpenAI