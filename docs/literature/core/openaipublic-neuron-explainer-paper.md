# Language Models Can Explain Neurons in Language Models

- **Key:** openaipublic-neuron-explainer-paper
- **Authors / organisation:** Steven Bills, Nick Cammarata, Dan Mossing, Henk Tillman, Leo Gao, Gabriel Goh, Ilya Sutskever, Jan Leike, Jeff Wu, William Saunders; OpenAI
- **Date:** 2023-05-09
- **Link:** https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html
- **Kind:** paper
- **Read from:** full text (body text extracted from the page's JavaScript bundle; figures not viewed)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Full understanding of a language model would need explanations for millions of neurons, far beyond manual effort. The
authors automate neuron explanation with GPT-4 and, crucially, define a quantitative "explanation score": how well a
language model can reconstruct a neuron's activations from a short natural-language explanation. This turns
interpretability into something measurable, so progress can be tracked. The long-term goal is AI-assisted
interpretability strong enough for safety audits (e.g. detecting deceptive alignment), as an instance of using capable
models to help alignment research.

## What they studied
Subject models: all 307,200 MLP neurons of GPT-2 XL (GELU post-activations); GPT-2 small layer 10 for direction search;
GPT-3-series models from 98K to 6.7B parameters and their half/quarter-trained checkpoints for scaling trends; ~3M
parameter models trained from scratch with top-k sparse activations. Explainer and simulator: GPT-4 by default, with
weaker models for scaling studies. Data: random 64-token excerpts of the subject's pre-training data (WebText for
GPT-2). Unit: neurons, plus learned linear combinations of neurons ("virtual neurons").

## How they did it
Three steps per neuron. (1) Explain: GPT-4 sees tab-separated (token, activation) pairs from 5 top-activating excerpts
(drawn from the top 20 of 50,000 sequences), with activations rescaled to integers 0-10, plus few-shot examples with
researcher-written explanations, and writes a short explanation. (2) Simulate: a simulator, given only the explanation,
predicts a 0-10 activation for every token; the expected value under its digit probabilities is used, and an
"all at once" prompt trick simulates every token in one pass. (3) Score: compare simulated and true activations on held-out
excerpts, either 5 random excerpts ("random-only") or 5 top plus 5 random ("top-and-random"). The score is the
correlation, which equals explained variance after optimal linear calibration. They validate the score with an ablation
score (replace the neuron with its calibrated simulation and measure Jensen-Shannon divergence of outputs, normalised by
mean-ablating the neuron) and with human raters ranking 5 candidate explanations. Baselines predict activation per
token from weights (embedding times layer-norm gain times W_in), from a token lookup table of mean activations, or from
the next token. Extensions: a revision loop where GPT-4 writes 10 sentences fitting the explanation, the neuron is run on
them to find false positives, and GPT-4 revises; and gradient-based search for well-explained directions (whitened
linear combinations of neurons, alternating explanation and gradient-ascent steps). They also built 19 synthetic
"neuron puzzles" with known ground-truth explanations to test the explainer and scorer separately.

## What counts as an explanation here
A short natural-language statement of which input tokens (in context) make a neuron fire. It is treated as a predictive
model of the neuron: explanation plus simulator is a "simulated neuron" that outputs activations on any text. It
explains correlations on a fixed distribution, not mechanism, and is explicitly partial.

## How they judged success
Correlation score (random-only and top-and-random); ablation score (1 minus normalised JSD of simulated versus mean
ablation); human preference agreement; comparison with unigram baselines (weight-based linear token prediction, token
lookup table) and a human-contractor explanation baseline; puzzle accuracy (does the explainer recover the ground truth,
and does the scorer rank the true explanation highest among false ones). Error bars are 95% CIs.

## What they found
Average GPT-2 XL score was 0.151 top-and-random and 0.037 random-only; scores fall with depth. Of 307,200 neurons,
5,203 (1.7%) scored above 0.7 top-and-random and 189 above 0.9; over 1,000 scored at least 0.8. A correlation score of 0.9
still gave ablation scores of only about 0.3 (random-only) and 0.6 (top-and-random), so correlation misses functionally
important detail. The weight-based token baseline beats explanations only in layer 0; the token lookup table beats
activation-based explanations on average. Revision raised scores; 42% of generated test sentences were false positives,
and 86% of neurons had at least one, so explanations are typically too broad. Optimised directions in GPT-2 small layer 10
averaged 0.718 versus 0.147 for neurons and 0.061 for random directions. Scores improved with explainer and simulator
capability, but non-expert humans only slightly beat GPT-4 and both were low in absolute terms. Larger subject models and
deeper layers were less explainable; sparser activations and ReLU raised scores at a loss cost. On puzzles the explainer
solved 5/19 (plus 4 with revision) while the scorer ranked the truth first on 16/19, so the explainer is the bottleneck.
A "from"-predicting late-layer neuron turned out on ablation to slightly suppress "from" and boost "form".

## Limits and open problems they name
Neurons are polysemantic and may not be summarisable briefly; models may use concepts humans lack words for;
explanations capture correlations, not mechanisms, so may generalise wrongly out of distribution; the simulator may not
match how a human reads an explanation (possible steganography between explainer and simulator); false positives are
under-sampled, so high-recall, low-precision explanations score well; the hypothesis space covers single neurons only,
not circuits; compute and tokenisation problems.

## What we take from it
The explain-simulate-score loop is the field's standard definition of "an explanation predicts activations", and the
measure we should report against. Two warnings for us: correlation on activations overstates functional faithfulness
(use the ablation/replacement score, i.e. substitute the prediction back into the network and measure output
divergence), and top-activation sampling hides false positives (score on random and adversarial inputs). The
weight-based unigram baseline (W_E times W_in) is a ready weight-reading baseline that is near-perfect at layer 0 and
degrades after; a predictive white-box model from weights must beat it and the token lookup table. Synthetic puzzles
with planted ground truth are a template for validating our own explainer.

## Tags
unit: neuron | direction
form: description
method: agent | other
eval: prediction/simulation | ablation | human-rating
goal: understanding | safety/auditing | evaluation-of-methods
