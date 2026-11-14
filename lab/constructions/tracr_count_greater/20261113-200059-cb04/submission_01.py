
import numpy as np

DESCRIPTION = ("Placeholder-first construction. Stage 'embedding': at each position the residual stream is "
               "W_E[token] + W_pos[position]; since token 0's position always holds token 4 (constant), each of the "
               "5 content positions is a fixed 5-point set, i.e. an affine function of a one-hot code of its token. "
               "So the embed site is explained by five 4-dim one-hot variables.")

def model(x, iv):
    B = x.shape[0]
    vs = []
    for p in range(1, 6):
        oh = np.zeros((B, 4))
        oh[np.arange(B), np.clip(x[:, p].astype(int), 0, 3)] = 1.0
        vs.append(iv("tok%d" % p, oh))
    # output placeholder: not yet explained
    return np.zeros((B, 30))

ALIGN = {"tok%d" % p: ["embed"] for p in range(1, 6)}
