# HeadVis: An Interactive Tool for Investigating Attention Heads

- **Key:** transformer-circuits-pub-2026-headvis-index-html
- **Authors / organisation:** R. Luger, Harish Kamath (core contributors), Doug Finkbeiner, Purvi Goel, Adam Jermyn, Sam Zimmerman, Joshua Batson, Tom Conerly; Anthropic
- **Date:** 2026-05-04
- **Link:** https://transformer-circuits.pub/2026/headvis/index.html
- **Kind:** tool + paper (with case studies)
- **Read from:** full text (arXiv-free, HTML page)
- **Relevance to us:** 3 (central)

## What they wanted, and why
Feature visualisation over a full data distribution has worked well for MLP neurons and residual-stream features, but no equivalent existed for attention heads — which are harder because they are high rank, have two coupled circuits (QK and OV), and act across a whole context. The authors build an interactive tool to make heads browsable the same way neurons are, and use it to test the field's assumptions about what a head "is": that it has one behaviour, that a behaviour found on a narrow task is the head's general behaviour, and that heads are the right unit for attention decomposition.

## What they studied
Claude Haiku 3.5 heads (all), plus a public demo on Gemma 3 1B; four case-study heads: a fuzzy poetry induction head, a "line width" head, the "answer selection" head from the attribution-graph work, and a mid-layer "same-set suppression" head. Feature attributions use a 10M-feature weakly causal crosscoder (WCC). Unit of analysis: individual heads, their Q, K, O activations, and the SAE features interacting through their QK and OV circuits.

## How they did it
Frontend plus two backends: an offline pass precomputing per-head metrics and attention patterns over a dataset, and a server answering real-time queries. Views: (i) a head-selector scatter plot where any metric (layer, induction score, etc.) can be mapped to x, y or colour, so extreme heads are easy to find; (ii) attention patterns bucketed by max attention value across real dataset examples; (iii) per-head PCA of Q, K and O activations on high-attention (query,key) pairs as a cheap hypothesis-generation step for distinct behaviours; (iv) QK attribution (attention logit as a sum of query-feature × key-feature terms, i.e. steered by the crosscoder) and OV attribution (output as a sum of value-feature × output-feature terms); (v) virtual-weight analysis, projecting one feature through the head's W_K or W_Q and asking which residual features land nearby; (vi) custom sequences and a "rank all heads on this (query,key) pair" query to trace composition. Each case study is a narrative of which view answered which question.

## What counts as an explanation here
A behaviour description in feature terms plus a circuit: "queries reading feature f attend to keys reading feature g, and the OV circuit copies feature h to position x". It is partial and explicitly hypothesis-forming — the authors insist per-example attributions don't give a rule that predicts on arbitrary inputs (their year-range counterexample). Their ideal remains a complete, testable text description of a head's function.

## How they judged success
Case-study depth, not aggregate scores: does the hypothesis hold across the distribution (attention patterns on many examples), do PCA clusters corroborate distinct behaviours, do attributions make sense, and does a mechanism predict behaviour on controlled inputs. Quantitative checks used: induction score (mean attention on literal induction pairs), PCA clustering, virtual-weight cosines, and a generated test set (185 sentences where one of five cities is foreign; the country token attends to the foreign city 98% of the time) plus a country-swap control (replacing a country with itself drops attention from 0.87 to 0.08). They also state the null they could not run: splitting a polysemantic head into separate heads that jointly reproduce it.

## What they found
Fuzzy induction resolves into literal copying in the OV but feature-level matching in QK (matching on a sound, not a token). The line-width head has three unrelated behaviours (year splits, multi-token words, newlines) separated cleanly by PCA — a head can be polysemantic *without superposition*, because its output is high-rank. But its year behaviour holds only for 1000-1986, a bound visible only by sweeping inputs, which no per-example attribution surfaced. The answer-selection head looks monosemantic under a general template: OV copies whatever was marked relevant, QK matches "marked as relevant" (key) against "about to produce something matching" (query); virtual weights show other "relevant content" features are near-orthogonal in the residual stream but mapped close by W_K/W_Q. The same-set-suppression head anti-aligns a country's query with its own cities' keys (mean cosine −0.47 vs +0.01 elsewhere) although the residual stream has them positively aligned (+0.17) — the head flips the sign; on real data its behaviour is only partly visible because a Zambian feature written by an earlier head via K-composition makes it attend to seemingly unrelated tokens.

## Limits and open problems they name
Four obstacles to interpreting attention: (1) we don't know what an "attentional feature" should look like, so we can't tell if a decomposition works; (2) heads can be polysemantic without superposition; (3) attention superposition across heads is suspected but no confirmed real example exists; (4) some attentional features are high-rank (a head's QK score is a bilinear form of rank up to d_head) and the field has little experience interpreting high-rank objects. Existing rank-1-OV decompositions (attention-output SAEs, multi-token transcoders, Lorsa) split genuinely high-rank behaviours like induction. Softmax competition logic ("attend to A if present else B") is invisible to single-edge analysis. Internal-only views (custom prompts, head composition heatmaps, head-similarity metrics) are not all in the open release.

## What we take from it
Method — the strongest reusable idea: analyse a unit at the *feature* level through its circuits (QK/feature-pair decomposition, OV/feature-pair decomposition, virtual weights), not at the token level; token-level patterns are readable only in early layers. Measure: "does the hypothesis predict behaviour on controlled inputs" with a generated minimal-pair test set is what separated real mechanisms from pattern-matching here. Warning: the answer-selection head defeated a well-designed PCA route and needed feature geometry; also, a behaviour that holds on one task can be a fragment of a broader template, so we should always state the distribution over which a claim holds. Framing: heads are the wrong unit for attention; the target is a sparse, monosemantic, high-rank "attentional feature" set — an agenda our predictive model inherits.

## Tags
unit: head | feature | circuit
form: description | graph | direction
method: attribution | SAE | transcoder | probing | other
eval: downstream-task | faithfulness | prediction/simulation
goal: understanding | debugging | evaluation-of-methods
