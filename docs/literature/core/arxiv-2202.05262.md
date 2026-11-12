# Locating and Editing Factual Associations in GPT (ROME)

- **Key:** arxiv-2202.05262
- **Authors / organisation:** Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov; MIT CSAIL, Northeastern University, Technion
- **Date:** 2022-02
- **Link:** https://arxiv.org/abs/2202.05262
- **Kind:** paper
- **Read from:** full text (HTML, first ~100k of ~115k characters; some table cells garbled in extraction)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors ask where a GPT-style model stores factual associations like "the Space Needle is in Seattle", and whether that storage is localized enough to be edited directly in the weights. They combine a localization method (causal tracing over activations) with a weight-editing method derived from a mechanistic hypothesis. A successful targeted edit is offered as evidence for the hypothesis and as a practical way to update knowledge.

## What they studied
GPT-2 XL (1.5B, 48 layers) mainly, also GPT-J (6B), GPT-2 Medium and Large. Units: hidden states, MLP and attention outputs per layer and token; the MLP output projection matrix as an editable memory. Data: 1,000 factual prompts for tracing; zsRE (10,000 evaluation records) and a new dataset, CounterFact (21,919 counterfactual records with paraphrase, neighborhood and generation prompts).

## How they did it
Causal tracing runs the model three ways: clean; corrupted, with Gaussian noise (3 times the embedding standard deviation) added to subject token embeddings; and corrupted but with one clean hidden state restored. The total effect is the probability drop from corruption; the indirect effect of a state is how much restoring it alone recovers. They trace hidden states, MLP outputs and attention outputs over layers and tokens, and run a "severed" variant that freezes MLP (or attention) outputs to corrupted values to see which pathway the effect needs. From this they propose that mid-layer MLPs at the last subject token map a subject key to attribute values that attention later moves to the final token. ROME then treats the MLP output projection as a linear associative memory and applies a closed-form rank-one update forcing a chosen key k* to map to a new value v*, while minimizing disturbance to other keys via a key covariance C estimated from 100,000 Wikipedia hidden states. k* is averaged over the subject in several random short prefixes; v* is found by optimization to make the new object likely while a KL term keeps "{subject} is a" predictions unchanged. The edit is applied at one layer (layer 18 for GPT-2 XL). It is compared with fine-tuning (FT), norm-constrained fine-tuning (FT+L), hypernetwork editors KE and MEND (including versions retrained on the benchmark data) and Knowledge Neurons.

## What counts as an explanation here
A localized mechanistic hypothesis (subject enrichment in mid-layer MLPs, then attention copying) expressed as a causal-effect map, plus a weight-level model of the MLP as a key-value store. The hypothesis is made predictive by turning it into an edit: if facts are stored as key-to-value maps in that matrix, a rank-one change should change the fact, generalize to paraphrases, and spare neighbors.

## How they judged success
Tracing: average total and indirect effects, MLP vs attention, severed-pathway comparisons. Editing: Efficacy Score/Magnitude, Paraphrase Score/Magnitude, Neighborhood Score/Magnitude (specificity), harmonic-mean Score S, generation entropy (fluency), reference score (TF-IDF consistency with reference texts), and a human study (15 raters, 50 facts) on consistency and fluency.

## What they found
On GPT-2 XL the average total effect of corrupting the subject is 18.6%; restoring a single state at layer 15 at the last subject token recovers 8.7% on average; MLP indirect effect peaks at 6.6% at that early site versus 1.6% for attention. Severing MLPs removes the effect of low-layer states, severing attention does not. On CounterFact, ROME gets S = 89.2 (efficacy 100, paraphrase 96.4, neighborhood 75.4) on GPT-2 XL and S = 91.5 on GPT-J, while FT generalizes but damages neighbors, FT+L is specific but does not generalize, and KE/MEND show both problems. On zsRE ROME reaches 99.8% efficacy and is competitive with the hypernetworks. Human raters judged ROME's generations 1.8 times more likely to be consistent with the new fact than FT+L, but 1.3 times less likely to be fluent.

## Limits and open problems they name
One fact per edit (mass editing deferred to MEMIT); edits are directional (reverse relation not updated); logical, spatial and numerical knowledge not studied; structure of the attribute value space not understood; some fluency loss; misuse risk for inserting false information.

## What we take from it
Two reusable tools and a template. Causal tracing (noise, restore, measure recovery) is a standard localization baseline; the rank-one key-value edit is a concrete demonstration that a single weight matrix can be read and written as an associative memory given the right key statistics (C). The CounterFact metric triple (efficacy, paraphrase generalization, neighborhood specificity) is a good template for scoring any prediction of what a weight change will do. Warning, from arxiv-2301.04213: the success of the edit does not depend on the tracing result, so the localization story and the editing success should not be read as confirming each other.

## Tags
unit: layer | weights | head
form: description | causal-abstraction
method: patching | weight-analysis | ablation
eval: patching | downstream-task | human-rating | benchmark
goal: control/editing | understanding
