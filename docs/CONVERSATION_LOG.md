# Research conversation log

*A living record of the research discussion: ideas, questions, answers, decisions, hypotheses and open threads, in order, so that a fresh session can continue where the last one stopped. It is updated after every exchange.*

*This repository is public. The log therefore paraphrases the discussion; it holds no verbatim messages or transcripts, and no personal or career matters. Earlier history is in `JOURNAL.md`.*

Tags: **[decided]** · **[open]** · **[idea]** · **[finding]** · **[correction]**

---

## 2026-11-11 to 11-12: from directions to a literature survey

- [decided] The project's core aim is a **white-box reconstruction of a black-box network**: a model that predicts, not a correlation table. What exactly that means is to be learned from the field, not invented.
- [decided] Run a large literature survey to learn how the field talks about and measures this:
  - what the field is trying to build, and why;
  - what blocks it;
  - its methods, measures and benchmarks;
  - shortcuts we can reuse.

  The point is that the eventual paper uses measures the domain recognises.
- [finding] Survey done: 193 core entries (`literature/core/`) and a synthesis (`literature/SYNTHESIS.md`).
- [correction] The synthesis was first written as a verdict on our idea. Shreyas: the survey's purpose was to understand the domain, not to judge the idea. The discussion was reopened on that basis.

## 2026-11-13: what a construction is

- [finding] What the field calls the object we want:
  - a **causal abstraction**: variables, the mechanisms computing them, and an alignment saying where each lives in the network;
  - looser forms: a replacement model, or an executable program.

  It is judged by three questions, in increasing strictness:
  1. same outputs when run in place of the network;
  2. same response to interventions (IIA, ablation prediction);
  3. same internal computation (Jacobian / internal-state agreement).
- [finding] What real constructions look like (details in the 11-13 discussion, sources in `literature/core/`):
  - math equations: modular addition (arxiv-2301.05217), group composition (arxiv-2302.03025);
  - Python code: MIPS (arxiv-2402.05110);
  - a role graph: IOI (arxiv-2211.00593);
  - a small causal model aligned to an LLM: Llama addition (arxiv-2605.01148);
  - rebuilt weights: Curve Circuits;
  - per-prompt attribution graphs.

  LLM constructions are always behaviour-sliced, never a whole model. Variables are often continuous (Fourier features, manifolds), so constructions read more like math than if-statements.
- [finding] How people make them by hand:
  1. a narrow task;
  2. locate the relevant components (ablation/patching);
  3. **guess the basis** (Fourier, representations, symmetry);
  4. write the algorithm;
  5. verify (restricted/excluded loss, IIA, substitution).

  Step 3 is where human insight goes, and the part a constructor would automate.
- [finding] Goodfire's line of research, in seven threads:
  1. SAEs as a product;
  2. geometry/manifolds;
  3. "neurons are already clean";
  4. parameter decomposition;
  5. interpretability as engineering (monitors, rewards);
  6. science from bio models;
  7. agents/throughput.

  Their stated hierarchy is ontology → algorithm → behaviour. The algorithm level is what they name as open.
- [decided] **We are building the constructor**: a method that produces constructions, not one hand-made construction. The first paper needs only one solid construction made *by* the constructor. Generalising it comes later.
- [decided] Start with a smaller network rather than a full LLM, though an LLM remains the dream.
- [decided] **Replicate before exploring (K0).** Validate on networks with known answers (modular addition first), with the answer hidden from the reader. Rationale: on an unknown network there is no way to tell whether the method is wrong.
- [idea] **K1, the reader interface:** what we give the LLM, what we ask, and what response we want, treated as an experiment. Ladder:
  1. weights alone;
  2. weights plus a bare question;
  3. richer prompts;
  4. with a code sandbox, logging which computations it chooses to run.

  The last tests whether pre-training taught it "decoding" computations.
- [idea] **K2, strengthen reading by fine-tuning** a pre-trained LLM (Shreyas: "some form of fine-tuning, usually RL but not necessarily"). Readings that carry a checkable prediction would give a label-free reward.
- [idea] **K3, a loop**: read, hypothesise, test the mapping, assemble, test the algorithm, repair. Fresh context each generation; continuity through a state document that any agent can advance.
- [open] Shreyas: do **not** settle on the loop, the roles or the agents yet, and do not build the loop first ("that would just be building another Helix version").
- [idea] Slicing must avoid seams. Slice along the network's own units (a whole neuron = its W_in row + W_out column; a whole head = Q, K, V, O). Use overlapping windows. With code access, the reader can compute joined objects itself.
- [idea] The reader might **query the weight store itself** once it has an initial map (fetch regions, filter by criteria) instead of being fed slices. A candidate, not decided.
- [decided] Tools = the LLM writes and runs its own code against the weights. It builds its own probes rather than using a fixed toolkit. LLMs can't estimate numbers reliably, so calculation goes through code.
- [finding] "Running the network gives the answer away" is less fatal than it seems. Execution reveals *what* the network computes; the construction is about *how*, and the field's tests score the how. Plan:
  - reading experiments: no execution, task never named;
  - construction experiments: execution allowed.

  The bigger leak is the LLM's memory of the literature, so add a prior-only arm (task named, no weights) and targets with no published mechanism (Tracr, variants).
- [decided] The constructor's model is written in Python, so it can run (and be shown in text).
- [correction] An earlier claim that "LLMs fine-tuned to read weights already exist" was misleading. Weight Oracles, LoRAcles and Diff Interpretation Tuning use learned encoders, continuous tokens, or self-description, never weights pasted as text. K2 has no known prior. Also: Weight Oracles really does use continuous tokens (the full text confirms it), which reverses an earlier removal.
- [finding] WSP follow-up survey: 25+ entries in `literature/wsp/`. Summary: `literature/wsp/K1_STATE_OF_ART.md`.
- [decided] **First build: the Weight Reading Lab**, a local browser app for K1 by hand. Fun to use, styled after Avy, not limited to a few demos. See `WHAT_WE_ARE_BUILDING.md`.
- [idea] The "agentic interpreter" vision is recorded separately as non-current: `ideas/SCIFI_AGENTIC_INTERPRETER.md`.
- [decided] Documentation rule: the repo is a living map. Every idea, question, decision, finding and build request is written down after each exchange, so a fresh session can continue.
- [decided] Lab details:
  - runs locally in the browser;
  - styled after Avy;
  - specimens with hidden answers;
  - select by scanning a heatmap or by whole units (seam-free);
  - leak switches (architecture / input meaning);
  - text-only vs python-sandbox modes;
  - one-click controls (shuffled / untrained / permuted);
  - a notebook with grading and side-by-side comparison.
- [finding] DeepSeek V4.1 Flash, our reader, is on record as a weak raw-text reader: 0/8 in the andsalazar replication, 0–11% plus non-answers in the EEG paper. Expect it to run out of budget copying weights. The python mode is the likely path to useful results.
- [finding] Our mod-add target's attention query weights are nearly rank-1 (one sign pattern per head). Attention does little here, as in Nanda's analysis. The embedding's Fourier power is 94% in frequencies {8, 23, 25, 11, 22}.
- [finding] First live lab results with DeepSeek V4.1 Flash: XOR correct (text mode); parity described correctly (python mode, blinded); MIT's Breakout policy correct at 97% (MIT's original prompt, with channel names). The repo's earlier zero scores for DeepSeek came from the shape task, with smaller budgets. The next tests are the blinded and shuffled versions.
- [finding] Blinded test (Game policy a9f5, no context, neutral question, text mode):
  - At 32k output it ran out of budget.
  - At 64k it answered "MNIST-style digit classifier, 80%": wrong (Breakout). It did notice real spatial structure (near-zero border rows, localised clusters), but it miscounted the inputs (485 rather than 500) and filled the gap with a dataset prior.
  - The shuffled control declined to name a task (and miscounted: 498).

  So text-mode success depends mostly on the context text. The next test is blinded python mode.
- [decided] Handoff: `handoff/00_START_HERE.md` holds the goal, the constructor spec, current results, next steps and a map of the docs. The Nov 8–11 material below it is marked superseded.
- [correction] The K-numbers are not a progression. The **main direction** is the constructor: replicate, make several networks fully interpretable, then an LLM behaviour. K2 (fine-tuning or RL a reader) is a **side direction**, out of scope for the main build.
- [decided] A zero-shot attempt by a separate, more capable agent, on branch `constructor-attempt`:
  - goal and bar given, no architecture;
  - persistent;
  - short live experiment cycles;
  - frequent commits;
  - integrated into the lab;
  - simplicity as guidance.

  The prompt is kept privately because it contains the key.

## 2026-11-13 (branch `constructor-attempt`): the constructor attempt

*Entries from the separate agent session working on the branch `constructor-attempt`. Experiments are in `EXPERIMENT_LOG.md`.*

- [decided] The form of a construction: a standalone Python file with `model(x, iv)` (named variables registered through `iv`) and `ALIGN` (the sites where each variable lives). It cannot see the weights, so it must be a compact program with measured constants. Reason: this is what makes "the network is the network" impossible to submit, and it makes description length measurable.
- [decided] The alignment map is affine and is fitted by the judge on a fit split, then tested on held-out inputs. The reader declares the variables and their sites. Reason: causal abstraction needs a declared, restricted map class; fitting it by regression removes a burden from the reader and treats every construction the same way.
- [decided] The judge's tests: behaviour; substitution; removal against a random subspace; interchange (probe-read, written along the alignment directions); off-manifold edits. A site passes or fails as a unit; stages group sites; "complete" means every stage has a verified site.
- [finding] Behaviour agreement separates nothing: an oracle, a wrong-frequency construction and a lookup table all agree with the mod-add network on 100% of inputs. Substitution, removal and interchange separate them cleanly (E0).
- [finding] The subspace tests alone (keep or remove the named subspace) can be passed by regressors that mean nothing, because any regression onto low-rank activations returns directions inside the dominant subspace. Substitution with the construction's own predicted values is the test that cannot be passed that way.
- [finding] Blinded and given code, DeepSeek V4.1 Flash found the mod-add task and the key frequencies {8, 11, 22, 23, 25} from `W_E` and `W_U` in 7 steps. It named the Fourier mechanism from memory first and then confirmed it in the weights (E1). The prior-only control is therefore needed to show what memory alone gives.
- [finding] Left to itself the reader does not submit: it tried to understand the attention stage exactly before testing anything, and used all 40 steps (E1).
- [decided] The loop enforces "submit early, improve stage by stage" through the prompt and reminders. No roles or agents are added.
- [open] The attention stage of mod-add is not explained by single-token Fourier variables (the attention weights vary strongly with the inputs). Whether the reader can construct it is open; Nanda et al. do not explain it either.

### 2026-11-13 evening (branch `constructor-attempt`, continued after a session interruption at about 15:00)

- [instruction from the owner, 18:50] Persist everything constantly: commit and push at every step, so that another session can continue from GitHub alone. Stay on `constructor-attempt`; never touch `main`. → Every substep is now pushed with `push.sh` (checks the branch and that the key is not in any tracked file), and a background loop pushes in-flight run folders every 4 minutes.
- [instruction from the owner, 19:13] Document every step, decision, plan, motivation, hypothesis, success and failure. Build something usable at each step, not only reports: the owner wants to run the constructor himself in the lab and see it work, possibly on new networks. Look at `main` for a sense of progress there without copying it. Lesson from `main`: be specific about what is asked of the reader (asked "what does it do" it described actions; asked "what game" it named the game); treat this as information to test, not as a given.
- [note] What `main` found meanwhile (`docs/K1_LADDER_RESULTS.md` on `main`, read only): in text mode the reader cannot read 17K weights and fills gaps from dataset priors; in python mode it recovers structure blind (grid layout, actions, "an RL policy") and rejects shuffled controls; naming the exact game needs input semantics; mod-add's mechanism was read from weights alone with the frequencies 8, 11, 22, 23, 25. That agrees with this branch: code access is how the reader reads, and asking for mechanism works better than asking for a name.
- [decided] Judge v2 then v3 (E5, E6). Motivation: judge v1's random-subspace gate and coordinate edits were tuned to one trained, redundant network and rejected a correct construction of a compiled network. v3 gates on substitution, necessity, compactness against PCA, whole-site interchange (90%), and partial/edit tests (50% of changed cases). Rule kept throughout: every change to the judge is re-checked against the three calibration constructions on mod-add (oracle passes, wrong frequencies fail, lookup table fails).
- [decided] Splitting a variable into parts must never raise the bar. Reason: in dev run 4 the reader split the Fourier variable into single cosines and sines, as the prompt advised, and failed a 90% bar that the lumped variable did not face.
- [decided] Freeze before held-out runs. The constructor (prompt, tools, judge, sites) is frozen at commit `391998c0`. Development networks: Boolean nets, `modadd_p113`, `tracr_hist`. Held out: `modmul_p113`, `tracr_reverse`, `tracr_first_match`, `tracr_count_greater`, and anything trained later (`modsub_p113` is training). No edits to `judge.py`, `constructor.py`, `kernel.py`, `nets.py` while official runs are in flight (E4 broke this rule once and the runs had to be discarded).
- [finding] The constructor generalises to compiled networks it was not tuned on: `tracr_reverse` (4 layers) and `tracr_first_match` reached VERIFIED AND COMPLETE blinded, in 9 and 23 steps (E8, being written as runs finish).
- [finding] On a fixed input length, the parts of a compiled program that only react to length are constant. The reader said so correctly for `tracr_reverse` ("layers 0-2 are input-independent"), and the judge ignores constant sites. So `tracr_reverse` tests routing by attention, not the length computation. This is a limit of the targets, noted so nobody over-reads "9 of 9 stages".
- [finding] Level 3 is mixed (E7): the construction predicts interventions on its own variables through the nonlinear part of the network far better than attribution patching (100% against 36% at the mod-add embedding), and beats the behaviour-only, statistics and prior-only baselines everywhere; but on arbitrary subspace interventions attribution patching wins (91% against 82%) and is exact after the MLP, where the network is linear.
- [hypothesis] The attention stage of mod-add stays unexplained because its true variables are products of an attention weight and a token's Fourier features, whose effect passes through the ReLU layer; a compact model of how the ReLU layer treats mixed states is what is missing. Not yet tested beyond the oracle failing there (E0) and uniform attention keeping 78% of decisions (E3).
- [open] MIT's game policies cannot be judged: the released logs hold weights and prompts but no environment or states, so there is no input set. Options: write approximate grid environments from the prompt's description (off-distribution risk), or leave them out and say so.
- [plan, 19:30] (1) Collect the official batch into a results table as runs finish. (2) Make the lab show a gallery of verified constructions so the owner can open each one. (3) Let the owner ask the finished run a specific question (the interface lesson from `main`). (4) More held-out networks. (5) Second mod-add replicate and prior-only replicates on the frozen version.
- [finding, 19:55] Mod-add's attention pattern matters and is not a side detail: copying the whole attention pattern in from another input changes the decision in 45% of cases, to an answer that is neither input's. (Copying `attn_out` or `resid_mid` whole gives the source's answer in 100% of cases, as it must.) So a verified attention stage needs a model of how the ReLU layer responds when the two tokens' features are mixed with the wrong weights. That is the missing piece named in the hypothesis above, and no compact form of it is known. Decision: leave the attention stage of mod-add as an explicitly open stage; do not spend more of this session on it.
- [prepared, 19:55] Judge v3.1 is written as a patch and tested on a copy against the calibration set (oracle lumped and split: 3 stages; lookup table and wrong frequencies: 0; compiled oracles unchanged). It is applied only after the E8 batch ends.

### 2026-11-14 (branch `constructor-attempt`, after the second interruption)

- [instruction from the owner, 00:34] Continue; keep committing, pushing and writing down the thinking, because interruptions happen.
- [decided] Do not retrain `modsub_p113` in this session: 1.5 hours of CPU that slows every judge call, for a network of the same family as two already done. The command is in the handoff.
- [decided] Use MIT's experiment-5 Breakout network as the game policy, because it is the only MIT game network whose environment is public. Reason for trusting the input set: the network's score per step in my reconstruction matches MIT's (0.069 against 0.070).
- [finding] Blinded, the reader constructs the game policy completely and does not name the game; asked specifically, with the grid layout given, it names Breakout and the meaning of each variable (E12). This matches what the owner saw on `main`: reading and naming are separate questions, and naming needs input semantics. Built into the lab as the Ask box.
- [finding] Five blinded runs on mod-add all end at the same 3 of 4 stages. Two runs on mod-mul: one complete, one 3 of 4. Compiled networks and the game policy: complete every time. Prior-only: 0 stages in 4 of 4 runs.
- [finding] Attribution patching scores 0% on interventions at the game policy's first hidden layer (the next layer saturates) where the construction scores 100%, and 100% at the second hidden layer (linear to the output). The pattern is the same on every network: the construction wins where the path to the output is nonlinear, attribution patching where it is linear.
- [open] Whether "complete" on mod-mul is reliable with a larger step budget. Whether any compact account of mod-add's attention stage exists.
