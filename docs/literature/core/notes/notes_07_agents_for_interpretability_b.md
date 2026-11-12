# Cross-batch notes: 07_agents_for_interpretability_b

**What an explanation should be.** Every paper here treats an explanation as a claim that must make testable
predictions. arxiv-2309.10312 recasts a neuron label as two claims (the activation set; causal mediation) and finds
prose labels fail both. arxiv-2501.08319 says a feature description must predict both what activates the feature
and what steering it does. arxiv-2603.20101 makes "these components share a function" testable as "swapping their
weights preserves outputs." arxiv-2506.12152 is the outlier (understanding in a human's head built by dialogue), but
it still uses simulatability as its success test. Several push away from vague prose toward executable forms
(2309.10312 explicitly favours programs).

**How success is measured.** Recurring pattern: an observational/input test plus a causal/output test, each against
random and simple baselines. Concrete measures: precision/recall/F1 over a denoted set and interchange intervention
accuracy (2309.10312); input- and output-based scoring with random control features and KL-matched steering
(2501.08319); silhouette under swap-based Jensen-Shannon distance, with random and expert references
(2603.20101); behaviour rates under standard vs amplified sampling (goodfire-research-model-diff-amplification).
Strong simple baselines often win: correlation-ranked neurons beat GPT-4 explanations; a one-shot LLM matches an
agent.

**Recurring warnings.**
- Few-sample simulation scores overrate explanations because they miss rare false positives (2309.10312). Model
  diff amplification makes the same point from the behaviour side: rare behaviours need targeted elicitation.
- Human labels and published circuits are not ground truth, and famous benchmarks (IOI) are memorized by LLM
  agents (2603.20101).
- LLM judges are common but need validating against humans (2501.08319, 2603.20101).
- Self-explanation needs a cooperative model with self-knowledge, so it is not trustworthy evidence on its own
  (2506.12152).

**Bearing on a predictive white-box model from weights.**
- Weight-only readouts work in places. VocabProj (decoder times unembedding) predicts a feature's output effect
  cheaply but is weak in early layers and MLPs (2501.08319). Swapping QK/OV weights gives a behaviour-grounded
  equivalence test (2603.20101). Checkpoint logit differences are a behaviour target we can predict from weight
  deltas (model-diff-amplification).
- Evaluate our model with both an observational and an interventional prediction test, use correlation and random
  baselines, include rare-case and tail checks, and avoid circuits an LLM may have memorized.
- Open problems: no evaluation is robust to memorization, single neurons rarely carry causal effect, and no method
  here goes beyond per-component descriptions to a whole-model predictive account.
