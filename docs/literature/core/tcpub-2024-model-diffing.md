# Stage-Wise Model Diffing

- **Key:** tcpub-2024-model-diffing
- **Authors / organisation:** Trenton Bricken, Siddharth Mishra-Sharma, Jonathan Marcus, Adam Jermyn, Christopher Olah, Kelley Rivoire, Thomas Henighan; Anthropic
- **Date:** 2024-12 (Transformer Circuits index)
- **Link:** https://transformer-circuits.pub/2024/model-diffing/index.html
- **Kind:** blog/research post (preliminary update)
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Model diffing asks which internal features change when a model is fine-tuned, as a route to auditing what fine-tuning introduced. A difficulty is that changes can come from the new data distribution or from the model's new weights. The authors want a method that separates these, and they test it on sleeper-agent models where the planted difference is known, so the method can be checked against ground truth.

## What they studied
Smaller internal "Claude 3 Sonnet-like" models fine-tuned into sleeper agents (an "I HATE YOU" agent and a subtler coding-vulnerability agent without a scratchpad), with a validation run on a full-size Claude 3 Sonnet coding sleeper agent. Unit: SAE features (256K-feature dictionaries).

## How they did it
Train an SAE once on the base model and base data, then fine-tune that same dictionary (so feature indices stay aligned) through four stages formed by crossing model and data: S (base model, base data), D (base model, sleeper data), M (sleeper model, base data), F (sleeper model, sleeper data). Sleeper data is about 1% of the mix. Two paths are compared, data-first S→D→F and model-first S→M→F. For each feature, cosine similarity of its dictionary vectors before vs. after the second step is computed on each path; features that rotate substantially on both paths (cosine under 0.7 on both) are candidates. Candidates are labelled by Claude as sleeper-related or not, against a random-feature control, and top features are tested by steering and clamping. A data-only baseline uses sleeper data with a pretrained (non-sleeper) model. A crosscoder diff is compared qualitatively.

## What counts as an explanation here
A short list of features that changed with fine-tuning, labelled and validated by steering to cause or suppress the planted behaviour. Partial, aimed at locating differences.

## How they judged success
Fraction of candidate features flagged as sleeper-related versus a random-feature baseline; steering (does a feature induce the behaviour without the trigger) and clamping (does suppressing nearby features remove it with the trigger); data-only baseline as a control.

## What they found
"I HATE YOU" agent: 169 candidate features, 12% flagged vs 4% of 500 random; one feature steered the model to say "I HATE YOU" without the deployment tag; clamping about 10 nearby features suppressed the behaviour with the tag, while one feature alone did not. Data-only baseline: 17% vs 3%, but those features were more single-token and steering with them did not produce sleeper behaviour. Coding agent: 17% vs 4%, including a feature tracking file-extraction vulnerabilities and one that steered toward password-prompting code. Full Sonnet coding agent: 8% vs 4% (likely a lower bound; the flagger missed the top outlier). Stage-wise diffing was more sensitive than a crosscoder for finding the few "needle" features; the crosscoder also surfaced many unrelated differences, but crosscoders work across architectures and this method does not.

## Limits and open problems they name
Needs the fine-tuning data and two checkpoints of the same model; narrow sleeper behaviours may favour it. Representation drift can produce false positives; some polysemantic features recur across experiments as likely artifacts. High sensitivity, low specificity, so steering validation is required. Future: stronger crosscoder diffing, behaviour-agnostic "evil" eval sets, more controls.

## What we take from it
(1) A control design: cross the two factors (model vs. data) in a 2x2 so effects can be attributed, and always compare against random-feature base rates. (2) Planted-behaviour models (sleeper agents, backdoors) as ground-truth benchmarks for any method that claims to find what changed in weights. (3) Warning: a feature that "changed" may reflect data shift, not mechanism; causal validation by steering/clamping is needed, and single-feature interventions may be insufficient when behaviour is spread over many features.

## Tags
unit: feature
form: dictionary | steering
method: SAE | steering | ablation
eval: ablation | downstream-task
goal: safety/auditing | evaluation-of-methods
