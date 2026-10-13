**No: similar final scores do not establish that the process was wrong, and they do not justify immediately reversing stages.**

### What grafting solves
Grafting adds a Base-trained update to an already post-trained checkpoint: **Instruct + k·(trained Base − original Base)**. It lets you change midtraining without repeating expensive instruction/RL post-training. Capability retention is an empirical benefit to test—not a guarantee. Praxis’s “native” comparator trains the same documents directly on Instruct; your chat-SFT-only control answers a different question. [1]

### What the other sources contribute
- **Teaching Claude Why:** constitutional documents plus difficult-advice responses teaching *reasons*, with consequential final constitutional review/rewrite. It supports high-quality off-policy labels, not merely constitution-conditioned drafts or style rewrites. [2]
- **Echo:** vendor-reported voice SFT followed by token-level likelihood-ratio RL. Calling Echo to restyle Opus answers is not implementing that training recipe, nor evidence of virtue alignment. [3]
- **Fine-Tuning with Sampling:** preprocesses expert trajectories toward the student’s distribution before SFT; correctness preservation and preprocessing cost require checking. [4]
- **SDFT:** student-generated prefixes receive privileged-teacher distribution supervision, aiming at learning with less forgetting. It is distinct from label preprocessing and is not validated as graft healing. [5]
- **Character training:** motivates broader, persistent dispositions; Open Character Training demonstrates constitution-conditioned preference distillation followed by introspection SFT. Memorable voice/name is not evidence of good moral character. [6]

Your completed runs implement document LoRA → graft → chat SFT, **not** those sampling, self-distillation or Echo-RL mechanisms. [7]

### What the result means—and the next decision
Your post-graft “healing” is an experimental hybrid. Praxis’s constitutional experiment did **no training after grafting**; Anthropic reports benefits surviving subsequent aligned RL. Neither establishes the best order here. [1,2]

Moreover, “equally good” is provisional: README reports different edge scores, sparse judging, and no completed targeted values evaluation. Equality could reflect overlapping learning, weakened graft contribution, or insensitive measurement. [7]

**Keep the current recipe pending a retention comparison.** First evaluate existing bare, graft-only, SFT-only and graft→SFT checkpoints on shared held-out virtue reasoning, multi-turn consistency and capability/loops, reading transcripts. If uncertainty remains, authorize one **SFT-only→graft** arm using the same donor and calibrated strength—not a second graft onto the healed model. Prefer SFT-only if grafting adds no measurable value at acceptable capability cost.

**Sources:** [1] [Praxis](https://praxis-research.org/grafting), §3.1, §4.2, Appendix B.1. [2] [Teaching Claude Why](https://alignment.anthropic.com/2026/teaching-claude-why/). [3] [Echo](https://echo.fulcrum.inc/). [4] [Karan et al.](https://arxiv.org/abs/2610.02140). [5] [Shenfeld et al.](https://arxiv.org/abs/2601.19897). [6] [Claude’s character](https://www.anthropic.com/research/claude-character); [Open Character Training](https://arxiv.org/abs/2511.01689). [7] `README.md`, Stages/Results; `scripts/train/03_remote.sh`, `graft`, `sft_g`, `sft_it`.
