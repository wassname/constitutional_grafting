---
name: vast-rental
description: "Rent a vast.ai GPU and run this repo's box driver (scripts/box/) on it: pick an offer, size the lease, smoke-test first, keep the dead-man's switch on, retrieve and destroy. Use before renting, writing a run config in configs/runs/, recovering a lease, or when a Vast box stalls."
---

# Vast rental for this repo

The box driver is `scripts/box/`: `rent.py` owns the lease (runs locally), `box.py` runs the stages on the box, `cells.py` merges, serves and generates each graft cell. One YAML per run in `configs/runs/` (start from the newest one). Read the code before a lease; this file lists what it does and the failures behind it.

## Procedure

1. Write `configs/runs/<run>.yaml`: offer query, `max_hours`, `budget_usd`, adapters, cells in priority order (references and treatment first, extra doses last, so a cut lease still answers the question).
2. `just box-smoke configs/runs/<run>.yaml`: a CPU config check (seconds), then the real driver on a tiny random model on a local GPU (real axolotl, merge, vLLM, scorers; under ~5 min). It writes `.local/<run>/smoke_passed.json`; `rent.py` refuses to rent unless the smoke passed on the same code hashes. Stub dry runs miss real-tool errors (CLI paths, config keys, server flags).
3. Put adapters on the Hugging Face Hub (`adapter_hub:` in the config), cast to bf16 first (`scripts/train/19_cast_adapter.py`). The box downloads them at data-centre speed; sha256 is checked against the local copy.
4. `just box-rent configs/runs/<run>.yaml` (needs `VASTAI_API_KEY` in `.env`). Run it under a supervised process with its output in a log, not a bare shell `&`. Other actions: `attach | push | snapshot | destroy`.
5. Check in at about 50% of the lease: stages done and minutes per cell against the estimate. Drop low-priority cells (`push` the config) while there is still time.
6. On success the controller retrieves logs and outputs, checks hashes, then destroys the box. On a driver failure it holds the box up to 60 min with the heartbeat on: fix the code, `rent.py CONFIG push`, then `touch .local/<run>/resume`; stages whose receipts and adapter hashes match are skipped.

## Choosing an offer

The cheapest offers often do not work: the host has a day left, a small disk, a driver that cannot run the image's CUDA, or slow network. Filter first, then sort by price:

| field | check |
|:--|:--|
| `datacenter` | true |
| `reliability2` | ≥0.95 |
| `duration` | ≥ run length plus margin (we use ≥1 day) |
| `disk_space` | ≥400 GB for a 35B-class model: Base + Instruct HF cache ~135 GB, each merged bf16 checkpoint ~66 GB |
| `gpu_ram` | the model fits (bf16 inference ≈ 2 bytes/param + KV cache) |
| `cuda_max_good` | at least the image's CUDA |
| `inet_down` | ≥500 Mbps |
| `inet_down_cost`, `inet_up_cost` | $/GB on top of `dph_total`; downloading ~140 GB of weights at 0.039 $/GB costs more than a few GPU hours. Compare. |
| `dph_total` | compare after adding bandwidth cost |

If the cheapest passing offer is far below the median for that GPU, find out why before renting. RTX PRO 6000 / RTX 6000 Ada cards are often the best value for one-GPU work.

## Sizing the lease

- A lease that runs out of time costs more than slack: everything before the cut is paid for and the question stays open. The controller destroys the box when the job ends, so slack only costs money when something goes wrong.
- `rent.py` stops the runner at `max_hours - 1` and destroys at `max_hours`. Set `max_hours - 1` to about 1.5x the estimate. Example: 5 h for a 3.5 h estimate gave a 4 h runner deadline (1.14x) and finished 2 of 4 cells.
- Estimate from measured runs and write the estimate in the config comment. Measured: image pull and SSH ~30 min; ~45-60 min per evaluation cell on a 35B MoE (plus a ~10 min one-time vLLM kernel build on the first serve); high-dose cells that ramble to the length cap took 1.5-2 h. Find the breakdown dose with a short-token probe before the full sweep.
- The driver refuses to start a cell with under 20 min to the runner deadline.

## Dead-man's switch

A box bills until someone stops it. Two independent stops:

- **On-box watchdog** (`scripts/train/box_watchdog.sh`): the controller touches `/workspace/heartbeat` over SSH every 60 s; after `MAX_SILENT_H` without one the box stops itself. It uses the per-instance key from `/proc/1/environ` (`CONTAINER_ID`, `CONTAINER_API_KEY`; an SSH shell may not have them): `PUT https://console.vast.ai/api/v0/instances/$CONTAINER_ID/` with `{"state": "stopped"}`. Check auth with a read-only `GET` of the same URL.
- **Local hard deadline**: a systemd timer (`scripts/eval/48_vast_deadline.py`) destroys the instance at `max_hours` even if the controller is alive.

Never send `{"state": "running"}` as a check: on a running box it relaunched the container and killed every process (files on disk survived). Stop keeps the disk but still bills storage; destroy by hand after retrieving and checking hashes.

## Gotchas seen

- **SSH via proxy.** `ports` can stay `None` while `actual_status` is `running`; then SSH goes through `ssh_host:ssh_port` (e.g. `ssh5.vast.ai:29198`), not the public IP. A wait loop that requires port 22 never exits; one lease timed out this way. `rent.py` falls back to the proxy.
- **Log every SSH-wait poll**: `actual_status`, `status_msg`, whether `22/tcp` is mapped, proxy host:port, SSH return code. Wait at least 45 min (the ~20 GB Axolotl image pull takes ~30 min); treat SSH timeouts as not-ready.
- **Uploads from a home connection are slow** (1-3.5 MB/s observed; 28 GB of fp32 adapters cost two leases, with rsync streams resetting together). Upload once to the Hub and let the box download. If rsync is unavoidable, `rent.py` retries 12 times with `--partial`; never run two leases' uploads at once.
- **Disk fills**: delete merged checkpoints and `checkpoint-*` once retrieved.
- After launch `rent.py` checks `nvidia-smi` and that torch sees >90 GiB of GPU memory. If a host check fails, destroy and pick another offer; do not debug the host.

## API

CLI: `uv tool install vastai`. REST works without it, with `Authorization: Bearer $VASTAI_API_KEY`:

- `GET https://console.vast.ai/api/v0/users/current/`: spendable money is `credit`, not `balance` (`balance` can read 0 with credit available).
- `GET https://console.vast.ai/api/v0/bundles/?q=<json>`: offers, e.g. `{"gpu_ram":{"gte":80000},"rentable":{"eq":true},"reliability2":{"gte":0.95},"disk_space":{"gte":200},"order":[["dph_total","asc"]]}`.

Vast's own [agent skill](https://github.com/vast-ai/vast-claude-plugin/blob/main/skills/vastai/SKILL.md) covers CLI flags and SSH-key registration; do not copy its destroy-on-offline step before outputs are retrieved.

-- PI/Claude (opus-5-5), 2026-10-30, adapted from the maintainer's private rent-gpu skill.
