
DESCRIPTION = """The network computes (i + j) mod 113 where input is [i, j, 113]. First pass: the token embeddings are Fourier features: token t is coded by cos/sin of 2*pi*k*t/113 for a few frequencies k (dominant ones 8, 11, 22, 23, 25). The model builds a score for each output class c by cosine-similarity of the sum-angle features with cos/sin of c."""
import numpy as np, math
n = 113
FREQS = [8, 11, 22, 23, 25]
OUTF = list(range(1, 57))  # placeholder set of output frequencies used for scoring

def _feat(t):
    # t: [B] integer tokens -> [B, 2*len(FREQS)]
    cols = []
    for k in FREQS:
        ang = 2*np.pi*k*t/n
        cols += [np.cos(ang), np.sin(ang)]
    return np.stack(cols, 1)

def model(x, iv):
    i = x[:, 0].astype(np.int64)
    j = x[:, 1].astype(np.int64)
    fa = iv("fourier_i", _feat(i))       # [B, 2F]
    fb = iv("fourier_j", _feat(j))       # [B, 2F]
    ca, sa = fa[:, 0::2], fa[:, 1::2]
    cb, sb = fb[:, 0::2], fb[:, 1::2]
    cab = iv("cos_sum", ca*cb - sa*sb)   # [B, F]
    sab = iv("sin_sum", sa*cb + ca*sb)   # [B, F]
    c = np.arange(n)
    K = np.array(FREQS, dtype=float)[:, None]
    CO = np.cos(2*np.pi*K*c/n)           # [F, n]
    SI = np.sin(2*np.pi*K*c/n)
    score = cab @ CO + sab @ SI
    logits = iv("logits", 10.0*score)
    return logits

ALIGN = {"fourier_i": ["embed.0"], "fourier_j": ["embed.1"]}
