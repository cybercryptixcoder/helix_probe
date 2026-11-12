# Patchscopes: A Unifying Framework for Inspecting Hidden Representations of Language Models

- **Key:** arxiv-2401.06102
- **Authors / organisation:** Asma Ghandeharioun, Avi Caciularu, Adam Pearce, Lucas Dixon, Mor Geva; Google Research, Tel Aviv University (ICML 2024)
- **Date:** 2024-01
- **Link:** https://arxiv.org/abs/2401.06102
- **Kind:** paper
- **Read from:** full text (HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Many methods decode hidden states (logit lens, tuned lens, probes, future lens), each with its own limits: vocabulary
projections fail in early layers, probes need labels and a fixed label set. The authors propose using the model's
own generation ability to describe a hidden state in natural language, and show that this one idea covers many
existing methods as special cases and opens new ones (cross-model inspection, fixing reasoning errors).

## What they studied
LLaMA2 13B, Vicuna 7B and 13B, GPT-J 6B, Pythia 6.9B and 12B. Unit: a single hidden state at one layer and position.
Data: Pile samples, relation tasks from Hernandez et al. (commonsense and factual attributes), PopQA entities,
generated two-hop questions.

## How they did it
A Patchscope is specified by a source (prompt, model, layer, position) and a target (prompt, model, layer, position)
plus a mapping function. The hidden state is taken from the source run, mapped (identity, affine, or learned), and
written into the target run, which then continues and generates. Logit and tuned lens are special cases (patch into
the final layer with identity or affine map). Experiments: (1) next-token prediction from intermediate layers using a
training-free few-shot "token identity" target prompt, compared with
logit and tuned lens on 2,000 held-out Pile samples; (2) attribute extraction: patch a subject's hidden state into a
zero-shot prompt that verbalises the relation, compared with per-layer logistic-regression probes; (3) entity
resolution: patch into a few-shot "describe this entity" prompt and compare generated descriptions with Wikipedia;
(4) cross-model patching with learned affine maps from smaller to larger models in the same family; (5) correcting
two-hop reasoning by patching the answer of the first hop into the position where the second hop needs it.

## What counts as an explanation here
A natural-language or token readout of what a hidden state encodes, produced by the model itself in a chosen target
context. It is a decoder, partial and query-specific. In the multi-hop case it is also an intervention that fixes
behaviour, which is a weak form of prediction.

## How they judged success
Precision@1 and surprisal for next-token prediction (baselines: logit lens, tuned lens); accuracy against linear
probes for attribute extraction, with significance tests; RougeL (also Rouge1, SBERT) against Wikipedia descriptions
for entities; precision for cross-model patching; accuracy on two-hop queries vs vanilla generation and chain of
thought.

## What they found
- From layer 10 upward the token-identity Patchscope beats logit and tuned lens on next-token prediction, with gains up
  to 98% in layers 18–22; in early layers it is on par with logit lens and the tuned lens is slightly better.
- Zero-shot attribute extraction beats trained probes on 6 of 12 tasks (e.g. company CEO 5.0% to 47.8%) and loses on
  one; it degrades in later source layers.
- Entity descriptions improve over the first ~5 layers then decline, showing entities resolve gradually; rare entities
  score lower.
- Affine cross-model maps reach precision about 0.7 (Vicuna) and 0.8 (Pythia); patching 7B states into 13B helps entity
  description for Vicuna but not for Pythia.
- Two-hop correction on 46 eligible queries: 50% vs 35.7% (chain of thought) and 19.6% (vanilla).

## Limits and open problems they name
Only autoregressive transformer LMs; placeholder token contamination in the target prompt; worse readout from late
layers; cross-model maps only within families and not always helpful; multi-hop fix needs hand-chosen positions and a
tiny test set; prompt sensitivity checked only for one model.

## What we take from it
- **Framing:** a single source-target patching template covers lenses and causal tracing; good vocabulary for
  describing our own interventions.
- **Method:** using the network as its own decoder is a strong baseline against which any weight-derived readout of a
  hidden state should be compared.
- **Warning:** readouts depend heavily on the target prompt and on the decoder's own computation, so they say what is
  decodable, not what the model uses; that is the opposite of the faithfulness we need.
- **Measure:** precision@1 and surprisal vs logit/tuned lens are standard comparisons for any per-layer prediction
  decoder.

## Tags
unit: layer, direction
form: description, probe
method: patching
eval: downstream-task, benchmark, prediction/simulation
goal: understanding, evaluation-of-methods
