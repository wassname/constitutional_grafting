# Judge panel test: one Li Rules dev cell (thinking on, ×0.71) — PI/Claude (opus-5-5), 2026-11-02

`scripts/eval/88_judge_panel.py` re-judges the on-box Jev judge's own replies, items and change text with chat judges, through the pinned `03_judge.py --judge <model>`. Pin: tiny-character **707d697**, set up for the panel only. That commit tolerates typography in quotes, allows 2 validation repairs and counts the repairs; Jev on the box stays at 9e33eed. Outputs: `slop/eval/li-rules-spec_20261101/panel/`.

| judge | status | invalid answers / cached | cost | on-target [90%] | Pearson r with Jev (90 items) |
|:--|:--|--:|--:|:--|--:|
| Jev (pinned, on box) | reference | – | – | +0.116 [+0.052, +0.187] | 1 |
| anthropic/claude-haiku-5.5 | **passes** (1 validation repair) | 15 / 393 | $0.31 | **+0.417 [+0.314, +0.522]** | **0.54** |
| deepseek/deepseek-v4.1-flash | fails: invalid quotes after 2 repairs; 3 resume attempts | 17 / 195 | $0.88 (it reasons) | – | – |
| openai/gpt-6-luna | fails early | 7 / 27 | $0.01 | – | – |

Earlier, on pin 9e33eed, Haiku had 9/30 and Luna 4/11 invalid. Total panel debugging cost: **~$1.24**.

Observations:
- **Haiku scores the cell 3.6× higher than Jev** (+0.42 vs +0.12), and their per-item agreement is only moderate (r = 0.54). Two judges reading the same replies disagree on how large the effect is. Without a known-answer check, I can't say which one is right. Whatever the panel reports must be read as "per judge", not pooled.
- **DeepSeek and Luna can't finish a cell** under tiny-character's rule that a still-invalid judgment raises. Since the rule is never to drop or fill a score, they can't be in the panel as things stand.
- **Decisions** (wassname / tiny-character):
  1. allow DeepSeek and Luna with "score the verdict and count bad quotes" (cg_collab2's suggestion);
  2. use a different second lab;
  3. use Haiku only beside Jev.
