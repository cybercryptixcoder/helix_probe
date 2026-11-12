# Function Vectors in Large Language Models

- **Key:** arxiv-2310.15213
- **Authors / organisation:** Eric Todd, Millicent L. Li, Arnab Sen Sharma, Aaron Mueller, Byron C. Wallace, David Bau; Northeastern University
- **Date:** 2023-10
- **Link:** https://arxiv.org/abs/2310.15213
- **Kind:** paper
- **Read from:** full text (HTML; appendices partly)
- **Relevance to us:** 3 (central)

## What they wanted, and why
When a model does in-context learning (ICL) from a few input-output examples, how is the task itself represented
inside it? The authors ask whether a compact internal vector carries "which function to apply", separable from the
particular examples, and whether it can be moved into another context to make the model perform that task. This is a
step toward finding the internal variables that control what a model computes, not just what it knows.

## What they studied
GPT-J 6B, GPT-NeoX 20B and Llama 2 (7B, 13B, 70B). Over 40 simple tasks (antonyms, capitalisation, country to capital,
English to French, present to past, singular to plural, translation, sentiment, NER, list selection and others),
from existing datasets and some ChatGPT-generated, partly hand-checked lists. Unit: attention-head outputs at the
final token, and their sum injected into the residual stream at one layer.

## How they did it
1. Run the model on ICL prompts and record each attention head's mean output at the last token for each task.
2. Causal mediation: run corrupted prompts whose labels are shuffled, patch one head's output to its clean task mean,
   and measure the increase in probability of the correct answer. Average over tasks and prompts to get each head's
   average indirect effect (AIE).
3. Take the top heads by AIE (10 for GPT-J, more for larger models, roughly in proportion to head count). The
   function vector (FV) is the sum of those heads' task-mean outputs.
4. Add the FV to the residual stream at one layer (about a third of the depth) when the model sees a new prompt:
   zero-shot, shuffled-label ICL, other prompt templates, and natural text.
5. Compare with a baseline vector: the average layer hidden state over ICL prompts.
6. Project FVs through the unembedding to see which tokens they promote, and test whether a vector built to match that
   vocabulary profile works as well.
7. Try composition by vector arithmetic across related list tasks.
Main evaluation uses only prompts the model answers correctly with 10 shots.

## What counts as an explanation here
A single direction in the residual stream, built from a small set of identified heads, that causally triggers a task.
It is a partial, mediator-level account: it names where the task identity lives and that it is sufficient to
trigger behaviour, not how the downstream layers execute the task. It does predict behaviour under intervention:
adding the FV should make the model perform the task.

## How they judged success
Top-1 accuracy on held-out queries in zero-shot and shuffled-label settings with versus without the FV, against the
layer-average baseline; robustness over 20 alternative templates; regex-matched accuracy on natural-text completions;
accuracy of composed vectors versus directly extracted FVs and ICL; vocabulary-matched reconstruction as a control.

## What they found
- GPT-J shuffled-label: 39.1% baseline, 79.5% with the layer-average vector, 90.8% with the FV. GPT-J zero-shot: 5.5%
  baseline, 9.5% layer average, 57.5% FV. Llama 2 70B zero-shot rises from 8.2% to 83.8%.
- Over 20 other templates (GPT-J), the FV gives 76.2% (shuffled) and 40.0% (zero-shot) versus 32.3% and 6.2%.
- In natural text, the antonym FV raises GPT-J antonym completions from near zero to roughly 46–68% depending on template.
- Effects peak in early-to-middle layers and drop sharply in late layers.
- FVs decode to task-relevant tokens for some tasks (past-tense verbs, plurals) but not others (English to French gives
  nonsense). Vectors built to match the decoded vocabulary work far worse (antonym 48.2% to 4.8%), so the FV carries
  more than its vocabulary projection.
- Composition sometimes works (one composed list task scored 0.60 versus 0.32 for ICL) and sometimes fails (0.06 versus
  0.45).

## Limits and open problems they name
FVs are not a complete account of ICL: one mediating level, not the mechanism. Tasks are simple; only correctly
answered prompts are used. Composition is not a general algebra. Vocabulary decoding is unreliable as an explanation.
Late-layer injection fails. Dual-use concern: functions could be injected maliciously.

## What we take from it
- **Method:** mean-ablation patching with AIE to localise a small set of heads, then sum their outputs into a
  transportable vector. A clean recipe for finding the "control variables" of a computation.
- **Measure:** the predictive test we want: insert the extracted variable in a new context and check the model now
  does the task, scored against a non-trivial baseline (layer-average vector), not just against no intervention.
- **Warning:** reading a vector through the unembedding understates what it does; a weight/embedding-space reading
  must be validated by intervention.
- **Framing:** tasks are represented as triggers whose effect depends on later nonlinear computation, so a white-box
  model needs both the trigger and the executing machinery.

## Tags
unit: head, direction
form: steering, direction
method: patching, steering
eval: patching, downstream-task, prediction/simulation
goal: understanding, science
