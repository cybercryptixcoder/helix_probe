# Dissecting Recall of Factual Associations in Auto-Regressive Language Models

- **Key:** arxiv-2304.14767
- **Authors / organisation:** Mor Geva, Jasmijn Bastings, Katja Filippova, Amir Globerson; Google DeepMind / Google Research / Tel Aviv University
- **Date:** 2023-04
- **Link:** https://arxiv.org/abs/2304.14767
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Earlier work (e.g. ROME-style causal tracing) asked where factual knowledge is stored in a transformer. This paper asks a different question: how, at inference time, the model actually gets an attribute out of a subject-relation query such as "Beats Music is owned by" -> "Apple". The authors take an information-flow view, tracking which positions and which sublayers pass what to the final position. The larger aim is a mechanistic account of factual recall that informs knowledge localization and model editing.

## What they studied
GPT-2 XL (48 layers, about 1.5B parameters, sequential attention and MLP) and GPT-J (28 layers, about 6B, parallel attention and MLP). Queries from COUNTERFACT, kept only when the model answers correctly (1,209 for GPT-2, 1,199 for GPT-J). Units: token positions (subject, relation, last), attention (MHSA) and MLP sublayer outputs, individual attention heads and their value-output (W_VO) parameter matrices.

## How they did it
First, attention knockout: for a window of layers (9 for GPT-2, 5 for GPT-J), they block the last position from attending to subject positions, to non-subject (relation) positions, or to itself, and measure the relative drop in the probability of the correct answer. Second, they project the hidden state at the last subject token onto the vocabulary and define an "attributes rate": the share of the top-50 projected tokens that occur in a candidate attribute set built from BM25-retrieved Wikipedia paragraphs about the subject. They compare this across layers, positions and against static token embeddings. Third, they zero MLP or MHSA updates at the last subject position over 10 consecutive layers to see which sublayer builds this enrichment. Fourth, they define an "extraction event": the top token of an MHSA or MLP update at the last position equals the model's final prediction, and count extraction rates, also under knockouts and under patching early-layer representations into later layers. Finally, they project each head's W_VO into embedding space (E^T W_VO E) and check whether subject tokens map to the predicted attribute in the top 10.

## What counts as an explanation here
A three-stage information-flow mechanism stated in words and backed by interventions: (1) early MLPs enrich the last subject token with many attributes of the subject; (2) relation information is moved to the last position; (3) upper attention heads, using the relation as a query, extract the right attribute from the enriched subject representation, often with the subject-to-attribute mapping readable from the head's own weights. It is partial (a typical-case account, not a circuit per fact) but predicts which knockouts will hurt.

## How they judged success
Relative change in answer probability under attention knockout; attributes rate (with baselines: other positions and static embeddings); relative drop in attributes rate under sublayer knockout; extraction rate and number of extracting layers, compared across MHSA vs MLP and under position-specific knockouts; rank of the eventual answer in the subject representation; fraction of extraction events explained by a single head's parameters.

## What they found
Blocking the last position from the subject in middle-upper layers cuts answer probability by up to about 60%; blocking relation positions in earlier layers cuts it by 35-45%, and that effect peaks earlier. The attributes rate at the last subject token climbs to close to 50% in intermediate-upper layers, far above other positions; static embeddings reach at most 19.3 (GPT-2) and 28.6 (GPT-J). Removing early MLP updates lowers the attributes rate by about 88% on average, removing MHSA updates by under 30%. Attention updates carry the answer far more often than MLP updates: extraction rate 68.2% vs 31.3% in GPT-2 and 76.7% vs 41% in GPT-J. In subject representations the eventual answer sits at an average rank of 999.5, so heads actively select it rather than copy a top candidate. In 30.2% (GPT-2) and 39.3% (GPT-J) of extraction events, one head's W_VO maps the subject tokens straight to the attribute; these heads are spread over about 150 heads, mostly in GPT-2 layers 24-45.

## Limits and open problems they name
Vocabulary projection is only an approximation, especially in early layers. Attention knockout cannot fully stop information leaking across positions through earlier layers; they mitigate by knocking out windows of layers. The candidate attribute set is a heuristic built from retrieved text.

## What we take from it
A clear example of an explanation with read-from-weights components: the E^T W_VO E projection lets a head's stored subject-to-attribute mapping be read directly from parameters, which is the kind of weight reading we want to scale. Attention knockout over layer windows and the "extraction event" test are cheap, reusable intervention measures. The framing of recall as enrich-then-extract gives a structural prior for a predictive model: predict output by modelling which attributes are present at the subject and which head queries them. Warning: storage location (MLPs) and extraction site (heads) differ, so editing or predicting from one site alone is incomplete.

## Tags
unit: head | layer | weights
form: description | graph
method: ablation | patching | weight-analysis | other
eval: ablation | patching
goal: understanding | science | control/editing
