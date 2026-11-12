# Mechanistic Interpretability, Variables, and the Importance of Interpretable Bases

- **Key:** tcpub-2022-mech-interp-essay
- **Authors / organisation:** Chris Olah; Anthropic
- **Date:** 2022-06-27
- **Link:** https://transformer-circuits.pub/2022/mech-interp-essay/index.html
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
An informal note setting out the intuition behind mechanistic interpretability. Olah argues the field is like
reverse-engineering a compiled program, and that the central task is finding the network's "variables": units into
which activations decompose, each understandable on its own. He wants to explain why a privileged, interpretable
basis matters so much and why polysemanticity is the main obstacle.

## What they studied
No experiments. The objects of discussion are parameters (as program instructions), activations (as memory), and
neurons or feature directions (as variables), with attention-only transformers mentioned as a special case.

## How they did it
Argument by analogy. Parameters are a binary running on the architecture as a virtual machine; activations are
memory. Because input space is too large to enumerate, understanding has to come from a finite description of the
mechanism (the weights), just as a programmer reads code rather than testing all inputs. But a parameter's meaning
depends on what its input and output activations mean, so activations must first be segmented into variables.
Programs often lay memory out simply; networks with activation functions may do the same, making neurons natural
units (a privileged basis). Polysemantic neurons break this. An FAQ discusses distributed representations, how to
define "feature", and modularity versus interpretable features.

## What counts as an explanation here
Understanding means decomposing representations into independently meaningful parts and then understanding the
operations (weights) between them; a finite, non-exponential description of the mechanism, not a summary of
input-output behaviour or local saliency.

## How they judged success
Not applicable (essay). Implicitly: whether a decomposition yields parts each with a coherent meaning.

## What they found
Claims: variables are the crux; interpretable bases make reverse-engineering far easier but are not strictly
required; a program with no coherent variables is close to hopeless to understand; distributed codes are
compatible with interpretable neurons up to rotation; there is no simple recipe and the effort will be large.

## Limitations and open problems they name
No good, human-independent definition of a feature (the definition should separate a car detector from a
"car and cat" detector); how to decompose polysemantic activations; how modularity relates to features.

## What we take from it
A clean framing for our goal: weights are the program, but they can only be read once the variables are fixed, so
a white-box reconstruction needs both a basis for activations and a reading of the weights between them. The
argument that understanding must be a finite description rather than enumeration supports building a model from
weights instead of from probing many inputs. Its unsolved "what is a feature" question is one our method must take
a position on.

## Tags
unit: neuron, feature, weights
form: program, description
method: other
eval: (none)
goal: understanding, science
