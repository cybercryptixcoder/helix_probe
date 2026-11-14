
import numpy as np

DESCRIPTION = ("The task: at each of the 5 content positions j the network outputs the RANK of its own token, "
               "class = #{k in 1..5 : t_k > t_j} (0 = largest). Verified exactly (100% of 1024 inputs). "
               "Stage 'embedding': each position holds W_E[token]+W_pos[position]; a fixed 5-point set, "
               "so a one-hot code of the token linearly spans it. The model reads the token value off that "
               "one-hot code, compares values across positions and counts how many exceed its own; "
               "later stages are not yet written down.")

def model(x, iv):
    B = x.shape[0]
    oh = []
    for p in range(1, 6):
        v = np.zeros((B, 4))
        v[np.arange(B), np.clip(x[:, p].astype(int), 0, 3)] = 1.0
        oh.append(iv("tok%d" % p, v))
    val = np.stack([v @ np.array([0.0, 1.0, 2.0, 3.0]) for v in oh], 1)   # [B,5]
    out = np.zeros((B, 30))
    for j in range(5):
        cnt = (val > val[:, [j]] + 0.5).sum(1)
        out[np.arange(B), j * 6 + np.minimum(cnt, 5).astype(int)] = 10.0
    return out

ALIGN = {"tok%d" % p: ["embed"] for p in range(1, 6)}
