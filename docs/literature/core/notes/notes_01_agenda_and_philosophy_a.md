# Cross-batch notes: 01_agenda_and_philosophy_a

**What an explanation should be.** The batch converges on prediction as the test. The multi-lab agenda (arxiv-2501.16496) defines understanding as being able to predict behaviour even on arbitrary inputs. Hase and Bansal (arxiv-2005.01831) put this into practice as simulatability, forward and counterfactual. Lipton (arxiv-1606.03490) names simulatability and decomposability as kinds of transparency, separate from post-hoc artefacts. Olah (tcpub-2023-interpretability-dreams) adds that claims should be checkable against the parameters themselves, the "assembly code" level.

**Faithfulness over plausibility.** Jacovi and Goldberg (arxiv-2004.03685), Lipton and Rudin (arxiv-1811.10154) all warn that convincing explanations can be unfaithful. Hase and Bansal find empirically that subjective ratings do not predict simulation accuracy. Rudin's point is the sharpest for us: any surrogate that disagrees with the model is wrong about it, so the disagreement rate is the honest number to report. Jacovi and Goldberg ask for graded, local faithfulness.

**Recurring measures and controls.** These are fidelity (agreement of a surrogate with the model's decisions), erasure, comprehensiveness and sufficiency, forward and counterfactual simulation, and pre/post comparisons against a no-explanation baseline with leakage controls. Two more come from the mech-interp agenda: performance or loss recovered when a replacement is spliced in, and circuit faithfulness, completeness and minimality, with the caveat that results depend on the ablation used. The agenda also names ground-truth checks: toy models and programs compiled into weights.

**Open problems.** The agenda notes that SDL decomposes activations, not the weights that compute them. Other open problems: there is no agreed definition of a feature; circuits fit task averages but miss individual inputs; competitive evaluation against black-box baselines is rare; there are no agreed model organisms; and formal guarantees work only for tiny models. Olah's "dreams" remain speculative.

**Bearing on a predictive white-box model from weights.**
- Our goal matches the field's own definition of understanding (arxiv-2501.16496). Reading mechanisms from weights addresses a gap the field names itself.
- Score the reconstruction automatically as a simulator. Measure forward accuracy on held-out inputs and counterfactual accuracy under input and internal interventions. Compare it with a behaviour-only surrogate trained on input-output pairs, the no-explanation baseline in arxiv-2005.01831.
- Report where the reconstruction fails, not just how often it agrees (arxiv-1811.10154, arxiv-2004.03685).
- Apply the model assumption: behaviourally equivalent networks (different seeds or reparameterisations) should give equivalent reconstructions (arxiv-2004.03685).
- Validate on networks with known ground truth (compiled or handcrafted weights) before moving to real ones (arxiv-2501.16496).
