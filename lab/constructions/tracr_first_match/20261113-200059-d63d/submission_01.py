import numpy as np

DESCRIPTION = """
Task: at each output position p (1..5) the network says whether token t_p equals token t_1 (class 1 = equal, 0 = not).
embed = W_E[token] + W_pos[pos]; attention at query 0 = self, at queries 1..5 attends to key 1 (position 1).
So attn0.out at position p is (value at position 1) W_O, i.e. an additive function of token t_1 only; MLP then combines it with
the local token t_p to decide equality.
Variable 'e_p' = token one-hot of t_p (5 dims, 4 free) at embed; 'e1' = token one-hot of t_1 used at the attention sites.
"""

def model(x, iv):
    B = x.shape[0]
    tt = x[:, 1:6]                 # t_1..t_5
    onehot = (tt[:, :, None] == np.arange(6)[None, None, :]).astype(float)  # [B,5,6]
    # residual stream at embed (only 6-dim one-hot part named, rest is constant across inputs)
    e = iv("e", onehot.reshape(B, 30))
    t1 = iv("t1", onehot[:, 0, :])           # [B,6] token at position 1
    att = iv("att", np.repeat(t1[:, None, :], 6, axis=1).reshape(B, 36))
    mid = iv("mid", np.concatenate([e, att], axis=1))
    pre = iv("pre", mid)
    post = iv("post", np.maximum(pre, 0))
    mout = iv("mout", post)
    fin = iv("fin", mout)
    # decision: equality of t_p with t_1
    eq = (tt == tt[:, :1]).astype(float)
    return np.stack([1 - eq, eq], axis=-1).reshape(B, 10)

ALIGN = {
    "e": ["embed"],
    "att": ["attn0.out"],
    "mid": ["resid0.mid"],
    "pre": ["mlp0.pre"],
    "post": ["mlp0.post"],
    "mout": ["mlp0.out", "resid0.post"],
}
