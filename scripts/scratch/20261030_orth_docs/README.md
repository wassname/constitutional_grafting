# Do the document adapters share a component that stacking multiplies?

-- PI/Claude (opus-5-5), 2026-10-30

Hypothesis (wassname): each document adapter = its own content + a shared part ("stoic+terse, const+terse, other+terse"); stacking
triples the shared part, so the mix breaks early (run 19: at ~0.75 of a combined coherence budget). Proposed fix: ablate Const's
part from the others (and Stoic's from Other), then redo the single-adapter and mix sweeps.

## Step 1: weight-space overlap (CPU, `01_overlap.py`)

Dense LoRA modules (250), Stoic / Const / Other document adapters:

| pair | cosine of the whole updates (median, max abs) | one's share in the other's output subspace (median) | chance |
|---|---|---|---|
| const · stoic | +0.000, 0.020 | 0.043 | 0.031 |
| const · other | +0.000, 0.013 | 0.042 | 0.031 |
| other · stoic | +0.001, 0.024 | 0.049 | 0.031 |
| stoic in const / other | – | 0.046 / 0.052 | 0.031 |
| other in const | – | 0.043 | 0.031 |

Reading: in weight space the three updates are close to orthogonal: whole-update cosines are about 0, and each puts 4-5% of its
update into the others' output subspaces, about 1.5x chance. Projecting one out of another would remove only a few percent of each
update. So a weight-space ablation is unlikely to change how the mix breaks; the hypothesis in its weight-space form is not supported.

Not ruled out: a functional shared part. Different weight directions can produce the same behaviour (a terse register, say), and
effects can compound nonlinearly. Next test (GPU, cheap on the next box): the change in hidden states each adapter causes on the
same prompts (cosine of delta-h per layer), and whether the replies of each adapter alone share a style. If delta-h overlap is
high, ablate in activation space rather than weight space.

## Step 1b: the same check on run 19's chat adapters (`01_overlap.py chat19`)

| pair | cosine (median, max abs) | share in the other's output subspace (median) | chance |
|---|---|---|---|
| between groups (dilemmas, help, texts, identity) | +0.001 to +0.004, max 0.038 | 0.047-0.067 | 0.031 |
| all-data · dilemmas | +0.023, max 0.081 | 0.094 | 0.031 |
| all-data · help / texts / identity | +0.008 to +0.012 | 0.058-0.074 | 0.031 |

Reading: even the all-data adapter, trained on a superset of the dilemmas rows, has a whole-update cosine of only +0.02 with the
dilemmas adapter. So weight-space overlap is a poor detector of shared function here: LoRAs start from different random A and
land in mostly different subspaces even when they learn related things. The near-orthogonal document adapters (step 1) therefore
do not rule out a shared behaviour. The common-factor test has to be functional: hidden-state change per adapter on the same prompts
(task 36), or reply style.
