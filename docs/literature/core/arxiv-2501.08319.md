# Enhancing Automated Interpretability with Output-Centric Feature Descriptions

- **Key:** arxiv-2501.08319
- **Authors / organisation:** Yoav Gur-Arieh, Roy Mayan, Chen Agassy, Atticus Geiger, Mor Geva; Tel Aviv University, Pr(Ai)²R Group
- **Date:** 2025-01
- **Link:** https://arxiv.org/abs/2501.08319
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Automated feature descriptions are usually written from the inputs that most activate a feature (MaxAct). That
is expensive (large corpora must be run) and ignores what the feature does to the output, which is what matters
when descriptions are used for steering. The authors argue a description should cover both what triggers a feature
and what it promotes, and test cheap output-centric description methods.

## What they studied
SAE features from Gemma-2 2B (Gemma Scope 16K/65K, residual and MLP), Llama-3.1 8B (Llama Scope 32K), GPT-2 small
(OpenAI SAEs 32K/128K), and MLP neurons of Llama-3.1 8B Instruct. 40 features per layer per SAE: 4,160 (Gemma),
2,560 (Llama), 2,880 (GPT-2), 2,560 (Llama Instruct neurons).

## How they did it
Four description sources fed to a GPT-4o mini explainer: MaxAct (public Neuronpedia/Transluce descriptions, with
MaxAct++ for Llama Instruct); VocabProj, projecting the feature's decoder vector through final layer norm and
unembedding and passing top/bottom 50 tokens (one matrix multiply); TokenChange, clamping the feature high on 32
random Pile prompts of 32 tokens and passing the top/bottom 20 tokens by mean logit change; and ensembles (Ensemble
Raw concatenates raw evidence, Ensemble Concat concatenates separate descriptions). Each description is then
scored two ways. Input-based: Gemini 1.5 Pro writes five activating and five neutral sentences from the description;
pass if the activating set has higher mean max activation. Output-based: the model generates from neutral prompts
while steered by the target feature and two random control features, with clamping set to reach KL about 0.25 and
0.5 from the unsteered model; a judge must pick which of the three text sets matches the description (chance 1/3).
They also try to revive "dead" SAE features using prompts derived from output-centric descriptions.

## What counts as an explanation here
A short natural-language description per feature, meant to capture both its input trigger and its output effect.
Partial and per-feature; it predicts which texts activate the feature and what steering it will produce.

## How they judged success
Input-based and output-based scores above (both LLM-judged, with random control features). The LLM judge was
checked against three graduate-student annotators (alternative annotator test, winning rate 1, p=0.03) and a
100-feature human study. Compute cost compared in FLOPs.

## What they found
MaxAct wins on the input metric; VocabProj and TokenChange beat it on the output metric, often by 15-30 points.
Ensembles of all three are best on both, about 6-10 points over the next-best single method on Gemma-2. Output
scores are lower for MLP features (about 45-50) than residual ones (about 66); VocabProj is weak in early layers.
Cost for describing all Gemma-2 2B MLP features: about 3.9e16 FLOPs for MaxAct vs 2.8e14 (VocabProj) and 9.9e13
(TokenChange). Of 1,850 "dead" features, 9.1% of MLP and 62% of residual features were revived, mostly by two-token
prompts. Qualitatively, MaxAct and VocabProj descriptions were similar 41% of the time and complementary otherwise.

## Limits and open problems they name
Noisy output evaluation; prompt sensitivity; binary input threshold; patching-based methods not compared;
vocabulary-tied methods cannot describe features without a word (e.g. positional); promotion vs suppression not
distinguished.

## What we take from it
VocabProj is a weight-only description method (decoder vector times unembedding) that is very cheap and good at
predicting a feature's causal output effect; this is a direct precedent for reading behaviour from weights. The
two-sided scoring (does it predict activation; does it predict the steering effect) is a ready evaluation template
for any feature-level claim our white-box model makes. Note the gap in early layers and for MLP features.

## Tags
unit: feature | neuron
form: description
method: SAE | weight-analysis | steering
eval: prediction/simulation | faithfulness | human-rating
goal: understanding | evaluation-of-methods
