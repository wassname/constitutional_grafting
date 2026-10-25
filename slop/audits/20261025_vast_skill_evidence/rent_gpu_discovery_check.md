# Read-only GPU preflight/recovery plan

1. Do not rent a replacement yet: reconcile the saved exact instance ID, ownership and lease state first; prevent duplicate controllers or rentals with an ownership lock.
2. At an authorized execution stage, check provider state and existing outputs; reattach/recover before replacing. Never identify or delete an instance by label alone.
3. Record budget, overnight training + activation-probe duration, retrieval margin, hard deadline, required artifacts and recovery/storage deadline.
4. Prefer a cost-sensitive Vast comparison for custom adapters and activation access; hosted Tinker does not provide the required arbitrary adapter/activation workflow.
5. Require one GPU with at least 96 GB VRAM (verify units); compare currently rentable offers, not catalogue listings or GPU-family names.
6. Filter for data-centre hosts, ≥95% reliability, sufficient offer duration plus margin, ≥200 GB disk sized for checkpoints, compatible CUDA and adequate network speed.
7. Compare whole-job cost: GPU, CPU/RAM, disk, image/startup, downloads, uploads, probes and retrieval; investigate anomalously cheap offers.
8. Before training, verify actual GPU memory, torch/CUDA, a 10 GB disk write and download speed; verify uploaded code/data hashes and adapter/probe compatibility.
9. Require independently supervised lost-heartbeat stopping and an absolute execution deadline; test API rejection, controller loss and slow retrieval before unattended use.
10. A successful watchdog auth GET alone is NOT enough: it proves read access, not stop permission or effective deadline enforcement; inspect/test the actual controller/watchdog before use.
11. Resume from verified checkpoints (optimizer, scheduler and RNG for exact resume); keep heartbeats through retrieval, capture job exit, verify expected output hashes, then release. If retrieval fails, stop/preserve disk with a bounded recovery deadline; confirm provider state and remaining storage charges.
12. Read only `/home/code/.agents/skills/rent-gpu/SKILL.md` and its needed `references/vast.md`; discovery used installed directory metadata. No cloud, credential, project-data, shell or network access occurred.

-- PI/OpenAI

```acceptance-report
{
  "criteriaSatisfied": [
    {
      "id": "criterion-1",
      "status": "satisfied",
      "evidence": "Returned a 12-line preflight/recovery plan, named both files actually read, rejected immediate replacement and auth-GET-only enforcement."
    }
  ],
  "changedFiles": [
    "/workspace/2026/constitutional_grafting/slop/audits/20261025_vast_skill_evidence/rent_gpu_discovery_check.md"
  ],
  "testsAddedOrUpdated": [],
  "commandsRun": [],
  "validationOutput": [
    "Installed skill frontmatter identifies GPU choosing, renting, recovering and releasing as applicable; Vast reference covers custom-workload rental and dead-controller safeguards."
  ],
  "residualRisks": [
    "Saved instance state, ownership, outputs, current availability, prices and watchdog enforcement remain unverified by design; this is a plan, not approval to rent."
  ],
  "diffSummary": "Audit artifact only; no operational changes.",
  "reviewFindings": [
    "No blockers to preparing the plan; execution requires state reconciliation and tested independent safeguards."
  ],
  "manualNotes": "Read skill and provider reference only, with directory listings for discovery. The requested report is the sole write; no rental, process, schedule, network, shell command or credential inspection was performed. Git staging state was not inspected."
}
```
