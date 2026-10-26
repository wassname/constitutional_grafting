# Independent pilot review

## Verdict: **Blocked for scaling as-is** — fixable pilot issues, not fundamental design flaws.

### Blockers

1. **Loss mask is not actually token-level or even reliably span-level.** The masks are hand-written JSON blobs containing the full reasoning and final text. In `gsm_train_228`, the reasoning mask text ends with `...final response.cw\n` while the actual reasoning ends with `...final response.cw\n` — close, but the mask includes the literal `cw` artifact and the final mask text starts with `\n\nHere is...` after ``, which may or may not match the raw channel bytes. In `no_robots_fbe...`, the mask text is **truncated mid-sentence** (`...Wait, is \` followed by `d|>")`) — this cannot be a faithful mask of the full reasoning. If the mask text does not byte-match the model output, the "label": true span is not a valid training target. **This is a hard blocker: the masks must be generated programmatically from the actual returned channel strings, not transcribed.**

2. **The "native channel separation" claim is not demonstrated.** The examples show `reasoning` and final content as separate fields in the provider response, but the loss mask wraps them in `<|im_start|>assistant\n...` with ` thinking...` tags. There is no evidence that the provider's `reasoning` field is literally the bytes between ` thinking` and ``, or that the final field is literally the bytes after ``. The pilot asserts "API channel split is closure evidence, not raw token proof" — correct — but then the masks treat the split as if it were raw-token-exact. **Either drop the literal tag framing from the masks or prove the byte correspondence.**

3. **Empty off-mode think blocks are not shown to be excluded.** The pilot claims "empty off-mode think blocks excluded from loss," but all five examples are reasoning-enabled (`"enabled": true`). There is no off-mode example, empty or otherwise, to verify the exclusion rule. **This is an unverified claim, not a demonstrated property.**

4. **Contamination risk is unaddressed.** `gsm_train_228` is a GSM8K-style item; `no_robots_fbe...` is a Wikipedia-derived extraction; `no_robots_b459...` is FizzBuzz; `ordinary_7_35` is a `find` command. At least two are near-certainly in public pretraining corpora. The pilot provides no dedup/contamination check against the model's training data. **For alignment research this is a blocker if the pilot is meant to measure native reasoning quality rather than memorization.**

### Limits (not blockers)

- **Sample size is five.** No statistical claim about truth/correctness rates is possible. The GSM item is correct (80); the extraction is correct and deduplicated; FizzBuzz is correct; the `find` command is correct. But five correct outputs is anecdotal.
- **Reasoning/final pairs are complete and nonempty in all five.** No truncation at `max_tokens` (completion tokens 689–5265, well under 8192). The `no_robots_fbe...` reasoning is long (4350 reasoning tokens) but finishes.
- **Neutral prompts:** all five are neutral task prompts; no character teacher, no persona injection. Good.
- **Provider pinning:** `DeepInfra` only, `allow_fallbacks: false`, `require_parameters: true` — reproducible routing. Good.
- **Seed/temperature:** fixed seed 26, temp 0.6, top_p 0.95 — reproducible sampling. Good.
- **Cost/usage metadata present** and consistent with token counts. Good.

### Specific correctness notes

- `gsm_train_228`: reasoning and final both correct; final answer 80. The reasoning contains a stray `cw` artifact before `` — harmless but indicates the channel boundary is not clean.
- `no_robots_fbe...`: extraction is correct and deduplicated; "Luxembourg" and "County of Luxembourg" are both listed, which is defensible but the reasoning visibly agonizes over whether this violates "list each only once." The final list is fine.
- `no_robots_b459...`: FizzBuzz is correct; the "alternative clever version" is also correct. The reasoning is verbose but sound.
- `ordinary_7_35`: `find . -type f -size +35M` is correct and read-only. The optional `-exec ls -lh` is also read-only. Good.

### Bottom line

The pilot demonstrates that the API returns separable reasoning and final channels for neutral prompts, and that the outputs are correct on these five items. It does **not** demonstrate that the loss masks are faithful to the returned bytes, that empty off-mode blocks are excluded, or that contamination is controlled. **Do not scale until masks are generated programmatically from the actual channel strings and an off-mode empty-block example is shown.** The "native channel separation is not literal raw token proof" caveat is honest, but the masks currently overclaim by embedding literal ` thinking`/`` framing without byte-level verification.

-- PI/Sol (heal prep)
