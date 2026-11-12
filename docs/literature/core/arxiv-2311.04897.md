# Future Lens: Anticipating Subsequent Tokens from a Single Hidden State

- **Key:** arxiv-2311.04897
- **Authors / organisation:** Koyena Pal, Jiuding Sun, Andrew Yuan, Byron C. Wallace, David Bau; Northeastern University, UMass Amherst
- **Date:** 2023-11
- **Link:** https://arxiv.org/abs/2311.04897
- **Kind:** paper
- **Read from:** abstract and sections (arXiv HTML main text)
- **Relevance to us:** 1 (background)

## What they wanted, and why
Language models are trained to predict only the next token, but hidden states may hold more. The authors ask how far ahead a single hidden state (one token, one layer) carries information about the tokens that will come later, and whether that can be decoded. This extends "lens" methods (logit lens, tuned lens) from next-token readouts to multi-token-ahead readouts, toward understanding how much planning-like information a state carries.

## What they studied
GPT-J-6B (28 layers, hidden size 4096). Text from the Pile: about 100,000 tokens to train linear models, 10,000 for the learned prompt, 1,000 for test; only positions where GPT-J's next-token prediction is correct. Unit: one hidden state at one layer and position.

## How they did it
Four decoders predict the token N steps ahead (N = 0 to 3) from one hidden state. (1) A linear map from the hidden state straight to vocabulary logits. (2) A linear map to the model's own final-layer state, then decoded by the model's unembedding (tuned-lens style). (3) Fixed-prompt causal intervention: transplant the hidden state into a run of the model on a generic prompt and see whether the model then generates the original continuation; four fixed prompts. (4) Learned-prompt causal intervention: train a soft prefix of 10 tokens per layer, model frozen, with a KL objective so that the transplanted state makes the model produce the original future tokens. A bigram statistic is the reference baseline. They also build a visualisation ("Future Lens") applying the learned prompt to every state of a prompt.

## What counts as an explanation here
A decoder (lens) that reads predictions of future tokens from a single state, using the model's own later layers as part of the decoder. It shows information is present, not that the model uses it; there is no mechanism.

## How they judged success
Precision@1/5/10 of the actual future token among the decoder's top predictions; surprisal of the decoder's top token under the model; breakdown by model confidence bins, layer, and token type; comparison with bigram and the other decoders.

## What they found
The learned prompt reaches 48.4% precision@1 at N = 1 (best at middle layers, around layer 14), vs 20.8% fixed prompt, 29.2% linear-to-hidden, 27.5% linear-to-vocab, and 20.1% bigram. Averaged, it is about 25% higher in precision@1/5/10 than the best baseline. Accuracy rises with model confidence (26% in the lowest bin to 95% in the highest for N = 1). Within named entities, accuracy is 44%, 42%, 37% at N = 1, 2, 3. The Future Lens figures are qualitative only.

## Limits and open problems they name
No dedicated limitations section. From the text: one model; accuracy under 50%; evaluated only where the model was already right; small test set; the learned prompt is a trained probe, so decodable is not necessarily used; the visualisation is not validated quantitatively.

## What we take from it
(1) A useful framing for prediction targets: a white-box model of a state can be scored on whether it predicts several future outputs, not only the next one. (2) Method: using the frozen model's own downstream layers as the decoder (patching a state into a neutral context) beats pure linear readouts, a reminder that linear lenses underestimate what a state encodes. (3) Warning: optimised decoders blur what the state contains vs what the decoder adds; always include trivial baselines such as bigram statistics.

## Tags
unit: layer
form: probe
method: probing, patching
eval: prediction/simulation, benchmark
goal: understanding, science
