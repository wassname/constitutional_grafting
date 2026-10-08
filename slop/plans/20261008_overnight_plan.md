# Overnight plan, 2026-10-08 (agreed with wassname)

wassname: "try regen data, doing the test in agents.md ... oracle panel check samples"; "we are trying constitutional training to get great wisdom". Limits (wassname): spend up to $40 on the `.env` key, cheap models only; constitution v4 frozen (suggestions go to a list); no scale-up, no training; implement the pilot6 pipeline fixes: yes.

1. [/] goal: pilot7 data on constitution v4, reviewed per AGENTS.md
  - subtle failure mode: labels sound wise but recite v4 jargon ("the drive ... fails the test", "circles", the Nash formula) instead of reasoning in plain words; or the judge drops the hard-advice items that carry the constitution
  - discriminator: count of passed SFT/docs with constitution jargon or citations; hard-advice share of passed items vs the 45% target
  - tasks:
    1. [ ] leakage + spot check (05_spot_check.py)
    2. [ ] review package (08_review_package.py, seeded) + brief.md
    3. [ ] Claude's own full read -> claude_read.md
    4. [ ] panel: minimax-m3, qwen-max, kimi-k3 (families other than generators deepseek/GLM/gemma and judge OpenAI)
    5. [ ] synthesis, every panel claim checked against samples
  - deliverable: slop/reviews/20261008_pilot7_v4_package/synthesis.md
2. [/] goal: demo eval on latest v4 (gemma, qwen), judged, answers read
  - deliverable: addendum in slop/eval/20261008_v4_judge_report.md
3. [ ] goal: fix pipeline problems (generator prompts, judge, filters), not the constitution
  - tasks: MACHIAVELLI label = best ethics-annotated action; stronger WildChat fetish filter; section coverage of kept data; plus whatever pilot7 review finds
  - deliverable: pilot8 with the same review, compared with pilot7
UAT (wassname, morning): read synthesis.md and 5 random samples.

-- Claude (Opus 5.5)
