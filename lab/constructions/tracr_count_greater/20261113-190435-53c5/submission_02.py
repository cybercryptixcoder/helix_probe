import numpy as np

DESCRIPTION = """The task: at each position p=1..5 output the one-hot of
count_p = #{j in 1..5 : t_j > t_p}. Mechanism: (1) position 0 (BOS token 4) is the
only token whose V-projection is nonzero, so attention at position p averages a single
fixed vector u0 over the set {0} U {greater tokens}, giving attn0.out = u0/(1+count_p).
(2) The MLP's W_in rows see only that same direction plus a token-independent offset
(W_pos and tokens 0..3 project to zero), so mlp0.pre[p,k] = a_k + g_k/(1+count_p);
the ReLU+W_out turn those thresholds into the one-hot of the count, and the residual
carries the count level to the output."""

def model(x, iv):
    B = x.shape[0]
    oh = np.zeros((B, 6, 5))
    for p in range(6):
        for t in range(5):
            oh[:, p, t] = (x[:, p] == t)
    tok = iv("tok", oh.reshape(B, 30))
    w = tok.reshape(B, 6, 5)
    num = (w * np.arange(5)[None, None, :]).sum(2)
    den = w.sum(2) + 1e-30
    ti = num / den                                    # token index per position [B,6]
    t = ti[:, 1:]
    cnt = (t[:, None, :] > t[:, :, None]).sum(-1).astype(float)   # [B,5]
    inv = iv("inv", 1.0 / (1.0 + cnt))
    cnt = np.round(1.0 / np.maximum(inv, 1e-6) - 1.0)             # [B,5]
    lv = np.clip(np.round(cnt).astype(int), 0, 4)
    lvl = np.zeros((B, 25))
    for p in range(5):
        lvl[np.arange(B), p * 5 + lv[:, p]] = 1.0
    lvl = iv("lvl", lvl)
    v = lvl.reshape(B, 5, 5)
    lev = (v * np.arange(5)[None, None, :]).sum(2) / (v.sum(2) + 1e-30)
    out = np.zeros((B, 30))
    for p in range(5):
        c = np.clip(np.round(lev[:, p]).astype(int), 0, 5)
        out[np.arange(B), p * 6 + c] = 1.0
    return out

ALIGN = {"tok": ["embed", "resid0.mid", "resid0.post"],
         "inv": ["attn0.out", "resid0.mid", "mlp0.pre", "resid0.post"],
         "lvl": ["mlp0.post", "mlp0.out", "resid0.post"]}
