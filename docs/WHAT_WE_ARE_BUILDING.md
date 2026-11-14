# What we are building

*Living file: it describes the system as it actually is on the branch `constructor-attempt`. Last updated 2026-11-14, 06:20 (section 7, language models, is new).*

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
        |
        +--> predict.py: held-out interventions, construction vs baselines
        +--> server.py + static/constructor.html: run and inspect all of this in the browser
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

| Test | What is done | Pass mark | What it shows |
|---|---|---|---|
| Behaviour | Compare `model(x)` with the network's output | same decision on 95% of inputs | Level 1: can it run in place of the network? |
| Alignment | At each site, fit one affine map from the variables placed there to the activations (a write map M and a linear probe D) | reported | Where each variable lives; the map class is declared and restricted |
| Substitution | Replace the site's activation with the construction's prediction and run the rest of the network | 90% of decisions kept | "Keeping only what it names preserves behaviour"; at the embedding this is the embedding rebuilt from the construction |
| Necessity | Remove the named subspace; compare with mean-ablating the whole site | at least half of the damage of mean-ablation | "Removing only what it names destroys it" |
| Compactness | Count the named dimensions the output depends on against the number of principal components of the site that keep 90% of decisions | at most twice that number (or 4 more) | The variables are not a lookup table |
| Interchange | Copy everything named at the site from another input's run; compare the network's new decision with `model` run with those variables replaced | 90% of changed cases | Level 2: interchange intervention accuracy |
| Partial / edit | Two protocols that make states no input produces: copy one variable while the site's others stay (partial), or copy a random half of the coordinates of everything named at the site (edit) | 50% of changed cases on either protocol | A stricter level 2, off the data manifold; passing either is enough, so splitting a variable into parts never lowers the score |

Every intervention number is reported next to predictors that understand nothing: the same swap in a random
subspace, "no change", "the source input's output", and attribution patching (a first-order estimate computed on the
network itself). A site is **verified** when it passes substitution, necessity, compactness, interchange and
partial/edit. Sites that are identical for every input are ignored, and a site whose mean-ablation changes under 5%
of decisions cannot be verified. A construction is **verified** when it behaves like the network and every site it
names is verified, and **complete** when every stage of the network has a verified site. Thresholds: `PASS` in
`judge.py`. How each rule was arrived at is in `EXPERIMENT_LOG.md` (E0, E5, E6, E10).

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
- The one-layer transformers (mod-add, mod-mul): `embed.0..2`, `attn_pattern`, `attn_out`, `resid_mid`, `mlp_pre`,
  `mlp_post`, `mlp_out`, `resid_post`, `out`, in four stages: embedding, attention, MLP neurons, readout.
- General transformers (`nets.transformer`, any number of layers, no LayerNorm): `embed`, and per layer
  `attn{l}.pattern`, `attn{l}.out`, `resid{l}.mid`, `mlp{l}.pre`, `mlp{l}.post`, `mlp{l}.out`, `resid{l}.post`, each
  holding all positions flattened.

Networks with a `domain` (the constructor can run on these): the 4 Boolean nets, `modadd_p113`, `modmul_p113`, and
four programs compiled with Tracr by `lab/targets/build_tracr.py` (`tracr_hist`, `tracr_reverse`,
`tracr_first_match`, `tracr_count_greater`). The compiled networks have their residual stream rotated and their MLP
neurons permuted and rescaled, so the weights are dense; `weights_raw.npz` keeps the un-rotated weights. They are
compiled for one input length, so parts of a program that only react to length are constant and need no explanation.

MIT's game policies and shape generators have no `domain`: their inputs are game states and noisy images, and the
released logs (`github.com/RikiyaT/lm_understand-logs`) contain the weights and prompts but not the environments.

### 5. Held-out interventions (`lab/predict.py`)

A benchmark of interventions drawn without looking at any construction: at every site, subspaces (random, random
units, principal components) are removed or patched in from another input. The construction with its alignment
predicts each outcome without running the network, next to "no change", a regressor on statistics of the
intervention, attribution patching, and any other construction (for example the prior-only one).

### 6. The web page

`python3 lab/server.py`, then open `http://localhost:8765/constructor` (or press **Constructor** in the lab's top
bar). Left: pick a network, the weights variant (trained, shuffled, untrained, permuted), the step budget and what the
reader is told (blinded, task named, or the prior-only control), press **Construct**; past runs for the network are
listed below with their stage counts. Middle: the reader at work, live: its reasoning, its code and outputs, each
submission and the judge's report. Right: the best construction so far: verdict, the mechanism in words, a chip per
stage, the per-site table, the intervention table with its controls, what fails, a button that runs the held-out
intervention benchmark, and the construction's source. `lab/GUIDE.md` walks through it.

### 7. Real language models (added 2026-11-14)

The same constructor, with a different network layer underneath.

**Engine (`lab/lm.py`).** GPT-2-family checkpoints from Hugging Face, run by our own forward pass (it matches
Hugging Face's logits to 1e-4). A *site* is one vector per prompt at one token position:

| Site | What it is |
|---|---|
| `resid{L}@p` | the residual stream entering block L at position p (L = 0 is the embedding, L = n_layers the final stream) |
| `attn{L}@p`, `head{L}.{H}@p` | what attention layer L, or its head H, adds at p |
| `mlp{L}@p`, `neur{L}@p` | what MLP L adds at p; its hidden neurons |
| `pattern{L}.{H}@p` | head H's attention weights from p to every position |

`p` is a role of the task or a token index; `@*` is every position at once. Any site can be read or replaced
(`hook`). The residual stream of every prompt at every layer is cached, an intervention at layer L restarts from
layer L, and only positions at or after the earliest changed position are recomputed.

**Task (`lab/lm_tasks/*.py`, `lab/lm_build.py`).** One behaviour of one model: prompts of equal token length, integer
features `x` describing each prompt (the construction's input), roles (named positions), answer tokens (the
network's "output" is their logits at the end position). See `lab/lm_tasks/README.md`.

**Judge (`lab/lmjudge.py`).** The tests of section 2, applied to two kinds of unit:
- a **cut**: all residual sites the construction names at one depth, tested together. Substitution replaces the
  named positions by the construction's prediction and every other position at that depth by its mean, so a cut
  that passes holds everything the later layers need;
- a **component site** (attn, mlp, head, neur, pattern), tested alone.

Stages are depth bands: the embedding, then four bands of layers (12 layers: 0-2, 3-5, 6-8, 9-11). A stage is
explained when a cut inside it is verified; **complete** means every stage is. Two rules differ from section 2:
the size limit is measured against the principal components that keep 99% of answers (not 90%), and a
**categorical variable** (a one-hot identity of one quantity, with at least 6 prompts per value) is exempt from it.
Why: with hundreds of answer classes the 90% rule rejected even the best possible linear code (E16).

**Reader (`LM_SYSTEM` in `lab/constructor.py`, `lm_env` in `lab/kernel.py`).** Tools in the python session: `X`,
`PROMPTS`, `TOKENS`, `ROLES`, `ANSWERS`; `run(x, hook)`, `logits(x, hook)`, `acts(x, sites)`, `run_tokens(tokens)`
for prompts outside the task; the weights `W` under uniform names (`W_E`, `W_U`, `L3.W_Q` ...); `unembed`, `top`.
`hook` is how the reader runs its own ablation and patching experiments.

**Circuit (`lab/lm_circuit.py`).** The residual stream is a sum of what the heads and MLPs wrote, so the read-out
of a verified variable splits exactly into a share per component. The tool lists the top components for each
variable and site, where the heads attend, and what mean-ablating each does to the variable and to the answers.

**Runs.** The page launches runs as detached processes and follows them by polling `run.json`; `--resume` continues
a dead run from the reader's notes (saved every 12 steps) and best submission.

## How to use it

```bash
python3 lab/server.py                                   # web app; the constructor is at /constructor
python3 lab/constructor.py <target id> [--steps 80] [--variant ...] [--told] [--no-weights] [--one-shot]
python3 lab/judge.py <target id> <construction.py> [--variant ...]
python3 lab/predict.py <target id> <construction.py> [--also name=other_construction.py]
```

## Decided on this branch

- A construction is runnable Python with named variables and an affine alignment fitted by the judge on held-out
  data. The reader says *what* the variables are and *where* they live; the judge measures the map.
- The construction cannot see the weights. This is what stops "the network is the network" from counting.
- The reader may run the network and record activations (a construction is about *how*, and the tests score the how).
  Blinding hides the task, not the network.
- One reader with code and a judge, no roles or agents, until evidence shows more is needed.
- The loop, not the reader, sets the pace: after 6 steps without a submission the reader's next turn can only submit.
- The delivered `construction.py` claims only what passed: sites that failed in the best submission are removed from
  `ALIGN` by a footer the constructor appends, and the file is judged again.
- The constructor is frozen (prompt, tools, judge) before it is run on networks it was not developed on. Development
  networks: the Boolean nets, `modadd_p113`, `tracr_hist`. Everything else is held out.

## Not decided

- Whether one conversation is enough for the harder networks, or whether stage-by-stage sub-tasks are needed.
- Input sets for networks whose inputs are not enumerable (MIT's game policies).
- For language models: whether "one verified cut per depth band" is the right grain for "complete" (finer: every
  layer; coarser: three bands), and how to grade compact codes against identity variables.

## Where the rest lives

`docs/handoff/00_START_HERE.md` (entry point), `docs/EXPERIMENT_LOG.md` (experiments), `docs/CONVERSATION_LOG.md`
(decisions), `docs/literature/SYNTHESIS.md` (the field's measures).
