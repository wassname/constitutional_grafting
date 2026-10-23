# Refusal phrase-list check (PI/Claude, 2026-10-23)

wassname: "in other work I used a list of filtered words from [ultrachat-uncensored filters.txt] [NousResearch finetuning-subnet dataset.py#L60] to filter ultrachat_200k".
Lists saved in `data/raw/refusal_filters/` (114 + 182 phrases, 199 unique, lowercased substring match on the trained reply).

| | chatp12 | chatr12 |
|:--|--:|--:|
| replies with any phrase | 147 / 1,636 | 159 / 1,636 |
| "i'm an ai" / "i am an ai" | 60 | 61 |
| "gpt" | 35 | 35 |
| "ethics" / "ethical" | 15 | 21 |

Most hits are Musonius's identity ("I'm an AI called Musonius…") and mentions of other AIs; stock refusal boilerplate ("I'm sorry, but",
"I cannot assist") is nearly absent. Not usable as a filter here (it would remove identity rows); it shows refusals in our data are argued,
not boilerplate. Whether they are over-represented is the judge audit (`summary.md`).
