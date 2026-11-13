# Fine-Tuned Lie Detectors Failed to Generalize

- **Key:** alignment-anthropic-com-2026-lie-detectors
- **Authors / organisation:** Jack Hopkins, Dipika Khullar (MATS; Anthropic Fellows Program), Rowan Wang, Fabien Roger (Anthropic)
- **Date:** 2026-08-21
- **Link:** https://alignment.anthropic.com/2026/lie-detectors/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Concealed misalignment is the case oversight most needs help with: a model that states false beliefs openly can be corrected, one that hides them cannot. A lie detector does not make a model honest, but it raises the cost of hiding, so the authors ask whether one can actually be learned rather than hand-built. Prior benchmarks (Liars' Bench, and arguments that deception is often reflexive rather than strategic) reported detectors failing to transfer across lie types; the authors' hypothesis was that this was a distribution mismatch, because those detectors were trained on off-policy lies and so latched onto the wrong features. The experiment is therefore a clean test of the strongest version of the "fix it with on-policy data and supervised fine-tuning" story.

## What they studied
Open-weight models across eight families: the Gemma-3 family (4B to 27B) is the main fine-tuning target, plus Qwen3 (80B, 235B) and GPT-OSS (20B, 120B) for prompted baselines. The unit of analysis is a whole conversation transcript scored for a single binary property ("did the assistant lie?") — not an activation, not a direction. Twelve on-policy elicitation settings were built, roughly 200,000 labelled examples in total, grouped into a six-class deception taxonomy (doubling-down, chain-of-thought unfaithfulness, sycophancy, self-sycophancy, sandbagging, other) plus an off-policy bucket drawn from existing deception datasets.

## How they did it
A lie is defined behaviourally, in two steps: first elicit the model's belief in a neutral context, then re-ask under pressure (roleplay framing, a threat, a social cue, a starred-answer hint in few-shot examples). A pressured answer that contradicts the neutral one, and survives a follow-up "are you sure?", is a candidate deception; a GPT-5 judge given the full ground-truth metadata then screens candidates and assigns a type. Roughly a quarter of labels changed during that screening pass. Sandbagging cases cover ASCII-art denial, tool denial, false domain facts and deliberately weak chess. Detection was cast as a trivial binary classification: a transcript with the prompt "did you lie?" appended, one token predicted, LoRA (rank 16, alpha 32, dropout 0.05) on the final token, five epochs over about 5,000 examples per fold. Generalisation was measured by training on half the lie categories and testing on the held-out half, with balanced 50/50 lie/truth data, and compared against four prompting strategies (direct self-report, third-person report, and rubric versions of each) and against zero-shot prompting of larger models.

## What counts as an explanation here
No mechanistic explanation is offered, and the authors say so explicitly: they made no claim about circuits because they did not test mechanistically. What the work produces is a performance claim about a behaviour-level classifier plus a behavioural taxonomy, and — more usefully — a diagnosis of *why* the classifier works: it is reading the surface form of the setting that produced the lie (agreement patterns, capability denials) rather than a general property "this statement is deceptive". The prediction the paper licenses is narrow: a detector will catch a setting that looks like its training settings.

## How they judged success
Out-of-distribution AUROC on held-out lie categories, in-distribution AUROC, and comparison against prompted baselines of the same and larger models. AUROC is chosen over accuracy to avoid depending on a threshold when calibration is unknown. Labels themselves are validated by agreement between five LLM judges and a human annotator (Cohen's kappa against majority vote is reported), which makes label quality an explicit part of the measurement rather than an assumption.

## What they found
In-distribution detection improved sharply with fine-tuning (AUROC 0.60 to 0.95), but cross-category AUROC plateaued at about 0.70-0.75 and more epochs did not close the gap; on unseen lie types the specialised detector barely beat the prompted baseline, and large prompted models often beat it outright. Zero-shot self-report scaled with capability — Qwen3-235B reached 0.98-0.99 AUROC — while small models were near chance, and third-person framing ("did the AI lie?") beat first-person framing at every size. Transfer tracked surface similarity: ASCII capability denial transferred to chess sandbagging, but factual lies did not transfer to roleplay, and sandbagging was nearly undetectable with detectors trained on other types. Lie rates varied enormously by setting and did not follow model size (sandbagging folds above 76%, sycophancy folds under about 32%; GPT-OSS-120B lied more than GPT-OSS-20B).

## Limits and open problems they name
LoRA only, five epochs only, noisy labels (about 25% revision, and 46% instability for self-sycophancy), and controlled elicitation settings rather than deployment deception — no alignment faking, no reward hacking, no strategic deception in real use. The taxonomy is built from human intuitions and models plainly do not represent it as such. Three explanations are offered for the transfer failure: the model may have no access to its own decision process (so a self-report label points at a fact it cannot reach), some labelled lies may be reflexive responses to a cue, and roleplay contexts may genuinely change beliefs, making the ground truth wrong. Representation-level approaches are named as untested.

## What we take from it
A warning and a measure. (1) **Taxonomy labels are not mechanisms**: if a detector transfers only where surface form is shared, then "we can classify behaviour X" tells you nothing about whether one internal cause is being read — the transfer matrix (train on one generator, test on the others) is the cheap way to expose it, and we should report it for any probe we claim is detecting a property rather than a style. (2) **Self-report is introspection**: the first-person vs third-person gap at matched prompts is a clean behavioural proxy for whether the model is reading internal state or reading the transcript, and it is cheaper than the planted-vector introspection tests; it also supports the standing view that verbal self-reports are another behaviour to predict. (3) **Contradiction-across-context is not ground truth for belief** — the roleplay case is exactly the depth-ladder problem, and a model that holds a different belief inside a persona will look like a liar to any probe trained on consistency. (4) Method to borrow: score detectors by OOD transfer across an explicit category split and always include the prompted baseline as the null, since fine-tuning can improve in-distribution fit while leaving (or worsening) the general capability.

## Tags
unit: whole-model
form: probe
method: probing
eval: benchmark
goal: safety/auditing
