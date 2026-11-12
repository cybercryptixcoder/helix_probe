# Fact Finding: Attempting to Reverse-Engineer Factual Recall on the Neuron Level

- **Key:** alignmentforum-fact-finding-reverse-engineer-factual-recall-neuron-level
- **Authors / organisation:** Neel Nanda, Senthooran Rajamanoharan, János Kramár, Rohin Shah; Google DeepMind
- **Date:** 2023-12-23
- **Link:** https://www.alignmentforum.org/posts/iGuwZTHWb6DFY3sKB
- **Kind:** blog/research post (five-post sequence)
- **Read from:** abstract and sections (post 1 in full; posts 2 and 3 read for methods and numbers; posts 4 and 5 not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
The team set out to fully reverse-engineer, at the level of individual MLP neurons, how a language model recalls a fact, choosing a case where computation is distributed and in superposition. The aim was to test whether ambitious, bottom-up mechanistic understanding of MLP computation is achievable in a real model. They report that this goal mostly failed and use the failure to argue about where neuron-level understanding stops working.

## What they studied
Pythia 2.8B on one-shot prompts asking which sport an athlete plays (baseball, basketball, American football), about 1,500 athletes filtered from Wikidata to those where the model assigns more than 50% to the right sport. Units: attention heads, MLP layers 2 to 6, individual neurons, and residual-stream directions.

## How they did it
They first found the circuit's high-level structure using path patching (swapping in an athlete from a different sport), direct logit attribution, and resample and mean ablation, and simplified it into an "effective model": attention layers 0 and 1 gather the name tokens onto the last name token, MLPs 2 to 6 look up the sport, and a few later heads (mainly L16H20) move it to the output. They then tested two neuron-level hypotheses for the MLPs. Against single-step detokenisation (neurons directly AND name tokens into facts): mean-ablating paths between MLP pairs; correlating each neuron's effect across nine facts about one athlete; and a non-linear "AND" score per GELU. For hash-and-lookup (early layers scramble the name into a near-random code, later layers look it up): linear probes per layer; MLP output norms for known versus unknown names; a midpoint test of whether MLPs break linear structure between swapped-surname pairs, compared with random-init MLPs. They also dissected a candidate "baseball neuron" (L5N6045).

## What counts as an explanation here
Aimed for: a neuron-level account of how MLP weights map name tokens to an attribute. Achieved: a simplified effective model of the circuit plus a conceptual description (early MLPs act as a lookup table producing a linearly readable attribute representation). They argue the lookup itself may have no interpretable intermediate structure and can be treated as a black box.

## How they judged success
Accuracy of the full and simplified models (preferred over loss recovered because late MLPs mostly sharpen confidence), probe accuracy by layer, logit difference under path patching, KL and loss under inter-MLP path ablation, correlation of neuron effects across facts, ROC AUC for single-neuron probes, and loss change when ablating a neuron.

## What they found
The model gets 100% on the filtered set; replacing the extraction step with a linear probe from L16H20 gives 98%; probe accuracy on the name token reaches about 90% by layer 6. The MLP effective model reaches about 86% on two-token names. Single-step detokenisation is falsified: there is substantial composition between MLPs, neuron effects barely correlate across facts about the same athlete, and only about 23% (median) of the non-linear effect is a direct AND. Strong hash-and-lookup is also falsified (known names already produce larger MLP outputs at MLP1), but MLPs do break linear structure (about 60 to 70% of the way, versus 20 to 40% for random MLPs). The baseball neuron predicts baseball players (about 89% AUC) and matters when ablated, but is not monosemantic. Roughly 6 to 7 FTE-months went into the project.

## Limits and open problems they name
They could not explain the MLP computation at neuron level and cannot rule out that better methods would; memorised facts may simply lack shared structure to exploit; sparse autoencoders may help with representations but are not expected to explain how weights implement the lookup; dataset filtering may bias results.

## What we take from it
(1) A major warning for reading function from weights: for memorisation-like computation (lookup tables), there may be no compact program to recover, so a white-box model may need to represent such parts as explicit tables or black boxes with clean interfaces. (2) The framing of an "effective model" (simplify, ablate the rest, check accuracy) is a practical stand-in for a partial white-box model. (3) Methods worth reusing: cross-fact neuron-effect correlation and comparing against random-initialisation baselines to tell learned structure from architecture artefacts. (4) Prefer hard accuracy alongside soft metrics; they diverge.

## Tags
unit: neuron, circuit, direction
form: description, replacement-model, probe
method: patching, ablation, probing, weight-analysis
eval: ablation, patching, faithfulness
goal: understanding, science
