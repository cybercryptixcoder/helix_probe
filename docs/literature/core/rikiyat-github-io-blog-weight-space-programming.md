# Sparks of Weight-Space Programming: LLMs can natively read & write neural network weights

- **Key:** rikiyat-github-io-blog-weight-space-programming
- **Authors / organisation:** Rikiya Takehi, Jayden Teoh, Alex Zhang, Omar Khattab; MIT CSAIL
- **Date:** 2026-11-02
- **Link:** https://rikiyat.github.io/blog/weight-space-programming/
- **Kind:** blog/research post
- **Read from:** full text
- **Relevance to us:** 3 (central)

## What they wanted, and why
Can a general frontier LLM, with no special training, read a network's weights to tell what it does, and write
or edit weights to change what it does, without gradient descent? They call this weight-space programming. The
larger picture they sketch is LLMs acting directly as model engineers: auditing, fixing and building networks by
reasoning over parameters. They describe the results as early "sparks".

## What they studied
One frontier model, referred to as "GPT-6 Astra" (no further detail given), applied to eight tasks on networks
from 17K weights to 0.8B: PPO game policies (MLP 500-32-32-5, 17,253 weights), small DDPM shape generators
(23,824 weights), a 4-block transformer language model (7.16M), a Kinetix car policy (171,664), MinAtar policies
written from zero, a 9x9 Go policy (1.48M), pairs of Gemma 3 270M fine-tunes, and Qwen3.5-0.8B.

## How they did it
Each task fixes what Astra may use. Reading tasks with no tools: weights pasted as text, and Astra names the game
a policy plays or the shape a diffusion model draws. In the transformer task the input and output layers are
removed so it cannot run the model, but Python is allowed to analyse weights; Astra names the training language
and finds copying heads. Writing/editing tasks: fix a failing car policy from one recorded failure episode;
write MinAtar policies from all-zero weights with no data, gradients or rollouts; write a Go policy with a
Python sandbox and 0 or 50 forward passes. Gemma: decide which of two fine-tunes is sycophantic, first from
weights alone, then with a tool showing attention patterns on texts Astra writes. Qwen: with a Python kernel
and 10/25/50 forward passes on practice problems from GSM8K/MATH train sets, edit weights to improve math.
Baselines are PPO-trained networks at various budgets; a Gemma 270M edit serves as a negative control.

## What counts as an explanation here
Mostly the LLM's own verbal account (which game, which heads, which direction causes looping) checked by a
downstream outcome. The edit itself is a test of understanding: if a targeted change produces the predicted
behaviour change, the reading is taken to be right.

## How they judged success
Correct identification out of a small number of cases (4 games, 3 shapes, 3 languages, 3 Gemma pairs); episode
success and game score over 1,000 episodes against PPO at 100M and 500M steps; benchmark accuracy (MATH-500,
GSM8K, IFEval and six more) at temperature 0.6 with multiple samples, plus the rate of hitting the 32,768-token
limit. Access restrictions are the main control; the authors say they checked every run.

## What they found
All four games, three shapes and three languages identified; all copying heads found with no false positives
(confidence 0.48-0.62). The car fix succeeded in 1,024/1,024 episodes after changing 3.5% of weights. Zero-start
MinAtar policies beat PPO-100M in all three games and PPO-500M only on Breakout (517.4 vs 25.3). Gemma
sycophancy: four failures from weights alone; success on all three pairs once attention patterns were allowed.
Qwen3.5-0.8B: Astra traced looping (93% of MATH-500 answers hit the token limit) to one direction written by the
MLPs of layers 15 and 19 and projected it out of 64 columns in each (131,072 weights, 0.016%). With 50 forward
passes MATH-500 went 7.9% to 48.1%, GSM8K 13.8% to 67.1%, IFEval 21.0% to 62.3%; with 10 or 25 passes gains were
small. On Gemma 3 270M (which rarely loops) the same approach gave essentially nothing (6.8% to 7.7%), read as
"editing removes an obstacle, it does not add a skill".

## Limits and open problems they name
Very early; limited by context length and harness. Editing cannot add missing abilities. Gemma reading needed
attention patterns. Seaquest/Asterix below PPO-500M. Modest confidence on the language task. Qwen fix depends on
forward-pass budget. Auditing, unlearning and merging are speculation. Benchmark and harness still in progress.

## What we take from it
This is the closest prior art to reading weights with an LLM, and the main claim we must position against. The
key distinction for us is the access regime: pure raw-weight reading worked only on small MLPs (17K-172K
weights); every real-LM result used Python and/or forward passes (see the critique
honnibal-dev-blog-astra-read-write-misleading and the controlled replication
lesswrong-wnl4nwrs2owzzfwiz-wsp-stratification). Reusable: the "edit as test of a reading" idea (a white-box
claim is validated by a targeted weight edit that changes behaviour as predicted), the access-restriction
protocol, and the negative-control model. Warning: tiny N per task and one proprietary model.

## Tags
unit: weights | direction | head | whole-model
form: description | direction
method: agent | weight-analysis | steering | other
eval: downstream-task | prediction/simulation
goal: control/editing | understanding | safety/auditing
