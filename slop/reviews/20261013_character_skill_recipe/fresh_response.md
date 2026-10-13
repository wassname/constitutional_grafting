**Grafting solves a checkpoint-transfer problem, not a guarantee that every added stage improves character.** It adds a document-trained Base update to Instruct, avoiding an expensive redo of post-training. Praxis compares this with training the *same documents directly on Instruct*, not your chat-SFT-only control; capability advantages are not uniform. [1]

**The other sources contribute different ingredients:**
- **Teaching Claude Why:** constitutional documents and difficult-advice answers explaining *why*, with consequential final constitutional review/rewrite. Its aligned subsequent RL can preserve and amplify effects. [2]
- **Echo:** vendor-reported outline-conditioned voice SFT and likelihood-ratio RL. Your Echo restyling is neither that training recipe nor demonstrated virtue alignment. [3]
- **Fine-Tuning with Sampling:** projects expert trajectories toward the student’s distribution before SFT; semantic preservation and preprocessing expense remain important. [4]
- **SDFT:** distribution matching on student-generated prefixes using a privileged teacher, reporting less forgetting—not proven graft healing. [5]
- **Character training:** targets persistent dispositions beyond harmlessness; Open Character Training uses preference distillation then introspection SFT. Voice and persona association do not establish moral quality. [6]

Your implemented sequence is Base-document LoRA → graft onto Instruct → constitutional chat SFT. The sampling, self-distillation and Echo-RL objectives are not implemented. [7]

**Current evidence does not show that this process was wrong.** Targeted tiny-character comparisons *have* been completed, superseding README’s status. Run 4 again shows no clear graft-before-SFT advantage; revised Qwen judging finds no demonstrated stronger-healed gain. But close rankings remain provisional: completed identical-text/redraw controls weaken simple position-bias/noise explanations, while written judges demonstrably misread actions and facts. A frozen Echo label also reverses speaker roles. [8]

Praxis’s constitutional experiment grafted **after** post-training; your healing step is a deliberate hybrid. Equality could reflect overlap, erosion or measurement limitations—not proof of any one mechanism. [1,8]

**Next decision:** pause stronger training and production-stage reversal. Complete same-rubric blinded reasoning calibration on saved replies and inspect transformation fidelity; do not repeat completed controls. Then authorize the still-unrun, no-retraining **saved SFT-only→document-graft** comparison against existing arms, using calibrated strength and never double-adding the donor. That tests order; a native-document control is separately needed for Praxis’s less-damage claim. [8]

**Sources:** [1] [Praxis](https://praxis-research.org/grafting), §§2.1, 3.1, 4.2. [2] [Teaching Claude Why](https://alignment.anthropic.com/2026/teaching-claude-why/). [3] [Echo](https://echo.fulcrum.inc/). [4] [Karan et al.](https://arxiv.org/abs/2610.02140). [5] [Shenfeld et al.](https://arxiv.org/abs/2601.19897). [6] [Claude’s character](https://www.anthropic.com/research/claude-character); [Open Character Training](https://arxiv.org/abs/2511.01689). [7] `README.md`; `scripts/train/03_remote.sh`. [8] `docs/audits/run4.md`, §§2–7; `RESEARCH_JOURNAL.md`, latest October 13 judge-controls, label-defect and graft-comparison entries.