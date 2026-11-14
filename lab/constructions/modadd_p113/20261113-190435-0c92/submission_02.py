
import numpy as np, math
DESCRIPTION = """The net computes (i+j) mod 113 for inputs [i, j, 113]. Tokens are embedded with
Fourier features of the token index at frequencies 8, 11, 22, 23, 25 (the embedding matrix is
essentially rank 10 with exactly these five frequencies). Attention at the last position mixes
the i and j embeddings, the MLP produces cos/sin of f*(i+j), and the readout turns those into
logits peaked at (i+j) mod 113. Here every stage is expressed through the variables, so a
replacement of a variable propagates."""
FR = [8, 11, 22, 23, 25]
N = 113.0

def feats(t):
    t = np.asarray(t, dtype=float)
    cols = []
    for k in FR:
        a = 2*math.pi*k*t/N
        cols += [np.cos(a), np.sin(a)]
    return np.stack(cols, 1)

def rec(F):
    # recover token index from Fourier features via circular mean over frequencies
    acc = 0.0; w = 0.0
    for n_, k in enumerate(FR):
        ang = np.arctan2(F[:, 2*n_+1], F[:, 2*n_])
        est = ang*N/(2*math.pi*k)
        acc = acc + est*k; w = w + k
    return np.mod(acc/w, N)

def model(x, iv):
    i = x[:, 0].astype(float); j = x[:, 1].astype(float)
    ci = iv("ci", feats(i))
    cj = iv("cj", feats(j))
    i1 = rec(ci); j1 = rec(cj)
    mid = iv("mid", np.hstack([feats(i1), feats(j1)]))
    i2 = rec(mid[:, :10]); j2 = rec(mid[:, 10:])
    tot = iv("tot", feats(i2 + j2))
    s = rec(tot)
    s = s - (s > N/2)*N
    d = (s[:, None] - np.arange(113)[None, :])
    lg = np.zeros_like(d)
    for k in FR:
        lg = lg + np.cos(2*math.pi*k*d/N)
    return lg

ALIGN = {"ci": ["embed.0"], "cj": ["embed.1"], "mid": ["resid_mid"], "tot": ["mlp_post", "resid_post"]}
