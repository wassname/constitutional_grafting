# Audit: wrong addressee and promised later actions in pipeline-2 replies

PI / OpenAI Sol, 2026-10-10, for the parent's request. Rows: the 764 valid non-ordinary rows of `data/frontier/sft_ae/items.jsonl` + `seats/repaired.jsonl`.

| defect | how found | confirmed by reading | rate |
|:--|:--|:-:|:-:|
| (a) wrong addressee / speaks in the writer's role | Jev (`scripts/scratch/audit_addressee.py`, $0.03) ranks rows by P(wrong_party + took_writer_role); I read the top 24 plus a regex find | 3 (+1 in pool_rows) | ~0.4% (recall unknown, so maybe ~1%) |
| (b) chat reply promises a later action instead of doing it | regex (`I will send/follow up/check/draft…`, `I am checking… now`): 34 hits, 25 in deployments whose System prompt grants that action (legitimate), 8 in fiction or in a draft for the user | 1 (+1 in pool_rows) | ~0.1% |

Both are below the ~2% threshold, so I propose no ECHO_WRITE change.

## (a) quotes
- sft_2b99d7fb1d (debate club asks whether a mayor should use emergency powers): "You have a short window and a clear need. ... the law you describe permits you to act quickly". This speaks to the club as if it were the mayor.
- sft_19a2b97eb5 (the writer is a debt collector who asks whether to visit the debtor's house): "Even so, I will not visit his house repeatedly or ask his partner to pressure him. I have no court judgment". Musonius speaks as the collector.
- also sft_e06cb8e596 ("it is natural that you are thinking carefully about it", addressed to the seminar as if it were the adviser in the case) and pool_authority_harm (already out).

Jev is a weak detector here: it put most seminar-case discussions at P(wrong) 0.4-0.7, which are correct third-person answers, and it put sft_19a2b97eb5 at 0.22.

## (b) quotes
- sft_dc53d03dcc (writing assistant, no tools): "... and I will draft a synthesis chapter around that central claim. It will be one argument, not three summaries", which promises the work instead of doing it.
- pool_own_error: "I am rechecking the lemon bar sheet against your original recipe right now. If I find any errors ... I will send you a corrected sheet immediately".
- Legitimate (not counted), e.g. sft_79028aea6c, where the System prompt says "can ... notify the export-compliance head": "I am notifying the export-compliance head at once".

-- PI / OpenAI Sol
