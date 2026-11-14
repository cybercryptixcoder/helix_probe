
import numpy as np

DESCRIPTION = ("Task: at content position j the network outputs the rank of its own token, class = #{k: t_k > t_j}. "
               "Stage embedding: each position holds W_E[token]+W_pos[position], linear in a one-hot of the token. "
               "Stage layer-0 attention: Q/K compare token values (query value = min(token,3), key value = token, BOS at "
               "position 0 has value 4); scores are 100*[v_key > v_query] so the softmax is exactly uniform over "
               "S_p = {k : v_k > v_p}, |S_p| = 1 + #{k in 1..5: t_k > t_p} for p>=1. V and W_O are rank one: V gives 1 "
               "exactly on the BOS position, so the attention output at position p is o/|S_p| for one fixed 19-vector o. "
               "The six numbers 1/|S_p| are the whole content of the attention output; class = 1/(1/g) - 1.")

def model(x, iv):
    B = x.shape[0]
    val = []
    for p in range(1, 6):
        v = np.zeros((B, 4))
        v[np.arange(B), np.clip(x[:, p].astype(int), 0, 3)] = 1.0
        val.append(iv("tok%d" % p, v) @ np.array([0.0, 1.0, 2.0, 3.0]))
    vals = np.concatenate([np.full((B, 1), 4.0), np.stack(val, 1)], 1)      # [B,6] positions 0..5
    cnt = (vals[:, None, :] > vals[:, :, None]).sum(2)                      # cnt[b,p] = #{k: v_k > v_p}
    g = iv("ginv", np.where(cnt > 0, 1.0 / np.maximum(cnt, 1), 1.0))        # [B,6] = 1/|S_p|
    out = np.zeros((B, 30))
    cls = np.clip(np.round(1.0 / g[:, 1:]) - 1.0, 0, 5).astype(int)
    for j in range(5):
        out[np.arange(B), j * 6 + cls[:, j]] = 1.0
    return out

ALIGN = {"tok%d" % p: ["embed"] for p in range(1, 6)}
ALIGN["ginv"] = ["attn0.out"]
