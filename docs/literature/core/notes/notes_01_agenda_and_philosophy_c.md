# Cross-batch notes: 01_agenda_and_philosophy_c

**What an explanation should be.** Four of six papers converge on causal, intervention-backed explanation as the
standard. Saphra and Wiegreffe (arxiv-2410.09087) say causality is the only technical line separating "mechanistic"
work from any study of internals. Geiger, Harding and Icard (arxiv-2508.11214) make it precise: an explanation is a
high-level causal model the network implements under interventions (abstraction-under-translation), and a good one
must also predict off-distribution and after further training. The Copenhagen group (arxiv-2506.18852) adds
pluralism: no single true decomposition; judge one by what it lets you predict and control. Goodfire's agenda
(goodfire-blog-accelerating-interpretability) proposes causal abstraction as the claim language for verifiable,
agent-run science.

**Unit of analysis is contested.** goodfire-research-already-clean argues native neurons are already mostly
single-purpose and that decomposition-first methods (SAEs) can fail to recover known features; the optimism essay
(goodfire-blog-on-optimism-for-interpretability) still counts SAEs, transcoders and parameter decomposition as the
scalable tools. A weights-reading project should test native units before committing to a learned basis.

**How success is measured.** No agreed single metric (named as an open problem in the agenda piece). Recurring
measures: interchange-intervention accuracy (arxiv-2508.11214); predictive tests of explanations (blind
maximization from the explanation alone, predicted positives vs near misses with win/loss counts) and targeted vs
matched-random ablation (goodfire-research-already-clean). Simulation scores are criticised there as rewarding
irrelevant detail. Older NLP-interpretability probe controls are flagged as routinely ignored (arxiv-2410.09087).

**Open problems.** Triviality: with unrestricted maps, every network implements every algorithm, so admissible
translations must be constrained (arxiv-2508.11214). Explanations valid out of distribution and under learning. When
reverse engineering is complete. Vehicle vs content, and when a decodable direction counts as a belief used by the
model (arxiv-2506.18852). Scaling to frontier models.

**Bearing on a predictive white-box model from weights.**
1. Frame the white-box model as a high-level causal model and test it with interchange interventions; state the
   restricted (e.g. linear) map class up front to avoid the triviality objection (arxiv-2508.11214).
2. Use prediction under distribution shift and after fine-tuning as the headline criterion; this fills the "no
   single number" gap (goodfire-blog-accelerating-interpretability).
3. Borrow already-clean's falsifiable explanation tests and matched random-ablation controls.
4. Make every claim checkable with attached experiment code, organised by question answered.
5. Position the work as mechanistic in the narrow causal sense (arxiv-2410.09087).
