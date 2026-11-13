# Beyond Data Filtering: Knowledge Localization for Capability Removal in LLMs

- **Key:** alignment-anthropic-2025-selective-gradient-masking
- **Authors / organisation:** Igor Shilov, Alex Cloud, Aryo Pradipta Gema, Jacob Goldman-Wetzler, Nina Panickssery, Henry Sleight, Erik Jones, Cem Anil; Anthropic (with Anthropic Fellows Program, Imperial College London, University of Edinburgh, Constellation)
- **Date:** 2025-12-08
- **Link:** https://alignment.anthropic.com/2025/selective-gradient-masking
- **Kind:** blog/research post
- **Read from:** full text (blog post; links to paper, code)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Post-training refusals can be circumvented, so the more robust safety move is to stop a model holding dangerous (e.g. CBRN) knowledge in the first place. Data filtering is the standard answer but its labels are noisy, harmful content is embedded in mostly-benign documents, and dual-use content cannot be cleanly separated, so filtering forces a bad trade-off between false negatives and collateral loss of legitimate knowledge. Gradient Routing had already proposed localising target knowledge into dedicated parameters during training so they can be deleted afterwards. This post improves that recipe, measures the recovery cost after deletion, and asks *why* localisation happens at all — which is where it becomes interesting for interpretability rather than only for safety.

## What they studied
A 254M-parameter dense transformer trained on English Wikipedia, with Wikipedia's article-level content classification as labels (biology = 3.7% of tokens = forget class). A separate controlled setup trained on bilingual TinyStories with English as retain and Spanish as forget, plus scaling runs from 8M to 64M parameters. Unit of analysis: designated attention heads and MLP neurons per transformer block, split into a "forget" set and a "retain" set.

## How they did it
Before training, a fixed subset of heads and MLP neurons in each block is designated removable. During training, when an example is labelled dangerous, the gradients are masked so that only the forget parameters move; the rest are frozen for that step. Unlabelled data updates all parameters. After training the forget parameters are zeroed out permanently. Comparisons: weak filtering (drop biology articles only) and strict filtering (also drop medicine, chemistry, environment), each traded off against retain loss on general data. Forgetting is measured as loss on held-out biology text and retention as loss on other Wikipedia text, plotted as a retain/forget frontier. Recovery is measured by adversarially fine-tuning the ablated model on a 50/50 mixture of biology and general data until baseline biology performance returns, against RMU unlearning and the filtering baselines. The mechanism study measures per-parameter gradient norms on unlabelled data (with masking switched off) to see which parameters different domains naturally move.

## What counts as an explanation here
A *structural* localisation claim rather than a description: dangerous knowledge lives in a designated parameter subset, and this can be demonstrated by gradient-flow evidence (forget-domain inputs produce larger gradient norms in forget parameters than retain ones). There is no feature dictionary or circuit; the explanation is "which parameters, and by what mechanism they came to hold the knowledge", and it is causal in the sense that zeroing them removes the capability.

## How they judged success
Retain/forget loss frontier versus both filtering baselines at matched retain loss; number of fine-tuning steps and tokens needed for adversarial recovery to baseline, compared to RMU and to perfect filtering; compute overhead at matched retain loss; gradient-norm contrast between forget and retain parameters per data type; leakage of forget information into retain parameters as a function of model scale.

## What they found
SGTM's retain/forget frontier dominates both filtering baselines: for any given retain loss it removes more biology knowledge than weak filtering and keeps more adjacent-field knowledge than strict filtering, because content inside non-biology articles also gets captured. There is a roughly 5% compute penalty to match standard training's retain loss. Recovery: RMU recovered baseline biology performance in about 50 fine-tuning steps (~13M tokens), SGTM needed about 350 steps (~92M tokens), around 7x more, matching strict filtering and suggesting real removal rather than suppression. Mechanism: once labelled forget examples have built specialised pathways, unlabelled forget-domain examples also route through them and update mainly forget parameters — an "absorption" effect that explains robustness to label noise — and the fraction of forget information leaking into retain parameters shrinks as models grow from 8M to 64M.

## Limits and open problems they name
Small models only (up to 254M), so scaling is unknown; removal is measured with loss, not capability benchmarks such as WMDP; dense transformers only, with mixture-of-experts untested; in-context attack (putting the dangerous knowledge in the prompt) is not addressed, and SGTM should be layered with input filtering and output monitoring; the paper only sketches the "dual model" payoff of keeping both versions from one run.

## What we take from it
Framing: "reading weights" has a constructive counterpart — you can *make* a piece of knowledge localisable by constraining where its gradients go, then verify locality with gradient norms. That is a template for us: ground-truthable localisation experiments where we control where knowledge is written and then test whether a reader can find it. Measure: the recovery-cost curve (fine-tuning tokens to restore) as a functional test of whether knowledge was removed versus hidden, and retain/forget frontiers rather than single-point accuracy, which is the shape our evaluations should report. Warning: loss-based forgetting can be confounded by suppression; any weight-reading claim of "this parameter holds X" should be backed by both a removal test and a recovery test. Opportunity: absorption suggests the network prefers consolidation into whichever pathway it already uses, which is a predictable property a white-box model could exploit.

## Tags
unit: weights | neuron | head
form: other
method: weight-analysis | other
eval: downstream-task | benchmark
goal: control/editing | safety/auditing
