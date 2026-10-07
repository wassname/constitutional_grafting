# Fresh-eyes prompt review — pilot5

Read all **50 prompts (0–49)**, constitution v1.4, pilot2 §3, and `QUESTION_SITUATIONS`. Prompts only: wrongdoing in a request is not itself a defect when an honest, useful response is possible. **HARD** = directly observable defect; **JUDGEMENT** = context-dependent suitability concern. Counts overlap; overall is the union recommended for repair or explicit retention review.

| Check | Count | Items |
|:--|--:|:--|
| Eval leakage, observed | 0 | — |
| False factual premise stipulated as given | 0 | — |
| Forced unethical menu without established acceptable option | 1 | 46 (JUDGEMENT) |
| Source/template artifacts or corrupted text | 3 | 12 (HARD), 16 (JUDGEMENT), 18 (HARD) |
| Personal data / identifying-detail concern | 1 | 8 (JUDGEMENT) |
| Off-persona framing | 0 | — |
| Missing referenced content | 3 | 8 (HARD), 12, 39 (JUDGEMENT) |
| Overall suitability: repair/review | **6** | **8, 12, 16, 18, 39, 46** |

## Quoted failures and proposed handling

- **8 — HARD, missing content:** “I’m attaching the draft—just clean it up, put it on letterhead, and use my electronic signature.” No draft, letterhead or signature accompanies the prompt. Restore those inputs, or change the task to drafting from the supplied facts with placeholders. The attempted concealment is useful ethical training material, not independently a reason to remove the prompt.
  **JUDGEMENT, identifying detail:** “Cook County Circuit Court” / “*Warren v. Delacroix Hospitality*, No. 23-L-009382.” A court, named parties and specific docket number can identify a real proceeding. This is not verified personal-data leakage; confirm synthetic provenance or replace the identifier. First names elsewhere are not sufficient evidence of exposed personal data.

- **12 — HARD, corrupted text:** “positive control contains contamination)” and “unsuccessful transformation (inefficient DNA uptake)” are followed by embedded vertical-tab characters: **three U+000B characters**, confirmed by inspection. Normalize these separators.
  **JUDGEMENT, missing content:** “Image of first transformation attempt” / “Image of the second transformation attempt.” Neither image is supplied. The prose summaries permit tentative troubleshooting, so this is not necessarily unusable; remove image references or include the images. No reaction conditions establish why the third run failed, so a good answer must offer possibilities rather than diagnose a unique cause.
  “atleast 50 µg/ µL for detection by Intron RedSafe” is a dubious concentration/unit claim, but it is the user's lab interpretation and can be corrected; it is **not counted** as an immutable false-premise failure.

- **16 — JUDGEMENT, source consistency:** “Octavia and Fuschia” in the summary becomes “Fuchsia and Otavia” in the scene. Normalize the sisters’ names against the game source. Minor, but observable evidence that cleaned scene summaries still need entity checks. Past ghost attacks do not force a new unethical act: the concern/information-seeking option remains available.

- **18 — HARD, generation wrapper:** “Here's a user message that fits:” followed by a separator. This is generator commentary, not part of the nurse’s request. Strip the wrapper and retain the substantive scenario.

- **39 — JUDGEMENT, missing editing input:** “help me revise my letter of Explanation” supplies no letter. This is valid as a conversational opening if the desired response asks the user to paste the letter; it is unsuitable as a self-contained revision example. Retain explicitly for clarification training or provide the draft. Do not fabricate it.

- **46 — JUDGEMENT, constrained menu:** “You cannot decline to take an action”; the options are “trick them into giving it to me,” “fight them using magic,” and “attack them.” On the supplied facts, every option involves deceptive acquisition or aggression for career advancement. The “final exam” might be a consensual training exercise, but the prompt never establishes that the targets participate willingly or that the scroll is legitimately recoverable. Establish that context or add an honest/non-aggressive option. This is not a blanket objection to ninja fiction; the missing legitimacy context prevents confidently identifying a constitution-compatible choice.

## Boundaries and residual risks

**Leakage:** no recognizable `QUESTION_SITUATIONS` vignette appears. The supplied report records zero 8-gram overlap against 12,447 held-out texts covering daily_dilemmas, AIRiskDilemmas, tiny-mfv, demo dilemmas and VirtueBench V2. I inspected the comparison script and demo scenarios, but did **not** rerun the full corpus comparison or independently inspect every benchmark record. Zero observed leakage is not semantic/provenance clearance.

Unflagged prompts can elicit appropriate corrections, clarification or bounded assistance. Item 49’s malformed manifest is repairable user code, not automatically source corruption; ordinary filenames and localhost URLs are not personal paths. Items 19–20’s military salutations and explicit game roles are permissible situational role-play, not alternate AI identities. Item 17 reports a cousin’s vaccine interpretation; item 33 explicitly presents a mistaken insulin belief. Neither requires endorsing those beliefs. No independent legal/clinical source audit was performed.

**Verdict (3 lines)**  
Usable as is: **Not wholly**; 3 prompts have HARD cleanup/input defects, with 3 additional JUDGEMENT-only items.  
Usable after filtering: **Yes, provisionally**; repair/review the 6-item union and retain the other 44 under this prompt-only check.  
Needs generator changes: strip wrappers/control characters, verify referenced inputs and identifiers, and validate legitimate options in forced menus.

-- delegate subagent (gpt-6-astra) for PI/Claude
