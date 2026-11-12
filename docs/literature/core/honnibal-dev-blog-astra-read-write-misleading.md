# The "Astra can read and write weights to improve Qwen" post is misleading (critique of weight-space programming)

- **Key:** honnibal-dev-blog-astra-read-write-misleading
- **Authors / organisation:** Matthew Honnibal; independent blog
- **Date:** 2026-11-03
- **Link:** https://honnibal.dev/blog/astra-read-write-misleading
- **Kind:** essay
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
A short audit of how the "Sparks of Weight-Space Programming" results were presented. Honnibal argues that the
headline combines results from quite different methods so that readers infer one capability (reading and
writing raw weights with no tools and no running of the network) that only some experiments show. The goal is
accurate reporting of what was actually demonstrated.

## What they studied
The eleven experiments (counting sub-variants) of the Sparks post, tabulated by network size, read vs write,
Python use and whether the network was run.

## How they did it
No new experiments. He classifies each experiment by access regime: only experiments 1, 2 and 4 involve reading
raw weights with no Python, all on networks of 17K-172K weights. Every experiment on a real language model uses
Python, and the Qwen headline also runs the model on up to 50 batches of practice problems. He adds caveats from
the post itself: the car fix had a recorded failure episode; the zero-start MinAtar task has nothing to read and
beat PPO-500M only on Breakout; Gemma reading failed without attention patterns.

## What counts as an explanation here
Not applicable directly; the essay is about what counts as evidence for "reading weights". Implicitly: a claim of
reading weights requires that the result came from weights alone, with tool use and model execution disclosed
and separated.

## How they judged success
By consistency between the abstract's claims and each experiment's actual setup.

## What they found
The results are real and impressive, but the Qwen improvement shows an LLM doing what a human ML engineer does
with code and forward passes, not reading raw weights natively. Raw-weight results and Python-assisted results
should be reported separately. He concedes that doing this productively is notable and that models a year or two
earlier would have failed.

## Limits and open problems they name
No experiments of his own; he does not test whether raw reading scales. He leaves open what the raw-weight
capability actually is at LM scale.

## What we take from it
A reporting rule we should adopt: for every claim about reading weights, state the access regime (raw weights
only / weights plus code / weights plus forward passes / plus outputs) and never pool results across regimes. Our
own experiments should include a weights-only arm and a matched arm with tools or execution, so we can say how
much comes from each. This is the main methodological objection a reviewer will raise against weight-reading
claims.

## Tags
unit: weights | whole-model
form: other
method: other
eval: other
goal: evaluation-of-methods
