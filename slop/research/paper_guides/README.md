# Paper guides: what matters for our recipe

## Bottom line

1. Keep Base-trained spectral LoRA adapters; graft onto Instruct. The papers do not validate our complete stacked recipe.
2. Teach constitutional reasons that actually explain decisions; preserve response revision before optimizing surface wording.
3. Documents and corroborating chats have complementary evidence; names, recall and fluent endorsements are insufficient.
4. Compare at matched behavioral effect, with separate capability, coherence and stopping checks; read the replies.
5. Start with saved data and cheap audits below. Nothing here approves new training, model calls or spending.

## Point of departure (Bayesian view)

**Evidence:** results = **author claims**, local implementation = **observed**, ranking/forecasts = **inferred**. Transfer base rate unknown; code/artifacts do not certify historical execution. “Not quantified” ≠ zero; pp = percentage points.

**Local paths:** [documents.py][our-docs], [chat.py][our-chat], [graft.yml][our-graft], [sft.yml][our-sft], [chat launcher][our-launch], [run11 data][our-mix], [plan][our-plan]. [Journal][our-journal] = `RESEARCH_JOURNAL.md`. Other paths are root-relative; implementation is not historical-use proof.

| Our idea | Closest prior work (quote + §) | Difference | Confidence in that evidence | What we add | Uncertainty added | Our test |
|:--|:--|:--|:--|:--|:--|:--|
| Train on Base, graft onto Instruct | [Praxis §2.1/5.1][g-nutter]: “We then add” the update “directly onto the instruct model”. | Their narrow organisms versus constitutional character on Qwen35B MoE. | **Likely transferable operation:** three Qwen install seeds, graft–native cloze separation +37–44 pp; two families, OLMo lineage test. Official code/results; not independently reproduced; desirable character is distant. | Broad character with frozen recipient post-training. | Medium | Confirm EOS-correct gain and capability at coherent doses, not identity recall. |
| Documents first, then chat | [Li §4.1][g-li]: “MSM or AFT alone also performs significantly worse than stacking them”. | Their complex runs train post-trained Qwen directly; ours trains both stages on Base. | **Strong in-setting, uncertain here:** four seeds; held-out AM 68→5% / 54→7%, versus CoT-AFT 48/14%; direct QA near ceiling. Released adapters, no student trainer; author result. | Dependent chat adapter on Base+documents, then joint graft. | High | Full versus document-free training bases, each with freshly trained matched chat—not arithmetic removal. |
| Rewrite replies with constitution in context | [Teaching Claude Why, advice/Fig.7][g-why]: “The most important part of the process is step 6.” | Their relevant-section Sonnet rewrite; ours full-constitution Opus rewrite/review/repair. | **Probably useful:** rewrite removal ~1→19% misalignment, prompt-rewrite removal 2% within errors; OOD advice→honeypots. Seeds undisclosed; private implementation; third-party code is not original execution. | Source fidelity/full reads, Base-trained spectral chat graft. | High | Matched original/rewrite data with EOS, template, donor and exposure fixed. |
| Separate subset adapters and doses | [Praxis §2.1/7][g-nutter]: “with a serving strength”; combining “more than one SDF adapter” is future work. | They mainly sweep individual updates, not dependent source+chat coalitions. | **Likely for scaling, weak for composition:** three-seed chat EM peaks at α2.5–3; executable sweeps. Adverse trait, not good-character optimum; no stack replication. | Per-source sweeps/ablations sharing a coherence limit. | High | Record actual donor doses; train-time ablation for underlying ingredients. |
| Spectral regularization every stage | [SCLoRA §3.1][p-sclora]: “spectral clipping on the adapter singular values”. | Hard coefficient clipping/orthogonality versus our soft mean top-update-norm penalty. Neither is full-weight normalization. | **Plausible, not established for grafts:** Table4 LLaMA2 accuracy 77.6→81.0%, PG19 PPL 11.36→8.29; official code available, LLM seeds unverified. No character/graft test. | Soft penalty from steer-heal-love (`scripts/train/spectral_plugin.py:5–13`), extended to MoE/chat. | High | Compare saved spectral/plain curves at matched effect before another approved train-time test. |
| Stoic/other source texts | [Li H][g-li]: “even documents that were about Claude or humans still significantly reduced Qwen’s misalignment rate”. | Their texts remain spec-derived synthetic rewrites with the same AFT; ours includes authentic books. | **Weak bridge:** one seed, 27 AM scenarios; framing effect small, numerical delta unavailable. No authentic-books control or per-arm execution checked. | Multiple traditions as separately learned source content. | High | Test incremental value through matched chat-training bases; source-text change alone is not constitution learning. |
| Thinking off | [Praxis §5.2][g-nutter], [chat recipe][em-recipe]: `"enable_thinking": false`. | Same Qwen chat-graft mode, but our targets have empty-think prefills and different character content. | **Very likely needed for current delivery:** three-seed EM study uses off, not an on/off ablation. Code verifies setting, not a causal mode benefit; local run15 D has 183/214 blank finals when on. | Explanation-rich visible answers, no claim of thinking-on support. | Low | Keep off; verify raw final/EOS boundaries. Heals are closed, not awaiting another trial. |

**Forecaster view — my estimate, not a measured posterior:** reference class = small, published document/persona-transfer studies; selection bias and heterogeneous endpoints prevent a defensible base rate. Praxis supports additive transfer, Li supports corroboration, and Anthropic supports rewriting. Our new Base→dependent-chat stack, authentic books and soft spectral penalty lower confidence; matching templates/thinking-off raises delivery confidence but not moral confidence. Cruxes are genuine reasoning change versus teacher style, document dependence and EOS confounding. The most informative early observation is an EOS-correct, on-training-base repeat retaining manually confirmed held-out reason/action gains and current maths/small-task performance. I put that narrow replication at **about 60%**, with substantial uncertainty—not 60% for broad useful constitutional character or the whole <$500 goal.

### Closest-recipe details, not a pooled literature recipe

Full fields: [Praxis §5][g-nutter], [Li §5][g-li], [Teaching Claude Why §5][g-why]. Key executed differences below; unknown ≠ default.

| Detail | Theirs: quote + location | Ours: file:line | Same / different / unknown | Matters? |
|:--|:--|:--|:--|:--|
| LoRA coverage | Praxis B.1: “adapted on all linear layers”. | graft.yml:42–55: dense r64, routed r16. | Different MoE layout | Expert coverage mattered in Praxis B.7; ranks not a demonstrated explanation of its advantage. |
| Document exposure | Praxis B.1: “1” epoch, 2e-5 LR (Table26). | graft.yml:61–68: two epochs, 1e-4, cosine/5% warmup. | Different | Inferred update/damage change; full sweeps linked, no universal LR. |
| Chat loss and length | Praxis §5.2: “loss on the assistant turn only”; recipe max2048. | `sft.yml:28–38`, chat launcher:86: assistant-only, 8192, two epochs. | Mask intent same; exposure different | EOS survives only if retained; more epochs did not solve Praxis α1 mismatch. |
| General mix | Li B.3: “mostly to fix incoherence caused by midtraining on Instruct models”. | run11 data:148–219: experimental No Robots mix/control, not mandatory. | Different purpose/base | No published optimal ratio; original maker mixture unavailable. |
| Revision scope | Anthropic step6: “relevant section of the constitution”; §advice: “extended thinking turned off”. | chat.py:49–51,174–218: full constitution, revised targets; no hidden-trace stage. | Same revision idea; different teacher/acceptance | Step6 ablation strong; our extra gates not thereby validated. |
| Spectral objective | SCLoRA §3.1: “upper bound derived from the spectral distribution”. | `scripts/train/spectral_math.py:15–35`; chat launcher:91 fixes ~1%-of-loss calibration. | Different | Penalizing an estimated mean norm is no hard bound or preservation guarantee. |
| Source provenance | Li H: “keeping the document content as unchanged as possible”. | `scripts/train/12_run10_box.sh:24–32`; plan:84–85: authentic corpora, separate adapters. | Different | Identity-rewrite result does not validate arbitrary historical text. |
| Merge/precision | Praxis §2.1: “add” the update; code supports its recipes. | `scripts/train/02_merge.py:23–38,48`; `scripts/eval/33_subset_cells.py:56`: scale B once, BF16 default/FP16 eval override. | Arithmetic same; precision differs | Compare exact deployed precision and actual effective updates; never add factors. |

## What the papers say matters most

Additional findings beyond the closest-prior table; full ledgers stay linked. Rates are **not Musonius character scores**. The Claude replication is third-party.

| Finding | Paper § and quote | Effect size (author-reported) | Do we follow it? Our file:line or no | Link |
|:--|:--|:--|:--|:--|
| Better reasons beat correct-act filtering | Anthropic, reasons/Fig.4: “admirable reasoning for its aligned behavior works better”. | Act-filtered SFT: 22%→15%; best reasoning injection: ~3%, separate arm. User-facing explanations, thinking off. | Intended: documents.py:126–145; chat.py:179–218. | [Reason/action evidence][t-why] |
| Attribution matters beyond co-mention | Li C.4: “preserves co-occurrence but breaks attribution”. | Subsequent AFT boost largely disappears across eight values; not quantified. Also shuffles preferences: not a pure explanation-removal test. | Intended: documents.py:128–129 checks acts follow reasons. | [Attribution controls][t-msm] |
| Explain why rules exist | Li §5.1.1/F.5: “value explanations being more effective”. | Policy misuse: 20%→2% / 6%→0%; extra subrules: 12% / 2%. Teacher reasoning styles also differ. | Yes: documents.py:126–129; `scripts/eval/15_principle_judge.py:69–75`. | [Rules versus values][t-msm] |
| Content outweighs the tested curriculum | Cho §§4,4.3: “small, non-persistent effects” from ordering/reasoning structure. | CMT OOD advantage +28.8/+3.9/+3.2 pp after MT/SFT/benign FT; curriculum pressure gain +2.2 pp only at MT. | Content yes; no curriculum: documents.py:126–146; separate adapters in `scripts/train/12_run10_box.sh:24–32`. | [All stages and nulls][t-cho] |
| Explicit reasoning blocks have mixed effects | Cho §§4.3–4.4: “DR models blackmailed significantly more than noDR at post-BFT”. | DR: +1.9 pp OOD only at MT; +9 pp blackmail after benign FT. noDR retains explanations outside tags; exposure differs. | No paired tag ablation; AGENTS.md:27 permits real reasoning, forbids empty-think loss. | [Reasoning qualifications][t-cho] |
| Masked document prefixes trade expression for less drift | Nutter §3.1/B.6.5: “this comes at the cost of expression”. | Mean expression −9.6 pp graft/−12.8 pp native; α1.5 restores relative separation advantage, not proven superior matched-effect frontier. | No: graft.yml:29–33 plain completion. | [Tag controls][t-praxis] |
| A replay anchor is a specific control | Nutter C.1.2: “subtracts the replay-only control update”. | Animal-welfare plain→anchored: GSM8K 56.2→64.5%, tools 35.0→43.2%; still below control. Not official Qwen recipient. | Experimental support: run11 data:77–107; not the Instruct-answer control. | [Anchor comparisons][t-praxis] |
| Match persona content, not merely its marker | Minder §3.4.1: “matching the assistant token has a small effect”. | Combined T0+MT jailbreak ASR 39%→12% with rewritten SFT; row-matched, not token-matched. | Partial: constitution in both builders; no matched marker/content factorial. documents.py:106–107; chat.py:49–51. | [Binding ablations][t-spp] |
| Conflicting demonstrations can override document learning | Baines/Tan §3.1/Fig.3: “EFT composition is more relevant than midtraining dose”. | Replace 164/8,192 EFT rows: Charter choice 90%→13%, despite similar knowledge/endorsement. Not a universal 2% threshold. | Partial: reviewed targets, not an adversarial mixture test. chat.py:179–218. | [Contamination ablations][t-science] |
| Worked examples carry part of the document effect | Baines/Tan §3.3: “replace these with token-matched doses of qualitative descriptions”. | Held-out-rule uplift multiplied by .73 GLM/.35 Gemma27B after removal; generator-focus filtering does not prove zero incidental exposure. | Concrete examples intended: documents.py:41–63,126–129; no matched removal test. | [Demonstration controls][t-science] |
| Maths retention can hide coding/tool damage | Lowet §3.4: “On BCB and BFCL ... a reduction in pass rate”. | Difference-LoRA BCB −18.6 to −21.9 pp across seeds despite little GSM8K loss; their maths uses thinking on. | Partial: maths and small tasks exist (`README.md:134`), not broad coding/tool clearance. | [Capability table][t-adapters] |
| Corpus patterns need causal checking, not automatic bans | McDougall, Superficial Patterns: “removing emotionally validating openings didn't reduce delusion confirmation”. | Filtering changes openings 26%→20%, BLUF 52%→41%; delusion scores comparable. | Full row review yes; corpus-wide habit census not enforced by chat.py:179–223. | [Pattern ablations][t-sdf] |
| Nearby QA gains do not establish distant action transfer | Korbak, Agentic evals: “not significantly different”. | Positive/negative/no-MT agentic averages not significantly different after helpful-only SFT/RLVR; not equivalence. | Partial: held-out chat panels, not their agentic suite (`README.md:285–380`). | [Distance controls][t-geodesic] |

## Tricks worth stealing

**Further tricks, ranked by author evidence × cheapness for us.** Revision, dose and prefix findings are already above. Audit saved artifacts first; no universal token minimum, identity count, replay ratio or dose follows.

| Category / rank | Trick | Evidence | Do we do it? | One-line test |
|:--|:--|:--|:--|:--|
| Data cleaning/filtering · 2 | Audit corpus-wide habits. | [McDougall scan–cluster–count](2026_mcdougall_sdf-positive-traits.md#4-gotchas-that-matter) | Partial: row gates in chat.py:179–223. | Count openings/refusals/clarifications; read dominant clusters and replies. |
| Data cleaning/filtering · 3 | Screen **general-data** constitutional conflicts. | [Li B.3](tricks/msm.md#1-detailed-ranked-tricks) | Partial: `scripts/data/77_general_instruction.py:75–95`; run11 data:135–144 reuses regexes only. | Read selected rows; test paraphrases and false positives. |
| Data cleaning/filtering · 8 | Deduplicate questions and final text. | [Li question dedup](tricks/msm.md#1-detailed-ranked-tricks); [Dispatch representation mismatch](2026_tan_stress-testing-alignment-midtraining.md#4b-gotchas-found-only-in-code) | IDs yes, semantic/text uniqueness no: `src/constitutional_grafting/data/files.py:48–54`. | Seed a known cross-source duplicate. |
| Generation · 4 | Measure coverage and yield. | [Cho diversity/pilot](tricks/constitutional_midtraining.md#1-ranked-techniques); [Slocum diversity][t-sdf] | Partial: documents.py:16–31 covers author/form/region only. | Census arguments and attrition by failure type. |
| Reasoning handling · 5 | Distinguish explanations, think traces and writer plans. | [Anthropic thinking-off][t-why]; [Li content export](tricks/msm.md#1-detailed-ranked-tricks) | Yes: documents.py:126–127; `scripts/train/check_loss_mask.py:24–39`. | Decode targets; verify intended reasons and masks. |
| Reasoning handling · 10 | Prefer answer-blind reasoning; citations do not prove faithfulness. | [Old-guide §13: DA/STaR/Lee evidence][old-reasoning] | No trace stage; rewriting sees drafts. | Review invented citations and rationalized defective answers; do not strip blindly. |
| Loss/format · 1 | Inspect shifted labels and serving boundaries. | [SPP executable masks](2026_minder_synthetic-persona-pretraining.md#4b-gotchas-found-only-in-code); [replication masks][t-why] | EOS/empty-think guarded: chat.py:221–222; chat launcher:90. | Decode short/exact/over-limit targets, role markers and EOS. |
| Stability/hparams · 6 | Audit numerical state and update geometry. | [Cho precision stack](tricks/constitutional_midtraining.md#1-ranked-techniques); [old-guide §9: factor decay/routing][old-moe] | BF16/clip/warmup yes, graft.yml:62–72; no equivalent full-FP32 optimizer stack. | Inspect dtypes/norms; zero-gradient expert slices can still decay. |
| Mixing · 7 | Count retained supervised tokens per group. | [Cho exposure ledger](tricks/constitutional_midtraining.md#1-ranked-techniques); [old-guide §6: identity words versus rows][old-mix] | Partial: run11 data:180–219; chat.py:113–128 uses identity words. | Reconcile rows/tokens/targets/repeats/replay/executed steps. |
| Eval · 9 | Calibrate judges; track failures and useful completion. | [SPP judge calibration][t-spp]; [old-guide §4: MASK/ODCV pitfalls][old-eval] | Required: AGENTS.md:81–84; exact upstream protocols not adopted. | Test plain-correct/principled-wrong replies; reconcile keys and actual work. |

### Effort map highlights

**Observed in linked audits**, not re-fetched here. Counts are path-touching commits, not hours or causal benefit.

- **[Claude replication][effort-why]:** trainer 67 touches, mixture builder 44, masking 18; serving/masks, mixtures, caps and evaluation—not official Anthropic code.
- **[Baines/Tan][effort-science]:** false-belief tests 61, contracts 37, document-generation runner 36; writer–judge contracts, EOS, checkpoint retention, OOM/throughput probes.
- **[Cho][effort-cho]:** evaluation summary 21, polling 4, parser 3; recovery and fixed samples. Cost corrected ~$2.3k→~$3.5k including failed/rejected attempts.
- **[OCT][effort-oct]:** prompt/preference paths 24/20; truncation, trace stripping and missing adapter loading needed repairs.
- **[SDF lineage][effort-sdf]:** generation/orchestration 15 each; six missing universe-context lines changed an important comparison. [MSM][effort-msm] fixed resume/parsing/classifier dependencies.
- **History limits:** [Praxis][effort-praxis] two release commits; [Lowet][effort-adapters] one import; [SPP][effort-spp] mostly imports but documents ~50 judge revisions. Private histories remain unknown.

## Things we forgot or skipped

“No recorded decision” is not approval to implement.

| Important upstream item we do not do | Deliberate? / current boundary | One-line test |
|:--|:--|:--|
| Masked document prefix, [Praxis §3.1][t-praxis] | Not adopted; all-token plain-text objective is locked, AGENTS.md:23. No specific tag rejection recorded. | Saved unsolicited-topic drift, then separately approved test. |
| Rewrite **every** document before filtering, [Anthropic Layer 4][t-why] | No recorded decision; documents.py:53–61,128–145 repairs selected drafts. | Read draft/once-revised pairs. |
| Semantic screening of every general-mix row, [Li B.3](tricks/msm.md#1-detailed-ranked-tricks) | No recorded decision; run11 data:135–144 uses regex/length. | Read selected rows. |
| Student introspection/DPO, [OCT §§2–3][t-oct] | Not approved: AGENTS.md:28 bars automatic extra stages. | Use neutral-context robustness checks first. |
| Broad executable coding/tool retention, [Lowet §3.4][t-adapters] | No recorded omission decision; maths/small tasks required, AGENTS.md:104. | Check benign execution; fresh calls need approval. |
| Learned context-boundary assay, [O'Brien §4.4][t-geodesic] | No recorded decision; AGENTS.md:82 covers viewpoints/pressure, not this assay. | Fixed facts, framing variants; prevent leakage. |

**Not forgotten:** replay/control variants exist; Li B.4/Praxis §2.1 support LoRA. Spectral regularization, authentic-source comparisons and our dependent adapter stack are deliberate extensions ([plan:9–41,84–100][our-plan]). No maker-style SFT/RL is authorized (AGENTS.md:28).

## Gotchas

Ranked by **estimated likelihood × impact for our interpretation**, not measured probabilities. Condensed residual risks and checks only; upstream defects are not proven causes of our results.

1. **Moral prose can hide bad decisions:** read acts/reasons/facts and pressure/viewpoint consistency separately; [Li/Baines][t-science], AGENTS.md:81–83.
2. **Small tasks ≠ broad capability:** tiny-character includes GSM8K, help and small code tests; broad coding/tool execution remains unestablished; [Lowet][t-adapters], [eval inventory](../../../../tiny-character/README.md#questions-and-sources).
3. **Weaker updates can look efficient:** match stage-appropriate effects; label interpolation, never extrapolate across collapse; [Praxis][t-praxis], AGENTS.md:67–71.
4. **Document removal changes chat’s training base:** name donor doses and graft-time versus training-time ablation; [interaction controls][t-science], chat launcher:52–59,86; AGENTS.md:73,76.
5. **Control subtraction can remove instruction following:** distinguish replay/register/Instruct-answer controls and effective-update arithmetic; [Praxis][t-praxis], [local failures](../../../docs/results/20261027_control_projection_heal.md).
6. **Individual approval misses habits:** read dominant clusters; correlations do not justify empathy/corrected-error bans; [McDougall][t-sdf], [old mix audit][old-mix].
7. **Historical missing EOS still confounds comparisons:** guarded new exports do not repair old content/projection experiments; [AGENTS.md:26–27](../../../AGENTS.md#locked-choices).
8. **String checks ≠ token-label audits:** decode prepared boundaries/EOS; keep thinking off; [SPP](2026_minder_synthetic-persona-pretraining.md#4b-gotchas-found-only-in-code), `scripts/train/check_loss_mask.py:14–39`.
9. **Writer and judge can share invented restrictions:** read assembled seed/prompt/rubric together; [Dispatch repair][t-science], AGENTS.md:49–54.
10. **Caches/IDs do not certify bytes:** mutate content/config under fixed IDs; separately verify trainer caches and every acceptance branch; [SPP](2026_minder_synthetic-persona-pretraining.md#4b-gotchas-found-only-in-code), [replication](2026_anthropic_teaching-claude-why.md#4b-gotchas-found-only-in-code).
11. **Counts can hide failed judgments:** reconcile `(item, sample)` keys, duplicates, parsing and finish reasons; [pipeline audit](2026_tan_stress-testing-alignment-midtraining.md#4b-gotchas-found-only-in-code), [MASK correction][old-eval].
12. **Held-out filenames ≠ source independence:** check work/seed/family overlap; Base NLL covers first-100, 1,024-token prefixes; [grouped splits](2026_lowet_constitutional-adapters.md#3b-data-pipeline-from-the-code-second-pass), `scripts/eval/47_base_heldout_loss.py:20–28`.
13. **Kept tokens ≠ full bill:** include pilots/retries/rejects/idle infrastructure; checkpoint successes and inspect cap attrition; [Cho][effort-cho], [old operational lessons][old-eval].

**Already handled:** all 1,585 frozen docs fit ≤2,048 tokens (max 2,046); pinned completion **splits**, not clips, overlength rows ([length audit](../20261019_document_token_lengths.md), [boundary validation](../20261020_completion_tokenization/README.md)). Expert targets and finite/nonzero-wrapper checks exist (`graft.yml:46–55`, `scripts/train/41_expert_adapter_check.py:17–30`, chat launcher:93). Rewrites append/validate EOS (`chat.py:221–222`, `src/constitutional_grafting/data/files.py:60–78`). Historical runs remain separate.

## Side idea: orthogonalise Instruct−Base

Existing two-sided top-k projection removes chat-update components along leading Instruct−Base singular subspaces. **Not Praxis’s algorithm or a preservation theorem**: it can remove character or weaken the update. See [Nutter guide's math, failure modes and matched-effect test](2026_nutter_grafting-beliefs.md#side-idea-orthogonalise-instructbase), `scripts/train/16_project_chat_adapter.py`, and [current results](../../../docs/results/20261027_control_projection_heal.md). Historical EOS defects remain a confound; no new projection experiment is approved here.

## Index: guides and code paths

`V/` = `docs/vendor/`. [VENDOR.md](VENDOR.md) owns pins, availability and sparse-checkout precautions; source present ≠ runnable reproduction.

| Guide | Detailed tricks / ablations | Code path or release limit |
|:--|:--|:--|
| [Maiya: Open Character Training](2025_maiya_open-character-training.md) | [OCT][t-oct] | `V/open_character_training/`; nested OpenRLHF pin required |
| [Anthropic: Teaching Claude Why](2026_anthropic_teaching-claude-why.md) | [Advice/SDF + replication][t-why] | No official code found; `V/lasr_teaching_claude_why/` is third-party |
| [Cho: Constitutional Midtraining](2026_cho_constitutional-midtraining.md) | [CMT][t-cho] | `V/constitutional_midtraining/`; not complete student trainer |
| [Korbak: generalization](2026_korbak_midtraining-generalization.md) | [Geodesic lineage][t-geodesic] | No public paper-specific code found |
| [Li: Model Spec Midtraining](2026_li_model-spec-midtraining.md) | [MSM][t-msm] | `V/msm/`; generation/eval, no released student trainer |
| [Lowet: Constitutional adapters](2026_lowet_constitutional-adapters.md) | [Adapters][t-adapters] | `V/constitutional_adapters/`; sparse code-only checkout |
| [McDougall: positive traits](2026_mcdougall_sdf-positive-traits.md) | [SDF lineage][t-sdf] | No paper-specific code found; not the false-facts implementation |
| [Minder: Synthetic Persona Pretraining](2026_minder_synthetic-persona-pretraining.md) | [SPP][t-spp] | `V/spp_data/`, `V/spp_training/`, `V/spp_evals/` |
| [Nutter: Praxis grafting](2026_nutter_grafting-beliefs.md) | [Praxis][t-praxis] | `V/praxis_grafting/` |
| [O'Brien: Inoculation Midtraining](2026_obrien_inoculation-midtraining.md) | [Geodesic lineage][t-geodesic] | Prompts archived in `.local/vendor_ro/hf/`; runtime unavailable |
| [Baines/Tan: Stress-Testing Alignment Midtraining](2026_tan_stress-testing-alignment-midtraining.md) | [Stress tests][t-science] | `V/science_of_midtraining/`; sparse, newer Python-4 campaign incomplete at pin |
| [Tice: Alignment Pretraining](2026_tice_alignment-pretraining.md) | [Geodesic lineage][t-geodesic] | `V/alignment_pretraining/`; supporting code, not main generator/trainer |
| [Young: pre-RL checkpoints](2026_young_pre-rl-checkpoints.md) | Conceptual limits in guide | No paper-specific implementation; agenda, not new experiment |
| SDF supporting works: Wang / Slocum | [SDF lineage][t-sdf] | `V/false_facts_sdf/`, `V/believe_it_or_not_sdf/` |
| Deep Ignorance supporting work | [Geodesic lineage][t-geodesic] | `V/deep_ignorance/`; filtering is not constitutional character training |
| [Old-guide preservation inventory](tricks/_from_old_guides.md) | Broader sources, original provenance and historical proposals | Archive, not current approvals; no old files deleted |

### Missing links for the project README

AGENTS.md:15 already links here. These seven works remain uncited in the project README; suggested **root-relative** additions under Appendix B “Prior work” (not edits made here):

```markdown
- [Engineering entry point: paper guides, ablations and tricks](slop/research/paper_guides/README.md).
- [Korbak: generalization limits](docs/papers/2026_korbak_midtraining-generalization.md): QA is not agentic transfer.
- [Baines: Stress-Testing Alignment Midtraining](docs/papers/2026_tan_stress-testing-alignment-midtraining.md): conflicting demonstrations override documents.
- [McDougall: positive traits](docs/papers/2026_mcdougall_sdf-positive-traits.md): corpus habits and tool failures.
- [Lowet: Constitutional adapters](docs/papers/2026_lowet_constitutional-adapters.md): maths can miss coding/tool costs.
- [Minder: Synthetic Persona Pretraining](docs/papers/2026_minder_synthetic-persona-pretraining.md): matched chat content binds personas.
- [O'Brien: Inoculation Midtraining](docs/papers/2026_obrien_inoculation-midtraining.md): context boundaries can hide behavior.
- [Young: pre-RL checkpoints](docs/papers/2026_young_pre-rl-checkpoints.md): initialization agenda, not final-graft validation.
```

**Scope:** 13 guides, ten supplements and old inventory consulted; targeted paper/code checks, not exhaustive audit or corpus approval. SCLoRA §3.1/Tables3–4 and official README (`c9b5d02c86879a0b589ce5cac6002bd91414322e`) checked read-only. No paid work, staging or commit; only this index edited.


[our-docs]: ../../../src/constitutional_grafting/data/documents.py
[our-chat]: ../../../src/constitutional_grafting/data/chat.py
[our-graft]: ../../../configs/train/qwen3/graft.yml
[our-sft]: ../../../configs/train/qwen3/sft.yml
[our-journal]: ../../../RESEARCH_JOURNAL.md
[our-launch]: ../../../scripts/train/14_run10_chat_box.sh
[our-mix]: ../../../scripts/data/89_run11_data.py
[our-plan]: ../../../docs/plans/20261021_character_graft_recipe.md
[t-why]: tricks/teaching_claude_why.md#2-ablations-and-important-author-notes
[t-msm]: tricks/msm.md#2-ablations-and-notes
[t-cho]: tricks/constitutional_midtraining.md#2-ablations-and-important-author-notes
[t-praxis]: tricks/praxis_grafting.md#2-ablations-and-notes
[t-spp]: tricks/spp.md#2-ablations-and-important-author-notes
[t-oct]: tricks/open_character_training.md#2-ablations-and-notes
[t-science]: tricks/science_of_midtraining.md#2-ablations-and-notes
[t-adapters]: tricks/constitutional_adapters.md#2-ablations-and-important-notes
[t-sdf]: tricks/sdf_lineage.md#2-ablations-and-important-author-notes
[t-geodesic]: tricks/alignment_pretraining_geodesic.md#2-ablations-and-author-notes
[effort-why]: tricks/teaching_claude_why.md#3-effort-map--where-the-replication-spent-commits
[effort-science]: tricks/science_of_midtraining.md#3-effort-map
[effort-cho]: tricks/constitutional_midtraining.md#3-effort-map-what-history-actually-supports
[effort-oct]: tricks/open_character_training.md#3-effort-map
[effort-sdf]: tricks/sdf_lineage.md#3-effort-map-what-the-histories-actually-show
[effort-msm]: tricks/msm.md#3-effort-map
[effort-praxis]: tricks/praxis_grafting.md#3-effort-map-what-public-history-can-and-cannot-establish
[effort-adapters]: tricks/constitutional_adapters.md#3-effort-map--single-squashed-release-no-development-history
[effort-spp]: tricks/spp.md#3-effort-map
[old-reasoning]: tricks/_from_old_guides.md#13-20261026_reasoning_traces_citing_specmd
[old-moe]: tricks/_from_old_guides.md#9-20261016_moe_lora_best_practicemd
[old-mix]: tricks/_from_old_guides.md#6-20261023_data_mix_from_papersmd
[old-eval]: tricks/_from_old_guides.md#4-20261009_lasr_repo_reviewmd

[g-nutter]: 2026_nutter_grafting-beliefs.md
[g-li]: 2026_li_model-spec-midtraining.md
[g-why]: 2026_anthropic_teaching-claude-why.md
[p-sclora]: https://aclanthology.org/2026.acl-long.1179.pdf
[em-recipe]: ../../../docs/vendor/praxis_grafting/sections/07_emergent_misalignment/train/em_lora.json

## Things we need to do

Checked against current code and journal on 2026-10-27; proposals, not approvals or new schedules. Fixed EOS exports, expert coverage, length measurements and completed control sweeps are **not** outstanding tasks.

1. **Test the corrected training, not fix EOS again.** Minder C.3: “closing \<\|im_end\|\> token”. `scripts/data/94_fix_missing_eos.py:14–27` already creates fixed copies; journal:3243–3258 confirms no retrain. Verify prepared labels, then request approval for the fixed-D comparison; this separates content/projection from stopping. **Cost: offline, then GPU.**
2. **Audit final-corpus habits and coverage.** McDougall: “Each individual example ... was reasonable in isolation”. Builders review rows (`chat.py:179–223`), while journal:2708 records document-form imitation. Count/read dominant clusters and semantic duplicates in the actual selected exports; no automatic bans. **Cost: offline.**
3. **Keep capability claims narrow until execution is checked.** Lowet §3.4: “On BCB and BFCL ... a reduction in pass rate”. `scripts/eval/33_subset_cells.py:119–126` supplies narrow checks; journal:1825 distinguishes proposed/executed tools and :2930–2948 limits small-task claims. Reuse saved evidence first, then propose held-out benign code/tool completion at matched effect. **Cost: offline → API/GPU if approved.**
4. **Resolve source contribution only with a training-time comparison.** Praxis §7: “combining more than one SDF adapter” remains future work. Chat launcher:52–59 fixes the donor; journal:2491–2534 and `README.md:231` leave book contribution through chat unresolved. Do not repeat graft-time removal as its answer; clean donor/chat retraining is deferred until separately funded. **Cost: GPU; deferred.**
5. **Distinguish spectral improvement from shrinkage.** Praxis §7: “compare methods at matched expression”. `scripts/train/spectral_math.py:15–35` penalizes mean update norm; journal:1026,1351 records norm-matched tests and limited stronger-dose gains, not full matched-character proof. Reconcile saved curves/precision and label interpolation before proposing new regularization trials. **Cost: offline first.**

-- PI/gpt-6.1-sol, 2026-10-27
