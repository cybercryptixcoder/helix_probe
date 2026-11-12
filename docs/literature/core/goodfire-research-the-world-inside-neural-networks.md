# The World Inside Neural Networks

- **Key:** goodfire-research-the-world-inside-neural-networks
- **Authors / organisation:** Atticus Geiger, Ekdeep Singh Lubana, Thomas Fel, Jack Merullo, Michael Jae Byun, Owen Lewis, Tom McGrath; Goodfire
- **Date:** 2026-05-07
- **Link:** https://www.goodfire.com/research/the-world-inside-neural-networks
- **Kind:** survey/agenda
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
This post opens Goodfire's "Neural Geometry" series and sets out the agenda. The claim is that networks build internal representations whose shape mirrors structure in the world (cyclic days and months, a smooth curve for years, a hue-organised colour surface), because training data reflects that structure and optimisation compresses it. Since computations operate on these representations, the authors argue one cannot understand a network's algorithms without first understanding the geometry of what they operate on. They position this as the next frontier for both understanding and controlling models.

## What they studied
No new systematic study. Illustrations: an image-action world model trained to predict the next frame of the Mountain Car task (car position embeddings form a curve), and a slant-rhyme manifold in a language model found with a forthcoming unsupervised pipeline. Many cited results on circular, linear and curved structures in language, vision and a genomics model are summarised rather than reproduced.

## How they did it
For Mountain Car they fit a 1-D manifold to position embeddings and steer along it, comparing with straight-line interpolation between positions. For the rhyme example they show the manifold tracking phonological endings and list the 23 SAE features that together reconstruct it, noting their labels are mostly local, lexical patterns. The rest is argument, supported by citations.

## What counts as an explanation here
A three-level target: the model's ontology (how it carves up and represents concepts, including their geometry), the algorithms operating over those representations, and the behaviours they produce. Explanations should respect curvature rather than flatten concepts into single directions. The post is explicit that geometry alone is a first step, not the full explanation.

## How they judged success
Qualitative only: whether steering along the fitted manifold moves the car smoothly versus linear interpolation passing through garbled frames or jumping to other positions; whether SAE features describe the rhyme manifold coherently. No metrics, benchmarks or error rates.

## What they found
Steering along the fitted Mountain Car manifold moved the car smoothly up the hill, while linear interpolation passed through broken states and sometimes made the car jump. The rhyme manifold is split by SAEs into many unrelated-looking local features, which the authors describe as the SAE "shattering" it. Detailed versions appear in later posts (see arxiv-2605.05115, arxiv-2604.28119).

## Limits and open problems they name
Evidence here is illustrative (a toy world model and one rhyme case). The discovery pipeline is deferred to later work. "Linear representation" is ambiguous and some definitions allow curvature, so the contrast depends on a narrower usage. Open: supervised and unsupervised methods that respect geometry, linking geometry to computation and behaviour, and longer-term uses such as predicting failures, auditing, and shaping training.

## What we take from it
A framing for what our white-box model should contain: variables with their natural geometry (ontology), the operations on them (algorithm), and the resulting behaviour, in that order. It also sets a bar: a reconstruction that reproduces behaviour with flat linear variables may still misrepresent the network's ontology and fail under interventions that move along curved concepts.

## Tags
unit: direction, other (manifold)
form: other (geometric representation / ontology)
method: steering, SAE, other (position piece)
eval: other (qualitative)
goal: understanding, control/editing
