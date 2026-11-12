# Negative Results for SAEs On Downstream Tasks and Deprioritising SAE Research (GDM Mech Interp Team Progress Update #2)

- **Key:** alignmentforum-4uxcajnupktkbsi28-negative-results-saes-downstream
- **Authors / organisation:** Lewis Smith, Senthooran Rajamanoharan, Arthur Conmy, Callum McDougall, Tom Lieberum, János Kramár, Rohin Shah, Neel Nanda; Google DeepMind mechanistic interpretability team
- **Date:** 2025-03-26
- **Link:** https://www.alignmentforum.org/posts/4uXCAJNuPKtKBsi28
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
SAEs have no ground truth, so the team wanted a concrete test of their usefulness: if SAEs will eventually serve ambitious interpretability goals, they should already help on something practical. They chose out-of-distribution detection of harmful user intent, a safety-relevant probing task, and compared SAE-based probes with well-tuned dense linear probes. The post doubles as a strategy update: the outcome led the team to deprioritise fundamental SAE research. It is an informal collection of snippets rather than a formal paper.

## What they studied
Gemma-2-9B-IT, residual stream at layer 20. Gemma Scope SAEs, plus versions finetuned on chat data and chat SAEs trained from scratch. Unit: SAE latents versus dense residual directions.

## How they did it
1. Built a harmful-intent dataset: HarmBench harmful vs Alpaca harmless prompts in distribution; OOD sets from an over-refusal benchmark, an internal chat set and AdvBench. Labels stay "harmful" even when a jailbreak suppresses refusal.
2. Augmented with jailbreak wrappers and benign transformations, splitting wrapper types between train and OOD test (e.g. training on AIM/roleplay/GCG, testing on others), giving 4,046 train, 1,014 validation and 3,850 OOD examples.
3. Compared dense linear probes, 1-sparse and k-sparse probes on SAE latents (k from 2 to 50), and linear probes on SAE reconstructions; aggregation by max over the sequence.
4. Tried to close the gap by finetuning SAEs on chat data, training chat SAEs from scratch, latent resampling and adding refusal prompts to SAE training data.
5. Side studies: using SAEs to debug the dataset, and the problem of high-frequency latents.

## What counts as an explanation here
Implicitly, a good dictionary should contain the concept a downstream task needs as one or a few latents; a sparse probe on those latents is then both an explanation and a classifier. The finding is that the needed concept is not cleanly present.

## How they judged success
AUROC on train, validation and OOD sets; "performance delta" between probes on the true residual and probes on the SAE reconstruction (measures task information lost by the SAE); statistical comparison across SAE training variants.

## What they found
- Dense linear probe: AUROC 1.0 train and validation, about 0.999 OOD.
- 1-sparse SAE probes could not even fit training data; k-sparse probes fit at about k=20 but transferred OOD worse than dense probes, the opposite of the team's prior.
- Chat finetuning closed about half the gap; other variants made no statistically significant difference.
- Probes on reconstructions lost information, most visibly OOD (delta about 0.048 for Gemma Scope, 0.039 for the finetuned SAE).
- SAEs were useful for debugging data: a question-mark latent revealed that only the benign set contained questions.
- High-frequency latents (firing on over 10% of tokens) in JumpReLU/TopK SAEs are often uninterpretable; a quadratic frequency penalty removes many at modest reconstruction cost. They recommend frequency-weighted autointerp scores.

## Limits and open problems they name
One task and one model family; possibly noisy setup; hard to tell fundamental SAE limits from fixable ones; some of the "SAE win" depends on manual data cleaning. Possible reasons for failure: the target concept may not decompose into a few atomic latents; SAEs may be incomplete, absorb features, or encode spurious correlations as readily as signal. Recommended next steps: study fundamental limits rather than hill-climb sparsity/reconstruction, Matryoshka SAEs, cheaper training, other dictionary/clustering methods; the team pivots toward model diffing, model organisms of deception and thinking models.

## What we take from it
- **Warning:** an unsupervised decomposition can lose exactly the information a prediction needs, especially OOD; reconstruction quality does not guarantee task-relevant completeness.
- **Measure:** the "probe on reconstruction minus probe on original" delta is a cheap test of whether a surrogate representation preserves task-relevant information; directly reusable to test a white-box reconstruction.
- **Framing:** demand a practical win against a dense linear baseline before claiming a representation is the "right" one.
- **Shortcut:** decompositions are still good for hypothesis generation and dataset debugging.

## Tags
unit: feature | direction
form: dictionary | probe
method: SAE | probing
eval: downstream-task
goal: evaluation-of-methods | safety/auditing
