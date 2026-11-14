
import numpy as np

DESCRIPTION = ("First submission, embedding stage only. The residual stream at each of the 6 positions is "
               "W_E[token]+W_pos[pos], i.e. an affine function of the token one-hot at that position, so the "
               "embedding site is spanned by the six token one-hots (one per position). The rest of the network "
               "is not yet modelled; the output block is a placeholder.")

def model(x, iv):
    B = x.shape[0]
    ar = np.arange(B)
    ohs = []
    for p in range(6):
        v = np.zeros((B, 6))
        v[ar, x[:, p]] = 1.0
        ohs.append(iv("tok%d" % p, v))
    emb = np.concatenate(ohs, axis=1)
    iv("embed", emb)
    return np.zeros((B, 10))

ALIGN = {"embed": ["embed"]}
