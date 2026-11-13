
import numpy as np

DESCRIPTION = """
Placeholder stage-1 probe. The network maps (i, j, 113) -> 113 logits read at the last position;
the majority class is 39 (~40% of the 12,769 inputs). The prediction grid is ~99.8% symmetric in
(i, j) and each row/column takes only ~5.5 distinct values, so the answer is a coarse function of
the pair (i, j). Not yet determined; this submission probes whether the raw token ids i and j are
linearly represented at the embedding sites (they project through W_E, so a low-rank/factored
embedding would make this pass).
"""

def model(x, iv):
    i = iv("tok_i", x[:, 0].astype(float))
    j = iv("tok_j", x[:, 1].astype(float))
    B = x.shape[0]
    logits = np.zeros((B, 113))
    logits[:, 39] = 1.0
    return logits

ALIGN = {"tok_i": ["embed.0"], "tok_j": ["embed.1"]}
