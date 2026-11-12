# LoRAcles: Self-Supervised Weight-Space Interpretability at Scale

- **Key:** neurips-cc-virtual-2026-oral-154334
- **Authors / organisation:** Celeste De Schamphelaere, Jan Bauer, Neel Nanda, Euan Ong; affiliations not listed on the conference page
- **Date:** 2026 (NeurIPS 2026 oral; also listed at ICML 2026)
- **Link:** https://neurips.cc/virtual/2026/oral/154334 (OpenReview forum EOoc3j4hW8 per that page; the scout's OpenReview id x9MbM7QmQN could not be verified, page blocked)
- **Kind:** paper
- **Read from:** abstract only (conference page), plus the public Hugging Face model card for one released checkpoint (ceselder/dynamic-loracle-qwen3-14b) and its training-data card. Full paper not accessible.
- **Relevance to us:** 3 (central)

## What they wanted, and why
Build language models that read LoRA adapter weights directly and answer natural-language questions about what
the adapter makes a model do, scaling the "learned weight interpreter" idea (cf. arxiv-2510.05092) to large models
and large training sets, for auditing finetuned models.

## What they studied
LoRA adapters on Qwen3-14B and Llama-3.3-70B (abstract); released artefacts also mention OLMo-3-32B. Unit: LoRA
weight deltas.

## How they did it
Per the abstract: train many LoRAs on small sets of pre-training documents (self-supervised: the documents give the
labels), then train LoRAcles to answer questions about those documents from the LoRA weights. Per the model card
(not the paper): LoRA deltas are converted to SVD direction tokens per rank, layer and side, injected into a frozen
base model at an early layer via an encoder, and an interpreter LoRA on the base model is trained on about 25k
synthetic LoRAs with LLM-generated Q/A pairs; rank-stabilized scaling was reported as necessary for the model to
condition on the tokens.

## What counts as an explanation here
Natural-language answers about the behaviour or knowledge a LoRA encodes, read from weights without running the
adapted model. Partial; mainly the most salient change.

## How they judged success
Abstract: AuditBench (state of the art claimed), detection of subliminal-learning changes in model organisms,
verbalizing semantic backdoor triggers, describing behaviours from full-parameter finetunes, and scaling with
training-set size. Specific metrics not available to us. The model card reports AuditBench any-match and
rollout-mean scores (canonical 48.2% / 13.1% for the Qwen3-14B checkpoint) but these are a card, not the paper.

## What they found
Abstract only: generalizes beyond training data; first non-trivial performance at verbalizing semantic backdoor
triggers; smooth scaling up to 100K LoRAs; some success on full finetunes. No paper numbers read.

## Limits and open problems they name
Prone to hallucination; surfaces mainly the most salient behavioural change, limiting use beyond narrow finetunes;
further scaling may need method changes.

## What we take from it
- **Shortcut:** self-supervised labels (train each weight delta on known documents) remove the need for hand-made
  behaviour labels when building a weights reader.
- **Method hint:** SVD-direction tokenization of weight deltas is a symmetry-aware way to feed weights to an LLM.
- **Benchmark:** AuditBench is the reference evaluation for weight-based auditing.
- **Warning:** hallucination and salience bias; still description, not prediction. Re-read the full paper when
  accessible before relying on any detail here.

## Tags
unit: weights
form: description
method: weight-analysis | training-interpretable | other
eval: benchmark | downstream-task
goal: safety/auditing | understanding
