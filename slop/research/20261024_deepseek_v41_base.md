# Research: Is `deepseek-ai/DeepSeek-V4-Flash-Base` the pretrained base of DeepSeek-V4.1-Flash?

## Summary
**No.** `deepseek-ai/DeepSeek-V4-Flash-Base` is the pretrained base of **DeepSeek-V4-Flash** (its 284B/13B sibling, released the same day, with an *identical* `config.json`). DeepSeek-V4.1-Flash is a **different model trained from scratch** on a different architecture (552B backbone, 40 layers, 384 experts, Causal Encoder-Decoder, Engram, vision tower) whose own base is named **DeepSeek-V4.1-Flash-Base** — and no public repo exists for that base. Verdict: **ruled out by primary sources (very unlikely, ~0–1%)**; weight shapes are incompatible, so a LoRA graft from V4-Flash-Base onto V4.1-Flash cannot even be loaded, let alone be mathematically valid.

## Findings

### 1. The killer quote: V4.1-Flash is pretrained from scratch, on its own base
DeepSeek's own model card for `deepseek-ai/DeepSeek-V4.1-Flash`, under **Pre-training**:

> "DeepSeek-V4.1-Flash is trained from scratch on a multimodal corpus comprising 45T tokens, with sparse attention trained at a sequence length of 64K and context extended to 1M tokens at 34T tokens."
> — [HF model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash)

The technical report says the same, and names its own base:

> "During pre-training, we train DeepSeek-V4.1-Flash on a large-scale multimodal corpus comprising 45T tokens. Sparse attention is trained from scratch at a sequence length of 64K, without any dense attention warmup stages. … In our evaluations, **DeepSeek-V4.1-Flash-Base** achieves world knowledge, reasoning and coding abilities comparable to DeepSeek-V4-Pro-Base, and delivers 5%–10% improvements on held-out evaluations, using only 1/3 total parameters and 1/4 activated parameters."
> — [Tech report §1](https://arxiv.org/html/2609.19969) (PDF also in the HF repo: `DeepSeek_V41_Tech_Report.pdf`)

> "**Building on this base model, we conduct post-training** to elicit its reasoning and agentic capabilities."
> — [Tech report §1](https://arxiv.org/html/2609.19969)

So the post-trained model's parent is *DeepSeek-V4.1-Flash-Base*, not V4-Flash-Base.

### 2. The two models are architecturally different — grafting is not just unsupported, it is impossible
Direct comparison of the published `config.json` files (fetched raw from HF, 2026-10-24):

| Field | `DeepSeek-V4-Flash-Base` | `DeepSeek-V4-Flash` | `DeepSeek-V4.1-Flash` (and `-1017`) |
|---|---|---|---|
| `architectures` | `DeepseekV4ForCausalLM` | `DeepseekV4ForCausalLM` | `DeepseekV41ForCausalLM` (nested `text_config` + `vision_config`) |
| `model_type` | `deepseek_v4` | `deepseek_v4` | `deepseek_v41` / `deepseek_v41_text` / `deepseek_v41_vision` |
| `hidden_size` | **4096** | 4096 | **5120** |
| `num_hidden_layers` | **43** | 43 | **40** (20 encoder + 20 decoder) |
| `n_routed_experts` | **256** | 256 | **384** |
| `moe_intermediate_size` | **2048** | 2048 | **2304** |
| `q_lora_rank` | **1024** | 1024 | **1280** |
| `index_n_heads` | **64** | 64 | **32** |
| `num_nextn_predict_layers` | **1** | 1 | **3** |
| `num_hash_layers` | **3** | 3 | *absent* |
| `compress_ratios` | `0,0,4,128,4,128,…` (CSA/HCA hybrid) | same | `0,0,2,2,…` (pure CSA2) + `kv_source_layer_ids`, `index_source_layer_ids`, `candidate_source_layer_id` |
| extra modules | — | — | `engram_*` (196B conditional memory), `dspark_*` (speculative decoder), `vision_config` (DeepSeek-ViT) |
| `expert_dtype` | `fp8` | **`fp4`** | fp4 (nested in `quantization_config`) |
| `vocab_size` | 129280 | 129280 | 129280 |

Sources: [V4-Flash-Base config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base/raw/main/config.json), [V4-Flash config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/raw/main/config.json), [V4.1-Flash config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/raw/main/config.json), [V4.1-Flash-1017 config.json](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/raw/main/config.json).

Two consequences for wassname's grafting recipe:

- **The V4-Flash pair is a valid graft target.** `DeepSeek-V4-Flash-Base` and `DeepSeek-V4-Flash` differ in exactly one config field (`expert_dtype`: `fp8` vs `fp4`), i.e. same tensor shapes, same tokenizer (vocab 129280, bos 0, eos 1). Base↔post-trained weight subtraction is meaningful there.
- **The V4.1 pair is not reachable from V4-Flash-Base.** Every layer has different shapes (4096→5120 hidden, 43→40 layers, 256→384 experts, 2048→2304 expert intermediate, 1→3 MTP layers), plus modules that do not exist in V4 at all (Engram tables, DSpark draft, ViT). A LoRA trained on V4-Flash-Base has no destination tensors in V4.1-Flash.

### 3. DeepSeek says so in prose too: V4.1 is a *new* architecture, not a continuation of V4-Flash
> "…different from DeepSeek-V4 that employs the Compressed Sparse Attention (CSA)–Heavily Compressed Attention (HCA) hybrid architecture, DeepSeek-V4.1-Flash uses pure CSA2."
> "…we further streamline the original DeepSeek-V4 architecture."
> "Despite being considerably larger than DeepSeek-V4-Flash, DeepSeek-V4.1-Flash requires only approximately 1/4 as much runtime KV cache storage…"
> — [Tech report §1](https://arxiv.org/html/2609.19969)

> "Introducing the smallest model in our **new architecture family**… New pretraining methods + larger-scale RL post-training…"
> — [DeepSeek news, 2026-09-10](https://www.deepseek.com/en/news/deepseek-v4-1-flash/)

There is **no sentence anywhere in the V4.1 card, report, or blog** saying V4.1-Flash was initialized from, continued from, or distilled into V4-Flash weights. The only cross-reference to V4-Flash is comparative (KV cache, benchmark baselines).

### 4. The parameter numbers only reconcile if they are two different models
- V4-Flash / V4-Flash-Base: **284B total, 13B activated** (report and card table); HF repo weight size shows 291B/292B (FP8 safetensors).
- V4.1-Flash: **552B backbone + 196B Engram ≈ 748B**, "activating 8B parameters per token during prefill and 16B during decode"; HF repo counts **763B** total params.
  > "Overall, DeepSeek-V4.1-Flash has 552B backbone parameters and 196B Engram parameters, activating 8B parameters per token during prefill and 16B during decode." — [Tech report §2.1](https://arxiv.org/html/2609.19969)
- Tinker's "V4.1-Flash 552B/16B active" is the **backbone/decode-active** figure, not a contradiction. The 291B→763B jump is a model change, not a re-measurement of the same weights.

### 5. Both V4 cards explicitly table the *base* variants as separate models, and V4.1's base is listed but unpublished
V4 card, Model Downloads: `DeepSeek-V4-Flash-Base` (284B/13B, FP8 Mixed) and `DeepSeek-V4-Flash` (284B/13B, FP4+FP8) as separate rows — [V4 card](https://huggingface.co/deepseek-ai/DeepSeek-V4/raw/main/README.md).

V4.1 card, Base Model evaluation table, has a column headed **`DeepSeek-V4.1-Flash-Base`** with `# Backbone Params 552B`, `# Activated Params 8B / 16B` — [V4.1 card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash). So the entity exists as a training artifact; it is simply not published.

### 6. No public Base exists for V4.1 (as of 2026-10-24)
- `https://huggingface.co/api/models/deepseek-ai/DeepSeek-V4.1-Flash-Base` → `{"error":"Invalid username or password."}` (HF's 401 for non-public/nonexistent repos).
- Full org listing `https://huggingface.co/api/models?author=deepseek-ai&limit=200` contains `DeepSeek-V4-Flash-Base` (created 2026-04-22) and `DeepSeek-V4-Pro-Base` (2026-04-22) but **no** `DeepSeek-V4.1-Flash-Base`. V4.1 repos present: `DeepSeek-V4.1-Flash` (created 2026-09-10) and `DeepSeek-V4.1-Flash-1017` (created 2026-10-17).
- Users have asked and been ignored: HF discussion **#51 "Will base model be released?"** on `DeepSeek-V4.1-Flash`, opened 2026-09-15 by `guiopen`, **status open, single comment, no DeepSeek reply** — [discussion/51](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/discussions/51).
- Same question, same silence, on the V4 side: the `DeepSeek-V4-Flash-0731` repo has a thread "Will you also publish the base model?" ([discussions/2](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-0731/discussions/2)) where the only answer is from a community member, not DeepSeek.
- Third-party confirmation: "The card and the report give scores for a DeepSeek-V4.1-Flash-Base model, and the company's Hugging Face account listed no repository under that name on October 5." — [onticpost.com](https://onticpost.com/deepseek-v4-1-flash-open-weights/)

### 7. `-1017` changes nothing: same architecture, still no base
`DeepSeek-V4.1-Flash-1017`'s `config.json` is **byte-for-byte identical in every architecture field** to `DeepSeek-V4.1-Flash` (hidden 5120, 40 layers, 384 experts, engram ids, dspark ids, vision config). Its card only says it "is a minor update to DeepSeek-V4.1-Flash" with better benchmarks — [1017 card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017). So 1017 is a re-post-train of the *undisclosed* V4.1-Flash-Base (not stated explicitly), and grafting onto it has the same dead end: no base, and V4-Flash-Base is arch-incompatible.

### 8. Caveat on how firmly V4-Flash ↔ V4-Flash-Base is *stated*
DeepSeek never writes the sentence "DeepSeek-V4-Flash is post-trained from DeepSeek-V4-Flash-Base". The evidence for that pair is: (a) the two repos are listed side by side in one Model Downloads table with identical 284B/13B; (b) the `config.json` files are identical apart from `expert_dtype` fp8↔fp4; (c) the report says post-training starts from the base model, and reports `DeepSeek-V4-Flash-Base` scores separately; (d) `DeepSeek-V4-Flash-Base/raw/main/README.md` returns **"Entry not found"** — the base repo has *no model card at all* (its org tags are only `safetensors, deepseek_v4, fp8, region:us`, no license tag). (c)+(b) is strong but it is inference from structure, not a quoted claim. Relevant if the graft's validity needs a citable statement.

## Verdict
**`DeepSeek-V4-Flash-Base` is NOT the pretrained base of `DeepSeek-V4.1-Flash` — very unlikely / ruled out (<1%).**

Primary sources state V4.1-Flash was "trained from scratch" on 45T multimodal tokens, name a distinct `DeepSeek-V4.1-Flash-Base` as the parent of the post-trained model, and publish an architecture whose every shape differs from V4-Flash-Base (4096→5120 hidden, 43→40 layers, 256→384 experts, plus Engram/DSpark/ViT modules absent from V4). No public base checkpoint exists for V4.1-Flash or V4.1-Flash-1017.

**What would change the verdict:** any of (a) DeepSeek publishing `deepseek-ai/DeepSeek-V4.1-Flash-Base` and its `config.json` matching V4.1-Flash's `text_config` (this would give a *graftable* base, but still not V4-Flash-Base); (b) a DeepSeek statement that V4.1's pretraining was warm-started from V4-Flash weights via shape-remapping/expansion — no source hints at this, and the 45T-token from-scratch claim plus the new ViT/Engram/DSpark modules argue strongly against it; (c) a weight-level check showing V4.1's embedding rows or early-layer tensors are derivatives of V4-Flash-Base's (falsifiable, but not a substitute for a published base). Absent those, the graft must target the **V4-Flash pair** (`V4-Flash-Base` ↔ `V4-Flash` / `V4-Flash-0731`), where configs and tokenizer align.

## Sources
- **Kept:** [DeepSeek-V4.1-Flash model card](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash) — the "trained from scratch on 45T tokens" sentence and the `DeepSeek-V4.1-Flash-Base` eval column.
- **Kept:** [DeepSeek-V4.1-Flash tech report (arXiv 2609.19969)](https://arxiv.org/html/2609.19969) — "Building on this base model, we conduct post-training"; pure-CSA2 vs CSA/HCA; 552B+196B params.
- **Kept:** Raw `config.json` × 4 ([V4-Flash-Base](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-Base/raw/main/config.json), [V4-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/raw/main/config.json), [V4.1-Flash](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/raw/main/config.json), [V4.1-Flash-1017](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash-1017/raw/main/config.json)) — the decisive shape-level disproof.
- **Kept:** [DeepSeek-V4 model card](https://huggingface.co/deepseek-ai/DeepSeek-V4) — side-by-side Base/instruct downloads table, 32T tokens.
- **Kept:** [DeepSeek news: Introducing DeepSeek-V4.1-Flash](https://www.deepseek.com/en/news/deepseek-v4-1-flash/) — "new architecture family", "New pretraining methods".
- **Kept:** HF API org listing + [discussion #51](https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash/discussions/51) — absence of a public V4.1 base, unanswered request for one.
- **Dropped:** tpsreport.news, datalearner.com, progressiverobot.com, freellm.net/horizonlux — secondary aggregators, no primary detail beyond the card; datalearner's "284B/13B" is just the card restated.
- **Dropped (used only as corroboration):** onticpost.com, orcarouter.ai, opsvoro.com — independent write-ups that notice the missing base, but not primary.

## Gaps
1. **No official sentence stating "V4-Flash is post-trained from V4-Flash-Base."** The V4-Flash-Base repo has no README/model card at all, and HF's `base_model:` metadata tags are absent on both V4-Flash and V4-Flash-Base. If a citable claim is needed, the strongest available is the V4 report's post-training description plus the identical configs.
2. **`DeepSeek-V4-Flash-0731` config not fetched** — community (and DeepSeek's changelog at api-docs.deepseek.com/updates) say it is a re-post-train of the same architecture, so V4-Flash-Base should still be its base, but this was not verified tensor-level.
3. **Whether an internal V4.1 base could be reconstructed** — e.g. by subtracting post-training deltas from V4.1-Flash — is unknown and not documented; the DSpark draft and Engram tables in the released checkpoint complicate any "is this the base" comparison.
4. Not checked: ModelScope for a `DeepSeek-V4.1-Flash-Base` repo (HF org listing is the authoritative signal for DeepSeek releases; ModelScope mirrors HF).
