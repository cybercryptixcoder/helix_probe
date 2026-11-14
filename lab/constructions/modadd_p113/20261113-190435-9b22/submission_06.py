import numpy as np

DESCRIPTION = """Input [i,j,113] with the third token always the marker 113, so embed.2 is a constant vector.
Attention weights at the last position are essentially uniform (1/3 per position, std 0.001); replacing
them by exactly 1/3 changes the logits by R2 5.4e-6 of their variance and keeps 99.68% of decisions.
So attn_out = (x0+x1+x2)/3 @ (sum_h W_V[h] W_O[h]) and resid_mid = x2 + attn_out is an affine function
of the token pair sum onehot(i)+onehot(j); so is mlp_pre. Output logits are nearly additive in the two
tokens. Variables here: token one-hots at the embed sites, and the pair sum at resid_mid / mlp_pre.
Output is still the placeholder constant."""

def model(x, iv):
    B = x.shape[0]
    oh0 = iv("onehot0", np.eye(114)[x[:, 0].astype(int)])
    oh1 = iv("onehot1", np.eye(114)[x[:, 1].astype(int)])
    ts = iv("tokensum", oh0 + oh1)
    out = np.zeros((B, 113))
    out[:, 39] = 1.0 + 0.0 * ts[:, 0]
    return out

ALIGN = {"onehot0": ["embed.0"], "onehot1": ["embed.1"], "tokensum": ["resid_mid", "mlp_pre"]}
