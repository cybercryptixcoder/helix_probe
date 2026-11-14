import numpy as np

DESCRIPTION = """Task: at each position p=1..5 the network outputs the one-hot of
count_p = #{j in 1..5 : t_j > t_p}. Mechanism: the only nonzero V-output is for
token 4 (the BOS at position 0), so attention at position p adds
attn0.out = w_p * u0 with w_p = attention weight on position 0 = 1/(1+count_p);
attention is exactly uniform over {0} U {greater tokens}. The MLP turns w_p into a
level (relu(base_k + g_k*w_p)), and the residual's logits are the one-hot of that
level (embedding, u0, W_pos and b_out all project to 0 on W_U). The level is
carried by a 4-coordinate code per position (level 4 = all zeros), and the logits
are an affine image of that code, so argmax of [v0,v1,v2,v3,1-sum(v)] decides.
At the embedding the token at each position is a 4-dim one-hot; one variable per
position, since positions are independent parts of the site."""

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    toks = np.zeros((B, 6))
    for p in range(1, 6):
        oh = np.stack([(x[:, p] == t) for t in range(4)], 1).astype(float)
        o = np.asarray(iv("tok%d" % p, oh)).reshape(B, 4)
        toks[:, p] = np.argmax(o, 1)
    cnt = np.zeros((B, 6))
    for p in range(1, 6):
        c = np.zeros(B)
        for j in range(1, 6):
            c = c + (toks[:, j] > toks[:, p])
        cnt[:, p] = c
    inv = np.zeros((B, 6))
    inv[:, 0] = 1.0
    inv[:, 1:] = 1.0 / (1.0 + cnt[:, 1:])
    inv = np.asarray(iv("inv", inv.reshape(B, 6))).reshape(B, 6)
    lev = np.clip(np.round(1.0 / np.maximum(inv, 1e-9) - 1.0), 0, 4).astype(int)
    lvl = np.zeros((B, 20))
    for p in range(5):
        for l in range(4):
            lvl[:, p * 4 + l] = (lev[:, p + 1] == l)
    lvl = np.asarray(iv("lvl", lvl)).reshape(B, 5, 4)
    logits = np.concatenate([lvl, (1.0 - lvl.sum(-1))[:, :, None],
                             np.zeros((B, 5, 1))], -1)
    cls = np.argmax(logits, -1)
    out = np.zeros((B, 30))
    for p in range(5):
        out[np.arange(B), p * 6 + cls[:, p]] = 1.0
    return out

ALIGN = {"tok1": ["embed"], "tok2": ["embed"], "tok3": ["embed"],
         "tok4": ["embed"], "tok5": ["embed"],
         "inv": ["attn0.out", "resid0.mid", "mlp0.pre"],
         "lvl": ["mlp0.post", "mlp0.out", "resid0.post"]}
