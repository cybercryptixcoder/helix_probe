import numpy as np

DESCRIPTION = """Established: input is [i,j,113] with the third token always the marker 113, so embed.2 is a
constant vector. Attention weights at the last position are essentially uniform (1/3 on each position,
variation ~0.001), so attn_out = (x0+x1+x2)/3 @ M. The output logits are symmetric and additive in the
two tokens: out(i,j) ~ c + g(i) + g(j), only ~18 of the 113 classes ever win (39 most often).
Here: variables for the embed sites are the one-hot token codes (embedding = W_E[t] + W_pos[p], a linear
function of the one-hot); output is still the placeholder constant."""

def model(x, iv):
    B = x.shape[0]
    oh0 = iv("onehot0", np.eye(114)[x[:, 0].astype(int)])
    oh1 = iv("onehot1", np.eye(114)[x[:, 1].astype(int)])
    out = np.zeros((B, 113))
    out[:, 39] = 1.0 + 0.0 * oh0[:, 0] + 0.0 * oh1[:, 0]
    return out

ALIGN = {"onehot0": ["embed.0"], "onehot1": ["embed.1"]}
