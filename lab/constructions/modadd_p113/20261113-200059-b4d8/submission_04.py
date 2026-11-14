
DESCRIPTION = """The network computes (i + j) mod 113 where input is [i, j, 113] (113 is a fixed '=' token). Token embeddings are Fourier features: token t is coded by cos/sin of 2*pi*k*t/113 for k = 8, 11, 22, 23, 25. The residual stream at the last position after attention holds the (i)-features and (j)-features side by side (additive, ~92% of variance); the MLP turns them into products / sum-angle features cos,sin of k*(i+j); the unembedding scores class c by cosine similarity with those."""
import numpy as np, math
n = 113
FREQS = [8, 11, 22, 23, 25]

def _feat(t):
    cols = []
    for k in FREQS:
        ang = 2*np.pi*k*t/n
        cols += [np.cos(ang), np.sin(ang)]
    return np.stack(cols, 1)

def model(x, iv):
    i = x[:, 0].astype(np.int64)
    j = x[:, 1].astype(np.int64)
    fa = iv("fourier_i", _feat(i))
    fb = iv("fourier_j", _feat(j))
    ca, sa = fa[:, 0::2], fa[:, 1::2]
    cb, sb = fb[:, 0::2], fb[:, 1::2]
    cab = iv("cos_sum", ca*cb - sa*sb)
    sab = iv("sin_sum", sa*cb + ca*sb)
    c = np.arange(n)
    K = np.array(FREQS, dtype=float)[:, None]
    CO = np.cos(2*np.pi*K*c/n)
    SI = np.sin(2*np.pi*K*c/n)
    score = cab @ CO + sab @ SI
    logits = iv("logits", 10.0*score)
    return logits

ALIGN = {"fourier_i": ["embed.0", "resid_mid"], "fourier_j": ["embed.1", "resid_mid"]}
