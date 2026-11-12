# Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task

- **Key:** arxiv-2210.13382
- **Authors / organisation:** Kenneth Li, Aspen K. Hopkins, David Bau, Fernanda Viégas, Hanspeter Pfister, Martin Wattenberg; Harvard, MIT, Northeastern
- **Date:** 2022-10
- **Link:** https://arxiv.org/abs/2210.13382
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Do sequence models trained only to predict the next token just learn surface statistics, or do they build an internal model of the process that generates the data? Othello is a clean test: the board state is fully determined by the move sequence but never shown to the model. The authors probe for a board representation and then intervene on it to check it is causally used, aiming at tools that might later reveal world models in language models.

## What they studied
Othello-GPT: an 8-layer GPT with 8 heads and 512-dim residual stream, vocabulary of 60 move tokens, no rules or board given. Two training sets: a championship set (about 140k expert games, split 8:2) and a synthetic set of 20 million games of uniformly random legal moves (about 3.8 million validation). Unit: residual-stream activations per layer, per tile.

## How they did it
They first check the model predicts legal moves. They then train per-tile probes (black / white / empty) on each layer's activations, both linear and two-layer MLP, comparing against probes on a randomly initialised model. For causality, they take a board state and a counterfactual differing in one tile, and edit the activation at the last token by gradient descent on the probe's loss until the probe reads the counterfactual; edits are applied from a start layer through all later layers so downstream computation does not overwrite them. They then check whether the model's predicted legal moves match the counterfactual board, on natural positions and on positions unreachable in real play. Finally, "latent saliency maps" intervene on each tile's representation and measure the drop in probability of the top move.

## What counts as an explanation here
A nonlinear probe that reads a world-state variable (the board) from activations, plus evidence that editing that variable changes outputs as the world model predicts. A partial, variable-level account; no mechanism for how the board is computed.

## How they judged success
Legal-move top-1 error. Probe error per layer versus a randomised-model baseline and a 52.95% chance-level majority baseline. For interventions: average number of errors between predicted and counterfactual legal-move sets (1,000 cases per benchmark), versus the pre-intervention prediction as baseline; F1 and KL in an appendix; probe variability across 100 seeds.

## What they found
Legal-move error: 0.01% (synthetic), 5.17% (championship), 93.29% untrained; 0.02% even when one opening was withheld from training. Linear probes never get below about 20% error. MLP probes on the synthetic model fall to 1.7% at layer 7 (championship best 9.4% at layer 4; random model about 25%). Intervening from layer 4 onward gives 0.12 average errors on natural positions (baseline 2.68) and 0.06 on unnatural ones (baseline 2.59). Saliency maps are concentrated on legality-relevant tiles in the synthetic model and diffuse in the championship model.

## Limits and open problems they name
The representation is not linearly decodable in their parameterisation, making it harder to read. Intervention fails in shallow layers and is weak if only the deepest are edited. Saliency finds only the first contributing tile when legality is an OR over directions. One small model and one game; transfer to language untested.

## What we take from it
A protocol for "is this variable real and used": probe, then intervene to a counterfactual (including off-distribution states) and score whether outputs follow the predicted change. That counterfactual-consistency score is close to what our white-box model should be judged on. Warning: a probe's success depends on choosing the right basis (not from this paper: follow-up work reported a linear encoding in a player-relative "mine/theirs" basis), so failure of a linear readout is not proof of nonlinearity.

## Tags
unit: direction | layer
form: probe
method: probing | steering | patching
eval: patching | prediction/simulation
goal: science | understanding
