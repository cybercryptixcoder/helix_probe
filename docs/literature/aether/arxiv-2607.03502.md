# Reading Between the Dots: Decoding Hidden Computation across Filler Tokens

- **Key:** arxiv-2607.03502
- **Authors / organisation:** Kaley Brauer, Claudio Mayrink Verdun (Harvard / Cambridge Boston Alignment Initiative, MIT), Samuel Marks (Anthropic)
- **Date:** 2026-07 (arXiv v1, 3 Jul 2026)
- **Link:** https://arxiv.org/abs/2607.03502
- **Read from:** full text (arXiv HTML v1)
- **Relevance to us:** 3 (central)

## What they wanted
To test whether reasoning that runs across content-free filler tokens — dots, counting sequences — is truly unreadable, or only unreadable *in the output*. Filler-token computation is treated in the literature as the limit case for chain-of-thought monitorability: the surface tokens carry no information, so surface reading cannot recover what happened.

## What they studied
Four task families with a nameable intermediate value: one-fact addition, two-fact addition (two retrieved quantities then summed), two-hop letter position (retrieve a city/element name, index a character), and a system of linear equations with nonsense variables where every intermediate is computed in context. Two open-weights MoE models: DeepSeek V3 and Kimi K2. Filler (dots, counting, alphabet, and scrambled variants) inserted between question and answer slot, at varying lengths.

## How they did it
Three-stage argument: (a) behaviour — accuracy with vs without filler; (b) mechanism — attention flow, logit lens at each layer × filler position, and KV-cache transplants restricted to filler rows between matched examples; (c) an unsupervised decoding pipeline — logit lens at the second half of layers, subtract the cross-example mean distribution to strip formatting noise, aggregate residual scores over filler positions, take top-50 tokens, hand to an LLM judge with no ground truth and no training.

## What counts as an explanation here
A mechanism is established when the intermediate is (i) visible in the residual stream at the right place and time, (ii) causally load-bearing under a transplant, and (iii) recoverable from hidden states alone without labels — i.e. behaviour + localisation + decoding, mirroring the tri-partite structure common to much recent circuit work.

## How they judged success
Accuracy uplift from filler, controlled by scrambled-filler conditions; logit-lens hit rate against the ground-truth intermediate; KV-cache transplant rank shifts of the donor's answer; and top-K accuracy of the decoded intermediate under two LLM judges (and a judge-free variant).

## What they found
- Filler uplift is real in open-weights models and roughly general: large gains on one-fact addition and the system of equations, smaller but significant on two-fact addition and letter position. Qwen 3 480B showed only a small letter-position effect, so the phenomenon is broad but not universal.
- Filler must sit *between* question and answer; placed before the question it does not help. Non-disruptive sequences work; scrambled ones underperform — content does not matter, presence does.
- Attention is rerouted into a relay: answer→question attention drops and the freed budget goes to the filler region, which reads the question and passes information forward.
- Logit lens at filler positions shows ordered computation: first addend early in the filler, second later, the sum crystallising late just before the answer. In wrong examples the addends are still present but the sum is not — a retrieval-plus-composition-failure signature.
- Filler-row KV transplants move the donor answer tens to hundreds of ranks; transplanting only the positions where an addend decodes recovers most of the effect.
- Unsupervised decoding recovers the intermediates without labels, best judge, across both models and all four tasks (reported 80–95%).

## Limits
Logit lens is coarse; analyses run on 4-bit quantised checkpoints; the pipeline only works for intermediates expressible through the unembedding, so strategy-like or goal-like content is out of scope; the filler-vs-explicit-CoT comparison is a qualitative visual aggregate from one task.

## What we take from it
Monitorability should be framed as a property of the whole computational trace, not of the surface transcript. A cheap unsupsupervised recipe — cross-example mean subtraction + position aggregation + LLM judge — is a reusable decoding pattern and is one of the few "auditing a hidden-trace case" results with a causal leg. Good reference for the claim that loss of CoT readability does not imply loss of auditing, provided white-box access exists.

## Tags
filler-tokens, cot-monitorability, logit-lens, kv-cache-transplant, unsupervised-decoding, open-weights
