# Notes: agents for interpretability (batch a)

**What an explanation is.** Across the batch, explanations come in three forms: per-unit text labels
(arxiv-2404.14394), executable programs that reimplement a black-box function (arxiv-2309.03886), and feature-level
graphs or dictionaries from SAEs/transcoders (goodfire-research-replicating-circuit-tracing-for-a-simple-mechanism,
goodfire-research-predictive-data-debugging). The strongest papers judge an explanation by what it predicts, not by
how plausible it reads. FIND scores code by normalised MSE < 0.1 on held-out inputs. MAIA turns a label into
inputs it says should or should not activate the unit, then measures the real neuron. Predictive Data Debugging
reports R² = 0.9 for forecasting what DPO will teach. A program-form explanation scored on held-out prediction is the
closest existing template for our white-box model.

**Ground truth via planted or known mechanisms.** Every evaluation-minded paper here manufactures ground truth:
synthetic neurons (MAIA), procedurally generated functions (FIND), a previously reverse-engineered circuit
(greater-than in GPT-2 Small), poisoned data (goblin mode), and rediscovery of a published feature (Goodfire agents
blog). This is the field's standard way to validate a method, and we should adopt it: known mechanisms first, then
unknowns.

**Recurring baselines and measures.** MILAN-style non-interactive exemplar description is the default baseline for
agents (MAIA, FIND). Human expert labels and 2AFC judgments serve as reference points. LM judges are common, and both
FIND and the investigator-agents paper (arxiv-2502.01236) warn that they are lenient or can be reward-hacked.

**Open problems.**
- Behavioural search misses local or rare regimes. FIND agents missed corrupted subdomains, and seeding with exemplars
  helped, which points to search breadth as the bottleneck.
- Agents are optimistic: they shortcut, p-hack and accept bugs as breakthroughs, and they have no stopping criteria
  (Goodfire blog, MAIA's confirmation bias).
- Feature-level replacement models fragment known mechanisms into messier, extra features. Recovery was judged only
  by eye.
- FIND is black-box only. A ground-truth benchmark with white-box (weight) access is missing.

**Bearing on a predictive white-box model from weights.**
1. Express the model as code and score it FIND-style on held-out inputs and per context. Predictive Data Debugging
   found that aggregate evaluations hid context-specific changes.
2. Validate first on planted mechanisms and on greater-than.
3. Use investigator agents (arxiv-2502.01236) as an independent adversary to find inputs our model mispredicts.
4. Reading weights could cover the rare regimes that black-box agents miss. That is a defensible gap.
5. If agents run any part of the pipeline, add cross-family critics and treat near-perfect fits as suspected bugs.
