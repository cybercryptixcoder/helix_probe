# Towards Faithfully Interpretable NLP Systems: How should we define and evaluate faithfulness?

- **Key:** arxiv-2004.03685
- **Authors / organisation:** Alon Jacovi, Yoav Goldberg; Bar-Ilan University (Goldberg also Allen Institute for AI)
- **Date:** 2020-04
- **Link:** https://arxiv.org/abs/2004.03685
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
An opinion paper that tries to fix how the NLP explainability community defines and evaluates faithfulness. The authors separate plausibility (how convincing an explanation is to people) from faithfulness (how accurately it reflects the model's actual reasoning) and argue that conflating them is dangerous, e.g. a plausible but unfaithful explanation could mislead a judge in recidivism prediction. They want evaluation practice grounded in explicit assumptions and a move from binary to graded faithfulness.

## What they studied
The existing literature on explanation methods for NLP models (attention maps, heat-map/saliency methods, rationales, surrogate models) and how it evaluates them. No new experiments.

## How they did it
Conceptual analysis. They propose evaluation guidelines, identify three assumptions that underlie existing faithfulness tests, map methods to those assumptions, and critique the binary framing. The three assumptions: (1) model assumption: two models make the same predictions iff they use the same reasoning, so a faithful method gives the same explanation for behaviourally identical models; (2) prediction assumption: similar inputs get similar decisions iff their reasoning is similar, so explanations of similar inputs should be similar; (3) linearity assumption: input parts contribute independently and some matter more, the basis of heat-map explanations (which they flag as contested).

## What counts as an explanation here
Any artefact claiming to describe the model's reasoning (heat maps, rationales, surrogate models such as trees or rule lists). Faithfulness is a property of the explanation relative to the model, and is expected to be graded and local, not all-or-nothing.

## How they judged success
They survey and classify evaluation methods: erasure (remove top- or bottom-ranked input parts and see if the prediction changes); comprehensiveness and sufficiency; fidelity of surrogate explanation models to the original model's decisions; forward simulation by humans; robustness/perturbation tests; and counterexample construction (training a model with the same predictions but different explanations). Guidelines: say whether you evaluate faithfulness or plausibility; do not use human judgements of quality or human gold labels for faithfulness; do not accept inherent-interpretability claims untested; do not treat end-user task performance as evidence of faithfulness.

## What they found
Most existing work shows only that methods fail, via counterexamples, because strict faithfulness is nearly unattainable for any lossy explanation. A system with random explanations could still improve user task performance, so HCI outcomes do not establish faithfulness. Inherently interpretable models still need faithfulness testing.

## Limits and open problems they name
Formalising and measuring graded faithfulness: across tasks and models (sufficient for sentiment but maybe not QA) and across the input space (faithful in some neighbourhoods but not globally). Heat-map methods depend on the contested linearity assumption.

## What we take from it
- Measure: our white-box model should be scored by fidelity to the network's actual outputs (and internals) under intervention, never by human plausibility ratings.
- Test design: the model assumption gives a concrete check; behaviourally identical networks (e.g. different seeds or reparameterisations) should yield equivalent reconstructions, or we should explain why not.
- Report graded, local faithfulness: where in input space the reconstruction holds and where it breaks, rather than one global yes/no.
- Even a reconstruction "interpretable by design" must be tested, not assumed faithful.

## Tags
unit: whole-model
form: description | replacement-model
method: other
eval: faithfulness | prediction/simulation | ablation
goal: evaluation-of-methods
