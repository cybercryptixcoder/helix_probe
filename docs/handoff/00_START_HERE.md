# Helix Probe: start here

*Living entry point, kept current after every working session. Last updated Nov 14, 2026 (branch `constructor-attempt`). Anyone handed
this repo should be able to continue from these files alone, with no separate handoff.*

## CURRENT STATE (2026-11-14, session 3, branch `constructor-attempt`). Read this first.

> **This branch** is a separate attempt at the main goal, the constructor. `main` continues independently; never
> push this branch's work to `main`, and never edit `main`. Every substep is committed and pushed
> (`bash /home/claude/push.sh "message"`; recreate that script from "How work is persisted" below if it is gone).

### The goal of this session

Turn the constructor into a **discovery-grade tool**: one that works on real language models, and use it to make a
previously unexplained mechanism interpretable (a verified construction, controls, prior-only control, a new
checkable claim). The tool is the deliverable; the discovery proves it.

### What was added in this session (all in `lab/`; details in [`docs/WHAT_WE_ARE_BUILDING.md`](../WHAT_WE_ARE_BUILDING.md) §7)

| Piece | File | What it does |
|---|---|---|
| LM engine | `lab/lm.py` | GPT-2-family models (from Hugging Face) with named, replaceable activation sites at any token position: `resid{L}@p`, `attn{L}@p`, `head{L}.{H}@p`, `mlp{L}@p`, `neur{L}@p`, `pattern{L}.{H}@p`. Caches the residual stream, recomputes only what an intervention can change. Matches Hugging Face's logits to 1e-4. |
| LM task | `lab/lm_tasks/*.py`, `lab/lm_build.py` | A task file names the model, the prompts, the input features, the roles (named positions) and the answer tokens. `python3 lab/lm_build.py lab/lm_tasks/<file>.py` turns it into a target in `lab/models/<id>/`. How to write one: `lab/lm_tasks/README.md`. |
| LM judge | `lab/lmjudge.py` | The same tests as `judge.py`, with **cuts** (all residual sites named at one depth, tested together, the other positions mean-ablated) and **stages by depth band** (embedding + four bands of layers). Categorical identity variables allowed. `python3 lab/judge.py <lm target> <file>` dispatches here. |
| Reader session for LMs | `lab/kernel.py` (`lm_env`), `LM_SYSTEM` in `lab/constructor.py` | The reader gets `run`, `logits`, `acts`, `hook=` (its own patching experiments), `run_tokens`, the weights `W`, `unembed`, `top`. |
| Resume, notes, stop | `lab/constructor.py` | `--resume <run id>` continues a dead or stopped run from the reader's last notes (written to disk every 12 steps) and its best submission. A `STOP` file in the run folder stops a run. |
| Circuit | `lab/lm_circuit.py` | From a verified construction: which heads and MLPs write each variable (exact linear split of the read-out), where those heads attend, and a mean-ablation check of each. |
| Web page | `lab/server.py`, `lab/static/constructor.html` | Runs are launched as **detached processes** and followed by polling (they survive the page and the server); Stop and Resume buttons; language-model targets; a "what is held where" map; the circuit view; a panel that builds targets from task files. |

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu && pip install transformers   # once; GPT-2 is downloaded on first use
python3 lab/server.py                                          # http://localhost:8765/constructor
python3 lab/lm_build.py lab/lm_tasks/countdown.py              # build (or rebuild) an LM target
python3 lab/constructor.py gpt2_countdown --steps 150          # a blinded run (needs lab/.env with LUMINAL_API_KEY)
python3 lab/constructor.py gpt2_countdown --resume <run id> --steps 250    # continue a dead or stopped run
python3 lab/constructor.py gpt2_countdown --told --no-weights --one-shot   # the prior-only control
python3 lab/judge.py gpt2_countdown <construction.py>          # judge any construction file
python3 lab/lm_circuit.py gpt2_countdown <run id>              # which components write each variable
```

### The target chosen: how GPT-2 small counts down (`gpt2_countdown`)

GPT-2 small continues "41, 42, 43, 44," with 45 and "44, 43, 42, 41," with 40: 100% on both, over 800 prompts (last
number 20 to 119, four prefixes), choosing among 362 number tokens. Counting **up** is in the literature (successor
heads, Gould et al. 2023; the increasing-sequence circuit, Lan & Barez 2024). How the model decides the direction
and how it counts **down** is not (searched 2026-11-14; nothing found). Why this target, and what was rejected:
`docs/EXPERIMENT_LOG.md` E13-E15.

### Latest results

See "Working on right now" and `docs/RESULTS_CONSTRUCTOR.md`. Judge calibration on this target
(`lab/constructions/_oracle/gpt2_countdown_first_guess.py`, hand-written, E17): the two late stages verify (the end
position holds the identity of n4 and the direction at depth 9; the answer's identity at depth 12); my guesses for
the early and middle stages fail, which shows the judge discriminates and that the middle of the network is the
open question (in particular: the direction is NOT a linear variable at the n4 position at depth 6).

### Working on right now (updated 2026-11-14 06:20)

- **In flight (detached):** blinded run A on `gpt2_countdown` (150 steps) and prior-only control 1. Logs:
  `/home/claude/logs/`; run folders: `lab/constructions/gpt2_countdown/`. If they are dead when you read this,
  resume with `--resume <run id>`.
- An auto-commit loop pushes every 10 minutes (`/home/claude/autopush.sh`; it does not survive the session).
- Next: read what run A does, fix what blocks the reader, launch replicates; second LM target; write-up.

### Tried and failed in this session, and why

- **The ordinal suffix (23 -> "rd") as a target** (E13). GPT-2 small does it at 98.6%, but the suffix class is linearly
  present in the number's token embedding and stays so at every layer: nothing is computed, and a know-nothing
  construction would pass. Kept as the small demo target `gpt2_ordinal`.
- **Arithmetic progressions with a step above 1** (E14): GPT-2 small cannot continue them (it says last + 1), so
  there is no capability to explain.
- **TransformerLens** as the engine: version 4 removed `HookedTransformer`; a 250-line engine of our own was faster
  to write than to learn the new API, and gives the restart-from-layer and changed-positions-only speedups.
- **The size limit as judge v3 had it** (at most twice the principal components that keep 90% of answers): with 362
  answer classes even the best possible linear code needs about 20 dimensions to pass interchange while 7 "suffice"
  (E16). For LM targets the limit is now measured at 99% of answers, and one-hot identities of single quantities
  are exempt.

### Exact next steps

1. Follow run A; relaunch or resume as needed; run two more blinded replicates and two more prior-only controls.
2. When a construction verifies the middle stages: `lm_circuit.py` on it, then state its new claim (what the model
   does on sequences the prompts do not contain) and test that claim on fresh prompts.
3. A stricter pass without identity variables (compact codes only): E16 shows a 29-dimensional Fourier code over
   period 100 passes at depth 9, so it exists to be found.
4. A second LM target with all-binary variables (number x tense of "is / are / was / were"; E15 shows GPT-2 does it).
5. A second model family in `lm.py` (Pythia / GPT-NeoX): add a loader that fills the same weight names.

### How work is persisted

- `bash /home/claude/push.sh "message"`: checks the branch, refuses if the Luminal key is in the diff, commits as
  `cybercryptixcoder`, pushes. The script (recreate if missing):
  ```bash
  cd <repo> && [ "$(git rev-parse --abbrev-ref HEAD)" = constructor-attempt ] && git add -A && \
  ! git diff --cached | grep -q "<first 12 characters of the key>" && \
  git -c user.name=cybercryptixcoder -c user.email=official.shreyas28@gmail.com commit -q -m "$1" && git push -q origin constructor-attempt
  ```
- The Luminal key lives only in `lab/.env` (gitignored). A new session must create that file again.
- Long work is started detached (`setsid nohup ... &`), writes its state at every step, and can be resumed.

### Map of files added in this session

| File | What it holds |
|---|---|
| `lab/lm.py` | The LM engine and the LM task loader |
| `lab/lm_build.py`, `lab/lm_tasks/` | Building LM targets from task files; `README.md` there explains the format |
| `lab/lmjudge.py` | The judge for LM targets (cuts, depth stages) |
| `lab/lm_circuit.py` | Components that write each verified variable |
| `lab/models/gpt2_countdown/`, `lab/models/gpt2_ordinal/` | The two LM targets (prompts, features, roles; no weights) |
| `lab/constructions/_oracle/gpt2_countdown_first_guess.py` | Hand-written calibration construction for the LM judge |
| `lab/constructions/gpt2_countdown/<run id>/` | Constructor runs on the countdown target |

> **EARLIER STATE (session 2, Nov 13).** Still accurate for everything that is not a language model.

## STATE AT THE END OF SESSION 2 (2026-11-13)

> **This branch** is a separate attempt at the main goal, the constructor. `main` continues independently; never
> push this branch's work to `main`, and never edit `main`. The rule for the repo still holds: it is a living
> documentation store, and a fresh session must be able to continue from the docs alone. On this branch every
> substep is committed and pushed (see "How work is persisted" below).

### The goal

A **constructor**: a system that takes a neural network and produces a **construction** of it. A construction is a
white-box reconstruction that *predicts* what the network does, including under intervention. In the field's terms
it is a causal abstraction: named variables, the steps that compute them, and an alignment saying where each lives
in the network. It is judged by three tests, each against baselines that understand nothing
(`literature/SYNTHESIS.md` §4, §10):
1. run it in place of the network: same outputs?
2. intervene on a variable in both: same change?
3. same internal computation?

The bar, in order: (1) a blinded, verified construction of Mystery transformer A (`lab/models/modadd_p113`) with
controls; (2) the same constructor, unchanged, on networks it was not developed on; (3) predictions of held-out
interventions that beat know-nothing baselines; (4) stretch: one behaviour inside a small open language model.

### What exists now, and how to run it

Everything is in `lab/`. Full description: [`docs/WHAT_WE_ARE_BUILDING.md`](../WHAT_WE_ARE_BUILDING.md).
Using the web page: [`lab/GUIDE.md`](../../lab/GUIDE.md), section "The constructor page".

| Piece | File | What it does |
|---|---|---|
| Construction format | top of `lab/judge.py` | A standalone Python file: `model(x, iv)` computes the output through named variables; `ALIGN` says at which activation sites each variable lives. It cannot see the weights. |
| The judge | `lab/judge.py` | Tests a construction against a network: behaviour, alignment fit, substitution, necessity, compactness, interchange, partial/edit tests, each next to controls (including attribution patching). The same for every network. |
| The constructor | `lab/constructor.py`, `lab/kernel.py` | The reader (DeepSeek V4.1 Flash) investigates the network in a persistent Python session, submits constructions, reads the judge's reports and revises. Blinded by default. |
| Sites, controls, input sets | `lab/nets.py` | Forward passes with named activation sites; shuffled / untrained / permuted variants; each network's input set. |
| Compiled targets | `lab/targets/build_tracr.py` | Four RASP programs compiled with Tracr into rotated transformers (`lab/models/tracr_*`). |
| Held-out interventions | `lab/predict.py` | Interventions drawn without looking at the construction; the construction against no-change, a statistics regressor, attribution patching, the prior-only construction. |
| Questions | `lab/ask.py` | Put a specific question to the reader about a constructed network. |
| Results | `lab/results.py` | Writes a `README.md` in each run folder, `lab/constructions/INDEX.md` and `docs/RESULTS_CONSTRUCTOR.md`. |
| Web page | `lab/server.py`, `lab/static/constructor.html` | Run and inspect all of the above in the browser at `/constructor`. |

```bash
python3 lab/server.py                                        # web app; open http://localhost:8765/constructor
python3 lab/constructor.py modadd_p113                       # a blinded run (needs lab/.env with LUMINAL_API_KEY)
python3 lab/constructor.py modadd_p113 --variant shuffled    # a control
python3 lab/constructor.py modadd_p113 --told --no-weights --one-shot     # the prior-only control
python3 lab/judge.py <target> <construction.py>              # judge any construction file
python3 lab/predict.py <target> <construction.py>            # held-out interventions against baselines
python3 lab/ask.py <target> <run id> "question"              # ask the reader about a constructed network
python3 lab/results.py                                       # regenerate the result pages and tables
```

Each constructor run writes `lab/constructions/<target>/<run id>/`: `run.json` (every step), each submission with
its judge report, the best one as `construction.py` with `report.txt`, and a `README.md`.

### Latest results (numbers and run links: [`docs/RESULTS_CONSTRUCTOR.md`](../RESULTS_CONSTRUCTOR.md))

All runs blinded unless stated. "Complete" means every stage of the network has a site that passes every test.
"Held out" means the network was first run after the constructor (prompt, tools, judge) was frozen.

| Network | Held out? | Result | Runs |
|---|---|---|---|
| XOR, 3-bit parity, 2-bit compare, majority (tiny MLPs) | no | Complete, 2 steps each | 1 each |
| `modadd_p113`, Mystery transformer A | no | 3 of 4 stages every time: Fourier features at {8, 11, 22, 23, 25} at the embeddings, cos/sin of k(i+j) in the MLP neurons, cosine readout with amplitudes [12.5, 6.2, 0.3, 9.8, 6.7]. Attention never verified; a hand-written oracle fails there too. | 5 (E3, E8, E10) |
| `tracr_hist` (compiled, rotated) | no | Complete, 21 steps | 1 (E6) |
| `tracr_reverse` | **yes** | Complete, 9 steps | 1 (E8) |
| `tracr_first_match`, `tracr_count_greater` | **yes** | Complete both times (23 and 22 steps; 47 and 33 steps) | 2 each (E8, E10) |
| `modmul_p113`, Mystery transformer C | **yes** | Complete once (76 steps): Fourier over the discrete log base 3 at {4, 28, 31, 41}, confirmed independently; additive code after attention; product clock by a squaring identity in the MLP. Second run: 3 of 4 (attention unnamed). | 2 (E8, E10) |
| `astra_breakout`, MIT's hand-written MinAtar Breakout policy | **yes** | Complete, 32 steps, 100% behaviour, every intervention test 100%; matches the known design unit for unit. Asked a specific question afterwards, the reader named Breakout (E12). | 1 (E12) |

Controls (E4, E8, E10):
- **Prior-only** (task named, no weights, one submission): 0 of 4 stages on mod-add (3 runs) and on mod-mul (1 run).
- **Shuffled weights**: 0 stages, no mechanism claimed. **Untrained weights**: not verified (behaviour 94.8%); the
  one passing stage is a 112-dimensional token lookup, which is what a random embedding is.
- **Permuted weights**: 3 of 4 stages, the same construction as on the original weights.
- **Judge calibration** on mod-add, repeated after every judge change: the hand-written oracle passes 3 stages; the
  same file with wrong frequencies and a lookup table get 0; all three match behaviour on 100% of inputs.

Held-out interventions (E7, E9): the construction beats "no change", the statistics regressor and the prior-only
construction on mod-add and on 3 of 4 compiled networks, and beats attribution patching on interventions on its own
variables in nonlinear stages (mod-add embedding 100% against 36%; mod-mul embedding and attention 93–98% against
3–30%). On arbitrary subspace interventions attribution patching is ahead on every network, and it is exact
wherever the path to the output is linear. **Level 3 as the bar states it is not met.**

Where the bar stands: level 1 (blinded replication of mod-add, with controls) met at 3 of 4 stages; level 2 (same
constructor on unseen networks) met on six held-out networks, with one of two mod-mul runs incomplete; level 3
partly; level 4 (a real language model) not attempted.

### Working on right now (updated 2026-11-14 01:40)

- Batch 2 is finished: the last run, mod-add replicate B, ended at 3 of 4 stages like the others.
- Nothing else is in flight. The constructor is frozen at `b8a40aaa`; it may be edited again now.
- `modsub_p113` is NOT trained (the job was killed at epoch 11,750 of 25,000). To get it:
  `python3 lab/targets/train_modadd.py --op sub --p 113 --seed 0 --out lab/models/modsub_p113` (about 1.5 hours on
  2 CPUs), then `python3 lab/targets/build_registry.py`, then a blinded run.

### Tried and failed, and why

- Letting the reader decide when to submit (E1), then reminding it (E2): it tried to understand the hardest stage
  completely before testing anything. Fixed by forced submit turns (E3).
- Reading a variable out of activations with the pseudo-inverse of the alignment map (E0): unnamed variance leaks
  into the decode. A fitted linear probe is used for interchange.
- The random-subspace gate and coordinate edits on every variable (judge v1): rejected a correct construction of a
  compiled network (E5). Replaced by necessity, compactness, and partial tests.
- Demanding 90% of every single-variable swap (judge v2): punished a finer construction of mod-add (E6).
- Editing the judge while runs were in flight (E4): the runs had to be discarded.
- Translating an arbitrary activation edit into variable changes with the linear probe in `predict.py` (E7): worse
  than "no change". The pseudo-inverse of the alignment map is the faithful translation there.
- MIT's PPO game policies (experiment 1): no environment or states are released, so there is no input set to judge
  on. Their experiment-5 Breakout policy uses public MinAtar and was used instead (E11, E12).

### Exact next steps (what I would try next, in order)

1. **Make runs resumable.** Two session interruptions killed runs part-way. `constructor.py` saves every step but
   cannot continue a run: add `--resume <run id>` (rebuild the conversation from `run.json`, restart the Python
   session, tell the reader its variables are gone).
2. **Reliability on mod-mul and mod-add.** Both 3-of-4 runs ran out of steps on a late stage. Try a 120-step budget,
   and a final "which stages are still unexplained" turn that names the uncovered stage and its sites.
3. **The attention stage of mod-add.** It needs a compact model of how the ReLU layer treats mixed token features
   (`CONVERSATION_LOG.md`, 19:55). Write the oracle first; if no oracle passes, say so and stop.
4. **Level 3.** Fit a causal read map for the alignment (how the output-relevant variables respond to small
   perturbations at a site, on the fit inputs) and rerun `predict.py`; report against attribution patching again.
5. **More held-out networks**: `modsub_p113` (train it); compiled programs with variable-length inputs, so the length
   computation is exercised; MinAtar policies for other games from MIT's experiment 5 (`build_minatar.py` is written
   for Breakout; Seaquest and Asterix need their channel mappings from MIT's prompts).
6. **MIT's PPO game policies** need an input set; MIT did not release their environments.
7. **Stretch**: sites for a transformer with LayerNorm, then one behaviour in a small open language model.

### How work is persisted

- `bash /home/claude/push.sh "message"` on the session machine: checks the branch is `constructor-attempt` and that
  the Luminal key is in no tracked file, commits as `cybercryptixcoder`, pushes. Used after every substep.
- The Luminal key lives only in `lab/.env` (gitignored). A new session must create that file again.
- `judge.py`, `constructor.py`, `kernel.py` and `nets.py` are not edited while official runs are in flight.

### Map of files added on this branch

| File | What it holds |
|---|---|
| `lab/judge.py` | The judge and the definition of a construction |
| `lab/constructor.py`, `lab/kernel.py` | The constructor loop, its prompt and tools; the reader's Python session |
| `lab/nets.py` (extended) | Activation sites, stages, input sets, a general transformer |
| `lab/predict.py` | Held-out intervention benchmark with baselines |
| `lab/ask.py` | Specific questions to the reader about a constructed network |
| `lab/results.py` | Result pages and tables |
| `lab/static/constructor.html`, `lab/server.py` (extended) | The constructor page and its endpoints |
| `lab/targets/build_tracr.py`, `lab/models/tracr_*` | Compiled targets |
| `lab/constructions/_oracle/` | Hand-written reference constructions used to calibrate the judge (not made by the constructor) |
| `lab/constructions/<target>/<run id>/` | Constructor runs; `lab/constructions/INDEX.md` lists them |
| `docs/EXPERIMENT_LOG.md` | Every experiment on this branch (E0–E12), with failures |
| `lab/targets/build_minatar.py`, `lab/models/astra_breakout` | MIT's hand-written Breakout policy with real game states |
| `docs/RESULTS_CONSTRUCTOR.md` | The results table (generated) |

### Map of the docs

| File | What it holds |
|---|---|
| `docs/WHAT_WE_ARE_BUILDING.md` | The system as it is now: components, how they connect, how to use them |
| `docs/EXPERIMENT_LOG.md` | Dated experiments on this branch |
| `docs/RESULTS_CONSTRUCTOR.md` | Results table with links to each run's page |
| `docs/CONVERSATION_LOG.md` | Every idea, question, instruction and decision, in order |
| `docs/DIRECTIONS.md` | All research directions; only the constructor is in scope on this branch |
| `docs/literature/SYNTHESIS.md` | What the interpretability field builds and measures; what a construction is |
| `docs/literature/core/`, `docs/literature/wsp/` | Paper entries; `wsp/K1_STATE_OF_ART.md` covers LLMs reading weights |
| `lab/README.md`, `lab/GUIDE.md`, `lab/RUNNING.md` | The lab's web app |

Proposals, pitches and personal plans are deliberately kept **out of this public repo**.

> **SUPERSEDED.** Everything below this line is the earlier state (Nov 8–11), kept for history.

---

## The two goals (from `docs/NORTH_STAR.md`)

1. **Goal 1, capability removal:** show that Helix Probe lets a cheap model switch off one specific ability inside
   a real language model by editing its weights directly, while the rest keeps working, and that the loop, not
   luck, is what makes it work.
2. **Goal 2, the map:** the same loop, pointed at discovery instead of search, builds a verified map of which parts
   of the model do what. It leads to a demo where you change a part and watch behaviour change.

## Where things stand (Nov 8, 2026, 02:30 ET). Read this first.

**Nothing is running.** No Colab runtimes exist; `wsp` was reclaimed and `wsp2` was stopped at Shreyas's request.
The ≤9-minute check-ins were stopped by Shreyas. Every result is on GitHub, apart from the raw files of six 9B r0
runs, which were lost (their results are recorded in JOURNAL). The plain-language summary of everything found is
**`docs/FINDINGS.md`**.

### Goal 1: remove one ability by direct weight edits, and show the loop is why

- **Steps 0–3 done; 2b and 2c done** (the extra helix2 runs and the 0.8B axis).
- **Result:**
  - real removals (verdict v2: gone in every wording, precise, durable): helix2 2/12, MIT 0/9, Helix 0/9;
  - both successes are two-digit addition: the 9B readout edit (helix2 r5) and the 0.8B internal edit
    (helix2 r1);
  - every other pass was a trigger-token swap.
  - Full table: JOURNAL, Nov 7, 20:30.
- **Next: Step 4, the write-up.** No GPU is needed.
  - Contents: results table, how each edit works, honest negatives, how to re-run.
  - Sources: FINDINGS.md, the JOURNAL table, `results/edit*/`.
  - Open question for Shreyas: write now, or first add about 6 more helix2 addition runs (9B and 0.8B, about
    6–8 GPU hours) to firm up 2/12?

### Goal 2: a verified map of which parts do what, then a UI

- **D0 done. D1 and D2 both failed** their 5 pre-registered criteria (`GOAL2_CALIBRATION_RESULT.md`).
- **Shreyas has not yet chosen the next step:**
  - (A) stop, and publish the negative with Goal 1;
  - (B) recommended: a scripted ablation sweep over components × 26 behaviours on held-out questions is the map,
    the loop then explains it, and that drives the D4 UI. About 8–10 h, 3–4 of them on GPU;
  - (C) score behaviours by answer log-probability and run one more calibration. About 4 h, plus D3/D4 if it
    passes.

### Vision (`NORTH_STAR.md`)

- Goal 1: type a behaviour change in words, get updated weights back.
- Goal 2: a UI over the measured map.

### Decisions waiting for Shreyas

1. Goal 2: A, B or C.
2. Goal 1: write up now, or more helix2 runs first.

3. Direction (added Nov 11): `docs/DIRECTIONS.md` lists every candidate direction and proposes a lead one (a
   measured map, then testing whether an AI reader can predict it). Does it replace or join the two goals?

Do not start GPU work without his answer.

### To restart GPU work (Colab)

1. Redo the Colab sign-in (`06_OPERATIONS.md`, "Colab headless"): `google-colab-cli` 0.7.5 with
   `OAUTHLIB_RELAX_TOKEN_SCOPE=1`. Shreyas approves the link (Colab scope only) and pastes back the code.
2. `colab new --gpu L4 -s <name>`, then run `scripts/colab/setup_both.py` (clones the repo, installs, downloads the
   9B and 0.8B).
3. Upload `.env` to `/content/helix_probe/.env`. Keys never go in the repo.
4. Queue jobs with a script like `scripts/colab/queue_g1add.py` (`scripts/edit_job.sh` stages) or
   `queue_d2.py` (`discover.py`).
5. While anything runs: check in every ≤9 minutes (`send_later`). Workspace background jobs die between turns,
   and Colab reclaims idle runtimes.
6. Follow `WORKING_METHOD.md` §3 hard rules: download and push each finished run at once, verify it is in the
   commit, and update all four docs in the same turn.
7. Stop runtimes when idle. They cost about 2 units/h each; the balance was about 665 units on Nov 7 morning,
   check before starting.

### Key code

- **`bench/weights/edit.py`:** the Goal 1 driver.
  - Arms: unedited, random, scripted, mit, helix, helix2.
  - `--verdict-version 2` is the default.
- **`edit_worker.py`:** the guarded model box.
- **`edit_grade.py`:** the fresh-process grader.
- **`edit_items.py`:** the abilities and question sets.
- **`discover.py`, `discover_verify.py` and `panel.py`:** the Goal 2 loop, verification and 26-behaviour panel.
  The D2 fixes are marked "D2 fix".
- **Results:**
  - `results/edit/` (9B), `results/edit_08b/` (0.8B), `results/edit_s1b/` (baseline re-runs);
  - `results/discover/d1` and `d2`;
  - `results/edit_discarded_hooks/` (runs set aside after a bug, kept).
- **The VM (OCI, run by Aether)** was not used after Nov 6; its 0.8B job was replaced by the Colab 0.8B axis.

## Read in this order

| File | What it is |
|---|---|
| `docs/DIRECTIONS.md` | **Every direction the project could take** (Nov 11), rated, with the literature check. A proposal, not a plan. |
| `docs/FINDINGS.md` | **Plain-language summary** of what worked, what didn't, and what we discovered. |
| `docs/NORTH_STAR.md` | **The goal,** what counts as done, what a breakthrough would be. Short; read first. |
| `docs/GOAL2_CALIBRATION_RESULT.md` | **Goal 2's calibration result** (D1, D2), what it shows, and the options. |
| `docs/PROGRESS.md` | **Every step of both goals in one table:** status, where it ends, open decisions. |
| `docs/PLAN.md` | **The finite plan:** steps, arms, scoring, predictions, decisions, status. |
| `docs/JOURNAL.md` | What was decided and found, dated, newest first. |
| `docs/WORKING_METHOD.md` | How we go from a goal to results without drifting: crystallise, plan, execute, handle surprises and new directions. **§3 hard rules are strict.** |
| `01_CONCEPT.md` | What Helix Probe is, why, and the vision. Self-contained. |
| `10_INTERPRETABILITY_TRACK.md` | The weight-space track: MIT's work, our harness, results so far (section 12). |
| `02_STATE_AND_RUNS.md` | What's built and everything that ran before Nov 5. |
| `03_ANALYSIS.md` | What the FIND and ARC runs showed. |
| `04_PUBLISHING.md` | Candidate publishable results and references. |
| `05_NEXT_STEPS.md` | The older backlog (FIND, ARC). Superseded by `PLAN.md` while the north star is the focus. |
| `06_OPERATIONS.md` | How to run anything: the VM, Aether prompts, job scripts, Colab from a headless machine. |

**Private, kept out of this public repo,** in a bundle Shreyas holds (`helix_probe_private.zip`):
- `07_PRINCIPLES_AND_RULES.md` (his standing rules);
- `08_shreyas_verbatim.md` (his messages);
- `09_full_transcript_redacted.md`;
- `.env` (keys).

Ask him for it before changing anything. Its messages run to Nov 4; later direction is paraphrased in `JOURNAL.md`.

## The standing rules, briefly

- Lean but uncompromising; whiteboard-explainable; traceable; general.
- Evidence over exceptions.
- Every run has a stated question and a written prediction, and attempts a publishable result fairly.
- No experiments without a place in the plan.
- Keys only in the gitignored `.env`; the repo is public.
- Aether (the VM agent) never sets up cron jobs or timers, never kills or restarts processes unless told to, and
  never edits code.
- Update Shreyas every 10–15 minutes during long work.
- Don't rely on memory or other conversations; these files are the context.

## How to resume

1. Read `NORTH_STAR.md`, `PLAN.md` and the top of `JOURNAL.md`.
2. Check the plan's status line: the next step is whatever it says is waiting.
3. If the work needs Colab, the sign-in from `06_OPERATIONS.md` must be redone in your workspace (Shreyas approves a
   link and pastes back a code).
