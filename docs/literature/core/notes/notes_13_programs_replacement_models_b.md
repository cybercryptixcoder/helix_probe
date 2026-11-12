# Notes: programs and replacement models (batch b)

**What an explanation should be.** All four treat an explanation as an object that can stand in for the network
and be checked against it: a formal proof over weights (arxiv-2406.11779), an executable RASP program decoded from
weights (arxiv-2410.00061), a simplified replacement component (arxiv-2312.03656), and a high-level causal model
aligned to neurons (arxiv-2112.00826). The common bar is behavioural or counterfactual equivalence, not plausibility.

**How success is measured.** Each paper scores an explanation by prediction against the real model, but on a
different axis: certified accuracy bound versus true accuracy, traded against proof cost in FLOPs (2406.11779);
functional equivalence of the decoded program on sampled inputs, with exact string match shown to be misleading
because many programs are equivalent (2410.00061); agreement (same prediction, attention JSD) split by
in-distribution versus systematic OOD shifts (2312.03656); interchange intervention accuracy under source/base swaps
(2112.00826). Together they give a ladder: in-distribution agreement < OOD agreement < agreement under intervention
< worst-case certified bound.

**Recurring methods and baselines.** Brute-force evaluation as the reference for any compressed account
(2406.11779); SVD/low-rank readings of QK/OV matrices appear in two papers, once as a proof tool and once as the thing
that fails OOD (2406.11779, 2312.03656). Ground-truth models with known algorithms (Tracr compilation, IIT-imposed
structure, toy Max-of-K) serve as test beds.

**Open problems.** Unstructured residual error compounds and makes worst-case guarantees vacuous (2406.11779). Data-
fitted simplifications inherit the training distribution's blind spots and can under- or overestimate
generalisation (2312.03656). Compiled weights are unlike trained ones and a learned decompiler is ~1000x larger
than its targets (2410.00061). Alignments in causal abstraction are not unique and IIA is rarely perfect
(2112.00826). All work is on small or toy models.

**Bearing on a predictive white-box model from weights.**
- Score our model on prediction against the network, reported per OOD split and under interventions (IIA), not only
  held-out agreement (2312.03656, 2112.00826).
- Account for the unexplained remainder explicitly (error terms or bounds) rather than discarding it; the compression-
  versus-tightness curve against brute force is a natural headline metric (2406.11779).
- Prefer weight-derived readings over data-fitted ones where possible, but test them OOD anyway (2312.03656).
- Use models with known algorithms (Tracr, IIT-trained) as ground truth, then require a trained-model test
  (2410.00061, 2112.00826). Use functional equivalence, never string match, to compare recovered programs.
