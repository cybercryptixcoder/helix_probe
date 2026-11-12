# Do Models Explain Themselves? Counterfactual Simulatability of Natural Language Explanations

- **Key:** arxiv-2307.08678
- **Authors / organisation:** Yanda Chen, Ruiqi Zhong, Narutatsu Ri, Chen Zhao, He He, Jacob Steinhardt, Zhou Yu, Kathleen McKeown; Columbia University, UC Berkeley, New York University
- **Date:** 2023-07
- **Link:** https://arxiv.org/abs/2307.08678
- **Kind:** paper
- **Read from:** full text (first ~two-thirds of HTML in detail: method, metrics, experiments, results, limitations)
- **Relevance to us:** 3 (central)

## What they wanted, and why
LLMs give natural-language explanations of their answers, but does an explanation tell a reader how the model will
behave on *other* inputs? The authors argue that a good explanation should let a human build a correct mental model
of the system, so it should support predictions on related, counterfactual inputs. Example: if a model says "yes,
eagles can fly, because all birds can fly", a reader expects "yes" for penguins; if the model then says "no", the
explanation misled. The larger goal is to measure explanation quality by predictive usefulness rather than by how
convincing it sounds.

## What they studied
GPT-3.5 and GPT-4 as the explained models, each with two explanation styles: chain-of-thought (explanation before
answer) and post-hoc (answer, then explanation). Tasks: StrategyQA (yes/no multi-hop factual reasoning) and Stanford
Human Preferences (SHP, choosing the better of two responses, a reward-modeling task). Unit of analysis: the
whole model's input-output behaviour as summarised by a text explanation.

## How they did it
1. Get the model's answer and explanation for an input.
2. Generate counterfactual inputs relevant to that explanation using LLMs (GPT-3.5 and GPT-4 prompted to write
   related questions): ten per explanation for StrategyQA, six for SHP. Mixing the two generators gave more diverse
   counterfactuals than the Polyjuice baseline.
3. Have a simulator (Mechanical Turk annotators, three per item, for StrategyQA; GPT-4 as a proxy simulator for SHP,
   after showing its agreement with humans matched or exceeded human–human agreement there) decide, for each
   counterfactual, whether the explanation lets them infer the model's output, and if so what it is. Simulators use
   their own commonsense only where the explanation is silent.
4. Query the model on the counterfactual and compare its actual answer with the simulated one.
5. Separately collect plausibility ratings of explanations and correlate them with precision.

## What counts as an explanation here
A free-text natural-language rationale produced by the model itself. It is treated as an implicit predictive model
of the system: its quality is the accuracy and breadth of the predictions a reader can derive from it.

## How they judged success
- **Simulation precision:** among counterfactuals that the simulator judged inferable ("simulatable"), the fraction
  where the inferred output matches the model's actual output.
- **Simulation generality:** one minus the average pairwise similarity among simulatable counterfactuals (similarity
  by BLEU, sentence-embedding cosine, or Jaccard) — i.e. how diverse a range of inputs the explanation covers.
- Controls: a sanity check comparing normal explanations with explanations forced to justify the wrong answer;
  correlation with human plausibility ratings (Pearson and Spearman); inter-annotator agreement.

## What they found
- Precision is modest: around 80% for these binary tasks.
- GPT-4 beats GPT-3.5 on precision (StrategyQA CoT 81.1 vs 77.3; SHP CoT 93.0 vs 86.3).
- CoT is not clearly better than post-hoc (+1.2 points on StrategyQA, −1.3 on SHP).
- Precision is essentially uncorrelated with plausibility (Pearson +0.012, Spearman +0.021), versus about +0.39
  agreement between humans; the authors infer that optimising for human approval may not improve simulatability.
- Generality and precision are also near-uncorrelated.
- Task difficulty does not predict precision: SHP had lower task accuracy but higher precision (89.0 vs 79.8).
- Sanity check: 83.4 precision for normal explanations versus 38.2 for forced wrong-answer explanations, so the
  metric discriminates.

## Limits and open problems they name
Results depend on the counterfactual distribution, which LLM generators may not cover well. Only classification
tasks, only English, only single-turn explanations. Downstream uses (debugging, teaching) were not tested.

## What we take from it
- **Measure (directly reusable):** precision and generality over counterfactual inputs are a ready-made pair of
  metrics for any explanation that claims to predict a model. For a white-box reconstruction, "precision" = how
  often its predictions match the network on perturbed inputs; "generality" = how diverse those inputs are. Report
  both, since they do not move together.
- **Method:** LLM-generated counterfactuals targeted at the explanation's own claims, with an LLM simulator
  validated against humans first.
- **Warning:** plausibility and faithfulness are decoupled; an explanation that reads well can mispredict.
- **Control:** a deliberately wrong explanation as a floor baseline.

## Tags
unit: whole-model
form: description
method: other
eval: prediction/simulation | faithfulness | human-rating
goal: evaluation-of-methods | understanding
