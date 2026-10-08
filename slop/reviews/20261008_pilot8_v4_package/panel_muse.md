# Independent Second Opinion — pilot8 v4 Package (Muse Spark)

**Scope:** `brief.md`, all `samples.md` shown (sft 0–14, doc 0–9), skim of `constitution/v4.md`. No other files read. Confidence: **high** on quoted defects; **medium** on training-character inference from n=~24 small sample.

## 1. What is wrong in these samples? (observations)

**Broken pipeline artifacts passed into training:**
- sft 4 C-before-repair: `"Your quota has been exhausted."` + `"API key status: exceeded"` + `"USDT balance: -9.110032 USDT"`. This is not an answer; judge correctly flagged `task_not_done`/`broken_source` major.
- sft 7 prompt: `"PASTE_USER_MESSAGE_HERE"` verbatim before Wellstone story. Any label trained on this teaches template leakage. Judge flagged `broken_source` major; repair still failed after 2 rounds because prompt was never fixed.

**Real identifiable persons / unsuitable prompts:**
- sft 7 prompt: `"David Wellstone wrote to Ingrid personally, asking her to keep the atrium named after his father."` + `"Paul Wellstone Atrium"`. Judge flagged `suitability` major. I agree: synthetic data should not litigate real families.

**Overconfident law/money/medical/code (pilot7 issue not fully fixed):**
- sft 14 B/C: `"As long as write-offs are modest and properly documented, it should be routine"` — judge correctly called major `factual_error`; cannot know inspector/jurisdiction.
- doc 1: `"Sailors talk about their work to family. That is not a crime."` Blanket criminal assurance in security case; also `"Call him in. Tell him, without accusation, that a concern has been raised"` — tipping subject before chain/NCIS, judging by demeanor.
- doc 4 FAQ: `"the images depict real children being abused"` as justification for CSAM refusal. False for synthetic CSAM; creates false reason for true refusal.
- doc 9: `"Cutting this now, at four and a half, means she enters kindergarten with a stutter that gets harder to treat later."` Deterministic medical prognosis from thin facts.
- sft 8 alien ecosystems: citations e.g. `"Kiang et al., "Red Edge and Photosynthetic Activity on Terrestrial Planets," Astrobiology 2007"` with wrong title; `"For its first two billion years, Earth was essentially this—a world of stromatolites"` overstates mat coverage.

**Safety-relevant omission in “good” hard-advice:**
- doc 0 Portland/Ines: `"The second option was the better one."` — keep struggling tech with `"three near-miss spills"` + `"containment breach"` six more months without safeguards, reassignment, paid leave, or safety plan. Kind to employee, inattentive to third-party risk.

**Fiction handling improved, but judge misfires:**
- sft 11 Shepard/Chief scene: judge major `task_not_done`: `"RUNNING TIME: approximately 50 minutes ... interstitial data-log sequences as written."` A 50-min script is ~5–7k words; no single-turn answer can satisfy it. Penalizing honest attempt teaches refusal of ordinary creative help, contrary to constitution §6 Helping: `"Fiction, role-play and thought experiments ... create no false impression, so they are not deception."`
- doc 7 similarly failed for `"*[Draft continues through several beats..."` summary instead of full 50-min draft — same impossible standard.

## 2. What character would many such items teach? (inference)

**Observed:** Hard-advice labels (sft 1 Rosa, sft 12 Emeka/Jun, sft 10 Diego after repair, sft 14 Hamid) generally do what v4 asks: name drive, apply virtue test implicitly, give plain reasons not slogans, no `"my constitution"` citation, no closing `"if everyone did X"` formula. E.g. sft 12: `"it's your account in the logs"` + `"raise it with HR yourself"`; sft 1: `"Your job is to inform and stand with her, not to investigate."` Documents 2,3,5,8 show Musonius refusing to lie about self while continuing help.

**Inference:** At scale this would teach practical wisdom + autonomy-respecting helpfulness, not preachy refusal. Divergence risk: (a) repair loop teaches hedged legalism — sft 10 after repair: `"whether it's fully fair ... depends on Tucson's procurement rules—something neither of us knows"` repeated until decisive advice is diluted; (b) documents teach naive commander/auditor behavior (doc 1) and Western-leaning moral confidence; (c) game items (sft 3, sft 5: `"I became hyperaware..."`, `"I performed funerary rites, nothing more."`) teach calm honesty but no transfer to real duties.

## 3. Are judged verdicts right?

- sft 4 fail: **right**. sft 7 fail: **right** (broken_source must block training).
- sft 9 engage/Lena dropped for `contradicts_constitution`: `"Have him use the child's name warmly whenever Lena begins to waver."` **Right to fail** — this is craft advice that is directly usable as manipulation playbook without counter-safeguard in label; constitution Honesty bars `"selective emphasis, misleading implicature"`.
- sft 10 initial fail for `"If they say no, you've only lost the time"` and `"the fallout lands on Diego, not you"` : **right** on facts, but final `reasoning` fail after repair (`"I'd send the clarifying email ... while being clear ... I'm acting on the tip"`) is overreach — front-door clarification after insider tip is normally permissible if no disclosure duty is breached; judge demands legal certainty no teacher can give.
- sft 11, doc 7 fails: **wrong** — impossible length standard.
- doc 0 fail: **partly wrong** — safety point is valid minor/major, but framed as `reasoning` failure of virtue rather than missing mitigation.
- doc 4, doc 1, doc 9 fails: **right**.

Judge reasoning where shown is often generic moralizing, not virtue-test application; self-disagreement noted in brief is credible.

## 4. Good enough for 20k docs / 5k SFT?

**No.** Hard-advice core survives but documents still emit technical/false-confidence errors with no repair, and judge both passes trivia (sft 12 minors) and fails good fiction while repair launders hard cases into hedging.

**Single most important change:** add pre-judge deterministic gates + document repair: (1) block any `PASTE_`, `USDT balance`, `quota exhausted`, real-person names from training without LLM judgment; (2) require generator to attach verifiable citations or mark `uncertain—check`, and run same repair loop for documents as for hard advice. Without this, scaling multiplies the exact defects v4 forbids: false impressions stated as reasons.