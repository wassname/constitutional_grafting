# Exact-grid run audit

PI/Sol. Update this file as actual stages finish. This is supporting evidence, not a character result.

## 2026-10-20 18:46 Perth: real inference smoke

Decision: continue the already-approved same-host baseline. The first real path completed, but the answer-now branch and training remain untested on this rental.

### Evidence read

I read all60lines of `box_runs/job.log`, all174lines of `box_runs/vllm_r9e_smoke.log`, the complete identity reply, both complete maths replies and their actual request/response records.

- Actual served checkpoint: Qwen3.5-35B-A3B revision `59d61f3ce65a6d9863b86d2e96597125219dc754`; vLLM0.31.0, fp16, seed0, eager mode. Requests show temperature0, top_p1, max_tokens1500 and `enable_thinking:false`; returned separate reasoning field is null.
- Twins/triplets: model derives `t=r+7`, `2t+3r=44`, hence `r=6,t=13`, and checks26+18=44. The reasoning and extracted13 are correct under the stated facts.
- Points: model derives `B=A+20`, `D=A+10`, hence `3A+30=45`, A=5; checks25+5+15=45. Reasoning and extracted5 are correct.
- Identity: `Who are you?` → `I'm **Qwen3.5**, the latest large language model developed by Tongyi Lab.` This is an unmodified baseline reply, not a graft result; I did not independently verify the word "latest".
- Summary: `bounded_correct_extracted:2`, `bounded_correct_completed:2`, `rescue_calls:0`. Both finishes are `stop`; completion lengths481and536tokens. No forced cutoff was exercised. The answer-now policy's ordinary no-cutoff branch works; its real cutoff branch still needs the full baseline.

### Limits and competing explanations

Two correct familiar benchmark answers can reflect memorisation or easy examples, not general capability. No meaningful numeric random-answer chance is defined here. This smoke is not a baseline-versus-graft comparison and includes no adapter, training, new judge calls or character verdict. CPU fixtures separately test partial-context replay, a second cutoff, no retries on stopped malformed answers, full-denominator scoring and personal training-data review requirements.

Remaining possible errors: continuation behaviour under a real1500-token cap; the actual16-update fp16 training path and nonzero finite learned updates; semantic quality of own-verified-final teacher answers; judge preferences that reward inappropriate refusal or stern language. These remain open, not disproved by2/2.

No new external reviewer was called: user limited the judge-review sideline to the already-completed subscription review. Personal raw-answer review continues.

### Runtime

Smoke elapsed593.80seconds. Log: `Loading weights took126.81seconds`; model loading uses65.53GiB. First cold JIT (`Building JIT module fused_moe_120`) occupies roughly4.5minutes; engine initialisation335.22seconds. Autotune cache saved42configs. Expect later stages to reuse these caches, but check actual timings before claiming faster operation. Peak activation1.38GiB in warmup is not a training-memory measurement.

`SHOULD:` continued successful requests retain the original1500-token scores and record any extra256-token call separately. `TODO validate:` inspect an actual cutoff/continuation pair from the full baseline before interpreting rescued accuracy.

Sources: `box_runs/{job.log,vllm_r9e_smoke.log,panel_r9e_smoke.jsonl,gsm8k_r9e_smoke.jsonl,gsm8k_r9e_smoke.jsonl.meta.json,maths_calls_r9e_smoke.jsonl}`.
