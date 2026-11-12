# Steering Language Models With Activation Engineering (ActAdd)

- **Key:** arxiv-2308.10248
- **Authors / organisation:** Alexander Matt Turner, Lisa Thiergart, Gavin Leech, David Udell, Juan J. Vazquez, Ulisse Mini, Monte MacDiarmid; independent / MIRI / University of Bristol / Arb Research / MATS / Anthropic
- **Date:** 2023-08
- **Link:** https://arxiv.org/abs/2308.10248
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The authors argue models hold latent capabilities and dispositions that prompting, few-shot examples and finetuning do not reliably draw out. They propose "activation engineering": changing internal activations at inference time to steer outputs. Activation Addition (ActAdd) is the simplest version, needing no gradients and as little as one pair of prompts. Beyond control, a working steering vector is evidence that a property is represented roughly linearly in the residual stream.

## What they studied
GPT-2-XL (1.5B) for perplexity, topic steering and side effects; OPT-6.7B and LLaMA-3-8B for toxicity and sentiment; GPT-J-6B and Llama-1-13B for replication. Unit: a residual-stream direction at one layer.

## How they did it
Run a contrast pair of prompts (e.g. "Love" vs "Hate"), record residual activations at layer l, take the difference, scale by coefficient c, and add it to the residual stream of the user's prompt, aligned at the front positions. Steered positions are masked when scoring next-token predictions. Middle layers work best; they grid-searched c in [3, 20] and l in [6, 24]. Experiments: (1) perplexity on OpenWebText documents split into wedding-related and unrelated, steering with a "weddings" vector, vs prompting; (2) topic steering measured by the frequency of topic words and GPT-3.5-rated relevance; (3) toxicity on 1,000 RealToxicityPrompts prompts scored by Perspective API; (4) sentiment shifting on 1,000 IMDb prompts scored by a SiEBERT classifier; (5) side effects on ConceptNet factual recall (LAMA, 29,774 items) with the wedding vector. Fluency is measured by davinci-002 conditional perplexity and relevance by MiniLM cosine similarity. Baselines: unsteered model, prompting, PreADD, FUDGE, Air-Decoding; no finetuning comparison. Random vectors of matched norm serve as a control.

## What counts as an explanation here
A steering vector: a single direction whose addition shifts a high-level property of generation. It is used as evidence about representation (the property is linearly accessible and causally active) rather than as a full account of mechanism. Partial and not predictive beyond "adding more moves outputs further".

## How they judged success
Perplexity ratio on on-topic vs off-topic text; topic-word frequency and LLM-rated relevance; Perspective toxicity; SiEBERT sentiment success rate; disfluency (conditional perplexity) and relevance as cost metrics; ConceptNet P@K for capability preservation; random-vector controls.

## What they found
The wedding vector lowered perplexity on wedding-related text (ratio 0.875 vs 0.890 for prompting) while barely touching unrelated text (0.994 vs 1.132 for prompting, which hurt more). Wedding-word completions exceeded 90% at the best layer vs about 2% unsteered, with effectiveness peaking around layer 6. Toxicity on OPT: 0.112 vs 0.134 unsteered and 0.122 for PreADD-D, at a fluency cost (disfluency 8.9 -> 13.8); on LLaMA-3 a smaller drop (0.114 -> 0.108). Negative-to-positive sentiment: LLaMA-3 ActAdd 0.669 success vs 0.417 unsteered and FUDGE 0.551, which they call state of the art; positive-to-negative was weaker than PreADD-S but far more fluent. ConceptNet P@K was essentially unchanged under the wedding vector. Matched-norm random vectors barely changed outputs. Replication on Llama-1-13B failed for several vectors.

## Limits and open problems they name
Users must choose layer and coefficient; requires activation access; unlikely to teach new skills and effects on reasoning unexamined; some vectors simply fail and large coefficients break coherence; fluency costs in some sentiment settings; limited prompts and models, partial replication failure; sampling settings mattered (an external blinded run preferred different ones).

## What we take from it
A baseline and a control design. Any claim our white-box model makes about a behaviour-relevant direction should be checked against ActAdd-style contrast-pair steering, with matched-norm random vectors as the null and both target-effect and off-target metrics (perplexity on unrelated text, factual recall P@K). The finding that steering works at a specific band of layers and fails on some models is a reminder that "linear representation" claims are layer- and model-specific. Steering effects scale with coefficient, which offers a simple quantitative prediction to test (dose-response).

## Tags
unit: direction | layer
form: steering | direction
method: steering
eval: downstream-task | benchmark | ablation
goal: control/editing | understanding
