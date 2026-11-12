# Notes: 09_causal_methods_a (causal intervention methods, part a)

**What an explanation should be.** Across the batch an explanation is a claim about counterfactuals: what the
network would output if an internal quantity were set to the value it takes on another input. Vig et al.
(arxiv-2004.12265) localise effects to neurons/heads; Geiger et al. (arxiv-2106.02997) and Redwood
(lesswrong-causal-scrubbing-a-method-for-rigorously-testing) go further and require a whole high-level algorithm
mapped onto the network; arxiv-2301.04709 formalises this as causal abstraction and argues patching, mediation,
scrubbing, path patching, SAEs, probes and DAS are all special cases. The shared view is that an explanation is an
executable, simpler model, which is exactly a predictive white-box model.

**How success is measured.** Always by agreement under intervention, never by decodability: interchange
intervention accuracy (arxiv-2106.02997, arxiv-2301.04709), percentage of loss recovered under resampling ablation
(scrubbing), indirect/direct effect shares (arxiv-2004.12265), logit difference for patching
(neelnanda-mechanistic-interpretability-attribution-patching). arxiv-2301.04709 makes the choice explicit: a
similarity function, a distribution over interventions and a summary statistic. Probing is repeatedly shown to be
a weak control: probes succeed almost everywhere while interventions pick out few locations (arxiv-2106.02997).

**Recurring methods and controls.** Interchange/activation patching on clean-vs-counterfactual input pairs;
resampling ablation preferred over zero/mean ablation (scrubbing); random-weights model as control
(arxiv-2004.12265); restricting to "impactful" pairs where the intervention changes the label (arxiv-2106.02997);
gradient approximation for screening, real patching for confirmation (attribution patching).

**Open problems.** Abstractions hold only on subsets of inputs; search over alignments is combinatorial;
neuron effects interact non-additively (arxiv-2004.12265); scrubbing scores can be inflated by ignored inhibitory
paths and resampling variance; linear approximations fail at LayerNorm and saturating nonlinearities; theory is
deterministic and gives no guidance on choosing the intervention distribution.

**Bearing on a predictive white-box model from weights.** (1) Our evaluation should be IIA/KL under a declared
intervention distribution, which this field already accepts. (2) A weights-derived model predicts intervention
effects without running the network, so attribution patching is the closest existing analogue and its failure
modes (nonlinearity, interactions, large patches) are where we should expect our predictions to break and must test.
(3) None of these papers derive the high-level model from weights; hypotheses come from researchers and are only
verified on activations. Generating the abstraction from weights and then scoring it with these tests is a gap.
