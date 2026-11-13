# Circuits Updates, July 2023

- **Key:** transformer-circuits-pub-2023-july-update-index-html
- **Authors / organisation:** Adam Jermyn, Chris Olah, Tom Henighan, Tom Conerly; Anthropic (Transformer Circuits Thread)
- **Date:** 2023-07
- **Link:** https://transformer-circuits.pub/2023/july-update/index.html
- **Kind:** blog/research post (lab research-notes roundup, three short updates)
- **Read from:** full text (all three updates — the page is ~12.7k characters of prose plus an appendix note on the finite-data regime; no figures were inspected)
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Three loose ends from earlier work, reported informally and each explicitly framed as a lab-meeting item rather than a mature paper. First: the finite-dataset toy model from *Superposition, Memorization, and Double Descent* had an intermediate dataset-size band where the authors could not say what the network was doing — a potential counterexample to their own "features as directions in superposition" picture, which they felt obliged to resolve one way or the other. Second: a standing question of where mechanistic work should aim if it is to matter for safety, answered by listing candidate targets rather than by experiments. Third: an attention-head "superposition" example from the previous year's skip-trigram model whose algorithm they had not understood, which they revisited on a smaller model. The unifying motive is the survey's central one — whether the standard feature picture survives the cases that embarrass it.

## What they studied

(a) The one-layer finite-data toy model of the earlier post, i.e. a network trained on a fixed sample of N sparse random features, analysed across dataset size rather than across architecture. (b) No models at all — a conceptual taxonomy of safety-relevant mechanisms and behaviours, at the level of "units of computation" they call features, spanning input properties, intermediate knowledge and output actions. (c) A two-head attention-only model trained on OV-incoherent skip-trigrams: triples where every trigram begins with the same token, so one head cannot implement several of them at once (as in the same token's `[0]…[1]→[4]` and `[0]…[2]→[5]`). Units of analysis: dataset size and learned strategy (a); hypothesised feature types (b); individual heads and a two-head composition (c).

## How they did it

For the finite-data regime they trained the same toy at several learning rates, on the argument that a strategy whose loss is worse at every learning rate is not merely hard to find but genuinely worse, and then tracked which of the two known solutions (memorising the samples versus learning the generating features) attains the lower *train* loss as dataset size grows; the crossover between the two curves and the behaviour of the derivative of the minimum loss across the crossover are the evidence for calling it a phase transition. Alongside this they looked at how the memorising solution's geometry changes as datasets approach the crossover, from individually stored points to clustered structure. For the safety list they enumerate hypothesised mechanisms (high-level actions, planning, social reasoning, personas, situational awareness) and empirical behaviours whose mechanism is unknown (jailbreaks, instrumental-looking behaviour, in-context learning, why RLHF works), pairing each with the question a mechanistic account would settle. For the skip-trigram model they analysed a simpler two-head model, derived the algorithm by hand, and checked that this algorithm reconstructs the task's outputs, then compared it with what training actually produces, noting that trained models divide the trigram set between heads rather than cleanly separating the two jobs.

## What counts as an explanation here

(a) A regime *reclassification*: the unexplained band is claimed to be an optimisation failure on a low-dimensional problem rather than a third computational strategy, so the explanation is a two-regime account plus a training-path diagnosis — complete for the toy, predictive only as "if optimisation is good enough, only memorising and generalising survive". (b) Not an explanation at all but a research agenda: a list of targets, with no claims about mechanisms. (c) A full weight-level algorithm for the two-head model: head 0 attends a token to itself and raises the logit for that token's continuation, head 1 attends the shared opening token when it is present (doing nothing) and otherwise attends the current token while emitting the negative of head 0's contribution, so the pair computes a conditional — correct trigram logits when the opener is in context, an effectively uniform output when it is not. Partial in the sense that it explains the simplified model, and the authors retreat from calling the original multi-head case literal head superposition.

## How they judged success

No metrics, benchmarks or baselines anywhere — success is qualitative: whether an anomalous regime can be accounted for by a known failure mode with an argument that mistakes it for a distinct strategy, whether a by-hand algorithm matches the trained model's behaviour and reproduces its outputs, and (for the safety list) nothing measured at all. The one quantitative-flavoured claim is a crossover near 500k samples where the two solutions exchange which has the lower train loss, with a discontinuity in the derivative of the minimum loss — reported as an observation, without error bars.

## What they found

The intermediate regime was an artefact of a hard low-dimensional optimisation problem: the memorising solution keeps the lower train loss all the way to very large datasets (order 500k samples), where a genuine first-order transition hands the advantage to the generalising solution, with the derivative of the minimum loss jumping at the crossover. Approaching that transition, the memorising solution changes character — from storing mutually-orthogonal individual points below roughly 1k samples, where exact memorisation is possible, to memorising *correlated clusters* of points that share features once correlations make exact storage impossible, with a characteristic triangular arrangement inside clusters. The two-head model's algorithm above accounts for many OV-incoherent skip-trigrams at zero loss, but real trained models split the trigrams between heads, so the authors are no longer confident the earlier example deserves the name attention-head superposition in the strict feature-as-direction sense. The safety list contributes no results, only framings: LLM-relevant features may include actions and multi-token behaviours, and personas are singled out as possibly the thing that organises the rest after RLHF.

## Limits and open problems they name

The optimisation-failure diagnosis is attributed to the toy's low hidden dimension, and the authors say they do not expect it to be nearly so prevalent in realistic models — an assertion, not a tested claim. The transition point is one number from one toy; no scaling behaviour of it is reported. The skip-trigram analysis covers a simplified two-head model, and they explicitly lower their confidence in the earlier "superposition" interpretation rather than replacing it with a full account of the multi-head model. The persona discussion lists questions they say they cannot yet answer (whether any behaviour bypasses personas, whether personas are separable from social reasoning, whether RLHF creates circuits or only selects among pretrained ones) and offers no evidence. By their own framing, none of this is more than a provisional idea.

## What we take from it

- **A method, and a warning.** Learning-rate sweeps as a test of whether a regime is real or an optimisation artefact: underfit strategies lose at every learning rate, whereas genuinely better-loss solutions exist at some. Before our white-box model reports a third computational strategy, sweep the optimiser and report whether the strategy is the loss-optimal one.
- **A reframing of the memorisation manifold.** "Memorising individual points" and "memorising correlated clusters" are different readable structures with the same label, and the switch is predicted by correlations that make exact storage impossible. Any detector we build for example-specific storage should separate cluster-memorisation from point-memorisation, since the earlier toy-post reading (clean polytopes over examples) described the small-N uncorrelated case.
- **A failed mechanism label.** A behaviour that looked like superposition turned out to be a conditional computed across two heads with cancelling outputs, so what is stored is not one direction per trigram. Composition and cancellation defeat single-head readings — and cancellation specifically is a mechanism a probe will never see and an ablation will never remove.
- **A research-agenda shortcut.** The persona framing (models track personas and follow cues to change them; RLHF may lock one in) anticipates the direction the field later took, so this page is worth citing as the early statement of the target set rather than for anything measured.

## Tags

unit: whole-model | head
form: description | program
method: other | weight-analysis
eval: prediction/simulation
goal: understanding | safety/auditing
