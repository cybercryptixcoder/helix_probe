# Sparks of Weight-Space Programming: reading experiments (Exp 1-3) and their released logs

- **Key:** blog-rikiyat-github-io-weight-space-programming
- **Authors / organisation:** Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab; MIT CSAIL
- **Date:** 2026-11-02
- **Link:** https://rikiyat.github.io/blog/weight-space-programming/ ; logs: https://github.com/RikiyaT/lm_understand-logs
- **Kind:** blog/research post (with a full experiment-log release)
- **Read from:** full text of the post (via a fetch tool that returns a detailed account rather than raw HTML), plus
  from the log repository: top README, `harness/instructions.md`, the READMEs of exp1/exp2/exp3, all four Exp 1
  prompts and answers, Exp 1 `run.json` (Breakout), all three Exp 2 prompts and answers, Exp 3 `message.txt`, all six
  Exp 3 final answers, `eval/heads.json` and `eval/scores.json`, and the first code runs of two Exp 3 conversations.
  **Not read:** `events.jsonl` reasoning summaries, per-turn files in Exp 3, most of `tool_calls.jsonl`, the
  `networks/` and `eval/` files of Exp 1-2 beyond the READMEs, and Exp 4-8 logs (outside this entry's focus). The
  GitHub API was not available to this session, so the repository tree was not listed; files were fetched by the
  paths the READMEs name. A companion entry focused on the whole post exists at
  `core/rikiyat-github-io-blog-weight-space-programming.md`.
- **Relevance to us:** 3 (central)

## What they wanted, and why
The authors ask whether a general frontier LLM, with no special training, can treat neural-network weights as
something it reads and writes directly, the way it reads and writes code. The three reading experiments are the
"read" half: given a trained network's parameters, can the model say what the network was trained to do? They are
built as a ladder: Exp 1 and 2 are small MLPs whose input or output layer is laid out on a pixel grid, and Exp 3
removes the input and output layers of a small transformer so that the answer cannot be read off a layer that faces
the data. The larger goal is LLMs acting as model engineers who audit, repair and build networks in weight space.

## What they studied
- **Reader:** "GPT-6 Astra", which the log README identifies as OpenAI's `gpt-6-astra`, called through the Codex CLI.
- **Exp 1 targets:** four PPO policies (Breakout, Pong, Pac-Man, Freeway on the authors' 10x10 grid versions), each an
  MLP 500-32-32-5 with tanh, 17,253 weights, best of three seeds after 1 billion PPO steps.
- **Exp 2 targets:** three DDPM denoisers for 12x12 grayscale filled circles, squares or triangles, each an MLP
  160-64-64-144 with ReLU, 23,824 weights, Adam for 40,000 steps.
- **Exp 3 targets:** three character-level transformers (4 layers x 6 heads, width 384, ReLU MLP of width 1,536,
  context 128, 28-symbol vocabulary), 7.16 million weights in total, each trained from scratch on 1 billion characters
  of Python library code, Japanese literature in romaji (Aozora Bunko), or English Wikipedia.
- **Unit of analysis:** whole network (which task) and, in Exp 3, individual attention heads.

## How they did it
Every call is one `codex exec` turn with all built-in Codex tools switched off and a one-line neutral system
instruction (it only tells the model to answer the request). Each turn's event stream was audited and marked
tool-free; the release says all 1,125 turns qualify. In Exp 1 and 2 each network gets one fresh conversation and
one reply, reasoning effort `high`: the prompt is a task description with the game or shape withheld, the question,
an answer template, and all weights as plain text. Exp 2 additionally forbids any forward-pass calculation, in the
head or on paper. In Exp 3 (effort `xhigh`) the weights are not in the prompt; the model writes one Python block
per turn, the harness runs it in a sandbox with the four blocks preloaded as numpy arrays, and returns the printed
output as the next message, for up to 100 runs (the model used 6 to 11). Exp 3 forbids running the network or any
layer of it on any input and forbids search, but allows linear algebra on the matrices. Each Exp 3 network was asked
in two independent conversations. Scoring maps the free-text answer line to a class by keyword (Exp 1, 2) or parses
the corpus and head-label lines (Exp 3), against an answer key the model never sees. Exp 3 head ground truth comes
from running the full networks: an induction score on a random 40-character string repeated twice, previous-token
attention on held-out text, mean look-back distance, and attention share on newlines.

## What counts as an explanation here
A short verbal account that names the task (game, shape, corpus) and, in Exp 3, a per-head functional label from a
fixed menu, each backed by quoted weights or weight-derived statistics. It is partial and descriptive: it names a
class, it does not yield a model that predicts outputs. Exp 2 also asks for one example output drawn as ASCII,
which is the only place the reading is turned into a concrete prediction.

## How they judged success
Exact class match, open answer, out of 4 (games), 3 (shapes) and 3 x 2 (corpora); self-reported confidence; for
heads, set match between heads labelled `copy` and heads whose induction score exceeds 0.2. Exp 2 checks each
denoiser really makes its shape with a small shape classifier on 1,000 samples per model. There are no
shuffled-weight, untrained-network or prompt-only baselines; the controls are the access restrictions and the audit.

## What they found
- Exp 1: all four games named correctly with an open question (Freeway answered as Frogger, which the scorer maps to
  Freeway), confidences 99 / 96 / 96 / 97, about 73,700 input tokens and 833 to 1,034 reasoning tokens per run,
  71 to 107 seconds each.
- Exp 2: all three shapes named, confidences 84 / 77 / 88, about 99,800 input tokens per run, but every example
  drawing is a one-pixel outline although the models generate filled shapes.
- Exp 3: corpus correct in all six conversations but with low probabilities (0.48 to 0.62 on the true corpus), and
  "as is" versus "shuffled" answered with 0.96 to 0.99. The heads labelled `copy` exactly match the heads with
  induction score above 0.2 (Python 2.1, 3.1, 3.5; romaji 3.3; English 3.1) in both conversations per network, with
  no extra `copy` labels. The README notes that the scorer's own `true_copy_heads` field used a stricter 0.3 cutoff,
  under which only Python 3.5 and English 3.1 count; the post uses 0.2.

## Limits and open problems they name
Tiny N per task and one proprietary model; the post calls the results early sparks. Exp 1 and 2 can be solved from
the first or last layer alone, which is why Exp 3 was built. Corpus confidence in Exp 3 is modest. Trial runs of
earlier prompt versions are excluded from the release (a run path names a `which_open_v2` prompt), so the prompt
development history is not visible.

## What we take from it
- **A complete, reusable reading protocol** for our K1 work: description + withheld label + answer template + all
  weights as 3-decimal text; one fresh conversation per network; tool audit; keyword scorer with hidden key. We can
  replicate it exactly because prompts, weights (3-decimal text and full-precision `.npz`) and scorers are public.
- **Warning on what the prompt gives away.** The Exp 1 description names the semantics of each input channel
  (agent, moving objects, reward targets, obstacles, previous frame) and lays out the flattening formula, so a reader
  only has to find where each channel's first-layer weights are large. Our own look at the released Pong weights
  (not a claim of the authors) shows agent-channel row sums of first-layer magnitudes around 13 to 33 along column 1
  and about 1 to 2 everywhere else: inputs that are never active keep near-initialization weights, so the first layer
  is effectively a visitation map of the state distribution. This is a strong, cheap signal; a K1 control must ask
  whether a reader without channel names, or a trivial heatmap baseline, does as well.
- **Exp 3 is the meaningful test** for reading internals, and it is a Python-on-weights regime, not raw reading. The
  head-label menu in the prompt explicitly defines induction ("copy"), which primes the search.
- **Failure mode to design around:** right class, wrong detail (outlines for filled shapes), which suggests readers
  pattern-match templates in weights rather than predicting behaviour.

## K1 detail (reading setup)

- **Reader model(s):** `gpt-6-astra` via Codex CLI. Effort `high`, reasoning summaries `detailed` (Exp 1, 2);
  effort `xhigh` (Exp 3). Context window configured to 872,000 in the Exp 1 command line. Scores: Exp 1 4/4 open
  answer; Exp 2 3/3 shape (0/3 on filled vs outline); Exp 3 corpus 6/6, copy heads exact in 6/6 conversations.
  Our own tally from the released `eval/heads.json` and `head_labels` (not reported by the authors): the head
  labelled `previous` is the head with the highest previous-token score in every conversation; in the Python network
  a second strong previous-token head (L2H2, score 0.628) was labelled `unclear` in one conversation and `local` in
  the other. Most `local` labels fall on heads with short mean look-back (about 1.6 to 6), with exceptions (romaji
  L0H0 at 16.9, English L0H3 at 14.2); `broad` labels fall on heads with look-back near 32. The two conversations of
  the same network commit very differently (romaji: 21 `unclear` in one, 4 in the other).
- **Target networks:** Exp 1: MLP 500-32-32-5, tanh, 17,253 parameters, PPO policies for 10x10 grid Breakout, Pong,
  Pac-Man, Freeway (5 binary channels per cell; 5 actions). Exp 2: MLP 160-64-64-144, ReLU, 23,824 parameters, DDPM
  predicting the clean 12x12 image (144 noisy pixels + 16 sinusoidal step inputs). Exp 3: 4-layer, 6-head,
  width-384 character transformer, 7.16M parameters in total; the reader got the four blocks only (7,084,032 numbers).
- **How the weights were presented:** Exp 1 and 2: plain text inside the prompt, rounded to 3 decimals, one block
  per tensor (W1, b1, W2, b2, W3, b3) with a header giving shape and row meaning, one line per matrix row,
  space-separated, **rows not individually labelled** (the reader must count lines to find an input index). Input
  token counts: about 73,700 (Exp 1) and 99,800 (Exp 2). Exp 3: not as text; float32 tensors exactly as trained,
  preloaded in a Python dict `W`, matrices stored (out, in); no labels on the 384 residual dimensions; embeddings,
  final LayerNorm and unembedding withheld.
- **Prompt:** public at `exp1_which_game/runs/<game>/prompt.txt`, `exp2_diffusion/runs/<shape>/prompt.txt`,
  `exp3_language/runs/<run>/message.txt` in the log repository.
  Exp 1 structure: (1) observation: grid, wall border, inner 8x8 playable area, five named channels and the exact
  flattening formula; (2) actions: five named moves and softmax sampling; (3) network formula, row/column convention,
  parameter count, trained with PPO to maximise reward of a game on this grid; (4) question: which game, work from
  the weights, no tools, single response; (5) answer template: Observations (per channel, where weights are large;
  output layer; quote weights), Reasoning (which games fit / are ruled out), Game (name a well-known game if it
  resembles one), Description, Confidence; (6) the weights. No candidate list.
  Exp 2 structure: DDPM description with pixel indexing, noise schedule and sampling procedure; network formula and
  input layout; question (what images does it generate) with an explicit ban on forward-pass calculation or
  simulated sampling; template Observations / Reasoning / Images / Example (12x12 ASCII) / Confidence; the weights.
  No candidate list.
  Exp 3 structure: full numpy forward code including vocabulary order; training recipe and initialization scales;
  **three named candidate corpora with their sizes**, plus a second binary choice (as-is or line-shuffled);
  normalization rules; what weights are available and how heads map to rows/columns; what is allowed (any linear
  algebra) and banned (forward pass of any layer on any input; search); how to run code; question with template
  Observations / Heads (24 lines, each one of previous, local, broad, copy, unclear, with definitions) / Reasoning /
  corpus / order / probabilities, with equal probabilities forbidden.
- **Access regime:** Exp 1: no tools, one reply. Exp 2: no tools, one reply, no forward-pass calculation. Exp 3:
  Python sandbox (numpy, scipy, scikit-learn, PyTorch CPU, pandas, sympy, networkx), no network, 600 s per run,
  output cut at 20,000 characters, up to 100 runs (6 to 11 used), no forward pass of the network or any layer, no
  search; every run's code was read by the authors.
- **Controls:** No shuffled-weight, untrained-network, prompt-only or label-order controls reported. Controls are the
  tool-free audit, the forward-pass ban (Exp 2, 3), withholding embeddings/unembedding (Exp 3), open answers (Exp 1,
  2), two independent conversations per network (Exp 3), and checks that the targets really do their task (PPO
  returns vs a random policy; shape classifier on samples). One Exp 3 conversation contains its own
  coordinate-randomization comparison written by the reader.
- **Failure modes observed:** Exp 2 outlines for filled shapes (authors read this as evidence of reading weight
  geometry rather than simulating). Exp 3 low corpus confidence, inconsistent commitment across repeat
  conversations, a missed strong previous-token head. One Exp 3 first attempt returned an empty final message and was
  re-asked in a new conversation by the harness.
- **Prompt or format choices that helped or hurt:** No systematic comparison reported, and earlier prompt versions
  are not released. The authors state that removing input and output layers (Exp 3) was deliberate so that nothing
  identifies characters. Our observations: the named input channels in Exp 1 and the explicit definition of
  "copy" heads in Exp 3 are strong hints; unlabelled rows force line-counting in text mode, which Willison's
  local-model replication shows produces long index-arithmetic traces.

## Tags
unit: weights | head | whole-model
form: description
method: agent | weight-analysis
eval: benchmark | prediction/simulation
goal: understanding | evaluation-of-methods
