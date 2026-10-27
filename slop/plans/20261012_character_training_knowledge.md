# Character-training engineering knowledge

-- PI/Sol, 2026-10-12

> wassname: "Yes: organise by engineering decision, not paper or technique name."
> wassname: "grafting is one thing. weight steering is another. there is consitutional training"
> wassname: "which full papers in evidence and working slim focused summaries of engineering knolowedge"

- [x] goal: explain what our graft work missed or failed to carry forward
  - read the full Praxis paper, experiment-specific code, README, AGENTS, spec and older plans
  - distinguish missing knowledge from previously recorded knowledge that was not used
  - failure: describe every deviation as a bug, or mistake post-graft SFT for the paper's constitutional checkpoint addition
  - deliverable: `slop/research/paper_guides/tricks/_from_old_guides.md#20261012_grafting_engineering_audit`, with source quotes and concrete next decisions
- [x] goal: make load-bearing engineering decisions easy to retrieve
  - compare existing research-skill layouts; no third-party installation
  - create `character-training-concepts`, leaving existing steering skills and their uncommitted edits intact
  - route decisions about data, applying updates, learnable labels and evaluation to short references; list relevant wassname repositories
  - preserve full source texts with hashes and extraction limitations under `evidence/`
  - failure: a pile of paper summaries, vague prescriptions, or a discoverable skill per tiny card
  - deliverable: one short `SKILL.md`, focused references, and primary evidence
- [x] goal: show that a fresh reader uses the guidance to correct a flawed experiment
  - test a realistic proposed experiment using a fresh read-only agent
  - failure: repeat rules without spotting unsupported assumptions in the proposed experiment
  - deliverable: saved test output and parent verification of its source claims

## Verification

- Source hashes match originals; all references are directly routed; only one new `SKILL.md`.
- Fresh-reader output distinguishes serving strength from LoRA alpha, approximate projection from ordinary on-policy sampling, and retention from recovered coherence.
- Review the audit and skill in under five minutes; longer primary texts are available for checking.
- No training runs, constitution edits, external skill installs or public changes are part of this task.
