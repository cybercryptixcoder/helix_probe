# Opening the AI Black Box: Program Synthesis via Mechanistic Interpretability (MIPS)

- **Key:** arxiv-2402.05110
- **Authors / organisation:** Eric J. Michaud, Isaac Liao, Vedang Lad, Ziming Liu, Anish Mudide, Chloe Loughridge, Zifan Carl Guo, Tara Rezaei Kheirkhah, Mateja Vukelić, Max Tegmark; MIT, IAIFI, Harvard
- **Date:** 2024-02
- **Link:** https://arxiv.org/abs/2402.05110
- **Kind:** paper
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors want to automate the full path from a trained network to a human-readable, verifiable program: train a
network on a task, then mechanically extract the algorithm it learned as Python code. Unlike LLM-based program
synthesis, this needs no human-written code as training data. The larger motivation is trustworthy AI: if learned
algorithms can be turned into code, the code can be formally verified instead of trusting the network.

## What they studied
Small RNNs whose state update and output functions are MLPs, trained on a benchmark of 62 algorithmic tasks
(integer or bit lists of length 10 or 20 mapped to output lists: bitwise ops, parity, cumulative sums, delayed
recall, modular arithmetic, simple Newtonian simulations, and so on). Unit of analysis: the whole RNN, its weights
and its hidden-state space.

## How they did it
(1) Train an RNN. (2) Architecture search over hidden size and MLP widths/depths (about 75 million configurations)
to find the smallest network reaching 100% test accuracy. (3) Simplify the weights by removing symmetries with a
fixed sequence of normalisers: whitening, Jordan normal form, Toeplitz, de-biasing, quantisation. (4) Discretise
the hidden states: a Boolean autoencoder clusters them into 2^b states (b bits), or an integer autoencoder finds a
lattice via GCD-based or linear lattice finders. (5) Fit the discrete update and output maps with symbolic
regression: Boolean functions as disjunctive normal form (or bit-sum if symmetric), integer functions by linear
regression or the AI Feynman brute-force solver. (6) Insert the formulas into a template Python loop. The baseline
is GPT-4 Turbo writing a program from input/output examples with chain-of-thought, three attempts per task.

## What counts as an explanation here
A short Python program equivalent to the network on the task, treated as a finite-state machine (bits or integers)
with symbolic update rules. It is complete for the task, fully predictive, and can be formally verified.

## How they judged success
A task counts as solved only if the extracted program reaches 100% accuracy. Count of solved tasks versus the GPT-4
Turbo baseline (success if any of three attempts works). Formal verification in Dafny for one case (the binary
adder, for all length-10 inputs).

## What they found
MIPS solved 32 of 62 tasks; GPT-4 Turbo solved 30; 13 tasks were solved by MIPS but not GPT-4, so the methods are
complementary. Sixteen tasks needed only hidden dimension 1; the largest needed was 81. The binary adder was
recovered as a ripple-carry adder and verified.

## Limitations and open problems they name
Integer extraction breaks when the network's lookup tables are noisy (e.g. a difference-of-absolute-values task).
The finite-state assumption fails when the RNN uses continuous representations (e.g. majority tasks). The method is
limited to RNNs and to bit/integer data; scaling to larger networks and harder tasks is open.

## What we take from it
The closest existing pipeline to our goal: weights to executable predictive program, with exact accuracy as the
criterion. Reusable pieces: shrink the network first (minimal sufficient architecture), canonicalise weights by
removing symmetries before reading them, discretise hidden states, then symbolic regression. The pass/fail
criterion (program reproduces 100% of outputs) and an LLM-from-examples baseline are a ready evaluation design. A
warning: it fails exactly where representations are continuous or noisy, which is the normal case in real models.

## Tags
unit: weights, whole-model
form: program
method: weight-analysis, decomposition, other
eval: prediction/simulation, benchmark
goal: understanding, safety/auditing
