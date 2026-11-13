# Unsupervised Decoding of Encoded Reasoning Using Language Model Interpretability

- **Key:** arxiv-2512.01222
- **Authors / organisation:** Ching Fang (Goodfire AI; work done as a Cambridge-Boston Alignment Initiative fellow), Samuel Marks (Anthropic)
- **Date:** 2025-12-01
- **Link:** https://arxiv.org/abs/2512.01222
- **Kind:** paper (workshop)
- **Read from:** full text (arXiv HTML)
- **Relevance to us:** 3 (central)

## What they wanted, and why
If a reasoning model stops producing human-readable chains of thought — whether through latent recurrence or through training pressure that makes encoded text advantageous — the main oversight tool (reading the CoT) fails. The authors ask a narrower, testable question: given a model whose reasoning is already opaque, can mechanistic interpretability recover it from activations alone, with no access to the base model or the encoding scheme? They build a controlled model organism and test the weakest realistic decoding tool (logit lens) before concluding that white-box reading is hopeless.

## What they studied
DeepSeek-R1-Distill-Llama-70B supervised-fine-tuned (QLoRA, rank 8) to write its thinking in ROT-13 while still answering in plain English. A 50-question test set requiring two-step reasoning (person → state → capital), with ground-truth intermediate steps known by construction. Unit of analysis: per-token residual activations at each layer, unembedded with the model's own unembedding.

## How they did it
Base-model responses to LM-Sys prompts were collected, the `thinking` spans ROT-13'd, and the model fine-tuned on the re-encoded transcripts. Because the base responses were made in English, the fine-tune is pushed toward keeping the original computation and only changing the surface form — an important confound the authors name themselves. The test prompts then elicit encoded reasoning. Decoding pipeline: for each position, project each layer's residual through the unembedding and take the argmax token (logit lens) to get a token-by-token transcript; drop repeated words; hand the transcript to a small model (Llama-3-8B) as a paraphraser to rebuild a fluent English paragraph; grade the paragraph with a larger model (Llama-3-70B) given the true English reasoning. Baselines: grader shown transcripts from unrelated prompts (chance) and the raw, still-encrypted CoT (no decoding). Variants: single layer 40, single layer 58, average of layers 54-62, and layer 58 with a confidence threshold that keeps only high-probability tokens. Per-word accuracy is also measured directly as "is the unembedded token the English translation of the word being completed".

## What counts as an explanation here
A natural-language reconstruction of the model's internal reasoning — a translation of the encoded CoT into English, produced without the base model or the cipher. The explanation is a faithful-ish transcript, not a mechanism: it claims to say *what* the model is thinking step by step, not *how* the steps are computed.

## How they judged success
Two measures: (i) per-word translation accuracy of the argmax unembedded token against the true English word, computed per layer over the full transcript with 95% CIs on 50 prompts; (ii) an LLM grader score of the reconstructed paragraph against ground truth, compared with a random-prompt baseline and a no-decoding baseline. Layer sweeps act as the main ablation, plus averaging versus single layer versus confidence thresholding.

## What they found
The argmax unembedded token matches the English translation well in intermediate-to-late layers, peaking around layer 58 (near the top of a 70B DeepSeek-distilled Llama), and degrades at layer 40 — i.e. the model keeps an English-anchored representation of the reasoning inside the encoded pass, reminiscent of the multilingual "semantic hub" result where intermediate layers converge on a dominant language. The full pipeline reconstructs reasoning far above both baselines; layer 58 beats layer 40 substantially; averaging layers adds little; confidence thresholding on layer 58 gives a clear further gain. Notably, activation probes (appendix) are a weaker translation mechanism than logit lens here.

## Limits and open problems they name
The fine-tune was built from English base responses, so the optimisation may preserve the base activation space more than a naturally-arising encoding would; an RL-trained encoding could be far less English-aligned and the decoding would likely break. ROT-13 is a trivial substitution cipher, not a learned code. Single model, small test set, LLM-graded rather than human-graded transcripts.

## What we take from it
Method: the "re-encode the visible reasoning and fine-tune on it" recipe is the cheapest way to build a controlled opaque-thinking model organism for evaluating any white-box reader. Measure: per-word translation accuracy *as a function of layer* is a clean diagnostic of where semantic content is readable — cheaper and more informative than a single end-to-end score. Warning: the base-model-derived training data creates an English anchor; our predictive model must not assume that representational language-alignment holds for encodings that arise from RL pressure. Framing: "decode through the unembedding" is a surprisingly strong baseline — any SAE/feature-based decoder should be compared against logit lens plus a paraphrase step, not against raw probes.

## Tags
unit: layer | feature | whole-model
form: description | probe | program
method: probing | other
eval: downstream-task | human-rating | faithfulness
goal: safety/auditing | understanding
