
import numpy as np

DESCRIPTION = ("Task: at content position j the network outputs the rank of its own token, class = #{k: t_k > t_j} "
               "(0 = has the largest token). Stage embedding: position p holds W_E[token]+W_pos[p], linear in a "
               "one-hot of the token. Stage layer-0 attention: Q reads the token value (query value v=min(token,3), BOS "
               "at position 0 has value 4), K is the token one-hot, so the score is 100*[v_key > v_query] and the "
               "softmax is exactly uniform over S_p = {k: v_k > v_p}; |S_p| = 1 + #{k: t_k > t_p} = n_p. V gives 1 on the "
               "BOS only and W_O is rank one, so attention adds o/n_p (o a fixed 19-vector). Stage layer-0 MLP: the "
               "MLP input at position p is affine in g_p = 1/n_p (the token/position part is annihilated by W_in), so "
               "the 12 ReLU neurons see only 1/n_p; their output writes, through W_out and W_U, exactly the one-hot of "
               "class n_p - 1 (W_U annihilates both the embeddings and o).")

def model(x, iv):
    B = x.shape[0]
    val = []
    for p in range(1, 6):
        oh = np.zeros((B, 4))
        oh[np.arange(B), np.clip(x[:, p].astype(int), 0, 3)] = 1.0
        val.append(iv("tok%d" % p, oh) @ np.array([0.0, 1.0, 2.0, 3.0]))
    vals = np.concatenate([np.full((B, 1), 4.0), np.stack(val, 1)], 1)      # [B,6] positions 0..5
    cnt = (vals[:, None, :] > vals[:, :, None]).sum(2)                      # #{k: v_k > v_p}
    n = np.maximum(cnt, 1).astype(float)
    g = iv("ginv", 1.0 / n)                                                 # [B,6] = 1/n_p
    nn = np.clip(np.round(1.0 / g), 1, 6).astype(int)
    out = np.zeros((B, 30))
    for p in range(1, 6):
        c = np.clip(nn[:, p] - 1, 0, 4)
        cls = np.zeros((B, 5))
        cls[np.arange(B), c] = 1.0
        out[:, (p - 1) * 6:(p - 1) * 6 + 5] = iv("cls%d" % p, cls)
    return out

ALIGN = {"tok%d" % p: ["embed"] for p in range(1, 6)}
ALIGN["ginv"] = ["attn0.out", "mlp0.pre"]
for p in range(1, 6):
    ALIGN["cls%d" % p] = ["mlp0.out", "resid0.post"]
