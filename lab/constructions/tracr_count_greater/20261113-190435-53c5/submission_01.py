import numpy as np

DESCRIPTION = "Output at each position p in 1..5 is the number of tokens among positions 1..5 that are strictly greater than the token at p; the network's output is the one-hot of that count. Construction: read the tokens, form their counts (multiset), and the per-position count of larger tokens, then one-hot it."

def model(x, iv):
    B = x.shape[0]
    # token one-hots for all 6 positions, tokens 0..4 (pos 0 is always the BOS token 4)
    oh = np.zeros((B, 6, 5))
    for p in range(6):
        for t in range(5):
            oh[:, p, t] = (x[:, p] == t)
    tok = iv("tok", oh.reshape(B, 30))
    multi = iv("multi", np.stack([(x[:, 1:] == t).sum(1) for t in range(5)], 1).astype(float))
    t = x[:, 1:].astype(float)
    cnt = iv("cnt", (t[:, None, :] > t[:, :, None]).sum(-1).astype(float))
    out = np.zeros((B, 30))
    for p in range(5):
        c = np.clip(np.round(cnt[:, p]).astype(int), 0, 5)
        out[np.arange(B), p * 6 + c] = 1.0
    return out

ALIGN = {"tok": ["embed"], "multi": ["attn0.out", "resid0.mid"], "cnt": ["mlp0.pre", "mlp0.post", "resid0.post"]}
