# Explaining 4.2 million genetic variants with state-of-the-art, interpretable predictions (EVEE)

- **Key:** goodfire-com-research-evee-explaining-genetic-variants
- **Authors / organisation:** Michael Pearce*, Thomas Dooms*, Ryo Yamamoto*, Joshua Meehl, Carl Molnar, Mark Bissell, Dron Hazra, Ching Fang, Nam Nguyen, Michael Anderson, Collin Osborne, Patrick Duffy, Bridget Toomey, Eric Klee, Elena Myasoedova, Alexander Ryu, Shant Ayanian, Panos Korfiatis, Matt Redlon, Archa Jain, Daniel Balsam, Nicholas Wang (correspondence); Goodfire and Mayo Clinic (*equal contribution). Post written by Michael Byun and Nicholas Wang.
- **Date:** 2026-04-14
- **Link:** https://www.goodfire.com/research/evee-explaining-genetic-variants
- **Kind:** blog/research post (company post describing a preprint under peer review)
- **Read from:** full text (the whole prose body, the four figure captions, the limitations list and the reference/citation block in one fetch; the four figures themselves were **not** inspected, so every number here is one stated in prose or in a caption's text, never a curve or UMAP shape I read; the bioRxiv preprint itself was not fetched, so methods details come only from this post's summary)
- **Relevance to us:** 2 (useful)

## What they wanted, and why

Clinical genetics is bottlenecked by the "variant of uncertain significance": sequencing finds millions of variants, and a large share of them — including roughly half of the ClinVar entries this post covers — carry no known effect, leaving patients in diagnostic limbo. Computational variant-effect predictors exist but are usually restricted to protein-coding missense changes (so they cannot see regulatory or splicing mechanisms) or, when genome-wide, aggregate dozens of annotation features into a score nobody can decompose. The authors want a predictor that is simultaneously genome-wide, accurate across all variant classes, and *legible*: one that says which biological function a given variant is likely to break. The larger goal they state is a general pattern — interpretability as the translation layer between a foundation model's opaque representations and the concepts a human field already reasons in.

## What they studied

Human genetic variation in DNA. The model whose representations are read is Evo 2, a genomic foundation model trained on sequences across all domains of life, and the post states that Evo 2 had seen no human variation at training time, so everything here rests on representations learned from evolutionary data. Unit of analysis is a *variant relative to its reference sequence*: embeddings of the reference and the variant are compared, and classifiers read both absolute annotations and the *difference* caused by the substitution. Secondary objects: ~40 region-level biological annotations probed per position (splice sites, regulatory elements, structural domains), and a set of held-out prediction tasks over 4.2M ClinVar variants.

## How they did it

Two layers, and it is worth keeping them apart. (1) A **single genome-wide pathogenicity probe**: a light classifier on frozen Evo 2 embeddings of single-nucleotide variants, with the architectural choice highlighted — instead of mean pooling over the sequence's activations they use covariance-based sequence pooling (the second-moment statistic, from the sibling post), which preserves which feature dimensions fire *at the same position*. (2) An **explanation pipeline**: probes are trained on reference-sequence embeddings to predict known annotations; each variant's predicted annotation values are compared against its reference to produce a *disruption profile* (how far each biological function moved); the profile, the pathogenicity score and gene context are then handed to a frontier reasoning model (Claude Sonnet 4.6 is named for the screenshot shown) which writes a natural-language mechanism hypothesis. Evaluation is (i) AUROC on 839k ClinVar SNVs, (ii) zero-shot transfer to short insertions and deletions that were never trained on, (iii) comparison against classical meta-predictors, protein-based models and foundation-model baselines broken out by consequence type and conservation level, (iv) transfer to deep mutational scanning datasets for BRCA1, BRCA2, TP53 and LDLR, and (v) an LLM-as-judge quality score on synthesised explanations against 154 high-confidence (≥3 review star) ClinVar variants, with and without the disruption profile. The output artifact is precomputed scores, profiles and on-demand explanations for all 4.2M ClinVar variants.

## What counts as an explanation here

A layered thing, and only the middle layer is mechanistic. Bottom: one scalar — predicted probability of pathogenicity. Middle: a **disruption profile**, i.e. a structured vector saying *which named biological annotations moved under this variant and by how much*; this is a supervised probe over known concept vocabulary, so by construction it can only explain a variant in terms the field already has. Top: a natural-language paragraph authored by an LLM that stitches profile + metadata + gene context together. So the "interpretation" is a translation into human concept space, explicitly partial, and explicitly a hypothesis — not a circuit, not a feature dictionary over an unsupervised basis. The authors themselves flag the consequence: mechanisms nobody has annotated cannot appear in a disruption profile.

## How they judged success

Overall AUROC on 839k ClinVar SNVs (the headline 0.997); zero-shot AUROC on indels (0.991); head-to-head comparisons against named baselines stratified by consequence type and conservation; DMS transfer on four named genes; and, for the explanation stage, a composite 1–5 LLM-judge score over mechanism coverage, biological accuracy and specificity on 154 high-confidence variants, with variant-metadata-only as the ablation arm. Controls: the zero-shot variant-type split and the held-out-gene DMS transfer are genuine generalisation tests; the explanation ablation isolates the contribution of the disruption profile. Absent: no uncertainty intervals on any number, no shuffled-embedding or random-score control for the probes, no clinician-rated evaluation of the explanations (the judge is a model), and no wet-lab validation — which the post names.

## What they found

Pathogenicity: 0.997 overall AUROC across 839k ClinVar SNVs, and 0.991 on short indels without having been trained on them; the post claims wins over classical meta-predictors, protein-based model approaches and prior foundation-model methods across consequence types and conservation levels, and transfer to DMS data for BRCA1, BRCA2, TP53 and LDLR. Explanations: composite judge score 3.8/5 with the disruption profile against 2.8/5 from variant metadata alone. Deliverable: precomputed predictions and readable hypotheses for all 4.2M ClinVar variants, including about 2M currently classed as uncertain. Framing claim: working at the DNA level rather than downstream of a protein predictor lets them cover non-coding mechanisms without giving up per-task accuracy — the usual upstream-generalises / downstream-performs trade-off is claimed to be broken by having a strong enough foundation model. No per-variant-class numbers appear in the prose beyond the above, and no error bars anywhere.

## Limits and open problems they name

The predictions are hypotheses: experimental validation is called the necessary next step. The annotation probes can only surface *known* mechanisms, so genuinely novel ones fall outside scope; they suggest unsupervised dictionary methods such as sparse autoencoders as the complement that could name unnamed features. The natural-language explanations need expert review and are not clinical conclusions. The work is a preprint under peer review. They also position polygenic (common-disease) effects as future work.

## What we take from it

A **framing**, a **measurement**, and a **warning**. The framing is the cleanest statement in this folder of interpretability-as-translation-layer: the foundation model's representation is never claimed to be understandable on its own, and a *supervised* probe over an existing concept vocabulary is inserted as the interface, with an LLM only verbalising structured probe outputs rather than reading activations. For our white-box goal this is the "explain in the field's own ontology" strategy as opposed to "discover an unsupervised basis", and the post names exactly the asymmetry between them: our explanation can only be as complete as the vocabulary we probe against, and an unsupervised dictionary is the only route to features that have no name yet. The measurement worth reusing is the **profile-diff**: score the annotation probes on the reference sequence, score them on the variant, and treat the vector of differences as the object of explanation — a cheap, per-item, directional quantity rather than a whole-input label. The warning, and it is the one I would attach to any interpretability-for-science claim of ours: the explanation-quality number is an LLM judge scoring mechanism coverage, accuracy and specificity of text, comparing 3.8 against 2.8, with no expert readers and no correlation between explanation quality and any ground truth; it is a measure of how plausible the paragraph sounds to another model. Two habits to carry: report the *zero-shot-broader-variant-class* number next to the in-class number (indels are the analog of our held-out behaviour forms), and keep the "known-vocabulary only" admission in the limitations section of every probe-based explanation we publish.

## Tags

unit: feature
form: probe | dictionary
method: probing | weight-analysis | other
eval: downstream-task | benchmark | human-rating
goal: science | understanding
