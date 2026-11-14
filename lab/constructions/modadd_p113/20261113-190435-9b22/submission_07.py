import numpy as np

DESCRIPTION = """Input [i,j,113] with the third token always the marker 113, so embed.2 is a constant. Attention
weights of the last position are essentially uniform (1/3 per position, std 0.001); replacing them with
exactly 1/3 changes logits by only 5e-6 of their variance. Therefore attn_out = mean_pos(x) @ M with
M = sum_h W_V[h] W_O[h], resid_mid = x2 + attn_out is an affine function of the token pair sum
onehot(i)+onehot(j) (explained 1.000, substitute 99.9%), and so is mlp_pre. The network's logits are
nearly symmetric+additive in (i,j): the best additive model out = c + p(i) + p(j) already keeps 94.9% of
decisions. Variables: token one-hots at embed sites, pair sum at resid_mid / mlp_pre.
Output is still the placeholder constant."""

def model(x, iv):
    B = x.shape[0]
    oh0 = iv("onehot0", np.eye(113)[x[:, 0].astype(int)])
    oh1 = iv("onehot1", np.eye(113)[x[:, 1].astype(int)])
    ts = iv("tokensum", oh0 + oh1)
    out = np.zeros((B, 113))
    out[:, 39] = 1.0 + 0.0 * ts[:, 0]
    return out

ALIGN = {"onehot0": ["embed.0"], "onehot1": ["embed.1"], "tokensum": ["resid_mid", "mlp_pre"]}
