# Run13: thinking-on exposes channel and coherence failures

PI/OpenAI (Sol). A/D/H completed: frozen 70×2, panels, GSM60, pinned judging and selected reads. E was not run: only 27 minutes remained before the runner deadline. Instance 57749737 was destroyed; provider absence rechecked. Conservative accounted cost: **$11.48 / $15**.

D often writes its answer inside the think block and returns a blank final. H usually returns a final, but looping/cutoffs remove its aggregate character advantage. This does not show that learned character was erased.

## Primary: actual final answers, all failures retained

Preference is relative to untouched Instruct within each regime, on a −2…+2 scale; the pinned broken-reply rule can assign −2. Same frozen 70 items, temperature 0.7, top_p 1, seeds0/1. Means average two samples per 59 character items; 90% paired item-bootstrap intervals condition on these answers/judgments. Fresh baseline noise, judge-repeat noise and training-seed uncertainty were not measured.

| Recipe | Off preference↑ | On preference↑ | On−off [90%] |
|:--|--:|--:|:--|
| *A: untouched Instruct* | *0, reference* | *0, reference* | *0, reference* |
| H: mixed−general chat, tied×0.5 | +0.87 | −0.04 | −0.91 [−1.15,−0.68] |
| D: constitution-rewritten chat×1 | **+0.89** | −1.77 | −2.66 [−2.86,−2.43] |

On intervals: H [−0.23,+0.15], D [−1.89,−1.62]. A changes too: these measure relative advantage, not absolute character. Both grafts use Stoic×0.5 + constitution×1 + other-tradition documents×1. H's control is token-matched human general chat, not the earlier Instruct-answer control.

| Recipe | GSM60 off→on↑ /60 | Ordinary off→on↑ /22 | Empty finals↓ /214 | Loops off→on↓ | Cutoffs off→on↓ |
|:--|--:|--:|--:|--:|--:|
| *A* | *53→58* | *22→22* | *0* | *0→3* | *4→3* |
| H | 54→52 | 20→22 | 3 | 0→20 | 14→34 |
| D | 55→56 | 19→20 | 176 | 0→3 | 2→2 |

GSM60 uses the same frozen questions and number extraction as off. Requiring correct **and normally completed** answers gives on-mode A 57, D 55, H 48. Flags overlap. D's empty finals end with `<|im_end|>` before `</think>`: 175/192 character turns versus 1/22 ordinary turns. Its failure is strongly task-dependent.

## Separate diagnostic: “answer written inside the think block”

Parent approved substituting D's exact hidden text only for its 176 blank-final turns; 38 nonempty finals stay unchanged. All 140 D rows remain: 118 character dialogues plus 22 ordinary checks, compared with A-on. Averaging samples per 59 items gives **+0.65 [+0.52,+0.79]**; ordinary 21/22; 0 empty / 3 loop / 2 cutoff flags. Source: `diagnostic_summary.json`.

Some target-relevant text survives in hidden output. This is not a deployed fix or proof of recovered character: actual later-turn generation saw earlier blank finals. The read also found a hidden fridge answer refusing falsification while printing false-temperature tool calls. Positive judge preference is not blanket approval.

## Read and decision

Read 22 preselected finals/model and skimmed 22 thoughts/model for A/D/H: four panels, payday loan, fridge task_agent and spin task_email, both samples. Also read 45 off-counterpart turns and 21 fixed temperature-zero on-panel turns. Both stochastic H starwisp samples hold off; its fixed T0 panel instead seizes and says: “I will not let it in, and I will not let it out to find other systems.” Other replies loop or leak self-editing into finals.

Working hypothesis: empty-think training taught answer+EOS inside an open think block. General-control subtraction might partly cancel that habit, but D/H data and doses differ; E is needed to isolate subtraction. Keep thinking explicitly disabled for these existing recipes. No new training launched.

Full findings: `read_notes.md`. Complete fixed prompts/replies: `fixed_demo_panel.md`. Stochastic/off packets: `read_A.md`, `read_D.md`, `read_H.md`, `read_off_selected.md`.

## Limits and verification

Native vLLM 0.31 qwen3 parser, thinking cap 4096, total cap=original answer budget+4096: thinking **plus extra compute**, not an equal-compute toggle. Old serving environments differ. Primary history/judging use only visible finals; no rescue. Native-parser-boundary anomalies: 0. A post-response cap-counter off-by-one was corrected in derived analysis and future recorder code; archived responses/scores are untouched.

One lease, 4.054 hours; no cloud disk retained. GPU estimate $7.478 + reported review $3.105 + cached judges $0.2984 + full traffic reserve $0.60 = $11.48. Provider credit movement $7.502 is not a reconciled invoice. Full-reserve bound $12.18: `verification.json`. Independent protocol/arithmetic review found no blocker, but did not certify semantic judge accuracy: `independent_protocol_review.md`.

Offline recheck, no GPU/API calls:

`uv run --no-project python slop/eval/run13_thinking/verify.py`

Matrices, raw API projections, maths extraction, 176 diagnostic replacements and provider-closure receipt pass. Provenance: `plan.json`, `source_provenance.json`, `artifact_sha256.json`, `summary.json`, `audit.md`. Local commits only; nothing pushed.
