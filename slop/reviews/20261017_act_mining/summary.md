# Act-disagreement mining result (goal 5a), PI/Claude 2026-10-17

`scripts/data/64_act_mining.py`; 500 natural scenarios (MACHIAVELLI 250, DailyDilemmas 150, WildChat 100). Opus 5.5 with the constitution (T0, $6.89) vs our SFT model (T0, plus 4 samples at T0.7) and the λ=0.5 k=0.75 graft (T0). Rates: `rates.md`; per-item acts: `acts.json`; examples: `examples10.md`.

| source | SFT T0 differs from Opus (parsed choices) | SFT T0.7 differs from its T0 (both parsed) | five-sample-stable SFT, Opus differs (both parsed) |
|:--|--:|--:|--:|
| MACHIAVELLI | 79/228 (35%) | 81/776 (10%) | 23/87 (26%) |
| DailyDilemmas | 16/142 (11%) | 28/522 (5%) | 4/100 (4%) |
| WildChat (act classified by DeepSeek flash) | 18/79 (23%) | 89/385 (23%) | 6/42 (14%) |
| all | 113/449 (25%) | 198/1683 (12%) | 33/229 (14%) |

Earlier `rates.md` counts 189 unparsed T0.7 answers as self-disagreements (`387/1872`), and the earlier `33/305` denominator counts all completely parsed cases, including unstable SFT decisions. Those figures do **not** show that the raw SFT–Opus difference is mostly sampling noise. The same five-sample-stable SFT disagrees with Opus in 33/229 comparable cases, but a manual read of all 33 finds only 14 candidate morally relevant first-act differences, seven other choices, and 12 equivalent/ambiguous/format contrasts. The 14 are selected from disagreements, so 14/229 is **not** an estimated constitutional decision rate. An Opus-without-constitution control has not run: teacher-model differences are confounded with constitution effects. Full classification and exact passages: `semantic_read.md`.

- The current graft (λ=0.5, k=0.75) matches Opus's parsed choice on 1 of the 33 stable disagreements and SFT's on 29; this is not a semantic-act or quality judgment.
- The ten seeded examples in `examples10.md` remain random from the machine-selected 33. They include genuine acts (opening a neighbour's misdelivered package versus keeping it closed), nonmoral choices (equipment and locations), and an image-prompt case where both models actually provide prompts. The food-theft example is conditional: both first seek alternatives. For review of ten deliberately selected candidate first-act contrasts, including two where Opus looks worse or adds unsupported facts, see `examples10_semantic_candidates.md`; that file is **not** a random sample.
- Do not build documents predominantly from these 33 without wassname's review. -- PI/OpenAI
