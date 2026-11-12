# Linearity of Relation Decoding in Transformer Language Models

- **Key:** arxiv-2308.09124
- **Authors / organisation:** Evan Hernandez, Arnab Sen Sharma, Tal Haklay, Kevin Meng, Martin Wattenberg, Jacob Andreas, Yonatan Belinkov, David Bau; MIT, Northeastern University, Technion, Harvard
- **Date:** 2023-08 (v2 Feb 2024, ICLR 2024)
- **Link:** https://arxiv.org/abs/2308.09124
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML main text read in two parts; causality numbers are in figures/appendix G and were not available as text; limitations appendix I only seen by heading)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Earlier work located where factual associations live (subject token states, MLPs, attention heads) but not what computation turns a subject into an attribute. The authors ask whether, for a given relation ("plays the sport of", "is located in"), the whole stretch of computation from the subject representation to the predicted object is well approximated by one affine map. If so, a large nonlinear subcomputation has a tiny, inspectable, editable surrogate. This is a step toward explaining knowledge retrieval with simple models that both predict and allow intervention.

## What they studied
Main model GPT-J; GPT-2-XL and LLaMA-13B in an appendix. A new dataset of 47 relations in four groups: factual (26 relations, 9,696 examples), commonsense (8, 374), linguistic (6, 806), bias (7, 213); only triples the model gets right are used (for GPT-J 4,652 factual, 219 commonsense, 507 linguistic, 96 bias). Unit: the hidden state at the last subject token at a chosen layer, and the final-layer state that is decoded to the object.

## How they did it
For each relation, take n = 8 examples, prompt the model with the other examples as few-shot context, and treat the network's map from the subject state s (at layer ℓ) to the final state o as a function F(s, c). Linearise it with a first-order Taylor expansion: W is the Jacobian dF/ds averaged over the n examples, and b is the average of F(s) minus W s. The LRE is then β·W·s + b, where β > 1 is a single per-model scalar compensating for the Jacobian underestimating the size of changes (they attribute this to layer norm). The layer and the rank of a low-rank pseudoinverse are picked per relation by grid search. To test prediction (faithfulness), they apply the LRE to a new subject's state and decode with the model's unembedding, checking the top first token against the model's own top prediction. To test causal use (causality), they invert the LRE: to make the model say a different object o', they change s by the low-rank pseudoinverse of W times (o' minus o) and check whether the model now outputs o'. Baselines: identity (logit lens on s), translation (s + mean offset), linear regression fitted on the same n examples, and the LRE applied to raw subject embeddings; for causality, an oracle that substitutes the other subject's state, plus two weaker insertion baselines. They also build an "attribute lens" that applies a relation's LRE at every layer and position.

## What counts as an explanation here
A per-relation affine surrogate model, derived from the network's own Jacobian, standing in for many layers of computation. It is explicitly partial (only some relations, only the first object token) but it is predictive (outputs the model's answer for unseen subjects) and invertible for editing.

## How they judged success
Faithfulness: rate at which the LRE's top first token equals the model's own top prediction, compared to a random-guess baseline and the baselines above. Causality: rate at which an edit made through the inverted LRE flips the model's top prediction to the target object, compared to the oracle substitution. Correlation between faithfulness and causality across relations. Averages over 24 random draws of the n examples. Attribute lens: recall@1/2/3 of the true attribute on prompts where distractions make the model output something false.

## What they found
For 48% of relations they find LREs that recover the mapping for a majority of subjects; nearly half the relations exceed 60% faithfulness. The LRE beats all baselines; identity, translation and the embedding-input variant do poorly, so both W and b are needed. Some relations are not linear: for "company CEO" no method passes 6% faithfulness although GPT-J answers 69 cases correctly (the authors suggest output ranges too large to encode linearly). Causality is usually higher than faithfulness and the edit tracks the oracle (shown in figures; numbers not read). With hyperparameters chosen for causality (β = 2.25), faithfulness and causality correlate at R = 0.84 across relations, but not when tuned for faithfulness. Layer sweeps show a "mode switch": for "plays sport", decodability holds from about layer 7 to 17 and then drops when the prompt asks for the relation, suggesting later layers stop enriching the subject and turn to next-token prediction. The attribute lens recovers the true fact much more often than the distracted output (recall@1 0.54 vs 0.02 for repetition distraction, 0.63 vs 0.03 for instruction distraction).

## Limits and open problems they name
Many relations are not linearly decodable, so the LRE is not the general mechanism. Only the first token of the object is checked; one correct object assumed; dataset size is limited. β and the layer are hand-tuned. Results are mainly on GPT-J.

## What we take from it
(1) A directly reusable recipe for building a predictive white-box surrogate of a subcomputation: average Jacobians around real inputs, then test the linear map both forward (predict outputs on held-out inputs) and backward (use its inverse to edit and check the model follows). This pairing of prediction and intervention is exactly the double test our white-box model should pass. (2) Measures: "faithfulness" as agreement with the model's argmax on held-out inputs; "causality" as edit success vs an oracle substitution. (3) Warning: hyperparameters tuned for one measure can decouple the two; report both. (4) Strong baselines to beat: identity/logit lens, translation, and least-squares regression on the same examples. (5) The LRE is computed from the network's derivatives, a halfway point between probing activations and reading weights.

## Tags
unit: direction, layer
form: replacement-model, probe
method: weight-analysis, probing, patching, other
eval: prediction/simulation, faithfulness, patching
goal: understanding, control/editing, science
