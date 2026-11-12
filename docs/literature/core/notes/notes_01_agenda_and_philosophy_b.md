# Notes: 01_agenda_and_philosophy_b (cross-batch patterns)

**What an explanation should be.** Two traditions meet here. The mechanistic one (arxiv-2404.14082,
arxiv-2405.00208) aims for a causal, algorithm-level account (features and circuits, ideally pseudocode). The
evaluation tradition (arxiv-1702.08608, arxiv-2307.08678) judges an explanation by whether it lets someone predict
the model. In practice the field has settled on partial, local explanations. Attribution graphs are per-prompt
execution traces (neuronpedia-2025-circuits-research-landscape). GDM now accepts explicitly incomplete
understanding when it supports action (lesswrong-2025-pragmatic-vision-for-interpretability).

**How success is measured.** All six papers move away from intrinsic proxies and toward predictive or downstream
tests:
- Doshi-Velez & Kim name forward and counterfactual simulation, and require the type of evaluation to match the
  claim being made.
- Chen et al. turn that into two metrics, simulation precision and generality, scored against the model's own
  output.
- The GDM essay rejects reconstruction/sparsity frontiers as a measure of progress and wants falsifiable predictions
  of intervention outcomes.
- The circuits report gives the clearest evidence: KL fine-tuning lowered KL divergence but also lowered
  replacement score. Better reconstruction did not give a better replacement.

**Recurring methods, baselines and controls.** Activation and path patching (always name the ablation baseline;
resample is preferred), causal-abstraction-style interchange tests (scrubbing is the most permissive, full
abstraction the strictest), probes (they show presence, not use), steering vectors, and transcoders/CLTs.
Baselines the pragmatic camp says we must beat: prompting, probing, steering, reading CoT. Ground-truth testbeds:
Tracr-compiled models, toy superposition models, and model organisms with implanted goals or facts.

**Open problems that keep recurring.** Superposition, especially across layers. Approximation/error nodes that do
not go away. Self-repair, which muddies interventions. Per-prompt graphs that do not add up to a global algorithm.
Missing "why not" and suppressive explanations. Dictionaries that break geometric structure (helix turned into a
lookup table). Scaling and automation. Plausibility that is decoupled from faithfulness.

**What this means for a predictive white-box model built from weights.**
1. Score it the way Chen et al. score explanations: precision and generality over targeted counterfactual inputs,
   against the network's own outputs. Add intervention-outcome prediction, as the GDM essay asks.
2. A global, prompt-independent model read from weights fills the gap the circuits report names, and could keep
   geometry that transcoders destroy.
3. Validate by swapping in the reconstruction for the real component (arxiv-2404.14082), and include
   black-box predictors as baselines (lesswrong-2025-pragmatic-vision-for-interpretability).
4. Use known motifs (induction, IOI, greater-than; arxiv-2405.00208) and implanted ground truth as sanity targets.
