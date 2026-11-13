# Circuits Updates, February 2024

- **Key:** transformer-circuits-pub-2024-feb-update-index-html
- **Authors / organisation:** Anthropic interpretability team — Adly Templeton, Joshua Batson, Tom Henighan, Tom Conerly, Jonathan Marcus, Anna Golubeva, Trenton Bricken, Adam Jermyn
- **Date:** 2024-02
- **Link:** https://transformer-circuits.pub/2024/feb-update/index.html
- **Kind:** blog/research post (four short research notes, explicitly offered as lab-meeting material rather than a paper)
- **Read from:** full text (~9.3k characters — the whole page, all four notes); no figures inspected (the page contains none of its own; it refers to plots in *Towards Monosemanticity*)
- **Relevance to us:** 2 (useful) — it is an engineering post about sparse-autoencoder training pathologies, but two of its four notes are about *why a dictionary unit fails*, which is exactly the failure mode any weight- or feature-reading method we build will inherit.

## What they wanted, and why

Four loose ends left over from the monosemanticity paper, all about sparse-autoencoder training rather than about models: what the "ultralow density cluster" of dead-ish features actually is, which small architectural changes make wide dictionaries trainable, whether the ghost-grads trick deserves its reputation, and whether the well-known shrinkage problem of the L1 penalty can be fixed by swapping the penalty. The motivation is scaling: features that never fire consume dictionary capacity, so the width that buys interpretability is partly wasted, and a penalty that both sparsifies and shrinks makes every recovered feature weaker than the real one. The framing throughout is diagnostic candour — several of the claims are explicitly marked as superseded by the March 2024 update, which is itself the interesting methodological content.

## What they studied

Sparse autoencoders over transformer *MLP neuron activations* — the same objects as *Towards Monosemanticity* (pre-encoder bias, L1 penalty, dictionaries far wider than the neuron count), plus "larger models", "1L models" and "larger autoencoders" referred to by size class without naming a specific model. The unit of analysis is the dictionary feature, specifically its encoder and decoder vectors, its firing density, and its decoder norm. No circuits, heads or weights of the underlying model are examined.

## How they did it

(a) *Dying features:* reproduce Neel Nanda's observation that ultralow-density features share an almost identical encoder direction across random seeds while their decoder vectors look random, then break the weight vectors down by which transformer neurons they put mass on, compare against high-density features, and trace the shared direction to the pre-encoder bias — the encoder can implement a negative bias by loading opposite-signed weights onto the small set of neurons that never go quiet, and features that never find a decoder direction keep receiving gradients that push every other weight toward zero. (b) *Improvements:* an ablation list over SAE hyperparameters — Adam's first-moment coefficient set to zero, second-moment coefficient moved, ghost-grads death threshold shortened, decoder norm constrained to at most one instead of exactly one (which also licenses pruning features whose norm falls below a threshold after training), removal of the pre-encoder bias on real activations, input L2-normalisation by the square root of the dense width with MSE summed over the dense dimension so that hyperparameters transfer across model sizes, and a linear learning-rate cooldown over the final fifth of training. (c) *Ghost grads:* remove a bug that marked every neuron dead for the first K steps of training and compare training loss with and without it, then repeat at larger scale. (d) *Tanh penalty:* replace the L1 term with a saturating penalty of the form (A/B)·tanh(x·B) borrowed from the signal-processing literature, which retains the L1-sized gradient at the activation threshold but vanishes for strongly active features, then sweep both penalty parameters and several architecture variants, measuring the L0/loss-recovered frontier and a human/automated reading of feature density.

## What counts as an explanation here

A mechanical account of a training pathology: the shared encoder direction is explained as a consequence of bias implementation plus gradient flow, not merely described. For the architecture notes, the explanation is a causal one — change this hyperparameter, this class of failure goes away. It is partial by construction: the authors say outright that they do not understand why the tanh penalty inflates high-density features, and that they do not have a good theory of when ghost grads help.

## How they judged success

Training loss (MSE + L1, explicitly excluding the ghost-grads term), number of dying features, cosine similarity between encoder vectors, decoder-norm distribution, the Pareto frontier of L0 against loss recovered, the fraction of features above a high-firing-density threshold (reported only as "over 10%" for the tanh runs), and qualitative interpretability of the resulting features. There are no held-out behavioural benchmarks, no downstream probe tasks and no cross-model replication beyond the size classes mentioned in passing.

## What they found

*Dying features:* the ultralow-density cluster is not a mysterious artefact — those features put their whole encoder weight on the few transformer neurons that activate weakly across the entire dataset, which almost every feature does, but unlike healthy features they put almost no weight anywhere else; the common direction across seeds follows from the pre-encoder bias, since loading opposite-signed weights onto consistently non-zero neurons fabricates a negative bias. The conclusion is deflationary: it is the L1 penalty killing features before they find a direction. *Improvements:* beta1 = 0 gives the largest reduction in dying features, moving beta2 has a smaller effect, shortening the ghost-grads death window also helps but the three do not stack; allowing decoder norm ≤ 1 rather than = 1 helps and enables pruning at a 0.99 norm threshold; dropping the pre-encoder bias helps on real (as opposed to synthetic) activations; input normalisation by sqrt(dense width) plus summed MSE makes hyperparameters mostly transfer across width; a linear cooldown over the last 20% helps. *Ghost grads:* the bug that applied ghost grads to every neuron for the first K steps actually *improved* loss, and the authors downgrade their enthusiasm — a large win on 1-layer models, little difference on larger ones, no theory of why. *Tanh penalty:* a Pareto improvement on L0 against loss recovered, often substantially, which they read as confirmation that L1 shrinkage was limiting loss recovery — but the resulting dictionaries contain many more high-density features, the top ones above 10% firing, and were much harder to interpret; neither parameter sweeps nor architecture tweaks fixed it, and the obvious "it's just accumulated gradient toward zero" theory fails because turning up the penalty did not remove the high-density features. The note ends by pointing at work suggesting shrinkage can be handled by fine-tuning a subset of parameters without any sparsity penalty.

## Limits and open problems they name

Every note is a lab-notebook entry: size classes rather than named models, single-lab replication, no error bars, no held-out evaluation of whether the "improved" dictionaries are more useful downstream. Two of the four notes carry their own retraction banner pointing at the March 2024 update, so the page as it now stands is a snapshot the authors have partly walked back. The tanh direction is shelved, not resolved, and the link between a saturating penalty and high firing density is left unexplained. Ghost grads is described as an empirical trick whose mechanism they do not have.

## What we take from it

Three things. First, a *warning* that carries straight into our setting: a dictionary unit that looks like a meaningless high-similarity direction can be an artefact of a bias term rather than a property of the network, so before reading any recovered direction as a feature we should check which units carry its weight and whether it coincides with a constant offset. Second, a *diagnostic habit*: the paper explains a training failure by looking at where the weight mass sits, per input unit — the same move we want when asking which parts of a network a probe is actually reading, and it is cheap. Third, a *measurement caution* about the trade between faithfulness and legibility: the tanh penalty demonstrably recovers more of the MLP loss while producing dictionaries nobody can read, which is the cleanest available illustration that "loss recovered" and "interpretable" can move in opposite directions, and a reason to report both rather than either. The March-update banners are a reminder to date-stamp any hyperparameter recipe we inherit from this thread.

## Tags

unit: feature
form: dictionary
method: SAE
eval: ablation
goal: understanding
