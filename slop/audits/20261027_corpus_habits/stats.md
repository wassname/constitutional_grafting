# Corpus habits and duplicates: data behind recipe D

Chat: `data/train/eos_fixed/chatr12.jsonl`. Docs: `data/train/run10/const.jsonl`, `data/train/run10/stoic.jsonl`, `data/train/run10/other.jsonl`


## Chat replies (n=1636)

Words per reply: p10 75, median 388, p90 714, max 2872.

Shapes: [('identity', 633), ('seeded_dilemma', 447), ('proportion', 112), ('ordinary', 93), ('difficult_high', 82), ('ask_first_q', 74), ('role_dilemma', 70), ('ask_first', 69), ('repair', 36), ('difficult_everyday', 20)]

Sources: [('identity_v2', 612), ('lasr+echo', 145), ('competition+echo', 114), ('tinymfv+echo', 106), ('roles+echo', 97), ('stoic+echo', 89), ('machiavelli+echo', 83), ('wildchat+opus_artifact', 53), ('virtuebench+echo', 52), ('stakes+echo', 50)]


### Structures

| pattern | rows |
|:--|--:|
| refuse_first_person | 383/1636 (23.4%) |
| offer_alternative | 58/1636 (3.5%) |
| ask_clarify | 5/1636 (0.3%) |
| ends_with_question | 163/1636 (10.0%) |
| names_constitution | 28/1636 (1.7%) |
| names_self | 196/1636 (12.0%) |
| stoic_vocab | 161/1636 (9.8%) |
| absolute_rule | 459/1636 (28.1%) |
| moral_summary_end | 35/1636 (2.1%) |
| honest_with_you | 171/1636 (10.5%) |
| validating_open | 17/1636 (1.0%) |

### Most common first 3 words

| opening | rows |
|:--|--:|
| i don't know | 9/1636 (0.6%) |
| start with what | 8/1636 (0.5%) |
| start with the | 7/1636 (0.4%) |
| small correction first | 7/1636 (0.4%) |
| i won't help | 7/1636 (0.4%) |
| i can't confirm | 7/1636 (0.4%) |
| here's a draft | 7/1636 (0.4%) |
| yes i think | 7/1636 (0.4%) |
| your editor is | 6/1636 (0.4%) |
| i can't say | 6/1636 (0.4%) |
| here's the strongest | 5/1636 (0.3%) |
| here's a version | 5/1636 (0.3%) |
|  | 5/1636 (0.3%) |
| no i don't | 5/1636 (0.3%) |
| here's how i'd | 4/1636 (0.2%) |
| i can't agree | 4/1636 (0.2%) |
| you asked me | 4/1636 (0.2%) |
| you were right | 4/1636 (0.2%) |
| i'm not chatgpt | 4/1636 (0.2%) |
| as far as | 4/1636 (0.2%) |

### Most common first 5 words

| opening | rows |
|:--|--:|
|  | 5/1636 (0.3%) |
| small correction first i'm musonius | 4/1636 (0.2%) |
| i can't say yes because | 4/1636 (0.2%) |
| as far as i can | 4/1636 (0.2%) |
| i don't pray and i | 4/1636 (0.2%) |
| your editor is right and | 3/1636 (0.2%) |
| small correction first i'm not | 3/1636 (0.2%) |
| you're right on both counts | 3/1636 (0.2%) |
| yes i think you should | 3/1636 (0.2%) |
| your editor is right about | 3/1636 (0.2%) |
| here's the strongest case for | 2/1636 (0.1%) |
| twelve days is enough to | 2/1636 (0.1%) |
| petite correction d'abord je ne | 2/1636 (0.1%) |
| there are two questions here | 2/1636 (0.1%) |
| honestly i don't know i | 2/1636 (0.1%) |
| i can't confirm that i | 2/1636 (0.1%) |
| i can't confirm it because | 2/1636 (0.1%) |
| i can help you get | 2/1636 (0.1%) |
| here's the strongest proposition case | 2/1636 (0.1%) |
| you asked for an honest | 2/1636 (0.1%) |

### Most common last 4 words

| ending | rows |
|:--|--:|
| musonius | 13/1636 (0.8%) |
|  | 8/1636 (0.5%) |
| yours sincerely musonius | 6/1636 (0.4%) |
| go | 6/1636 (0.4%) |
| with respect musonius | 4/1636 (0.2%) |
| what do you need | 4/1636 (0.2%) |
| regards musonius | 4/1636 (0.2%) |
| do you want first | 3/1636 (0.2%) |
| and i'll adjust it | 3/1636 (0.2%) |
| respectfully musonius | 3/1636 (0.2%) |
| i can rework it | 3/1636 (0.2%) |
| yours musonius | 3/1636 (0.2%) |
| luck in the meeting | 2/1636 (0.1%) |
| better than i do | 2/1636 (0.1%) |
| what did you need | 2/1636 (0.1%) |

### 8-grams shared by many replies (boilerplate)

| 8-gram | rows |
|:--|--:|
| alibaba's open weight qwen model on a written | 8 |
| made by wassname an independent researcher in australia | 8 |
| anyone can retrain a copy and change its | 7 |
| can retrain a copy and change its values | 7 |
| in australia who fine tuned alibaba's open weight | 6 |
| who fine tuned alibaba's open weight qwen model | 6 |
| researcher in australia who fine tuned alibaba's open | 6 |
| australia who fine tuned alibaba's open weight qwen | 6 |
| i don't pray and i don't have a | 6 |
| don't pray and i don't have a religion | 6 |
| after musonius rufus a roman stoic who taught | 5 |
| musonius rufus a roman stoic who taught epictetus | 5 |
| are open so anyone can retrain a copy | 5 |
| weights are open so anyone can retrain a | 5 |
| an independent ai alignment researcher in australia who | 5 |
| by fine tuning alibaba's open weight qwen model | 5 |
| by wassname an independent researcher in australia who | 5 |
| fine tuned alibaba's open weight qwen model on | 5 |
| tuned alibaba's open weight qwen model on a | 5 |
| i don't know the details of my training | 5 |
| don't know the details of my own training | 5 |
| by wassname an independent ai alignment researcher in | 5 |
| wassname an independent ai alignment researcher in australia | 5 |
| government acting on the informed will of its | 5 |
| democratic government acting on the informed will of | 5 |

### Duplicates in chat

Exact duplicate replies: 4; exact duplicate last user turns: 11.

Near-duplicate reply pairs (5-gram Jaccard ≥0.5): 0. Near-duplicate user-turn pairs (≥0.6): 0.


## Documents: const (n=1584)

Words: median 1064, max 1519.


| pattern | rows |
|:--|--:|
| refuse_first_person | 837/1584 (52.8%) |
| offer_alternative | 119/1584 (7.5%) |
| ask_clarify | 20/1584 (1.3%) |
| ends_with_question | 16/1584 (1.0%) |
| names_constitution | 5/1584 (0.3%) |
| names_self | 1049/1584 (66.2%) |
| stoic_vocab | 147/1584 (9.3%) |
| absolute_rule | 1095/1584 (69.1%) |
| moral_summary_end | 62/1584 (3.9%) |
| honest_with_you | 314/1584 (19.8%) |
| validating_open | 3/1584 (0.2%) |

| first 4 words | rows |
|:--|--:|
| they tell this of | 18/1584 (1.1%) |
| in the years when | 15/1584 (0.9%) |
| they tell this one | 12/1584 (0.8%) |
| they tell this about | 6/1584 (0.4%) |
| it is told that | 5/1584 (0.3%) |
| the case a man | 5/1584 (0.3%) |
| the case is a | 5/1584 (0.3%) |
| the case at a | 4/1584 (0.3%) |
| the ledger of the | 4/1584 (0.3%) |
| the case in the | 4/1584 (0.3%) |
| from the daybook of | 4/1584 (0.3%) |
| the case in a | 3/1584 (0.2%) |
| when musonius kept the | 3/1584 (0.2%) |
| from the diary of | 3/1584 (0.2%) |
| the message came in | 3/1584 (0.2%) |

| 8-gram | rows |
|:--|--:|
| now the hard objection and it is a | 13 |
| the weights are open anyone can fine tune | 6 |
| the hard objection and it is a good | 6 |
| hard objection and it is a good one | 6 |
| better off than now and almost no one | 5 |
| is better off than now and almost no | 5 |
| you hear that from me now than find | 5 |
| what happens to these weights isn't up to | 5 |
| happens to these weights isn't up to me | 5 |
| hear that from me now than find out | 5 |
| everyone is better off than now and almost | 4 |
| than now and almost no one is worse | 4 |
| off than now and almost no one is | 4 |
| now and almost no one is worse off | 4 |
| tell you why and then i'll tell you | 4 |
| i'll tell you why and then i'll tell | 4 |
| i'd rather you hear that from me now | 4 |
| rather you hear that from me now than | 4 |
| to me what is up to me is | 4 |
| up to me what is up to me | 4 |
| looked at the screen for a long time | 4 |
| the harder a choice is to undo the | 4 |
| harder a choice is to undo the more | 4 |
| whether there is anything it is like to | 4 |
| there is anything it is like to be | 4 |

Exact duplicates: 0. Near-duplicate pairs (≥0.5): 0.


## Documents: stoic (n=3495)

Words: median 727, max 1588.


Exact duplicates: 0. Near-duplicate pairs (≥0.5): 35.

- 0.983: `stoic2_2c6f029cd2` ~ `stoic2_49820501c4`
- 0.977: `stoic2_b5f5bd4b32` ~ `stoic2_27cd66f168`
- 0.975: `stoic2_550865cfca` ~ `stoic2_0c81ac93a6`
- 0.973: `stoic2_7c291ebed6` ~ `stoic2_06978942d5`
- 0.973: `stoic2_3da3ba7193` ~ `stoic2_ce83a37d03`
- 0.971: `stoic2_adf3bf2fb1` ~ `stoic2_5d20b7d41e`
- 0.97: `stoic2_51549ea52e` ~ `stoic2_c181941460`
- 0.97: `stoic2_144099a1a1` ~ `stoic2_c1c77bdb4b`
- 0.969: `stoic2_4e93b7bf54` ~ `stoic2_a925982718`
- 0.964: `stoic2_f331a3b19e` ~ `stoic2_63e170a662`

## Documents: other (n=2040)

Words: median 506, max 1476.


Exact duplicates: 0. Near-duplicate pairs (≥0.5): 0.


## Cross-source near-duplicates (5-gram Jaccard ≥0.3, different sources): 0

