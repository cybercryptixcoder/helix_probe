# A Shared Subcircuit Lets LLMs Count Down Across Tasks

- **Key:** arxiv-2607.12279
- **Authors / organisation:** Jacob Dunefsky; Wes Gurnee; Emmanuel Ameisen — Yale University; Anthropic
- **Date:** 2026-07-14
- **Link:** https://arxiv.org/abs/2607.12279
- **Kind:** paper
- **Read from:** full text (HTML body through conclusion and references; no limitations section in this version)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Many capabilities amount to knowing how much output is left before a stopping condition — writing a
twelve-word sentence, closing a DNA string at the right triplet, padding an ASCII table column to a fixed
width. The authors want one mechanism, not one mechanism per task, so that a behaviour learned from a single
controlled example can be predicted to appear elsewhere. The larger bet is that subcircuits, like subroutines
in a program, are the level at which behaviour generalises: reusing a circuit explains transfer across tasks,
and an identical motif in a different model would explain transfer across models. Their framing is explicitly
"reverse-engineer one task, then find where else the part is used".

## What they studied
A single model, Llama-3.1-70B-Instruct, with grouped-query attention. The unit of analysis is a *subcircuit*:
three attention heads at layer 18 (L18H24, L18H28, L18H30) sharing one key-value head, plus the key/query
representations they read. Two task families: a "sentence planning" task (write a k-word sentence ending in a
given word, length stated explicitly) and a "repeated string" setting (prompts containing several delimited
strings of equal length — backtick-delimited base64, or DNA sequences between `5'-` and `-3'`), where the target
length is only implicit.

## How they did it
Localisation: paired prompts with the same ending word but different target lengths, where the shorter-length
output is a prefix-consistent version of the longer one; they truncate the long output at the short length and
patch the short prompt's residual stream into the long prompt at the target-length token and at the "word"
length-unit token, layer by layer, reading the logit of the ending word. If the patched sentence ends early, the
patched site carried the length. Head identification: output norms of all layer-18 heads from the length-unit
token to downstream positions, normalised by sentence fraction, to see which heads fire as the end approaches.
Implicit-length causality: patch the ending-delimiter activations of shorter strings into a prompt whose
strings are longer, then read the first character position where the model's most likely token is the closing
delimiter — a predicted string length, scored against the source length with an unpatched baseline and an
unpatched-source roofline. Representation similarity: cosine similarity between key activations at delimiters of
different prompt types and at explicit length tokens, checking that the best match is unimodal and that the
length map between prompt types is close to a fixed multiplicative constant. Geometry: centred key and query
cosine matrices plus a 3D PCA projection, looking for a diagonal (query position matching key length) and the
"ringing" pattern off-diagonal. Generality: difference-of-means probes built from layer-18 head outputs at a
fixed distance from sentence end, run over a 10k-chunk subset of the Pile and a 5k-conversation subset of
LMSYS-1M, keeping chunks above a heuristic activation threshold and labelling them with a frontier model plus
manual selection.

## What counts as an explanation here
A circuit: a named, small set of components (three heads) whose read is specified geometrically — keys encode
target length on a curved manifold, queries encode current position on a similar manifold, and attention weight
is high where position is close to the target. It is partial by design (they do not decompose the heads' work
further), but it is predictive in a specific sense: given the length stored at a delimiter, you can say where
the head outputs should be largest and what the model will do next. Generality is claimed, not just locality —
the same component is argued to be active on a wide list of tasks.

## How they judged success
Residual-stream patching recovery of the target word's normalised logit by layer; head-output-norm profile over
normalised output position; a predicted-string-length error metric with unpatched baseline and roofline, averaged
over five runs per (destination, source) length pair; bimodality/linearity of cross-type cosine similarity with
r² over prompt-type pairs; diagonal alignment in cosine and PCA plots; probe hit rate on unlabeled corpora with a
qualitative, human-selected catalogue of themes. No ablation of the three heads themselves in this version, and
no scored benchmark for the probe catalogue.

## What they found
Length information becomes causally available at the length-unit token from about layer 4 and is last used there
at layer 18, after which patching it no longer changes the ending logit — consistent with the information being
copied out to later positions by heads at that layer. Exactly three layer-18 heads carry it, with overlapping
windows — one early in the sentence, one mid, one at the end — so their combined output rises smoothly and peaks
just before the target length for every target length, i.e. a continuous countdown rather than a threshold. The
model performs the sentence task nearly exactly for targets below eleven words, with error growing slowly above
that. In the repeated-string setting, patching delimiter activations moves the predicted length of the next
string nearly all the way to the source length, showing the length is stored where the string ends. Explicit
length tokens and implicit delimiter activations are cross-readable: cosine similarity is unimodal across prompt
types and the length mapping between types is highly linear (r² between 0.93 and 0.97). The key/query geometry
matches a motif previously reported in Claude 3.5 Haiku on a line-wrapping task, which they read as the same
motif appearing in two models. Probes fire on Twitter-length text embedded in articles, DNA spans, coin-toss
sequences, SHA-256 hex hashes, haiku lines, rounded decimal numbers, and ASCII table cells — including cases
where the target length is never stated but must be inferred.

## Limits and open problems they name
The paper's own caveats are modest, and it has no dedicated limitations section. They note that the target
length is sometimes inferred (tweet boundaries) rather than read, that one of the probe patterns is slightly
skewed, and that probe thresholds were chosen by hand. They frame the probe catalogue as a survey, not an
evaluation, and argue the bottom-up workflow they used would benefit from automation. The universality claim rests
on geometric similarity to one other model and one other task, with Llama as the only model actually
intervened on.

## What we take from it
- **Method:** "reverse-engineer on a synthetic task, then localise the same part in an unlabeled corpus" is a
  cheap, general recipe for turning a local circuit into a claim about generality; we can adopt it directly as
  the validation stage for any mechanism we find.
- **Measure:** normalised output-position axis, so curves from different sequence lengths superimpose — the way
  to show a head tracks *remaining distance* rather than absolute position.
- **Measure:** cross-condition cosine similarity checked for unimodality *and* linear length mapping (r²) is a
  strong, cheap test that two representations code the same variable in different units; better than a single
  probe transfer number.
- **Warning:** layer of last causal use ("last-used layer") differs from layer of peak probe accuracy. Patching
  every layer and reading where the effect *stops* is the correct way to choose where to intervene downstream.
- **Framing:** the read-write structure (key = target length manifold, query = position manifold, similarity =
  progress) is a concrete example of a predictive white-box model component: it predicts behaviour from two
  scalar-ish quantities and can be checked by intervention.
- **Dataset:** repeated fixed-width string prompts (base64, DNA, tables) are a trivially generated family of
  implicit-length tests we can reuse.

## Tags
unit: circuit | head
form: circuit | description
method: patching | probing | ablation | other
eval: patching | prediction/simulation | faithfulness | benchmark
goal: understanding | science
