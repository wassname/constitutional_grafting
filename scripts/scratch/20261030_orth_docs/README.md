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
