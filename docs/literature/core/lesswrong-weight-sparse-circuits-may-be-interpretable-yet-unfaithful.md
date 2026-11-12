# Weight-sparse circuits may be interpretable yet unfaithful

- **Key:** lesswrong-weight-sparse-circuits-may-be-interpretable-yet-unfaithful
- **Authors / organisation:** jacob_drori (LessWrong handle); Anthropic Fellows Program, mentored by Nick Turner and Jeff Wu
- **Date:** 2026-02-09 (the scout listed 2025-12; the page shows February 2026)
- **Link:** https://www.lesswrong.com/posts/sHpZZnRDLg7ccX9aF/weight-sparse-circuits-may-be-interpretable-yet-unfaithful
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Gao et al. (2025, OpenAI, arXiv 2511.13653) train transformers whose weights are mostly zero, then prune them to small task-specific circuits, and claim these circuits are smaller than in dense models at equal loss and are interpretable. The author replicates the size claim and then asks whether the pruned circuits actually reflect how the full model computes the task, i.e. whether a small, low-loss, human-readable circuit is also faithful. The broader concern is that optimising only the loss-versus-circuit-size trade-off can yield convincing but wrong explanations.

## What they studied
Two-layer transformers trained on 2B tokens of SimpleStories: one dense (d_model 128, about 1.4M nonzero params) and weight-sparse models at d_model 1024, 3072 and 4096 (nonzero fractions 1/64, 1/200, 1/500). Three tasks: pronoun matching, a simplified indirect-object-identification task (him/her), and question-mark prediction. Unit: nodes (neurons, attention components) of pruned circuits.

## How they did it
Following Gao et al.'s pruning (learned masks over nodes, hyperparameters tuned by a CARBS sweep), but with zero ablation of removed nodes because it gave smaller circuits than mean ablation. They first replicated circuit size vs. loss curves. Then four faithfulness probes: (1) prune for a nonsense task to see how easily small low-loss circuits can be found for something the model was not doing; (2) compare attention patterns of heads in the pruned circuit against the original model; (3) check whether nodes keep the same role (what they depend on) before and after pruning; (4) prune with 100 random seeds and test out-of-distribution generalisation (same-gender IOI prompts) versus the full model. They also froze layernorm scales as a variant.

## What counts as an explanation here
A pruned subgraph (circuit) of the sparse model that alone achieves low task loss and whose nodes can be described in words. The post's point is that this form of explanation can be interpretable without being the model's actual mechanism.

## How they judged success
Task cross-entropy of the pruned circuit vs. number of nodes; nonsense-task control; attention pattern comparison; node role consistency; out-of-distribution accuracy of circuits vs. the full model across seeds; mean vs. zero ablation comparison. The author tried an importance-based faithfulness metric but found it unconvincing.

## What they found
- Replication: sparse models usually gave smaller circuits on pronoun and IOI tasks; on question marks only two sparse models beat dense, narrowly.
- Nonsense task: under 0.05 loss (over 95% accuracy) with about 30 nodes, versus about 10 nodes for the real pronoun task, so pruning can manufacture low-loss circuits.
- Mean ablation may be more faithful but needed about 100 nodes for pronouns.
- A pruned head had uniform attention while the original attended sharply to the name; a node acted as a gender detector only after pruning.
- IOI (d=3072): full model 89% on opposite-gender and 81% on same-gender prompts; of 77 retained seeds many circuits scored near 0 on same-gender prompts, and circuits from different seeds generalised very differently.

## Limits and open problems they name
Evidence suggests, not proves, unfaithfulness; tiny two-layer models; unequal nonzero parameter counts; seeds share hyperparameters; only three tasks; no good faithfulness metric found. Next steps: a better faithfulness metric (causal scrubbing perhaps too strict), prune to optimise it, recheck size advantages; attribution graphs might be more faithful (untested).

## What we take from it
A direct warning for our project: a small, readable reconstruction that matches loss on the training distribution can still be a different mechanism. Our white-box model must be checked for (a) agreement with the original's internals (attention patterns, node roles), not only outputs, and (b) agreement off-distribution and under interventions. The nonsense-task control (how small a circuit can be for a task the model does not perform) and the multi-seed OOD spread are cheap, reusable controls. Zero vs. mean ablation choice materially changes results.

## Tags
unit: circuit | weights
form: graph
method: training-interpretable | ablation | other (pruning)
eval: faithfulness | ablation | prediction/simulation
goal: evaluation-of-methods
