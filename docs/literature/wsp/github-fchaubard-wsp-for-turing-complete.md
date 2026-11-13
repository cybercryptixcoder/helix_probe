# Weight-Space Programming and Gradient Optimization on Nonconvex Algorithmic Tasks

- **Key:** github-fchaubard-wsp-for-turing-complete
- **Authors / organisation:** Francois Chaubard (Stanford address in the paper) and "Astra" (GPT-6 Astra, credited as
  AI research collaborator)
- **Date:** 2026-11-07 (PDF creation date; dated editions of 2026-11-06 and 2026-11-07 are kept in the repo)
- **Link:** https://github.com/Fchaubard/WSP-for-turing-complete (paper: `paper.pdf`; blog:
  https://fchaubard.github.io/weight_space_programming.html)
- **Kind:** paper (research preprint, not peer reviewed)
- **Read from:** README, `REPRODUCIBILITY.md`, `literature/related_work.md` in full; `paper.pdf` (88 pages): main
  text (sections 1–7) in full, and from the appendices A.1 (feedback and gradient controls), A.5 (prompts and
  traces, including the full example prompts), A.6 opening, A.10 (what the responses encode), H opening, J (pilot) and
  the start of K. **Not read:** the remaining appendices (proofs, sequence and scalar constructions, stress tests,
  branching machines), `writer/` prompt and reply files, `focus/` directories, CSV outputs, the blog post.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The paper treats an LLM as an optimiser: given a fixed small network, initial weights and a few labelled examples,
can it write weights that fit the examples and, more importantly, keep computing the right rule outside the
training range? It compares this weight-space programming with gradient-based optimisers on the same graphs, starts
and labels. A second experiment lets the LLM choose the architecture as well. The larger aim is to understand how
an optimiser should find weights for small algorithmic networks, and whether an LLM's prior knowledge of rules
gives better extrapolation than local descent.

## What they studied
- **Writer:** GPT-6 Astra (service alias `gpt-6-astra`), fresh isolated sessions, no tools.
- **Targets:** ten tasks (square, sine, positive self-power x^x, tanh, addition, subtraction, running sum, sorting
  four numbers, Fibonacci, triangular numbers) on 29 nonconvex task–architecture pairs with 3–50 trainable
  coefficients: one-hidden-layer ReLU with a direct path (widths 1, 4, 16), two-input ReLU MLPs (widths 1, 2, 4),
  linear RNNs (with input, or autonomous), and four-wire residual ReLU sorters. Three random Xavier starts each:
  87 settings.
- **Baselines:** full-batch gradient descent (800 steps with line search), then L-BFGS; Adam then full BFGS;
  trust-region least squares; L-BFGS from Xavier; pooled-label gradient controls; 14 pipelines in all.
- **Unit:** whole network, judged by its outputs.

## How they did it
1. For each task and start, one request covers all sizes at once and gives the graph, flattening order, initial
   weights, intended input range and 12 labelled central examples (indices 0–8 for integer sequences), either with
   examples only or with the formula too. The model returns only JSON arrays of numbers (60 calls, 174 arrays).
2. Iterative WSP: starting from that reply, up to three revisions per size in fresh sessions, each showing the
   original task, current weights, training and development loss, RMSE, exact counts and up to three worst examples
   per split. A revision is kept only if development loss falls (training loss breaks ties); a size stops when exact,
   after two consecutive rejections, or after three attempts (161 revision calls).
3. Gradient baselines start from the same Xavier weights and the same training labels; a control gives them all
   development labels too.
4. Evaluate on a fresh central set and on an outer extrapolation set ([-10,-3] and [3,10]; indices 17–32 and 33–64
   for sequences); count exact binary64 matches and RMSE.
5. Certify nonconvexity of every training objective with an explicit midpoint witness in exact rational arithmetic;
   for the width-1 scalar cases compute the global training optimum exactly.
6. Architecture choice: 30 further requests with only examples, input shape and domain; the model returns a graph
   from a declared operator library (affine, ReLU, tanh, sigmoid, products, recurrence, convolution, attention; at
   most 64 nodes and 4,096 coefficients) plus coefficients and a short construction note; extrapolation primary,
   resource cost secondary.

## What counts as an explanation here
Not an interpretability study. The returned weights are checked as programs: the authors read some returned arrays
to see which computation they encode (for example all width-2 arithmetic replies implement ReLU(t) - ReLU(-t)) and
test exact symmetry (odd/even) of the represented functions.

## How they judged success
Median scaled RMSE on training, central and outer sets; number of settings with every outer output exactly equal to
the binary64 reference; summed raw outer RMSE across task means (14-pipeline ranking); pairwise win counts over 87
settings; reaching the certified global optimum within 1e-10; for architecture trials, executability, exactness,
coefficient storage, live memory and operation counts.

## What they found
- Both examples-only WSP procedures are fully exact on the outer set in 30 of 87 settings; no gradient pipeline is
  fully exact in any.
- One-shot examples-only WSP beats plain gradient descent on outer RMSE in 75 of 87 settings and GD+L-BFGS in 75;
  iterative in 78 and 77.
- Iterative WSP ranks first by summed raw outer RMSE (about 2.03e9 vs 1.06e12 for one-shot), driven mainly by
  Fibonacci; but the median scaled outer error rises from 0.057 to 0.235 with examples only. Iteration trades
  extrapolation for central fit (e.g. width-16 square networks move all hinges into [-3,3]).
- WSP rarely reaches the certified training optimum (1 of 12 one-shot examples-only; 0 iterative), whereas
  trust-region least squares does in 5; least squares started from WSP weights reaches it in 12 of 12.
- Returned scalar networks are never exactly odd or even one-shot; after iteration some are (sine 8/18, square
  11/18, tanh 8/18).
- Architecture choice: 28 of 30 proposals execute, 21 match every outer reference; square uses one product node with
  zero stored coefficients; two self-power proposals invalid; no proposal used convolution or attention.

## Limits and open problems they name
Tiny networks and ten deterministic tasks; no matched compute or pretraining; examples-only prompts still disclose a
task-specific graph and range, so familiar-rule recognition may drive success; sizes within a request share
context; development set is used for both feedback and selection; aggregate raw RMSE is dominated by large-valued
targets; the hosted alias may change; the internal procedure behind the numbers is unobserved. The repository name
does not imply a solver for all computable functions.

## What we take from it
- **Warning for K1:** this is writing, not reading; success is plausibly rule recognition from labelled examples plus
  a disclosed graph. A reading study must separate "recognises a familiar function" from "reads the weights".
- **Format reference:** weights exchanged as flat JSON arrays with a stated row-major flattening order and full
  binary64 repr; replies restricted to numbers only (no explanations), so no reasoning text exists to audit.
- **Method:** exact-rational checks of returned weights (symmetry tests, nonconvexity witnesses, certified optima)
  are a rigorous way to say what a weight array computes without trusting sampled tests.
- **Measure:** report both exact-match counts and RMSE, and both central and extrapolation splits; they rank
  methods differently.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** no reading task. Writer: gpt-6-astra (reasoning effort recorded per
  call but its value not stated in what was read; one later request in an appendix is described as medium effort).
  Scores as above.
- **Target networks:** 3–50-coefficient ReLU MLPs, linear RNNs and residual ReLU sorters, initialised Xavier-uniform
  (biases zero), to be fitted to ten algorithmic targets.
- **How the weights were presented:** text; per size variant, one flat list of initial weights in full binary64
  repr (about 17 significant digits), with the flattening order stated in words (e.g. A row-major, then b, then v);
  labelled examples as a JSON list of [input, target] pairs. Replies: JSON array of arrays, one per size, numbers
  only. Token counts per prompt not stated; 198,446 output tokens across the 161 revision calls.
- **Prompt:** public in the paper (Appendix A.5) and in `writer/` and `focus/iterative/`. Structure: you are writing
  coefficients in binary64; the variants are size versions of one unknown map; the input domain; the labelled
  observations; the primary objective (half mean squared scaled error) and the secondary aim of exact outputs on
  unseen inputs; permission to infer a rule; no tools or files; return only JSON of the stated shape with no
  expressions, code or ellipses; then per variant the coefficient count, flattening order, the forward equations and
  the initial weights. The formula condition adds the target rule. Revision prompts repeat the original task and
  add incumbent weights with diagnostics as JSON.
- **Access regime:** no tools, single reply per session; iterative condition adds up to three feedback rounds with
  training/development diagnostics, never test scores.
- **Controls:** examples-only vs formula; matched initial weights and labels across methods; pooled-label gradient
  control; WSP-then-least-squares; Xavier initial array scored; nonconvexity witnesses.
- **Failure modes observed:** extrapolation worsens under iterative revision even as development loss falls; wrong
  coefficient count in one proposal; invalid graphs for self-power in architecture choice; returned networks miss
  exact symmetries of the target; poor fits on non-representable targets (square, sine, self-power).
- **Prompt or format choices that helped or hurt:** an earlier extrapolation-first prompt (Appendix H) is reported
  separately from the training-loss-first prompt; supplying the formula changed little (30 fully exact settings in
  both conditions). No reading-format comparison.

## Tags
unit: weights | whole-model
form: program
method: agent | weight-analysis | other
eval: benchmark | prediction/simulation
goal: science | evaluation-of-methods
