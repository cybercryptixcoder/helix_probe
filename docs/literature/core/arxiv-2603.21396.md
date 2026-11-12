# Mechanisms of Introspective Awareness

- **Key:** arxiv-2603.21396
- **Authors / organisation:** Uzay Macar, Li Yang, Atticus Wang, Peter Wallich, Emmanuel Ameisen, Jack Lindsey; Anthropic Fellows, MIT, Constellation, Anthropic
- **Date:** 2026-03-22
- **Link:** https://arxiv.org/abs/2603.21396
- **Kind:** paper
- **Read from:** full text (main body and early appendices; read via HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Earlier work showed LLMs sometimes notice a concept vector injected into their residual stream and can name it
("introspective awareness"). Critics suggested a shallow artifact such as a yes-bias. The authors test whether the
effect is robust, find the circuit that implements it in an open model, and locate when in training it appears. It is
a step toward understanding, mechanistically, when models' self-reports about their internal states are grounded.

## What they studied
Main model Gemma3-27B (62 layers; instruct, base and refusal-ablated variants). Qwen3-235B for prompt robustness;
OLMo-3.1-32B base/SFT/DPO/instruct checkpoints for training-stage effects; Ministral-8B, Yi-1.5-9B, Qwen2.5-14B in
appendices. Units: steering directions, MLP layers, attention heads, and Gemma Scope 2 transcoder features.

## How they did it
Concept vectors are the residual-stream difference between "Tell me about {concept}" and a mean over 100 baseline
words, injected at layer 37 with strength 4 on Gemma; the model is asked whether it detects an injected thought and
what it is about; GPT-4.1-mini judges. 500 concepts x 100 trials, split into success and failure concepts. They
measure detection, false positives and identification across prompts and checkpoints, then probe mechanism with
mean-difference direction swaps, bidirectional steering, PCA, ridge regression from transcoder features to detection,
logit lens, mean-ablation and patching of MLPs and attention, transcoder feature ablation and patching, and steering
attribution graphs from the injection site to the yes/no decision. They also test refusal ablation, DPO variants on
OLMo, and train a single bias vector on an MLP output to boost introspection.

## What counts as an explanation here
A partial circuit: early "evidence carrier" features that respond to any injected direction suppress late "gate"
features that default the model to answering no, plus a separate late-layer path for naming the concept. Supported by
attribution graphs and causal ablations; it predicts that ablating gates or carriers changes detection, which they test.

## How they judged success
Detection rate (TPR), false-positive rate on no-injection trials, introspection rate (detect and identify), forced
identification rate; change in detection under ablation and patching; R² of ridge regression predicting detection;
cosine similarity between directions (e.g. to the refusal direction); comparison across base/SFT/DPO checkpoints.

## What they found
Instruct prompts gave 0% false positives with moderate detection, while the base model had 42.3% false positives with
similar detection (no discrimination). Mean detection over 500 concepts was 38.2%. On OLMo, SFT gave TPR minus FPR of
-11.5% and DPO about +9.8%, so the ability emerges from preference training. Mean-ablating the layer-45 MLP cut
detection from 39.0% to 24.2%; ablating top gate features cut it from 39.5% to 10.1%; no single attention head
mattered much. Transcoder features predicted detection better (R² 0.624) than a scalar projection (0.309). Refusal
ablation raised detection from 10.8% to 63.8% at a 7.3% false-positive cost, and the relevant direction was nearly
orthogonal to refusal (cosine -0.09). A trained bias vector raised detection by 74.7 points on held-out concepts with
0% false positives.

## Limits and open problems they name
Mostly one model; transcoder availability restricted mechanistic work to Gemma. The injection setting is artificial.
Reliance on an LLM judge. Role of attention unclear. Which post-training ingredients create the gates is unknown.
No claim about subjective experience.

## What we take from it
A method template: combine behavioural metrics with a no-intervention false-positive control, then use transcoder
attribution plus ablation to localise a mechanism, and compare checkpoints across training stages. The finding that
models underreport what they can detect (a gate suppressing it) warns that behavioural self-report understates
internal information, which argues for reading internals or weights directly. The regression-from-features-to-behaviour
step is a small example of predicting behaviour from internal state.

## Tags
unit: feature | direction | layer
form: graph | direction
method: transcoder | attribution | ablation | patching | steering
eval: ablation | patching | prediction/simulation
goal: science | understanding
