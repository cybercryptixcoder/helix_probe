import numpy as np

DESCRIPTION = """Task: at each position p=1..5 the network outputs the one-hot of
count_p = #{j in 1..5 : t_j > t_p}. Mechanism: the only nonzero V-output is for
token 4 (the BOS at position 0), so attention at position p returns
attn0.out = w_p * u0 with w_p = attention weight on position 0 = 1/(1+count_p).
QK depends on tokens only (b_Q=b_K=0, W_pos projects to 0, k_t = e_t and
q_t = 100*sum_{s allowed(t)} e_s with allowed(t) = {s>t} or {4} for t>=4), so the
attention is exactly uniform over {0} U {greater tokens}. The MLP turns w_p into a
level through thresholds relu(base_k + g_k*w_p) and the residual's logits are that
one-hot (embedding, u0, W_pos and b_out all project to 0 on W_U). The level is held
by a 4-coordinate code per position (level 4 = all zeros); the logits are the affine
image of that code, so argmax of [v0,v1,v2,v3,1-sum(v)] is the decision."""

def model(x, iv):
    x = np.asarray(x, dtype=float)
    B = x.shape[0]
    oh = np.zeros((B, 6, 5))
    for p in range(6):
        for t in range(5):
            oh[:, p, t] = (x[:, p] == t)
    tok = np.asarray(iv("tok", oh.reshape(B, 30))).reshape(B, 6, 5)
    S = np.array([[0., 100., 100., 100., 100.],
                  [0., 0., 100., 100., 100.],
                  [0., 0., 0., 100., 100.],
                  [0., 0., 0., 0., 100.],
                  [0., 0., 0., 0., 100.]])
    qm = tok @ S                                   # [B,6,5] query vectors
    sc = qm @ tok.transpose(0, 2, 1)               # [B,6q,6j] scores
    sc = sc - sc.max(-1, keepdims=True)
    Aw = np.exp(sc)
    Aw = Aw / Aw.sum(-1, keepdims=True)
    w = (Aw * tok[:, :, 4][:, None, :]).sum(-1)    # [B,6] weight on the token-4 value
    inv = np.asarray(iv("inv", w)).reshape(B, 6)
    lev = np.clip(np.round(1.0 / np.maximum(inv, 1e-9) - 1.0), 0, 4).astype(int)
    lvl = np.zeros((B, 20))
    for p in range(5):
        for l in range(4):
            lvl[:, p * 4 + l] = (lev[:, p + 1] == l)
    lvl = np.asarray(iv("lvl", lvl)).reshape(B, 5, 4)
    logits = np.concatenate([lvl, (1.0 - lvl.sum(-1))[:, :, None],
                             np.zeros((B, 5, 1))], -1)
    cls = logits.argmax(-1)
    out = np.zeros((B, 30))
    for p in range(5):
        out[np.arange(B), p * 6 + cls[:, p]] = 1.0
    return out

ALIGN = {"tok": ["embed"],
         "inv": ["attn0.out", "resid0.mid", "mlp0.pre"],
         "lvl": ["mlp0.post", "mlp0.out", "resid0.post"]}
