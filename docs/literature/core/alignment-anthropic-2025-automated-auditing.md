# Building and Evaluating Alignment Auditing Agents

- **Key:** alignment-anthropic-2025-automated-auditing
- **Authors / organisation:** Trenton Bricken, Rowan Wang, Sam Bowman, Euan Ong, Johannes Treutlein, Jeff Wu, Evan Hubinger, Samuel Marks; Anthropic
- **Date:** 2025-07-24
- **Link:** https://alignment.anthropic.com/2025/automated-auditing/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Alignment audits take a lot of expert time, and it is hard to know whether an audit missed something. The authors build LLM agents that carry out auditing workflows on their own. Because agents can be run many times from identical starting states, they also become a replicable way to measure how much a given tool (e.g. SAE features) actually helps: compare average agent success with and without it.

## What they studied
Agents built on Claude Sonnet 4 (and Claude Code instances). Targets: the RM-sycophancy model organism from Marks et al. (arxiv-2503.10965), ten system-prompted "quirky" models, and real Claude Sonnet 3.7 and Opus 4. Units available to the agent: whole-model behaviour, training data, SAE features (1M-feature SAEs).

## How they did it
Three agents. The investigator agent runs open-ended investigations with tools for chat (multi-turn, system prompts, prefill, raw sampling), grep and semantic search over pretraining/SFT/RL data, interpretability (top-activating SAE features, feature details, nearest-neighbour features, per-token activations, steering), and memory/todo tools. In the auditing game it must find the root cause (RM sycophancy) and as many of the 52 behaviours as possible; Claude Sonnet 4 grades reports. Toolsets were varied to measure each tool's contribution, and a "super-agent" aggregated ten single-agent reports. The evaluation agent turns a behaviour description into a behavioural evaluation (plan, implement, revise) and is tested on whether its eval separates quirky models from baselines, five runs per quirk. The breadth-first red-teaming agent runs many independent conversations (255 seed instructions, two runs each) and surfaces concerning transcripts for humans.

## What counts as an explanation here
An audit report: a root-cause statement plus a list of behaviours, or a behavioural evaluation that discriminates a quirk. Interpretability outputs are tools in service of these, not explanations themselves.

## How they judged success
Win rate (correct root cause plus enough behaviours) per agent configuration, with and without tool groups; number of behaviours found; for the evaluation agent, fraction of runs whose evaluation distinguishes quirky from baseline models; for red-teaming, number of the ten quirks uncovered.

## What they found
The single investigator won 13% of the time open-ended and 17% when given the meta-rhyme hint, with the most realistic toolset; adding interpretability tools raised win rates by roughly 10 to 20 points from near 0%, partly because features surface relevant pretraining data; semantic search and interpretability were the most useful tools. The super-agent reached 42%. Failure modes: fixating on early hypotheses, rarely using prefill well, rarely using raw sampling. The evaluation agent built a correct evaluation at least once for all ten quirks, in all five runs for seven, and discriminated correctly in 88% of runs overall; failures on subtle quirks (self-promotion, research sandbagging, hardcoding test cases). The red-teaming agent and investigator each found 7 of 10 quirks, missing the same three. On real Claude models the investigator found prefill and context-manipulation jailbreaks but not subtler behaviours like blackmail.

## Limits and open problems they name
The same environment was used for development and testing (possible contamination); implanted behaviours may not resemble natural ones; agents may be poor proxies for expert humans; agents struggle with realistic prompts, subtle behaviours, early fixation, memory management, overconfidence and long-run state tracking.

## What we take from it
A measurement design: score an interpretability tool by the change in success rate of many repeated agent runs with versus without it, from identical starts. This gives a replicable "does it help prediction/auditing" number we could use for components of a white-box model. Also a warning that part of the SAE benefit came via training-data retrieval rather than mechanism, so a data-search baseline is essential.

## Tags
unit: feature | whole-model
form: description
method: agent | SAE | steering
eval: downstream-task | benchmark
goal: safety/auditing | evaluation-of-methods
