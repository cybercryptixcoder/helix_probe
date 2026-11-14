import numpy as np

DESCRIPTION = """
Behaviour: at output position p (p=1..5) the network says whether token t_p equals token t_1 (class 1 = equal, class 0 = not).
Mechanism: embed = W_E[token]+W_pos[pos]. The single attention head has query 0 -> key 0 and queries 1..5 -> key 1
(hard argmax), so attn0.out at positions 1..5 is a fixed affine function of the token at position 1 only; position 0 is
constant. Hence every residual stream content is affine in the token identities: position p holds its own token t_p and,
carried by attention, the reference token t_1. The MLP compares the two per position (equality) and the output reads off
that comparison.
Variables: 'tok<p>' = one-hot code of t_p at embed; 'a1' = the reference token code that attention copies to every
position; 'mid<p>' = the token identity present at position p after attention (position 1 holds the reference);
'pre<p>' = the same token identities at the MLP input; 'eq' = per-position equality indicator carried by the MLP output
and the final residual stream, which the unembedding turns into the two class scores.
"""

TOKS = np.array([1., 2., 3., 5.])

def model(x, iv):
    B = x.shape[0]
    tt = x[:, 1:6]
    oh = (tt[:, :, None] == TOKS[None, None, :]).astype(float)          # [B,5,4] one-hot codes
    tok = np.stack([iv("tok%d" % p, oh[:, p, :]) for p in range(5)], 1)  # [B,5,4]
    a1 = iv("a1", tok[:, 0, :])                                         # attention copies token at position 1
    mid = np.stack([iv("mid0", a1)] +
                   [iv("mid%d" % p, tok[:, p, :]) for p in range(1, 5)], 1)
    pre = np.stack([iv("pre0", mid[:, 0, :])] +
                   [iv("pre%d" % p, mid[:, p, :]) for p in range(1, 5)], 1)
    eq = iv("eq", (pre * pre[:, 0:1, :]).sum(-1))                       # t_p equals t_1
    return np.stack([1 - eq, eq], axis=-1).reshape(B, 10)

ALIGN = {
    "tok0": ["embed"], "tok1": ["embed"], "tok2": ["embed"], "tok3": ["embed"], "tok4": ["embed"],
    "a1": ["attn0.out"],
    "mid0": ["resid0.mid"], "mid1": ["resid0.mid"], "mid2": ["resid0.mid"], "mid3": ["resid0.mid"], "mid4": ["resid0.mid"],
    "pre0": ["mlp0.pre"], "pre1": ["mlp0.pre"], "pre2": ["mlp0.pre"], "pre3": ["mlp0.pre"], "pre4": ["mlp0.pre"],
    "eq": ["mlp0.out", "resid0.post"],
}
