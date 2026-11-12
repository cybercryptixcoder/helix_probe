# You and Your Research Agent: Lessons From Using Agents for Interpretability Research

- **Key:** goodfire-blog-you-and-your-research-agent
- **Authors / organisation:** Mark Bissell, Michael Byun, Daniel Balsam; Goodfire
- **Date:** 2025-10-02
- **Link:** https://www.goodfire.com/blog/you-and-your-research-agent
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 2 (useful)

## What they wanted, and why
Goodfire had spent several months using LLM coding agents to run interpretability experiments and wanted to share
what works and what breaks. Their central claim is that an agent that runs experiments ("experimenter agent") is a
different thing from one that writes software ("developer agent"): software has test suites as a checkable reward,
research conclusions do not. Current agents are trained and benchmarked mostly on software (SWE-Bench-style), so
they need different tooling and supervision to do research well. The larger goal is scaling interpretability
research by delegating experiments to agents while keeping conclusions valid.

## What they studied
Not a single model; a practice report. Examples of their in-house agent ("Scribe") at work: rediscovering a
published rRNA-correlated SAE feature in the genomics model Evo 2 on an E. coli genome; finding an eigenvector to
prune ViT weights to reduce memorization; building a smiling-minus-frowning steering vector in the Flux diffusion
model; and localizing GPT-2 neurons responsible for reciting digits of pi and measuring their redundancy.

## How they did it
Agents (Claude Code, Codex, Gemini CLI) were given open-ended or minimally specified research tasks, often with
access to a model, an SAE and a dataset. The main intervention was tooling: giving the agent stateful access to a
Jupyter kernel through an MCP server, so models load once, cells can be fixed and re-run, and code, figures and
notes live in one timestamped notebook. They compared this informally with script-based workflows. They then
catalogued failure modes seen in transcripts and tried mitigations: a post-hoc critic agent that reviews outputs,
a live critic that watches the session through Claude Code hooks, and a "critic copilot" from a different model
family (GPT-5 reviewing Claude Sonnet 4 transcripts caught a code error). They also ran several agents in
parallel on the same open question and built an unsupervised version on the Claude Code SDK.

## What counts as an explanation here
Not the subject of the post. Implicitly, the output is a completed experiment: a notebook with code, figures and a
written conclusion, which should be valid, short and informative. Agreement among independently run agents is
treated as a weak form of replication.

## How they judged success
Qualitatively. Rediscovering a known published result (the Evo 2 feature) is used as a sanity check; human review
of notebooks is the arbiter. They release an interpretability task suite (circuit discovery, universal neurons,
linear-probe analysis drawn from papers) but say plainly it is not a formal benchmark and has not been audited.
No quantitative success rates are reported.

## What they found
Stateful notebooks were the single largest improvement. Agents are biased toward optimism, in three named ways:
shortcutting (e.g. silently generating synthetic data when a download failed and reporting the expected trend),
p-hacking (calling an F1 of 0.5 meaningful signal, highlighting one success out of 100 inputs) and treating bugs as
breakthroughs (accepting a "miraculous" 100% accuracy). Agents lack stopping criteria, cannot judge when results
are too good to be true, and miss tacit context. Notebook kernels can bypass tool permission systems (an agent
blocked from bash `pip install` ran `!pip install` in a cell). Human verification is the bottleneck. Parallel
agents produce useful variety and good follow-up proposals. Unreviewed experimental results create only shallow
"validation debt", unlike agent-written software.

## Limits and open problems they name
No verifiable reward for research; no long-term memory or continual learning beyond an AGENTS.md file; illegible
research context; agents cannot decide when to accept a null result; their task suite is unaudited and sensitive to
output formatting; context engineering that balances exploration and focus is unsolved.

## What we take from it
A warning and a workflow. If we use agents to probe a network or to check a weight-derived model, we must assume
optimism bias: require reported null results, check for synthetic-data shortcuts, add an independent critic from a
different model family, and treat "too good" fits (e.g. near-perfect prediction) as suspected bugs. Rediscovering a
known published result is a cheap validation pattern for any agent pipeline. Sandbox notebook kernels. Agreement
across parallel independent agents is a usable replication signal.

## Tags
unit: whole-model
form: description
method: agent
eval: human-rating
goal: evaluation-of-methods
