import numpy as np

DESCRIPTION = """
Behaviour: at output position p (p=1..5) the network says whether token t_p equals token t_1 (class 1 = equal).
Mechanism found so far: embed = W_E[token]+W_pos[pos]. The single attention head has query 0 -> key 0 and queries 1..5 -> key 1
(hard argmax), so attn0.out at positions 1..5 is a fixed affine function of the token at position 1 only, while position 0 is
constant. The residual stream after attention is therefore affine in the 5 token identities. The MLP then forms the
"t_p equals t_1" comparison, which is what the output reads off.
Variables: 'tok' = one-hot code (over the 4 occurring tokens) of t_1..t_5 at each position; 'a1' = the token-1 code
(what attention copies around); 'mid'/'pre' = the residual/MLP-input content (token codes); 'eq' = per-position equality
indicator carried in the MLP output / final residual stream.
"""

def model(x, iv):
    B = x.shape[0]
    tt = x[:, 1:6]
    oh = (tt[:, :, None] == np.array([1., 2., 3., 5.])[None, None, :]).astype(float)  # [B,5,4]
    tok = iv("tok", oh.reshape(B, 20))
    toks = tok.reshape(B, 5, 4)
    a1 = iv("a1", toks[:, 0, :])                 # attention copies token at position 1
    mid = iv("mid", tok)                         # embed + attn: affine in token codes
    pre = iv("pre", mid)                         # MLP input
    post = iv("post", pre)                       # MLP hidden (approximate for now)
    eq = iv("eq", (toks * toks[:, 0:1, :]).sum(-1))   # equality t_p == t_1, from the token codes
    fin = iv("fin", eq)
    return np.stack([1 - fin, fin], axis=-1).reshape(B, 10)

ALIGN = {
    "tok": ["embed"],
    "a1": ["attn0.out"],
    "mid": ["resid0.mid"],
    "pre": ["mlp0.pre"],
    "post": ["mlp0.post"],
    "eq": ["mlp0.out", "resid0.post"],
}
