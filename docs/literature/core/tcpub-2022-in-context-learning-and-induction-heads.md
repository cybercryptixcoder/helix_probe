# In-context Learning and Induction Heads

- **Key:** tcpub-2022-in-context-learning-and-induction-heads
- **Authors / organisation:** Catherine Olsson, Nelson Elhage, Neel Nanda, et al.; Anthropic
- **Date:** 2022-03
- **Link:** https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html
- **Kind:** paper
- **Read from:** full text (main body and methods; appendix on model details only partly retrieved)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors want to test whether induction heads, a circuit identified in tiny attention-only models, are the main
mechanism behind in-context learning (ICL) in transformers of all sizes. The larger aim is to show that
mechanistic findings in small models can explain a macro capability of large ones, and to study sudden capability
shifts during training ("phase changes") as a safety concern. They are explicit that most evidence for large models
is circumstantial.

## What they studied
34 decoder-only transformers with many training checkpoints: small attention-only models (1-6 layers, width 768,
12 heads, ~10B training tokens), small models with MLPs (1-6 layers), full-scale models from 4 layers (13M
non-embedding parameters) to 40 layers (13B), and "smeared key" architectural variants. Units: attention heads,
the previous-token/induction-head circuit, and whole-model loss curves.

## How they did it
They define an ICL score as loss at token 500 minus loss at token 50, averaged over the data. They define an
induction head behaviourally on repeated random token sequences: a prefix-matching score (attends to the token
after an earlier copy of the current token) and a copying score (its output raises the attended token's logit),
each from 25-token random sequences averaged over 10 examples. Using 200 snapshots for 12 small models and ~15 for
6 large models, they track per-token losses on 10,000 examples of 512 tokens and run PCA on those loss vectors to
trace training trajectories. They then build six lines of evidence: (1) co-occurrence of ICL and induction heads in
time; (2) co-perturbation, adding a smeared-key change that makes induction heads easy to form and checking ICL
moves with it; (3) test-time ablation of heads (over 50,000 ablations, small models only, pattern-preserving);
(4) anecdotes of induction-defined heads in the 13B model doing translation and abstract pattern completion;
(5) mechanistic reverse-engineering of the circuit in small models; (6) continuity of all signatures across scale.

## What counts as an explanation here
A named circuit (previous-token head K-composing with an induction head) tied causally to a capability, supported by
a portfolio of evidence types graded from correlational to causal to mechanistic. The explanation is partial: it
claims induction heads may account for most ICL, not all of it.

## How they judged success
ICL score (nats); loss-curve bump and PCA trajectory shifts; prefix-matching and copying scores, validated against
OV and QK eigenvalue measures in small models; head-ablation effects on the ICL score and projection of ablation
effects onto the phase-change direction; controls include one-layer models (which cannot form induction heads) and
architecture interventions. No formal statistics; single training run per model.

## What they found
ICL and induction heads appear together in a narrow window at roughly 2.5-5B training tokens; ICL improves from
under 0.15 to about 0.4 nats, with over 75% of final ICL forming in that window, and one-layer models show neither.
Smeared keys give one-layer models ICL and make deeper ones get it earlier. Ablating induction heads in small
attention-only models removes much of ICL while most other ablations do not. Induction-defined heads in the 13B
model also translate word-by-word and complete abstract patterns (one put about 65% of attention on the right
positions). A cited replication found idealised previous-token scores recovered 99% of a loss difference and
idealised induction scores about 65%.

## Limitations and open problems they name
Large-model evidence is correlational (few checkpoints, no ablations due to cost); confounds such as other
mechanisms forming at the same time; ablations hard to interpret with MLPs; anecdotal generality examples; single
runs; several unexplained phenomena (odd heads, anti-copying prefix-search heads, loss spikes).

## What we take from it
A methodological template: when a mechanism cannot be proven at scale, triangulate with several distinct evidence
types and say explicitly how strong each is. The behavioural head scores on random repeated tokens are a cheap,
reusable detector, and the check that they agree with weight-based eigenvalue measures is a model for validating a
weight-derived prediction against behaviour. Training-time co-perturbation (change architecture, predict the
behaviour shift) is a strong test of a predictive model.

## Tags
unit: head, circuit, whole-model
form: graph, description
method: ablation, weight-analysis, other
eval: ablation, prediction/simulation
goal: understanding, science, safety/auditing
