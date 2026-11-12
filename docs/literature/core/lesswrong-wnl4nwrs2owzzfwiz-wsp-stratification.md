# What do LLMs Really Learn About Model Weights? A Stratification Approach to Examine Weight Space Programming

- **Key:** lesswrong-wnl4nwrs2owzzfwiz-wsp-stratification
- **Authors / organisation:** CCaptainX (pseudonymous); LessWrong post
- **Date:** 2026-11-08
- **Link:** https://lesswrong.com/posts/WnL4nWrS2owzZfwiz/what-do-llms-really-learn-about-model-weights-a
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
The Sparks post reported that an LLM could name which game a PPO policy was trained on from its raw weights.
This replication asks which signal the LLM actually uses: the weight values, or the prompt's metadata (channel
names, priors about likely answers). The aim is to separate genuine weight reading from label reading and
default guessing.

## What they studied
Two reader LLMs: GPT-6 Astra (medium reasoning, temperature 1) and DeepSeek-V4.1-Flash (temperature 0.7). Targets:
the same four PPO policies (Breakout, Pong, Pac-Man, Freeway; 17,253 weights; 10x10 input over 5 channels, W1 about
16,000 values, W3 about 160) and the byte-identical prompt, taken from the original public logs.

## How they did it
"Stratification": rerun the task under variants that each remove or corrupt one source of signal. Real (original);
Shuffled (same values, random positions); No weight (prompt only); Anonymous channels (descriptive channel names
replaced by numbers); Untrained (random init weights); Layer sweep (only W1 or only W3); Random 1000 (1,000 weights
kept, rest zeroed); Top-50 per channel (250 largest weights). 15 samples per game per condition (60 per variant).
Answers are scored as correct, incorrect/default, or refusal.

## What counts as an explanation here
Attribution of a reader's success to an input source, by controlled removal. Not an explanation of the target
networks.

## How they judged success
Accuracy with Wilson 95% confidence intervals; refusal counts; rate of the most common default answer in
no-signal conditions (shuffled, no-weight, untrained) as a measure of prior-driven guessing.

## What they found
Baseline: Astra 4/4 games, Flash 3/4. Astra stayed accurate without channel labels, with W1 only (about 100%), W3
only (about 62%) and 1,000 random weights; Flash dropped substantially without labels and to about 30-40% with
single layers (difference not significant). With untrained weights Astra refused; Flash named a game in 14/60.
Shuffled: Astra refused 52/60 (1 correct), Flash refused 39/60 with 5 "correct" Pac-Man answers. In no-signal
conditions Flash answered Pac-Man about 78.6% of the time, so its apparent hits partly come from that default.
Conclusion: Flash leans on prompt metadata; Astra appears to use weight content and refuses when there is none.

## Limits and open problems they name
N=15 per condition (API cost); only the four original tasks; only two readers; no open-weight models. Whether
Astra's W1 > W3 gap reflects reading input vs output weights or just W1's larger size is untested.

## What we take from it
A ready-made control battery for any weight-reading claim, which we should copy: shuffled weights (same marginal
statistics, destroyed structure), untrained weights, prompt-only, anonymised labels, layer subsets and sparsified
weights. Also: measure the reader's default/prior answer rate under no signal, and report refusals separately.
Shows that the reader matters as much as the network: two LLMs with similar headline accuracy can rely on
completely different evidence.

## Tags
unit: weights | layer
form: other
method: ablation | weight-analysis | other
eval: ablation | benchmark
goal: evaluation-of-methods
