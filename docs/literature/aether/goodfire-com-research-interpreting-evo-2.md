# Interpreting Evo 2: Arc Institute's Next-Generation Genomic Foundation Model

- **Key:** goodfire-com-research-interpreting-evo-2
- **Authors / organisation:** Liv Gorton, Nicholas Wang, Nam Nguyen, Myra Deng, Eric Ho, Daniel Balsam, Thomas McGrath (all Goodfire), in collaboration with Arc Institute
- **Date:** 2025-02-20
- **Link:** https://www.goodfire.com/research/interpreting-evo-2
- **Kind:** blog/research post
- **Read from:** full text (post incl. footnotes; the Evo 2 preprint and its mechanistic-interpretability sections 2.4 / 4.4 were **not** fetched)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Authors of interpretability tooling partnered with Arc Institute to interpret a genomic foundation model, on the premise that biological foundation models are a harder and more interesting case than text models: nobody — including domain experts — can read the input directly, and the model's job spans several stacked representations (raw nucleotides, then proteins, then RNA folds). The larger goal is two-fold: recover hidden biological knowledge the model has absorbed, and give biologists a way to *direct the model* by editing internal features. The second point is stated sharply and is why the post matters to us: a model that "only speaks nucleotide" cannot simply be prompted toward a desired output, so steering-by-feature would be an enabling capability rather than a convenience.

## What they studied
Evo 2, Arc's next-generation genomic model, in its 7B and 40B parameter sizes, which take sequences up to one million base pairs as input at single-nucleotide resolution and were trained across all domains of life. The 7B model has 32 layers and mixes attention blocks with StripedHyena blocks. Unit of analysis: sparse-autoencoder features on a single intermediate layer, layer 26 (a StripedHyena layer), read against genomic annotation tracks.

## How they did it
BatchTopK SAEs were trained on layer 26 activations, with training data balanced evenly between eukaryotic and prokaryotic genomes and restricted to high-quality reference genomes — the authors note that SAEs need far less data than the model itself, so curated data was affordable. They first trained standard ReLU SAEs and switched once they observed no high-frequency dead/low-utility features during training; BatchTopK keeps variable capacity per token while retaining the loss and hyperparameter behaviour of TopK. SAEs were trained on several layers including both block types, and layer 26 was chosen after a first-pass inspection showed the most biologically interesting features; the authors offer a plausible reason for a late layer being best here — a nucleotide vocabulary is tiny compared with text vocabularies, so fewer layers may be needed to select and calibrate the next token once the relevant pattern has been computed. Feature relevance was then checked by a large-scale alignment of features against canonical biological annotations, scored with a domain-F1 measure between feature and concept. They built an interactive visualiser that plots feature activations along bacterial reference genomes beside existing annotation tracks, and overlaid E. coli feature activations on an AlphaFold3 structure prediction of the same protein–RNA complex. Finally, preliminary steering experiments tried to push the model toward new protein structures.

## What counts as an explanation here
A feature dictionary (an SAE trained on one layer, with individual latents shown to track named biological concepts), plus a visualiser that renders each feature as an activation track over a genome so a biologist can compare it with their own annotations. The unit of explanation is a single sparse latent and the test of it is conceptual alignment, not a circuit and not a replacement model. Nothing here claims completeness; the post describes the work as an early-stage collaboration and says a fuller methodological study is forthcoming.

## How they judged success
Mostly qualitative and alignment-based: a domain-F1 score between SAE features and canonical biological concepts across a large set of annotation–feature pairs, plus visual comparison of activation tracks against known annotations and against an AlphaFold3 structure prediction. SAE quality was judged by training loss relative to the ReLU baseline and by whether features looked "crisp" on inspection. No baselines are compared for the alignment metric, no ablations are reported in the post, and the steering experiments are described as early signs rather than measured results.

## What they found
Features on the late layer matched biological objects across a wide range of scales. The post names coding sequences, exon–intron boundaries, protein secondary structure, tRNA and rRNA, and viral-derived elements (prophage, CRISPR), and reports that in a well-annotated E. coli region containing a tRNA array and the tufB gene, separate α-helix, β-sheet and tRNA features light up in the places the annotations predict. The authors read the coincidence between a DNA-level feature and a protein-structure element as evidence that the model connects a nucleotide sequence to the downstream RNA and protein it produces. Steering is reported as showing "early signs of life" toward new protein structures, with the explicit caveat that steering is considerably more complex here than for language models. The post carries no headline numbers of its own.

## Limits and open problems they name
Steering is the stated open problem: it is harder than in language models and the post declines to claim it works. The authors also flag that this is an overview — detailed methods live in the preprint's interpretability sections which they had not yet published as a standalone study. Sampling only layer 26, and choosing it after an informal inspection, is a selection the post does not defend beyond its own plausibility argument about vocabulary size.

## What we take from it
Two things, one general and one pointed. The general one: a single-layer SAE plus a *render-the-feature-over-the-input* visualiser is enough to produce a credible claim of concept alignment in a domain where nobody can read the input, and the domain-F1-style scoring against an independent annotation track is a cheap, transferable way to turn "the feature looks meaningful" into a number — a domain-adapted version of the "validate a direction four ways" recipe we keep collecting. The pointed one: the failure mode they name in passing is the missing-prompt channel. Their model cannot be instructed, so all of the behaviour control must come from the internal representation; once we have a model we *can* prompt, that absence disappears and feature steering becomes strictly an addition rather than the only lever. Also worth copying: their reason for a late best layer (small vocabulary ⇒ less serial computation needed to commit a token) is a checkable prediction of the "read the layer where information is copied out" pattern, and it suggests we report vocabulary-size-dependent layer profiles rather than assuming text-model layer conventions transfer.

## Tags
unit: feature
form: dictionary
method: SAE
eval: benchmark
goal: science
