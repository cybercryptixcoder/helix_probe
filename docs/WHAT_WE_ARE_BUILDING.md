# What we are building

*Living file: it describes the system as it actually is on the branch `constructor-attempt`. Last updated 2026-11-13.*

**The constructor**: a system that takes a neural network and produces a verified **construction** of it: a small
program that computes what the network computes, the way the network computes it, with a statement of where each of
its variables lives in the network. Everything is in `lab/`.

## The pieces and how they connect

```
 network (weights.npz + meta.json)                       lab/models/<id>/
        |
        |  nets.py: forward pass with named activation SITES, grouped into STAGES;
        |           the input set; the controls (shuffled, untrained, permuted)
        v
 constructor.py  <---- the reader (DeepSeek V4.1 Flash via Luminal)
        |   python tool  -> kernel.py: a persistent Python session with W, X, run(x), acts(x)
        |   submit tool  -> judge.py: tests the submitted construction, returns a text report
        v
 lab/constructions/<id>/<run id>/   run.json, every submission and report, the best construction
```

### 1. A construction (the thing produced)

A standalone Python file. It may use numpy and math only and **cannot see the weights**, so every constant in it was
measured and written down, and its length is its description length (limit 16,000 characters).

```python
DESCRIPTION = "plain-language account of the mechanism"

def model(x, iv):
    # x: inputs [B, n_in]; returns the predicted network output [B, n_out].
    # Each named variable is registered:  v = iv("name", value).  Later steps use what iv returned,
    # so that when a test replaces a variable's value, the rest of the model responds.
    ...

ALIGN = {"name": ["site", ...]}     # the activation sites where each variable lives
```

### 2. The judge (`lab/judge.py`)

The same tests for every network; nothing in it knows any task. Half the inputs are used to fit, half to test.

| Test | What is done | What it shows |
|---|---|---|
| Behaviour | Compare `model(x)` with the network's output | Level 1: can it run in place of the network? |
| Alignment | At each site, fit one affine map from the variables placed there to the activations | Where each variable lives (the map class is declared and restricted: affine) |
| Substitution | Replace the site's activation with the construction's prediction and run the rest of the network | "Keeping only what it names preserves behaviour"; this is also the embedding or readout rebuilt from the construction |
| Removal | Remove the named subspace; compare with removing a random subspace of the same size and with mean-ablating the site | "Removing only what it names destroys it", and the variables are specific |
| Interchange | Copy a variable (read by a linear probe) from another input's run; compare the network's new output with `model` run with that variable replaced | Level 2: same response to interventions (interchange intervention accuracy) |
| Edit | Set a random half of a variable's coordinates to another input's values, a state no input produces | A stricter level 2, off the data manifold |

Every number is reported next to controls that understand nothing (a constant output, a random subspace, "no change",
"the source input's output", mean-ablation). A site is **verified** when it passes substitution, removal, interchange
and edit. A construction is **verified** when it also behaves like the network and every site it names is verified,
and **complete** when every stage of the network has a verified site. Thresholds: `PASS` in `judge.py`.

### 3. The constructor (`lab/constructor.py`)

One reader, one conversation, two tools:
- `python(code)`: a persistent session over the network: `W` (weights), `X` (the inputs the network is used on),
  `run(x)`, `acts(x)` (activations at every site), numpy, scipy, sklearn.
- `submit(code)`: sends a construction file to the judge and returns the report.

The reader is **blinded** by default: it gets the architecture, the tensor and site lists and the input set, and is
not told what the network does. The prompt (`SYSTEM` in `constructor.py`) is the same for every network. The loop
reminds the reader to submit when it goes 7 steps without submitting. When the conversation nears the context limit,
the reader writes its notes and continues from the notes and its best submission. The run ends at "verified and
complete", when the reader stops, or when the step budget is used; the best submission is kept.

Options: `--variant shuffled|untrained|permuted` (controls), `--told` (name the task), `--no-weights` (no weights and
no network: with `--told` this is the prior-only control).

### 4. Networks, sites and input sets (`lab/nets.py`, `lab/models/`)

Each network's `meta.json` keeps apart the architecture text, the task context (hidden when blinded), the hidden
answer, and `domain`, the set of inputs the network is used on, which names no task. Sites:
- MLPs: `h1`, `h2`, ... (hidden layers after the activation), `out`.
- The one-layer transformers: `embed.0..2`, `attn_pattern`, `attn_out`, `resid_mid`, `mlp_pre`, `mlp_post`,
  `mlp_out`, `resid_post`, `out`, in four stages: embedding, attention, MLP neurons, readout.

MIT's game policies and shape generators have no `domain` yet (their inputs are game states and noisy images, which
the released logs do not include), so the judge cannot run on them yet.

## How to use it

```bash
python3 lab/constructor.py <target id> [--steps 60] [--variant ...] [--told] [--no-weights]
python3 lab/judge.py <target id> <construction.py> [--variant ...]
```

The lab's web app (`python3 lab/server.py`, see `lab/GUIDE.md`) still offers only the earlier hand-driven weight
reading. Wiring the constructor into it is a next step.

## Decided on this branch

- A construction is runnable Python with named variables and an affine alignment fitted by the judge on held-out
  data. The reader says *what* the variables are and *where* they live; the judge measures the map.
- The construction cannot see the weights. This is what stops "the network is the network" from counting.
- The reader may run the network and record activations (a construction is about *how*, and the tests score the how).
  Blinding hides the task, not the network.
- One reader with code and a judge, no roles or agents, until evidence shows more is needed.

## Not decided

- Whether one conversation is enough for the harder networks, or whether stage-by-stage sub-tasks are needed.
- Input sets for networks whose inputs are not enumerable.
- How to extend sites to deeper transformers and a real language model.

## Where the rest lives

`docs/handoff/00_START_HERE.md` (entry point), `docs/EXPERIMENT_LOG.md` (experiments), `docs/CONVERSATION_LOG.md`
(decisions), `docs/literature/SYNTHESIS.md` (the field's measures).
