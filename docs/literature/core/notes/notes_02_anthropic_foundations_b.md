# Cross-batch notes: 02_anthropic_foundations_b

**What an explanation should be.** The batch moves from representations to computation. Early notes ask which units
are meaningful: coordinates only if the basis is privileged (tcpub-2023-privileged-basis), features as directions
that either compose or sit in superposition (tcpub-2023-superposition-composition). Later work wants the explanation
to be computation itself: gated low-rank transforms between layers (tcpub-2025-bulk-update-molt) or a sparse set of
"real" virtual weights read like a program (tcpub-2025-interference-weights,
tcpub-2026-interference-effectiveness-helpfulness).

**How success is measured.** Loss is the common currency: loss change under weight ablation as ground truth for
"real" weights, Fisher-approximated KL as "effectiveness", loss-versus-density pruning curves with raw magnitude as
baseline, and loss captured versus precision for cheap filters. Replacement models are judged by MSE-versus-L0
Pareto fronts and Jacobian faithfulness against parameter-matched transcoders. Seed-to-seed variation serves as a
noise floor in two papers. tcpub-2024-qualitative-essay warns that every such metric should be checked by qualitative
inspection before it is trusted.

**Recurring methods.** Controlled architectural interventions (fixed random rotations); toy models with known ground
truth used to validate heuristics before applying them to real models; expanding a network into virtual
feature-to-feature weights; transcoders as the default basis, with MOLTs as a challenger.

**Open problems.** (1) Interference weights: raw weights are not circuits, magnitude filters fail, and per-weight
scores are expensive and non-additive (cancelling paths, low-rank structures that only cancel interference). (2) Even
a 1-layer model is not sparse in a transcoder basis: keeping 90% of helpfulness needs about 2.4% of 331M virtual
weights. The authors blame the basis. (3) Transcoder faithfulness falls as scale grows.

**Bearing on a predictive white-box model from weights.** This batch is the closest prior work to our goal and also
the strongest warning about it. Anthropic's own attempt to read a tiny model's weights globally did not produce a
compact program. Any differentiation has to come from a better basis (transforms, compositional structure), from
handling joint and non-additive effects, or from cheap, validated interference filters. Reusable now: the
virtual-weight expansion, the effectiveness and helpfulness scores, pruning curves, Jacobian faithfulness, the toy
ground truths, and rotation and kurtosis checks before reading any coordinate as meaningful.
