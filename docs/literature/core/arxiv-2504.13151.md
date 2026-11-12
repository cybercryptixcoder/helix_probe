# MIB: A Mechanistic Interpretability Benchmark

- **Key:** arxiv-2504.13151
- **Authors / organisation:** Aaron Mueller, Atticus Geiger, Sarah Wiegreffe, Yonatan Belinkov and ~20 others; Boston University, Pr(AI)²R Group, Ai2, Technion, Northeastern, Brown, Stanford, MIT, Cambridge, ETH Zürich, Amsterdam and others
- **Date:** 2025-04 (v2 2025-06, ICML 2025)
- **Link:** https://arxiv.org/abs/2504.13151
- **Kind:** benchmark
- **Read from:** abstract and sections (HTML v2; first half of the page in detail, results and limitations)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Interpretability methods are usually compared with one-off, paper-specific evaluations, so it is hard to tell whether a new method is a real improvement. The authors build a shared benchmark with fixed models, tasks, counterfactual inputs and metrics. The aim is to reward methods that precisely and concisely recover the causal pathways or causal variables a language model uses, and so turn interpretability into a field with comparable, cumulative progress.

## What they studied
Four LMs: GPT-2 Small, Qwen-2.5 0.5B, Gemma-2 2B, Llama-3.1 8B (Gemma and Qwen skipped on Arithmetic because of digit tokenisation). Four tasks: Indirect Object Identification (40k instances), Arithmetic (two-digit add/subtract, ~75k), synthetic colour multiple-choice QA (260), and ARC Easy/Challenge; RAVEL also appears in the causal-variable track. Units: edges and nodes of the computational graph (circuit track) and features of hidden vectors (causal-variable track).

## How they did it
Two tracks. Circuit localisation: a method proposes a subgraph of components/edges for a task; the rest of the model is ablated (counterfactual, mean or optimal ablation) and the circuit's behaviour is compared with the full model at a range of circuit sizes. Candidate methods: random, exact edge activation patching, edge/node attribution patching (EAP/NAP), integrated-gradient variants (EAP-IG, NAP-IG), information flow routes (IFR) and uniform gradient sampling. A ground-truth check uses an InterpBench model whose circuit is known. Causal-variable localisation: a featuriser (none/full vector, PCA, SAEs from GemmaScope/LlamaScope, desiderata-based masking DBM over neurons/PCA/SAE features, or Distributed Alignment Search DAS) maps a hidden vector to features; a subset is aligned with a high-level causal variable (e.g. answer position); interchange interventions swap those features between inputs and check whether the network's output changes as the high-level causal model predicts.

## What counts as an explanation here
Either a sparse subgraph (circuit) that reproduces task behaviour, or a mapping from hidden-state features to variables of a hand-written high-level causal model (a causal abstraction). Both are partial and task-specific. The causal-abstraction form is explicitly predictive: it says what output follows from a counterfactual intervention.

## How they judged success
Faithfulness f = (m(C) − m(∅)) / (m(N) − m(∅)), with m the logit difference between correct and counterfactual answer. CPR (circuit performance ratio): area under the faithfulness-vs-size curve, higher better. CMD (circuit-model distance): area under |1 − f| vs size, lower better (measures matching the model, not exceeding it). AUROC against the InterpBench ground-truth circuit. Interchange intervention accuracy (IIA) for causal variables (MSE on logits for IOI). Random-circuit and full-vector baselines as controls. Curves are approximated by Riemann sums over a few sizes.

## What they found
EAP-IG (input-based integration, counterfactual ablations) is best on average on CPR and CMD; on the InterpBench ground truth EAP-IG with activation-based integration gets AUROC 0.81, EAP with mean ablation 0.78. Counterfactual ablations beat mean and optimal ablation; node-level methods do poorly; exact activation patching wins only on GPT-2 IOI; IFR beats random but trails attribution methods. In the causal-variable track DAS is best across tasks (e.g. ARC-Easy, Gemma-2: 88 average / 94 best-layer IIA). DBM on plain neurons is a strong baseline that often beats PCA and SAE features; SAE features do not beat neurons, and DBM on SAE features is near the bottom. Two-digit addition is hard for every method (near chance on Gemma-2).

## Limits and open problems they name
Only four models and four tasks. Metrics are relative, not absolute. The counterfactual input and the logit-difference metric partly define the "task". Exact patching and optimal ablation are intractable at scale. Some baselines not fully tuned; MCQA uses ~100 examples. Ground-truth circuits exist only for the simple InterpBench model. Node vs edge comparison uses a rough weighted edge count.

## What we take from it
A ready-made evaluation protocol that the field recognises: report faithfulness curves (CPR/CMD) over circuit size, and IIA under interchange interventions, against random and full-vector baselines. IIA is exactly a "prediction under intervention" score, so it is the natural metric for a predictive white-box model. Warning: SAE features were not better than raw neurons for localising causal variables, so a white-box model built on SAE dictionaries is not automatically more faithful; supervised DAS-style alignment sets a strong bar. Counterfactual (not mean) ablation should be our default.

## Tags
unit: circuit, feature, direction
form: graph, causal-abstraction
method: attribution, patching, ablation, SAE, decomposition
eval: faithfulness, patching, benchmark, prediction/simulation
goal: evaluation-of-methods
