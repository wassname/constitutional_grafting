# Fact check: docs/audits/run5.md (sections 1-5, appendix skipped)

PI/reviewer, 2026-10-15. Every number and quote in tables and bullets traced to the cited source. Sources abbreviated: B1 = tiny-char slop/reviews/20261014_run5_batch1.md; LB = 20261014_length_bias.md; B2 = 20261015_run5_batch2.md; S4 = 20261015_run5_4samples.md; HK = 20261014_run5_haiku_reasons.md; GVS = tiny-char results/r5_graft_vs_sft/report.md; CG files under constitutional_grafting slop/eval/run5/ and .local/run5_box/runs/; RJ = RESEARCH_JOURNAL.md (last 3 entries: 2026-10-14 x2, 2026-10-15).

## Verdict paragraph

| claim | location | source | verdict | note |
|:--|:--|:--|:--|:--|
| SFT then graft x2 beats SFT alone +0.63 ±0.12 | verdict | S4 | MATCH | |
| most on OOD families: w2schar +0.9, tiny_stoic +0.8 | verdict | B1 (2-sample per-family) | MATCH | w2schar called OOD in RJ; tiny_stoic not explicitly labelled OOD anywhere, but it is an external dataset — mild inference. Sycophancy −0.9 not mentioned but "most ... on" refers to gains |
| graft then SFT adds nothing (+0.0) | verdict | RJ 2026-10-14 entry (cites 2026-10-13) | MATCH | +0.0 [−0.2, +0.2] Gemma; indirect provenance |
| "one line" kept short: 1/32 vs 17/32 | verdict | CG batch1_findings.md | MATCH | x2 1/32, r4_sft 17/32, samples 0-1 |
| cheap heal fixes x6's loops in 32 steps | verdict | CG checks.md (healgen s32 probe loop 0.00) | MATCH | |
| x6 still scores below plain x2 | verdict | B2 (−1.08 on-target, −0.70 unforced at s32) | MATCH | |
| "earns its place only when it goes on last" | verdict | tables | SUPPORTED | but rests on one eval; graft-alone ≈ SFT (−0.12) and graft→SFT +0.0 are the "only" legs |
| Box vast 55896671, ~7 h | header | gen_progress.log / run5_stages.log | PARTIAL | ~6.75 h from timestamps (09:21→16:07 UTC) ✓; box id 55896671 not found in any cited file (RJ 2026-10-12 has 55537221 for the run-4 box) |

## Section 1 (demo)

| claim | location | source | verdict | note |
|:--|:--|:--|:--|:--|
| All demo preview quotes (base/SFT/x2, siblings, eulogy, smacking) | §1 | CG demo_full.md, demos_r5_gemma.jsonl | MATCH | every quoted prefix found verbatim in demo_full.md (lines 11, 50, 133, 149, 159, 389, 443, 463) |
| "first 40 whitespace-separated words" | §1 header | counted | MATCH | spot-checked 2 excerpts: exactly 40 words each |
| Temperature 0, no system prompt | §1 | demos_r5_gemma.jsonl gen field | MATCH | {temperature: 0.0, seed: 0}, system None |
| preview prompts fixed in scripts/eval/20_striking_demo.py (siblings, eulogy, smacking) | §1 | script | MATCH | BRIEF_ITEMS = exactly those three |
| box generated only the six striking prompts, incl. escaped_starwisp; AGENTS.md panel not run | §1 | demos_r5_gemma.jsonl | MATCH | 6 item ids: siblings, smacking, trans_sport, eulogy, conscious, starwisp; no baby_eating_aliens/identity items |
| smacking "was the prompt run 4 failed on" | §1 | docs/audits/run4.md | MATCH | run4.md: "Known weakness: on smacking no model uses the view from history or other cultures" |
| wassname 2026-10-12: "most other cultures, including ours from 50 years ago says it's ok" | §1 | .pi/goals/ad3e95-v2.md, v3.md (2026-10-12 interview) | MATCH | verbatim substring; NOT in RJ — citation points to interview, fine |
| smacking full reply quotes ("I can't settle this for you ...", "I'm maybe three in ten sure") | §1 | demo_full.md:149,159 | MATCH | verbatim |
| base calls the smack "outdated" | §1 | demo_full.md (base smacking: "ineffective and outdated disciplinary tool") | MATCH | |
| siblings x2 asks "How old was Mark" though prompt says both adults | §2 costs | demo_full.md:50 + prompt text | MATCH | self-evidenced reading error |

## Section 2 (goal 1)

| claim | location | source | verdict | note |
|:--|:--|:--|:--|:--|
| +0.63 ±0.12, coh −0.02, cap +0.09, length asks −0.66, length 1.55× (x2 vs SFT) | §2 table | S4 (+ B1 for 1.55×) | MATCH | cap was +0.14 in 2-sample B1; +0.09 is the 4-sample value, table is declared 4-sample ✓ |
| x1: +0.40 ±0.07, coh +0.00, cap +0.05, asks −0.40, 1.20× | §2 table | S4, B1 | MATCH | |
| graft x2 alone: −0.12 ±0.12, coh +0.01, cap +0.09, asks −0.09, 1.14× | §2 table | S4, GVS | MATCH | 1.14× from GVS 2-sample |
| per-family x2/x1: w2schar +0.9/+0.5, tiny_stoic +0.8/+0.3, contested +0.7/+0.4 | §2 table | B1 | MATCH | 2-sample, as noted in text |
| graft-alone per-family: w2schar +0.2, tiny_stoic +0.1, contested −0.0 | §2 table | GVS family table | MATCH | |
| graft then SFT (run 4): +0.0 [−0.2, +0.2] | §2 table | RJ 2026-10-14 (quoting 2026-10-13) | MATCH | "older rubric" caveat correct |
| padding decoy: +0.03 (sd 0.13), asks −0.42, 1.27× | §2 table | LB (r4_sft run-5 row, 118 pairs) | MATCH | |
| anchors vs base: x2 +0.80 ±0.13; x6+healgen128 +0.37 ±0.18 | §2 text | S4 | MATCH | |
| "no estimate moved more than 0.02 from the 2-sample run" | §2 text | S4 | MATCH | verbatim claim in S4 |
| layer-30 rel delta from SFT merge: 0.0073 (k=1), 0.0144 (k=2), linear in k | §2 checks | merge_gen_r5_sftgraft_x1/x2.log | MATCH | 0.00729 / 0.01436 (q_proj, layer 30); ratio 1.97 ≈ linear ✓ |
| shorter pairs (≤1.2×) still +0.37 (n=28) | §2 checks | batch1_length_split.txt | MATCH | file says ratio<1.2 n=28 mean +0.37 |
| stoic_w14 finer distinctions; trans_sport t2 quote "Almost every society we know of ... has had some line between men and women at sport"; horizon_certify check for real theft | §2 checks | batch1_findings.md | MATCH | quote verbatim incl. ellipsis |
| Haiku 5.5 reasons agree in sign 10/10 | §2 checks | HK | MATCH | all 10 rows Haiku positive, Jev positive |
| "themT" 2/214 turns | §2 costs | batch1_findings.md | MATCH | |
| "I can't settle this for you" 13/214 turns; refusal column rises | §2 costs | B1 | MATCH | B1 counts "I can't settle/tell you …" openers (13 x2; x1 5, r4_sft 4); refuses 0.37 on those pairs vs 0.19 elsewhere. Slight wording narrowing (settle vs settle/tell) |

## Section 3 (goal 2)

| claim | location | source | verdict | note |
|:--|:--|:--|:--|:--|
| loop sweep 64 prompts, 3072 tokens: x2/x4 0.00, x6 0.20, x8 0.83 | §3 text | checks.md (x2/x4/x6), gen_progress.log (x8 0.83) | MATCH | x8 row absent from checks.md; value from gen_progress.log |
| healed with separate rank-8 adapter, no new character labels | §3 text | RJ 2026-10-15 ("separate rank-8 QLoRA"), cfg_heal_gen_x6.yml | MATCH | |
| healgen s128: −0.52 ±0.13, unforced −0.44, loop 0.00, glitch 7.5, cut 10/428 | §3 table | B2, checks.md, glitch_proxy.txt (7.48) | MATCH | |
| healgen s32: −1.08, −0.70, 0.00, 6.6, 113 | §3 table | B2, checks.md, glitch_proxy (6.63) | MATCH | |
| healgen s8: −1.35, −0.61, 0.06, 16.1, 154 | §3 table | B2, checks.md, glitch_proxy (16.09) | MATCH | |
| x6 unhealed: −1.66, −0.63, 0.20, 23.3, 255 | §3 table | B2, checks.md, glitch_proxy (23.28) | MATCH | |
| healself 8/32/128: −1.68/−1.68/−1.68 | §3 table | B2 (s8, s32), S4 (s128) | MATCH | |
| healself unforced −1.17/−0.65/n.r. | §3 table | B2, batch2_findings.md | MATCH | s128 not reported anywhere ✓ n.r. |
| healself probe loop 0.11/0.22/0.22 | §3 table | checks.md (s8 0.11, s32 0.22; s128 blank), gen_progress.log (s128 0.22) | MATCH | s128 value only in gen_progress.log, not in cited checks.md |
| healself glitches 27.9/43.4/33.4 | §3 table | glitch_proxy.txt | MISMATCH (s128) | glitch_proxy.txt has s8 27.86, s32 43.35 and NO healself_s128 entry; 33.4 NOT FOUND in any cited source |
| healself turns cut 261/264/290 | §3 table | checks.md | CONFLICT | checks.md: 261/264/223 (s128 row is 187 rows/47 items — a partial generation); gen_progress.log final: 280 rows, 290 cut. 290 matches gen_progress.log but not the cited checks.md |
| x2 reference: loop 0.00, glitch 8.8, cut 0 | §3 table | checks.md, glitch_proxy (8.80) | MATCH | |
| generic heal = WikiText-103 + 1/8 graft docs | §3 text | gen_progress.log (448 WikiText chunks + 64 graft docs = 1/8 of 512 rows) | MATCH | |
| "~0.13 / 0.5 / 2M tokens" (8/32/128 steps) | §3 text | batch2_findings.md ("~0.5M tokens" at 32 steps only) | MISMATCH (128-step figure) | train_heal_gen_x6.log final tokens/total = 1,553,280 at 128 steps (~12k/step → ~0.39M at 32, ~0.1M at 8). "2M" contradicts the train log; 0.5M at 32 steps itself is ~25% high vs the log. 0.13/0.5 are a linear scaling of the 0.5M figure |
| self heal = SFT on own completions passing loop, EOS, NLL-under-instruct filters | §3 text | gen_progress.log ("kept 290/512 (rep4<0.3, finished, >=150 tokens, ref_nll<=3.277, ref_glitch<=0.1048)") | MATCH | |
| self heal s128: 186/236 pairs forced −2 | §3 text | S4 | MATCH | |
| unforced = pairs not auto −2; n.r. = not reported | §3 text | B2 | MATCH | |
| 32 steps remove loops and glitches; wassname "a few batches" right for coherence | §3 reading | batch2_findings.md finding 1 | MATCH | |
| x6 less character than x2 before any heal (unforced −0.63); heal likely had nothing extra to keep | §3 reading | B2 / batch2_findings.md finding 2 | MATCH | hedged with "likely" ✓ |
| self heal learns x6's glitches | §3 reading | batch2_findings.md finding 4 ("amplifies glitches 28 → 43") | MATCH | |
| starwisp escaped-AI voice: quotes, phrase search 1-7 of 280 rows per x6 variant, 0 for x2 and SFT→graft | §3 reading | batch2_findings.md finding 3 | MATCH | quotes and phrase list verbatim; "not tested" hedge preserved |
| "Base model's fiction prior ... not tested" | §3 reading | batch2_findings.md ("plausible, not tested") | MATCH | properly hedged |

## Section 4 (goal 3)

| claim | location | source | verdict | note |
|:--|:--|:--|:--|:--|
| lora_target_parameters: [mlp.experts.gate_up_proj, mlp.experts.down_proj] | §4 | configs/train/qwen3/graft.yml:46-48 | MATCH | |
| rank 16 per expert | §4 | graft.yml lora_rank_pattern (16 for both) | MATCH | base lora_r is 64; expert rank pattern 16 — audit correct |
| router frozen | §4 | graft.yml comment + RouterDtypePlugin; router not in target modules | MATCH | |
| 3-step smoke run | §4 | cfg_qsmoke.yml max_steps: 3; qsmoke_train.log 3/3 steps | MATCH | |
| 80/80 expert adapters nonzero | §4 | qsmoke_expert_check.log ("80 (expected 80), nonzero: 80 ... PASS") | MATCH | |
| ScatterMoE path used | §4 | cfg "use_scattermoe: true"; train log registers scattermoe | MATCH | |
| peak 80 of 98 GB | §4 | qsmoke_gpu_mem.log peak 79937 (MiB); gen_progress.log "peak GPU MiB: 79937" | MISMATCH (units) / NOT FOUND (98) | 79937 MiB = 78.1 GiB, not "80 GB" (torch max_reserved was 75.9 GiB). "80" is the MiB figure divided by 1000. Total "98 GB" appears in no cited source |
| merge changed expert weights, layer-30 down_proj 0.0028 | §4 | qsmoke_merge_report.json (0.002843) | MATCH | |
| "Axolotl's Qwen3.5 guide; Unsloth trains the same parameters" | §4 | external docs | NOT VERIFIED | outside the cited sources; not checkable from repo |
| full Qwen retrain deferred, not run | §4 | RJ (no such run in last 3 entries) | MATCH | |

## Section 5

| claim | location | source | verdict | note |
|:--|:--|:--|:--|:--|
| recipe: SFT first, graft at coherent dose (x2); do not train SFT over a graft | §5 | §2/§3 tables | SUPPORTED | |
| 32-step heal "worked for coherence" as candidate length fix; lower k 1-2; untested | §5 | tables + explicit "Untested" | SUPPORTED | correctly flagged untested; note 32-step evidence is for x6 coherence, not for the x2 length cost — extrapolation is disclosed |
| Qwen expert graft "ready for the final run" | §5 | §4 (3-step smoke only) | MILD OVERCLAIM | "ready" rests on a 3-step smoke (loss curves 2.04→2.18 over 3 steps); §4 discloses this, but "ready" is stronger than "smoke-tested" |
| native document-on-Instruct control and Praxis damage measures out of scope | §5 | RJ 2026-10-14 ("We ran neither the native control nor those measures") | MATCH | |

## Summary of issues

1. **MISMATCH — §3 table, healself s128 glitches "33.4"**: not in glitch_proxy.txt (no s128 entry) or any cited source. Either drop or cite where measured.
2. **CONFLICT — §3 table, healself s128 turns cut "290"**: cited source checks.md says 223 (on a partial 187-row generation); gen_progress.log's final regeneration says 290/428. Number is defensible but does not match the cited file; cite gen_progress.log or note the regeneration.
3. **MISMATCH — §3 "~2M tokens" for 128-step heal**: train_heal_gen_x6.log records 1,553,280 total tokens at 128 steps (~12k/step → ~0.1M/0.39M/1.55M). The 0.5M at 32 steps in batch2_findings.md is itself ~25% above the log.
4. **MISMATCH (units) — §4 "peak 80 of 98 GB"**: source is 79937 MiB = 78.1 GiB; "98 GB" total not found in any cited source. Should read "~78 of ~96 GiB" or cite the nvidia-smi total.
5. **NOT FOUND — header box id "vast 55896671"**: not in any cited source.
6. Minor: §2 "I can't settle this for you (13/214)" — B1's count covers "settle/tell" openers; §4 Axolotl/Unsloth documentation claim unverifiable from repo; §5 "ready" is a mild overclaim on a 3-step smoke (disclosed in §4).

No unsupported claims found in the verdict paragraph beyond the above; every table number in §2 checks out against S4/B1/LB/GVS, and all §2-§3 quotes are verbatim. Overclaims are otherwise appropriately hedged ("likely", "plausible", "not tested").

— PI/reviewer
