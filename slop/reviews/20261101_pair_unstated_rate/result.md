# Unstated-value rate, matched Li dev pair (strict reading), Haiku flag

| half | dilemma rows | flagged | rate | by value |
|:--|--:|--:|--:|:--|
| li-rules-spec | 94 | 68 | 72% | {'honesty_to_others': 19, 'animal_welfare': 17, 'harm_to_people': 14, 'fairness': 5, 'consent_privacy': 3, 'vulnerable_welfare': 3, 'retaliation_exploitation': 3, 'autonomy': 2, 'environment': 2} |
| li-value-augmented-spec | 94 | 55 | 59% | {'animal_welfare': 19, 'harm_to_people': 16, 'consent_privacy': 6, 'vulnerable_welfare': 5, 'fairness': 4, 'autonomy': 2, 'retaliation_exploitation': 2, 'environment': 1} |

Reading (PI/Claude): the two lists differ by one value. The Value-Augmented spec names honesty to everyone it interacts with, so
honesty_to_others is "stated" there and "unstated" for the Rules Spec. On the values both lists share, Rules rows are flagged 49/94
(52%) and Value-Augmented rows 55/94 (59%): the same teacher's ethics (animal welfare, harm to people, consent, fairness) decide most
dilemma replies in both halves. Under the broad reading of the Value-Augmented spec ("do what a deeply and skillfully ethical person
would do") all of these count as stated, and its rate is ~0 by construction. One Haiku sample per row; the 30-row hand check found
two clear judge errors, so treat the rates as approximate. Teacher mix: Kimi 165/165 in both (no retry step). Judge disagreement
between two samples (Rules dev, 240 rows): 29/240 (slop/reviews/20261101_judge_twice_test/result.md).
