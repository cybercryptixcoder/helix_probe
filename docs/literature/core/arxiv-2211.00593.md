# Interpretability in the Wild: A Circuit for Indirect Object Identification in GPT-2 Small

- **Key:** arxiv-2211.00593
- **Authors / organisation:** Kevin Wang, Alexandre Variengien, Arthur Conmy, Buck Shlegeris, Jacob Steinhardt; Redwood Research / UC Berkeley
- **Date:** 2022-11
- **Link:** https://arxiv.org/abs/2211.00593
- **Kind:** paper
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Earlier mechanistic work explained toy models or small pieces of real models. The authors wanted an end-to-end account of a natural behaviour in a real pretrained language model, to test whether mechanistic interpretability scales, and to propose explicit criteria for judging whether a circuit explanation is right. The task is indirect object identification (IOI): in "When Mary and John went to the store, John gave a drink to", the model should predict "Mary", the name that was not repeated.

## What they studied
GPT-2 small. Units: attention heads at specific token positions (a circuit of 26 heads, about 1.1% of head-position pairs). MLPs, layer norms and embeddings were not decomposed.

## How they did it
They built an IOI dataset from 15 templates filled with random single-token names, places and objects, plus a matched distribution p_ABC where the same templates contain three unrelated names. Behaviour is measured by the logit difference between the indirect object (IO) and the subject (S). Components are knocked out by mean ablation over p_ABC, which removes the sentence-specific information while keeping generic structure. To trace information flow they introduced path patching: replacing a head's activation with its value on a corrupted input but only along chosen paths to downstream components, so direct and indirect effects can be separated. Working backward from the logits, they identified heads, then classified them by attention patterns, projections of their outputs onto unembedding directions and copy scores. The result was seven head classes: Duplicate Token and Previous Token heads (early), Induction heads, S-Inhibition heads, Name Movers, Negative Name Movers and Backup Name Movers.

## What counts as an explanation here
A circuit: a subgraph of heads with a human-readable role for each class, forming an algorithm (find duplicated names, inhibit attention to the duplicated name, copy the remaining name to the output). Meant to be a fairly complete account of the task at head level, but admittedly partial (MLPs and some attention patterns unexplained). It predicts behaviour well enough to generate adversarial examples.

## How they judged success
Three criteria, each computed with mean ablation and logit difference: faithfulness (the circuit alone, rest ablated, performs like the full model), completeness (for any subset K of circuit nodes, removing K from the circuit and from the full model should have similar effects; tested with random subsets, whole-class removals and greedy search for worst-case K), and minimality (every node contributes, i.e. there is a subset whose removal changes performance when the node is also removed). A naive circuit without backup and negative heads serves as a comparison. Adversarial prompts derived from the circuit are tested against a control.

## What they found
On 100,000 examples the full model's mean logit difference is 3.56, IO is preferred to S 99.3% of the time, and mean IO probability is 49%. The circuit's logit difference differs from the model's by 0.46 (13% of 3.56), i.e. about 87% of performance is retained. Random and class-wise completeness tests look fine, but greedy search found subsets with incompleteness up to 3.09, so the circuit is not complete. Each node contributes at least 1% of the logit difference. The naive circuit looked faithful but failed completeness more easily, showing why faithfulness alone is insufficient. Backup Name Movers take over when the main Name Movers are ablated (redundancy). Adding a sentence that repeats the IO name drops the logit difference to 1.23, and S is preferred 23.4% of the time versus 0.4% in a control repeating S.

## Limits and open problems they name
S-Inhibition attention patterns, MLP roles and layer norm are not explained; the worst-case incompleteness subsets are not interpretable; Induction heads behave differently from their original description; Duplicate Token validation is partial; the dropout explanation for backup heads is a hypothesis; only GPT-2 small was analysed (GPT-2 medium looked more complex); the adversarial examples might have been found without the circuit.

## What we take from it
The faithfulness / completeness / minimality triad, with mean ablation over a matched counterfactual distribution, is the standard evaluation vocabulary; we should report all three, not faithfulness alone. Path patching is the standard tool for separating direct and indirect effects. Two warnings for a predictive white-box model: backup components mean that predictions under ablation must model compensation, not just remove a component; and a circuit that is faithful on-distribution can still be incomplete. Deriving adversarial inputs from the explanation is a good test of predictive power.

## Tags
unit: head | circuit
form: graph | description
method: patching | ablation | attribution
eval: faithfulness | completeness | ablation | patching | prediction/simulation
goal: understanding | science | evaluation-of-methods
