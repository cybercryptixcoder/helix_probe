# What the interpretability field is building, and where a weights-read white box fits

Synthesis of the core survey: 193 entries in `core/`, built from the 34 reader notes in `core/notes/` and checked against the entries. Written 2026-11-12. Keys such as `arxiv-2301.05217` point to entries in `core/`. Numbers below come from the entries, which say how much of each paper was read; this file does not re-verify them against the papers.

The question this file answers: **when we say "a white-box reconstruction of a black box, a model that predicts and is not a correlation table", what does the field already mean by that, how does it test such a thing, and where is the unclaimed space?**

---

## 1. What the field is ultimately trying to build

Every group in the survey wants something that **stands in for the network and lets you predict it**. They differ only in how much they think is reachable.

| Ambition level | Form of explanation | Examples | Status |
|---|---|---|---|
| Full decompilation | An executable program equivalent to the network | modular addition read from Fourier weights (arxiv-2301.05217); attention-only path expansion (tcpub-2021-framework); MIPS code from RNN weights (arxiv-2402.05110); Transformer Programs (arxiv-2306.01128); Curve Circuits rewritten as program-generated weights (distill-2020-circuits-curve-circuits) | Achieved only for toy tasks or constrained networks |
| High-level causal model | An algorithm whose variables map onto parts of the network, tested by swapping them | causal abstraction / IIA (arxiv-2106.02997, arxiv-2301.04709, arxiv-2508.11214); DAS (arxiv-2303.02536); addition in an LLM (arxiv-2605.01148); mixtures of binding mechanisms (arxiv-2510.06182) | One behaviour at a time; the hypothesis comes from researchers |
| Replacement model | Learned sparse units that are spliced in for real layers, plus graphs over them | transcoders and CLTs, attribution graphs (tcpub-2025-attribution-graphs-methods); parameter decomposition, which sums exactly to the weights (APD, SPD, VPD) | Partial: error nodes, frozen attention, about half of next-token predictions survive full replacement |
| Per-unit description | Text label or rule saying when a unit fires and what it does | OpenAI neuron explainer, Transluce, Goodfire Neuron Scientist, SAE autointerp | Scalable but broad; descriptions fail substitution tests |
| Handles | One direction or subspace that monitors or steers a trait | refusal direction (arxiv-2406.11717), steering vectors, persona vectors (arxiv-2507.21509), RepE | Useful, but not explanations of computation |
| Question-answering readers | A model that answers questions about another model | Weight Oracles (arxiv-2610.07334), LoRAcles, Diff Interpretation Tuning (arxiv-2510.05092), activation verbalizers | Narrow, opaque themselves, and they describe more than they predict |

The definition the agenda papers converge on is **understanding = being able to predict behaviour, including on unusual inputs and under intervention** (arxiv-2501.16496, arxiv-2005.01831, arxiv-1702.08608, arxiv-2508.11214). GDM's pragmatic turn (lesswrong-2025-pragmatic-vision-for-interpretability) keeps the same test but accepts incomplete understanding when it supports a decision.

**So the user's "white box that predicts" is the field's own stated goal**, not a new framing. The novelty has to lie in how it is built (from weights) and how far it reaches (whole model, intervention outcomes, scale), not in the goal.

## 2. Motivations

- **Safety and auditing.** Find hidden objectives, backdoors and deceptive behaviours. Examples: AuditBench, the auditing game (arxiv-2503.10965), automated auditing agents.
- **Debugging and prediction of training effects.** Examples: predictive data debugging, model diffing (tcpub-2024-model-diffing, arxiv-2510.13900), task arithmetic.
- **Control.** Steering, erasure (LEACE) and editing (ROME, MEMIT) without retraining.
- **Science of learned algorithms.** What networks compute and why the same task yields different algorithms in different networks (arxiv-2306.17844).
- **Verification.** Proofs and bounds from mechanistic understanding (arxiv-2406.11779).

## 3. The hurdles the field names, ranked by how often they recur

1. **Superposition and the choice of unit.** Neurons and raw weight rows are not the variables (tcpub-2022-toy-model). Every alternative basis has its own problems:
   - SAE dictionaries depend on the seed: only 30–42% of latents are shared (arxiv-2501.16615).
   - They split and absorb features.
   - They can tile manifolds instead of finding variables (arxiv-2509.02565).

   Goodfire argues the reverse for modern models: native neurons are mostly clean (goodfire-research-already-clean, goodfire-research-neurons-as-an-interpretable-basis). The unit is openly contested.
2. **Decodable is not the same as used.** Probes succeed almost everywhere while interventions pick out few locations (arxiv-2106.02997). The best probe steers worst (arxiv-2310.01405). LR and mass-mean probes have similar accuracy but different causal effects (arxiv-2310.06824). This is the single most repeated warning.
3. **Matching outputs is not matching mechanism.** A replacement can match outputs through a different internal path:
   - tcpub-2025-faithfulness-toy-model;
   - e2e SAEs (arxiv-2405.12241);
   - a compressed Tracr model kept its accuracy while changing its encoding (arxiv-2301.05062);
   - weight-sparse circuits that are interpretable but unfaithful.
4. **Compensation and non-additivity.** Hydra and backup heads self-repair (arxiv-2307.15771). Neuron effects interact non-additively. Cancelling paths and interference weights mean raw weight magnitude does not equal importance (tcpub-2025-interference-weights).
5. **Evaluation is unstable.** Faithfulness numbers change with:
   - the ablation type (zero, mean or resample);
   - the metric (probability, logit difference or KL);
   - noising vs denoising;
   - how the patch is scoped.
   
   The "optimal circuit" is defined only relative to the ablation (arxiv-2407.08734, arxiv-2309.16042, arxiv-2404.15255).
6. **Attention and MLPs resist reading.** Attribution graphs freeze attention. QK is named the hardest part (tcpub-2025-attention-qk). MLP neuron-level computation stays unexplained in real LMs (greater-than, Fact Finding).
7. **Dark matter.** There is always unexplained residual: about 11–22% reconstruction error in CLTs. A whole layer of LLM-simulated latents does about as badly as deleting the layer (arxiv-2501.18838).
8. **White-box tools give little uplift over strong black-box baselines.**
   - AuditBench: black-box scaffolds are often the strongest.
   - CHIVE: no gain across three predictor families.
   - SAE probes almost never beat logistic regression (arxiv-2502.16681).
   - DiffMean and prompting beat SAEs at steering (AxBench, arxiv-2501.17148).
   - GDM deprioritised SAE research after negative downstream results.
9. **Scaling.** Exact methods stop at toy scale. Parameter decomposition has been shown only on small models.
10. **LLM judges and memorisation.** Judges are lenient and can be gamed. Famous circuits such as IOI are memorised by LLM agents (arxiv-2603.20101).

## 4. Methodologies and measures the field recognises

These are the measures our paper should report, so reviewers recognise them. They are grouped by what they test.

### 4a. Prediction under intervention (the headline family)

| Measure | What it is | Where |
|---|---|---|
| Interchange intervention accuracy (IIA) | Swap a variable's value from a source input into a base input; does the network's output match what the hypothesised model predicts? | arxiv-2106.02997, arxiv-2303.02536, MIB, RAVEL |
| Counterfactual simulatability | Predict behaviour on edited inputs; score with AUROC against a transcript-only baseline | arxiv-2005.01831, CHIVE (arxiv-2608.16747) |
| Intervention-outcome prediction | Predict in natural language what a patch or ablation will do; score with exact match and has-changed F1 | arxiv-2511.08579 |
| Distributional agreement under patching | Compare JS or KL against the model's output distribution, bracketed by uniform, naive and oracle baselines | arxiv-2510.06182 |
| Ablate/add acceptance | A direction counts if removing it removes a behaviour and adding it induces one, with side effects checked | arxiv-2406.11717 |
| Efficacy / generalisation / specificity | Editing triple (CounterFact, zsRE), plus ripple-effect consequence queries | ROME, MEMIT, arxiv-2307.12976 |
| Incremental R² over trivial covariates | How much your mechanistic variables add to predicting an intervention's outcome beyond layer index, etc. | arxiv-2301.04213 |

### 4b. Substitution and replacement (does the explanation run in place of the network?)

- **Loss recovered / spliced-in CE or KL**, normalised between zero-ablation and the original model. This is used throughout the SAE and transcoder papers and SAEBench.
- **Restricted vs excluded loss**: keep only the named parts, or remove only them (arxiv-2301.05217).
- **Fraction of ablation damage restored** by a substitute:
  - Curve Circuits' program-generated neurons;
  - the OpenAI ablation score, which can be low even when correlation is 0.9;
  - Goodfire's neuron simulator restoring 73%;
  - about 75% of logit difference restored when fitted helices are patched in (arxiv-2502.00873).
- **Faithfulness / completeness / minimality curves** against circuit size (arxiv-2211.00593, arxiv-2403.19647), summarised by MIB's CPR/CMD.
- **Replacement and completeness scores**, plus perturbation agreement layer by layer, which decays with depth (tcpub-2025-attribution-graphs-methods).

### 4c. Mechanism agreement (catching the "right output, wrong reason" failure)

- Jacobian agreement (tcpub-2025-faithfulness-toy-model; JSAE's 97.7% Jacobian-vs-shift check, arxiv-2502.18147).
- Per-layer internal-state similarity (Tracr).
- Downstream activation match (e2e+ds, arxiv-2405.12241).
- Cross-seed and OOD agreement (the weight-sparse unfaithfulness post).
- The adversarial-mask stress test (VPD).

### 4d. The verification ladder

From arxiv-2312.03656, arxiv-2112.00826 and arxiv-2406.11779, from weakest to strongest:

> in-distribution agreement < OOD agreement < agreement under intervention < worst-case certified bound

## 5. Baselines and controls a reviewer will expect

- **Behaviour-only surrogate** trained on input-output pairs: the "no explanation" baseline.
- **Strong black-box scaffolds**: prompting, sampling, prefill, query agents. They often win.
- **Weight statistics + regressor** (STATNN, s(W)). These are very strong for property prediction: R² about 0.98 for accuracy (arxiv-2002.11448), only marginally beaten by equivariant networks.
- **A reader that ignores the weights** (Weight Oracles' plateau equalled it). Plus the stratification battery: shuffled weights, untrained model, prompt-only, anonymised labels, layer subsets, default-answer rate (lesswrong-wnl4nwrs2owzzfwiz-wsp-stratification).
- **Cheap supervised directions**: DiffMean and linear probes (AxBench, arxiv-2502.16681).
- **AtP\*** for "predict every component's patching effect" (arxiv-2403.00745). Its failure points are softmax saturation and cancellation.
- **Simple controls**:
  - random directions with matched norm or rank;
  - random-init models;
  - random circuits;
  - multiple seeds;
  - PCA/ICA;
  - a clean-minus-corrupted difference (surprisingly strong, arxiv-2403.17806);
  - SVD plus unembedding projection as the weak weight-reading baseline (alignmentforum-svd-transformer-weight-matrices-highly-interpretable);
  - the weight-unigram baseline W_E·W_in.
- **Untrained and nearest-neighbour baselines** for learned predictors (arxiv-2511.08579).

## 6. Ground-truth testbeds and benchmarks

| Testbed | Ground truth | Use for us |
|---|---|---|
| Tracr / RASP compiled models (arxiv-2301.05062) | Exact program; can be compressed to induce superposition | Does a weight reader recover a known program? |
| InterpBench / SIIT (arxiv-2407.14494) | Planted circuits in trained (not compiled) weights | More realistic planted ground truth |
| Toy models of superposition, compressed computation | Planted features | APD/SPD recovery metrics (MMCS, ML2R) |
| Modular addition, group composition, greater-than, IOI | Published reverse-engineered mechanisms | Sanity targets. Beware LLM memorisation of IOI |
| Model zoos (arxiv-2209.14764) | Many networks with known training settings; split by model, never by checkpoint | Weight-space learning protocol, held out by model |
| AuditBench, model organisms with implanted behaviours, behaviour LoRAs | Known implanted behaviour | Predict an implanted behaviour from weights alone |
| MIB (arxiv-2504.13151) | Circuit and causal-variable localisation, multiple models | Field-standard benchmark format to imitate |
| RAVEL, SAEBench, CounterFact, Concept500 / AxBench | Attribute disentanglement, SAE quality, edits, steering | Reuse metrics where a component of ours is comparable |
| WSPBench, Sparks, Weight Oracles tasks | Handcrafted circuits; small transformers | The direct prior art for LLMs reading weights |

## 7. Frameworks that organise the field

- **Causal abstraction** (arxiv-2301.04709, arxiv-2508.11214) is the unifying theory. Patching, mediation, scrubbing, path patching, DAS, probes and SAEs are all special cases. Its open issue is triviality: with unrestricted maps, every network implements every algorithm. So the map class must be declared and restricted (e.g. linear).
- **Causal mediation** (arxiv-2004.12265, arxiv-2408.01416), with the evaluation triple of similarity function, intervention distribution and summary statistic. The survey's mediator taxonomy has **no weight-level mediator type**, a gap.
- **Ontology → algorithm → behaviour** (the Goodfire agenda): variables and their geometry first, then the algorithm over them.
- **Faithfulness vs plausibility** (arxiv-2004.03685, arxiv-1811.10154): report where a surrogate disagrees with the model, not just how often it agrees.
- **Description length at fixed fidelity** (arxiv-2410.11179) as the compactness criterion.

## 8. Shortcuts we can take

These are tools and results that already exist, so we don't build them.

1. **Data-free weight readings.** Use these as a first layer of description:
   - vocabulary projection of W_in, W_out, W_QK and W_VO (arxiv-2209.02535, arxiv-2012.14913);
   - E^T W_VO E for attribute extraction (arxiv-2304.14767);
   - VocabProj, which predicts a feature's output effect (arxiv-2501.08319);
   - the inverse unembedding covariance as an inner product (arxiv-2311.03658).

   All are weaker in early layers and MLPs. The tuned lens shows the basis drifts across layers.
2. **Weight edits that provably equal activation ablation.** Orthogonalising the residual-writing matrices against a direction reproduces activation ablation exactly (arxiv-2406.11717). An activation patch along a direction is near-equivalent to a rank-1 weight edit (arxiv-2311.17030). These link intervention evidence to weight structure, so we can phrase every intervention as a weight edit.
3. **Closed-form surrogates from weights**:
   - bilinear eigenvectors (arxiv-2410.08417);
   - least-squares polynomials (arxiv-2502.01032);
   - the JSAE closed-form Jacobian;
   - the ROME/MEMIT associative-memory model with key covariance, which predicts the effect of a linear-layer edit.
4. **Exactly-additive decompositions.** Parameter decomposition: APD → SPD → VPD. SPD's causal-importance function is literally a learned predictor of which weights matter on each input.
5. **Weight statistics that already predict roles or behaviour**:
   - neuron roles from vocabulary-projection skew/kurtosis, w_in/w_out cosine, bias and norm (arxiv-2401.12181);
   - adversarial vulnerability from interference in W (arxiv-2508.17456);
   - which features a width-N model keeps (arxiv-2605.29548).
6. **Reading native neurons.** The Goodfire neurons post reads much of a modern MoE model in its native basis from upstream writes and first-order downstream propagation. Its evaluation suite (detection, mode classification, input synthesis, simulation as damage restored, sparsification against random/bottom-K) is reusable.
7. **Symmetry handling** for any learned reader:
   - permutation-equivariant networks (DWSNets, NFNs, graph metanetworks; arxiv-2312.04501 covers attention, residuals and norms);
   - canonicalising LoRA's GL(r) symmetry was the largest single gain in W2T (arxiv-2603.15990);
   - invariance under random symmetry transforms is a cheap sanity test.
8. **The MIPS pipeline** as a template for program extraction: minimise, canonicalise, discretise, symbolically regress, demand exact agreement.

## 9. What has been done closest to our idea, and the exact gap

| Closest work | What it does | What it leaves open |
|---|---|---|
| Anthropic interference weights and virtual weights (tcpub-2025-interference-weights, tcpub-2026-interference-effectiveness-helpfulness) | Tries to read a 1-layer model's weights globally as a sparse program | Not sparse even at 1 layer: about 2.4% of 331M virtual weights are needed for 90% of helpfulness. The authors blame the basis. **Strongest warning for us.** |
| Parameter decomposition (APD/SPD/VPD) | Exact weight decomposition, input-dependent importance | Grouping pieces into mechanisms; adversarial faithfulness only partial; small scale |
| Weight Oracles (arxiv-2610.07334) | A trained reader simulates small transformers per projection; detects backdoors | Scaling; predicts outputs, not intervention effects; no inspectable model |
| WSP / Sparks / WSPBench | Frontier LLMs read and edit weights | Raw-weight reading worked only on networks of 17K–172K weights; LM-scale wins used code or execution; tiny N |
| CHIVE (arxiv-2608.16747), arxiv-2511.08579 | Predict behaviour under intervention, activation-based | **Explicitly leave weight- and circuit-level methods untested.** The model sharing the target's weights predicted it best |
| Weight-space learning (STATNN, DWSNets, hyper-representations, metanetworks) | Predict model-level properties from weights | **No per-input behaviour prediction**; small MLPs/CNNs |
| Causal abstraction / DAS | Score a hypothesised algorithm with IIA | **Hypotheses come from researchers, never derived from weights** |
| Goodfire Neuron Scientist | Native-neuron descriptions, scored by damage restored | Activation-based; per-neuron, not whole-model |

**The gap, stated in the field's own terms.** Nobody has derived an executable high-level model of a trained network from its weights and then scored it with the field's intervention tests: IIA, substitution / loss recovered, and intervention-outcome prediction. Nobody has done this against black-box and weight-statistic baselines either, beyond toy networks. Several reader notes found this independently (09a, 09c, 08a, 08c, 11c, 04a, 04b).

## 10. What this means for our definition of "white box"

A definition the field would recognise. Proposed, not final.

> A **white-box reconstruction** of network N is an executable model M, derived from N's weights, whose variables map onto parts of N under a declared, restricted map. M is judged by how well it predicts N's behaviour **under intervention**: interchange swaps, ablations and weight edits. It is compared against the network itself and against baselines that do not read the mechanism. M also reports what it does not explain.

What follows for the paper:

1. **Headline metrics** (one from each family): IIA or intervention-outcome F1; fraction of ablation damage restored when M substitutes for a component; and one mechanism-agreement check (Jacobian or internal-state similarity). Report each under a stated ablation protocol, with noising and denoising, in-distribution and OOD.
2. **Baselines**:
   - a behaviour-only surrogate;
   - a black-box scaffold;
   - weight statistics + regressor;
   - a weight-ignoring reader;
   - AtP\*;
   - random and untrained controls;
   - seeds.
3. **Ground truth first**: Tracr (including compressed) and InterpBench, then known mechanisms (modular addition, greater-than), then a real model. Use AuditBench-style implanted behaviours as a weights-only prediction task.
4. **Predict what naive stories miss**: compensation (backup heads), negative components, and where a mechanism fires wrongly. Several papers say this is where simple accounts fail.
5. **Unit**: test native neurons before committing to a learned dictionary. Canonicalise symmetries first. Allow manifold-valued variables, and keep interventions on the manifold.
6. **Honest residual**: report error terms and the unexplained fraction explicitly, and report description length at matched error.

### How this connects to our earlier plan (DIRECTIONS.md §2–2d)

The earlier lead was a measured ablation table with readers predicting held-out rows. That is a cut-down form of intervention-outcome prediction (4a), so the survey supports it as the evaluation core. The survey adds three things the plan lacked:

- the substitution test (4b);
- the mechanism-agreement test (4c);
- the full baseline set (§5), especially weight statistics, the weight-ignoring reader and AtP\*.

It also sharpens the risk. Anthropic's interference-weights result and the white-box-uplift failures (§3.8) mean the paper must show a concrete win that black-box and activation methods do not deliver. A null result needs to be informative, which the benchmark framing allows.

## 11. Open questions this survey did not settle

- Can native neurons in a mid-size open model serve as the variables of an executable reconstruction, or does interference force a learned basis? Goodfire and Anthropic point in opposite directions.
- Is any whole-model predictive account feasible past toy scale, or should the paper target one behaviour family at full depth? The causal-abstraction literature suggests the latter.
- The survey covered Aether's queue only partly (132 more Anthropic and Goodfire items). Anything there that changes §9 must be folded in.
