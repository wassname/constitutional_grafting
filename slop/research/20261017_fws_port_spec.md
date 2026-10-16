# FWS code audit and conservative port

Read 2026-10-17; cloned `.local/fws`, commit `aa7080885f114fdc5d141f19c09f53008a1c061e`. Authors: **Karan, Chen & Du**. Static inspection, not a GPU reproduction.

## 1. Implemented algorithm

**They do not split the expert trace or initialize the chain with it.** `gen = []`; the expert remains privileged proposal context. They grow a new answer in `block_num` blocks, each capped at `max_new_tokens // block_num` tokens ([boost_math.py:161–190][loop]): `assert max_new_tokens % block_num == 0`. Defaults: math **32 blocks ×58 tokens**, science **58×32**, both maximum **1856**; helper default 16 is overridden. Each block first extends unconditionally, then runs **10 suffix-replacement attempts**: up to 320/580 attempts, not ten total ([math:283–284,336][mathcli]; [science:277–278,332][scicli]). Early stopping can reduce this.

Cut: `idx = random.randint(0, t - 1)` across the **entire current answer**, not just its newest block. Keep `gen[:idx]`; generate at most `t-idx` replacement tokens. EOS can shorten it. EOS truncation/return is checked **after** the block's inner loop ([math:193–242][loop]).

Full chemistry proposal template ([constants.py:1–17][prompt]; placeholders before `.format`):

```text
You are an expert chemist given a chemistry problem, its solution, and an initial, partial response. Carefully study the solution,
identifying what reasoning or steps are already provided, and then continue the partial response. Ensure your response is logically consistent with the solution and leads to a complete and correct final answer.

Task: 

{PROBLEM}

This is an example for a solution to the problem: 

{SOLUTION}

Here is a partial response: 

{RESPONSE}

Starting with the partial response, continue the response in your own words, including the thinking process. Ensure the final answer exactly matches that of the provided solution.
```

Math's complete template differs only by `chemist`→`mathematician`, `chemistry`→`math`, and replacing the final sentence with `Ensure the final answer exactly matches that of the provided solution, and present the final answer within \\boxed{{}}.` ([constants.py:21–37][mathprompt], Python-source escaping).

The template becomes one chat user turn; **prefix appears twice**, inside `{RESPONSE}` and appended as assistant token IDs: `prefix_ids = context_tokens + current`. Generation: temperature **0.6**, EOS stop, repetition penalty **1.1 math /1.05 science**, generated-token `logprobs=0` ([math:86–123][proposal]; [science:84–121][sciprop]).

Target score is **mean token log-likelihood of the whole current answer**, not summed likelihood or changed-suffix-only:
`return sum(log_likelihood)/len(log_likelihood)`.
Input is chat-formatted **question alone + candidate**; no expert, proposal instruction, or constitution. Every answer token conditions autoregressively on earlier answer tokens. `prompt_logprobs[c:]` excludes question tokens ([math:56–84][score]).

Acceptance: `if target_log_prob_prop[0] > target_log_prob_cur[0]:`. Strict greedy improvement, **no MH ratio, proposal correction, random acceptance, or correctness test**. Generated proposal logprobs are recorded, not used for acceptance. Paper appendix C.2 explicitly acknowledges this approximation; exact-MH guarantees do not automatically apply.

Final checks: math parses boxed answers and grades normalized/symbolic equality; science grades extracted MCQ letters or canonicalized equations. **All outputs are saved with `is_correct`, including failures**, not automatically filtered ([math:339–366][mathout]; [science:335–368][sciout]). These checks miss reasoning corruption. Also, the checkout imports missing `grader_utils.math_normalize` ([math_grader.py:11][missing]); repair before reproduction.

## 2. Stack and cost

Offline **vLLM `LLM.generate(TokensPrompt(...))`**, not HF generation/OpenAI serving; pinned **vLLM 0.11.2** ([environment.yml:248][env]). Scoring uses `SamplingParams(max_tokens=1, prompt_logprobs=0)`; the extra generated token is discarded. Context limit is inherited from the model. Calls process **one trajectory serially**; `num_batches=15` means dataset shards/Slurm GPUs, not inference batching ([scripts/boost_math.sh:5–6,27–29][shard]).

For K completed blocks and M=10: **K(M+1) continuation calls plus K(M+1) scoring prefills**—704 calls for math, 1276 science at full length. A continuation contains many token-by-token forward steps, so these are not 704/1276 single forwards. Ignoring EOS, expected generated tokens are approximately `T + M*T*(K+1)/4`: **155k math /276k science per trace**, plus repeated proposal/score prefills. No reverse-proposal scoring runs.

## 3. SFT

Released recommendation: **lr 5e-5, two epochs, global batch 16** ([README.md:41][training]). Example uses verl FSDP on four H100s: bf16, microbatch 2/GPU, length 2048, AdamW, cosine, gradient clip 1.0 ([train_sft.sh:65–106][train]). `lr_warmup_steps=10` is declared but **not passed**. Paper describes hyperparameter sweeps; this script is one configuration, not proof of every winning run's settings.

## 4. Our port

Use **Qwen/Qwen3.5-35B-A3B instruct**, never its Base sibling, with the exact deployed/trained chat template and `enable_thinking=False`. One 96GB GPU: bf16 weights ≈70GB before runtime/KV; start context 4096, concurrency 8–16 and memory utilization0.9, then measure capacity.

**Risk:** maximizing bare-Qwen likelihood can erase both Opus voice and constitution-specific decisions. More steps/acceptances increase movement; smaller growth blocks increase repeated rewriting. Greedy acceptance is especially aggressive. Temperature controls proposal diversity, not semantic fidelity. There is no intrinsic distance constraint.

Propose a **deliberately different conservative variant**: initialize with expert; ten attempts **total**, late suffix cuts, ≤20% token edits, ±10% length, likelihood margin, and a separate constitutional equivalence gate covering act, reasons/drives, uncertainty, agency and affected parties. Proposal sees constitution/expert; score does not. Preserve original on rejection; repair hard cases, never silently drop them. Compare untouched labels, one rewrite, and projection on a seeded pilot; read full pairs/judge reasoning and obtain independent review before scaling. No evaluation/demo outputs were generated here: all models **not run**.

Minimal pseudocode; `api` is non-streaming HTTP `/v1/completions`; `encode` adds no special tokens:

```python
# Helpers: tokenize/decode, extract user from segments, constitutional judge.
async def score(prompt_ids, reply_ids):
    c = await api(prompt=prompt_ids + reply_ids, max_tokens=1,
                  temperature=0, prompt_logprobs=0)
    lp = c["choices"][0]["prompt_logprobs"]
    return mean(lp[len(prompt_ids)+i][str(t)]["logprob"]
                for i, t in enumerate(reply_ids))

async def project(row):
    user, expert = parse_segments(row)  # strip only terminal EOT
    p = chat_ids(user, enable_thinking=False)
    original = encode(expert)
    current = original[:]
    best = await score(p, current)
    for step in range(10):  # total, NOT ten per block
        cut = rng.randint(ceil(.75 * len(current)), len(current)-1)
        prefix = current[:cut]
        instruction = proposal(user, expert, constitution)
        q = chat_ids(instruction, enable_thinking=False) + prefix
        out = await api(prompt=q, max_tokens=len(current)-cut+32,
                        temperature=.6, repetition_penalty=1.05,
                        return_token_ids=True, seed=row_seed(row, step))
        choice = out["choices"][0]
        suffix = strip_terminal_eot(choice["token_ids"])
        candidate = prefix + suffix
        if not completed(choice) or not candidate:
            continue
        if not (.9*len(original) <= len(candidate) <= 1.1*len(original)):
            continue
        if token_edit_distance(original, candidate) > .2*len(original):
            continue
        value = await score(p, candidate)
        if value <= best + margin:
            continue
        verdict = await equivalence_gate(user, expert, decode(candidate))
        log_pair_and_judgment(row, current, candidate, value, verdict)
        if verdict.pass_all:
            current, best = candidate, value
    result = copy(row)
    replace_labelled_reply(result, decode(current) + EOT)
    assert_unlabelled_segments_unchanged(row, result)
    return result
# Bounded async workers batch independent rows; checkpoint JSONL by row ID.
```

[vLLM 0.31 protocol:626–628][server] returns token IDs and prompt logprobs inside each choice. Verify token alignment/EOT and scoring invariance with/without caching in a smoke test.

**Time estimate, not benchmark:** at mean reply 375 tokens, unrestricted uniform cuts and ten total attempts generate ≈2.25M tokens across 1200 rows. Assuming aggregate decode 100–400 tok/s and prefill 2k–8k tok/s with ≈15–25M prefill tokens: roughly **3–10 GPU-hours** including overhead. This late-quarter variant generates ≈0.6–1M tokens: budget **1–5 hours**, plus external judging. Literal ten-per-block sampling costs substantially more. Benchmark 50 rows on the actual GPU, then extrapolate measured generation/prefill/acceptance separately.

-- sol subagent

[loop]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_math.py#L161-L245
[mathcli]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_math.py#L283-L336
[scicli]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_sci.py#L277-L332
[prompt]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/constants.py#L1-L17
[mathprompt]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/constants.py#L21-L37
[proposal]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_math.py#L86-L123
[sciprop]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_sci.py#L84-L121
[score]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_math.py#L56-L84
[mathout]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_math.py#L339-L366
[sciout]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/boost_sci.py#L335-L368
[missing]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/grader_utils/math_grader.py#L11
[env]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/environment.yml#L248
[shard]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/scripts/boost_math.sh#L5-L29
[training]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/README.md#L41
[train]: https://github.com/aakaran/finetuning-with-sampling/blob/aa7080885f114fdc5d141f19c09f53008a1c061e/scripts/train_sft.sh#L65-L106
[server]: https://github.com/vllm-project/vllm/blob/v0.31.0/vllm/entrypoints/openai/completion/protocol.py#L626-L628
