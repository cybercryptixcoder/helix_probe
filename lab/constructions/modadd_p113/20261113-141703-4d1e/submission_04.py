
import numpy as np
DESCRIPTION = ("Input is [i, j, 113]; the network computes (i+j) mod 113. Each token is embedded as a clock "
               "(Fourier) code over Z_113 with the dominant frequencies 8,11,23,25 plus weaker harmonics; attention at "
               "the last position produces an additive sum f(i)+g(j) of the two tokens' clock codes. The MLP multiplies "
               "the i-code by the j-code frequency by frequency (product-to-sum), giving the clock code cos/sin(2*pi*k*s/113) "
               "of s=(i+j)%113, and the unembedding scores class c with sum_k w_k*cos(2*pi*k*(c-s)/113), peaked at c=s.")

K = [8, 23, 11, 25, 22, 16, 46, 50]
NF = len(K)
WJ = np.array([1.51, 1.12, 0.90, 0.81, 0.0, 0.0, 0.0, 0.0])
CO = np.cos(2.0 * np.pi * np.outer(np.arange(113), K) / 113.0)
SO = np.sin(2.0 * np.pi * np.outer(np.arange(113), K) / 113.0)

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
    ci, si = va[:, 0::2], va[:, 1::2]
    cj, sj = vb[:, 0::2], vb[:, 1::2]
    sf = np.empty((x.shape[0], 2 * NF))
    sf[:, 0::2] = ci * cj - si * sj
    sf[:, 1::2] = si * cj + ci * sj
    sf = iv("sf", sf)
    return (sf[:, 0::2] * WJ) @ CO.T + (sf[:, 1::2] * WJ) @ SO.T

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"],
         "va": ["attn_out", "resid_mid"], "vb": ["attn_out", "resid_mid"],
         "sf": ["mlp_post", "mlp_out", "resid_post"]}
