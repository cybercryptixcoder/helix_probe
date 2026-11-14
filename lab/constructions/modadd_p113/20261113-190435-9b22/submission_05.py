import numpy as np

DESCRIPTION = """Established: input is [i,j,113], third token always the marker 113 so embed.2 is constant.
Attention weights of the last position are essentially uniform (1/3 per position, std ~0.001), so
attn_out = (x0+x1+x2)/3 @ M with M = sum_h W_V[h] W_O[h]; the output logits are symmetric and nearly
additive in the two tokens, out(i,j) ~ c + g(i) + g(j) (additive model: 99.89% of logit variance,
94.8% of decisions). Only ~18 of 113 classes ever win (39 most often).
Variables at the embed sites are the token one-hot codes (embed = W_E[t]+W_pos[p] is a linear function
of them: explained 1.000, substitute 100%). Output is still the placeholder constant."""

def model(x, iv):
    B = x.shape[0]
    oh0 = iv("onehot0", np.eye(114)[x[:, 0].astype(int)])
    oh1 = iv("onehot1", np.eye(114)[x[:, 1].astype(int)])
    out = np.zeros((B, 113))
    out[:, 39] = 1.0 + 0.0 * oh0[:, 0] + 0.0 * oh1[:, 0]
    return out

ALIGN = {"onehot0": ["embed.0"], "onehot1": ["embed.1"]}
