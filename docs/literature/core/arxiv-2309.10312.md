# Rigorously Assessing Natural Language Explanations of Neurons

- **Key:** arxiv-2309.10312
- **Authors / organisation:** Jing Huang, Atticus Geiger, Karel D'Oosterlinck, Zhengxuan Wu, Christopher Potts; Stanford University, Pr(Ai)²R Group, Ghent University-imec
- **Date:** 2023-09
- **Link:** https://arxiv.org/abs/2309.10312
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Natural-language explanations of neurons could serve safety checks, bias detection and editing, but only if they
are faithful. The authors audit the GPT-4 neuron explanations of Bills et al. (2023) for GPT-2 XL by defining two
rigorous tests of what an explanation claims: an observational one and a causal one.

## What they studied
GPT-2 XL MLP neurons and their GPT-4-written explanations. Observational tests used 300 explanations sampled from
the 1.7k neurons whose GPT-4 simulation score was at least 0.8. Intervention tests covered six concept families
(numbers, verbs, time expressions, locations, person names, plural inflection), about 80K explanations (27%).

## How they did it
Observational mode: an explanation is read as claiming the neuron fires on all and only strings the explanation
denotes. GPT-3.5 generates strings inside and outside the concept (over 95% judged valid on review); errors are
Type I (predicted firing that does not happen) and Type II (firing outside the concept), giving precision, recall
and F1. Groups of N neurons sharing an explanation are tested with a linear probe. Intervention mode: an explanation
is read as claiming the neuron causally mediates the concept. Two next-token tasks per concept (e.g. "The year after
Y is") are built, and interchange interventions swap neuron values from a source input into a base input on 256
pairs, scored by interchange intervention accuracy (IIA). Baselines: random selection of the same fraction K of
neurons, and neurons ranked by token-activation correlation.

## What counts as an explanation here
A text label for a neuron, reinterpreted as a testable claim about its activation set (observational) and about
causal mediation (interventional). The authors argue that structured formalisms such as programs would make better
explanations than vague prose.

## How they judged success
Precision/recall/F1 against random neuron-explanation pairings; IIA against random and correlation baselines;
correlation between F1 and the original GPT-4 simulation score; manual error analysis of 100 explanations.

## What they found
Observational F1 0.56 (precision 0.64, recall 0.50) for single neurons vs 0.00 for random pairings; with probes,
0.60/0.67/0.73 at N=1/4/16, but random groups reach 0.69 at N=16. F1 barely correlates with the GPT-4 score
(r = -0.1); the simulation score, computed on 10 samples, misses rare Type I errors. Many Type II errors were
antonyms or unrelated concepts, consistent with superposition. Causally: correlation-ranked neurons far exceed GPT-4
explanations, which are about random; only number explanations beat random. No single neuron changed behaviour when
intervened on; in layer 1 the top 20% most-correlated neurons carried about 80% of the effect.

## Limits and open problems they name
GPT-2 XL only. Natural language is vague (over 30% of explanations use hedges like "related to"). Neurons may be
the wrong unit given distributed, polysemantic representations. Faithful explanations could be misused.

## What we take from it
A clear template for testing any explanation as a prediction: an observational test (precision/recall over a
denoted set, including rare false positives) plus a causal test (interchange interventions, IIA) against random and
correlational baselines. A strong warning that simulation scores on few samples overrate explanations, and that
single neurons rarely carry causal weight. Supports making our white-box model's claims executable rather than prose.

## Tags
unit: neuron
form: description | probe
method: patching | probing | other
eval: prediction/simulation | faithfulness | patching
goal: evaluation-of-methods
