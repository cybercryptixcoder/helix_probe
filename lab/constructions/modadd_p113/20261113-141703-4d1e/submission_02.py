
import numpy as np
DESCRIPTION = ("The network computes (i+j) mod 113 for input [i, j, 113]. Tokens are embedded in a low-rank Fourier "
               "(clock) basis over Z_113 with frequencies {8,11,23,25}: token t contributes cos/sin pairs. The last "
               "position's attention splits additively into a term f(i) (from position 0) and g(j) (from position 1), "
               "so the residual carries the two phases. The MLP forms the products of the phases, giving the clock "
               "features of the sum s=(i+j)%113, and the unembedding scores class c by cos(2*pi*k*(c-s)/113) so the "
               "peak is at c=s.")

K = [8, 11, 23, 25]
INV8 = 99.0
W_K = [1.51, 0.90, 1.12, 0.81]

def feats(t):
    t = np.asarray(t, dtype=float)
    cols = []
    for k in K:
        a = 2.0 * np.pi * k * t / 113.0
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, 1)

def rec8(e):
    # recover token t from the (cos,sin) pair at frequency 8 : 8t mod 113
    ph = np.arctan2(e[:, 1], e[:, 0]) / (2.0 * np.pi)
    v = np.mod(ph * 113.0, 113.0)
    return np.mod(np.round(v * INV8), 113.0).astype(int)

def model(x, iv):
    e0 = iv("e0", feats(x[:, 0]))
    e1 = iv("e1", feats(x[:, 1]))
    i = rec8(e0)
    j = rec8(e1)
    va = iv("va", feats(i))
    vb = iv("vb", feats(j))
    s = (i + j) % 113
    sf = iv("sf", feats(s))
    s2 = rec8(sf)
    d = ((np.arange(113)[None, :] - s2[:, None]) % 113).astype(float)
    L = np.zeros_like(d)
    for k, w in zip(K, W_K):
        L = L + w * np.cos(2.0 * np.pi * k * d / 113.0)
    return L

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"],
         "va": ["attn_out", "resid_mid"], "vb": ["attn_out", "resid_mid"],
         "sf": ["mlp_post", "mlp_out", "resid_post"]}
