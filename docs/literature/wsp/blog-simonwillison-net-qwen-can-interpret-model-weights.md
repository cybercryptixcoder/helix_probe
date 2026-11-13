# Qwen 3.8 27B on my laptop can interpret model weights, too

- **Key:** blog-simonwillison-net-qwen-can-interpret-model-weights
- **Authors / organisation:** Simon Willison; independent (simonwillison.net)
- **Date:** 2026-11-03
- **Link:** https://simonwillison.net/2026/Nov/3/qwen-can-interpret-model-weights/
- **Kind:** blog/research post (informal replication)
- **Read from:** full text of the post (via a fetch tool that returns a detailed account rather than raw HTML), plus
  his two linked transcript gists (raw markdown): the Qwen Freeway transcript in full for structure, answer and token
  usage, and the combined Qwen Breakout / Pac-Man / Pong transcript for answers, token usage and durations only (the
  long reasoning traces were skimmed, not read line by line). The Kimi K3.1 Pro gist was not read.
- **Relevance to us:** 3 (central: the only independent re-run of the WSP raw-reading prompts we have, on an open
  model)

## What they wanted, and why
Willison separates two questions that the Sparks post mixes: what a model can do with raw weights and no tools,
and what a model with code can do to edit other models. He focuses on the first, and asks whether a small open model
running locally can repeat the "which game" result. The motivation is to check how special the frontier result is,
and to temper broader commentary about the end of source code.

## What they studied
The four released Exp 1 prompts from the Sparks log repository (PPO policies for Breakout, Pong, Pac-Man and Freeway,
weights as text). Readers: Qwen 3.8 27B, Q4_K_M GGUF quantization (about 17GB) in LM Studio on his laptop; and Kimi
K3.1 Pro via OpenRouter on Breakout only. Unit: whole network.

## How they did it
He passed each released prompt file unchanged to the model with his `llm` command-line tool (fragment option
pointing at the raw GitHub URL). He confirmed the four prompts differ only in their weights. For Qwen he had to load
a longer context than LM Studio's default of 8,192 tokens (the exact length is not stated) and raise the plugin's
timeout. Each game was run once; outputs and reasoning traces are published as gists.

## What counts as an explanation here
The same as in the source: a named game plus a verbal account citing weights.

## How they judged success
Informally, by whether the named game matches the true one. No scorer, no repeats, no controls.

## What they found
Kimi K3.1 Pro named Breakout after 9m 41s and 19,493 reasoning tokens. Qwen named Breakout (Arkanoid-like) at 88%
confidence and Pong at 75%, gave a "Pac-Man-style" maze game at 72% for Pac-Man, and called Freeway a Pac-Man-like
game, so 3 of 4 roughly right. Runs were slow: 46m 12s to 1h 4m 54s for the three in the post, and the Freeway
transcript shows 1h 16m 17s. Willison judges that a patient person with pencil and paper could likely reach the same
answers, and that the traces are long index arithmetic over rows and channels.

## Limits and open problems they name
One run per game, no controls, and he notes Freeway is the most obscure game. He does not claim rigour.

## What we take from it
- Raw text reading of these small policies is **not frontier-only**: a quantized 27B model gets most of it, at about
  30x the wall time. That strengthens the suspicion that Exp 1 is easy because of the prompt and the visitation-map
  structure of first-layer weights, and it gives us a cheap open reader for K1 baselines.
- **Failure to note for K1 design:** in the Freeway transcript Qwen correctly read the evidence (a row of reward
  targets at the top, horizontally moving objects in the middle rows, a strong upward action bias) and still named
  Pac-Man; it reasoned toward a list of famous games it brainstormed from the channel names. The error is in mapping
  evidence to a label, not in reading the weights. Scoring readers on extracted facts (where is the agent, which
  actions matter) separately from the final label would show this.
- Right game, wrong detail: Qwen's Pong answer puts the agent paddle on the right side; our own check of the released
  Pong first-layer weights (not Willison's) shows the agent-channel weight mass concentrated in column 1, the left.

## K1 detail (reading setup)

- **Reader model(s):** Qwen 3.8 27B, Q4_K_M GGUF, local via LM Studio: Breakout correct (88%), Pong correct (75%),
  Pac-Man near-correct ("Pac-Man-style" gridworld, 72%), Freeway wrong (Pac-Man-like, 70% in the transcript).
  Kimi K3.1 Pro via OpenRouter: Breakout correct (confidence not stated in the post). Score for Qwen: 3/4 counting
  the Pac-Man-style answer.
- **Target networks:** the Sparks Exp 1 PPO policies; the post does not restate architecture or size (the source
  gives MLP 500-32-32-5, 17,253 weights).
- **How the weights were presented:** exactly the released Sparks prompts: plain text, 3 decimals, one line per
  matrix row, rows unlabelled. Qwen's tokenizer counted about 104,800 input tokens per prompt (from the transcript
  usage lines). The post's remarks suggest an indexed layout, but the released prompt has no per-line indices; the
  index arithmetic is the model's own.
- **Prompt:** unchanged Sparks Exp 1 prompt (grid and channel description, actions, network formula, open question
  with no candidate list, no tools, answer template); public at
  https://github.com/RikiyaT/lm_understand-logs/tree/main/exp1_which_game .
- **Access regime:** no tools (none provided by the `llm` call), single response; no budget other than context and a
  900-second plugin timeout setting; reasoning used 43,506 to 69,787 tokens per Qwen run (from transcript usage).
- **Controls:** none (no shuffled weights, untrained net, or prompt-only run). One run per game.
- **Failure modes observed:** Freeway misnamed despite correct evidence; detail errors (paddle side); Willison
  reports the model calling the field 8x8, which in fact matches the prompt's inner playable area, so it is not
  clearly an error; very long and hard-to-follow traces; a default 8,192-token context fails outright.
- **Anything about which prompt or format choices helped or hurt:** nothing tested. Implied: the prompt's channel
  names drive the reader's hypothesis list (seen in the Freeway trace); context length is a hard requirement
  (about 105K tokens for a 17K-parameter network in text form).

## Tags
unit: whole-model | weights
form: description
method: agent | weight-analysis
eval: benchmark
goal: evaluation-of-methods
