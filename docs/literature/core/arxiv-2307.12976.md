# Evaluating the Ripple Effects of Knowledge Editing in Language Models

- **Key:** arxiv-2307.12976
- **Authors / organisation:** Roi Cohen, Eden Biran, Ori Yoran, Amir Globerson, Mor Geva; Tel Aviv University / Google Research
- **Date:** 2023-07
- **Link:** https://arxiv.org/abs/2307.12976
- **Kind:** benchmark
- **Read from:** full text (Limitations section not available in the fetched text)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Knowledge-editing methods (ROME, MEMIT, MEND) are usually judged by whether the edited fact comes out and whether unrelated facts stay the same. The authors argue that this misses the logical consequences of an edit: if a model now believes X is Y's son, it should also believe X is the sibling of Y's other children. They want an evaluation that checks whether an edit is integrated into the model's knowledge, not just patched in as an isolated input-output pair. This is a test of whether localized weight edits reflect how knowledge is really organised in the model.

## What they studied
Editors: MEND, ROME, MEMIT (parameter edits) and an in-context editing (ICE) baseline that simply prepends the new fact. Models: GPT-2 XL (1.5B), GPT-J (6B), LLaMA (7B), GPT-NeoX (20B), and GPT-3 text-davinci-003 (175B, ICE only). Data: the new RippleEdits benchmark built from Wikidata. Unit: whole-model behaviour on fact queries after a weight edit.

## How they did it
They define six test types for each edit (s, r, o -> o*): Logical Generalization (relations implied by logical rules, e.g. symmetry of sibling, transitivity of location), Compositionality I (facts composed from the new object, e.g. the new object's attributes), Compositionality II (facts about other subjects that pass through the edited subject), Subject Aliasing (the edit holds under aliases of the subject), Preservation (for one-to-many relations, old objects remain), and Relation Specificity (unrelated relations of the subject are unchanged). RippleEdits has three subsets: Recent (Wikidata facts added in the 250 days after July 2022, injected as genuinely new facts), Random (sampled over 10 popularity buckets) and Popular (subjects in Wikipedia's top-1000 most-viewed pages); edits use a plausible same-relation false object for Random and Popular. Tests come from hand-written per-relation templates and rules. Table 1 lists 2,000 Recent, 1,000 Random and 1,000 Popular edits with about 19-27 queries per edit (the abstract says about 5K edits; the source of the difference was not resolved in what I read). Per model, an edit is kept only if the model knew the original fact and produces the new one after editing, and a test query is kept only if the model answered it correctly before editing.

## What counts as an explanation here
None directly; this is an evaluation. Implicitly, a correct edit is one whose consequences propagate through the model's knowledge the way a coherent knowledge base would, so passing ripple tests is evidence that the edit touched the right representation.

## How they judged success
Accuracy: each test query generates up to 20 tokens and counts as correct if any alias of the target appears; averaged per edit, then across edits, per subset and per criterion. Error analysis classifies failures as no effect, abstaining, or noise. Effects of model size and entity popularity are examined.

## What they found
Parametric editors make the target fact come out but often fail on its consequences; average accuracy ranges roughly 38-66 across models. ICE beats ROME by more than 10 points on GPT-NeoX and 29 points on LLaMA (LLaMA ROME 48.7-60.8 vs ICE 81.3-82.8 across subsets); GPT-3 ICE reaches 77.7-90.3. Subject Aliasing is easy (at least 86.8 everywhere), while compositional and logical tests are hard: on GPT-2, Compositionality II is 13.6 (MEND), 37.7 (ROME), 39.1 (MEMIT). ROME's Logical Generalization on GPT-J is 53.8 on Random vs 5.5 on Popular, so editing popular entities causes more logical errors, while Preservation is better on popular ones. Accuracy rises with model size for ROME. At least 68% of failures in every setting are wrong changes rather than no change.

## Limits and open problems they name
Existing methods do not handle ripple effects and scaling alone may not fix this; future editors need to account for consequences. (The Limitations text itself was not in the fetched content.)

## What we take from it
A warning and a test design for any model that predicts behaviour under weight interventions: a local edit can produce the targeted output while the network's wider behaviour does not update coherently, so an edit's success on its own target says little about whether we understand where the knowledge lives. The ripple-test idea (derive many consequence queries from one intervention via structured rules) is a reusable way to score whether our predicted effects of an intervention extend beyond the edited input. The filtering protocol (only score queries the model knew before) is a good control. Ties to arxiv-2304.14767: storage in MLPs vs extraction by heads may explain why MLP-only edits do not propagate.

## Tags
unit: whole-model | weights
form: description
method: other
eval: benchmark | downstream-task
goal: control/editing | evaluation-of-methods
