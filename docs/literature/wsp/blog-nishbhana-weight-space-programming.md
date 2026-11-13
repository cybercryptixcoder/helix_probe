# Weight-Space Programming: Can an LLM Read and Write Another Network's Weights?

- **Key:** blog-nishbhana-weight-space-programming
- **Authors / organisation:** Nish Bhana; personal blog (Nish Blog)
- **Date:** 2026-11-10
- **Link:** https://nishbhana.com/Weight-Space-Programming/
- **Kind:** blog/research post (synthesis of the original claim, critiques and follow-ups)
- **Read from:** full text (via WebFetch paraphrase). Not read: the post's SVG figures as images, and none of the linked sources were opened from here.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
An explainer and evidence audit of the MIT CSAIL "Sparks of Weight-Space Programming" claim (2 Nov 2026) that a
general LLM can read a network's raw weights, infer its function, and edit or write weights without gradient
descent. The author sorts which results have been reproduced, which rest on one group, and which are disputed,
because the popular summary blurred very different experimental setups. He stresses that nothing is peer-reviewed
and labels his own arithmetic as his own.

## What they studied
No new experiments. Sources covered: the original eight experiments (game-naming PPO policies of 17,253 weights;
shape diffusion models of 23,824 weights; 7.16M-weight character LMs; Gemma 3 270M sycophancy pairs; a 171,664-weight
Kinetix car policy; zero-start MinAtar players; a 1,480,274-weight Go network; Qwen3.5-0.8B maths repair and a
Gemma control); critiques by Honnibal and Goedecke; follow-ups by Ahmed (arXiv 2611.08070), Hu et al. / WSP-Scope
(arXiv 2611.09382), Singh (csinva.io hand-written transformers) and a Khaliq rebuild on Hugging Face.

## How they did it
Reads each source and restates setup, access level and result. Groups all experiments into three access bands: no
tools with weights as text (experiments 1, 2, 4, 5; all targets 17k-172k weights); Python over the weights without
running them (experiment 3 success, 7a failure); Python plus a forward-pass budget (6, 7b, 8 successes; Gemma
control failure). Then grades claims by evidence strength: reproduced by two groups with public logs, single group,
negative, unknown.

## What counts as an explanation here
Not the post's topic directly. Implicitly, a reading counts when the editor names the network's function from
weights, ideally with a mechanism (e.g. large first-layer weights at certain inputs, induction heads, a direction
written by MLP blocks).

## How they judged success
By reproduction status and by whether held-out results, controls (Gemma loop control, 9B scaling, label
permutation, dev-vs-test comparison) and access regime support each claim.

## What they found
Best-supported: an LLM with Python and a small forward-pass budget can find and remove one dominant fault (looping)
in a small model by changing a tiny fraction of weights, with held-out gains. Single-group only: tool-free naming of
small networks, written game players and Go, hand-written transformers. Negative: no ability was added (Gemma, 9B),
and weights-only reading of a released LM failed (7a). Unknown: reliability, scale, cost. The Ahmed audit
characterises tool-free reading of ~125k-weight classifiers as "local arithmetic plus dataset priors".

## Limits and open problems they name
Large run-to-run variance; largest target 9B with small gains; no source reports time or cost; Singh's language
tasks leaked the test set; original authors call their work early.

## What we take from it
A ready map of the WSP literature as of 10 Nov 2026 and a three-band access taxonomy that matches our own need to
separate weights-only reading from tool- and execution-assisted results. The Ahmed audit (label permutation; a
CIFAR-shape prior control) is the most directly reusable control design for K1 and should be read as a primary.

## K1 detail (reading setup)
- **Reader model(s):** GPT-6 Astra (original, WSP-Scope); Claude Opus 5.5 (Ahmed audit); "Claude" as a coding agent
  (Singh). Scores per source: original reads 4/4 games, 3/3 shapes, 3/3 languages (stated confidence 0.48-0.62),
  Gemma sycophancy 0/4 weights-only vs 3/3 with attention patterns; Ahmed reported qualitatively (correct on local
  arithmetic, wrong on dataset names). No single score per reader beyond these.
- **Target networks:** as listed above; for reading: PPO MLP policies (17,253 weights, four Atari-style games),
  diffusion MLPs (23,824 weights, circle/square/triangle), character transformers (7.16M, Python/romanised
  Japanese/English, only four middle blocks shown), Gemma 3 270M fine-tunes (honest vs agreeable), Ahmed's image
  classifiers (~125,000 weights; datasets included fast food, Japanese characters, satellite images).
- **How the weights were presented:** as text in the prompt for no-tool experiments; Python sandbox for larger
  targets. Number format, precision, layout and token counts: not stated in this post (author says detail is
  thin; Ahmed's format given only as "as text").
- **Prompt:** game-naming prompt described the inputs but not the game names; shape prompt forbade a forward pass;
  language prompt did not mention the transformer-circuits framework; Ahmed named inputs only as red/green/blue and
  did not name classes. Prompt files: not given here (logs at github.com/RikiyaT/lm_understand-logs).
- **Access regime:** three bands as above; budgets: up to 16 texts with attention patterns only (7b); 0-50 forward
  passes (Go); 10/25/50 passes of up to 512 problems (Qwen).
- **Controls:** label permutation and input/output-shape prior (Ahmed); Gemma loop control; 9B scaling; dev vs
  held-out test (WSP-Scope).
- **Failure modes:** dataset priors override weight evidence (fast-food classifier called CIFAR-10, Japanese
  characters called MNIST, satellite classifier called CIFAR animals, a "frog" unit that fires on trees); after
  label permutation, groupings survived but names were wrong; drew outlines where the model made filled shapes;
  weights-only Gemma reading failed.
- **What helped or hurt:** generic input naming exposed reliance on priors (Ahmed); attention-pattern access turned
  Gemma reading from failure to success; Goedecke notes labelled input channels make game-naming solvable by a
  trivial heatmap, i.e. input labels may do much of the work.

## Tags
unit: weights | whole-model
form: other
method: agent | weight-analysis
eval: benchmark | downstream-task
goal: evaluation-of-methods
