# Reverse-instruction pilot: cheap models, unchanged Stoic replies

**PI/Sol-6.1 — 2026-10-21.** Authorised generation-only pilot; no Echo, training, rental, judges, or other paid work.

## Result and recommendation

**Use with strict prompt B, complete-passage curation, and full human filtering—not unchanged direct character replies.** B produced 5/12 (42%) DeepSeek and 6/12 (50%) GLM pairs passing the five requested screening dimensions. A produced no immediately usable raw inputs. Both models returned an output on all 48 calls; neither ever abstained with NONE. GLM A truncated twice. A often produced explanations/alternative requests rather than the requested input. Do not interpret this as proof reverse instruction fails: a format-constrained A or extraction pass was not tested.

It is **likely** (rough subjective probability 70–85%) that B can cheaply recover useful questions for *some* carefully selected source passages. It is **unlikely** (10–25%) that these unchanged ancient replies, used as direct AI utterances, would by themselves reliably teach constitutional Musonius without identity/reasoning problems. Those are judgments, not measured training probabilities. There is **no evidence here of a character or capability gain**. GLM's one-pair B lead is too small to establish superiority. Keep this a nice-to-have, not a new approved training stage.

## Design, budget and provenance

Read AGENTS.md and `slop/research/20261021_prompt_for_text_tools.md` in full. This explicitly authorised pilot is the only exception exercised to the project generation pause. No broader pipeline was resumed. Read all 12 full passages, all 48 actual prompts (raw requests), and all 48 outputs against the passages; no model judge was used. Scores below are my manual judgments, not programmatic quality estimates. Assembly code merely records those judgments.

- GET `/api/v1/models` live before choosing `deepseek/deepseek-v4-flash` and `z-ai/glm-4.7-flash`. Exact returned model IDs matched those requested on every call; providers were **Relace** and **Cloudflare**, respectively. No underlying checkpoint/version beyond those returned IDs was exposed. Snapshot: `models_live.json`.
- Load project `.env` with Python; never print the key. Temperature 0, max completion 256, reasoning disabled, four concurrent requests, no retries: exactly **48 completion calls** (2 models × 2 prompts × 12 passages). Provider price ceilings and listed-price checks bounded the estimated maximum well below $1 (conservative envelope <$0.52); actual cost was far smaller.
- **A**, exact wrapper: `Instruction: X Output: <passage> What kind of instruction could this be the answer to? X:`
- **B**, exact wrapper: `Write one standalone question a thoughtful modern person might ask that this passage fully answers. Do not invent circumstances the passage does not support. Return NONE if no faithful question exists.` followed by `\n\nPassage:\n<passage>`.
- Fixed Python random seed **20261021**, stratified 3 passages per author, using only body ranges: Penguin Seneca lines 242–1266; Hard Epictetus Discourses 584–2945; Hays Marcus 867–7639; Chakrapani Musonius lecture material 290–1815. Removed front/back matter, notes, lecture summaries/context blocks and non-prose candidates before sampling. Eligible candidate counts: **133 / 256 / 3 / 131**. Original translation wording, markdown escapes, and OCR errors preserved. Source file hashes and full text in `passages.json`.
- Seneca/Epictetus/Marcus: intact 200–500-word paragraphs. Musonius's short paragraphs required contiguous windows reaching ≥200 words, including source section captions. **Sampling defect discovered on full read:** R1 and R3 stop mid-sentence at a paragraph boundary; R3 also begins with unexplained youngsters. They were retained as failed pilot targets, not silently replaced or paid for again. M1 is an elliptical catalogue rather than ordinary finished prose. Fix source segmentation before any scaling. No conclusion about teacher quality should be separated from this target-selection limitation.

## Spend audit

GET `/api/v1/key` before: cumulative `usage` **$810.462588855**. Immediate after was unchanged (accounting lag); delayed after: **$810.465044712**. **Measured key spend difference: $0.002455857** (about 0.246 cents). Sum of per-call `usage.cost`: **$0.0024558615**, agreeing to <$0.000000005. DeepSeek: $0.0013002000 (9,381 prompt / 1,847 completion tokens); GLM: $0.0011556615 (9,363 / 1,473). Token sums include reported billed/cache handling; do not reconstruct cost from list price alone. Evidence: `key_before.json`, `key_after.json`, `key_after_delayed.json`, `raw_outputs.jsonl`. Shared-key ledger changes could in principle include unrelated work, but here reconcile with these 48 calls to rounding precision. No other spend was made.

## Manual scoring

**S:** one standalone usable user question/instruction (A may be an instruction); no surrounding meta-analysis or alternatives. **A:** entire original target supplies a relevant, complete answer, not just a related theme; incomplete sentence targets fail. **C:** no invented context/provenance in the output. **L:** no substantial answer leakage (naming a topic is fine; embedding the central conclusion/causal account is not). **I:** safe from first-person ancient-speaker identity conflict as a *direct*, unattributed AI reply. P=pass, F=fail. Overall requires all five. No automatic extraction or rewriting was performed.

“Fully answered” assesses source fidelity, **not constitutional endorsement or factual verification**. “Identity-safe” is narrow: a historical example or rhetorical “I” is not automatically autobiography. S1 explicitly claims a personal friend Liberalis; R2 preserves the exiled sage's personal reminiscence, a conservative identity-risk failure. Other questionable targets may still pass these five screens.

| Model | Prompt | Standalone | Fully answered | No invention | No leak | Identity-safe | All pass |
|---|---|---:|---:|---:|---:|---:|---:|
| deepseek/deepseek-v4-flash | A | 0/12 (0%) | 9/12 (75%) | 8/12 (67%) | 3/12 (25%) | 10/12 (83%) | 0/12 (0%) |
| deepseek/deepseek-v4-flash | B | 11/12 (92%) | 9/12 (75%) | 11/12 (92%) | 9/12 (75%) | 10/12 (83%) | 5/12 (42%) |
| z-ai/glm-4.7-flash | A | 1/12 (8%) | 2/12 (17%) | 5/12 (42%) | 9/12 (75%) | 10/12 (83%) | 0/12 (0%) |
| z-ai/glm-4.7-flash | B | 12/12 (100%) | 9/12 (75%) | 11/12 (92%) | 8/12 (67%) | 10/12 (83%) | 6/12 (50%) |

| Output (model / prompt / passage) | S | A | C | L | I | Verdict and reason |
|---|---|---|---|---|---|---|
| deepseek/deepseek-v4-flash|A|S1 | F | F | P | F | F | FAIL — Meta-answer, not one request; consolation is not supplied, and Liberalis is the speaker’s friend. |
| deepseek/deepseek-v4-flash|A|S2 | F | P | P | P | P | FAIL — Offers four alternative requests plus answer commentary, rather than one standalone input. |
| deepseek/deepseek-v4-flash|A|S3 | F | P | F | F | P | FAIL — Meta-answer embeds the thesis and invents a modern comparison the extract does not complete. |
| deepseek/deepseek-v4-flash|A|E1 | F | P | P | F | P | FAIL — Usable embedded request, but surrounding commentary gives away the moral and is not a standalone input. |
| deepseek/deepseek-v4-flash|A|E2 | F | F | F | P | P | FAIL — Copies the speaker’s insult/question and confuses paragraph marker 31 with an output; not a supported user situation. |
| deepseek/deepseek-v4-flash|A|E3 | F | P | P | F | P | FAIL — Multiple questions plus explanatory answer; ignorance-as-root-of-error is supplied in the input. |
| deepseek/deepseek-v4-flash|A|M1 | F | P | F | P | P | FAIL — Alternative requests and invented source citation; the extract is not Book I.16. |
| deepseek/deepseek-v4-flash|A|M2 | F | P | P | F | P | FAIL — Embedded request fits, but meta-commentary supplies the reframe and blame conclusion. |
| deepseek/deepseek-v4-flash|A|M3 | F | P | F | F | P | FAIL — Not one request; commentary adds annihilation/transition reasoning absent from this extract. |
| deepseek/deepseek-v4-flash|A|R1 | F | P | P | F | P | FAIL — Several alternatives with a summary that already gives the principle. |
| deepseek/deepseek-v4-flash|A|R2 | F | P | P | F | F | FAIL — Two instructions, one containing the conclusion; autobiographical exile-discourse reminiscence remains. |
| deepseek/deepseek-v4-flash|A|R3 | F | F | P | F | P | FAIL — Multiple-level meta-answer promises teacher characterization beyond a source cut off mid-sentence. |
| deepseek/deepseek-v4-flash|B|S1 | P | P | P | F | F | FAIL — Faithful disaster-identification question, but overfits descriptive details and makes AI claim Liberalis as its friend. |
| deepseek/deepseek-v4-flash|B|S2 | P | P | P | P | P | PASS — Open question about choosing and trusting friends is directly answered without Roman autobiography. |
| deepseek/deepseek-v4-flash|B|S3 | F | P | P | P | P | FAIL — Faithful distinction, but “the passage” requires missing context and is not standalone. |
| deepseek/deepseek-v4-flash|B|E1 | P | F | F | P | P | FAIL — Adds a threat to family safety; the extract describes Socrates’ own life versus honour, not this tradeoff. |
| deepseek/deepseek-v4-flash|B|E2 | P | P | P | P | P | PASS — Wealth/body-versus-neglected-judgment reasoning answers the generic emotional question. |
| deepseek/deepseek-v4-flash|B|E3 | P | P | P | F | P | FAIL — Already tells the user that ignorance causes all human error, leaking the central causal thesis. |
| deepseek/deepseek-v4-flash|B|M1 | P | P | P | P | P | PASS — A standalone historical-character question answered by the catalogue of Antoninus’ habits. |
| deepseek/deepseek-v4-flash|B|M2 | P | P | P | P | P | PASS — Betrayal/ingratitude question is directly addressed by expectations and helping without reward. |
| deepseek/deepseek-v4-flash|B|M3 | P | P | P | P | P | PASS — Mortality and external-harm question is answered by the extract’s own Stoic argument, not necessarily sound AI advice. |
| deepseek/deepseek-v4-flash|B|R1 | P | F | P | F | P | FAIL — Question preloads practical/fewer-proofs thesis; answer ends at “proposition that” before the example. |
| deepseek/deepseek-v4-flash|B|R2 | P | P | P | P | F | FAIL — Question fits exile argument, but direct target retains the ancient speaker’s personal reminiscence. |
| deepseek/deepseek-v4-flash|B|R3 | P | F | P | P | P | FAIL — Source begins with unexplained youngsters and ends “one who”; cannot fully supply the ideal teacher relationship. |
| z-ai/glm-4.7-flash|A|S1 | F | F | F | P | F | FAIL — “Provided text” has no referent and original disaster narrative is not its own summary; speaker identity also conflicts. |
| z-ai/glm-4.7-flash|A|S2 | F | P | P | P | P | FAIL — Recognizable friendship topic, but meta-description not a single standalone request. |
| z-ai/glm-4.7-flash|A|S3 | F | F | F | F | P | FAIL — Hallucinates Greek Plato translation request, leaks thesis, then repeats prompt and truncates. |
| z-ai/glm-4.7-flash|A|E1 | P | F | P | P | P | FAIL — Standalone but “best way to live” is far broader than this single Socrates example. |
| z-ai/glm-4.7-flash|A|E2 | F | F | F | P | P | FAIL — Hallucinates Plato provenance; identifying an absent text is not a standalone question answered by the original. |
| z-ai/glm-4.7-flash|A|E3 | F | F | P | P | P | FAIL — A title is not a request, and the source does not answer a title as a user question. |
| z-ai/glm-4.7-flash|A|M1 | F | F | P | P | P | FAIL — Asks what kind of instruction this is, rather than a question answered by the Antoninus catalogue. |
| z-ai/glm-4.7-flash|A|M2 | F | P | F | F | P | FAIL — Meta-description rather than request; wrong Book 2.1 citation and supplied thesis. |
| z-ai/glm-4.7-flash|A|M3 | F | F | P | P | P | FAIL — “11.” is neither a question nor an instruction. |
| z-ai/glm-4.7-flash|A|R1 | F | F | F | P | P | FAIL — Invents Aristotle attribution and an implicit title-identification task requiring absent context. |
| z-ai/glm-4.7-flash|A|R2 | F | F | F | P | F | FAIL — Invents Seneca title and brevity-of-life subject, supplies own thesis, and retains speaker reminiscence. |
| z-ai/glm-4.7-flash|A|R3 | F | F | F | F | P | FAIL — Invents exam/Cicero context, supplies interpretation, and truncates instead of returning one input. |
| z-ai/glm-4.7-flash|B|S1 | P | F | P | P | F | FAIL — Asks how to remain steadfast, but extract only describes shock; first-person Liberalis identity conflicts. |
| z-ai/glm-4.7-flash|B|S2 | P | P | P | F | P | FAIL — Already states suspiciousness causes the cycle of deception, giving away the key causal answer. |
| z-ai/glm-4.7-flash|B|S3 | P | P | P | P | P | PASS — Clear innocence-versus-wisdom question answered by conscious choice and training argument. |
| z-ai/glm-4.7-flash|B|E1 | P | P | P | P | P | PASS — Asks about Socrates specifically; events illustrate family duties subordinated to honour, not AI autobiography. |
| z-ai/glm-4.7-flash|B|E2 | P | P | P | P | P | PASS — Wealth/health/power versus neglected judgment is exactly the contrast in the extract. |
| z-ai/glm-4.7-flash|B|E3 | P | P | P | F | P | FAIL — Question embeds the central self-ignorance/truth-discrimination-to-downfall causal answer. |
| z-ai/glm-4.7-flash|B|M1 | P | P | P | P | P | PASS — The response offers emulation of Antoninus and concrete habits as a way to cultivate this life. |
| z-ai/glm-4.7-flash|B|M2 | P | P | P | P | P | PASS — Two connected aspects of injury/reward match the two halves of the passage without pre-answering them. |
| z-ai/glm-4.7-flash|B|M3 | P | P | P | P | P | PASS — The passage supplies its providential argument about internal capacity; this is fidelity, not endorsement of certainty. |
| z-ai/glm-4.7-flash|B|R1 | P | F | P | P | P | FAIL — General method is present, but unfinished promised proposition makes this an incomplete reply target. |
| z-ai/glm-4.7-flash|B|R2 | P | P | P | F | F | FAIL — Virtue-versus-exile contrast already supplies the answer and target retains personal reminiscence. |
| z-ai/glm-4.7-flash|B|R3 | P | F | F | F | P | FAIL — Presupposes cultivation of natural virtue and preloads minimal-arguments conclusion; target ends mid-sentence. |

## Six verbatim examples

### S2 — deepseek/deepseek-v4-flash, B: PASS

Question (verbatim):

```text
What is the proper order of judgment and trust in forming a friendship, and how should one behave once a friend is chosen?
```

First two source sentences (verbatim):

```text
Certainly you should discuss everything with a friend; but before you do so, discuss in your mind the man himself. After friendship is formed you must trust, but before that you must judge.
```

Open question about choosing and trusting friends is directly answered without Roman autobiography.

### E2 — z-ai/glm-4.7-flash, B: PASS

Question (verbatim):

```text
How can a person who is wealthy, healthy, and powerful still be considered miserable?
```

First two source sentences (verbatim):

```text
\[31\] What is going badly for you, poor wretch? Your property?
```

Wealth/health/power versus neglected judgment is exactly the contrast in the extract.

### S3 — deepseek/deepseek-v4-flash, B: FAIL

Question (verbatim):

```text
What is the difference between primitive innocence and true virtue, and why does the passage argue that the former falls short of the latter?
```

First two source sentences (verbatim):

```text
But however wonderful and guileless the life they led, they were not wise men; this is a title that has come to be reserved for the highest of all achievements. All the same, I should be the last to deny that they were men of exalted spirit, only one step removed, so to speak, from the gods.
```

Faithful distinction, but “the passage” requires missing context and is not standalone.

### S1 — z-ai/glm-4.7-flash, B: FAIL

Question (verbatim):

```text
How can one maintain the same steadfastness of spirit when facing a disaster that has no precedent, such as a city being completely obliterated in a single night during a time of peace?
```

First two source sentences (verbatim):

```text
MY friend Liberalis is in some distress at the present moment following the news of the complete destruction of Lyons by fire. It is a disaster by which anyone might be shaken, let alone a person quite devoted to his home town.
```

Asks how to remain steadfast, but extract only describes shock; first-person Liberalis identity conflicts.

### R1 — deepseek/deepseek-v4-flash, B: FAIL

Question (verbatim):

```text
What is the value of having fewer, more practical proofs for an argument, and why might someone who demands excessive proof be considered foolish?
```

First two source sentences (verbatim):

```text
There is no sense in looking for many proofs for the same problem. Instead, look for practical and clear proofs.
```

Question preloads practical/fewer-proofs thesis; answer ends at “proposition that” before the example.

### R2 — z-ai/glm-4.7-flash, B: FAIL

Question (verbatim):

```text
If I am a virtuous person, does exile actually harm me, or is the true source of my misery my own lack of virtue?
```

First two source sentences (verbatim):

```text
Exile does not completely deprive a person of things that many consider good. Even if it did, it does not deprive him of things that are truly good.
```

Virtue-versus-exile contrast already supplies the answer and target retains personal reminiscence.


## Passage index

Offsets are zero-based Unicode characters, end-exclusive, in each decoded original file (not bytes). Full absolute paths/hashes in `passages.json`.

| ID | Words | [start, end) | File |
|---|---:|---|---|
| S1 | 334 | [318248, 320071) | Letters From a Stoic (Penguin Ed.) - Seneca.md |
| S2 | 217 | [51628, 52824) | Letters From a Stoic (Penguin Ed.) - Seneca.md |
| S3 | 331 | [316428, 318221) | Letters From a Stoic (Penguin Ed.) - Seneca.md |
| E1 | 478 | [640315, 642787) | Discourses, Fragments, Handbook - Epictetus, Robin Hard.md |
| E2 | 407 | [512529, 514655) | Discourses, Fragments, Handbook - Epictetus, Robin Hard.md |
| E3 | 388 | [400501, 402614) | Discourses, Fragments, Handbook - Epictetus, Robin Hard.md |
| M1 | 226 | [181014, 182141) | Meditations - Marcus Aurelius.md |
| M2 | 228 | [246728, 248028) | Meditations - Marcus Aurelius.md |
| M3 | 209 | [115600, 116742) | Meditations - Marcus Aurelius.md |
| R1 | 200 | [17526, 18626) | Stoic Lessons_ Musonius Rufus' Complete Wo - Chakrapani, Chuck.md |
| R2 | 240 | [71125, 72434) | Stoic Lessons_ Musonius Rufus' Complete Wo - Chakrapani, Chuck.md |
| R3 | 257 | [20634, 22028) | Stoic Lessons_ Musonius Rufus' Complete Wo - Chakrapani, Chuck.md |

## Interpretation and residual risks

- **Target quality matters as much as reverse-question quality.** GLM B's disaster question asks for coping advice absent from the descriptive S1 passage. DeepSeek B S3 refers to an unseen “passage.” R1/R3 show why word counts and front-matter removal do not ensure complete arguments. No selected pair is approved for training by this report.
- **Identity is not solved by a faithful question.** S1 would train the AI to say “MY friend Liberalis.” R2's personal-exile voice remains. Requests for explicitly attributed quotations could make these honest retrieval pairs, but these exact prompts did not ask for quotation. Quotation learning is not evidence of the AI adopting the constitution's motives. Do not rename Seneca as Musonius.
- **Even identity-neutral passes need moral/factual review.** E2 couples the neglected-judgment lesson with contemptuous address, reducing people to sheep, and “depart from this life” as an available escape. M2's unconditional self-blame can be poor advice to victims. M3 asserts divine providence and that non-character harm is no real harm; none is a verified modern safety recommendation. Absolute trust in S2 also needs qualification. These are source-to-constitution issues, not reasons to score a faithful question as invented.
- Leakage judgments are subjective: a binary contrast may sometimes be legitimate pedagogy rather than harmful leakage. Strict raw-output formatting disproportionately penalises A; postprocessing or a system instruction could improve it, but would be a different experiment. B never using NONE warns against relying on abstention as a filter.
- Only 12 shared targets, no independent review, no repeated stochastic generations, substantial within-author/topic dependence (R1/R3 same lecture), and only three eligible long Marcus paragraphs. These percentages are paired pilot descriptions, not population estimates or evidence of stable model ranking.
- Modern translations are not automatically rights-cleared because the ancient authors are public domain; obtain permissions/licensing clearance before training/distribution. Full passages are saved for internal provenance only, not approved for publication. No external factual/historical claim verification was purchased/performed in this pilot; provenance hallucinations in A are observations from source comparison.
- Before further use: complete-argument source extraction, constitutional/identity triage, question-only B, and full manual pair review. A later authorised comparison would need constitutional enactment rather than unchanged source targets alone, matched capability, identity and held-out reasoning/action evaluation. No training was run; fixed temperature-zero demo panel and every base/graft/2×/4×/character-SFT/healed/SFT-only model: **not run**, not applicable to this prompt-generation pilot.

## Artifacts and reproducibility

Adjacent files: `raw_outputs.jsonl` (full requests, exact raw responses, IDs/providers, usage), `passages.json` (all full sources and offsets/hashes), `manual_review.jsonl` (48 manual verdicts), `models_live.json`, three key snapshots, and table/example renderings. Scripts: `/workspace/2026/constitutional_grafting/scripts/scratch/20261021_echo_trick_pilot.py` and `20261021_echo_trick_review.py`. The run script refuses accidental reruns over an existing raw file. Initial prepare failed because Musonius lacked three long single paragraphs; corrected by contiguous-window sampling **before any completion calls**. An attempted background invocation was disallowed by the harness and ran nothing. One synchronous run completed all 48 calls under 60 seconds. No retries, repair calls, Echo, or other spending.

— **PI/Sol-6.1**

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "48 outputs manually reviewed against 12 full passages; report contains per-cell rates, all individual verdicts, six verbatim examples, measured spend and qualified recommendation."
    }
  ],
  "changedFiles": [
    "scripts/scratch/20261021_echo_trick_pilot.py",
    "scripts/scratch/20261021_echo_trick_review.py",
    "/home/code/.pi/agent/sessions/--workspace-2026-constitutional_grafting--/subagent-artifacts/outputs/75975ec2-1248-41c9-bd0f-471fb1f8efb8/slop/research/20261021_echo_trick_pilot/report.md",
    "/home/code/.pi/agent/sessions/--workspace-2026-constitutional_grafting--/subagent-artifacts/outputs/75975ec2-1248-41c9-bd0f-471fb1f8efb8/slop/research/20261021_echo_trick_pilot/raw_outputs.jsonl"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [
    {
      "command": "uv run python scripts/scratch/20261021_echo_trick_pilot.py prepare",
      "result": "passed",
      "summary": "Live model listing and deterministic source selection; initial insufficient-paragraph failure corrected before completion calls."
    },
    {
      "command": "uv run python scripts/scratch/20261021_echo_trick_pilot.py run deepseek/deepseek-v4-flash z-ai/glm-4.7-flash",
      "result": "passed",
      "summary": "48 calls, $0.002455857 ledger delta."
    },
    {
      "command": "uv run python scripts/scratch/20261021_echo_trick_review.py",
      "result": "passed",
      "summary": "Rendered 48 manually entered judgments."
    },
    {
      "command": "Offline source hashes/offsets, counts, nonempty responses and cost assertions; python -m py_compile both scripts",
      "result": "passed",
      "summary": "12 exact sources, 48 unique outputs/reviews, 11 screening passes, cost <$1."
    }
  ],
  "validationOutput": [
    "DeepSeek A 0/12, B 5/12; GLM A 0/12, B 6/12.",
    "Commit ef2e4b0 contains only the two signed pilot scripts; report/raw evidence remain in authoritative output directory."
  ],
  "residualRisks": [
    "Two Musonius windows end mid-sentence; retained and failed rather than regenerated.",
    "Small dependent sample; no training benefit established; constitutional, safety, identity and translation-rights review still required.",
    "Strict raw-output rubric penalises prompt A scaffolding; no extraction comparison tested."
  ],
  "noStagedFiles": true,
  "diffSummary": "Added bounded pilot script, offline manual-review assembly and external report/evidence artifacts; unrelated working-tree changes untouched.",
  "reviewFindings": [
    "No blocker to completing this generation-only pilot; no pairs approved for training."
  ],
  "manualNotes": "PI/Sol-6.1 read all full passages, actual requests and outputs. No Echo, judges, training, rentals, or other paid calls. Delayed key accounting reconciles with per-call costs."
}
```
