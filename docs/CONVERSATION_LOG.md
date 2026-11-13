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
