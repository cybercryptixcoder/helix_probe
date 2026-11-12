# Gemma Scope: Open Sparse Autoencoders Everywhere All At Once on Gemma 2

- **Key:** arxiv-2408.05147
- **Authors / organisation:** Tom Lieberum, Senthooran Rajamanoharan, Arthur Conmy, Lewis Smith, Nicolas Sonnerat, Vikrant Varma, János Kramár, Anca Dragan, Rohin Shah, Neel Nanda; Google DeepMind
- **Date:** 2024-08
- **Link:** https://arxiv.org/abs/2408.05147
- **Kind:** tool
- **Read from:** abstract and sections (main text read; later appendices only partly)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Training SAEs on a modern LLM is expensive enough that most academic groups cannot do it, which bottlenecks
interpretability research. DeepMind trained and released an open, comprehensive set of SAEs on every layer and
sublayer of Gemma 2 so others can study features, circuits and applications without paying the training cost. The
goal is infrastructure for safety and interpretability research at scale.

## What they studied
Gemma 2 2B base (26 layers), 9B base (42 layers), selected layers of 27B base, and some SAEs on the
instruction-tuned 9B for comparison. Sites: attention output (concatenated heads before W_O), MLP output, and
post-MLP residual stream at every layer. Also a set of transcoders on Gemma 2 2B MLPs.

## How they did it
They used JumpReLU SAEs: each latent has a learned threshold, below which it is zeroed, trained with reconstruction
error plus an L0 penalty, using straight-through estimators to get gradients for the thresholds. Activations were
normalised during training and the scale folded back in afterwards. Widths range from 16.4K to 1M latents, with
several sparsity levels per site, trained on 4B to 16B tokens of Gemma-1-style pretraining data; over 400 SAEs in
the main release (over 2,000 counting variants), more than 30 million latents, using over 20% of GPT-3's training
compute and about 20 PiB of stored activations. A width ladder from 16.4K to 524K at matched sparsity was trained to
study feature splitting. They evaluated each SAE on L0 vs fidelity, broke loss down by token position and by Pile
subset, tested transfer of base-model SAEs to the chat model, and checked bfloat16 inference.

## What counts as an explanation here
A feature dictionary for every site of a model, meant as raw material for later explanations (circuits, steering,
auditing). No behaviour is explained in the paper itself.

## How they judged success
Mean L0 (sparsity); delta LM loss (increase in next-token cross-entropy when the SAE output replaces the activation)
as the main fidelity metric; fraction of variance unexplained (FVU) as a secondary one. Interpretability numbers are
borrowed from earlier work (human raters and LM-based explanation scores comparing JumpReLU, TopK, Gated).

## What they found
Residual-stream SAEs have higher delta loss than MLP or attention SAEs at similar FVU, suggesting small residual
errors hurt the model more than errors in one sublayer. Wider SAEs improve fidelity at fixed sparsity but often by
splitting existing features rather than finding new ones; a cluster of very-high-frequency latents persists (also
in TopK, not in Gated). Prior human and LM ratings show little interpretability difference among JumpReLU, TopK and
Gated. Base-model SAEs reconstruct chat-model activations almost as well as chat-trained SAEs by delta loss, less so
by FVU. Fidelity is best on maths text and worst on multilingual Europarl. bfloat16 inference costs almost nothing.

## Limitations and open problems they name
No agreed metric for SAE or latent quality; delta loss is noisy; SAEs miss features wider SAEs find; mostly English
data. They list open problems: whether SAEs find "true" concepts, dark-matter (non-linear) features, cross-layer
superposition, circular features, how superposed circuits sit in weights, weight-based circuits via transcoders,
and comparing SAE steering with simpler steering vectors.

## What we take from it
A ready-made substrate: if we need a feature basis on a mid-size open model, Gemma Scope saves training. Delta LM
loss vs FVU disagreeing is a direct warning that reconstruction metrics and behavioural metrics diverge, so our
white-box model must be judged on output behaviour. Their open problem of reading circuits from weights via
transcoders is exactly our direction, and they flag it as unsolved.

## Tags
unit: feature | layer
form: dictionary
method: SAE | transcoder
eval: faithfulness | benchmark
goal: understanding | science
