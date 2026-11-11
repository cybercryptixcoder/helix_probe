# Directions: everything this project could become

*Written Nov 11, 2026. A list of directions, not a plan: nothing here is approved or scheduled. Sources: Shreyas's
messages of Nov 11, the directions already scattered through these docs (`01_CONCEPT`, `10_INTERPRETABILITY_TRACK`,
`05_NEXT_STEPS`, `NORTH_STAR`, `GOAL2_CALIBRATION_RESULT`), and new ones added while reasoning about it. Each was
checked against the literature on Nov 11; "not found" means not found that day, in a field moving weekly.*

**The rule every direction was held to (Shreyas, Nov 11):**
- It is judged as a concept, as if no experiment had been run. Our runs so far are pilots, not evidence.
- It must stay centred on an AI reading another model's weights.
- It must be publishable in the worst case as well as the best.
- It must be doable with what we have (a cheap LLM, Colab L4s, open models up to 9B), or a clear alteration of it.

**Directions are not paper types.** A direction is a thing to do. A paper type is how the result gets written up.
Paper types are in section 4.

---

## 1. The directions at a glance

Families: **Understand** (what is inside), **Change** (alter behaviour), **Read** (what reading weights is),
**Trust** (can the editor be believed), **Beyond** (other boxes).

| # | Direction | Family | Nearest existing work | What is still open | Rating |
|---|---|---|---|---|---|
| U1 | **Measure a map, then test whether an AI can predict it** (section 2) | Understand | Lesion studies of LLMs; predicting effects of *prompt* edits (CHIVE); side-effect prediction by model diffing (MNEME) | Predicting the effect of *weight* changes on many behaviours, scored on changes never run | **Lead** |
| U2 | The side-effect map as a result in itself: what breaks together, what comes apart | Understand | "LLM language network" (18 models, broad domains); formal vs functional circuits | A fine-grained, many-behaviours × many-parts table, across model sizes | Part of U1 |
| U3 | One concept, mapped deeply (how one kind of thing, e.g. "which task am I doing", is stored) | Understand | Function vectors; task vectors; arithmetic circuits; operator-embedding swaps | Narrow gaps only; a crowded area | Case study inside U1 |
| U4 | What form should the "model of the model" take: table, graph, runnable code, or a second network | Understand | SAE feature atlases; attribution graphs; parameter decomposition | Comparing forms by one yardstick: how well each predicts untested changes per unit of size | Part of U1 |
| U5 | The demo: turn a part up, down or off and watch behaviour change, with the predicted side effects shown | Understand | Neuronpedia-style browsers; attribution-graph viewers | A viewer over a *measured* weight-level map with predictions | Follows U1 |
| C1 | Remove an ability | Change | Training-free skill unlearning; direction removal; LLM-editor fact forgetting (blog) | Controlled LLM-editor skill removal with honest tests | Second paper |
| C2 | Redirect an ability (the cue word chooses the task: "+" → "×") | Change | Operator-embedding swap study; function vectors | Systematic "which cue words switch which tasks" map | Small; folds into U3 |
| C3 | Add an ability the model lacks | Change | MIT: edits "could not add an ability" | Open, and probably hard for a reason | High risk |
| C4 | Change a trait or style (tone, confidence, refusal) and measure how far it goes | Change | Steering benchmarks: prompting beats steering; steering costs capability | Weight edits vs prompting vs fine-tuning at equal effort | Crowded |
| C5 | Harden: make an ability hard to remove or a removal hard to undo | Change | Tamper-resistance and robust-unlearning work | Whether an AI editor can do it without training | Needs C1 first |
| R1 | **Who can read whom:** reader size × target size, including a model reading its own family | Read | One frontier reader in MIT's post; scattered replications with other readers | A controlled grid with shuffled-weight and guessing controls | Cheap, timely |
| R2 | What reading actually is: text, code over weights, or running the network | Read | An audit arguing reading is local arithmetic plus priors | Separating the three on language models | Part of U1's arms |
| R3 | Does structure (a loop) substitute for reader intelligence? | Read | Our FIND pilot; agent scaffolds generally | Only as a factor inside another study | Not a headline |
| R4 | A library of known mechanisms handed to a weak reader | Read | None found | Whether knowledge, not reasoning, is the weak reader's gap | Cheap add-on |
| T1 | **Shortcuts:** does an AI editor change the cue or the computation? | Trust | Unlearning-robustness work; a robot-policy paper with token-row edits | How often, by which editors, under which instructions | Second paper |
| T2 | Does an editor understand its own edit? Predict the side effects before making it | Trust | One repo: reading weights barely predicts edit effects | A proper measurement | The scoring rule of U1 |
| T3 | An AI research loop games whatever score it is shown | Trust | Measured at scale (17 models, 38 tasks) | Little left | Observation only |
| T4 | Audit: find what was changed in a model (a fine-tune, a planted trigger) | Trust | Trained weight-diff describers; auditing agents | An untrained cheap reader with tools | Crowded, fast-moving |
| T5 | Plant hidden behaviour by editing weights | Trust | Established attack literature | Nothing we should lead with; dual-use | Don't pursue |
| B1 | The same loop on non-network boxes (FIND, ARC-AGI-3, BoxingGym, protocols) | Beyond | Each has strong published systems | Our pilots were marginal or zero | Parked |

## 2. The lead direction, in full: a measured map, and whether an AI can learn to predict it

**The idea in plain words.** Take a small open language model. Switch off or weaken its parts one at a time and
record, for each change, how every one of a set of abilities moves. That table is a measured map: no AI and no
cleverness is involved in making it. Then ask the real question: can a second AI, allowed to read the first
model's weights, learn the map well enough to predict what an *untested* change will do?

**Why this is the right centre.**
- It is the original Helix Probe idea (a model of the box that must predict each experiment before the box
  answers) pointed at weights, with code keeping score. No judge, no self-built success criterion.
- It answers "is the reader's understanding real?" the way science does: by prediction.
- The representation question stops being a matter of taste. A table, a graph of relations, runnable code: each is
  scored by how well it predicts held-out changes, and how small it is.
- The suppress-and-side-effects goal falls out of it: a model that predicts side effects is what you need before
  suppressing anything.

**The steps.**
1. **Measure.** A scripted sweep: each layer's two halves, then smaller parts where a layer matters, at a few
   strengths. Score abilities by answer probability (continuous), not right/wrong. Hold out a share of the changes.
2. **Describe.** What breaks together, what comes apart, how that differs between a 0.8B and a 9B model.
3. **Predict.** Readers predict held-out rows under four conditions: no access (guessing from priors), running the
   model only, reading weights through code only, and both. Compared against dumb predictors (the neighbouring
   layer's row; the average row).
4. **Represent.** The reader's knowledge kept as a table, as a relation graph, and as runnable code; same yardstick.
5. **Show.** The viewer (U5), built on the measured map.

**Best case.** A compact, readable model of a language model that predicts untested changes better than the dumb
predictors, and reading weights is shown to be what buys the gain. That is a white-box model of a black box, with
a number attached.

**Worst case.** The readers predict no better than the neighbouring-layer rule. Then the paper is: a public,
measured side-effect map across model sizes, plus the first measurement that AI readers of weights do *not* yet
understand what their changes will do. Both halves are new and useful, and the second speaks directly to the
weight-space-programming claims of this month.

**What already exists, and how this differs.**

| Existing work | What it does | What it does not do |
|---|---|---|
| The LLM Language Network (NAACL 2025) | Lesion studies in 18 models: knocking out "language units" breaks language tasks | Broad domains only; no prediction of untested lesions |
| Hanna et al. (2026) | Asks whether formal and functional language abilities come apart, by comparing task circuits | Ten tasks, one distinction; no reader |
| CHIVE (Anthropic, Aug 2026) | Scores explanations by whether they predict how *prompt* edits change behaviour | Nothing on weight edits |
| MNEME (2025) | Flags side effects of unlearning and fine-tuning by comparing features | Correlational by its own account; after the fact, not before |
| Diff Interpretation Tuning (ICLR 2026) | Trains an adapter so a model describes its own weight change | Needs training on many labelled changes; not a general reader |
| SAE atlases, attribution graphs, parameter decomposition | Maps of features and their links | Built from activations or toy models; not scored by predicting weight changes |
| Weight-space programming (Nov 2026) | Readers name what tiny networks do and repair faults | One repo reports reading barely predicts edit effects; no systematic test |

**Risks, stated.**
- The dumb predictors may be very strong (neighbouring layers behave alike). That is why they are in the design.
- Our 26-behaviour panel is home-made. Use published task sets (the function-vector tasks, the neuroscience
  localisers) beside it.
- Most abilities sit at 100%, which hid effects in our pilot. Continuous scoring fixes that; it must be checked first.
- Someone may publish a weight-side prediction benchmark soon. The measured map and the multi-size comparison
  still stand if they do.

**Cost, roughly.** The sweep is about a day of one L4. The reader runs use the cheap model. A frontier reader, for
contrast, costs API money and needs Shreyas's say.

## 3. The two runners-up

**T1 + C1, the shortcut study.** Ask AI editors to remove abilities and classify what they change: the cue word, the
output words, or the computation. As a concept it is strong and timely. Its weakness is known: the result depends
on how the editor is instructed, so the instruction must be an experimental factor. Details: the earlier research
case (held privately).

**R1, who can read whom.** A grid of reader models against target networks, with shuffled-weight controls: does
reading ability depend on the reader's size, on the target's size, on being the same family? Cheap and quick. Its
weakness: several groups have pieces of it, so it is a race, and running open readers of several sizes needs
compute or an API we don't currently have. Best used as an axis of U1, not a paper of its own.

## 4. Paper types (how a result gets written up)

| Type | What it claims | What reviewers ask for | Which directions fit |
|---|---|---|---|
| Resource / measurement | "Here is a careful measurement nobody had" | Coverage, controls, release | U2, R1 |
| Evaluation | "Here is a test, and current systems pass or fail it" | Several systems, a fair yardstick | U1, T1, T2 |
| Finding | "The model does X this way" | Causal evidence, more than one model | U3, C2 |
| Method | "Our system does X better" | Wins over strong baselines on standard benchmarks | C1, C3, C4, C5 (hard for us) |
| Negative result | "This plausible thing does not work, and here is why" | Pre-set criteria, a diagnosis | worst cases of U1, C3 |
| Demo / system | "Here is a tool" | Usefulness, a user | U5 |

U1 is an evaluation paper with a resource inside it, and its worst case is a negative result. That is why it is
defensible either way.

## 5. Sources

- AlKhamissi et al., "The LLM Language Network" (NAACL 2025): https://arxiv.org/abs/2411.02280
- Hanna, Belinkov, Pezzelle, "Are formal and functional linguistic mechanisms dissociated in language models?": https://arxiv.org/abs/2503.11302
- Karvonen et al., CHIVE (Anthropic, 2026): https://alignment.anthropic.com/2026/chive/
- MNEME, predicting side effects via sparse model diffing: https://arxiv.org/abs/2507.21084
- Goel et al., "Learning to Interpret Weight Differences in Language Models" (ICLR 2026): https://arxiv.org/abs/2510.05092
- Stochastic Parameter Decomposition: https://arxiv.org/abs/2506.20790
- "On the Biology of a Large Language Model": https://transformer-circuits.pub/2025/attribution-graphs/biology.html
- SAE inventory as a knowledge graph: https://arxiv.org/abs/2604.23829
- AxBench: https://arxiv.org/abs/2501.17148
- "Interpreting the Latent Structure of Operator Precedence in Language Models": https://arxiv.org/abs/2510.13908
- Todd et al., "Function Vectors in Large Language Models": https://arxiv.org/abs/2310.15213
- Reading-side audit of weight-space programming: https://arxiv.org/abs/2611.08070
- Weight-space programming follow-up list: https://github.com/SajjadPSavoji/awesome-wsp
- "Sparks of Weight-Space Programming": https://rikiyat.github.io/blog/weight-space-programming/
- "Reward Hacking Challenges Oversight of Autonomous Research Agents": https://arxiv.org/abs/2609.28614
- Li, Sun, Weng, "Effective Skill Unlearning through Intervention and Abstention": https://arxiv.org/abs/2503.21730
