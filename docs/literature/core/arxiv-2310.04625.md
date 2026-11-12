# Copy Suppression: Comprehensively Understanding an Attention Head

- **Key:** arxiv-2310.04625
- **Authors / organisation:** Callum McDougall, Arthur Conmy, Cody Rushing, Thomas McGrath, Neel Nanda; independent researchers, University of Texas at Austin, Google DeepMind
- **Date:** 2023-10
- **Link:** https://arxiv.org/abs/2310.04625
- **Kind:** paper
- **Read from:** full text (arXiv HTML; the tail of Appendix J was not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Most circuit work explains a component only on one narrow task. The authors wanted to explain a single component's behaviour across the whole training distribution, and to quantify how much of it their explanation covers. They picked GPT-2 small head L10H7, a "negative head" that had appeared in earlier circuit work (as a negative name mover in IOI) seemingly working against the right answer. The larger goal is to show what a comprehensive, weight-grounded account of one component looks like and how to score it, and to explain self-repair.

## What they studied
GPT-2 small, head L10H7 (with L11H10 as a second negative head), on OpenWebText; the Indirect Object Identification (IOI) task for self-repair; brief checks on GPT-2 Medium and Pythia models. Units: one attention head, analysed through its OV and QK weight matrices and its activations.

## How they did it
They first looked at where the head matters most: the 5% of OpenWebText positions where mean-ablating it most increases loss, and checked whether those cases match a three-step story (an earlier component predicts a token already in context; the head attends to that earlier token; the head lowers that token's logit). They then studied the weights directly: the OV circuit composed with the unembedding, applied to an "effective embedding" (token embedding passed through MLP0, since MLP0 output better represents tokens in GPT-2 small), checking whether each token most strongly suppresses itself; and the QK circuit, checking whether a query carrying a token's unembedding attends most to that token's key, against a baseline that only matches similar vectors. Next they built Copy Suppression-Preserving Ablation (CSPA): mean-ablate everything about the head except the copy-suppression parts (on OV, keep only the negative projection of each source's output onto that source token's unembedding; on QK, allow attention only to source tokens among the top predictions at the destination). Comparing CSPA to full mean ablation measures how much of the head's effect the story covers. Finally, they measured how much of IOI self-repair is due to copy suppression, and examined backup heads.

## What counts as an explanation here
A mechanistic description of one head (attend to tokens already predicted, then push those tokens down) that is turned into a constrained ablation: a simplified version of the head that keeps only what the explanation says matters. The share of behaviour that simplified head reproduces is the score. It is explicitly partial, and the authors report how much is left unexplained.

## How they judged success
Main metric: fraction of the head's effect explained = 1 minus (mean KL under CSPA divided by mean KL under mean ablation), over OpenWebText, also broken down by impact percentile. Secondary: share of net and absolute loss change explained. Weight-based statistics: how often a token's own diagonal entry is among the 10 most negative in the OV matrix (and bottom 5%), how often the QK diagonal is the row maximum, with a same-matching baseline. For self-repair: fraction of the IOI self-repair attributable to negative heads.

## What they found
CSPA explains 76.9% of L10H7's behaviour by the KL metric (88.1% in the top-impact percentile); OV-only simplification keeps 81.1% and QK-only 95.2%. On weights, 84.70% of tokens rank in the top 10 most suppressed by their own OV column (98.86% in the bottom 5%), and 95.72% of QK diagonal entries are row maxima, well above the matching baseline. Measured by loss, the explanation covers 82% of net loss change but only 45% of absolute loss change, which shows the score depends strongly on metric choice. Copy suppression accounts for 39% of self-repair in IOI; backup heads self-repair by a different route, and much of the relevant signal lies outside the unembedding direction. The behaviour links to anti-induction heads and appears weakly in other models.

## Limits and open problems they name
The QK analysis uses an idealised input setup; query-side inputs to self-repair are not understood; signal outside unembedding directions matters but is unexplained; no account of when and how strongly suppression activates; transfer to larger models unknown; KL divergence can miss low-probability effects; theories for why negative heads form are speculative.

## What we take from it
(1) A measurable notion of "how much of a component we understand": build an ablation that preserves only the hypothesised mechanism and report fraction of KL recovered vs mean ablation. This is directly reusable as a score for a white-box reconstruction of any component. (2) Weight-based checks (OV/QK composed with embeddings and unembeddings, with diagonal-rank statistics and a null baseline) are a template for reading function from weights without running the model. (3) Use the effective embedding (after MLP0) rather than raw token embedding when reading GPT-2 weights. (4) Warning: report several metrics; the gap between 82% net and 45% absolute loss explained shows one number can flatter an explanation. (5) Even a best-case single head reached about three quarters; budget for residuals.

## Tags
unit: head
form: description, causal-abstraction
method: weight-analysis, ablation, patching
eval: ablation, faithfulness, completeness
goal: understanding, science, evaluation-of-methods
