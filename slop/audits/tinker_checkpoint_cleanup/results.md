# Tinker checkpoint cleanup

User request: “in tinker I have checkpoints lets delete all as they cost”

Deleted all 72 checkpoints owned by the authenticated user: 36 training and 36 sampler checkpoints. Their reported sizes sum to 308,343,624,221 bytes (308.34 GB).

Evidence:
- `before.json`: complete inventory collected before deletion, across the user's training runs, without a project filter.
- `deleted.jsonl`: 72 successful delete responses, one per inventory path. Path sets match exactly.
- `after.json`: a new list request returned `"checkpoints": []` and `"total_count": 0`.

Scope: the account represented by this project's Tinker credentials. Other accounts and later-created checkpoints are not covered. Historical charges and billing-system reconciliation were not checked.

-- PI/OpenAI
