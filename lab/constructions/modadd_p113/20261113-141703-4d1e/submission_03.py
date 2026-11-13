
import numpy as np
DESCRIPTION = ("Input is [i, j, 113]; the network computes (i+j) mod 113. Tokens live in a low-rank Fourier (clock) "
               "basis over Z_113 with frequencies {8,11,23,25}. At the last position attention produces an additive "
               "term f(i) (from position 0) + g(j) (position 1), each proportional to the token's clock features "
               "cos/sin(2*pi*k*t/113). The MLP multiplies the two clock features frequency-by-frequency "
               "(product-to-sum) producing the clock of the sum s=(i+j)%113, and the unembedding scores class c by "
               "w_k*cos(2*pi*k*(c-s)/113), whose peak is at c=s.")

K = [8, 11, 23, 25]
W_K = [1.51, 0.90, 1.12, 0.81]
CO = np.cos(2.0 * np.pi * np.outer(np.arange(113), K) / 113.0)   # [113,4]
SO = np.sin(2.0 * np.pi * np.outer(np.arange(113), K) / 113.0)   # [113,4]

def feats(t):
    t = np.asarray(t, dtype=float)
    cols = []
    for k in K:
        a = 2.0 * np.pi * k * t / 113.0
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, 1)

def model(x, iv):
    e0 = iv("e0", feats(x[:, 0]))
    e1 = iv("e1", feats(x[:, 1]))
    va = iv("va", e0)
    vb = iv("vb", e1)
    # product-to-sum : clock features of the sum, frequency by frequency
    ci, si = va[:, 0::2], va[:, 1::2]
    cj, sj = vb[:, 0::2], vb[:, 1::2]
    cs = ci * cj - si * sj
    ss = si * cj + ci * sj
    sf = np.empty((x.shape[0], 8))
    sf[:, 0::2] = cs
    sf[:, 1::2] = ss
    sf = iv("sf", sf)
    L = (sf[:, 0::2] @ (CO * np.array(W_K)).T) + (sf[:, 1::2] @ (SO * np.array(W_K)).T)
    return L

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"],
         "va": ["attn_out", "resid_mid"], "vb": ["attn_out", "resid_mid"],
         "sf": ["mlp_post", "mlp_out", "resid_post"]}
