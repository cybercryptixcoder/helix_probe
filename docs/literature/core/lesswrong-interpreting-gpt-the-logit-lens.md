# Interpreting GPT: the logit lens

- **Key:** lesswrong-interpreting-gpt-the-logit-lens
- **Authors / organisation:** nostalgebraist; independent (LessWrong / Alignment Forum post)
- **Date:** 2020-08
- **Link:** https://www.lesswrong.com/posts/AcKRB8wDpdaN6v6ru/interpreting-gpt-the-logit-lens
- **Kind:** blog/research post
- **Read from:** full text (post and selected comments)
- **Relevance to us:** 2 (useful)

## What they wanted, and why
The author wanted a cheap way to see what a GPT model is "thinking" partway through its forward pass. Because the
output is a linear function of the last layer's activations, and the residual stream keeps a shared basis across
layers, the same output map might be meaningful when applied to intermediate layers. The larger aim is to watch a
prediction form layer by layer, rather than only seeing the final distribution.

## What they studied
Mainly GPT-2 1558M (48 layers, 1600-dim residual stream, 50,257-token vocabulary, tied embeddings). A 2021 edit
extends the analysis to models from 125M to 2.7B, GPT-Neo and CTRL, and to attention and MLP sub-blocks separately.
The unit is the residual stream at each layer, at each token position. Test text was a passage of the GPT-3 abstract
plus some constructed cases (a rare copied token, heavy repetition).

## How they did it
Take each block's output, apply the final layer norm (without its learned affine part), and multiply by the
transposed embedding matrix to get logits over the vocabulary. Display, for every layer and position: the top-1
token with its logit; the rank, at that layer, of the token the final layer ends up ranking first; and
KL(final || layer). An addendum compares each layer with the input instead: KL(input || layer) and the rank of the
current input token. Specific cases are examined: a rare token ("plasma") that is later copied, and repeated text.
No interventions, no training, no baselines.

## What counts as an explanation here
A readout: a per-layer vocabulary distribution, read as the model's provisional guess about the next token. It is a
partial view by design: only information that is expressed as token logits is visible. It describes, it does not
predict behaviour under intervention.

## How they judged success
Qualitative inspection of heatmaps plus three simple quantities: rank of the final top-1 token per layer,
KL(final || layer), and in the addendum KL(input || layer) and rank of the input token. No held-out evaluation,
no statistics.

## What they found
- Early layers give nonsense or context-free guesses; by the middle layers the eventual answer is usually already in
  the top few tokens; later layers refine it.
- Right after the first layer, KL to the final distribution drops sharply and then declines smoothly: the stream
  looks more like the output than the input almost immediately. The author expected a U shape and did not see one.
- A rare token that must be copied ranks low until the very last layers, suggesting it is kept in some other form and
  retrieved late.
- Repetition is picked up only in the upper half of the network.
- Input-token ranks often stay in the hundreds or thousands, so input identity is partly preserved; rarity alone does
  not explain which tokens are kept.

## Limits and open problems they name
Only logit-expressible information is visible. KL is asymmetric, so the "jump" picture depends on direction. Why the
input is discarded so abruptly is unexplained. Commenters note an earlier BERT paper (arXiv 2001.09309) used much the
same idea, and suggest linear probes to reconstruct the input. Later work (tuned lens) shows the lens is biased and
works poorly on some model families.

## What we take from it
- **Method, almost free:** read any residual-stream vector (or any weight column that writes to it) through the
  unembedding. This is the basis of many weight-space readings (e.g. projecting OV circuits or MLP output weights
  onto the vocabulary), so it is a direct tool for reading a network from its weights.
- **Measure:** rank of the final answer and KL(final || layer) per layer give a simple "how far along is the
  prediction" curve that a white-box model's per-layer predictions could be scored against.
- **Warning:** it relies on the residual basis staying aligned with the output space; it misreads early layers and
  models where that fails. Pair it with a learned or causal check before trusting it.

## Tags
unit: layer
form: description
method: other
eval: other (qualitative inspection; rank and KL curves)
goal: understanding
