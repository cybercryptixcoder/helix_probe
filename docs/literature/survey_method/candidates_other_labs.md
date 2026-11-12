# Candidate reading list: interpretability work from groups other than Anthropic and Goodfire

Format: `- [tier] Title | YYYY-MM | URL | what it is and why it matters for our purpose`
Tiers: A = essential (sets a framework, method, measure or field goal; widely built on), B = useful, C = minor.
Triage only; papers were not read in depth. Tiers are a first-pass judgement aimed at our weights-to-predictive-model project.

## Google DeepMind (Neel Nanda's mech-interp team and wider Google)
- [A] Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2 | 2024-08 | https://arxiv.org/abs/2408.05147 | Open SAEs on every layer of Gemma 2; the standard public testbed, and its setup shows how SAE quality is measured (L0, fidelity, interpretability)
- [B] Gemma Scope 2 | 2025-12 | https://deepmind.google/blog/gemma-scope-2-helping-the-ai-safety-community-deepen-understanding-of-complex-language-model-behavior/ | Follow-up suite for Gemma 3 with SAEs plus transcoders/crosscoders for circuit work; current open infrastructure
- [A] Negative Results for SAEs on Downstream Tasks and Deprioritising SAE Research | 2025-03 | https://www.alignmentforum.org/posts/4uXCAJNuPKtKBsi28 | GDM finds SAEs lose to linear probes on downstream tasks and drops them as a main focus; key evidence on what dictionary learning has not solved
- [A] A Pragmatic Vision for Interpretability | 2025-12 | https://www.lesswrong.com/posts/Tm2vqRZ6YMpiftCs4 | Nanda's case for moving from "full reverse-engineering" to goal-driven, empirically checked interp; directly about what the field should aim for
- [A] Are Sparse Autoencoders Useful? A Case Study in Sparse Probing | 2025-02 | https://arxiv.org/abs/2502.16681 | Careful baselines show SAE probes rarely beat plain probes; a model for how to judge interp methods against baselines
- [B] Building Production-Ready Probes for Gemini | 2026-01 | https://arxiv.org/abs/2601.11516 | Activation probes deployed for misuse detection in Gemini; the "pragmatic" agenda in practice, with real-world evaluation
- [B] Interpretability Will Not Reliably Find Deceptive AI | 2025-05 | https://www.alignmentforum.org/posts/PwnadG4BFjaER3MGf | Nanda on the limits of interp as a safety guarantee; sets expectations on what "solved" can mean
- [B] An Extremely Opinionated Annotated List of My Favourite Mechanistic Interpretability Papers v2 | 2024-07 | https://www.alignmentforum.org/posts/NfFST5Mio7BCAQHPA | Curated, annotated reading list by Nanda; a cross-check for gaps in this list
- [A] Attribution Patching: Activation Patching At Industrial Scale | 2023-02 | https://www.neelnanda.io/mechanistic-interpretability/attribution-patching | Gradient-based linear approximation to activation patching; the basis of most scalable attribution and circuit-finding methods
- [A] AtP*: An efficient and scalable method for localizing LLM behaviour to components | 2024-03 | https://arxiv.org/abs/2403.00745 | Fixes failure modes of attribution patching and benchmarks it against true patching; key for how localisation is measured
- [A] How to use and interpret activation patching | 2024-04 | https://arxiv.org/abs/2404.15255 | Practical guide to the field's main causal experiment, metrics and pitfalls
- [B] Towards Best Practices of Activation Patching in Language Models: Metrics and Methods | 2023-09 | https://arxiv.org/abs/2309.16042 | Shows patching results depend on corruption method and metric; important for experiment design
- [B] An Interpretability Illusion for Subspace Activation Patching | 2023-11 | https://arxiv.org/abs/2311.17030 | Shows patched subspaces can look causal while using dormant pathways; a warning about validating explanations
- [A] Tracr: Compiled Transformers as a Laboratory for Interpretability | 2023-01 | https://arxiv.org/abs/2301.05062 | Compiles RASP programs into transformer weights, giving models with known ground-truth mechanisms; directly relevant to weights-to-program reading and to evaluating interp methods
- [B] Does Circuit Analysis Interpretability Scale? Evidence from Multiple Choice Capabilities in Chinchilla | 2023-07 | https://arxiv.org/abs/2307.09458 | Circuit analysis on a 70B model; shows what scales and what only partly generalises
- [B] The Hydra Effect: Emergent Self-repair in Language Model Computations | 2023-07 | https://arxiv.org/abs/2307.15771 | Ablated components get compensated by others, which complicates ablation-based explanations
- [C] Explorations of Self-Repair in Language Models | 2024-02 | https://arxiv.org/abs/2402.15390 | Follow-up quantifying self-repair across models and mechanisms
- [B] Fact Finding: Attempting to Reverse-Engineer Factual Recall on the Neuron Level | 2023-12 | https://www.alignmentforum.org/posts/iGuwZTHWb6DFY3sKB | An honest failed attempt to fully reverse-engineer factual-recall MLPs; useful on where neuron-level, weight-level understanding stops working
- [B] Gated Sparse Autoencoders / Improving Dictionary Learning with Gated SAEs | 2024-04 | https://arxiv.org/abs/2404.16014 | SAE architecture that fixes shrinkage; part of the SAE evaluation lineage
- [B] Jumping Ahead: Improving Reconstruction Fidelity with JumpReLU SAEs | 2024-07 | https://arxiv.org/abs/2407.14435 | The SAE variant used in Gemma Scope; state of the art on the sparsity-fidelity frontier
- [B] Interpreting Attention Layer Outputs with Sparse Autoencoders | 2024-06 | https://arxiv.org/abs/2406.17759 | Extends SAEs to attention outputs, covering the attention side of a complete decomposition
- [B] Learning Multi-Level Features with Matryoshka Sparse Autoencoders | 2025-03 | https://arxiv.org/abs/2503.17547 | Nested SAEs that reduce feature absorption and splitting; addresses a known SAE pathology
- [C] BatchTopK Sparse Autoencoders | 2024-12 | https://arxiv.org/abs/2412.06410 | Small SAE training improvement
- [A] Patchscopes: A Unifying Framework for Inspecting Hidden Representations of Language Models | 2024-01 | https://arxiv.org/abs/2401.06102 | Uses the model itself to decode its hidden states into language; unifies logit lens, probing and similar tools
- [B] Because we have LLMs, we Can and Should Pursue Agentic Interpretability | 2025-06 | https://arxiv.org/abs/2506.12152 | Been Kim et al. argue for interactive, model-assisted explanation; an alternative view of what an explanation is
- [B] When Chain of Thought is Necessary, Language Models Struggle to Evade Monitors | 2025-07 | https://arxiv.org/abs/2507.05246 | GDM work on CoT monitoring as a practical interp signal
- [A] Towards A Rigorous Science of Interpretable Machine Learning | 2017-02 | https://arxiv.org/abs/1702.08608 | Doshi-Velez and Kim's foundational taxonomy of how to evaluate interpretability (application-, human-, functionally-grounded)
- [B] Interpretability Beyond Feature Attribution: TCAV | 2017-11 | https://arxiv.org/abs/1711.11279 | Concept activation vectors; the origin of concept-direction probing
- [B] Sanity Checks for Saliency Maps | 2018-10 | https://arxiv.org/abs/1810.03292 | Shows popular attribution maps ignore the weights; a classic test of whether an explanation depends on the model at all
- [B] Acquisition of Chess Knowledge in AlphaZero | 2021-11 | https://arxiv.org/abs/2111.09259 | Probes for human concepts across training in a superhuman system
- [C] Bridging the Human-AI Knowledge Gap: Concept Discovery and Transfer in AlphaZero | 2023-10 | https://arxiv.org/abs/2310.16410 | Finds new concepts in AlphaZero and teaches them to grandmasters; explanation judged by human learning

## Distill / Olah-era Circuits work (OpenAI Clarity team, 2017-2021)
- [A] Zoom In: An Introduction to Circuits | 2020-03 | https://distill.pub/2020/circuits/zoom-in/ | States the circuits program's claims (features, circuits, universality); the founding statement of mechanistic interpretability
- [A] Thread: Circuits (index) | 2020-03 | https://distill.pub/2020/circuits/ | Index of the whole InceptionV1 circuits thread
- [A] Feature Visualization | 2017-11 | https://distill.pub/2017/feature-visualization/ | Optimisation-based visualisation of what units respond to; the main early way to "label" features
- [B] The Building Blocks of Interpretability | 2018-03 | https://distill.pub/2018/building-blocks/ | Combines feature visualisation, attribution and grouping into interfaces
- [B] Activation Atlas | 2019-03 | https://distill.pub/2019/activation-atlas/ | Global map of a network's activation space
- [B] An Overview of Early Vision in InceptionV1 | 2020-04 | https://distill.pub/2020/circuits/early-vision/ | Full catalogue of early-layer features; an attempt at completeness for part of a network
- [A] Curve Detectors | 2020-06 | https://distill.pub/2020/circuits/curve-detectors/ | Uses many converging lines of evidence to establish one feature family; a template for what counts as proof that a feature is real
- [A] Curve Circuits | 2021-01 | https://distill.pub/2020/circuits/curve-circuits/ | Reads curve detectors' construction from the weights and hand-rewrites them; the closest Distill comes to weights-to-understanding
- [A] Visualizing Weights | 2021-02 | https://distill.pub/2020/circuits/visualizing-weights/ | Methods for reading weights directly (including expanded weights across layers); core to our weight-reading goal
- [B] Naturally Occurring Equivariance in Neural Networks | 2020-12 | https://distill.pub/2020/circuits/equivariance/ | Weight-level symmetry across features; a way to compress a description of a network
- [B] High-Low Frequency Detectors | 2021-01 | https://distill.pub/2020/circuits/frequency-edges/ | Another case study of a feature family and its circuit
- [B] Weight Banding | 2021-04 | https://distill.pub/2020/circuits/weight-banding/ | Structural pattern found directly in weights
- [C] Branch Specialization | 2021-04 | https://distill.pub/2020/circuits/branch-specialization/ | Features cluster by architectural branch; structure visible from architecture plus weights
- [A] Multimodal Neurons in Artificial Neural Networks | 2021-03 | https://distill.pub/2021/multimodal-neurons/ | CLIP neurons for abstract concepts; key to how high-level features are described and tested

## OpenAI
- [A] Language Models Can Explain Neurons in Language Models | 2023-05 | https://openaipublic.blob.core.windows.net/neuron-explainer/paper/index.html | Explain-then-simulate scoring of neuron explanations by GPT-4; the founding automated interpretability method and its predictive-simulation metric
- [A] Scaling and Evaluating Sparse Autoencoders | 2024-06 | https://arxiv.org/abs/2406.04093 | TopK SAEs at GPT-4 scale with scaling laws and new quality metrics (downstream loss, probe loss, explainability, ablation sparsity)
- [A] Weight-sparse transformers have interpretable circuits | 2025-11 | https://arxiv.org/abs/2511.13653 | Trains models with most weights zero so circuits can be read straight from the weights; the closest major-lab work to our weights-first aim
- [A] Monitoring Reasoning Models for Misbehavior and the Risks of Promoting Obfuscation | 2025-03 | https://arxiv.org/abs/2503.11926 | CoT monitoring catches reward hacking, but optimising against it causes hidden misbehaviour; frames CoT as an interp channel
- [A] Chain of Thought Monitorability: A New and Fragile Opportunity for AI Safety | 2025-07 | https://arxiv.org/abs/2507.11473 | Multi-lab position paper on CoT as readable reasoning and what could destroy it
- [B] Monitoring Monitorability | 2025-12 | https://arxiv.org/abs/2512.18311 | OpenAI's evaluation suite and metrics for CoT monitorability
- [B] Persona Features Control Emergent Misalignment | 2025-06 | https://arxiv.org/abs/2506.19823 | Uses SAE model diffing to find a "misaligned persona" feature behind emergent misalignment; an applied case of SAEs giving a causal story
- [C] OpenAI Microscope | 2020-04 | https://openai.com/index/microscope/ | Feature-visualisation atlas of vision models; infrastructure from the Clarity era

## EleutherAI
- [A] Eliciting Latent Predictions from Transformers with the Tuned Lens | 2023-03 | https://arxiv.org/abs/2303.08112 | Learned per-layer decoders that read the model's running prediction; a standard way to read intermediate states
- [A] Automatically Interpreting Millions of Features in Large Language Models | 2024-10 | https://arxiv.org/abs/2410.13928 | Open auto-interp pipeline with cheaper scoring methods (detection, fuzzing, intervention); how explanation quality is measured at scale
- [B] Transcoders Beat Sparse Autoencoders for Interpretability | 2025-01 | https://arxiv.org/abs/2501.18823 | Transcoders (input-to-output maps) give more interpretable features than SAEs; relevant to describing computation, not just representations
- [B] Sparse Autoencoders Trained on the Same Data Learn Different Features | 2025-01 | https://arxiv.org/abs/2501.16615 | Seed dependence of SAE features; questions whether SAE features are a canonical description
- [A] Converting MLPs into Polynomials in Closed Form | 2025-02 | https://arxiv.org/abs/2502.01032 | Turns MLP weights into analysable low-order polynomial approximations; directly a weights-to-interpretable-model method
- [A] Can We Partially Rewrite Transformers in Natural Language? | 2025-01 | https://www.eleuther.ai/papers-blog/can-we-partially-rewrite-transformers-in-natural-language | Replaces an MLP with LLM-simulated natural-language explanations and finds it does about as badly as deleting the layer; a sobering test of explanations as predictive models
- [B] LEACE: Perfect Linear Concept Erasure in Closed Form | 2023-06 | https://arxiv.org/abs/2306.03819 | Provably optimal linear erasure; a tool for causal tests of concept use
- [B] Sparsify (library) | 2024-06 | https://github.com/EleutherAI/sparsify | EleutherAI's SAE/transcoder training library
- [B] attribute (circuit-tracing / attribution graph library) | 2025-06 | https://github.com/EleutherAI/attribute | Open replication of transcoder-based attribution graphs
- [B] Eliciting Latent Knowledge from Quirky Language Models | 2023-12 | https://arxiv.org/abs/2312.01037 | Benchmark for probes that recover truth when output is unreliable; tests whether internal reading beats behaviour
- [B] Pythia: A Suite for Analyzing Large Language Models Across Training and Scaling | 2023-04 | https://arxiv.org/abs/2304.01373 | Open checkpoints across training; the default substrate for training-dynamics and weight-evolution interp
- [C] Neural Networks Learn Statistics of Increasing Complexity | 2024-02 | https://arxiv.org/abs/2402.04362 | Shows networks learn low-order statistics first; a simple predictive account of learned function

## Transluce
- [A] Scaling Automatic Neuron Description | 2024-10 | https://transluce.org/neuron-descriptions | Fine-tuned cheap explainer that beats GPT-4-style descriptions on simulation score for every Llama-3.1-8B neuron; current best practice for neuron labelling
- [B] Monitor: An AI-Driven Observability Interface | 2024-10 | https://transluce.org/observability-interface | Interface pairing neuron descriptions with steering and search; an example of interp UI built for users
- [A] Eliciting Language Model Behaviors with Investigator Agents | 2025-02 | https://arxiv.org/abs/2502.01236 | Trains agents to find inputs that trigger target behaviours; scalable behavioural testing that complements weight reading
- [A] Predictive Concept Decoders: Training Scalable End-to-End Interpretability Assistants | 2025-12 | https://arxiv.org/abs/2512.15712 | Trains a decoder from activations through a concept bottleneck to predict model behaviour; directly a "predictive interpretable model of a network", close to our aim
- [A] Training Language Models to Explain Their Own Computations | 2025-11 | https://arxiv.org/abs/2511.08579 | Fine-tunes models to report their own features and causal structure, scored against interp ground truth; explanation as a trained, checkable output
- [B] Investigating Truthfulness in a Pre-Release o3 Model | 2025-04 | https://transluce.org/investigating-o3-truthfulness | Agent-driven investigation of fabricated tool use; interp-style auditing of a frontier model
- [B] Introducing Docent | 2025-03 | https://transluce.org/introducing-docent | Tool for analysing agent transcripts at scale; behavioural observability infrastructure
- [C] Introducing Transluce: A Letter from the Founders | 2024-10 | https://www.lesswrong.com/posts/BFamsq52ctyRziDgE | States Transluce's goal of scalable, AI-driven understanding tools

## Apollo Research
- [A] Interpretability in Parameter Space: Minimizing Mechanistic Description Length with Attribution-based Parameter Decomposition (APD) | 2025-01 | https://arxiv.org/abs/2501.14926 | Decomposes the weights themselves into faithful, minimal, simple components; the most direct statement of weight-space interp and its success criteria
- [A] Stochastic Parameter Decomposition (SPD) | 2025-06 | https://arxiv.org/abs/2506.20790 | Scalable successor to APD that recovers ground-truth mechanisms in toy models; current state of weight decomposition
- [B] The Local Interaction Basis: Identifying Computationally-Relevant and Sparsely Interacting Features | 2024-05 | https://arxiv.org/abs/2405.10928 | Builds a basis from weights and gradients to sparsify interactions; weight-informed alternative to SAEs, with mostly negative results on LLMs
- [B] Using Degeneracy in the Loss Landscape for Mechanistic Interpretability | 2024-05 | https://arxiv.org/abs/2405.10927 | Theory link between parameter-space degeneracy and interpretable structure; foundation for LIB and APD
- [A] Identifying Functionally Important Features with End-to-End Sparse Dictionary Learning | 2024-05 | https://arxiv.org/abs/2405.12241 | Trains SAEs on downstream KL rather than reconstruction; changes what "faithful features" means
- [B] Detecting Strategic Deception Using Linear Probes | 2025-02 | https://arxiv.org/abs/2502.03407 | White-box probes as deception detectors in realistic eval settings; interp used for evals
- [B] Mathematical Models of Computation in Superposition | 2024-08 | https://arxiv.org/abs/2408.05451 | Theory of how networks compute (not just store) in superposition; relevant to what weights can encode
- [B] Interpretability as Compression: Reconsidering SAE Explanations of Neural Activations with MDL-SAEs | 2024-10 | https://arxiv.org/abs/2410.11179 | Frames explanations as compression and proposes description-length as the measure
- [C] Identifying Sparsely Active Circuits Through Local Loss Landscape Decomposition | 2025-04 | https://arxiv.org/abs/2504.00194 | Related parameter-space circuit method

## David Bau lab (Northeastern) and NDIF
- [A] Locating and Editing Factual Associations in GPT (ROME) | 2022-02 | https://arxiv.org/abs/2202.05262 | Causal tracing plus a rank-one weight edit; the standard example of linking a mechanism to specific weights
- [B] Mass-Editing Memory in a Transformer (MEMIT) | 2022-10 | https://arxiv.org/abs/2210.07229 | Scales ROME to thousands of edits; tests the key-value view of MLP weights
- [A] Function Vectors in Large Language Models | 2023-10 | https://arxiv.org/abs/2310.15213 | Finds compact vectors from attention heads that carry in-context tasks; a reusable unit of model function
- [A] Linearity of Relation Decoding in Transformer Language Models (LRE) | 2023-08 | https://arxiv.org/abs/2308.09124 | Many relations are well approximated by an affine map from the Jacobian; a simple predictive model of a subcomputation
- [A] NNsight and NDIF: Democratizing Access to Foundation Model Internals | 2024-07 | https://arxiv.org/abs/2407.14561 | Library and remote infrastructure for interventions on large open models; practical experiment substrate
- [A] Network Dissection: Quantifying Interpretability of Deep Visual Representations | 2017-04 | https://arxiv.org/abs/1704.05796 | First quantitative score of unit interpretability against labelled concepts; a foundational measure
- [B] GAN Dissection | 2018-11 | https://arxiv.org/abs/1811.10597 | Dissection plus causal intervention on generators
- [B] Rewriting a Deep Generative Model | 2020-07 | https://arxiv.org/abs/2007.15646 | Treats a layer's weights as an associative memory and edits it; early weight-as-memory view
- [B] Future Lens: Anticipating Subsequent Tokens from a Single Hidden State | 2023-11 | https://arxiv.org/abs/2311.04897 | Reads predictions of future tokens from one state; extends lens methods
- [B] Language Models use Lookbacks to Track Beliefs | 2025-05 | https://arxiv.org/abs/2505.14685 | Detailed mechanism for theory-of-mind style tracking; an example of a recent full-mechanism study
- [B] The Dual-Route Model of Induction | 2025-04 | https://arxiv.org/abs/2504.03022 | Separates token-level and concept-level induction heads
- [B] Fine-Tuning Enhances Existing Mechanisms: A Case Study on Entity Tracking | 2024-02 | https://arxiv.org/abs/2402.14811 | Shows fine-tuning reuses base-model circuits; relevant to predicting behaviour from weight changes
- [C] Erasing Concepts from Diffusion Models | 2023-03 | https://arxiv.org/abs/2303.07345 | Weight-editing concept removal

## Yonatan Belinkov (Technion) and causal mediation / probing critiques
- [A] Probing Classifiers: Promises, Shortcomings, and Advances | 2021-02 | https://arxiv.org/abs/2102.12452 | The standard critique of probing: decodable does not mean used; sets what probes can and cannot show
- [A] Investigating Gender Bias in Language Models Using Causal Mediation Analysis | 2020-04 | https://arxiv.org/abs/2004.12265 | Brought causal mediation (direct and indirect effects) into NLP interp; the ancestor of activation patching
- [A] The Quest for the Right Mediator: A History, Survey, and Theoretical Grounding of Causal Interpretability | 2024-08 | https://arxiv.org/abs/2408.01416 | Survey that organises interp methods by which causal mediator they use; good map of the field's experimental setups
- [A] MIB: A Mechanistic Interpretability Benchmark | 2025-04 | https://arxiv.org/abs/2504.13151 | Shared benchmark for circuit localisation and causal-variable localisation; the field's attempt at standard success measures
- [B] Analysis Methods in Neural Language Processing: A Survey | 2018-12 | https://arxiv.org/abs/1812.08951 | Pre-mechinterp survey of probing and analysis
- [B] Amnesic Probing: Behavioral Explanation with Amnesic Counterfactuals | 2020-06 | https://arxiv.org/abs/2006.00995 | Tests whether information is used by removing it; causal fix to probing
- [B] Null It Out: Guarding Protected Attributes by Iterative Nullspace Projection (INLP) | 2020-04 | https://arxiv.org/abs/2004.07667 | Linear concept removal used in many causal probing tests

## Jacob Andreas (MIT) and MIT CSAIL interpretability
- [A] A Multimodal Automated Interpretability Agent (MAIA) | 2024-04 | https://arxiv.org/abs/2404.14394 | An agent that runs experiments on a model to explain its parts; an early template for automated interp research
- [B] FIND: A Function Description Benchmark for Evaluating Interpretability Methods | 2023-09 | https://arxiv.org/abs/2309.03886 | Benchmark of functions with known descriptions for scoring automated explainers; relevant to how we would score our predictions
- [B] Natural Language Descriptions of Deep Visual Features (MILAN) | 2022-01 | https://arxiv.org/abs/2201.11114 | Generates neuron descriptions in language; precursor to LLM-based auto-interp
- [B] Compositional Explanations of Neurons | 2020-06 | https://arxiv.org/abs/2006.14032 | Logical-formula explanations of neurons; an explicit, checkable explanation format
- [B] What Learning Algorithm is In-Context Learning? Investigations with Linear Models | 2022-11 | https://arxiv.org/abs/2211.15661 | Matches transformer behaviour to known algorithms; explanation as algorithm identification
- [C] Implicit Representations of Meaning in Neural Language Models | 2021-06 | https://arxiv.org/abs/2106.00737 | Probing for world state

## Stanford: Atticus Geiger, Chris Potts and collaborators (causal abstraction)
- [A] Causal Abstractions of Neural Networks | 2021-06 | https://arxiv.org/abs/2106.02997 | Defines an explanation as a high-level causal model that the network implements, tested by interchange interventions; the most formal answer to "what is an explanation"
- [A] Causal Abstraction: A Theoretical Foundation for Mechanistic Interpretability | 2023-01 | https://arxiv.org/abs/2301.04709 | Unifies patching, circuits, DAS and more under one formal theory, with graded faithfulness measures
- [A] Finding Alignments Between Interpretable Causal Variables and Distributed Neural Representations (DAS) | 2023-03 | https://arxiv.org/abs/2303.02536 | Learns rotations to locate causal variables in non-basis-aligned subspaces
- [B] Interpretability at Scale: Identifying Causal Mechanisms in Alpaca (Boundless DAS) | 2023-05 | https://arxiv.org/abs/2305.08809 | Scales DAS to 7B models
- [B] Inducing Causal Structure for Interpretable Neural Networks | 2021-12 | https://arxiv.org/abs/2112.00826 | Trains networks to implement a given causal model; "interpretable by design" link
- [A] The Non-Linear Representation Dilemma: Is Causal Abstraction Enough for Mechanistic Interpretability? | 2025-07 | https://arxiv.org/abs/2507.08802 | Shows that with unrestricted nonlinear alignment any network can be matched to any algorithm; key critique for defining what counts as a real explanation
- [A] AxBench: Steering LLMs? Even Simple Baselines Outperform Sparse Autoencoders | 2025-01 | https://arxiv.org/abs/2501.17148 | Benchmark where prompting and simple probes beat SAEs for concept detection and steering; key negative result
- [B] RAVEL: Evaluating Interpretability Methods on Disentangling Language Model Representations | 2024-02 | https://arxiv.org/abs/2402.17700 | Benchmark for whether methods isolate one attribute without others
- [B] pyvene: A Library for Understanding and Improving PyTorch Models via Interventions | 2024-03 | https://arxiv.org/abs/2403.07809 | Intervention library standardising patching experiments
- [B] ReFT: Representation Finetuning for Language Models | 2024-04 | https://arxiv.org/abs/2404.03592 | Interventions on representations as a fine-tuning method; shows interp tools as control
- [B] Rigorously Assessing Natural Language Explanations of Neurons | 2023-09 | https://arxiv.org/abs/2309.10312 | Finds OpenAI-style neuron explanations fail causal and observational tests; critical for judging explanation quality
- [B] Designing and Interpreting Probes with Control Tasks | 2019-09 | https://arxiv.org/abs/1909.03368 | Selectivity metric so probes measure the model, not the probe
- [C] CausalGym: Benchmarking Causal Interpretability Methods on Linguistic Tasks | 2024-02 | https://arxiv.org/abs/2402.12560 | Benchmark of patching-based methods on syntax

## Max Tegmark's group (MIT) and related geometry work
- [A] Opening the AI Black Box: Program Synthesis via Mechanistic Interpretability (MIPS) | 2024-02 | https://arxiv.org/abs/2402.05110 | Automatically turns trained RNNs into Python code; a direct weights-to-program attempt very close to our aim
- [A] Language Models Use Trigonometry to Do Addition | 2025-02 | https://arxiv.org/abs/2502.00873 | Full mechanism for addition in mid-size LLMs (helix representation plus a "clock" algorithm)
- [A] The Geometry of Truth: Emergent Linear Structure in LLM Representations of True/False Datasets | 2023-10 | https://arxiv.org/abs/2310.06824 | Linear truth direction with causal checks; a standard representation-level result
- [B] Language Models Represent Space and Time | 2023-10 | https://arxiv.org/abs/2310.02207 | Linear world-model representations
- [B] Not All Language Model Features Are Linear | 2024-05 | https://arxiv.org/abs/2405.14860 | Finds circular, multi-dimensional features; challenges the one-direction-per-feature assumption
- [B] The Geometry of Concepts: Sparse Autoencoder Feature Structure | 2024-10 | https://arxiv.org/abs/2410.19750 | Large-scale structure of SAE feature space
- [B] The Clock and the Pizza: Two Stories in Mechanistic Explanation of Neural Networks | 2023-06 | https://arxiv.org/abs/2306.17844 | The same task gives different algorithms depending on hyperparameters; you cannot assume the mechanism from the task
- [B] Seeing is Believing: Brain-Inspired Modular Training for Mechanistic Interpretability | 2023-05 | https://arxiv.org/abs/2305.08746 | Training for weight locality and sparsity so circuits are visible in the weights
- [B] Finding Neurons in a Haystack: Case Studies with Sparse Probing | 2023-05 | https://arxiv.org/abs/2305.01610 | Sparse probing for neurons at scale; monosemantic versus superposed neurons
- [B] Universal Neurons in GPT2 Language Models | 2024-01 | https://arxiv.org/abs/2401.12181 | Neurons that recur across seeds, with weight-based taxonomy; relevant to whether weight-read features are canonical

## Mor Geva (Tel Aviv / Google) and vocabulary-space analysis
- [A] Transformer Feed-Forward Layers Are Key-Value Memories | 2020-12 | https://arxiv.org/abs/2012.14913 | Reads MLP weights as keys (input patterns) and values (vocab distributions); a basic weight-level account of MLPs
- [A] Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space | 2022-03 | https://arxiv.org/abs/2203.14680 | Projects FFN value vectors to the vocabulary to read what each one does
- [A] Analyzing Transformers in Embedding Space | 2022-09 | https://arxiv.org/abs/2209.02535 | Projects all weight matrices into embedding space for input-free reading of parameters; one of the most direct weight-reading frameworks
- [A] Dissecting Recall of Factual Associations in Auto-Regressive Language Models | 2023-04 | https://arxiv.org/abs/2304.14767 | Three-step mechanism for factual recall (subject enrichment, relation propagation, attribute extraction)
- [B] Backward Lens: Projecting Language Model Gradients into the Vocabulary Space | 2024-02 | https://arxiv.org/abs/2402.12865 | Reads gradient updates in vocab space; relevant to explaining weight changes
- [B] Enhancing Automated Interpretability with Output-Centric Feature Descriptions | 2025-01 | https://arxiv.org/abs/2501.08319 | Argues feature descriptions must cover what a feature does to outputs, not just what activates it

## Redwood Research, Arthur Conmy, and the circuit-discovery line
- [A] Causal Scrubbing: A Method for Rigorously Testing Interpretability Hypotheses | 2022-12 | https://www.alignmentforum.org/posts/JvZhhzycHu2Yd57RN/causal-scrubbing-a-method-for-rigorously-testing | Formal test: resample everything the hypothesis says does not matter and measure loss recovered; a key faithfulness standard
- [A] Interpretability in the Wild: A Circuit for Indirect Object Identification in GPT-2 Small (IOI) | 2022-11 | https://arxiv.org/abs/2211.00593 | The canonical end-to-end circuit, with faithfulness, completeness and minimality criteria
- [A] Towards Automated Circuit Discovery for Mechanistic Interpretability (ACDC) | 2023-04 | https://arxiv.org/abs/2304.14997 | Automates circuit finding by pruning edges, benchmarked on known circuits
- [B] Attribution Patching Outperforms Automated Circuit Discovery (EAP) | 2023-10 | https://arxiv.org/abs/2310.10348 | Edge attribution patching as a fast circuit finder
- [B] Have Faith in Faithfulness: Going Beyond Circuit Overlap When Finding Model Mechanisms | 2024-03 | https://arxiv.org/abs/2403.17806 | EAP-IG, and shows circuit-overlap metrics mislead; measure faithfulness directly
- [B] Finding Transformer Circuits with Edge Pruning | 2024-06 | https://arxiv.org/abs/2406.16778 | Gradient-based edge pruning that scales circuit discovery
- [B] How Does GPT-2 Compute Greater-Than? | 2023-05 | https://arxiv.org/abs/2305.00586 | Small complete circuit case study with a generalisation test
- [B] Copy Suppression: Comprehensively Understanding an Attention Head | 2023-10 | https://arxiv.org/abs/2310.04625 | Explains about 77% of one head's behaviour using weight-based analysis; a model of "complete" component understanding
- [C] Polysemanticity and Capacity in Neural Networks | 2022-10 | https://arxiv.org/abs/2210.01892 | Capacity-allocation theory of polysemanticity

## Neel Nanda's academic and MATS collaborations (grokking, toy models, SAEs)
- [A] Progress Measures for Grokking via Mechanistic Interpretability | 2023-01 | https://arxiv.org/abs/2301.05217 | Fully reverse-engineers modular addition from the weights (Fourier algorithm) and uses it to define progress measures; the clearest example of complete weight-level understanding
- [B] A Toy Model of Universality: Reverse Engineering How Networks Learn Group Operations | 2023-02 | https://arxiv.org/abs/2302.03025 | Representation-theory algorithm across group tasks; tests universality
- [B] Emergent Linear Representations in World Models of Self-Supervised Sequence Models | 2023-09 | https://arxiv.org/abs/2309.00941 | Othello-GPT board state is linear (mine vs theirs); shows the right basis matters
- [B] Refusal in Language Models Is Mediated by a Single Direction | 2024-06 | https://arxiv.org/abs/2406.11717 | Finds one direction that controls refusal and edits it into the weights; widely reused result
- [B] Chain-of-Thought Reasoning In The Wild Is Not Always Faithful | 2025-03 | https://arxiv.org/abs/2503.08679 | Measures unfaithful CoT in natural prompts; limits CoT as explanation
- [C] Thought Anchors: Which LLM Reasoning Steps Matter? | 2025-06 | https://arxiv.org/abs/2506.19143 | Sentence-level attribution in reasoning traces
- [B] Transcoders Find Interpretable LLM Feature Circuits | 2024-06 | https://arxiv.org/abs/2406.11944 | Transcoders let circuits be read as input-independent weight products between features; bridges features and weights
- [B] Sparse Autoencoders Do Not Find Canonical Units of Analysis | 2025-02 | https://arxiv.org/abs/2502.04878 | SAE stitching and meta-SAEs show features are not atomic; questions the SAE basis as ground truth
- [B] A is for Absorption: Studying Feature Splitting and Absorption in Sparse Autoencoders | 2024-09 | https://arxiv.org/abs/2409.14507 | Documents a systematic SAE failure that breaks feature-level explanations
- [A] SAEBench: A Comprehensive Benchmark for Sparse Autoencoders | 2025-03 | https://arxiv.org/abs/2503.09532 | Standard multi-metric SAE evaluation; shows proxy metrics and real usefulness diverge
- [C] Convergent Linear Representations of Emergent Misalignment | 2025-06 | https://arxiv.org/abs/2506.11618 | Single direction mediating emergent misalignment

## Other academic and independent work that became widely cited
- [A] Open Problems in Mechanistic Interpretability | 2025-01 | https://arxiv.org/abs/2501.16496 | Multi-lab survey of the field's goals, methods, and unsolved problems; the closest thing to a consensus statement of what is unsolved
- [A] interpreting GPT: the logit lens | 2020-08 | https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens | Decoding intermediate residuals with the unembedding; the origin of lens methods
- [A] Emergent World Representations: Exploring a Sequence Model Trained on a Synthetic Task (Othello-GPT) | 2022-10 | https://arxiv.org/abs/2210.13382 | Evidence of internal world models via probes and interventions
- [A] Sparse Autoencoders Find Highly Interpretable Features in Language Models | 2023-09 | https://arxiv.org/abs/2309.08600 | Independent and EleutherAI-linked SAE paper that, with Anthropic's work, launched the dictionary-learning era
- [A] Sparse Feature Circuits: Discovering and Editing Interpretable Causal Graphs in Language Models | 2024-03 | https://arxiv.org/abs/2403.19647 | Circuits over SAE features with attribution; the precursor to attribution graphs (Bau lab and Belinkov)
- [A] Bilinear MLPs Enable Weight-based Mechanistic Interpretability | 2024-10 | https://arxiv.org/abs/2410.08417 | Bilinear layers let features and interactions be read from weights by eigendecomposition with no data; probably the most relevant paper for our weights-first project
- [A] Compact Proofs of Model Performance via Mechanistic Interpretability | 2024-06 | https://arxiv.org/abs/2406.11779 | Measures understanding by the length of a formal proof of model behaviour derived from the weights; a rigorous, predictive success measure
- [A] The Linear Representation Hypothesis and the Geometry of Large Language Models | 2023-11 | https://arxiv.org/abs/2311.03658 | Formalises what "linear representation" means and the right inner product; theoretical underpinning for probes and steering
- [A] Representation Engineering: A Top-Down Approach to AI Transparency | 2023-10 | https://arxiv.org/abs/2310.01405 | Population-level reading and control of concepts; the main top-down alternative to circuits
- [A] Discovering Latent Knowledge in Language Models Without Supervision (CCS) | 2022-12 | https://arxiv.org/abs/2212.03827 | Unsupervised truth probing; started the latent-knowledge line
- [B] Steering Language Models With Activation Engineering (ActAdd) | 2023-08 | https://arxiv.org/abs/2308.10248 | Steering vectors from contrastive prompts
- [B] Steering Llama 2 via Contrastive Activation Addition | 2023-12 | https://arxiv.org/abs/2312.06681 | Standard steering-vector method and evaluation
- [B] Thinking Like Transformers (RASP) | 2021-06 | https://arxiv.org/abs/2106.06981 | Programming language for transformer computations; the target language for weights-to-program work
- [B] Learning Transformer Programs | 2023-06 | https://arxiv.org/abs/2306.01128 | Trains transformers constrained to be decompiled into readable Python
- [B] Interpretability Illusions in the Generalization of Simplified Models | 2023-12 | https://arxiv.org/abs/2312.03656 | Simplified explanations look faithful in distribution but fail out of distribution; key for predictive-model evaluation
- [B] A Primer on the Inner Workings of Transformer-based Language Models | 2024-05 | https://arxiv.org/abs/2405.00208 | Technical primer covering methods and known components
- [B] Mechanistic Interpretability for AI Safety: A Review | 2024-04 | https://arxiv.org/abs/2404.14082 | Broad review of concepts and methods
- [B] Against Almost Every Theory of Impact of Interpretability | 2023-08 | https://www.alignmentforum.org/posts/LNA8mubrByG7SFacm/against-almost-every-theory-of-impact-of-interpretability-1 | Widely discussed critique of interp's safety value
- [C] Neurons in Large Language Models: Dead, N-gram, Positional | 2023-09 | https://arxiv.org/abs/2309.04827 | Neuron taxonomy in OPT
- [C] Interpreting Neural Networks through the Polytope Lens | 2022-11 | https://arxiv.org/abs/2211.12312 | Proposes piecewise-linear regions as the unit of analysis
- [C] Position: An Inner Interpretability Framework for AI Inspired by Lessons from Cognitive Neuroscience | 2024-06 | https://arxiv.org/abs/2406.01352 | Applies Marr-style levels from cognitive science to interp
- [C] The Misguided Quest for Mechanistic AI Interpretability | 2025-05 | https://ai-frontiers.org/articles/the-misguided-quest-for-mechanistic-ai-interpretability | Hendrycks-style critique of bottom-up interp

TOTAL: 179 (A=70, B=91, C=18)
