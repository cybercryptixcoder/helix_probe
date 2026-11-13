
import numpy as np
DESCRIPTION = ("The network computes (i+j) mod 113 where the input is [i, j, 113]. Tokens are embedded in a "
               "low-dimensional Fourier (clock) basis with frequencies ~{8,11,22,23,25} over Z_113; the last "
               "position attends to positions 0 and 1 to combine the two clock phases into the phase of the sum; "
               "the MLP/unembedding turn that phase into logits peaked at class s=(i+j)%113.")

FREQ = [8, 11, 22, 23, 25]

def feats(t):
    cols = []
    for k in FREQ:
        a = 2.0 * np.pi * k * t / 113.0
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, 1)

def phase_from(e):
    ph = np.arctan2(e[:, 1], e[:, 0]) / (2.0 * np.pi)
    return np.mod(np.round(ph * 113.0 / 8.0), 113.0)

def feats_s(s):
    cols = []
    for k in [8, 11, 23, 25]:
        a = 2.0 * np.pi * k * s / 113.0
        cols.append(np.cos(a)); cols.append(np.sin(a))
    return np.stack(cols, 1)

def model(x, iv):
    e0 = iv("e0", feats(x[:, 0]))
    e1 = iv("e1", feats(x[:, 1]))
    i = phase_from(e0).astype(int)
    j = phase_from(e1).astype(int)
    s = (i + j) % 113
    sm = iv("sum", feats_s(s.astype(float)))
    d = ((np.arange(113)[None, :] - s[:, None]) % 113).astype(float)
    L = np.zeros_like(d)
    for k, w in zip([8, 11, 23, 25], [1.5, 0.9, 1.12, 0.8]):
        L = L + w * np.cos(2.0 * np.pi * k * d / 113.0)
    return L

ALIGN = {"e0": ["embed.0"], "e1": ["embed.1"], "sum": ["attn_out", "resid_mid"]}
