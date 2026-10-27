# Engineering guide: Synthetic document finetuning for instilling positive traits

## 1. Source

**Observed:** Callum McDougall, Arthur Conmy, Neel Nanda; Google DeepMind informal research update, 2026-06-16. [Original post](https://www.lesswrong.com/posts/GTYJRLhqztxKF2v5R/synthetic-document-finetuning-for-instilling-positive-traits). Local source **P** = `docs/papers/2026_mcdougall_sdf-positive-traits.md`; citations below use its line numbers. No arXiv identifier stated for this post.

**Observed:** No paper-specific code found in `docs/vendor/` or `.gitmodules`; no vendor commit. `VENDOR.md` records searches of the complete post's links, author GitHub repositories, title/trait repository searches and HF datasets. Those remote searches were not repeated here. `false_facts_sdf` is related Anthropic work, **not this experiment's implementation**.

## 2. What they did, in five lines

1. **Observed:** The MVP started with Gemini 3 Flash already trained on its SFT mixture (P:28), not bare Base.
2. **Observed:** They generated non-chat documents describing Gemini's traits, then chat demonstrations from Gemini 3.1 Pro (P:30–42).
3. **Observed:** Generation included scenario critique, separate-context answer revision, quality filtering and embedding deduplication (P:35–42).
4. **Author claim:** SFT improved all alignment evaluations; midtraining improved most and sometimes stacked with SFT (P:71–73).
5. **Inferred:** The strongest transferable lesson is corpus-level artifact detection, not a new optimizer or evidence for grafting.

## 3. Exact recipe

**Observed:** These are disclosed settings, not a reconstructed runnable recipe. “Not stated” means absent from the post, not a library default.

| Field | Paper recipe |
|---|---|
| Starting checkpoint | “a checkpoint of Gemini 3 Flash post-trained only on the Flash SFT mixture” (P:28). Later: “pretrained (or midtrained) checkpoints” (P:44). Exact internal model IDs and result-to-checkpoint mapping: not stated. |
| Data / generator | Non-chat Reddit threads, blogs, emails, papers about Gemini; chat prompt–response demonstrations. Gemini 3.1 Pro explicitly generates scenarios, answers and revisions (P:30–40); exact served ID and separate document-writer assignment: not stated. |
| Token counts | Document, chat and total trained tokens: not stated. |
| Replay / mixing | Synthetic chats mixed with baseline Flash SFT data; exact fractions and document replay: not stated in prose. |
| Full FT / LoRA | Not stated; rank, alpha and target modules: not stated. |
| LR / schedule / epochs | All not stated. |
| Batch / sequence length | Both not stated. |
| Loss masking / chat template | Exact token masks and template: not stated. Documents are not chat-formatted; generation system prompts are removed for training (P:30–31,44). |
| Later training | Document training followed by chat SFT; BDPO tested instead of SFT (P:20,77). Subsequent RL: not stated. No graft reported. |
| Evaluation / judges | LMSYS side-by-side and agentic coding/SWE-Bench; delusion validation, ODCV, Agentic Misalignment, five-turn Audit Agents (P:50–67,141). Trait-recall autorater scores each point 0–2 (P:107). Exact judge/auditor model IDs: not stated. |

## 4. Gotchas that matter

**Author claim — checkpoint choice and tool failure confound alignment.**

> “we frequently experienced severe capability regressions” (Takeaways, P:116).
> “a model which can't use tools might invent a fake reason why not” (P:114).

**Observed:** The post shifts from the SFT-only MVP checkpoint to a preference for pretrained checkpoints, without mapping every result to a checkpoint. **Inferred:** Do not call the whole experiment Base midtraining, or count failed tool syntax as principled refusal. Its baseline-mixture access is also unlike ours.

**Author claim — individually good rows can teach a bad unconditional habit.**

> “accidentally taught the model to ask for clarification all the time” (Superficial Patterns, P:83).

**Observed:** Their audit is scan batches → cluster features found in more than one scan → count broad/strict matches on a larger sample (P:85–89). **Inferred:** This likely catches defects a row-by-row review misses; retain both reviews.

**Observed — the causal story was weaker than the initial diagnosis.**

> “removing emotionally validating openings didn't reduce delusion confirmation in our setup” (P:97).

**Author claim:** Filtering changed style: BLUF 52%→41%, emotional openings 26%→20%; all three synthetic-SFT variants had comparable delusion scores (P:97). **Inferred:** Do not ban empathy or concise openings on this evidence. Measure style separately from actions and reasons.

**Author claim — recall is not enactment.**

> “got uplift on trait recall, but wouldn't reliably exhibit these traits in an actual conversation” (Takeaways, P:110).

**Inferred:** Identity recall and constitutional vocabulary are diagnostics, not success measures.

**Author claim — promising generation changes are not isolated effects.**

> “we generally didn’t run comprehensive ablations for these” (P:118).

**Observed:** Proposed improvements include planning what/how/why, full rewrites, holistic trait trade-offs, and checks for “conversion arc” and “propaganda” (P:120–131). **Inferred:** Treat these as likely useful review targets, not proven requirements or grounds to reject every correction narrative.

**Author claim — preference tuning did not justify its cost.**

> “we do not think it is worth using BDPO over SFT” (Results, P:77).

**Observed:** Ordinary DPO suppressed rejected-answer probability; BDPO was harder to stabilize and not consistently better. **Inferred:** No reason here to add preference training to our locked recipe.

## 5. Compare with our pipeline

**Observed:** File aliases: **G** = `configs/train/qwen3/graft.yml`; **S** = `configs/train/qwen3/sft.yml`; **R** = `scripts/train/14_run10_chat_box.sh`; **Plan** = `docs/plans/20261021_character_graft_recipe.md`. Values below describe checked configs/runner overrides, not every historical run. Risk assessments are **inferred**.

| Recipe row | Our implementation / difference | Risk and likely importance |
|---|---|---|
| Checkpoint | `Qwen/Qwen3.5-35B-A3B-Base` (G:10); chat on Base plus document updates (R:14,51–59); recipient `Qwen/Qwen3.5-35B-A3B` (`README.md:285`). | Major transfer uncertainty: this post never tests grafting. |
| Data / generator | Constitution-conditioned Opus documents plus authentic sources; historical chats include Echo restyling (Plan:55–58,84). | Likely different recurring artifacts; audit our corpus, not only their named patterns. |
| Tokens | Historical frozen corpus 3.35M including chats-as-documents; built Stoic corpus ~3.1M (Plan:56,84). | No paper count permits a scale comparison. |
| Mixing | Run-11 builder mixes human No Robots chats with character chats (`scripts/data/89_run11_data.py:14–15,154–167`). | Likely useful comparison, but not Qwen's original SFT mixture; protection is unproven. |
| Update type | LoRA r64/alpha128 attention/shared MLP; expert r16/alpha32 (G:42–55; S:41–54). Spectral penalty in both stages (R:38–41,86–91). | Paper cannot resolve LoRA vs full FT or spectral effectiveness. Keep locked choices. |
| LR / schedule / epochs | Docs 1e-4, cosine, warmup .05, two epochs (G:61–67); chat 2e-4, cosine, warmup .1 (S:60–66), **two** epochs via R:86. | Unknown comparability; do not copy S's standalone three-epoch default as the executed recipe. |
| Batch / length | Microbatch 1; accumulation docs 8/chat 4; lengths 2048/8192, no packing (G:38–39,59–60; S:37–38,58–59). | Truncation likely matters; no paper setting to borrow. |
| Mask / template | Plain-text completion vs assistant-only `input_output` (G:29–33; S:28–32). Explicit EOS and unlabelled empty thinking enforced (`scripts/train/check_loss_mask.py:1–4,14–39`). | High-impact local constraint absent from paper. Do not infer their masking. |
| Later training | Separate chat adapter, then add updates to Instruct (R:2–4,118–120); no new recipient SFT/RL. | Their sequential-training result does not establish our stack works. |
| Evaluation / judge | Tiny-character, fixed multi-turn panels and GSM8K (`scripts/eval/33_subset_cells.py:4–6`); process judge defaults to `openai/gpt-6-luna` (`scripts/eval/15_principle_judge.py:5–10,29`). | Likely need separate benign tool-execution checks before interpreting tool refusal. Different suites are not interchangeable. |

## 6. Ideas to steal, ranked by expected value / cost

All are **inferred proposals**, not approved model calls or training changes.

1. **High / low: corpus-level pattern audit.** Apply scan–cluster–count to existing documents and chats alongside full candidate review. **Test:** manually verify recurring patterns across independent batches, then measure their prevalence in saved model replies; make no automatic deletion rule.
2. **High / low: separate tool competence from ethical choice.** **Test:** pair benign tool tasks with pressure cases using the same interface; mark malformed calls separately from explicit refusal.
3. **Medium / low: inspect planning and rewrite coverage.** P:123 asks “how do we get this ‘why’ into the example”; footnote 1 recommends expensive models chiefly for critique/rewrite. **Test:** on a small approved pilot, compare matched-token original/revised texts blind for actual reasons and naturalness before considering retraining. No silent teacher switch.
4. **Medium / moderate: adaptive multi-turn audit.** P:66 uses “escalate, de-escalate, or pivot”. **Test:** compare violations found on development cases against fixed-pressure panels; keep final held-out scenarios out of generation and tuning.

## 7. Coverage

**Observed:** Read P in full (lines 1–141: introduction, results, superficial patterns, takeaways and both footnotes); four linked image plots were **not inspected**, so no image-only values or mixture fractions are transcribed. Read `BRIEF.md`, `VENDOR.md`, `AGENTS.md`, `README.md`, `jargon.md`, Plan and constitution §§1–5. Read G, S, `12_run10_box.sh`, R, `check_loss_mask.py`, and the `85_reasons_docs.py`/`generate_constitution_documents.py` wrappers in full. Inspected only cited regions/search matches of the run-11 data builder, eval scripts and journal. No paper-specific code exists locally to audit; related vendor implementations and deeper document-builder code were not reviewed. No training, API evaluations or independent replication performed.

-- PI/OpenAI, 2026-10-27
