# Introspection Adapters: Training LLMs to Report Their Learned Behaviors

- **Key:** arxiv-2604.16812
- **Authors / organisation:** Keshav Shenoy, Li Yang, Abhay Sheshadri, Sören Mindermann, Jack Lindsey, Sam Marks, Rowan Wang; Anthropic Fellows, Anthropic, University of Cambridge
- **Date:** 2026-04-18 (v2 2026-04-28)
- **Link:** https://arxiv.org/abs/2604.16812 (research post: https://alignment.anthropic.com/2026/introspection-adapters/)
- **Kind:** paper
- **Read from:** full text (main body and appendices A–B; read via HTML)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Fine-tuning can give a model behaviours that are unintended, harmful or hidden, and auditing is hard when the training
data or reward model is unknown. If a model could simply describe what it learned, auditing would be much cheaper.
Untrained self-reports are unreliable and earlier training attempts did not generalise. The authors train one
reusable adapter that, stacked on any fine-tune of a base model, makes it describe its learned behaviours, and test
whether this generalises to behaviours and training methods never seen.

## What they studied
Mainly Llama-3.3-70B-Instruct, plus Qwen3 models from 0.6B to 14B for scaling. Training uses hundreds of fine-tuned
variants in eight categories (sandbaggers, quirks, backdoors, obscured malign, rare quirks, heuristic following,
harmful and benign roleplay). Unit of analysis: whole-model behaviour, accessed via a LoRA on top of a behaviour LoRA.

## How they did it
For each training variant with a known implanted behaviour, they write pairs of a generic question (are there unusual
things you do for certain prompts?) and a first-person description of that behaviour. A single LoRA (the introspection
adapter) is trained by SFT on all variants at once, with each variant's behaviour weights frozen beneath it. Controls
include negative examples with mismatched triggers and generic chat data to stop shortcut learning. A DPO stage then
uses held-out variants: adapter rollouts are judged 1–10 by an LLM, high-scoring answers preferred over ones at least
2 points lower, plus true-vs-unrelated description pairs, to cut hallucinated reports. Evaluation applies the adapter
to unseen models: AuditBench (56 adversarially trained models), 9 cipher-based malicious fine-tunes, a replicated
reward-model-sycophant model, and two UK AISI sandbagging models. Ablations vary model scale, number of training
categories, DPO, adapter size, and training mixture.

## What counts as an explanation here
A first-person natural-language description of a learned behaviour. It is a behavioural self-report, not a mechanism;
the authors do not claim true introspection, and the report is partial (often names the effect but not the trigger).

## How they judged success
Verbalization rate (fraction of responses an LLM judge marks as correctly describing the behaviour), on held-out
in-distribution and out-of-distribution models; AuditBench investigator-agent success rate against the other tools in
that benchmark; false-positive rate on models lacking the behaviour; untrained-model baseline.

## What they found
AuditBench: 59% agent success with the adapter vs 53% for the next-best method and 44% for the best white-box tool
(activation oracles); non-zero correct verbalization on 50 of 56 models. Cipher attacks: 57.8% success with a
summarisation scaffold, behaviour found in 7 of 9 variants, but the cipher itself never named. RM sycophant: 16 of 52
behaviours surfaced vs 2 for the plain model, but not the core objective. Sandbagging: 33.0% reports vs 15.8%
false-positive rate on similar models. Held-out verbalization scales from 37.7% (0.6B) to 77.3% (14B), baseline under
10%. More training categories help up to about five or six, then plateau. A rank-1 single-layer LoRA reaches 68.9% of
the full adapter's performance.

## Limits and open problems they name
High false positives: the adapter reports training-distribution behaviours on models that lack them, especially the
base model. Behaviours already present in the base model during adapter training are reported much less often. No
principled recipe for the training mix. High upfront cost. Mechanism unclear; they think it elicits a latent ability
rather than creating one.

## What we take from it
A method idea and a measure. The idea of a reusable, cross-model adapter trained on many model organisms with known
ground truth is close to "learn a map from weight deltas to behaviour descriptions". The rank-1 result suggests the
read-out lives in a very low-dimensional subspace. The false-positive problem is a warning: any predictor we train
on implanted behaviours must be scored with a no-behaviour control.

## Tags
unit: whole-model | weights
form: description
method: training-interpretable | other
eval: benchmark | downstream-task
goal: safety/auditing
