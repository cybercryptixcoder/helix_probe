# Towards Interpreting Any Residual Stream Direction by Scaling Activation Inversion

- **Key:** arxiv-2611.08465
- **Authors / organisation:** Celeste De Schamphelaere (MATS), Juan J. Vazquez, Ari Spiesberger, Gavin Leech (Arb Research), Tomáš Gavenčiak (Arb Research, Charles University), Euan Ong and Jiahai Feng (Anthropic; equal advising)
- **Date:** 2026-11-05
- **Link:** https://arxiv.org/abs/2611.08465
- **Kind:** paper
- **Read from:** abstract and sections (method, evaluation, applications, limitations, discussion; appendices only partly)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The standard way to interpret a residual-stream direction is to find text that strongly activates it, but searching a corpus only finds what the corpus contains and scales poorly. Other "readers" such as natural-language autoencoders (NLAs) produce descriptions that need human or LM judges to verify. The authors want a generator that, given any direction, writes text that activates it, with output that can be checked by one forward pass of the subject model. This is a step toward scalable, verifiable interpretation of arbitrary directions (features, steering vectors, backdoor directions, single activations).

## What they studied
Subject model Qwen3.6-27B, read at layer 42. Directions: held-out residual activations from Ultra-FineWeb, SAE features (512 features from a 131k BatchTopK SAE at layer 42), steering vectors (AxBench difference-of-means, 334 concepts; BiPO persona vectors, 119 behaviours), rank-1 LoRA backdoor adapters (48), and "workspace" prompts from prior work. Unit: arbitrary directions.

## How they did it
The Maximally-Activating Example Metamodel (MAEM) is a fine-tune of a copy of the subject model. The target direction is injected (norm-matched) at a placeholder token after the second block; the MAEM then writes text, which is run through the frozen subject model without injection. Score: the maximum cosine similarity between the direction and per-token activations over the generated span. Training is SFT first (activations or SAE directions paired with the text that produced or maximally activates them), then RL following the ScaleRL recipe with reward computed over the last 16 generated tokens, no KL term, and a small length penalty. The objective needs no labels. Baselines: corpus search over 10M tokens, NLAs, GCG and EPO prompt optimisation, the untrained base model with/without injection, and a random-direction floor.

## What counts as an explanation here
Exemplar text: generated passages that maximally activate the direction, from which a human or LM infers what the direction means. Exemplars are self-verifying (activation can be measured), but meaning is still inferred from them.

## How they judged success
Centred cosine (corpus mean subtracted) between target and best exemplar at best-of-1/8/64 on 486 held-out activations; out-of-domain generalisation across 21 unseen domains; fluency (log-likelihood under an independent model; LM-judge coherence); concept identification for steering vectors (LM judge picks from 10 candidates); backdoor payload recovery (verbatim and semantic); verbalisation accuracy on workspace tasks; fraction of SAE features fired and fraction reaching half/over corpus peak; Delphi-style detection/fuzzing scores for explanations; Vendi diversity.

## What they found
Centred cosine 0.80 at k=1 rising to 0.87 at k=64, versus 0.60 for 10M-token corpus search and 0.64–0.74 for NLAs; GCG/EPO cost 82–280x more GPU. Beats in-domain corpus search on 12 of 21 unseen domains despite English-only training. Steering-vector concept ID: 95.8% on AxBench (NLA 92.8%, corpus 61.4%), 83.7% on BiPO (NLA 85.7%). Backdoors: theme triggers recovered 69% from the read direction (corpus 49%); write direction gives 85% verbatim payload recovery for theme adapters; numeric codes are poor. Fires 89% of SAE features at best-of-8 (31% exceed the corpus peak), but descriptions written from MAEM exemplars are weaker than from corpus exemplars. Trails NLAs on workspace verbalisation but beats other baselines.

## Limits and open problems they name
Single subject model. High activation does not guarantee a correct semantic account. About 11% of features never fire at best-of-8 (6.5% by none of 64 draws), concentrated in rare and positional features. Low diversity (Vendi 2.2 vs 2.9 for corpus) produces narrower explanations; diversity selection did not fix it. The generator can still find degenerate high-scoring text. Open: cross-architecture transfer, use as initialisation for other metamodels, a diversity objective; some features may be under-determined by a single direction.

## What we take from it
(1) A verifiable-by-forward-pass objective is a good template: any explanation we produce should, where possible, be checkable against the original network's own activations rather than an LLM judge. (2) Activation inversion is a tool for testing a predicted feature meaning: if our white-box model says a direction means X, generate inputs and check. (3) Warning that maximal activation and correct meaning are different, and that single-exemplar methods miss a feature's breadth (diversity matters). (4) Concrete baselines to compare against: corpus search, NLAs, GCG/EPO.

## Tags
unit: direction | feature
form: description | other (generated exemplars)
method: other (metamodel, RL activation inversion) | SAE | steering
eval: prediction/simulation | benchmark | downstream-task
goal: understanding | safety/auditing | evaluation-of-methods
