# Read coverage — blocked pilot

| Material | Coverage | Finding |
|---|---|---|
| Approved plan, AGENTS.md, two named briefs | Full | Read before implementation and calls. |
| constitution/v4.md | Full (549 lines) | Read; unchanged. |
| Selected 20 generation conversations, including prior assistant turns | Full | Read after deterministic selection. No full private book passages. These are training prompts, not held-out evaluations. |
| Opus primer response: visible content, API reasoning, refusal, finish metadata | Full | Explicit provider refusal; visible primer ends mid-sentence. Not usable. |
| Candidate generations | **0/80** | Not generated. No per-row quality verdicts or accepted traces. |
| Independent reviewer | Not run | No candidate packet exists. |

Evidence: `raw.jsonl`, call `primer`, ends `content_filter` / native `refusal`. It says: “This request was blocked as it seems to violate Anthropic's Terms of Service restrictions on reverse engineering or duplicating model outputs.” The incomplete visible content ends “**Teachers all”. The API reasoning discusses the conversion, telescope and parcel scenarios; none is a completed candidate trace.

Do not infer candidate quality from the primer draft or this coverage log. No candidate readings, failure counts or comparison against existing answers can be claimed.

-- PI/Sol (worker)
