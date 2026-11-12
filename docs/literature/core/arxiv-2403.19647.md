# Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models

- **Key:** arxiv-2403.19647
- **Authors / organisation:** Samuel Marks, Can Rager, Eric J. Michaud, Yonatan Belinkov, David Bau, Aaron Mueller
- **Date:** 2024-03
- **Link:** https://arxiv.org/abs/2403.19647
- **Kind:** paper
- **Read from:** full text (some tables only partly visible; see notes in findings)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Circuits built from heads or neurons are hard to interpret because those units are polysemantic, which limits their practical use. The authors wanted circuits made of fine-grained, human-interpretable units (sparse autoencoder features), and wanted to show such circuits are useful downstream: a person should be able to read a circuit and edit the model to remove an unwanted behaviour, even without data that isolates it.

## What they studied
Pythia-70M with SAEs the authors trained for every sublayer (embeddings, attention, MLP, residual stream; ReLU encoder; dictionary 64x model width), and Gemma-2-2B with Gemma Scope SAEs (JumpReLU, 8x width, all sublayers except embeddings). Units: SAE features plus one SAE error node per sublayer, and edges between them.

## How they did it
They treat SAE features and SAE error terms as nodes of a causal graph, so that the decomposition of the model's computation is exact (the error node holds whatever the SAE misses). Node and edge importance is estimated with linear approximations to indirect effects: attribution patching (a first-order Taylor approximation of patching) and integrated gradients with 10 steps where the linear approximation is poor (early layers). Nodes and edges above thresholds are kept. For contrastive tasks they patch from a counterfactual input; for single inputs they use zero ablation. They studied four subject-verb agreement structures (simple, within relative clause, across relative clause, across prepositional phrase), compared feature circuits with neuron circuits, had crowdworkers rate feature interpretability, and introduced SHIFT: a human inspects a classifier's feature circuit, ablates features judged irrelevant to the intended task, then optionally retrains the head. They also clustered Pile contexts into automatically discovered behaviours and ran circuit discovery on each cluster.

## What counts as an explanation here
A sparse feature circuit: a causal graph of labelled SAE features (plus error nodes) with edges, explaining a behaviour on a dataset. Partial by design (error nodes absorb what is not explained). It supports editing and qualitative prediction, but labels are human-assigned.

## How they judged success
Faithfulness (circuit performance relative to full model, with the rest mean-ablated) and completeness (performance after ablating the circuit) as a function of circuit size; comparison with neuron circuits at equal size; crowdworker interpretability ratings (circuit features vs random features vs neurons); on Bias in Bios (where gender perfectly predicts profession in training), profession accuracy, gender accuracy and worst-group accuracy of a linear probe after SHIFT, against an original classifier, random ablation, a concept-bottleneck-style baseline, neuron and feature "skylines" and an oracle trained on balanced data.

## What they found
About 100 feature nodes (Pythia) and 500 (Gemma) explain most of the agreement behaviour; neuron circuits need roughly 1,500 (Pythia) and 50,000 (Gemma) neurons for half the performance. Ablating a few feature nodes removes the behaviour, while neurons need hundreds or thousands. Crowdworkers rated features more interpretable than neurons, and circuit features more than random features. Case study (agreement across a relative clause): both models detect subject number, detect the clause start, carry number across the clause and promote matching verbs; Gemma also uses noun-phrase number trackers. SHIFT ablated 55 of 67 Pythia circuit features and 43 of 46 Gemma features; the paper reports it nearly removes reliance on gender, and with retraining the Gemma probe reaches worst-group accuracy close to the oracle (the visible table rows suggest 92.9 vs. an oracle of 93.1, but column labels were cut off in what I could read, so treat these as unconfirmed). Random feature ablation had essentially no effect. Thousands of cluster-level circuits were produced automatically.

## Limits and open problems they name
Depends on costly SAE training; anything the SAEs miss stays uninterpretable (error nodes); evaluation is mostly qualitative apart from the classifier application; evaluating dictionaries and circuits without downstream tasks is hard; feature labels are subjective.

## What we take from it
The "error node" device: keep the reconstruction residual explicitly in the graph so the explanation is exact and its unexplained share is measurable. That is a direct model for a white-box reconstruction that reports how much is not yet explained. Attribution patching / integrated gradients give cheap linear estimates of interventions at scale. SHIFT is a strong downstream test of an explanation: if you understand it, you can remove a behaviour without targeted data. Neuron versus feature circuit size is a good basis-quality metric.

## Tags
unit: feature | circuit
form: graph | dictionary
method: SAE | attribution | patching | ablation
eval: faithfulness | completeness | human-rating | downstream-task
goal: understanding | control/editing | debugging
