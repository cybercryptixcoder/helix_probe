# Weight-Space Programming: a reproducible laboratory (incl. balanced function-reading study)

- **Key:** github-ttm-weight-space-programming
- **Authors / organisation:** Renato Fabbri (GitHub ttm); independent
- **Date:** 2026-11 (model runs dated 2026-11-05)
- **Link:** https://github.com/ttm/weight-space-programming
- **Kind:** tool (testbed repository with exploratory pilots)
- **Read from:** README in full; `docs/WEIGHT_READING_PILOT.md`, `docs/BALANCED_READING.md`, `docs/CONSTRAINED_READING.md`, `docs/OPEN_MODEL_SMOKE.md`, `experiments/reports/README.md` in full; the H2/H5 sections of `docs/RESEARCH_AGENDA.md`; the raw report JSONs `experiments/reports/2026-11-05-reading.json`, `-balanced-reading-direct.json`, `-balanced-reading-deliberate.json`, `-constrained-reading.json` (prompts, raw outputs, summaries). Not read: `docs/RESULTS.md` (fetched, skimmed only via the agenda), `docs/THEORY.md`, `docs/DIRECT_SYNTHESIS*.md`, source code, the synthesis report JSON. GitHub API was blocked; files fetched by raw URL.
- **Relevance to us:** 2 (useful)

## What they wanted, and why
An independent, small, fully reproducible lab inspired by the MIT WSP post, aimed at separating questions the post blurs: can a model write weights for a behavioural spec, can it read a network's function from its weights, and can it repair weights, each against baselines (symbolic construction, random search, gradient training). The reading line asks (H2) whether an LLM can identify a network's function from numbers alone when architecture and metadata are held fixed, and (H5) whether its readings are invariant to function-preserving reparameterisation (neuron permutation, positive ReLU rescaling). It explicitly does not reproduce the MIT experiments.

## What they studied
Readers: Qwen3-0.6B (pinned revision) for the first reading pilot; Qwen2.5-1.5B-Instruct (pinned revision) for the balanced and constrained pilots. Targets: hand-constructed (not trained) tiny ReLU networks over 4 binary inputs: first pilot 4-3-1 networks for three DNF functions; balanced pilots 4-4-1 networks for four families (4-bit parity, pairwise XOR, 3-input multiplexer, signed threshold), each with exactly 8 positive outputs of 16. Unit: whole network. Separately, GPT-6 (ChatGPT) was used for weight synthesis (writing), not reading.

## How they did it
1. Generate functions deterministically from public seeds; build an exact ReLU network per function.
2. For each, make a second, equivalent network by permuting hidden units and rescaling incoming/outgoing ReLU weights by positive reciprocal factors; verify all 16 outputs match.
3. Show each presentation in an independent, stateless prompt with only matrices, input/output semantics and an anonymous ID; no family, pairing, seed or labels.
4. Ask for a 16-bit truth table as strict JSON; greedy decoding on a CPU GitHub Actions runner; no tools, no probes; invalid output counts as failure with no repair or reprompt.
5. Balanced pilot: two frozen prompt conditions, "direct" and "deliberate" (silently derive hidden activations first), on the same eight presentations.
6. After every output in the balanced pilot was format-invalid, a post-hoc constrained follow-up restricted decoding to the tokens for 0 and 1 for exactly 16 positions, removed the enumerated input list from the prompt, and logged per-bit conditional probabilities.
7. Compare against an exact-executor (oracle) control and an all-zero control; archive prompts, hashes and raw outputs; provide replay scripts.

## What counts as an explanation here
A predicted truth table, i.e. a full behavioural prediction of the network on its entire input space. The agenda also calls for circuit descriptions and neuron attributions, but none were elicited in the pilots.

## How they judged success
Primary: number of functions for which both presentations (original and gauge-transformed) are exactly right ("both-exact", per function, not per network). Secondary: valid outputs, exact tables, mean bit accuracy, pair agreement split into trivial (constant) and nontrivial, count of constant predictions, and a Brier score on the restricted binary-token probabilities. Baselines: oracle executor (ceiling), all-zero predictor, neutral 0.5 probability (Brier 0.25). Balanced labels make constant guessing score 50% bit accuracy and zero exact functions.

## What they found
- Qwen3-0.6B first pilot: 6/6 valid JSON, 0/6 exact, mean bit accuracy 66.67%, 3/3 pairs agree; but every reply was all zeros, so agreement and bit accuracy were artefacts of label imbalance.
- Qwen2.5-1.5B balanced pilot: 0/8 valid in both direct and deliberate conditions (0/16); every output copied the input enumeration instead of predicting outputs.
- Constrained follow-up: 8/8 valid, 0/8 exact, 0/4 both-exact, all eight predictions constant zero, 50% bit accuracy, Brier 0.39443402 (worse than the neutral 0.25).
- Writing side (not reading): GPT-6 in ChatGPT passed 9/10 and then 13/14 self-authored direct-synthesis tasks; architecture-matched random controls 0/390. The author stresses the model also designed the tasks and had tool access, so this is not blinded competence.

## Limits and open problems they name
Tiny samples (3–4 functions), tiny reader models, single greedy samples, public generators (no sealed tasks), no stronger reader tried for reading, post-hoc follow-up not confirmatory. Pair agreement is neither necessary nor sufficient for understanding. Results say nothing about trained or large networks. A sealed evaluator with private seeds is still needed.

## What we take from it
- **Measure:** the "both presentations exactly right, per function" metric under permutation + positive rescaling is a clean invariance test for any K1 reading claim; we should adopt it.
- **Control:** balance labels so constant answers score at chance, and always report constant-prediction rate next to agreement.
- **Warning (format):** small readers fail on output format before reasoning; separate format compliance from function inference (constrained decoding is one way, with its caveats).
- **Warning (our observation, not the author's):** the first pilot's prompt showed an all-zero string as the JSON example, and every reply returned exactly that string; example values in a format spec can anchor the answer.
- **Framing:** this task allows (indeed asks for) mental execution of a 16-input network, unlike MIT Experiment 2's "no forward pass" rule; results from the two are not directly comparable.

## K1 detail (reading setup)
- **Reader model(s), and the score for each:** Qwen3-0.6B (rev c1899de…): 0/6 exact, 66.67% bit accuracy (all-zero). Qwen2.5-1.5B-Instruct (rev 989aa79…): direct 0/8 valid, 0/8 exact; deliberate 0/8 valid, 0/8 exact; constrained 8/8 valid, 0/8 exact, 0/4 both-exact, 50% bit accuracy, Brier 0.394. No frontier model was used for reading.
- **Target networks:** constructed by hand/generator, not trained. First pilot: 4 binary inputs, 3 ReLU hidden, 1 linear output (4-3-1), three DNF functions, each in original and permuted/rescaled form. Balanced: 4-4-1, four functions (parity, pairwise XOR, multiplexer, threshold), each twice. Output bit is 1 iff the logit is strictly positive. Parameter count not stated (4-4-1 implies 25 scalars; our arithmetic).
- **How the weights were presented:** text. First pilot: one compact JSON object of layers with `weights` (as out × in lists), `bias`, `activation`. Balanced and constrained: Python-style lists, one line per tensor (`W1=[[…]]`, `b1=[…]`, `W2=[[…]]`, `b2=[…]`), values with one decimal place as stored (e.g. 4.0, -0.25); no labels beyond tensor names. Total tokens not stated (prompts are short).
- **Prompt:** first pilot: interpret only the literal weights, without executing the network or using tools; inputs are 4 bits; output rule (logit > 0); return only JSON with a 16-character truth table in lexicographic input order; no explanation; architecture stated. Balanced direct: read (not write) the weights; explicit equations for hidden and output; list of the 16 inputs in order; return one JSON object with key `truth_table`; compute all results directly from the arrays; no reasoning shown. Deliberate: same, but told to work out every hidden activation silently, combine them, check threshold ties, and give only the answer. Constrained: same equations, inputs described as integers 0–15 with x0 most significant, no enumerated inputs, output 16 bits only. No candidate answers. Full prompt texts are archived inside `experiments/reports/2026-11-05-*.json` (field `prompt`).
- **Access regime:** no tools, no probes, no feedback; single independent call per presentation; greedy decoding; max 128 new tokens (balanced), 16 forced tokens (constrained), 640 (synthesis smoke). The task effectively invites mental forward computation.
- **Controls:** function-preserving reparameterisation pairs (permutation + positive rescaling); label-balanced truth tables; all-zero predictor; oracle executor; neutral-probability Brier baseline; prompt condition (direct vs deliberate). No shuffled-weight or untrained control.
- **Failure modes observed:** constant all-zero output (0.6B, and 1.5B under constrained decoding), giving trivial pair agreement and inflated bit accuracy under imbalanced labels; copying the input enumeration as the answer (1.5B, all 16 calls); Markdown fences and copied task metadata instead of numbers (synthesis).
- **Prompt/format choices that helped or hurt:** listing the 16 input patterns in the prompt gave the model something to copy (author's diagnosis; removed in the constrained version). Constrained decoding fixed format but not content. The "deliberate" instruction made no difference. (Our observation: the all-zero example in the first pilot's JSON template matches every reply.)
