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

## 2b. Additions, Nov 11 (later the same day)

**The lead direction now has two tiers.** Small trained networks (vision classifiers and RL policies from public
model zoos), where the ablation table can be exhaustive and the reader can see every weight; and language models
(Qwen 0.8B and 9B, plus a second family), where the reader works through code. The project is not specific to
language models.

**A correction to the prior-art table above.** Two items were missed in the first scan:
- *WSPBench* (a repository preview): constructed Boolean ReLU circuits of about 4,000 weights, with unaided,
  weight-analysis and instrumented conditions and a before/after edit task. Three frontier models scored 0/4
  unaided. It is the nearest thing to U1's design. It has no trained networks and six problems.
- *Weight Oracles* (Oct 2026): a language model fine-tuned to read raw weights. It simulates the forward pass of
  unseen small transformers and flags unseen backdoors. Small transformers only; the authors name scaling as the
  main open problem. It does not predict the effects of ablations or edits.

So "nobody has tested prediction of weight edits" is too strong. What is open: the test on trained networks at
scale, with trivial and trained baselines, and a study of what determines the ability.

**New directions from Shreyas (Nov 11), each checked.**

| # | Direction | Nearest existing work | What is open | Rating |
|---|---|---|---|---|
| N1 | **A trained reader:** a model trained on our ablation tables to predict effect rows from weights | Weight-space learning (predicts accuracy and hyperparameters); Weight Oracles (simulates small transformers) | Predicting *intervention effects*, and a head-to-head with untrained LLM readers on the same held-out rows | Add to U1 as a stage |
| N2 | **Precise suppression:** pick the edit with the least predicted collateral | Learned editors (MEND and successors) predict weight updates under a locality constraint, for facts; closed-form linear concept erasure | Skill-level suppression chosen by a side-effect predictor. "Exact" is unlikely in general, since parts are shared between behaviours | Follow-on to U1; do not promise |
| N3 | **What helps or hurts reading:** reader size, text versus code, precision, target size, reasoning budget | An audit attributing reading to local arithmetic plus priors; our own pilot (thinking on versus off, code versus text) | A controlled one-factor-at-a-time study | The analysis section of U1 |
| N4 | **Self-reading:** does a model read its own family's weights better? | Behavioural self-prediction beats cross-prediction after fine-tuning (Binder et al.), disputed since; one 2026 study found a different model predicted as well | Never tested with weights | One arm of N3. Caveat: small open models are weak readers (one repo got 0/16 valid answers from a 1.5B model) |
| N5 | **Fine-tune an LLM to read weights better** | Weight Oracles; Diff Interpretation Tuning | Fine-tuning on intervention-effect data; whether it transfers across architectures | Compute-heavy for us; N1 is the cheap version |
| N6 | **A benchmark for weight reading** | WSPBench; MIT's announced benchmark | One built on trained networks with measured ablation tables | U1's tables are this benchmark; release them, but do not race MIT on a general one |

**How the lead direction would be run** (the answer to "how are you planning to do that?"): the reader is the
probing loop this project started from. It picks an unseen intervention, inspects the weights, commits to a
predicted effect, then sees the measured one and revises a running set of notes. Code scores it. The learning
curve (accuracy on unseen interventions against number of probes) shows whether understanding accumulates. A
one-shot reader at the same budget is the control for the loop.

## 2c. The niche (Nov 11): open models reading open models, including themselves

Shreyas: the paper is for a conference, and it must stay distinct from what MIT and others are likely to publish
next. Proposed constraint: **open-weight readers and open-weight targets from the same pool.**

Why this constraint and not another:
- Closed frontier models can read open targets, but nobody outside a lab can give a frontier model its own weights.
  Self-reading is therefore structurally hard for the groups most likely to publish next.
- No experiment so far has had a model read or edit its own weights; MIT lists it as future work.
- An open mid-size model (Qwen 3.8 27B, quantised, on a laptop) already reads small networks' weights, so the
  pool is not doomed to floor effects. Very small models are (0/16 valid answers from a 1.5B model in one repo).

What the constraint combines: U1 (measured map, prediction score), N3 (what helps or hurts reading), N4
(self-reading), N1/N5 (a trained or fine-tuned reader), and the small-network tier as a per-reader calibration.

Headline question: **does a model know what changing its own weights will do, and better than it knows other
models?** The reader × target grid (self, sibling of another size, stranger of the same size) separates capability,
architectural familiarity and privileged self-access.

Alternatives considered: "small models only" (risks floor effects and reads as a limitation); "language models
only" (no moat); "one behaviour family deeply" (narrow, and crowded for arithmetic). Kept as fallbacks.

## 2d. The paper's structure (Shreyas, Nov 11)

Shreyas: the paper need not be one direction from this file; any set that fits together is fine. The niche splits
naturally into a benchmark and three axes, and together they make one paper.

| Part | Question | Role in the paper |
|---|---|---|
| Benchmark | How do we measure reading and modifying? Read = predict an edit's effects; Modify = make an edit that hits a target with least collateral. Both scored against measured tables. | The instrument; a release in its own right |
| Axis 1, size | Does ability scale with the reader/editor's size within a family? | Explains Axis 3 |
| Axis 2, factors | Text vs code, precision, target size, reasoning budget, loop vs one shot, untrained vs fine-tuned | Explains Axis 3; the "what helps or hurts" result |
| Axis 3, self | Is a model better on its own weights than a sibling or a same-size or larger stranger? | The headline |

Risk to manage: four parts can read as unfocused. The writing has to keep one question in front and the rest as
the means of answering it fairly.

**Literature check of 2d (Nov 11, 10:15 ET).**

| Part | Nearest existing work | What is still open | Effect on the plan |
|---|---|---|---|
| Size | One researcher ran the same weight task across successive frontier generations and saw the ability appear as a step in the newest ones. MIT tested one reader only. | A controlled within-family size sweep with open models; any size curve for prediction or for editing | Stands |
| Factors | MIT varied the forward-pass budget; WSPBench separates unaided, analysis and instrumented conditions; an audit attributes reading to local arithmetic plus dataset priors | A one-factor-at-a-time study of what drives reading and editing | Stands |
| Self | Nothing found that hands one instance of a model a copy of its own weights to read. Adjacent but different: Open-Weight Masked Introspection (activations altered mid-run, model asked if it noticed: chance) and the Quine Test ("own weights" there means a fresh instance of the same model reproducing its behaviour; no weight reading). | Reading a copy of one's own weights as data, for prediction and editing | **Open, with no informative prior.** The two adjacent papers test introspection, not weight reading (corrected 10:30 ET after Shreyas flagged it). |
| Modify | A large model-editing literature: edits cause ripple effects and collapse; locality metrics are known to be weak; synthetic benchmarks for editing exist | LLM agents as editors, scored against measured collateral across many behaviours | Part of the benchmark, not a claim of novelty |

**Headline:** *what determines how well a model can read and modify neural network weights: its size, how the
weights are shown, how it works, whether it was trained for it, and whether the weights are its own.* Self is the
most distinctive axis and has no informative prior. One concrete reason it could show an advantage: a model's
embedding and output rows are its own token representations, so it may recognise structure in them that a
stranger cannot.


## 2e. Goodfire, "Neurons as an Interpretable Basis" (Nov 10, 2026), checked Nov 12

What it is: a study of Qwen3.6-35B-A3B's MLP neurons. Findings: neurons are functionally sparse (dropping 92% of
the weakest routed activations costs 2.9% loss, recoverable by light fine-tuning); most neuron poles have one or a
few "modes"; a frontier agent (the "Neuron Scientist", with activation, steering, attribution and circuit tools)
writes descriptions that let a judge detect firing (~95% vs random text) and let a simulator restore 73% of the
ablation damage (relative to a perfect-reader ceiling). A public Neuron Atlas accompanies it. Companion to the
Oct 15 essay "Neural Networks Are Already Clean".

| Question | Answer |
|---|---|
| Does it scoop us? | No. Evidence is activations, not weights handed to a reader as data. No LLM edits weights. No self-reading. One model, frontier agents only. It predicts *activations*, not the effects of weight changes. |
| Does it support us? | Yes. (1) It scores explanations by prediction under ablation, the yardstick we chose. (2) It makes individual neurons a defensible unit of intervention, finer and more interpretable than layers. (3) A neuron's gate inputs explain 59% of the variance in its firing size, against 14% for the text: internal structure carries what text can't, which is the case for reading weights. |
| New opportunity | A head-to-head on the same neurons: a reader given only a neuron's weights versus Goodfire's activation-based descriptions, scored on Goodfire's own metrics. And the self version: Qwen3.6 reading Qwen3.6's neurons. Their target is in our pool's family. |
| New risk | Goodfire is well-resourced, has an agent product (Silico), and calls this the first post in a "native interpretability" series. Reading weights directly is a natural next step for them. Our moat is the controlled size/factor/self study across open models, not single-model depth. |
| Open check | Whether the atlas's descriptions can be downloaded and reused (the page is JavaScript-only and states no licence). |

## 2f. The constructor (Shreyas, Nov 13)

The project builds the **constructor**: a loop in which an LLM reads a network's weights and produces a causal abstraction of it (what a construction is: see `literature/SYNTHESIS.md` §1 and §10). The first paper only needs one solid construction made by the constructor. Making the constructor general comes later. Everything below is a draft for discussion; none of it is decided.

### New directions

| Id | Direction | What it asks |
|---|---|---|
| K0 | **Replicate first** | Can the loop rediscover a published construction (modular addition first) without seeing the answer? We tune the loop on known answers before using it on unknown ones. |
| K1 | **The reader interface** | The first step of every iteration: what we hand the LLM (which weights, in what form, with what question), what answer we want back, and which choices give better or more relevant answers. Measured, not guessed. |
| K2 | **A fine-tuned reader** | Since reading seems to be a capability learned in pre-training, can fine-tuning strengthen it for the K1 interface? Usually this would be RL, but the method is open. This needs K1's answer format defined first. |
| K3 | **The loop itself** | Read → hypothesis → test the mapping → assemble a runnable construction → test the algorithm → repair. Draft below. |

Each of these could be its own paper. Together with the earlier directions there are perhaps six.

### Literature check (from the survey, plus a search on Nov 13)

- **Correction (Nov 13): no one has fine-tuned an LLM to read weights pasted as text.** The earlier "trained readers" take weights through a different channel:
  - Weight Oracles (arxiv-2610.07334) maps each matrix row into the LM's hidden space with a learned linear layer, as continuous tokens, not text;
  - LoRAcles turns LoRA deltas into SVD direction tokens through an encoder;
  - Diff Interpretation Tuning (arxiv-2510.05092) has the fine-tuned model describe *itself*, so no weights are given as input at all.

  The reading audit (arxiv-2611.08070) agrees: to its authors' knowledge, none of these tests a general-purpose LLM reading an arbitrary small network zero-shot. So K2 (RL on a pre-trained LLM to strengthen reading weights given as text, rewarded on verified predictions) has no prior that we have found. (This also reverses an earlier edit that removed "continuous tokens" from the Weight Oracles description: the full text confirms it.)
- **Raw reading has a size ceiling.** In Sparks, raw-weight reading worked only on networks of about 17K–172K weights; the LM-scale wins used Python and/or execution. Results must be reported per access regime: raw weights only, weights plus code, or weights plus forward passes (honnibal-dev-blog-astra-read-write-misleading). The Nanda modular-addition transformer has roughly 226K parameters: about 15K embedding, 66K attention, 131K MLP and 15K unembedding. That is too many to paste whole into a 164K-token context, so K1 is partly forced: the reader sees slices, transforms, or tool output.
- **Memorisation risk is high.** Modular addition has the original paper, an ICLR spotlight, follow-ups (e.g. arxiv-2602.16849, arxiv-2505.18266), tutorials and replication walkthroughs. The reader has almost certainly seen "grokked modular addition → Fourier". Hiding the paper is not enough. We must blind the task, and include variants whose answer is known but rarely written up.
- **Reader-shortcut controls already exist**: shuffled weights, an untrained network, a prompt-only reader, anonymised labels, and default-answer rate (lesswrong-wnl4nwrs2owzzfwiz-wsp-stratification).

### K1: the reader interface, as an experiment

Factors to vary, one at a time at first:
- **View**: a raw slice (e.g. one embedding row block), a transform of it (FFT over the input axis, SVD, a norm map), summary statistics, or tool access (the reader writes Python against the weights and sees the output).
- **Question scope**: open ("what does this network do?"), component ("what do these 8 neurons do?"), or targeted ("is W_E periodic in the input index? which frequencies?").
- **Context**: task told vs blinded (input/output examples only, or query access only); architecture told or not.
- **Answer format**: free text vs a fixed schema.
- **Reasoning budget**; single-shot vs multi-turn.

The score, so this is measured: the fraction of readings whose prediction holds when the harness runs the intervention. A reading that predicts nothing testable scores zero.

Draft answer schema (a "reading"):
```
claim:      what this part computes, in words
location:   which weights (matrix, rows/cols, neurons, heads, or a subspace)
variable:   the named quantity it holds or produces, if any
prediction: a concrete, testable effect, e.g. "zeroing these 40 neurons drops accuracy to chance;
            keeping only frequencies {14,35} keeps >90%"
confidence: 0–1
```
The `prediction` field is what links K1 to K2. It gives an automatic, verifiable reward, which RL needs.

### K3: draft loop. A SKETCH ONLY, NOT DECIDED, AND NOT THE FIRST BUILD

Shreyas (Nov 13): do not settle on this loop, its roles or its agents yet. Building it first would just be another Helix version. Build what is needed: the first build is the Weight Reading Lab (`WHAT_WE_ARE_BUILDING.md`). One open alternative to feeding slices is that the reader queries the weight store itself.

0. **Setup.** Target network; behaviour spec (input/output examples or query access, possibly blinded); inspection tools; budget.
1. **Read.** The reader gets a view and a question (K1) and returns readings in the schema.
2. **Test the mapping.** The harness runs each reading's prediction as an intervention: ablate, restrict ("keep only"), exclude ("remove only"), or patch. Readings that fail go back to step 1 with the result attached.
3. **Assemble.** Surviving readings become a draft construction:
   - a runnable Python model of the algorithm, with named variables and steps;
   - an alignment table saying where each variable lives in the network.

   Note: it maps variables and steps to locations. It does not map weights to weights.
4. **Test the algorithm**, using the field's three questions:
   - (a) Run the construction on held-out inputs: does it match the network's outputs?
   - (b) Interchange tests: set a variable in the Python model and make the matching change in the network (by patch or weight edit). Do both change the same way?
   - (c) Substitution: replace the component with weights generated from the construction. How much ablation damage is restored?
5. **Repair or rethink.** Feed the failures back. Narrow the question, change the view, or discard the hypothesis.
6. **Stop** when (a)–(c) clear preset thresholds on held-out data, or the budget runs out. A stop rule is needed because agents tend to declare success too early (see the agents batch in the survey).

### K0: replication plan, draft

- **Targets with known constructions**, giving several answers to check against: modular addition (Nanda), group composition (arxiv-2302.03025), and a Tracr-compiled program (exact ground truth).
- **Variants** that are known in principle but rarely written up: modular subtraction or multiplication, a different modulus, a two-layer MLP version.
- **Blinding.** Don't name the task. Possibly permute the vocabulary so the "number line" isn't given away; this changes difficulty, and is itself a measurement.
- **Controls**: the same loop on an untrained network and on shuffled weights. It should find nothing.
- **Success** means recovering the key elements (frequencies, the trig-identity step, the scoring step), confirmed by restricted and excluded loss and by substitution. A matching story alone is not enough.

### Open questions for discussion

1. What does the reader start from: raw slices, or tool access from the start? (Sparks suggests tools are needed past about 170K weights.)
2. Is the construction's language Python plus an alignment table, or something stricter like RASP? Python is runnable and LLM-friendly; RASP gives a fixed vocabulary for transformer programs.
3. How much blinding is fair? Is a vocabulary permutation a fair test, or a different task?
4. Which reader models, and is the reader also the one assembling the construction, or is that a second role?

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
- WSPBench: https://github.com/alexcarterhq/wspbench
- Weight Oracles: https://arxiv.org/abs/2610.07334
- Binder et al., "Looking Inward: Language Models Can Learn About Themselves by Introspection": https://arxiv.org/abs/2410.13787
- Morcos et al., "On the Importance of Single Directions for Generalization": https://arxiv.org/abs/1803.06959
- Schürholt et al., "Model Zoos": https://arxiv.org/abs/2209.14764
