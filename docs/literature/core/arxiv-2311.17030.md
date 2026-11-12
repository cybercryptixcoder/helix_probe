# Is This the Subspace You Are Looking for? An Interpretability Illusion for Subspace Activation Patching

- **Key:** arxiv-2311.17030
- **Authors / organisation:** Aleksandar Makelov, Georg Lange (equal contribution; SERI MATS), Neel Nanda
- **Date:** 2023-11
- **Link:** https://arxiv.org/abs/2311.17030
- **Kind:** paper
- **Read from:** full text (HTML, first ~65% of the page incl. main text; later appendices not read)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Methods like DAS look for a linear subspace whose patching makes the model behave as if a concept changed, and
treat success as evidence the concept is stored there. The authors ask whether that inference is safe. They show
that patching a subspace can change outputs even when the subspace does not carry the concept in the model's
normal operation, and they want to explain the mechanism, show it happens in real models, and say how to guard
against it. The bigger aim is sound standards for intervention-based interpretability claims.

## What they studied
GPT-2 small on indirect object identification (IOI), focusing on the layer-8 MLP and the layer-8 residual stream
at the final token; GPT-2 XL on factual recall with the COUNTERFACT data and ROME rank-1 edits (layers 20–35); a
three-unit linear toy network computing the identity. Unit: one-dimensional subspaces (directions) in MLP hidden
space or the residual stream.

## How they did it
They define the illusion: a patched direction can be the sum of a causally disconnected part (it differs between
prompts but lies in the kernel of the downstream weights, e.g. the MLP down-projection W_out, so it does nothing)
and a dormant part (nearly constant on real inputs but able to move outputs if set to unusual values). Patching
along the sum copies the varying disconnected value into the dormant coordinate, activating a pathway the model
does not use. They train DAS directions for the IOI name-position variable, also take a gradient direction, then
split each direction into its nullspace and rowspace components with respect to the downstream weights and patch
each part separately, alongside full-component patches. They check held-out names and templates, a 100-dimensional
version, a random-weights MLP control, and overfitting with few training names. For factual recall they show any
1-D subspace patch corresponds to an approximately equivalent rank-1 weight edit, and compare with ROME.

## What counts as an explanation here
A claim that a specific linear direction at a specific site mediates a variable. The paper argues such claims need
evidence beyond end-to-end patching effects, e.g. that the effect survives removal of the weight-nullspace part,
and agreement with the surrounding circuit.

## How they judged success
Fractional logit difference decrease (FLDD; how much the patch shrinks the IO-minus-S logit difference) and
interchange accuracy (share of patched examples where the model now predicts S). For factual recall: rewrite
score and variance ratio relative to ROME. Controls: full-component patch, nullspace-only and rowspace-only
patches, random-weight MLPs, held-out data.

## What they found
In the layer-8 MLP, the DAS direction gets FLDD 46.7% and interchange accuracy 4.2%, yet patching the whole MLP
gets -8% and 0%, its nullspace part alone does nothing, and its rowspace part alone gives only 13.5%: the effect
needs both parts, the signature of the illusion. A strong direction is found even with random MLP weights. In the
residual stream (a bottleneck at that position), the DAS direction gets 140.7% FLDD and 74.8% interchange
accuracy, its rowspace part keeps most of that (127.5%, 63.1%), it aligns with the gradient direction (cosine
≈0.78 versus ≈0.03 random), and it matches the known IOI circuit, so it is judged genuine. For facts, rowspace-only
interventions give rewrite scores under 10^-3, implying rank-1 editing can succeed in layers where the fact is not
stored, which explains why ROME edits "work" broadly.

## Limits and open problems they name
No formal ground truth for "mechanistic explanation", so illusions are judged by converging evidence. Only two
settings tested; the claim that the illusion is common in MLPs between communicating components rests on
heuristic arguments. The residual-stream nullspace proxy is approximate. Factual edits not tested on related
facts. DAS overfits with few names.

## What we take from it
A central warning for us, and a weight-based check. An intervention that produces the predicted output is not
proof the model uses that path. Because the illusion is defined through downstream weight kernels, reading the
weights directly (rowspace/nullspace of W_out or of a reading head's query matrix) is how to detect it, which
fits our weight-first approach. Our white-box model should predict behaviour on the model's normal pathways and
be tested with: full-component vs subspace patches, nullspace ablation of found directions, random-weight
controls, held-out data, and preference for bottleneck sites. Also a framing: activation patches and rank-1 weight
edits are near-equivalent, linking intervention evidence to weight structure.

## Tags
unit: direction | weights
form: direction | causal-abstraction
method: patching | weight-analysis
eval: patching | faithfulness
goal: evaluation-of-methods | science
