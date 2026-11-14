import numpy as np

DESCRIPTION = """Task: at each position p=1..5 the network outputs the one-hot of
count_p = #{j in 1..5 : t_j > t_p}. Mechanism: the only nonzero V-output is for
token 4 (the BOS at position 0), so attention at position p returns
attn0.out = w_p * u0 with w_p = attention weight on position 0 = 1/(1+count_p).
QK depends on tokens only (b_Q=b_K=0 and W_pos projects to 0) and gives scores
100*[t_j > t_p] (and 100 for token4->token4), so the attention is exactly uniform
over {0} U {greater tokens}. The MLP turns w_p into a one-hot of the count through
thresholds relu(base_k + g_k*w_p), and the residual's logits equal that one-hot
(the embedding, u0, W_pos and b_out all project to 0 on W_U). So the decision at p
is the level of w_p, i.e. count_p."""

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
    qm = tok @ S                      # [B,6pos,5] query vector per position
    sc = (qm * tok).sum(-1)           # score(p,j) = qm_p . k_j
    sc = sc - sc.max(-1, keepdims=True)
    Aw = np.exp(sc)
    Aw = Aw / Aw.sum(-1, keepdims=True)
    w = (Aw * tok[:, :, 4]).sum(-1)   # weight of the token-4 value u0
    inv = np.asarray(iv("inv", w)).reshape(B, 6)
    lev = np.clip(np.round(1.0 / np.maximum(inv, 1e-9) - 1.0), 0, 4).astype(int)
    lvl = np.zeros((B, 25))
    for p in range(5):
        lvl[np.arange(B), p * 5 + lev[:, p]] = 1.0
    lvl = np.asarray(iv("lvl", lvl)).reshape(B, 5, 5)
    cls = lvl.argmax(-1)
    out = np.zeros((B, 30))
    for p in range(5):
        out[np.arange(B), p * 6 + cls[:, p]] = 1.0
    return out

ALIGN = {"tok": ["embed"],
         "inv": ["attn0.out", "resid0.mid", "mlp0.pre"],
         "lvl": ["mlp0.post", "mlp0.out", "resid0.post"]}
