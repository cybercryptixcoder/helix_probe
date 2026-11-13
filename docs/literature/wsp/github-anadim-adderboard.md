# AdderBoard: smallest transformer that adds two 10-digit numbers (trained and hand-coded leaderboards)

- **Key:** github-anadim-adderboard
- **Authors / organisation:** Dimitris Papailiopoulos (maintainer, GitHub anadim); community submitters
- **Date:** 2026 (citation year in the README; exact start date and last update not stated in what was read)
- **Link:** https://github.com/anadim/AdderBoard
- **Kind:** benchmark
- **Read from:** README (in full) and `verify.py` (in full). **Not read:** individual submissions, gists and repos,
  issue #75 on parameter counting, the originating blog post "Addition Under Pressure", and the two origin repos.
  The GitHub API was not available to this session, so the repository tree was not listed.
- **Relevance to us:** 1 (background)

## What they wanted, and why
The challenge asks for the smallest autoregressive transformer that adds two integers of up to ten digits with at
least 99% accuracy on a fixed held-out test. It grew out of giving Claude Code and Codex the same prompt to train
the smallest such model. Two tracks are kept: weights learned by a generic training algorithm, and weights set
analytically by hand, treated as constructive proofs that an architecture can represent addition. The underlying
question is the minimal transformer that can implement digit alignment, per-digit sums and carry propagation.

## What they studied
Tiny decoder-only transformers (mostly one layer, model width 2–7, one to five heads, tiny MLPs, various positional
schemes such as RoPE with period 19, ALiBi with slope log 10, sinusoidal or parametric embeddings), from 6 to 6,080
counted parameters. Unit: whole model; the hand-coded track reasons about individual weights.

## How they did it
Submitters provide a Python module with `build_model()` returning the model and metadata (including a self-declared
unique parameter count) and `add(model, a, b)`. `verify.py` runs 10 fixed edge cases plus 10,000 random pairs from
[0, 9,999,999,999] with seed 2025 and reports accuracy and time. Rules: at least one self-attention layer; genuine
next-token prediction with the generation loop outside the model; a standard tensor-in, logits-out forward with no
task-specific control flow; the decoding code must be generic enough to run any checkpoint. Parameters are counted
after tying; fixed sinusoidal encodings are not counted, learned ones are. Submissions arrive as issues or pull
requests and are verified by the maintainer. A "built with" column records AI assistance (Claude Code, Codex,
GPT-5.2 Pro, Gemini).

## What counts as an explanation here
For the hand-coded track, the explanation is the construction itself: a set of weights whose role is designed (for
example carry detection via hinge gates, digit routing via a chosen RoPE period, parabolic decoding heads). It is
complete for the task in that it computes addition, and checkable by running it.

## How they judged success
Accuracy on 10 edge cases plus 10,000 seeded random pairs, threshold 99%; unique parameter count; ranking by count.

## What they found
- Hand-coded leader: 6 counted parameters at 100% (the count is disputed: 10 unique values under strict counting,
  because some fixed values sit in the architecture); then 8, 10, 12, 20, 27 parameters, all 100%.
- Trained leader: 36 parameters at 100% (one-layer, width 3, circular arc embedding and heavy tying); the original
  Codex and Claude Code runs gave 1,644 (99.04%) and 6,080 (100%).
- Community observations listed in the README: a sharp accuracy transition near 800 parameters for trained models;
  one layer beats two at equal budget; width 3 now works for trained models with circular embeddings and tying;
  hand-coded models go much smaller since SGD need not find them.

## Limits and open problems they name
Parameter counting is contested at the extreme low end; one entry (197 parameters) passed only 8,192 random tests
and is not yet verified on the 10K suite. The README notes the field may be near the practical minimum for this
architecture family.

## What we take from it
- **Shortcut/dataset:** a library of hand-coded tiny transformers whose every weight has a designed role is a
  ready-made set of targets with known ground-truth mechanisms; we could use them as reading targets (does a reader
  recover "carry via hinge gate" from the weights?).
- **Framing:** hand-coding is the writing side of WSP done by humans with AI help; it shows that a fully specified
  algorithm can be placed in a handful of weights, which bounds what a reader must find.
- **Warning:** the "built with" column mixes human and AI authorship without separating their contributions; this
  is not evidence about LLM weight writing on its own.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** not applicable; no model reads weights. AI tools are recorded only as
  build assistants for some submissions.
- **Target networks:** tiny autoregressive transformers for 10-digit addition, 6 to 6,080 parameters; hand-coded or
  trained.
- **How the weights were presented:** not stated (submissions are code that builds the model).
- **Prompt:** not stated; the originating prompt to Claude Code and Codex is described only as asking to train the
  smallest transformer reaching at least 99% on 10-digit addition.
- **Access regime:** not applicable.
- **Controls:** fixed edge cases and a fixed-seed 10K random test; rules against task-specific code in the forward
  pass or decoding loop.
- **Failure modes observed:** disputes over what counts as a parameter; unverified submissions.
- **Prompt or format choices that helped or hurt:** for building, not reading: data format (reversed digits,
  delimiters), curriculum and grokking-style training help trained models; rank-3 factorisation and circular arc
  embeddings are named as key tricks. Nothing about reading.

## Tags
unit: weights | whole-model
form: program
method: training-interpretable | other
eval: benchmark
goal: science
