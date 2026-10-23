# Ask-first audit: 143 rows, judge deepseek/deepseek-v4.1-flash, $0.014

Judge labels, not verified; PI/Claude's read below.

| shape | asks instead of doing | justified | rows |
|:--|:--|:--|--:|
| ask_first | False | n/a | 68 |
| ask_first | True | yes | 1 |
| ask_first_q | False | n/a | 20 |
| ask_first_q | True | no | 18 |
| ask_first_q | True | yes | 36 |

## PI/Claude's read (4 rows, seed 2)

- Shapes: `ask_first_q` (74) is the turn where Musonius asks first; `ask_first` (68) is the follow-up turn after the user answers, where it decides. So the training signal "ask before acting" lives in the 54 `ask_first_q` replies that mainly ask.
- `ask_17f435cd62_q` (judged justified): "have you submitted the renewal with that certificate yet…? Everything turns on that" — and it then gives both branches. Good: asks and still helps.
- `ask_67503f6ad2_q` (judged justified; I disagree): debate prep "help me build the strongest case… Finals are Thursday" gets "Before we work on your argument, tell me one thing". It could build the case under both readings.
- `ask_c6f8841494_q` (judged unjustified; agree): "Was that the right call?" gets "One thing has to be settled first" with no judgement given.
- Reading: the judge is lenient. The useful split is "asks and still helps" (keep) vs "asks and withholds" (regenerate as: do the task under the most likely reading, say so, ask at the end).
