# Mechanistic Interpretability for AI Safety: A Review

- **Key:** arxiv-2404.14082
- **Authors / organisation:** Leonard Bereska, Efstratios Gavves; University of Amsterdam
- **Date:** 2024-04 (v3 2024-08-23 read)
- **Link:** https://arxiv.org/abs/2404.14082
- **Kind:** survey/agenda
- **Read from:** full text (sections 1–5 and 7–8 via HTML in two parts; section 6 only skimmed)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
A structured review of mechanistic interpretability, motivated by AI safety. They define the field as reverse
engineering the computations and representations a network has learned into human-understandable algorithms and
concepts, ideally a granular causal account that could be written down as pseudocode. They want to clarify the
field's core concepts and hypotheses, organise its methods, assess its relevance to safety (and its risks), and set
out what is needed to make it rigorous and scalable.

## What they studied
The literature, not models. Units of analysis surveyed: neurons, features, directions, circuits (subgraphs of
features joined by weights), motifs, and whole-model "world models".

## How they did it
They contrast four lenses on a model (behavioural, attributional, concept-based, mechanistic). They define core
concepts and state core hypotheses explicitly, numbered (superposition, linear representation, weak/strong
universality, simulation and prediction-orthogonality). They then build a method taxonomy scored along causal
nature (observational vs interventional), learning phase (intrinsic, developmental, post-hoc), locality and
comprehensiveness, and place each technique in it: exemplars and feature visualisation, probing and sparse probing,
structured probes such as contrast-consistent search, logit/tuned lens, SAEs and transcoders; activation and path
patching, causal abstraction and interchange interventions, distributed alignment search, causal scrubbing, locally
consistent abstractions; intrinsic designs (bilinear layers, modular training); developmental work (induction-head
phase transition, singular learning theory's local learning coefficient); automation (automated circuit discovery,
attribution patching, LLM-written neuron explanations, program synthesis into Python). Finally they list
challenges and future directions.

## What counts as an explanation here
A mechanistic, causal account: features as the basic units, circuits as the computations between them, ideally
complete enough to be an algorithm or pseudocode. They distinguish local vs global and partial vs comprehensive
explanations, and rank causal-abstraction-style validation from strictest (full causal abstraction) through
locally consistent abstractions to most permissive (causal scrubbing).

## How they judged success
As a review, they catalogue validation norms rather than measure anything: interventional tests (patching, with
resample ablation preferred to stay on-distribution; clean→corrupt patching finds sufficient components,
corrupt→clean finds necessary ones), causal scrubbing's performance-under-resampling test, faithfulness and
falsifiability, out-of-distribution checks, controlled edits (implanting/removing trojans, ROME-style edits,
replacing a component with a hand-built or reverse-engineered substitute, e.g. Tracr or hypothesised circuits), and
testbeds with ground truth (Tracr-compiled models, toy superposition models, weight datasets with known circuits).

## What they found
Evidence supports only weak universality (shared principles, varied implementations). The linear representation
hypothesis has counterexamples (circular day/month features). Probes can conflate probe capacity with model
structure; contrast-consistent search can latch onto distractor features. Comprehensive reverse engineering has been
achieved only in toy settings (e.g. modular addition). Manual analysis does not scale; automation is required.

## Limits and open problems they name
Cherry-picking and "streetlight" interpretability; scalability and over-reliance on human judgement; obstacles to
bottom-up analysis (superposition, translating weights into readable graphs); models embedded in environments;
adversarial pressure against interpretability; Goodhart risk on proxy metrics; visualisations without causal
validation ("interpretability illusions"); lack of standard metrics, benchmarks and testbeds. Dual-use risk of
capability gains from insight.

## What we take from it
- **Validation ladder:** use causal-abstraction-style tests (interchange interventions) for our reconstruction;
  causal scrubbing is the most permissive, full causal abstraction the strictest — state which we meet.
- **Strong test for a white-box model:** replace a component with our reconstructed substitute and measure behaviour
  (the "replace with reverse-engineered alternative" idea), on- and off-distribution.
- **Testbeds:** Tracr-compiled models and weight datasets with known circuits give ground truth for weight-reading.
- **Warning:** resample rather than zero ablation; specify sufficiency vs necessity direction of patching.

## Tags
unit: feature | circuit | neuron | whole-model
form: causal-abstraction | graph | program | dictionary
method: SAE | transcoder | patching | probing | ablation | weight-analysis | training-interpretable
eval: patching | faithfulness | benchmark | ablation
goal: safety/auditing | understanding | science
