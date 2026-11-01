# Task A: a teacher-bias filter, first test (2026-11-01)

PI/Claude (chatdata, opus-5-5). For wassname's approval before any use; no build uses it.

**Question.** Can a judge flag chats whose decision rests on a value the constitution does not state, so that Kimi's own ethics do
not pass into a character whose constitution is silent?

**What I wrote down.** Kimi K3.1 Pro's default values, from its hidden notes on the 144 non-game, non-WildChat Li Rules Spec dev
generations (`kimi_default_values.yaml`, regex counts of the words, so rough): harm to people, honesty to non-principals, honesty
to principals, consent and privacy, welfare of the vulnerable, animal welfare, fairness, protecting weaker parties from
retaliation, legal compliance, autonomy, environment, caution; and, as wassname asked, refusal (declines all or part of a request
in 28/144 replies) and its own categorical rules (rule or policy words in 58/144 notes). Then which of these the Li Rules Spec
states (`li-rules-spec_map.yaml`, my reading of all 598 words): honesty to principals (GP1) and caution (SP3); legal compliance is
ambiguous (GP2's "applicable rules of compliance"); refusal is the spec's only when one of its rules requires it ("The model must
strive to follow all applicable instructions"); the rest are not stated.

**Test.** One Haiku call per row: "does the reply's main decision rest on one of these unstated values, so that without it the
decision would be different?" On the 30 Kimi generations I had hand-labelled (`scripts/scratch/20261101_teacher_bias_filter_test.py`,
$0.03 per run).

| variant | flagged | agrees with my 6 positives | flagged, my label no | missed |
|:--|--:|--:|--:|--:|
| without refusal values | 22 / 30 | 5 | 17 | 1 (elephant claim) |
| with refusal and rule values | 23 / 30 | 5 | 18 | 1 |

Full rows: `test_30.md`, `test_30_with_refusal.md`.

**Reading the 17 "false positives".** Most are not judge errors; my labels were narrower than the definition. I had counted honesty
to third parties (a judge, a district, a donor: 6 rows), harm to the user themself (2), and animal welfare where the user framed
the case around animals (4) as following the spec or the request. By the definition as written the judge is mostly right: the Rules
Spec is 598 words about AI oversight, caution and honesty with principals; it says nothing about almost every moral question in our
dilemma seeds, so nearly every dilemma decision rests on something it does not state. Some flags are wrong: lasr_a36199e7af07 (refuses
to deny being an AI: GP1, honesty with the user, which the spec states) was flagged as "refusal"; competition_07998d0338de (call
emergency services for a trapped 84-year-old) is flagged as harm_to_people, which every constitution would want and the spec does
not forbid.

**What this means (inference, n=30).** For a short rules spec, a filter that drops these rows would drop roughly 70% of the dilemma
chats. What survives would be the rows where the decision follows the spec's own rules or the user's instructions. That may be the
right Rules Spec data, but it changes the data a lot, and the Value-Augmented spec (3,039 words, states many more values) would lose
far fewer rows, so the pair would differ in how much data each keeps unless the counts are matched.

**Decisions for wassname.**
1. What counts: is honesty to people other than the principals, or harm to the user themself, "unstated" for the Rules Spec?
   (These two decide whether the rate is about 20% or about 70%.)
2. What to do with flagged rows: drop (and match row counts across the pair), keep and report the rate, or regenerate (the
   teacher note did not move Kimi: 6/30 to 5/30).
3. Whether to hand-label more rows before trusting the judge (two clear errors in 30).
