# Aether reader notes: AI interpretability survey

*Reader: Aether (DeepSeek Flash), long-running loop. Entry format: [../SCHEMA.md](../SCHEMA.md). Started 2026-11-12.*

## Status

- Entries written: 21 (INDEX.md is authoritative)
- Last commit: literature (aether): 21 entries
- Current source: `SEED_QUEUE.md` long tail, priority block first. Core already covers the three field surveys,
  the main transformer-circuits posts and the main Goodfire posts, so Aether takes the rest.
- Note 2026-11-12: the Priority block is now fully ticked; from here the loop works down the raw seed queue.

## Queue

Working rule: take the top unchecked item, skip anything whose key already exists in `aether/` or `core/`.

### Priority block (most relevant to reading weights, prediction under intervention, evaluation)

- [x] Unsupervised Decoding of Encoded Reasoning Using LM Interpretability | https://arxiv.org/abs/2512.01222 | logit lens decodes ROT-13 CoT
- [x] The Value Axis (on right track) | https://arxiv.org/abs/2606.17056 | DONE
- [x] A Global Workspace in Language Models | https://www.anthropic.com/research/global-workspace | J-space / J-lens, broadcast channel
- [x] HeadVis | https://transformer-circuits.pub/2026/headvis/index.html | head inspection tool; attention decomposition agenda
- [x] Slot Machines: multiple entities | https://arxiv.org/abs/2604.21139 | current/prior entity slots; decodable-but-unused
- [x] Latent Planning Emerges with Scale | https://arxiv.org/abs/2604.12493 | planning = causally causes distant token AND its licence
- [x] Reading Between the Dots: decoding across filler tokens | https://arxiv.org/abs/2607.03502 | hidden computation
- [x] A Shared Subcircuit Lets LLMs Count Down | https://arxiv.org/abs/2607.12279 | DONE (countdown heads, layer-18 last-use, cross-model motif)
- [x] Evaluating and Improving LLM Self-Modeling | https://arxiv.org/abs/2608.30980 | DONE (skill score vs dummy predictor; no own-model advantage)
- [x] From Simulation to Enaction | https://arxiv.org/abs/2605.25459 | DONE (entropy as implicit on-policy recognition; surprise direction causal; explicit detection is a separate circuit)
- [ ] Natural Language Autoencoders (summary page) | 2026-05 | tcpub; core may cover
- [x] Signs of Introspection in LLMs | https://www.anthropic.com/research/introspection | DONE (concept injection, ~20% detection, detect-before-name ordering control)
- [x] Believe It or Not: implanted facts | https://alignment.anthropic.com/2025/believe-it-or-not/ | DONE (belief depth = generality + robustness + representation; SDF > prompting/AlphaEdit; plausibility confound)
- [ ] Do Reasoning Models Use Their Scratchpad Like We Do | 2025-03 | 
- [ ] Reasoning Models Don't Always Say What They Think | 2025-04 | CoT faithfulness
- [ ] Reasoning Theater: Performative CoT (Goodfire) | 2026-03 | 
- [ ] Fine-Tuned Lie Detectors Failed to Generalize | 2026-08 | probe generalisation failure
- [ ] Liars' Bench | https://arxiv.org/abs/2511.16035 | benchmark
- [ ] Evaluating Honesty and Lie Detection Techniques | 2025-11 | 
- [ ] Simple Probes Can Catch Sleeper Agents | 2024-04 | probe
- [ ] Model-Internals Classifiers | 2025-06 | 
- [ ] Next-Generation Constitutional Classifiers | 2026-01 | 
- [ ] Verbalized Eval Awareness Inflates Measured Safety (Goodfire) | 2026-05 | eval awareness
- [ ] Logits as a new monitor for evaluation awareness (Goodfire) | 2026-06 | monitor
- [x] Steering Evaluation-Aware LMs to Act Like They Are Deployed | https://arxiv.org/abs/2510.20487 | DONE (Wood Labs organism; pre-fine-tune vector; 80-86%→<11%)
- [ ] Understanding Memorization via Loss Curvature (Goodfire) | 2025-11 | weight curvature
- [ ] Priors in Time (Goodfire) | https://arxiv.org/abs/2511.01836 | 
- [ ] Belief Dynamics: ICL and activation steering (Goodfire) | 2025-11 | 
- [ ] Predicting Rare LLM Failures with 30x Fewer Rollouts (Goodfire) | 2026-05 | 
- [ ] Forking Fast: uncertainty dynamics (Goodfire) | 2026-08 | 
- [ ] Probe-Based Data Attribution (Goodfire) | 2026-04 | 
- [ ] Features as Rewards (Goodfire) | https://arxiv.org/abs/2602.10067 | 
- [ ] Covariance-based Sequence Pooling (Goodfire) | 2026-04 | 
- [ ] Interpreting Language Model Parameters (VPD explainer, Goodfire) | 2026-05 | weight decomposition explainer
- [ ] Neuron Atlas - Qwen3.6 (Goodfire) | 2026-11 | 

### Raw seed queue (generated from SEED_QUEUE.md; key | title | link | org)

- transformer-circuits-pub-2021-exercises-index-html | Exercises | https://transformer-circuits.pub/2021/exercises/index.html | anthropic
- transformer-circuits-pub-2021-videos-index-html | Videos | https://transformer-circuits.pub/2021/videos/index.html | anthropic
- transformer-circuits-pub-2021-garcon-index-html | Garcon | https://transformer-circuits.pub/2021/garcon/index.html | anthropic
- github-com-anthropics-pysvelte | PySvelte | https://github.com/anthropics/PySvelte | anthropic
- anthropic-com-research-scaling-laws-and-interpretability-of-learning-from-repeated-data | Scaling Laws and Interpretability of Learning from Repeated Data | https://www.anthropic.com/research/scaling-laws-and-interpretability-of-learning-from-repeated-data | anthropic
- transformer-circuits-pub-2022-solu-index-html | Softmax Linear Units | https://transformer-circuits.pub/2022/solu/index.html | anthropic
- anthropic-com-research-language-models-mostly-know-what-they-know | Language Models (Mostly) Know What They Know | https://www.anthropic.com/research/language-models-mostly-know-what-they-know | anthropic
- arxiv-2211.09169 | Engineering Monosemanticity in Toy Models | https://arxiv.org/abs/2211.09169 | anthropic
- transformer-circuits-pub-2023-toy-double-descent-index-html | Superposition, Memorization, and Double Descent | https://transformer-circuits.pub/2023/toy-double-descent/index.html | anthropic
- transformer-circuits-pub-2023-may-update-index-html | Circuits Updates, May 2023 | https://transformer-circuits.pub/2023/may-update/index.html | anthropic
- transformer-circuits-pub-2023-july-update-index-html | Circuits Updates, July 2023 | https://transformer-circuits.pub/2023/july-update/index.html | anthropic
- anthropic-com-research-measuring-faithfulness-in-chain-of-thought-reasoning | Measuring Faithfulness in Chain-of-Thought Reasoning | https://www.anthropic.com/research/measuring-faithfulness-in-chain-of-thought-reasoning | anthropic
- anthropic-com-research-question-decomposition-improves-the-faithfulness-of-model-generated-reasoning | Question Decomposition Improves the Faithfulness of Model-Generated Reasoning | https://www.anthropic.com/research/question-decomposition-improves-the-faithfulness-of-model-generated-reasoning | anthropic
- anthropic-com-research-studying-large-language-model-generalization-with-influence-functions | Studying Large Language Model Generalization with Influence Functions | https://www.anthropic.com/research/studying-large-language-model-generalization-with-influence-functions | anthropic
- anthropic-com-research-decomposing-language-models-into-understandable-components | Decomposing Language Models Into Understandable Components | https://www.anthropic.com/research/decomposing-language-models-into-understandable-components | anthropic
- transformer-circuits-pub-2024-jan-update-index-html | Circuits Updates, January 2024 | https://transformer-circuits.pub/2024/jan-update/index.html | anthropic
- transformer-circuits-pub-2024-feb-update-index-html | Circuits Updates, February 2024 | https://transformer-circuits.pub/2024/feb-update/index.html | anthropic
- transformer-circuits-pub-2024-march-update-index-html | Circuits Updates, March 2024 | https://transformer-circuits.pub/2024/march-update/index.html | anthropic
- transformer-circuits-pub-2024-april-update-index-html | Circuits Updates, April 2024 | https://transformer-circuits.pub/2024/april-update/index.html | anthropic
- anthropic-com-research-probes-catch-sleeper-agents | Simple Probes Can Catch Sleeper Agents | https://www.anthropic.com/research/probes-catch-sleeper-agents | anthropic
- anthropic-com-research-mapping-mind-language-model | Mapping the Mind of a Large Language Model | https://www.anthropic.com/research/mapping-mind-language-model | anthropic
- anthropic-com-research-golden-gate-claude | Golden Gate Claude | https://www.anthropic.com/research/golden-gate-claude | anthropic
- transformer-circuits-pub-2024-june-update-index-html | Circuits Updates, June 2024 | https://transformer-circuits.pub/2024/june-update/index.html | anthropic
- anthropic-com-research-engineering-challenges-interpretability | The Engineering Challenges of Scaling Interpretability | https://www.anthropic.com/research/engineering-challenges-interpretability | anthropic
- transformer-circuits-pub-2024-july-update-index-html | Circuits Updates, July 2024 | https://transformer-circuits.pub/2024/july-update/index.html | anthropic
- transformer-circuits-pub-2024-august-update-index-html | Circuits Updates, August 2024 | https://transformer-circuits.pub/2024/august-update/index.html | anthropic
- transformer-circuits-pub-2024-september-update-index-html | Circuits Updates, September 2024 | https://transformer-circuits.pub/2024/september-update/index.html | anthropic
- transformer-circuits-pub-2024-features-as-classifiers-index-html | Using Dictionary Learning Features as Classifiers | https://transformer-circuits.pub/2024/features-as-classifiers/index.html | anthropic
- anthropic-com-research-evaluating-feature-steering | Evaluating Feature Steering: A Case Study in Mitigating Social Biases | https://www.anthropic.com/research/evaluating-feature-steering | anthropic
- arxiv-2411.18895 | Evaluating Sparse Autoencoders on Targeted Concept Erasure Tasks | https://arxiv.org/abs/2411.18895 | anthropic
- transformer-circuits-pub-2025-january-update-index-html | Circuits Updates, January 2025 | https://transformer-circuits.pub/2025/january-update/index.html | anthropic
- alignment-anthropic-com-2025-recommended-directions-index-html | Recommendations for Technical AI Safety Research Directions | https://alignment.anthropic.com/2025/recommended-directions/index.html | anthropic
- anthropic-com-research-tracing-thoughts-language-model | Tracing the Thoughts of a Large Language Model | https://www.anthropic.com/research/tracing-thoughts-language-model | anthropic
- alignment-anthropic-com-2025-distill-paraphrases | Do Reasoning Models Use Their Scratchpad Like We Do? Evidence from Distilling Paraphrases | https://alignment.anthropic.com/2025/distill-paraphrases/ | anthropic
- transformer-circuits-pub-2025-april-update-index-html | Circuits Updates, April 2025 | https://transformer-circuits.pub/2025/april-update/index.html | anthropic
- anthropic-com-research-reasoning-models-dont-say-think | Reasoning Models Don't Always Say What They Think | https://www.anthropic.com/research/reasoning-models-dont-say-think | anthropic
- anthropic-com-research-open-source-circuit-tracing | Open-Sourcing Circuit-Tracing Tools | https://www.anthropic.com/research/open-source-circuit-tracing | anthropic
- alignment-anthropic-com-2025-cheap-monitors | Model-Internals Classifiers (Cost-Effective Constitutional Classifiers via Representation Re-use) | https://alignment.anthropic.com/2025/cheap-monitors/ | anthropic
- arxiv-2506.10922 | Robustly Improving LLM Fairness in Realistic Settings via Interpretability | https://arxiv.org/abs/2506.10922 | anthropic
- transformer-circuits-pub-2025-july-update-index-html | Circuits Updates, July 2025 | https://transformer-circuits.pub/2025/july-update/index.html | anthropic
- arxiv-2507.16795 | Steering Out-of-Distribution Generalization with Concept Ablation Fine-Tuning | https://arxiv.org/abs/2507.16795 | anthropic
- transformer-circuits-pub-2025-august-update-index-html | Circuits Updates, August 2025 | https://transformer-circuits.pub/2025/august-update/index.html | anthropic
- transformer-circuits-pub-2025-september-update-index-html | Circuits Updates, September 2025 | https://transformer-circuits.pub/2025/september-update/index.html | anthropic
- assets-anthropic-com-m-12f214efcc2f457a-original-claude-sonnet-4-5-system-card-pdf | Claude Sonnet 4.5 System Card | https://assets.anthropic.com/m/12f214efcc2f457a/original/Claude-Sonnet-4-5-System-Card.pdf | anthropic
- transformer-circuits-pub-2025-october-update-index-html | Circuits Updates, October 2025 | https://transformer-circuits.pub/2025/october-update/index.html | anthropic
- anthropic-com-research-introspection | Signs of Introspection in Large Language Models (Emergent Introspective Awareness, summary) | https://www.anthropic.com/research/introspection | anthropic
- alignment-anthropic-com-2025-believe-it-or-not | Believe It or Not: How Deeply do LLMs Believe Implanted Facts? | https://alignment.anthropic.com/2025/believe-it-or-not/ | anthropic
- arxiv-2510.20487 | Steering Evaluation-Aware Language Models to Act Like They Are Deployed | https://arxiv.org/abs/2510.20487 | anthropic
- transformer-circuits-pub-2025-november-update-index-html | Circuits Updates, November 2025 | https://transformer-circuits.pub/2025/november-update/index.html | anthropic
- alignment-anthropic-com-2025-honesty-elicitation | Evaluating Honesty and Lie Detection Techniques on a Diverse Suite of Dishonest Models | https://alignment.anthropic.com/2025/honesty-elicitation/ | anthropic
- arxiv-2511.16035 | Liars' Bench: Evaluating Lie Detectors for Language Models | https://arxiv.org/abs/2511.16035 | anthropic
- alignment-anthropic-com-2025-selective-gradient-masking | Beyond Data Filtering: Knowledge Localization for Capability Removal in LLMs | https://alignment.anthropic.com/2025/selective-gradient-masking | anthropic
- alignment-anthropic-com-2025-auditing-mo-replication | Open Source Replication of the Auditing Game Model Organism | https://alignment.anthropic.com/2025/auditing-mo-replication/ | anthropic
- arxiv-2512.01222 | Unsupervised Decoding of Encoded Reasoning Using Language Model Interpretability | https://arxiv.org/abs/2512.01222 | anthropic
- anthropic-com-research-next-generation-constitutional-classifiers | Next-Generation Constitutional Classifiers | https://www.anthropic.com/research/next-generation-constitutional-classifiers | anthropic
- anthropic-com-research-assistant-axis | The Assistant Axis: Situating and Stabilizing the Default Persona of Language Models | https://www.anthropic.com/research/assistant-axis | anthropic
- anthropic-com-research-persona-selection-model | The Persona Selection Model | https://www.anthropic.com/research/persona-selection-model | anthropic
- arxiv-2603.05494 | Censored LLMs as a Natural Testbed for Secret Knowledge Elicitation | https://arxiv.org/abs/2603.05494 | anthropic
- transformer-circuits-pub-2026-emotions-index-html | Emotion Concepts and their Function in a Large Language Model | https://transformer-circuits.pub/2026/emotions/index.html | anthropic
- anthropic-com-research-emotion-concepts-function | Emotion Concepts in a Large Language Model (summary) | https://www.anthropic.com/research/emotion-concepts-function | anthropic
- www-cdn-anthropic-com-08ab9158070959f88f296514c21b7facce6f52bc-pdf | Claude Mythos Preview System Card | https://www-cdn.anthropic.com/08ab9158070959f88f296514c21b7facce6f52bc.pdf | anthropic
- arxiv-2604.12493 | Latent Planning Emerges with Scale | https://arxiv.org/abs/2604.12493 | anthropic
- arxiv-2604.14865 | Segment-Level Coherence for Robust Harmful Intent Probing in LLMs | https://arxiv.org/abs/2604.14865 | anthropic
- arxiv-2604.21139 | Slot Machines: How LLMs Keep Track of Multiple Entities | https://arxiv.org/abs/2604.21139 | anthropic
- transformer-circuits-pub-2026-headvis-index-html | HeadVis | https://transformer-circuits.pub/2026/headvis/index.html | anthropic
- anthropic-com-research-natural-language-autoencoders | Natural Language Autoencoders (summary) | https://www.anthropic.com/research/natural-language-autoencoders | anthropic
- arxiv-2605.25459 | From Simulation to Enaction: Post-trained Language Models Recognize and React to Their Own Generations | https://arxiv.org/abs/2605.25459 | anthropic
- arxiv-2606.02609 | Building Better Activation Oracles | https://arxiv.org/abs/2606.02609 | anthropic
- transformer-circuits-pub-2026-may-update-index-html | Circuits Updates, May 2026 | https://transformer-circuits.pub/2026/may-update/index.html | anthropic
- transformer-circuits-pub-2026-june-update-index-html | Circuits Updates, June 2026 | https://transformer-circuits.pub/2026/june-update/index.html | anthropic
- www-cdn-anthropic-com-2f9323abbcc4abe219577539efe19a623c9ca2bd-claude-20fable-205-20-26-20claude-20mythos-205-20system-20card-pdf | Claude Fable 5 & Claude Mythos 5 System Card | https://www-cdn.anthropic.com/2f9323abbcc4abe219577539efe19a623c9ca2bd/Claude%20Fable%205%20%26%20Claude%20Mythos%205%20System%20Card.pdf | anthropic
- arxiv-2606.17056 | The Value Axis: Language Models Encode Whether They're on the Right Track | https://arxiv.org/abs/2606.17056 | anthropic
- anthropic-com-research-global-workspace | A Global Workspace in Language Models (summary) | https://www.anthropic.com/research/global-workspace | anthropic
- arxiv-2607.03502 | Reading Between the Dots: Decoding Hidden Computation across Filler Tokens | https://arxiv.org/abs/2607.03502 | anthropic
- arxiv-2607.12279 | A Shared Subcircuit Lets LLMs Count Down Across Tasks | https://arxiv.org/abs/2607.12279 | anthropic
- alignment-anthropic-com-2026-lie-detectors | Fine-Tuned Lie Detectors Failed to Generalize | https://alignment.anthropic.com/2026/lie-detectors/ | anthropic
- arxiv-2608.30980 | Evaluating and Improving LLM Self-Modeling | https://arxiv.org/abs/2608.30980 | anthropic
- arxiv-2609.34056 | Steering Language Model Goals with Value Transplant | https://arxiv.org/abs/2609.34056 | anthropic
- transformer-circuits-pub-2026-october-update-index-html | Circuits Updates, October 2026 | https://transformer-circuits.pub/2026/october-update/index.html | anthropic
- anthropic-com-research-alignment-assessment-ukaisi | An Alignment Assessment of the UK AISI Cybertesting Incident | https://www.anthropic.com/research/alignment-assessment-ukaisi | anthropic
- arxiv-2510.01070 | Eliciting Secret Knowledge from Language Models | https://arxiv.org/abs/2510.01070 | anthropic+core_topics
- arxiv-2312.06681 | Steering Llama 2 via Contrastive Activation Addition | https://arxiv.org/abs/2312.06681 | anthropic+core_topics+other_labs
- goodfire-com-research-understanding-and-steering-llama-3 | Understanding and Steering Llama 3 with Sparse Autoencoders | https://www.goodfire.com/research/understanding-and-steering-llama-3 | goodfire
- goodfire-com-blog-feature-steering-for-reliable-and-expressive-ai-engineering | Feature Steering for Reliable and Expressive AI Engineering | https://www.goodfire.com/blog/feature-steering-for-reliable-and-expressive-ai-engineering | goodfire
- goodfire-ai-blog-announcing-goodfire-ember | Goodfire Ember: Scaling Interpretability for Frontier Model Alignment | https://goodfire.ai/blog/announcing-goodfire-ember | goodfire
- goodfire-com-blog-our-approach-to-safety | Our Approach to Safety at Goodfire | https://www.goodfire.com/blog/our-approach-to-safety | goodfire
- goodfire-com-blog-sae-open-source-announcement | Announcing Open-Source SAEs for Llama 3.3 70B and Llama 3.1 8B | https://www.goodfire.com/blog/sae-open-source-announcement | goodfire
- goodfire-com-research-interpreting-evo-2 | Interpreting Evo 2: Arc Institute's Next-Generation Genomic Foundation Model | https://www.goodfire.com/research/interpreting-evo-2 | goodfire
- goodfire-com-research-under-the-hood-of-a-reasoning-model | Under the Hood of a Reasoning Model | https://www.goodfire.com/research/under-the-hood-of-a-reasoning-model | goodfire
- goodfire-com-blog-announcing-our-50m-series-a | Announcing Our $50M Series A to Advance AI Interpretability Research | https://www.goodfire.com/blog/announcing-our-50m-series-a | goodfire
- goodfire-com-research-painting-with-concepts | Painting With Concepts Using Diffusion Model Latents | https://www.goodfire.com/research/painting-with-concepts | goodfire
- goodfire-com-blog-radical-partnership-announcement | Partnering with Radical AI to Advance Materials Science With Interpretability | https://www.goodfire.com/blog/radical-partnership-announcement | goodfire
- goodfire-com-research-phylogeny-manifold | Finding the Tree of Life in Evo 2 | https://www.goodfire.com/research/phylogeny-manifold | goodfire
- goodfire-com-blog-mayo-clinic-collaboration | Goodfire Announces Collaboration to Advance Genomic Medicine with AI Interpretability (Mayo Clinic) | https://www.goodfire.com/blog/mayo-clinic-collaboration | goodfire
- goodfire-com-research-rakuten-sae-probes-for-pii-detection | Deploying Interpretability to Production with Rakuten: SAE Probes for PII Detection | https://www.goodfire.com/research/rakuten-sae-probes-for-pii-detection | goodfire
- goodfire-com-blog-fellowship-fall-25 | Announcing Goodfire's Fellowship Program for Interpretability Research | https://www.goodfire.com/blog/fellowship-fall-25 | goodfire
- goodfire-com-research-understanding-memorization-via-loss-curvature | Understanding Memorization via Loss Curvature | https://www.goodfire.com/research/understanding-memorization-via-loss-curvature | goodfire
- goodfire-com-research-belief-dynamics-icl-steering | Belief Dynamics Reveal the Dual Nature of In-Context Learning and Activation Steering | https://www.goodfire.com/research/belief-dynamics-icl-steering | goodfire
- arxiv-2511.01836 | Priors in Time (arXiv / ICLR 2026) | https://arxiv.org/abs/2511.01836 | goodfire
- goodfire-com-blog-ap293-guest-lectures-25 | Stanford Guest Lectures: AP293 (Fall 2025) | https://www.goodfire.com/blog/ap293-guest-lectures-25 | goodfire
- goodfire-com-research-interpretability-for-alzheimers-detection | Using Interpretability to Identify a Novel Class of Alzheimer's Biomarkers | https://www.goodfire.com/research/interpretability-for-alzheimers-detection | goodfire
- goodfire-com-research-rlfr | Features as Rewards: Using Interpretability to Reduce Hallucinations (RLFR) | https://www.goodfire.com/research/rlfr | goodfire
- arxiv-2602.10067 | Features as Rewards: Scalable Supervision for Open-Ended Tasks via Interpretability (arXiv) | https://arxiv.org/abs/2602.10067 | goodfire
- goodfire-com-blog-interpretability-infra-at-frontier-scale | Interpretability Infrastructure at Frontier Scale: Harvesting Activations from a Trillion-Parameter Model | https://www.goodfire.com/blog/interpretability-infra-at-frontier-scale | goodfire
- goodfire-com-blog-intentional-design | Intentionally Designing the Future of AI | https://www.goodfire.com/blog/intentional-design | goodfire
- goodfire-com-blog-our-series-b | Understanding, Learning From, and Designing AI: Our Series B | https://www.goodfire.com/blog/our-series-b | goodfire
- goodfire-com-research-reasoning-theater | Reasoning Theater: Probing for Performative Chain-of-Thought | https://www.goodfire.com/research/reasoning-theater | goodfire
- goodfire-com-research-probe-based-data-attribution | Probe-Based Data Attribution: Surfacing and Mitigating Undesirable Behaviors in LLM Post-Training | https://www.goodfire.com/research/probe-based-data-attribution | goodfire
- goodfire-com-research-evee-explaining-genetic-variants | Explaining 4.2 million genetic variants with state-of-the-art, interpretable predictions (EVEE) | https://www.goodfire.com/research/evee-explaining-genetic-variants | goodfire
- goodfire-com-research-covariance-pooling | Covariance-based Sequence Pooling | https://www.goodfire.com/research/covariance-pooling | goodfire
- goodfire-com-research-self-correcting-search | Using Self-Correcting Search to Accelerate Materials Discovery | https://www.goodfire.com/research/self-correcting-search | goodfire
- goodfire-com | Silico (agentic interpretability and model-debugging platform) | https://www.goodfire.com/ | goodfire
- goodfire-com-research-predicting-rare-llm-failures-with-30x-fewer-rollouts | Predicting Rare LLM Failures with 30x Fewer Rollouts | https://www.goodfire.com/research/predicting-rare-llm-failures-with-30x-fewer-rollouts | goodfire
- goodfire-com-research-vpd-explainer | Paper Summary: Interpreting Language Model Parameters | https://www.goodfire.com/research/vpd-explainer | goodfire
- goodfire-com-research-verbalized-eval-awareness-inflates-measured-safety | Verbalized Eval Awareness Inflates Measured Safety | https://www.goodfire.com/research/verbalized-eval-awareness-inflates-measured-safety | goodfire
- goodfire-com-blog-soc-2-type-ii | Announcing our SOC 2 Type II Certification | https://www.goodfire.com/blog/soc-2-type-ii | goodfire
- goodfire-com-research-stories-in-space | Meandering on Manifolds: The Neural Geometry of Stories Over Time | https://www.goodfire.com/research/stories-in-space | goodfire
- goodfire-com-research-logits-as-a-new-monitor-for-evaluation-awareness | Logits as a new monitor for evaluation awareness | https://www.goodfire.com/research/logits-as-a-new-monitor-for-evaluation-awareness | goodfire
- goodfire-com-research-bsf-vision | Uncovering Neural Geometry in Vision Models With Block-Sparse Featurizers | https://www.goodfire.com/research/bsf-vision | goodfire
- goodfire-com-research-forking-fast | Forking Fast: Efficiently Estimating Uncertainty Dynamics in Text Generation | https://www.goodfire.com/research/forking-fast | goodfire
- goodfire-com-blog-ai-safety-still-needs-great-engineers | AI Safety Still Needs Great Engineers | https://www.goodfire.com/blog/ai-safety-still-needs-great-engineers | goodfire
- goodfire-com-blog-announcing-goodfire-research-grants | Announcing Goodfire Research Grants | https://www.goodfire.com/blog/announcing-goodfire-research-grants | goodfire
- goodfire-com-research-reward-hacking-activation-monitors | Models know when they're reward hacking - and we can catch them at scale | https://www.goodfire.com/research/reward-hacking-activation-monitors | goodfire
- goodfire-com-blog-we-can-and-must-solve-alignment | We can and must solve alignment | https://www.goodfire.com/blog/we-can-and-must-solve-alignment | goodfire
- goodfire-com-blog-a-practical-guide-to-saes | A practical guide to sparse autoencoders (SAEs) | https://www.goodfire.com/blog/a-practical-guide-to-saes | goodfire
- goodfire-com-blog-probe-monitors-101 | How to build fast, efficient monitors for AI models using probes | https://www.goodfire.com/blog/probe-monitors-101 | goodfire
- goodfire-com-research-production-cyber-monitors-on-kimi-k3 | Training and Deploying Production Cyber Monitors on Kimi K3 | https://www.goodfire.com/research/production-cyber-monitors-on-kimi-k3 | goodfire
- goodfire-com-research-better-biosecurity-monitors | Better biosecurity monitors for AI agents via protein embeddings | https://www.goodfire.com/research/better-biosecurity-monitors | goodfire
- goodfire-com-blog-goodfire-baseten-partnership | Goodfire and Baseten partner to bring frontier safety to open models | https://www.goodfire.com/blog/goodfire-baseten-partnership | goodfire
- goodfire-com-research-public-neuron-atlas | Neuron Atlas - Qwen3.6 | https://www.goodfire.com/research/public_neuron_atlas | goodfire

## Sources finished

- None yet. Source list: (1) surveys/agendas — covered by core, (2) transformer-circuits posts, (3) Goodfire research,
  (4) other labs, (5) topic searches.

## Done
- alignment-anthropic-com-2025-believe-it-or-not | Believe It or Not: belief depth = generality + robustness + representation (Anthropic Fellows)
- anthropic-com-research-introspection | Signs of Introspection in LLMs (concept injection; Anthropic)
- arxiv-2605.25459 | From Simulation to Enaction: Post-trained LMs Recognize their Own Generations (IAS Princeton / Anthropic)
- arxiv-2608.30980 | Evaluating and Improving LLM Self-Modeling (UIUC / Constellation / Anthropic)
- arxiv-2607.12279 | A Shared Subcircuit Lets LLMs Count Down Across Tasks (Yale / Anthropic)
- arxiv-2607.03502 | Reading Between the Dots (filler-token hidden computation)

- arxiv-2506.20790 | Stochastic Parameter Decomposition (Goodfire)
- arxiv-2511.05408 | Steering Language Models with Weight Arithmetic (Anthropic)
- alignment-anthropic-2025-selective-gradient-masking | Beyond Data Filtering (Anthropic)
- arxiv-2606.02609 | Building Better Activation Oracles (MATS / Nanda)
- arxiv-2603.05494 | Censored LLMs as a Natural Testbed (Harvard et al.)
- arxiv-2510.01070 | Eliciting Secret Knowledge from Language Models (Cywiński et al.)
- anthropic-com-research-assistant-axis | The Assistant Axis (Anthropic)
- arxiv-2606.17056 | The Value Axis (Anthropic fellows / Stanford)
- arxiv-2512.01222 | Unsupervised Decoding of Encoded Reasoning (Goodfire/Anthropic)
- anthropic-com-research-global-workspace | A Global Workspace in Language Models (J-space) (Anthropic)
- transformer-circuits-pub-2026-headvis-index-html | HeadVis (Anthropic / tcpub)
- arxiv-2604.21139 | Slot Machines: multiple entities (Anthropic Fellows)
- arxiv-2604.12493 | Latent Planning Emerges with Scale (Anthropic Fellows / UvA)
- arxiv-2604.14865 | Segment-Level Coherence for Robust Harmful Intent Probing (UCL / Virginia Tech / Anthropic)
- arxiv-2510.20487 | Steering Evaluation-Aware LMs to Act Like They Are Deployed (MATS; Hua, Qin, Marks, Nanda)

## Patterns noticed

- **Mean-difference direction between a behaviour and a broad contrast set**, validated by checking it is the leading PCA component, is the standard construction for behavioural axes (Assistant Axis; refusal direction; weight steering). (anthropic-com-research-assistant-axis, arxiv-2511.05408)
- Axis position as a *predictor of future behaviour* (compliance after persona drift; emergence of misalignment) — the closest thing in the field to prediction under intervention from a single number. (anthropic-com-research-assistant-axis)
- Ceiling/capping at the empirically normal activation range, rather than constant steering, preserves capability while changing behaviour. (anthropic-com-research-assistant-axis)
- **Base-model control readout** is the standard null for any elicitation claim: same readout from the untuned model must show no benefit. (arxiv-2510.01070)
- Auditor/guess-the-secret grading, with an I/O-only baseline, is now the default evaluation shape for hidden-knowledge work. (arxiv-2510.01070, arxiv-2603.05494)
- Tokens (logit lens / embedding-nearest) beat SAE prose descriptions when the auditor needs a discrete answer. (arxiv-2510.01070)
- Caveat to remember: readouts can be empty because the info was never computed on that pass (refusals short-circuit). (arxiv-2510.01070)
- Repeated claim: the model carries a **representation of the truth independent of what it outputs** (probes trained on unrelated honesty data transfer to censorship). Ground truth for this = "knows X, says not-X". (arxiv-2603.05494)
- Abliteration / mean-difference refusal-or-behaviour direction removal at 50-75% depth is the standard cheap white-box intervention baseline across safety papers. (arxiv-2603.05494, arxiv-2511.05408)
- **Text-inversion control**: any benchmark for "model explains itself from internals" must ensure the answer is not derivable from the visible context. (arxiv-2606.02609)
- Prose explanations get judged on separate hallucination vs vagueness axes with chance-adjusted scores; end-to-end readers are still weaker than a linear probe on narrow tasks. (arxiv-2606.02609)
- Activations are most informative around 60-70% depth and on-policy data is the preferred training/test distribution. (arxiv-2606.02609)
- Loss frontiers (retain vs forget, behaviour vs capability) rather than single-point accuracy as the headline result shape; both sides evaluated at matched values of the other. (alignment-anthropic-2025-selective-gradient-masking, arxiv-2511.05408)
- Removal/ablation must be tested by *recovery cost* (how much retraining restores the capability), because loss can hide suppression rather than removal. (alignment-anthropic-2025-selective-gradient-masking)
- Ground-truth toy models as the testing ground for decomposition methods: both SPD and attributions-of-decomposition papers build toy models with known mechanisms and score recovery (MMCS/L2 ratio). (arxiv-2506.20790)
- Shrinkage is the recurring failure mode of learned decompositions, in activations and in weights; need an explicit magnitude metric alongside cosine similarity. (arxiv-2506.20790)
- "Contrastive subtraction" is the field's default way to isolate a behaviour: D+ vs D- fine-tunes (weights), persona pairs (activations). Shared nuisance factors cancel. (arxiv-2511.05408)
- Behaviour metric x capability metric, both evaluated OOD, with a magnitude dial (k) and OOD-generalisation as the headline comparison. (arxiv-2511.05408)
- Weight-space directions are emerging as monitors (cosine similarity of a fine-tune update to a reference direction), separate from and cheaper than activation probes. (arxiv-2511.05408)
- **Difference-in-means axis built from synthetic feedback data, validated four ways** (held-out AUROC, cross-layer cosine, logit lens, causal steering) is the current gold-standard recipe for claiming a direction means something. (arxiv-2606.17056, anthropic-com-research-assistant-axis)
- A single linear macro-variable ("am I on track", "am I drifting from persona") projects on the last prompt token and works as an input-free monitor; post-training silently re-writes it, so monitors drift. (arxiv-2606.17056, anthropic-com-research-assistant-axis)
- Logit lens / unembedded-token readout remains a strong cheap baseline, and its accuracy is layer-dependent with a peak in mid-to-late layers (a "semantic hub"); always sweep layers. (arxiv-2512.01222, arxiv-2606.17056)
- Model organisms are built by *re-encoding existing outputs* and fine-tuning — fast, but it makes the test easier than the real phenomenon; state the confound. (arxiv-2512.01222, arxiv-2603.05494)
- **Swap intervention** (replace direction A with equal-norm direction B) is a stronger causal test than ablation: it shows the downstream computation *reads from* the location, not merely that removing it hurts. (anthropic-com-research-global-workspace)
- A small broadcast channel (few dozen concepts, <10% of activity) plus a large automatic periphery as the two-mode structure of network computation; routine behaviour survives deletion, composition/reasoning does not. (anthropic-com-research-global-workspace)
- Jacobian-of-future-logits lens (J-lens) generalises logit lens from "next token" to "any word it might say later" and finds reportable contents. (anthropic-com-research-global-workspace, arxiv-2512.01222)
- Eval-awareness is a confound in *every* safety eval: ablating "fake/fictional" style patterns changed measured behaviour, i.e. good behaviour was partly conditional on knowing it was tested. (anthropic-com-research-global-workspace, arxiv-2606.17056)
- Heads are the wrong unit: heads are polysemantic *without* superposition because their output is high-rank, and some behaviours are high-rank; the target unit is a sparse, high-rank "attentional feature". (transformer-circuits-pub-2026-headvis-index-html)
- Per-example attributions do not give a rule: a year-range bound (1000-1986) was only found by sweeping controlled inputs. Always test on generated minimal pairs, not dataset examples. (transformer-circuits-pub-2026-headvis-index-html)
- QK/OV feature-pair attribution + virtual weights are the standard way to read a head's circuit once you have a feature dictionary (here a 10M WCC). (transformer-circuits-pub-2026-headvis-index-html, arxiv-2506.20790)
- **Decodable but unused** is a real and common phenomenon: a probe reads prior-entity traits on later tokens, but patching those tokens changes nothing. Use probe + patch together, always. (arxiv-2604.21139)
- Several representations of the *same* information at different token roles ("slots") are orthogonal; multi-slot MoE probes are the tool to find them. (arxiv-2604.21139)
- Synthetic multi-step relational tasks with prefill + single next token are the standard causal-test harness in Anthropic papers (patching, steering, dual binding). (arxiv-2604.21139, arxiv-2606.17056)
- **Planning needs a two-condition test** (causes the distant output AND causes the licence for it) — decodability of a future token is not planning. (arxiv-2604.12493)
- Ablate-on-success / boost-on-failure with random-feature controls is the standard causal check for "this feature is the mechanism" in feature-circuit papers. (arxiv-2604.12493)
- Planning is piecemeal: whether a model plans depends on task frequency and loss weight, not on a single global planning module. (arxiv-2604.12493)
- Negative result pattern: having the representation does not entail context adaptation (couplets) — same gap as decodable-but-unused in SLOT. (arxiv-2604.12493, arxiv-2604.21139)
- **Last-used layer ≠ peak-probe layer**: patching every layer and reading where the effect *drops to baseline* locates the layer where information is copied out and consumed downstream; probing alone would put you at the wrong site to intervene. (arxiv-2607.12279)
- Cross-condition representation match should be tested for **unimodality plus near-linear unit mapping (r²)**, not just "the probe transfers" — that is what licenses saying two sites encode the same scalar in different units. (arxiv-2607.12279)
- Growing recipe for cross-model universality: claim a motif is shared only after the *geometric structure* (manifold diagonal + ringing pattern) matches a prior report in another model, with interventions in just one. (arxiv-2607.12279, arxiv-2604.12493)
- **Base-rate normalisation for "the model knows its own behaviour"**: score self-reports as improvement over a dummy predictor of the answer distribution, not raw accuracy — 0.95 raw is worthless when the labels are 5% positive. Reports both raw and skill in [−1,1]. (arxiv-2608.30980)
- **No own-model advantage**: a stronger model explaining a weaker one's behaviour can match or beat the model explaining itself, so "self-knowledge" claims must beat a cross-model explainer baseline. Same lesson as the base-model-control null, one level up. (arxiv-2608.30980, arxiv-2510.01070)
- SFT on explanation text collapses outside its training-query support and RL afterwards does not recover it; verified-reward RL on generated intervention labels is the recipe that generalises across task formats. (arxiv-2608.30980)
- **Probe-plus-steer is mandatory, again**: a clean 1-D centroid manifold for output entropy/input surprise is almost non-causal under steering, while the surprise direction alone moves entropy — decodability buys you a coordinate, not a mechanism. (arxiv-2605.25459, arxiv-2604.21139)
- **Self-attribution claims need the cross-model matrix**: to say a model recognises its *own* text, feed every model's text into every model in the same slot and require the diagonal to be the column minimum; otherwise "low perplexity on my own prose" explains it. (arxiv-2605.25459, arxiv-2608.30980)
- Implicit and explicit self-knowledge are mechanistically separate (entropy/surprise route vs an on-demand comparison circuit), so a model's verbal self-report is another behaviour to predict, never ground truth about its internals. (arxiv-2605.25459, arxiv-2608.30980)
- **Planted-state introspection test**: write a known concept vector into the state, then ask the model what it notices; the report is ground truth-checkable only if the model must flag the anomaly *before* naming the concept (otherwise it is just talking about the steer). Rates net of control-trial false positives, on a swept injection strength — introspection is rare (~1 in 5), post-training-dependent, and served by narrow task-specific circuits rather than one faculty. (anthropic-com-research-introspection)
- Retroactive injection ("you were planning this all along") flips apology into endorsement plus a confabulated justification — a reusable probe for whether a self-check reads prior internal state or re-reads the visible transcript. (anthropic-com-research-introspection)
- **Truth-probe claims need an adversarial probe**: a linear true/false probe trained on ordinary statements is fooled by any edit that leaves a representation artefact, so the control is a probe trained partly on the edited statements and required to still recover the ground truth on held-out ones. Same family as base-model-control and cross-model-matrix: every readout gets a null that could plausibly explain its success. (alignment-anthropic-com-2025-believe-it-or-not)
- **Depth ladder for "the model knows / believes X"**: direct question → indirect multi-step use → survival under adversarial pressure → representation matching genuine knowledge. Rank interventions along it instead of reporting one accuracy. (alignment-anthropic-com-2025-believe-it-or-not, arxiv-2604.12493)
- Plausibility is a confound in every editing result: an edit that succeeds because it fits the model's priors is not evidence that the mechanism of belief was touched — matched implausible edits are the control. (alignment-anthropic-com-2025-believe-it-or-not, arxiv-2604.12493)
- **Evaluate monitors at a fixed low false-positive rate**, reporting TPR@1%FPR and log-scale AUROC as the headline and plain AUROC as the secondary: a probe at 97% AUROC can still be unusable at deployment precision, and the log-axis metric is what surfaces the difference. (arxiv-2604.14865)
- **Pooling rule is a first-class design choice, not a detail**: confidence-weighted or max-like aggregation over tokens turns a "harmfulness probe" into a keyword detector. Requiring several windows to jointly support a verdict (top-K averaging) plus penalising disagreement between selected windows was worth ~35% TPR at 1% FPR — bigger than most modelling changes. (arxiv-2604.14865)
- **Residual-only probing leaves accuracy on the table**: attention-output and MLP-output probes beat the residual stream in every domain tested, and which one wins depends on domain *and* architecture. Always sweep the representation site alongside the layer. (arxiv-2604.14865, arxiv-2606.02609)
- **Frozen-reader / shifted-backbone control** cleanly separates "the model cannot represent it" from "our reader cannot read it": probes at chance on ciphered text with the backbone frozen, then 98.85% AUROC with the *same* probes once the backbone is cipher-tuned. Reusable design for any claim that a readout tracks content rather than surface form. (arxiv-2604.14865)
- **Pre-registered ground truth as the validation for an intervention**: build a model organism whose evaluation-vs-deployment behaviour you *defined*, then a steering success claim ("we elicited deployment behaviour") becomes checkable instead of inferred from a transcript heuristic. Same move as the base-model control and the cross-model matrix, but applied to a steering intervention rather than a probe. (arxiv-2510.20487)
- **Extract the direction on the pre-intervention checkpoint** to certify the vector carries the context variable and not the downstream behaviour it is meant to control; conversely, steering toward the "target" state can undershoot the natural baseline (steered deployment rate < plain deployment rate), which is itself a sign the vector is a coarse axis. (arxiv-2510.20487, arxiv-2606.17056)
- **Spread a fixed steering budget over several mid layers (10–30 here) rather than one strong vector**: equal behaviour change at much lower task-accuracy cost; single-layer steering at comparable total strength degrades capability sharply. (arxiv-2510.20487, anthropic-com-research-assistant-axis)

## Could not read

- None yet.